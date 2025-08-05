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
   - API Documentation: <http://localhost:5000/apidocs>
   - API Base URL: <http://localhost:5000/api>

## API Documentation

### Base URL

- **Local**: `http://localhost:5000/api`
- **Kubernetes**: `http://flask-user-app.local/api` (with ingress configured)

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | Get all users (supports department filter) |
| GET | `/api/users/{id}` | Get user by ID |
| POST | `/api/users` | Create new user |
| GET | `/apidocs` | Swagger UI documentation |

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

5. **Setup Ingress (Optional)**

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

### Access the Application

```bash
# Port forward to access locally
kubectl port-forward svc/flask-user-app-service 8080:80 -n flask-user-app-dev-namespace

# Access at http://localhost:8080
```

## Demo Video

### Video Demonstration Requirements

The demo video should showcase the following:

1. **Kubernetes Cluster Overview**
   - Display all deployed objects: `kubectl get all -n flask-user-app-dev-namespace`
   - Show pods, services, deployments, statefulsets, and persistent volumes
   - Video URL: <>

2. **Application Functionality**
   - Access Swagger UI: `http://flask-user-app.local/apidocs`
   - Demonstrate API calls to retrieve user records
   - Show database connectivity and data persistence
   - Video URL: <>

3. **Self-Healing Demonstration**
   - **Kill API Pod**:  

     ```bash
     kubectl delete pod <flask-app-pod-name> -n flask-user-app-dev-namespace
     ```

    Show automatic pod regeneration by Kubernetes
    Video URL: <>

   - **Kill Database Pod**:

     ```bash
     kubectl delete pod <postgres-pod-name> -n flask-user-app-dev-namespace
     ```

    Demonstrate pod regeneration and data persistence (StatefulSet behavior)
    Video URL: <>

4. **Data Persistence Verification**
   - Make API calls before killing database pod
   - After database pod regeneration, verify data is still available
   - Show that StatefulSet maintains data integrity
   - Video URL: <>

## Resources

- **Code Repository**: `https://github.com/Harshil-Kansagara/Flask-User-App-Kubernetes.git`
- **Docker Hub**: `https://hub.docker.com/r/harshilkansagara/flask_user_app`
- **API Documentation**: `http://flask-user-app.local/apidocs`

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
