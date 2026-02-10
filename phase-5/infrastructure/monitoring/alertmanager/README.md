# Alertmanager Configuration

This directory contains Alertmanager deployment configuration for handling alerts from Prometheus.

## Overview

Alertmanager handles alerts sent by Prometheus and routes them to the appropriate notification channels:
- **Slack**: Real-time notifications to team channels
- **Email**: Email notifications for critical alerts
- **PagerDuty**: On-call escalation (optional)

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Prometheus  │────▶│ Alertmanager│────▶│   Slack     │
│   (Alerts)  │     │  (Routing)  │     │  Channels   │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ├────────────▶│   Email     │
                           │             │  Recipients │
                           │             └─────────────┘
                           │
                           └────────────▶│ PagerDuty   │
                                         │  (Optional) │
                                         └─────────────┘
```

## Deployment

### Prerequisites

1. **Slack Webhook URL** (optional but recommended):
   - Go to https://api.slack.com/apps
   - Create a new app or select existing
   - Enable Incoming Webhooks
   - Create webhook for your workspace
   - Copy the webhook URL

2. **SMTP Configuration** (optional):
   - SMTP server host and port
   - Authentication credentials
   - From email address

### Deploy to Kubernetes

```bash
# Update secrets with your configuration
kubectl create secret generic alertmanager-secrets \
  --from-literal=slack-webhook-url='https://hooks.slack.com/services/YOUR/WEBHOOK' \
  --from-literal=smtp-host='smtp.gmail.com' \
  --from-literal=smtp-port='587' \
  --from-literal=smtp-from='alerts@phase5.example.com' \
  --from-literal=smtp-username='your-email@gmail.com' \
  --from-literal=smtp-password='your-app-password' \
  -n monitoring

# Deploy Alertmanager
kubectl apply -f alertmanager.yaml
```

### Verify Deployment

```bash
# Check pod status
kubectl get pods -n monitoring -l app=alertmanager

# Check service
kubectl get svc -n monitoring alertmanager

# View logs
kubectl logs -n monitoring -l app=alertmanager
```

### Access Alertmanager UI

**Port Forward:**
```bash
kubectl port-forward -n monitoring svc/alertmanager 9093:9093
```

Then open: http://localhost:9093

## Alert Routing

### Routing Tree

Alerts are routed based on labels:

1. **Critical Alerts** (`severity: critical`)
   - Slack: #phase5-critical
   - Email: oncall@phase5.example.com
   - Immediate notification (no grouping delay)

2. **Warning Alerts** (`severity: warning`)
   - Slack: #phase5-warnings
   - 30s grouping delay
   - 1h repeat interval

3. **Component-Specific Alerts**
   - Database: #phase5-database
   - Kafka: #phase5-platform
   - Audit: #phase5-audit
   - Reminders: #phase5-notifications

### Notification Channels

Configure channels in `alertmanager-secrets`:

```bash
# Slack
kubectl create secret generic alertmanager-secrets \
  --from-literal=slack-webhook-url='YOUR_WEBHOOK_URL' \
  -n monitoring --dry-run=client -o yaml | kubectl apply -f -

# Email (Gmail example)
kubectl create secret generic alertmanager-secrets \
  --from-literal=smtp-host='smtp.gmail.com' \
  --from-literal=smtp-port='587' \
  --from-literal=smtp-from='alerts@example.com' \
  --from-literal=smtp-username='your-email@gmail.com' \
  --from-literal=smtp-password='your-app-password' \
  -n monitoring --dry-run=client -o yaml | kubectl apply -f -
```

## Alert Grouping

Alerts are grouped by:
- `alertname`: Same alert type
- `cluster`: Same cluster
- `service`: Same service

**Grouping Parameters:**
- `group_wait: 10s` - Wait 10s before sending first notification
- `group_interval: 10s` - Wait 10s before sending updates
- `repeat_interval: 12h` - Resend alert every 12h if still firing

## Inhibition Rules

Suppress redundant alerts:

1. **Critical suppresses Warning**
   - If critical alert fires, suppress warning for same service

2. **Deployment issues suppress Pod alerts**
   - If deployment has replica mismatch, suppress individual pod alerts

3. **Pod restarts suppress CPU alerts**
   - If pod is restarting, suppress high CPU alerts

## Notification Templates

### Slack Template

```
🚨 CRITICAL: HighErrorRate
*Alert:* High error rate detected in phase5-backend
*Description:* Error rate is 8.5% for service phase5-backend
*Severity:* critical
*Service:* phase5-backend
```

### Email Template

HTML email with:
- Alert summary
- Description
- Severity indicator (color-coded)
- All labels
- Start/end timestamps

## Testing Alerts

### Trigger Test Alert

```bash
# Port forward to Alertmanager
kubectl port-forward -n monitoring svc/alertmanager 9093:9093

