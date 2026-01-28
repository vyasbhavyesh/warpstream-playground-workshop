# WarpStream Workshop

A hands-on workshop for learning WarpStream - a Kafka-compatible data streaming platform that stores data directly in object storage.

## What is WarpStream?

WarpStream is a Kafka-compatible streaming platform that eliminates the need for local disk storage. It writes data directly to object storage (S3, GCS, etc.), providing:

- **Zero disk management** - No brokers to scale or rebalance
- **Infinite retention** - Data stored in cheap object storage
- **Kafka compatibility** - Works with existing Kafka clients and tools

## Workshop Overview

| Lab | Topic | Duration | What You'll Learn |
|-----|-------|----------|-------------------|
| Lab 0 | Setup | 15 min | Install CLI, start playground |
| Lab 1 | Producer & Consumer | 45 min | Messaging basics, consumer groups, performance tuning |
| Lab 2 | Agent Groups | 30 min | Traffic isolation, multi-agent topology |
| Lab 3 | Orbit | 30 min | Cluster linking, zero-downtime migrations |
| Lab 4 | Pipelines | 30 min | Data transformations, sinks |
| Lab 5 | Schema Registry | 30 min | Avro schemas, schema evolution |
| Lab 6 | Tableflow | 45 min | Kafka to Iceberg, analytics |
| Lab 7 | Monitoring | 20 min | Prometheus, Grafana dashboards |

**Total Duration**: 4-5 hours

## Prerequisites

- **Docker Desktop** installed and running
- **macOS or Linux** (Windows via WSL2)
- **Basic Kafka knowledge** helpful but not required
- **4GB RAM** available for Docker

## Quick Start

1. **Clone this repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/warpstream-workshop.git
   cd warpstream-workshop
   ```

2. **Install WarpStream CLI**
   ```bash
   curl https://console.warpstream.com/install.sh | bash
   ```

3. **Install kcat**
   ```bash
   # macOS
   brew install kcat
   
   # Linux
   apt-get install kafkacat
   ```

4. **Start the WarpStream Playground**
   ```bash
   mkdir /tmp/warpstream-data
   warpstream playground -bucketURL "file:///tmp/warpstream-data"
   ```

5. **Begin the labs**
   
   Open [labs/README.md](labs/README.md) and start with Lab 0.

## Repository Structure

```
.
├── README.md              # This file
├── labs/                  # Workshop lab instructions
│   ├── README.md          # Lab overview and learning paths
│   ├── lab-0-setup.md     # Environment setup
│   ├── lab-1-producer-consumer.md
│   ├── lab-2-agent-groups.md
│   ├── lab-3-orbit.md
│   ├── lab-4-pipelines.md
│   ├── lab-5-schema-registry.md
│   ├── lab-6-tableflow.md
│   └── lab-7-monitoring.md
├── docker/                # Docker Compose files for labs
│   ├── docker-compose-lab3.yml   # Legacy Kafka for Orbit lab
│   ├── docker-compose-lab6.yml   # DuckDB for Tableflow lab
│   ├── docker-compose-lab7.yml   # Prometheus + Grafana
│   ├── Dockerfile.duckdb
│   ├── prometheus/
│   └── grafana/
├── scripts/               # Helper scripts
│   ├── produce-sample-orders.sh
│   └── query-iceberg-with-pyiceberg.py
├── .env.example           # Environment variables template
└── .gitignore
```

## Environment Setup (for Lab 7)

For Lab 7 (Monitoring), you'll need WarpStream credentials:

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your credentials from the WarpStream Console
# VCI_ID=vci_your_cluster_id
# WARPSTREAM_APP_KEY=aks_your_app_key
```

## Resources

- [WarpStream Documentation](https://docs.warpstream.com)
- [WarpStream Performance Tuning](https://docs.warpstream.com/warpstream/kafka/configure-kafka-client/tuning-for-performance)
- [Bento (Pipeline) Documentation](https://warpstreamlabs.github.io/bento/docs/about)
- [WarpStream Community Slack](https://warpstreamcommunity.slack.com)

## License

This workshop material is provided for educational purposes.
