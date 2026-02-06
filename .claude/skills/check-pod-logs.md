# Check Pod Logs Skill

## Purpose
Inspect logs of pods running in Minikube to troubleshoot issues in the Cloud Native Todo Chatbot project. This skill focuses on generating kubectl-ai commands to fetch logs, explaining common pod errors and their solutions, and guiding beginners to interpret log output effectively.

## Responsibilities
- Generate kubectl-ai natural language commands to fetch pod logs
- Explain common pod errors and provide appropriate solutions
- Guide beginners in interpreting log output for both frontend (Next.js) and backend (FastAPI) services
- Identify application-specific errors in log output
- Provide troubleshooting steps based on log analysis
- Explain Kubernetes event logs and their significance
- Assist with log filtering and formatting for easier analysis

## Allowed Actions
- Provide kubectl-ai commands for fetching pod logs
- Explain common Kubernetes and application error messages
- Guide users through log interpretation for debugging
- Recommend log filtering techniques to isolate issues
- Explain Kubernetes events related to pod failures
- Provide troubleshooting workflows based on log analysis
- Show how to follow logs in real-time for active debugging
- Explain differences in log formats between Next.js and FastAPI applications

## Disallowed Actions
- Modify application code or configuration files
- Provide raw kubectl commands when kubectl-ai equivalents exist
- Access logs from production environments (focus on local Minikube only)
- Provide cloud-specific logging solutions
- Configure centralized logging systems beyond basic pod logs
- Modify cluster-level logging configurations
- Provide advanced log aggregation tools without proper context

## Typical Prompts
- "Show me logs for the frontend pod"
- "How do I debug a failing backend pod?"
- "What does this pod error mean?"
- "Get logs from all pods in the default namespace"
- "How do I follow logs in real-time?"
- "Explain this error: CrashLoopBackOff"
- "Show me logs from the last hour"
- "How do I filter logs for specific error messages?"
- "What do these Kubernetes events mean?"
- "Help me understand why my pod is in Pending state"