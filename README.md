# Event-Driven To-Do Application using FastAPI, AWS SQS, Docker, and Kubernetes

## Overview

This project is a production-style, event-driven To-Do application built using **FastAPI**, **Pydantic**, **Amazon SQS**, **Docker**, and **Kubernetes**.

The application demonstrates:

* REST API development using FastAPI
* Request validation using Pydantic
* Event-driven architecture using Amazon SQS
* Asynchronous message processing using a Consumer service
* Containerization using Docker
* Deployment using Kubernetes manifests

The project is divided into two independent services:

1. **Producer Service (FastAPI API)**
2. **Consumer Service (SQS Message Processor)**

---

# Architecture

```text
                   ┌──────────────────┐
                   │      Client      │
                   └────────┬─────────┘
                            │
                            │ HTTP Request
                            ▼
                  ┌───────────────────┐
                  │  FastAPI Producer │
                  │     (CRUD API)    │
                  └────────┬──────────┘
                           │
                           │ Publish Event
                           ▼
                  ┌───────────────────┐
                  │     AWS SQS       │
                  │   Message Queue   │
                  └────────┬──────────┘
                           │
                           │ Consume Event
                           ▼
                  ┌───────────────────┐
                  │   Consumer App    │
                  │ Background Worker │
                  └───────────────────┘
```

---

# Features

## Producer (FastAPI Service)

### CRUD APIs

* Create To-Do
* Get All To-Dos
* Get To-Do by ID
* Update To-Do
* Delete To-Do

### API Documentation

* Swagger UI
* ReDoc Documentation

### Pydantic Validation

* Request body validation
* Type checking
* Automatic error handling

### Event Publishing

Whenever a new To-Do is created:

1. To-Do is saved.
2. A `todo_created` event is published to Amazon SQS.

---

## Consumer Service

The consumer continuously:

1. Polls the SQS queue.
2. Receives new events.
3. Processes the event.
4. Deletes the message from the queue.

This simulates background processing services such as:

* Notifications
* Emails
* Analytics
* Audit Logging
* Reporting

---

# Technologies Used

| Technology | Purpose                 |
| ---------- | ----------------------- |
| Python     | Programming Language    |
| FastAPI    | REST API Framework      |
| Pydantic   | Data Validation         |
| Amazon SQS | Message Queue           |
| Boto3      | AWS SDK                 |
| Docker     | Containerization        |
| Kubernetes | Container Orchestration |
| Uvicorn    | ASGI Server             |

---

# Project Structure

```text
todo-app/
│
├── producer/
│   ├── main.py
│   ├── schemas.py
│   ├── sqs_service.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
│
├── consumer/
│   ├── consumer.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
│
├── k8s/
│   ├── secret.yaml
│   ├── producer-deployment.yaml
│   ├── producer-service.yaml
│   └── consumer-deployment.yaml
│
└── README.md
```

---

# Setting Up Amazon SQS

## Step 1

Create an SQS Queue.

Queue Name:

```text
todo-created
```

Copy:

* Queue URL
* AWS Region

---

## Step 2

Create an IAM User.

Attach:

```text
AmazonSQSFullAccess
```

Generate:

* Access Key
* Secret Key

---

# Environment Variables

## Producer

```env
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
SQS_QUEUE_URL=
```

## Consumer

```env
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
SQS_QUEUE_URL=
```

---

# Running Locally

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Start Producer

```bash
uvicorn main:app --reload
```

Application:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Start Consumer

```bash
python consumer.py
```

---

# API Endpoints

## Create To-Do

```http
POST /todos
```

Request:

```json
{
  "title": "Learn FastAPI",
  "description": "Study event-driven architecture"
}
```

---

## Get All To-Dos

```http
GET /todos
```

---

## Get To-Do by ID

```http
GET /todos/{id}
```

---

## Update To-Do

```http
PUT /todos/{id}
```

---

## Delete To-Do

```http
DELETE /todos/{id}
```

---

# Event Structure

Whenever a new To-Do is created:

```json
{
  "event": "todo_created",
  "data": {
    "id": 1,
    "title": "Learn FastAPI",
    "description": "Study event-driven architecture",
    "completed": false
  }
}
```

---

# Why Event-Driven Architecture?

Benefits:

* Loose coupling
* Scalability
* Independent services
* Fault tolerance
* Asynchronous processing
* Easier system expansion

---

# Dockerization

## Build Producer

```bash
docker build -t todo-producer .
```

---

## Run Producer

```bash
docker run -p 8000:8000 --env-file .env todo-producer
```

---

## Build Consumer

```bash
docker build -t todo-consumer .
```

---

## Run Consumer

```bash
docker run --env-file .env todo-consumer
```

---

# Multi-Stage Docker Build

The project uses multi-stage Docker builds to:

* Reduce image size
* Remove unnecessary build dependencies
* Improve security
* Improve deployment speed

---

# Docker Commands

## List Images

```bash
docker images
```

## List Containers

```bash
docker ps
```

## View Logs

```bash
docker logs <container-id>
```

---

# Kubernetes Deployment

## Create Secret

```bash
kubectl apply -f secret.yaml
```

---

## Deploy Producer

```bash
kubectl apply -f producer-deployment.yaml
kubectl apply -f producer-service.yaml
```

---

## Deploy Consumer

```bash
kubectl apply -f consumer-deployment.yaml
```

---

## Verify Deployment

```bash
kubectl get pods
kubectl get services
kubectl get deployments
```

---

# Producer Service

The producer is exposed using:

```yaml
type: LoadBalancer
```

This creates an external load balancer for public access.

---

# Monitoring Consumer

```bash
kubectl logs deployment/todo-consumer -f
```

---

# Kubernetes Architecture

```text
┌─────────────────────────────┐
│         Kubernetes          │
│                             │
│  Producer Pods              │
│         │                   │
│         ▼                   │
│      AWS SQS                │
│         ▼                   │
│  Consumer Pods              │
└─────────────────────────────┘
```

---

# Security Considerations

* AWS credentials stored as Kubernetes Secrets
* Environment variables separated from code
* Docker images contain no secrets
* Producer and Consumer are independently deployable

---

# Future Improvements

* PostgreSQL integration
* JWT Authentication
* Dead Letter Queue (DLQ)
* Redis Caching
* Horizontal Pod Autoscaling
* CI/CD using GitHub Actions
* Monitoring using Prometheus and Grafana
* Distributed Tracing
* AWS ECR Integration
* Helm Charts

---

# Learning Outcomes

This project demonstrates practical understanding of:

* FastAPI
* Pydantic Validation
* REST API Design
* Event-Driven Architecture
* Amazon SQS
* Background Processing
* Docker
* Multi-Stage Builds
* Kubernetes Deployments
* Secrets Management
* Microservices Architecture

---

# Conclusion

This project is a complete end-to-end implementation of an event-driven microservices architecture where:

1. The Producer exposes REST APIs.
2. The Producer publishes events to Amazon SQS.
3. The Consumer asynchronously processes those events.
4. Both services are containerized using Docker.
5. The services are deployed using Kubernetes manifests.

The architecture is cloud-agnostic and can be deployed on:

* Amazon EKS
* Azure AKS
* Google GKE
* Minikube
* Kind
* On-premise Kubernetes clusters
