"""Test books CRUD endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book import Book


@pytest.mark.asyncio
async def test_create_book(client: AsyncClient) -> None:
    """Test creating a new book."""
    book_data = {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "isbn": "9780743273565",
        "description": "A classic American novel",
        "published_year": 1925,
    }

    response = await client.post("/api/v1/books", json=book_data)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == book_data["title"]
    assert data["author"] == book_data["author"]
    assert data["isbn"] == book_data["isbn"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_list_books_empty(client: AsyncClient) -> None:
    """Test listing books when database is empty."""
    response = await client.get("/api/v1/books")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []
    assert data["page"] == 1
    assert data["pages"] == 0


@pytest.mark.asyncio
async def test_list_books_with_data(
    client: AsyncClient,
    test_db_session: AsyncSession,
) -> None:
    """Test listing books with data."""
    # Create test books
    book1 = Book(
        title="Book 1",
        author="Author 1",
        isbn="1234567890123",
    )
    book2 = Book(
        title="Book 2",
        author="Author 2",
        isbn="1234567890124",
    )
    test_db_session.add_all([book1, book2])
    await test_db_session.commit()

    response = await client.get("/api/v1/books")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2
    assert data["page"] == 1
    assert data["pages"] == 1


@pytest.mark.asyncio
async def test_get_book(
    client: AsyncClient,
    test_db_session: AsyncSession,
) -> None:
    """Test getting a specific book."""
    # Create test book
    book = Book(
        title="Test Book",
        author="Test Author",
        isbn="9876543210987",
    )
    test_db_session.add(book)
    await test_db_session.commit()
    await test_db_session.refresh(book)

    response = await client.get(f"/api/v1/books/{book.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book.id
    assert data["title"] == book.title
    assert data["author"] == book.author


@pytest.mark.asyncio
async def test_get_book_not_found(client: AsyncClient) -> None:
    """Test getting a non-existent book."""
    response = await client.get("/api/v1/books/99999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_update_book(
    client: AsyncClient,
    test_db_session: AsyncSession,
) -> None:
    """Test updating a book."""
    # Create test book
    book = Book(
        title="Original Title",
        author="Original Author",
    )
    test_db_session.add(book)
    await test_db_session.commit()
    await test_db_session.refresh(book)

    update_data = {"title": "Updated Title"}
    response = await client.patch(f"/api/v1/books/{book.id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["author"] == "Original Author"


@pytest.mark.asyncio
async def test_update_book_not_found(client: AsyncClient) -> None:
    """Test updating a non-existent book."""
    update_data = {"title": "Updated Title"}
    response = await client.patch("/api/v1/books/99999", json=update_data)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_book(
    client: AsyncClient,
    test_db_session: AsyncSession,
) -> None:
    """Test deleting a book."""
    # Create test book
    book = Book(
        title="Book to Delete",
        author="Test Author",
    )
    test_db_session.add(book)
    await test_db_session.commit()
    await test_db_session.refresh(book)
    book_id = book.id

    response = await client.delete(f"/api/v1/books/{book_id}")

    assert response.status_code == 204

    # Verify book is deleted
    get_response = await client.get(f"/api/v1/books/{book_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_book_not_found(client: AsyncClient) -> None:
    """Test deleting a non-existent book."""
    response = await client.delete("/api/v1/books/99999")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_books_pagination(
    client: AsyncClient,
    test_db_session: AsyncSession,
) -> None:
    """Test books list pagination."""
    # Create 15 test books
    books = [
        Book(title=f"Book {i}", author=f"Author {i}", isbn=f"123456789012{i}") for i in range(15)
    ]
    test_db_session.add_all(books)
    await test_db_session.commit()

    # Test first page
    response = await client.get("/api/v1/books?page=1&size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 15
    assert len(data["items"]) == 10
    assert data["page"] == 1
    assert data["pages"] == 2

    # Test second page
    response = await client.get("/api/v1/books?page=2&size=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 5
    assert data["page"] == 2
