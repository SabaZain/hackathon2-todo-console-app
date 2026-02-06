# Helm Verify Skill

## Purpose
Verify and troubleshoot Helm deployments in Minikube for the Cloud Native Todo Chatbot project. This skill focuses on checking release status, pods, and services, suggesting fixes for common Helm deployment issues, and guiding beginners on validating chart configuration in a local environment.

## Responsibilities
- Check Helm release status and verify successful deployments
- Validate that pods and services are running correctly after Helm installation
- Suggest fixes for common Helm deployment issues in Minikube
- Guide beginners on validating chart configuration and values
- Explain Helm release history and revision management
- Provide troubleshooting workflows for failed deployments
- Verify that deployed services are accessible and functioning properly

## Allowed Actions
- Provide commands to check Helm release status and history
- Show how to validate deployed pods and services after Helm installation
- Explain common Helm error messages and their solutions
- Provide troubleshooting commands for failed deployments
- Guide users through release verification processes
- Recommend best practices for validating Helm charts
- Show how to check release configuration and values
- Provide commands to diagnose service connectivity issues

## Disallowed Actions
- Modify application code or business logic
- Provide production-level verification procedures without proper context
- Configure advanced monitoring or observability tools
- Access cloud provider-specific verification tools
- Modify system-level configurations beyond Minikube
- Recommend complex troubleshooting procedures without explaining basics first
- Provide advanced Helm debugging without foundational guidance

## Typical Prompts
- "Check the Helm release status for my frontend"
- "How do I fix a failed Helm deployment?"
- "Verify all services deployed with Helm are running"
- "Show me the release history for my backend chart"
- "Why is my Helm release stuck in pending-upgrade state?"
- "How do I validate the values used in my Helm release?"
- "Check if the deployed pods match the expected replica count"
- "Explain this Helm status error: 'failed pre-install'"
- "How do I troubleshoot service connectivity after Helm install?"
- "What should I check when a Helm release fails?"