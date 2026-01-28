# Lab 7: Monitoring with Prometheus and Grafana

## Learning Objectives

By the end of this lab, you will:
- Understand WarpStream's hosted Prometheus endpoint
- Set up Prometheus to scrape metrics from multiple sources
- Configure Grafana dashboards for monitoring
- Explore both control plane and agent metrics

## Concept Introduction

WarpStream provides comprehensive monitoring through Prometheus metrics at two levels:

1. **Hosted Prometheus Endpoint**: Control plane metrics including consumer group analytics, partition information, and cluster health. This endpoint avoids high cardinality issues by aggregating metrics server-side.

2. **Agent Metrics**: Local agent performance metrics exposed via HTTP `/metrics` endpoint on each WarpStream agent.

## Architecture

```
┌─────────────────────────────────────────┐
│  WarpStream Hosted Prometheus Endpoint  │
│  (api.warpstream.com)                   │
│  - Consumer group metrics               │
│  - Partition information                │
│  - Control plane utilization            │
└─────────────────┬───────────────────────┘
                  │
                  │ HTTPS + Basic Auth
                  │
┌─────────────────▼───────────────────────┐
│          Prometheus Server              │
│  - Scrapes both endpoints               │
│  - Stores time-series data              │
└─────────────────┬───────────────────────┘
                  │
                  │ PromQL queries
                  │
┌─────────────────▼───────────────────────┐
│          Grafana Dashboard              │
│  - Visualizes metrics                   │
│  - Pre-configured dashboards            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  WarpStream Agent (localhost:9092)      │
│  - Agent performance metrics            │
│  - HTTP /metrics endpoint               │
└─────────────────┬───────────────────────┘
                  │
                  │ HTTP scrape
                  │
          (connects to Prometheus)
```

## Step 1: Get Your WarpStream Credentials

Before setting up monitoring, you need to obtain your WarpStream credentials from the console.

### Option A: If Using WarpStream Playground (Lab 0)

When you started the playground with `warpstream playground`, you should have received a console URL. If not, you can find your credentials in the playground output.

1. **Find Your Virtual Cluster ID (VCI_ID)**:
   - The playground automatically creates a temporary cluster
   - Check the terminal output where you ran `warpstream playground`
   - Look for the Virtual Cluster ID in the output

2. **Create an App Key for Monitoring**:
   - Open the WarpStream console URL provided by the playground
   - Navigate to **Dashboard** → **API Keys**
   - Click **Create New Key**
   - Give it a name like "prometheus-monitoring"
   - Copy the generated key (starts with `aks_`)

### Option B: If Using Your Own WarpStream Cluster

1. **Login to WarpStream Console**: https://console.warpstream.com
2. **Get Virtual Cluster ID**:
   - Go to **Dashboard** → **Cluster**
   - Copy the **Virtual Cluster ID** (starts with `vci_`)
3. **Create App Key**:
   - Go to **Dashboard** → **API Keys**
   - Click **Create New Key**
   - Select your virtual cluster
   - Copy the generated key (starts with `aks_`)

### Step 2: Configure Environment Variables

Update your `.env` file with your credentials:

```bash
# Add to .env
VCI_ID=vci_YOUR_CLUSTER_ID_HERE
WARPSTREAM_APP_KEY=aks_YOUR_APP_KEY_HERE
```

**Example format** (use your own values):
```bash
VCI_ID=vci_3ca57c80_95a8_464a_b302_f2ec3332c9ee
WARPSTREAM_APP_KEY=aks_5ca89ca28c10828b8a3de50df49c2eb8b89937e64570622565f109c6607eb8f3
```

> **Important**: Replace the placeholder values with your actual credentials. The monitoring will not work with example values.

## Step 3: Start the Monitoring Stack

Launch Prometheus and Grafana:

```bash
docker-compose -f docker/docker-compose-lab7.yml up -d
```

This starts:
- **Prometheus**: Metrics collection and storage (port 9090)
- **Grafana**: Metrics visualization (port 3000)

## Step 4: Verify Prometheus is Scraping

Open Prometheus in your browser:

```
http://localhost:9090
```

Check the targets:
1. Go to **Status** → **Targets**
2. Verify both targets are UP:
   - `warpstream-hosted` (api.warpstream.com)
   - `warpstream-agent` (localhost:9092/metrics)

## Step 5: Explore Metrics in Prometheus

Try some sample queries in the Prometheus UI (Graph tab):

**Consumer Group Lag:**
```promql
warpstream_consumer_group_lag_seconds
```

**Agent CPU Usage:**
```promql
warpstream_agent_cpu_usage_percent
```

