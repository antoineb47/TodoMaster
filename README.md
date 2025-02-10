# TodoMaster

## Description
TodoMaster is a production-ready Django web application for todo management with secure user authentication, responsive UI, and automated tests.

## Tech Stack
- Python/Django
- Bootstrap
- SQLite (development) / PostgreSQL (production)
- Docker
- GitHub Actions
- Pytest

## Features
- User registration/login/logout
- Todo CRUD (create, update, delete, mark complete)
- Filtering
- Responsive menus

## Security
- Uses Django authentication
- CSRF protection
- Secure sessions
- .env for sensitive settings

## Deployment
- Docker & Docker Compose configured for one-step deployment in GitHub Codespaces.

## Installation and Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd TodoMaster
   ```

2. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```

3. Access the application at `http://localhost:8000`.

## CI/CD
- GitHub Actions configured for automated tests and deployment.

## Testing
- Automated tests for models, views, and forms using Pytest.

## Documentation
- Inline code comments and clear developer documentation included.