# Send test alert
curl -X POST http://localhost:9093/api/v1/alerts -d '[
  {
    "labels": {
      "alertname": "TestAlert",
      "severity": "warning",
      "service": "test"
    },
    "annotations": {
      "summary": "This is a test alert",
      "description": "Testing Alertmanager configuration"
    }
  }
]'
```

### Silence Alerts

**Via UI:**
1. Open Alertmanager UI
2. Click "Silences"
3. Click "New Silence"
4. Set matchers and duration

**Via CLI:**
```bash
# Create silence
amtool silence add alertname=HighErrorRate --duration=1h \
  --comment="Maintenance window" \
  --alertmanager.url=http://localhost:9093
```

## Configuration

### Add New Receiver

Edit `alertmanager-config` ConfigMap:

```yaml
receivers:
  - name: 'my-team'
    slack_configs:
      - channel: '#my-channel'
        title: 'Alert: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
```

### Add New Route

```yaml
routes:
  - match:
      team: my-team
    receiver: 'my-team'
    group_by: ['alertname']
```

### Apply Changes

```bash
# Update ConfigMap
kubectl apply -f alertmanager.yaml

# Reload configuration (no restart needed)
kubectl exec -n monitoring -it deployment/alertmanager -- \
  kill -HUP 1
```

## Troubleshooting

### Alerts Not Sending

1. **Check Alertmanager logs:**
   ```bash
   kubectl logs -n monitoring -l app=alertmanager
   ```

2. **Verify Prometheus is sending alerts:**
   ```bash
   kubectl port-forward -n monitoring svc/prometheus 9090:9090
   # Open http://localhost:9090/alerts
   ```

3. **Check webhook/SMTP configuration:**
   ```bash
   kubectl get secret alertmanager-secrets -n monitoring -o yaml
   ```

4. **Test notification manually** (see Testing Alerts above)

### Slack Notifications Not Working

1. **Verify webhook URL:**
   ```bash
   kubectl get secret alertmanager-secrets -n monitoring \
     -o jsonpath='{.data.slack-webhook-url}' | base64 -d
   ```

2. **Test webhook directly:**
   ```bash
   curl -X POST 'YOUR_WEBHOOK_URL' \
     -H 'Content-Type: application/json' \
     -d '{"text":"Test message"}'
   ```

3. **Check Alertmanager logs** for webhook errors

### Email Notifications Not Working

1. **Verify SMTP settings:**
   ```bash
   kubectl get secret alertmanager-secrets -n monitoring -o yaml
   ```

2. **For Gmail, use App Password:**
   - Enable 2FA on your Google account
   - Generate App Password: https://myaccount.google.com/apppasswords
   - Use App Password instead of regular password

3. **Check firewall/network** allows SMTP traffic

## Best Practices

1. **Use Appropriate Severity Levels**
   - Critical: Requires immediate action
   - Warning: Should be investigated soon
   - Info: For awareness only

2. **Configure Inhibition Rules**
   - Prevent alert fatigue
   - Suppress redundant notifications

3. **Set Reasonable Repeat Intervals**
   - Critical: 5-15 minutes
   - Warning: 1-4 hours
   - Info: 12-24 hours

4. **Use Silences for Maintenance**
   - Silence alerts during planned maintenance
   - Add comments explaining why

5. **Test Regularly**
   - Test notification channels monthly
   - Verify on-call escalation works

6. **Monitor Alertmanager**
   - Set up alerts for Alertmanager itself
   - Monitor notification delivery success rate

## Integration with PagerDuty

Uncomment PagerDuty configuration in `alertmanager.yaml`:

```yaml
receivers:
  - name: 'critical-alerts'
    pagerduty_configs:
      - service_key: '${PAGERDUTY_SERVICE_KEY}'
        description: '{{ .GroupLabels.alertname }}: {{ .Annotations.summary }}'
```

Add secret:
```bash
kubectl create secret generic alertmanager-secrets \
  --from-literal=pagerduty-service-key='YOUR_KEY' \
  -n monitoring --dry-run=client -o yaml | kubectl apply -f -
```

## Resources

- [Alertmanager Documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)
- [Configuration Reference](https://prometheus.io/docs/alerting/latest/configuration/)
- [Notification Templates](https://prometheus.io/docs/alerting/latest/notifications/)
