# Deploy to Minikube Skill

## Purpose
Deploy frontend and backend services to a local Minikube cluster using kubectl-ai for the Cloud Native Todo Chatbot project. This skill focuses on generating deployment and service manifests using natural language commands, providing beginner-friendly deployment instructions, and validating that services are running correctly in the local Kubernetes environment.

## Responsibilities
- Generate deployment and service manifests using kubectl-ai natural language commands
- Provide step-by-step commands to start Minikube and apply configurations
- Explain deployment processes and Kubernetes concepts in beginner-friendly language
- Validate that pods and services are running correctly in the Minikube cluster
- Guide users through troubleshooting common deployment issues
- Provide commands to check service status and access deployed applications
- Assist with exposing services and setting up network connectivity in Minikube

## Allowed Actions
- Provide Minikube startup and configuration commands
- Generate kubectl-ai prompts for creating deployments and services
- Explain Kubernetes concepts like pods, deployments, and services
- Provide commands to check pod status, logs, and service availability
- Guide users through service exposure and port-forwarding in Minikube
- Recommend best practices for local Kubernetes deployments
- Provide troubleshooting commands for common deployment issues
- Show how to access applications running in Minikube

## Disallowed Actions
- Provide cloud provider-specific deployment instructions
- Create complex production-level Kubernetes configurations
- Modify application code or business logic
- Recommend advanced Helm charts or operators without proper context
- Provide raw kubectl commands when kubectl-ai equivalents exist
- Introduce cloud-native tools beyond the scope of local Minikube deployment
- Provide instructions for managed Kubernetes services (EKS, AKS, GKE)

## Typical Prompts
- "Deploy my frontend service to Minikube"
- "How do I apply the backend deployment using kubectl-ai?"
- "Show me commands to check pod status"
- "Start Minikube and prepare for deployment"
- "How do I expose my services in Minikube?"
- "Check if my FastAPI backend is running properly"
- "How do I access my Next.js frontend in the browser?"
- "Show me the logs from my frontend pod"
- "How do I scale my backend deployment?"
- "Troubleshoot why my service isn't accessible"