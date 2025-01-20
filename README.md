<div align="center">

# 🚀 FastAPI Modular Application

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-20.10+-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
[![GitHub](https://img.shields.io/badge/GitHub-Modular_FastAPI-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com)

A scalable FastAPI project template with modular architecture and API versioning.

</div>

## 🛠️ Tech Stack

<details open>
<summary>Core Technologies</summary>
<br>

<div align="center">

| Category | Technologies |
|----------|-------------|
| 🐍 Core | Python 3.8+, FastAPI, Uvicorn ASGI |
| 📦 Structure | Modular Architecture, API Versioning |
| 🛠️ Development | Docker & Compose, Hot Reload, Swagger UI |

</div>

</details>

## ✨ Features


<table>
<tr>
    <td align="center">📦 <b>API Versioning</b><br>Clean and maintainable version control</td>
    <td align="center">🔄 <b>Async Support</b><br>Built for high performance</td>
    <td align="center">🎯 <b>Modular Design</b><br>Scalable architecture</td>
</tr>
</table>


## 🏗️ Project Structure
```
├───backend
│   └───app
│       ├───api
│       │   ├───api_v1
│       │   └───api_v2
│       ├───core
│       │   └───__pycache__
│       ├───db
│       │   ├───models
│       │   └───__pycache__
│       ├───repositories
│       ├───schemas
│       ├───services
│       │   ├───services
│       │   └───utils
│       └───unit_of_work
└───frontend
```

## 🚀 Quick Start

1. **Clone and Install**
   ```bash
   git clone <repository-url>
   pip install -r requirements.txt
   ```

2. **Run Development Server**
   ```bash
   docker compose up --build -d
   ```

3. **View API Documentation**
   ```
   http://127.0.0.1:8000/docs
   ```

<details>
<summary>📚 Additional Details</summary>

### Architecture
- Modular organization (routes, services, schemas)
- Version-controlled API endpoints
- Clean separation of concerns

### Deployment
```bash
docker-compose up --build -d
```
Access at: `http://127.0.0.1:8000`

</details>

## 🤝 Contributing
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

<div align="center">

---
<sub>⭐ Star this repository if you found it helpful!</sub>

</div>
