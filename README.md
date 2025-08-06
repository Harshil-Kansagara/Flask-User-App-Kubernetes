# Flask User Management Microservice

A scalable Flask-based REST API microservice for user management with PostgreSQL database, containerized with Docker and deployable on Kubernetes.

## Features

- **RESTful API** for user management (CRUD operations)
- **PostgreSQL** database integration with SQLAlchemy ORM
- **Docker containerization** for consistent deployment
- **Kubernetes deployment** with StatefulSet for database persistence
- **Swagger/OpenAPI documentation** for API exploration
- **Sample data initialization** for quick testing
- **Database migrations** support with Flask-Migrate

## Table of Contents

- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Docker Deployment](#docker-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Development](#development)
- [Demo Video](#demo-video)

## Architecture

The application follows a microservice architecture with the following components:

- **Flask Application**: REST API service running on port 5000
- **PostgreSQL Database**: Data persistence layer running on port 5432
- **Docker Containers**: Containerized application and database
- **Kubernetes Cluster**: Orchestrated deployment with auto-scaling and self-healing

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Kubernetes cluster (local or cloud)
- kubectl configured

### Local Development with Docker Compose

1. **Clone the repository**
  
   ```bash
   git clone https://github.com/Harshil-Kansagara/Flask-User-App-Kubernetes.git
   cd flask-user-microservice
   ```

2. **Start the application**

   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - API Documentation: <http://localhost:5000/>
   - API Base URL: <http://localhost:5000/api>

## API Documentation

### Base URL

- **Local Development**: `http://localhost:5000` (root redirects to Swagger UI)
  - Swagger UI: `http://localhost:5000/`
  - API endpoints: `http://localhost:5000/api/*`
- **Kubernetes (Ingress)**: `http://user-app.flask.com` (requires hosts file entry and ingress setup)
  - Swagger UI: `http://user-app.flask.com/`
  - API endpoints: `http://user-app.flask.com/api/*`

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | Get all users (supports department filter) |
| GET | `/api/users/{id}` | Get user by ID |
| POST | `/api/users` | Create new user |
| GET | `/` | Swagger UI documentation |

## Docker Deployment

### Docker Hub Repository

**Docker Image**: `harshilkansagara/flask_user_app:latest`

## Kubernetes Deployment

### Deploy to Kubernetes

1. **Apply namespace and secrets**

   ```bash
   kubectl apply -f k8s-secret.yml
   ```

2. **Deploy ConfigMap**

   ```bash
   kubectl apply -f k8s-configmap.yml
   ```

3. **Deploy PostgreSQL StatefulSet**

   ```bash
   kubectl apply -f k8s-postgresql-statefulset-deployment.yml
   ```

4. **Deploy Flask Application**

   ```bash
   kubectl apply -f k8s-flask-deployment.yml
   ```

5. **Setup Ingress**

   ```bash
   kubectl apply -f k8s-ingress.yml

### Verify Deployment

```bash
# Check all resources
kubectl get all -n flask-user-app-dev-namespace

# Check pods status
kubectl get pods -n flask-user-app-dev-namespace

# Check services
kubectl get svc -n flask-user-app-dev-namespace

# Check persistent volumes
kubectl get pv,pvc -n flask-user-app-dev-namespace
```

## Development

### Project Structure

```text
flask-user-microservice/
├── app/
│   ├── __init__.py              # Application factory
│   ├── config/
│   │   └── config.py            # Configuration settings
│   ├── models/
│   │   └── user.py              # User model
│   ├── routes/
│   │   └── api.py               # API routes
│   └── utils/
│       └── db_helpers.py        # Database utilities
├── docker-compose.yml           # Docker Compose configuration
├── Dockerfile                   # Docker file
├── requirements.txt             # Python dependencies
├── main.py                      # Application entry point
├── .env                         # Environment variables
└── k8s/                         # Kubernetes manifests
    ├── k8s-configmap.yml
    ├── k8s-flask-deployment.yml
    ├── k8s-ingress.yml
    ├── k8s-postgresql-statefulset-deployment.yml
    └── k8s-secret.yml
```

## Demo Video

### Video Demonstration Requirements

The demo video should showcase the following:

1. **Kubernetes Cluster Overview**
   - Display all deployed objects: `kubectl get all -n flask-user-app-dev-namespace`
   - Show pods, services, deployments, statefulsets, and persistent volumes
   - Video URL: [Kubernetes Cluster Overview](https://nagarro-my.sharepoint.com/:v:/p/kansagara_harshil/ESKlnLveOT1Gio9Mmgidr6cBxtDmqpSgVTPZRSRI5YPd_w?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=oFR8HU)

2. **Application Functionality**
   - Access Swagger UI: `http://user-app.flask.com/`
   - Demonstrate API calls to retrieve user records
   - Show database connectivity and data persistence
   - Video URL: [Application Functionality](https://nagarro-my.sharepoint.com/:v:/p/kansagara_harshil/EWdKgpixsZVFuRqG13vjqPoB4BNDGQb3N63KuDo_eEG1sg?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=VOmy18)

3. **Self-Healing Demonstration**
   - **Kill API Pod**:  

     ```bash
     kubectl delete pod <flask-app-pod-name> -n flask-user-app-dev-namespace
     ```

    Show automatic pod regeneration by Kubernetes
    Video URL: [Kill API Pod](https://nagarro-my.sharepoint.com/:v:/p/kansagara_harshil/EbPYH6GRpl5JtFWcytY6VHIBkyPovXskVhw9JpVfd7jpIA?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=SsDcKa)

   - **Kill Database Pod**:

     ```bash
     kubectl delete pod <postgres-pod-name> -n flask-user-app-dev-namespace
     ```

    Demonstrate pod regeneration and data persistence (StatefulSet behavior)
    Video URL: [Kill Database Pod](https://nagarro-my.sharepoint.com/:v:/p/kansagara_harshil/EWDFgUTa_8JNiCOhMkvdRKoBzQHUC8X084MGQUAI-hXIdA?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=KOyE6I)

4. **Data Persistence Verification**
   - Make API calls before killing database pod
   - After database pod regeneration, verify data is still available
   - Show that StatefulSet maintains data integrity
   - Video URL: [Data Persistence Verification](https://nagarro-my.sharepoint.com/:v:/p/kansagara_harshil/Ed8tOtUBVgdElQHmGuTjFQoBNyPfpvWUdrW50OFSi1nYXg?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=1vaIdP)

## Resources

- **Code Repository**: [Github Repository](https://github.com/Harshil-Kansagara/Flask-User-App-Kubernetes.git)
- **Docker Hub**: [Docker Hub](https://hub.docker.com/r/harshilkansagara/flask_user_app)
- **Demo Video folder**: [Demo Videos](https://nagarro-my.sharepoint.com/:f:/r/personal/kansagara_harshil_nagarro_com/Documents/NAGP%20Assignments/Kubernetes%20and%20Advanced%20DevOps%20Assignment/Demo%20Videos?csf=1&web=1&e=cD0cay)

## Configuration Details

### Kubernetes Resources

- **Namespace**: `flask-user-app-dev-namespace`
- **Flask App Replicas**: 4 (configurable)
- **Database**: PostgreSQL 15 with persistent storage
- **Storage**: 1Gi persistent volume for database
- **Resource Limits**: CPU 100m-200m, Memory 128Mi-256Mi

### Default Sample Data

The application initializes with 8 sample users across different departments:

- Engineering (3 users)
- Marketing (1 user)
- Sales (1 user)
- HR (1 user)
- Finance (1 user)
- Operations (1 user)
