# GitHub Actions CI/CD Guide for Phase 4

This document provides a guide for setting up CI/CD automation for the Cloud Native Todo Chatbot Phase 4 deployment using GitHub Actions.

## Required GitHub Secrets

Before using the workflow, add these secrets to your GitHub repository:

- `DOCKER_USERNAME` - Your Docker Hub username
- `DOCKER_PASSWORD` - Your Docker Hub password or personal access token
- `SSH_PRIVATE_KEY` - Private key for SSH access (if needed for production deployments)
- `KUBE_CONFIG_DATA` - Base64 encoded kubeconfig file for remote cluster access (if needed)

## Workflow Overview

The provided workflow in `.github/workflows/deploy-phase4.yml` includes:

1. **Build Phase**: Builds Docker images for frontend and backend
2. **Optimization Phase**: Optimizes Docker images for size and security
3. **Test Phase**: Runs unit tests and validates Docker images
4. **Deploy Phase**: Deploys to Minikube for validation
5. **Validation Phase**: Performs health checks and functional tests
6. **Reporting Phase**: Generates and stores reports

## Customization Options

### For Production Deployment

To extend this for production deployment, add a new job:

```yaml
production-deploy:
  runs-on: ubuntu-latest
  needs: build-and-deploy
  if: github.ref == 'refs/heads/main'
  environment: production

  steps:
  - name: Deploy to Production
    run: |
      # Add production deployment commands here
      # Use kubectl to deploy to production cluster
      # Example:
      # kubectl config use-context production-cluster
      # kubectl set image deployment/frontend-deployment frontend=your-repo/frontend:${{ github.sha }}
```

### For Different Environments

Create separate workflows for different environments (staging, production) by duplicating the workflow file and changing:
- The trigger conditions (`on:`)
- The cluster context
- The image tags
- The validation steps

## Best Practices

### 1. Secure Secrets Management
- Never hardcode secrets in the workflow files
- Use GitHub Secrets for sensitive information
- Rotate secrets regularly
- Limit permissions of service accounts

### 2. Image Tagging Strategy
- Use commit SHA for precise versioning
- Use semantic version tags for releases
- Consider using timestamps for development builds

### 3. Resource Management
- Set up auto-scaling for runners
- Clean up resources after workflow completion
- Use ephemeral runners for security

### 4. Monitoring and Alerting
- Set up notifications for failed deployments
- Monitor deployment frequency and success rates
- Track mean time to recovery (MTTR)

## Common Issues and Solutions

### 1. Docker Build Failures
- Check if all dependencies are available in the build environment
- Ensure the Dockerfile syntax is correct
- Verify that the build context contains all required files

### 2. Minikube Startup Issues
- Increase timeout values if Minikube takes longer to start
- Check if there are sufficient resources allocated to the runner
- Consider using a larger runner with more memory and CPU

### 3. Kubernetes API Issues
- Ensure kubectl is installed and configured
- Verify that the correct context is selected
- Check RBAC permissions for the CI user

## Testing Locally

To test the workflow locally, you can use [act](https://github.com/nektos/act) which allows running GitHub Actions locally:

```bash
# Install act
brew install act  # Or follow installation guide for your OS

# Run the workflow locally
act -j build-and-deploy
```

## Extending the Workflow

### Add Security Scanning
```yaml
- name: Security Scan
  uses: anchore/scan-action@a5ad2b9ad5a55d9a1e0d30af4e0beeaa8dbd5e1a
  with:
    image: "cloud-native-todo-frontend:${{ github.sha }}"
    severity-cutoff: "high"
```

### Add Performance Testing
```yaml
- name: Performance Test
  run: |
    # Add performance testing scripts
    npm install -g autocannon
    autocannon -c 10 -d 10 -p 1 http://$(minikube service frontend-service --url)
```

### Add Notification
```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    channel: '#deployments'
  if: always() # This ensures the notification runs regardless of job success/failure
```

## Troubleshooting Tips

### For Beginners:
1. Always test changes in a development branch first
2. Enable verbose logging during debugging
3. Check the GitHub Actions documentation for syntax validation
4. Use GitHub's workflow editor to avoid YAML syntax errors

### Common Commands:
- `kubectl get pods` - Check if pods are running
- `kubectl describe pod <pod-name>` - Get detailed pod information
- `kubectl logs <pod-name>` - View pod logs
- `kubectl get services` - Check service status
- `minikube logs` - Check Minikube logs