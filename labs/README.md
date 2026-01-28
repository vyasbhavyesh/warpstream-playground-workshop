# WarpStream Workshop Labs

Welcome to the WarpStream hands-on workshop! This series of labs will guide you through WarpStream's key features and capabilities.

## Workshop Overview

**Total Duration**: 4-5 hours
**Difficulty**: Beginner to Advanced
**Prerequisites**:
- Basic Kafka knowledge
- Command line familiarity
- Docker installed

## Lab Structure

| Lab | Topic | Duration | Difficulty | Key Concepts |
|-----|-------|----------|------------|--------------|
| [Lab 0](lab-0-setup.md) | Setup | 15 min | Beginner | CLI installation, playground startup |
| [Lab 1](lab-1-producer-consumer.md) | Producers, Consumers & Fundamentals | 45 min | Intermediate | Production, consumption, consumer groups, tuning |
| [Lab 2](lab-2-agent-groups.md) | WarpStream Agent Groups | 30 min | Intermediate | Agent Groups, Isolation, Routing |
| [Lab 3](lab-3-orbit.md) | Orbit (Cluster Linking) | 30 min | Intermediate | Replication, migration, zero-downtime |
| [Lab 4](lab-4-pipelines.md) | Managed Data Pipelines | 30 min | Intermediate | Transformations, S3 sink, Bloblang |
| [Lab 5](lab-5-schema-registry.md) | Schema Registry | 30 min | Intermediate | Avro, Protobuf, schema evolution |
| [Lab 6](lab-6-tableflow.md) | Tableflow (Kafka to Iceberg) | 45 min | Advanced | Analytics, DuckDB, partitioning |
| [Lab 7](lab-7-monitoring.md) | Monitoring (Prometheus) | 20 min | Intermediate | Metrics, dashboards, observability |

---

## Learning Paths

### Beginner Path (2 hours)
Perfect for getting started with WarpStream:
1. Lab 0: Setup (15 min)
2. Lab 1: Producers, Consumers & Fundamentals (45 min)
3. Lab 5: Schema Registry (30 min)
4. Lab 4: Pipelines basics (30 min)

### Full Workshop (4-5 hours)
Complete coverage of WarpStream features:
1. All core labs in order (Lab 0 → Lab 7)

### Production-Focused (3 hours)
For teams preparing to deploy WarpStream:
1. Lab 0: Setup (15 min)
2. Lab 1: Producers, Consumers & Fundamentals (45 min)
3. Lab 2: Agent Groups (30 min)
4. Lab 3: Orbit (30 min) - Migration strategies
5. Lab 6: Tableflow (45 min) - Analytics integration

---

## Prerequisites Check

Before starting, ensure you have:

- [ ] **macOS or Linux** (Windows via WSL2)
- [ ] **Docker Desktop** installed and running
- [ ] **Homebrew** (macOS) or curl (Linux)
- [ ] **At least 4GB RAM** available for Docker
- [ ] **Internet connection** for downloading tools
- [ ] **Port 9092** available (for Kafka)
- [ ] **Ports 9000-9001** available (for MinIO in Lab 4)

---

## Lab Completion Checklist

Track your progress:

- [ ] Lab 0: Setup complete
- [ ] Lab 1: Producers, Consumers & Fundamentals complete
- [ ] Lab 2: Agent Groups complete
- [ ] Lab 3: Orbit complete
- [ ] Lab 4: Pipelines complete
- [ ] Lab 5: Schema Registry complete
- [ ] Lab 6: Tableflow complete
- [ ] Lab 7: Monitoring complete

---

## Getting Help

1. **WarpStream Documentation**: [docs.warpstream.com](https://docs.warpstream.com)
2. **WarpStream Community**: [Community Slack](https://warpstreamcommunity.slack.com)
3. **Performance Tuning**: [WarpStream Performance Tuning](https://docs.warpstream.com/warpstream/kafka/configure-kafka-client/tuning-for-performance)
4. **Bento Documentation**: [warpstreamlabs.github.io/bento](https://warpstreamlabs.github.io/bento/docs/about)

---

**Ready to begin?** Start with [Lab 0: Setup](lab-0-setup.md)
