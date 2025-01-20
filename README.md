<div align="center">
  <div style="background: linear-gradient(45deg, #2193b0, #6dd5ed); padding: 20px; border-radius: 15px; margin: 20px 0;">
    <h1 style="color: white; font-size: 3em; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">🚀 FastAPI Modular Application</h1>
  </div>

  <div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin: 20px 0;">
    <a href="https://www.python.org" style="text-decoration: none;">
      <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    </a>
    <a href="https://fastapi.tiangolo.com" style="text-decoration: none;">
      <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
    </a>
    <a href="https://www.docker.com" style="text-decoration: none;">
      <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
    </a>
  </div>

  <div style="background: linear-gradient(135deg, #1a1a1a, #2d2d2d); color: white; padding: 25px; border-radius: 15px; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
    <h2 style="color: #60d9fa; margin-top: 0;">🛠️ Base Tech Stack</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; text-align: left;">
      <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
        <h3 style="color: #60d9fa; margin: 0;">Core</h3>
        <ul style="list-style-type: none; padding: 0; margin: 10px 0;">
          <li>🐍 Python 3.8+</li>
          <li>⚡ FastAPI Framework</li>
          <li>🔄 Uvicorn ASGI server</li>
        </ul>
      </div>
      <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
        <h3 style="color: #60d9fa; margin: 0;">Project Structure</h3>
        <ul style="list-style-type: none; padding: 0; margin: 10px 0;">
          <li>📊 Modular Architecture</li>
          <li>📝 API Versioning</li>
          <li>🔍 Scalable Structure</li>
        </ul>
      </div>
      <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
        <h3 style="color: #60d9fa; margin: 0;">Development</h3>
        <ul style="list-style-type: none; padding: 0; margin: 10px 0;">
          <li>🐳 Docker & Compose</li>
          <li>🔄 Hot Reload</li>
          <li>📊 API Documentation</li>
        </ul>
      </div>
    </div>
  </div>

  <div style="background: linear-gradient(135deg, #000428, #004e92); color: white; padding: 25px; border-radius: 15px; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
    <h2 style="color: #60d9fa; margin-top: 0;">✨ Base Features</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; text-align: left;">
      <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
        <h3 style="color: #60d9fa; margin-top: 0;">📦 API Versioning</h3>
        <p>Clean API versioning system for better maintainability and backwards compatibility.</p>
      </div>
      <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
        <h3 style="color: #60d9fa; margin-top: 0;">🔄 Async Support</h3>
        <p>Built with async/await patterns for optimal performance.</p>
      </div>
      <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
        <h3 style="color: #60d9fa; margin-top: 0;">🎯 Modular Design</h3>
        <p>Structured for easy scaling and maintenance of your application.</p>
      </div>
    </div>
  </div>
</div>

# Project Overview

This project demonstrates a modular FastAPI setup with versioned routes, user management, item management, and math operations.

## Structure

- **/backend/app/main.py**  
  FastAPI application entry point. Configures CORS, includes routers, and handles startup/shutdown events.
- **/backend/app/api**  
  Contains separate controllers for different routes and versions (API V1 and API V2).

## Getting Started

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:

   ```bash
   uvicorn app.main:app --reload
   ```

3. Access documentation at:

   ```bash
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

### Deployment

1. Build and run containers:

   ```bash
   docker-compose up --build -d
   ```

2. Access the application at:

   ```bash
   http://127.0.0.1:8000
   ```

## Contributing

- Fork the repository.
- Create a feature branch.
- Submit merge requests with clear descriptions.
