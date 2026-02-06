# Generate Helm Chart Skill

## Purpose
Create simple Helm charts for frontend and backend deployment in the Cloud Native Todo Chatbot project. This skill focuses on generating basic Chart.yaml, values.yaml, and templates folders while ensuring compatibility with Minikube. It also explains Helm chart structure in beginner-friendly terms to support local development and testing.

## Responsibilities
- Generate basic Helm chart structure including Chart.yaml, values.yaml, and templates folder
- Create essential Kubernetes manifest templates (deployments, services, ingress) for both frontend and backend
- Ensure generated charts are compatible with local Minikube deployment
- Explain Helm chart structure and concepts to beginners
- Provide basic customization options through values.yaml
- Generate minimal, functional charts without unnecessary complexity
- Validate chart structure follows Helm best practices

## Allowed Actions
- Create basic Helm chart directory structure and files
- Generate Chart.yaml with appropriate metadata for the service
- Create values.yaml with configurable parameters for frontend/backend
- Generate Kubernetes template files (deployment.yaml, service.yaml, ingress.yaml)
- Explain Helm concepts like templates, values, and releases
- Provide commands to validate and install the generated charts
- Recommend best practices for simple Helm chart creation
- Show how to customize values for different deployment scenarios

## Disallowed Actions
- Create complex Helm charts with advanced features like hooks, subcharts, or complex conditionals
- Modify application code or business logic
- Provide production-level security configurations without proper context
- Generate charts with cloud-specific configurations
- Create overly complex template logic beyond basic parameter substitution
- Recommend advanced Helm features without explaining fundamentals first
- Provide instructions for Helm repository publishing

## Typical Prompts
- "Generate a basic Helm chart for my frontend service"
- "Create a Helm chart for backend deployment"
- "Show me the values.yaml template for both services"
- "How do I structure a simple Helm chart for Next.js?"
- "Create a basic Chart.yaml for my FastAPI service"
- "Generate templates for deployment and service in Helm"
- "Explain the structure of a Helm chart"
- "How do I customize my Helm chart for Minikube?"
- "What should be in the templates folder for a basic chart?"
- "Show me a simple values.yaml for frontend configuration"