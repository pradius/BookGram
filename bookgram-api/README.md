# BookGram API

A production-ready FastAPI application for managing short books summary videos, built with modern Python best practices.

## 🚀 Tech Stack

- **Framework**: FastAPI with Python >= 3.9
- **Database**: PostgreSQL with SQLAlchemy 2.0 (async)
- **Dependency Management**: `uv` for fast, reliable Python package management
- **Linting & Formatting**: Ruff (replaces Black, isort, flake8)
- **Type Checking**: Pyright (integrated with Ruff)
- **Testing**: Pytest with httpx AsyncClient
- **Containerization**: Podman (Containerfile + compose.yaml)
- **Migrations**: Alembic for database schema management

## 📁 Project Structure

```
bookgram-api/
├── app/
│   ├── api/              # API route handlers
│   │   ├── v1/          # API v1 endpoints
│   │   │   └── books.py # Books CRUD endpoints
│   │   └── health.py    # Health check endpoint
│   ├── core/            # Core configuration
│   │   └── config.py    # Pydantic Settings
│   ├── db/              # Database setup
│   │   └── session.py   # Async session management
│   ├── models/          # SQLAlchemy models
│   │   └── book.py      # Book entity
│   ├── schemas/         # Pydantic schemas
│   │   └── book.py      # Book request/response models
│   ├── services/        # Business logic layer
│   │   └── book.py      # Book service
│   └── main.py          # Application entry point
├── tests/               # Test suite
│   ├── conftest.py      # Pytest fixtures
│   ├── test_health.py   # Health check tests
│   └── test_books.py    # Books CRUD tests
├── alembic/             # Database migrations
│   └── versions/        # Migration scripts
├── deploy/              # Deployment & containerization
│   ├── Containerfile    # Podman/Docker image definition
│   └── compose.yaml     # Multi-container setup
├── pyproject.toml       # Project dependencies & config
└── README.md            # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- Python >= 3.9
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- PostgreSQL (or use Podman for containerized setup)

### Local Development Setup

1. **Clone the repository**
   ```bash
   cd bookgram-api
   ```

2. **Install uv (if not already installed)**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start PostgreSQL** (if running locally)
   ```bash
   # Using Podman
   podman run -d \
     --name bookgram-db \
     -e POSTGRES_USER=bookgram \
     -e POSTGRES_PASSWORD=bookgram \
     -e POSTGRES_DB=bookgram \
     -p 5432:5432 \
     postgres:16-alpine
   ```

6. **Run database migrations**
   ```bash
   uv run alembic upgrade head
   ```

7. **Start the development server**
   ```bash
   uv run uvicorn app.main:app --reload
   ```

   The API will be available at: `http://localhost:8000`
   
   Interactive API docs: `http://localhost:8000/docs`

## 🐳 Production Deployment with Podman

### Using Podman Compose (Recommended)

This method starts both the API and PostgreSQL database:

```bash
# Build and start all services (from project root)
podman-compose -f deploy/compose.yaml up -d

# View logs
podman-compose -f deploy/compose.yaml logs -f

# Stop services
podman-compose -f deploy/compose.yaml down

# Stop and remove volumes (data will be lost)
podman-compose -f deploy/compose.yaml down -v
```

The API will be available at: `http://localhost:8000`

### Manual Podman Build

```bash
# Build the image
podman build -t bookgram-api:latest -f deploy/Containerfile .

# Run the container (ensure PostgreSQL is running)
podman run -d \
  --name bookgram-api \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql+asyncpg://bookgram:bookgram@db:5432/bookgram \
  -e SECRET_KEY=your-production-secret-key \
  -e DEBUG=False \
  bookgram-api:latest
```

## 🧪 Testing

### Run all tests
```bash
uv run pytest
```

### Run with coverage
```bash
uv run pytest --cov=app --cov-report=html
```

### Run specific test file
```bash
uv run pytest tests/test_books.py -v
```

### Run with verbose output
```bash
uv run pytest -vv
```

## 📝 API Endpoints

### Health Check
- `GET /health` - Health check endpoint (verifies DB connectivity)

### Books CRUD (API v1)
- `GET /api/v1/books` - List all books (with pagination)
- `GET /api/v1/books/{id}` - Get a specific book
- `POST /api/v1/books` - Create a new book
- `PATCH /api/v1/books/{id}` - Update a book
- `DELETE /api/v1/books/{id}` - Delete a book

## 🔧 Development Tools

### Code Formatting & Linting
```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check --fix .
```

### Type Checking
```bash
uv run pyright
```

### Database Migrations

```bash
# Create a new migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Rollback last migration
uv run alembic downgrade -1

# View migration history
uv run alembic history
```

## ⚙️ Configuration

Configuration is managed through environment variables (see `.env.example`):

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | BookGram |
| `APP_VERSION` | Application version | 0.1.0 |
| `DEBUG` | Enable debug mode | False |
| `ENVIRONMENT` | Environment (development/production) | production |
| `DATABASE_URL` | PostgreSQL connection string | postgresql+asyncpg://... |
| `SECRET_KEY` | Secret key for security (change in production!) | - |
| `API_V1_PREFIX` | API v1 prefix | /api/v1 |
| `ALLOWED_HOSTS` | CORS allowed hosts | ["*"] |

## 🏗️ Architecture Highlights

### Modern FastAPI Patterns
- ✅ **APIRouter** for modular route organization
- ✅ **Lifespan events** for startup/shutdown logic
- ✅ **Annotated dependencies** with type hints
- ✅ **Pydantic V2** for data validation

### Database Layer
- ✅ **SQLAlchemy 2.0** async engine
- ✅ **Async sessions** with proper transaction handling
- ✅ **Alembic migrations** for schema versioning
- ✅ **Service layer** pattern for business logic

### Security & Best Practices
- ✅ **Non-root user** in containers
- ✅ **Multi-stage builds** for smaller images
- ✅ **Health checks** for container orchestration
- ✅ **Dependency injection** for testability
- ✅ **Type hints** throughout codebase

### Testing
- ✅ **Pytest-asyncio** for async test support
- ✅ **Test database isolation** with fixtures
- ✅ **AsyncClient** for realistic API testing
- ✅ **Coverage reporting** integrated

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests and linting (`uv run pytest && uv run ruff check .`)
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [uv](https://github.com/astral-sh/uv)
- Database migrations with [Alembic](https://alembic.sqlalchemy.org/)
- Code quality with [Ruff](https://github.com/astral-sh/ruff)

---

**Happy Coding! 📚✨**
