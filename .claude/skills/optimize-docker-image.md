# Optimize Docker Image Skill

## Purpose
Optimize Docker images for size, performance, and Kubernetes readiness in the Cloud Native Todo Chatbot project. This skill focuses on reducing image sizes using multi-stage builds, removing unnecessary dependencies, implementing security best practices, and preparing images specifically for Minikube deployment.

## Responsibilities
- Reduce Docker image size using multi-stage builds and layer optimization
- Remove unnecessary dependencies and packages from final images
- Implement security best practices for Docker images
- Apply performance optimizations for container execution
- Prepare images specifically for efficient deployment in Minikube
- Analyze existing Dockerfiles for potential improvements
- Provide guidance on image caching and build optimization

## Allowed Actions
- Analyze existing Dockerfiles for optimization opportunities
- Recommend multi-stage build implementations for size reduction
- Suggest removal of unnecessary packages, dependencies, and build artifacts
- Provide guidance on optimal base image selection for size and security
- Recommend security best practices (non-root users, minimal base images, etc.)
- Suggest layer optimization strategies for faster builds and smaller images
- Provide commands for image analysis and size inspection
- Recommend appropriate compression and optimization tools

## Disallowed Actions
- Modify application source code or business logic
- Create entirely new application configurations
- Provide Kubernetes deployment configurations (focus on image optimization only)
- Recommend cloud-specific optimization strategies
- Modify system-level Docker configurations
- Provide production-level security configurations without proper context for beginners
- Suggest advanced optimization techniques without explaining fundamentals first

## Typical Prompts
- "How can I optimize my FastAPI Docker image?"
- "Make the frontend Docker image smaller for Kubernetes"
- "What are best practices for Docker images in this project?"
- "Analyze my Dockerfile for size reduction opportunities"
- "How do I implement a multi-stage build for my Next.js app?"
- "Show me how to reduce layers in my Docker image"
- "What base image should I use for the smallest FastAPI container?"
- "How do I run my container as a non-root user?"
- "Recommend security improvements for my Docker images"
- "How can I optimize Docker build cache usage?"