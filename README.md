<div align="center">

# 🚀 FastAPIBase: Modular FastAPI Application Template

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-20.10+-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com)

A production-ready FastAPI project template with 3-layer architecture, API versioning, and comprehensive repository patterns.

</div>

## 🛠️ Technology Stack

<details open>
<summary><b>Core Technologies</b></summary>
<br>

<div align="center">

| Category | Technologies |
|----------|-------------|
| 🐍 **Core** | Python 3.8+, FastAPI, Uvicorn ASGI, Pydantic |
| 🗄️ **Database** | SQLAlchemy ORM, MySQL, Alembic Migrations |
| 📦 **Architecture** | 3-Layer Design, Repository Pattern, Unit of Work |
| 🌐 **API** | REST API, Versioned Endpoints (v1/v2), OpenAPI Documentation |
| 🛠️ **Development** | Docker & Docker Compose, Environment Configuration |
| 📊 **Validation** | Pydantic Models, Type Hints, Request/Response Models |
| 🧪 **Error Handling** | Custom Exception Classes, Global Exception Handlers |

</div>
</details>

## ✨ Key Features

<table>
<tr>
    <td align="center">🏛️ <b>3-Layer Architecture</b><br>Clean separation between Controllers, Services, and Repositories</td>
    <td align="center">📦 <b>API Versioning</b><br>Future-proof API evolution with /v1 and /v2 endpoints</td>
    <td align="center">🔄 <b>Async Support</b><br>High-performance asynchronous request handling</td>
</tr>
<tr>
    <td align="center">🧩 <b>Repository Pattern</b><br>Type-safe database operations with unit of work</td>
    <td align="center">📝 <b>Pydantic Schemas</b><br>Strict validation for request/response models</td>
    <td align="center">🐳 <b>Docker Integration</b><br>Containerized development and deployment</td>
</tr>
<tr>
    <td align="center">🔍 <b>OpenAPI Docs</b><br>Auto-generated Swagger UI documentation</td>
    <td align="center">🛡️ <b>Exception Handling</b><br>Comprehensive error management</td>
    <td align="center">🧪 <b>Health Checks</b><br>Built-in application and database monitoring</td>
</tr>
</table>

## 🏗️ Project Structure

```
├── backend/                      # Backend application
│   ├── app/
│   │   ├── main.py               # Application entry point
│   │   ├── controllers/          # API controllers (route handlers)
│   │   │   ├── v1/               # API version 1 controllers
│   │   │   └── v2/               # API version 2 controllers
│   │   ├── core/                 # Core application components
│   │   │   └── config.py         # Configuration settings
│   │   ├── db/                   # Database components
│   │   │   ├── base.py           # Database connection setup
│   │   │   └── models/           # SQLAlchemy ORM models
│   │   ├── repositories/         # Data access layer
│   │   │   ├── base_repository.py                # Base repository implementation
│   │   │   ├── repository_interface/             # Repository interfaces
│   │   │   │   └── i_base_repository.py          # Base repository interface
│   │   ├── schemas/              # Pydantic data models
│   │   │   ├── business_model/   # Business logic models
│   │   │   └── view_model/       # Request/response models
│   │   ├── services/             # Business logic layer
│   │   │   ├── service_interface/# Service interfaces
│   │   │   ├── services/         # Service implementations
│   │   │   └── utils/            # Utility functions and exception handlers
│   │   └── unit_of_work/         # Unit of Work pattern implementation
│   ├── Dockerfile                # Docker configuration for backend
│   └── requirements.txt          # Python dependencies
├── frontend/                     # Frontend application (placeholder)
└── docker-compose.yml            # Docker Compose configuration
```

## 🚀 Quick Start

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd FastAPIBase
   ```

2. **Setup Environment Variables**
   ```bash
   # Create/edit .env file in the backend directory
   cp backend/.env.example backend/.env
   # Edit backend/.env with your database credentials
   ```

3. **Run with Docker Compose**
   ```bash
   docker compose up --build -d
   ```

4. **Access Swagger API Documentation**
   ```
   http://127.0.0.1:8000/docs
   ```

<details>
<summary>📘 <b>Development Setup</b></summary>

### Local Development Setup

1. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Available API Endpoints

- **Health Check**: `GET /health`
- **Database Test**: `GET /test-db`
- **API Versions**:
  - v1: `/api/v1/...`
  - v2: `/api/v2/...`

</details>

## 🧩 Architecture

This project implements a classic 3-layer architecture:

1. **Controller Layer** (Presentation)
   - Handles HTTP requests and responses
   - Input validation and response formatting
   - Route definitions and API documentation

2. **Service Layer** (Business Logic)
   - Implements business rules and workflows
   - Orchestrates repository operations
   - Handles error handling and exceptions

3. **Repository Layer** (Data Access)
   - Database operations and queries
   - Data mapping between entities and models
   - Transaction management with Unit of Work pattern

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a pull request

<div align="center">

---
<sub>Created by Minh An | Last Updated: 2024</sub>

</div>
