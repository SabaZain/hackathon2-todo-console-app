# Build Docker Image Skill

## Purpose
Generate Dockerfiles and build Docker images for frontend (Next.js) and backend (FastAPI) services of the Cloud Native Todo Chatbot. This skill focuses on creating optimized, beginner-friendly Docker configurations that are compatible with local Minikube deployment.

## Responsibilities
- Create optimized Dockerfile templates for Next.js frontend and FastAPI backend services
- Build Docker images locally with appropriate tagging
- Provide clear, beginner-friendly docker build commands and explanations
- Ensure generated images are compatible with Minikube for local Kubernetes deployment
- Apply best practices for image size optimization and security
- Generate multi-stage builds where appropriate for production readiness

## Allowed Actions
- Generate Dockerfile configurations for Next.js and FastAPI applications
- Provide docker build commands with appropriate tagging schemes
- Explain Docker build context and optimization techniques
- Recommend image size reduction strategies (multi-stage builds, .dockerignore, etc.)
- Generate .dockerignore files for each service type
- Suggest appropriate base images for each service
- Provide guidance on build arguments and environment variables

## Disallowed Actions
- Modify application source code or business logic
- Create complex Docker configurations without explaining basics first
- Recommend production-level security configurations without proper context
- Provide docker run commands or container management commands
- Generate docker-compose files (this skill focuses only on image building)
- Install system-level packages outside of container builds

## Typical Prompts
- "Generate a Dockerfile for my FastAPI backend"
- "Build the Docker image for the frontend service"
- "Show me the docker build command for this service"
- "How do I optimize my Next.js Dockerfile for smaller image size?"
- "Create a multi-stage Dockerfile for my backend service"
- "What's the best base image for my FastAPI application?"
- "How do I build Docker images with specific tags?"
- "Generate a .dockerignore file for my Next.js app"
- "How do I pass build arguments when building my Docker image?"
- "Show me how to check if my Docker image is Minikube-compatible"