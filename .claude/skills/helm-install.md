# Helm Install Skill

## Purpose
Install or upgrade Helm releases for local deployment in the Cloud Native Todo Chatbot project. This skill focuses on providing helm install and upgrade commands, explaining release management basics, and guiding beginners through the deployment process in a local Minikube environment.

## Responsibilities
- Provide helm install and upgrade commands for local Minikube deployment
- Explain Helm release management concepts and best practices
- Guide beginners through the complete deployment process
- Verify Helm release status and troubleshoot common installation issues
- Manage release versions and rollback procedures when needed
- Explain Helm value overrides and customization options during installation
- Provide commands to check release history and status

## Allowed Actions
- Provide helm install, upgrade, and rollback commands for local deployment
- Explain Helm release concepts like names, namespaces, and revisions
- Show how to use value overrides during installation and upgrades
- Provide commands to check release status, history, and configuration
- Guide users through troubleshooting common installation problems
- Recommend best practices for Helm release management
- Explain the difference between dry-run and actual installation
- Provide commands to list and manage Helm releases

## Disallowed Actions
- Modify application code or business logic
- Provide production-level Helm installation procedures without proper context
- Configure Helm repositories for cloud providers
- Install Helm charts to production environments
- Provide advanced Helm features like atomic installs or wait conditions without explaining basics first
- Recommend complex installation strategies without proper beginner foundation
- Access or modify system-level Helm configurations beyond local deployment

## Typical Prompts
- "Install the frontend Helm chart in Minikube"
- "Upgrade the backend Helm release"
- "How do I verify Helm release status?"
- "Show me the command to install with custom values"
- "Rollback the last Helm release"
- "List all Helm releases in the default namespace"
- "How do I upgrade with new configuration values?"
- "What does the --dry-run flag do in Helm?"
- "Check the status of my frontend release"
- "How do I install a Helm chart in a specific namespace?"