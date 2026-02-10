# Phase 5 - Deployment Guide

## Overview

Phase 5 provides multiple deployment options:
1. **Local Development** - Docker Compose for rapid development
2. **Minikube** - Local Kubernetes testing
3. **Cloud** - Production deployment to DOKS/GKE/AKS (coming soon)

---

## Prerequisites

### All Deployments
- Node.js 18+
- npm 9+
- Git

### Docker Compose Deployment
- Docker Desktop or Docker Engine
- docker-compose

### Minikube Deployment
- Minikube
- kubectl
- Docker

### Cloud Deployment
- Terraform
- Helm 3
- Cloud provider CLI (doctl/gcloud/az)

---

## 1. Local Development with Docker Compose

### Quick Start

**Windows:**
```bash
cd phase-5/infrastructure/scripts
.\deploy-local.bat
```

**Linux/Mac:**
```bash
cd phase-5/infrastructure/scripts
chmod +x *.sh
./deploy-local.sh
```

### What It Does

1. Starts infrastructure services (PostgreSQL, Redis, Kafka, Zookeeper)
2. Initializes Kafka topics
3. Runs database migrations
4. Builds and starts all application services
5. Starts all 4 agents

### Services

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Next.js web application |
| Backend API | http://localhost:3001 | Express.js REST API |
| Kafka UI | http://localhost:8080 | Kafka management interface |
| PostgreSQL | localhost:5432 | Database |
| Redis | localhost:6379 | State store |

### Health Checks

```bash
# Backend health
curl http://localhost:3001/health

# Check all services
docker-compose -f infrastructure/docker/docker-compose.yml ps
```

### View Logs

**All services:**
```bash
cd infrastructure/scripts
./logs.sh
```

**Specific service:**
```bash
./logs.sh backend
./logs.sh frontend
./logs.sh audit-agent
```

### Stop Services

**Windows:**
```bash
.\stop-local.bat
```

**Linux/Mac:**
```bash
./stop-local.sh
```

### Clean Up (Remove All Data)

```bash
./clean.sh
```

---

## 2. Minikube Deployment

### Prerequisites

Install Minikube and kubectl:
```bash
# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

### Deploy to Minikube

```bash
cd phase-5/infrastructure/scripts
./deploy-minikube.sh
```

### What It Does

1. Starts Minikube (if not running)
2. Enables Ingress addon
3. Builds all Docker images in Minikube's Docker daemon
4. Applies all Kubernetes manifests
5. Waits for deployments to be ready

### Access Services

**Via NodePort:**
```bash
# Get Minikube IP
minikube ip

# Access services
# Frontend: http://<minikube-ip>:30000
# Backend:  http://<minikube-ip>:30001
```

**Via Port Forwarding:**
```bash
# Frontend
kubectl port-forward -n phase5 svc/frontend 3000:3000

# Backend
kubectl port-forward -n phase5 svc/backend 3001:3001
```

### Kubernetes Commands

**View resources:**
```bash
# All resources
kubectl get all -n phase5

# Pods
kubectl get pods -n phase5

# Services
kubectl get svc -n phase5

# Deployments
kubectl get deployments -n phase5
```

**View logs:**
```bash
# Backend logs
kubectl logs -n phase5 -l app=backend -f

# Frontend logs
kubectl logs -n phase5 -l app=frontend -f

# Specific pod
kubectl logs -n phase5 <pod-name> -f
```

**Describe resources:**
```bash
kubectl describe pod -n phase5 <pod-name>
kubectl describe deployment -n phase5 backend
```

**Execute commands in pods:**
```bash
kubectl exec -n phase5 -it <pod-name> -- /bin/sh
```

### Scale Deployments

```bash
# Scale backend to 3 replicas
kubectl scale deployment/backend -n phase5 --replicas=3

# Scale frontend to 3 replicas
kubectl scale deployment/frontend -n phase5 --replicas=3
```

### Update Deployments

```bash
# Rebuild images
eval $(minikube docker-env)
docker build -t phase5-backend:latest backend/

