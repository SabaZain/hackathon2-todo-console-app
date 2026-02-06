# Phase 4 Quick Start Guide

## One-Time Setup

1. **Install Prerequisites**:
   ```powershell
   # Run as Administrator
   powershell -File setup-prerequisites.ps1
   ```

2. **Verify Installation**:
   ```bash
   docker --version
   kubectl version --client
   minikube version
   helm version
   ```

## Deployment

1. **Run Deployment Script**:
   ```cmd
   # On Windows
   deploy-phase4.bat
   ```

   ```bash
   # On Linux/Mac
   chmod +x deploy-phase4.sh
   ./deploy-phase4.sh
   ```

2. **Access Application**:
   - The script will output the URL when complete
   - Usually accessible at: `http://<minikube-ip>:<nodeport>`

## Common Commands

```bash
# Check status
kubectl get pods,svc

# Check logs
kubectl logs -l app=backend
kubectl logs -l app=frontend

# Scale services
kubectl scale deployment backend-deployment --replicas=2
kubectl scale deployment frontend-deployment --replicas=2

# Open dashboard
minikube dashboard

# Reset if needed
kubectl delete all --all
```

## Troubleshooting

**If Docker won't start**: Restart Docker Desktop application

**If Minikube won't start**: Run as Administrator with adequate resources

**If services aren't accessible**: Check that both backend and frontend pods are running

**To check detailed status**:
```bash
kubectl describe pod <pod-name>
kubectl get events --sort-by='.lastTimestamp'
```

## Next Steps

- Explore the application features
- Test the scaling capabilities
- Try the optional Helm deployment
- Review the validation scripts