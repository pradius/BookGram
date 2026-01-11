"""SaveFile API endpoint."""

from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.services.file_service import FileService
from app.services.user_service import UserService

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/save", response_model=str, status_code=status.HTTP_201_CREATED)
async def save_file(
    db: Annotated[AsyncSession, Depends(get_db)],
    file: UploadFile = File(..., description="Text file to upload (supports compressed/chunks)"),
    title: str = Form(..., description="Title for the file (will be normalized as topic)"),
    user_id: int = Form(..., description="User ID for subscription"),
) -> str:
    """
    Save a file and subscribe user to the topic.

    **Business Logic:**
    1. **File Service:**
       - Validates the file (non-empty, text format)
       - Saves file to disk
       - Creates file record in database with metadata
    2. **User Service:**
       - Subscribes the user to the topic

    **Returns:** Topic string (normalized title)
    """
    # Validation: Check for empty title
    if not title or not title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title cannot be empty",
        )

    # Validation: Check for empty or corrupted file
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File name is required",
        )

    # Read file content
    try:
        file_content = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read file: {str(e)}",
        ) from e

    # Validation: Check if file is empty
    if not file_content or len(file_content) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty or corrupted",
        )

    # Normalize title to topic
    topic = FileService.normalize_topic(title)

    # Get file extension
    file_format = FileService.get_file_extension(file.filename)

    # Validate file format (text formats only)
    allowed_formats = ["txt", "md", "log", "pdf", "epub"]
    if file_format not in allowed_formats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format. Allowed formats: {', '.join(allowed_formats)}",
        )

    try:
        # Save file to disk
        location_url = await FileService.save_file_to_disk(
            file_content=file_content,
            topic=topic,
            file_extension=file_format,
        )

        # Create file record in database
        file_record = await FileService.create_file_record(
            db=db,
            location_url=location_url,
            topic=topic,
            size=len(file_content),
            file_format=file_format,
        )

        # Subscribe user to topic
        await UserService.subscribe_user_to_topic(
            db=db,
            user_id=user_id,
            topic=topic,
        )

        # Commit transaction
        await db.commit()

        # Return topic string
        return file_record.topic

    except ValueError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}",
        ) from e