**Partition Count:**
```promql
warpstream_partition_count
```

**Control Plane Utilization:**
```promql
warpstream_control_plane_utilization
```

## Step 6: Access Grafana

Open Grafana:
```
http://localhost:3001
```

**Default Credentials:**
- Username: `admin`
- Password: `admin`

(You'll be prompted to change the password on first login)

> **Note**: Grafana is on port 3001 instead of the default 3000 to avoid conflicts with other services that might be running on your machine.

## Step 7: Add Prometheus Data Source

1. Go to **Configuration** → **Data Sources**
2. Click **Add data source**
3. Select **Prometheus**
4. Set URL: `http://prometheus:9090`
5. Click **Save & Test**

## Step 8: Create a Dashboard

Create a simple dashboard to monitor WarpStream:

1. Click **+** → **Dashboard** → **Add new panel**
2. Use these queries for different panels:

**Panel 1: Consumer Group Lag**
```promql
sum by (consumer_group) (warpstream_consumer_group_lag_seconds)
```

**Panel 2: Throughput (Bytes In)**
```promql
rate(warpstream_bytes_in_total[5m])
```

**Panel 3: Active Connections**
```promql
warpstream_active_connections
```

**Panel 4: Partition Count by Topic**
```promql
sum by (topic) (warpstream_partition_count)
```

## Step 9: Generate Load and Observe

Let's generate some traffic to see metrics in action:

**Terminal 1 - Produce messages:**
```bash
for i in $(seq 1 1000); do
  echo "message-$i" | kcat -b localhost:9092 -t monitoring-test -P
  sleep 0.1
done
```

**Terminal 2 - Consume messages:**
```bash
kcat -b localhost:9092 -t monitoring-test -G test-consumer-group -C
```

Watch the metrics update in real-time in Grafana!

## Available Metrics Reference

### Hosted Prometheus Endpoint Metrics

The hosted endpoint provides these key metrics:

- `warpstream_consumer_group_lag_seconds`: Consumer group lag in seconds
- `warpstream_consumer_group_state`: Consumer group state (0=Dead, 1=Empty, 2=Stable)
- `warpstream_partition_count`: Number of partitions per topic
- `warpstream_partition_size_bytes`: Size of each partition
- `warpstream_control_plane_utilization`: Control plane CPU/memory usage
- `warpstream_diagnostic_status`: Overall cluster health

### Agent Metrics

Local agent metrics include:

- `warpstream_agent_cpu_usage_percent`: Agent CPU utilization
- `warpstream_agent_memory_bytes`: Agent memory usage
- `warpstream_bytes_in_total`: Total bytes received
- `warpstream_bytes_out_total`: Total bytes sent
- `warpstream_active_connections`: Current active connections
- `warpstream_produce_requests_total`: Total produce requests
- `warpstream_fetch_requests_total`: Total fetch requests

## Advanced: Alert Rules

Prometheus can be configured with alerting rules. Here's an example for high consumer lag:

```yaml
# prometheus/alerts.yml
groups:
  - name: warpstream_alerts
    interval: 30s
    rules:
      - alert: HighConsumerLag
        expr: warpstream_consumer_group_lag_seconds > 300
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High consumer lag detected"
          description: "Consumer group {{ $labels.consumer_group }} has lag of {{ $value }}s"
```

## Troubleshooting

**Run script validation errors:**
- Make sure you've replaced placeholder values with your actual credentials
- VCI_ID should start with `vci_`
- WARPSTREAM_APP_KEY should start with `aks_`
- Get credentials from WarpStream Console (see Step 1)

**Prometheus target is DOWN:**
- Check VCI_ID and WARPSTREAM_APP_KEY are correct in `.env`
- Verify they are your actual credentials, not placeholder/example values
- Test the hosted endpoint manually:
  ```bash
  curl -u prometheus:$WARPSTREAM_APP_KEY \
    "https://api.warpstream.com/api/v1/monitoring/prometheus/virtual_clusters/$VCI_ID"
  ```
- If you get a 401/403 error, your credentials are invalid

**No agent metrics:**
- Ensure WarpStream playground is running
- Check agent exposes metrics: `curl http://localhost:9092/metrics`

**Grafana shows no data:**
- Verify Prometheus data source is configured correctly
- Check Prometheus is successfully scraping (Status → Targets)

## Cleanup

Stop the monitoring stack:

```bash
docker-compose -f docker/docker-compose-lab7.yml down
```

## Additional Resources

- [WarpStream Hosted Prometheus Endpoint Documentation](https://docs.warpstream.com/warpstream/agent-setup/monitor-the-warpstream-agents/hosted-prometheus-endpoint)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
