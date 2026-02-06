# Phase 4: History and Logs Directory

This directory contains historical data, logs, reports, and backups for the Phase 4 Cloud Native Todo Chatbot deployment to Minikube.

## Directory Structure

```
history/
├── builds/     # Build logs and artifacts for Docker images
├── logs/       # Runtime logs for deployed services
├── reports/    # Validation and test reports
└── backups/    # Backup configurations and data
```

### Builds (`/builds`)
- `frontend-build-YYYYMMDD-HHMM.log` - Frontend Docker build logs
- `backend-build-YYYYMMDD-HHMM.log` - Backend Docker build logs
- `build-summary-YYYYMMDD.json` - Build statistics and metadata

### Logs (`/logs`)
- `frontend-logs-YYYYMMDD.log` - Frontend service logs
- `backend-logs-YYYYMMDD.log` - Backend service logs
- `k8s-events-YYYYMMDD.log` - Kubernetes cluster events
- `minikube-status-YYYYMMDD.json` - Minikube cluster status reports

### Reports (`/reports`)
- `validation-report-YYYYMMDD.md` - Deployment validation reports
- `security-scan-YYYYMMDD.json` - Docker image security scan results
- `performance-report-YYYYMMDD.md` - Performance and resource utilization reports
- `health-check-YYYYMMDD.json` - System health check results

### Backups (`/backups`)
- `config-backup-YYYYMMDD.tar.gz` - Kubernetes configuration backup
- `data-backup-YYYYMMDD.tar.gz` - Application data backup (if applicable)
- `helm-values-backup-YYYYMMDD.yaml` - Helm configuration backup