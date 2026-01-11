# Deployment Files

This directory contains all files needed for containerization and deployment of the BookGram API.

## Files

### `Containerfile`
Multi-stage container image definition optimized for Podman/Docker:
- **Stage 1 (Builder)**: Installs dependencies using `uv`
- **Stage 2 (Runtime)**: Minimal production image running as non-root user
- Includes health check endpoint monitoring
- Exposes port 8000

### `compose.yaml`
Podman-compose/Docker-compose configuration for local development and production deployment:
- **db service**: PostgreSQL 16 Alpine with persistent volume
- **api service**: BookGram FastAPI application
- Configured with health checks and automatic restarts
- Uses bridge network for service communication

## Usage

### Using Podman Compose

From the project root directory:

```bash
# Start all services
podman-compose -f deploy/compose.yaml up -d

# View logs
podman-compose -f deploy/compose.yaml logs -f

# Stop services
podman-compose -f deploy/compose.yaml down

# Stop and remove volumes
podman-compose -f deploy/compose.yaml down -v
```

### Using Docker Compose

```bash
# Start all services
docker-compose -f deploy/compose.yaml up -d

# View logs
docker-compose -f deploy/compose.yaml logs -f

# Stop services
docker-compose -f deploy/compose.yaml down
```

### Manual Build

```bash
# Build from project root
podman build -t bookgram-api:latest -f deploy/Containerfile .

# Or with Docker
docker build -t bookgram-api:latest -f deploy/Containerfile .
```

## Environment Variables

The `compose.yaml` includes default environment variables for local development. For production:

1. Copy `.env.example` to `.env` in the project root
2. Update the values, especially:
   - `SECRET_KEY` - Use a secure random string (min 32 chars)
   - `DATABASE_URL` - Update if using external PostgreSQL
   - `DEBUG` - Set to `False` in production

## Security Notes

- The container runs as non-root user (`bookgram`, UID 1000)
- PostgreSQL credentials in `compose.yaml` are for local development only
- Always use strong passwords and secrets in production
- Consider using secrets management for sensitive values

## Kubernetes Deployment

For Kubernetes deployment, consider:
- Converting `compose.yaml` using `kompose`
- Creating separate manifests for ConfigMaps and Secrets
- Using Persistent Volume Claims for the database
- Implementing proper health checks and resource limits
