# Project Overview

This project demonstrates a modular FastAPI setup with versioned routes, user management, item management, and math operations.

## Structure

- **/backend/app/main.py**  
  FastAPI application entry point. Configures CORS, includes routers, and handles startup/shutdown events.
- **/backend/app/api**  
  Contains separate controllers for different routes and versions (API V1 and API V2).

## Getting Started

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the application:
   ```
   uvicorn app.main:app --reload
   ```
3. Access documentation at:
   ```
   http://127.0.0.1:8000/docs
   ```

## Additional Details

### Architecture
- Organized into logical modules (routes, services, schemas).
- Versioned APIs (API V1 and API V2).
- Controllers manage specific application areas (users, items, math).

### Modules
- app: Holds the core application, including main.py and configs.
- api: Contains different FastAPI routers for versioned endpoints.
- services: Contains business logic for users, items, and math.
- schemas: Defines request/response Pydantic models.

### Testing
Use pytest or any preferred framework:
```bash
pytest
```

### Deployment
- Production server recommendation: Gunicorn with Uvicorn workers.
- Example:
```bash
gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
```

## Contributing

- Fork the repository.
- Create a feature branch.
- Submit merge requests with clear descriptions.
