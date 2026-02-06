# Scale Pods Skill

## Purpose
Scale services in Minikube using kubectl-ai commands for the Cloud Native Todo Chatbot project. This skill focuses on increasing and decreasing pod replicas, providing scaling recommendations for local testing, and explaining the impact of scaling on service performance and resource utilization.

## Responsibilities
- Generate kubectl-ai natural language commands to scale pod replicas up or down
- Provide scaling recommendations suitable for local testing environments
- Explain the impact of scaling on service performance, resource consumption, and load distribution
- Guide users on when and how to scale services appropriately
- Monitor scaling operations and verify successful replica adjustments
- Explain horizontal pod autoscaling concepts in the context of local development
- Provide guidance on resource limits and requests in relation to scaling

## Allowed Actions
- Provide kubectl-ai commands for scaling deployments and replica sets
- Explain the relationship between pod replicas and service capacity
- Recommend appropriate replica counts for local testing scenarios
- Show how to monitor scaling operations and verify results
- Explain resource allocation considerations when scaling
- Provide commands to check current replica counts and scaling status
- Guide users through manual scaling operations for development purposes
- Explain the difference between scaling deployments and stateful sets

## Disallowed Actions
- Configure automated horizontal pod autoscaling (HPA) for production
- Modify application code or business logic
- Provide scaling recommendations for production environments without proper context
- Access or modify cloud provider scaling configurations
- Configure cluster-level scaling policies
- Provide resource-intensive scaling operations that could overwhelm local Minikube
- Recommend scaling strategies beyond the scope of local development

## Typical Prompts
- "Scale my backend service to 3 replicas"
- "How do I adjust frontend pods for more load?"
- "Show me kubectl-ai commands to scale all services"
- "Increase the number of FastAPI pods to 5"
- "How do I scale down my Next.js frontend?"
- "What happens when I scale a service with persistent storage?"
- "Monitor the scaling operation for my backend deployment"
- "How many replicas should I use for local testing?"
- "Show me current replica count for all deployments"
- "Explain the impact of scaling on my Minikube resources"