# Restart deployment
kubectl rollout restart deployment/backend -n phase5
```

### Delete Deployment

```bash
kubectl delete namespace phase5
```

---

## 3. Cloud Deployment (Coming Soon)

Cloud deployment infrastructure is planned for:
- DigitalOcean Kubernetes (DOKS)
- Google Kubernetes Engine (GKE)
- Azure Kubernetes Service (AKS)

Will include:
- Terraform infrastructure as code
- Helm charts for application deployment
- CI/CD pipelines with GitHub Actions
- Monitoring with Prometheus and Grafana
- Distributed tracing with Jaeger
- Log aggregation with ELK/Loki

---

## Configuration

### Environment Variables

**Backend (.env):**
```env
NODE_ENV=development
PORT=3001
DATABASE_URL=postgresql://phase5_user:phase5_password@localhost:5432/phase5_todo
JWT_SECRET=your-secret-key
JWT_EXPIRES_IN=7d
KAFKA_BROKERS=localhost:9092
CORS_ORIGIN=http://localhost:3000
LOG_LEVEL=info
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:3001
NEXT_PUBLIC_WS_URL=ws://localhost:3001
NEXT_TELEMETRY_DISABLED=1
```

**ReminderAgent (.env):**
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=Phase 5 Todo <noreply@phase5todo.com>
```

### Update Configuration

**Docker Compose:**
Edit `infrastructure/docker/docker-compose.yml` environment variables.

**Kubernetes:**
Edit `infrastructure/kubernetes/minikube/configmap.yaml` and `secrets.yaml`, then apply:
```bash
kubectl apply -f infrastructure/kubernetes/minikube/configmap.yaml
kubectl apply -f infrastructure/kubernetes/minikube/secrets.yaml
kubectl rollout restart deployment -n phase5 --all
```

---

## Troubleshooting

### Docker Compose Issues

**Services won't start:**
```bash
# Check logs
docker-compose -f infrastructure/docker/docker-compose.yml logs

# Restart specific service
docker-compose -f infrastructure/docker/docker-compose.yml restart backend

# Rebuild and restart
docker-compose -f infrastructure/docker/docker-compose.yml up -d --build backend
```

**Database connection errors:**
```bash
# Check PostgreSQL is running
docker-compose -f infrastructure/docker/docker-compose.yml ps postgres

# Check database logs
docker-compose -f infrastructure/docker/docker-compose.yml logs postgres

# Reset database
docker-compose -f infrastructure/docker/docker-compose.yml down -v
docker-compose -f infrastructure/docker/docker-compose.yml up -d postgres
```

**Kafka connection errors:**
```bash
# Check Kafka is running
docker-compose -f infrastructure/docker/docker-compose.yml ps kafka

# Recreate topics
docker-compose -f infrastructure/docker/docker-compose.yml up kafka-init
```

### Minikube Issues

**Minikube won't start:**
```bash
# Delete and recreate
minikube delete
minikube start --cpus=4 --memory=8192 --driver=docker
```

**Images not found:**
```bash
# Ensure you're using Minikube's Docker daemon
eval $(minikube docker-env)

# Rebuild images
docker build -t phase5-backend:latest backend/
```

**Pods in CrashLoopBackOff:**
```bash
# Check pod logs
kubectl logs -n phase5 <pod-name>

# Describe pod for events
kubectl describe pod -n phase5 <pod-name>
```

---

## Performance Tuning

### Docker Compose

**Increase resources:**
Edit Docker Desktop settings:
- CPUs: 4+
- Memory: 8GB+
- Swap: 2GB+

### Minikube

**Start with more resources:**
```bash
minikube start --cpus=6 --memory=12288 --disk-size=50g
```

### Database

**Optimize PostgreSQL:**
```sql
-- Add indexes for common queries
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
```

---

## Security Considerations

### Production Deployment

Before deploying to production:

1. **Change all default passwords and secrets**
2. **Enable SSL/TLS for all services**
3. **Configure proper CORS origins**
4. **Enable authentication on Kafka**
5. **Use managed databases (not containers)**
6. **Enable network policies in Kubernetes**
7. **Scan images for vulnerabilities**
8. **Set up proper backup strategies**
9. **Configure monitoring and alerting**
10. **Review and harden security settings**

---

## Next Steps

1. **Test the deployment** - Verify all services are working
2. **Load test** - Use k6 or Artillery to test performance
3. **Set up monitoring** - Deploy Prometheus and Grafana
4. **Configure CI/CD** - Set up GitHub Actions
5. **Plan cloud deployment** - Choose cloud provider and configure Terraform

---

## Support

For issues or questions:
- Check logs first
- Review troubleshooting section
- Check GitHub issues
- Consult architecture documentation in `docs/architecture.md`
