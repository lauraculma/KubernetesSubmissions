

Submissions for the DevOps with Kubernetes course.

## Exercises

### Chapter 2

- [1.1](https://github.com/lauraculma/KubernetesSubmissions/tree/1.1/log_output)
- [1.2](https://github.com/lauraculma/KubernetesSubmissions/tree/1.2)
- [1.3](https://github.com/lauraculma/KubernetesSubmissions/tree/1.3)
- [1.4](https://github.com/lauraculma/KubernetesSubmissions/tree/1.4)
- [1.5](https://github.com/lauraculma/KubernetesSubmissions/tree/1.5)
- [1.6](https://github.com/lauraculma/KubernetesSubmissions/tree/1.6)
- [1.7](https://github.com/lauraculma/KubernetesSubmissions/tree/1.7)
- [1.8](https://github.com/lauraculma/KubernetesSubmissions/tree/1.8)
- [1.9](https://github.com/lauraculma/KubernetesSubmissions/tree/1.9)
- [1.10](https://github.com/lauraculma/KubernetesSubmissions/tree/1.10)
- [1.11](https://github.com/lauraculma/KubernetesSubmissions/tree/1.11)
- [1.12](https://github.com/lauraculma/KubernetesSubmissions/tree/1.12)
- [1.13](https://github.com/lauraculma/KubernetesSubmissions/tree/1.13)

### Chapter 3
- [2.1](https://github.com/lauraculma/KubernetesSubmissions/tree/2.1)
- [2.2](https://github.com/lauraculma/KubernetesSubmissions/tree/2.2)
- [2.3](https://github.com/lauraculma/KubernetesSubmissions/tree/2.3)
- [2.4](https://github.com/lauraculma/KubernetesSubmissions/tree/2.4)
- [2.5](https://github.com/lauraculma/KubernetesSubmissions/tree/2.5)
- [2.6](https://github.com/lauraculma/KubernetesSubmissions/tree/2.6)
- [2.7](https://github.com/lauraculma/KubernetesSubmissions/tree/2.7)
- [2.8](https://github.com/lauraculma/KubernetesSubmissions/tree/2.8)
- [2.9](https://github.com/lauraculma/KubernetesSubmissions/tree/2.9)
- [2.10](https://github.com/lauraculma/KubernetesSubmissions/tree/2.10)


### Chapter 4
- [3.1](https://github.com/lauraculma/KubernetesSubmissions/tree/3.1)
- [3.2](https://github.com/lauraculma/KubernetesSubmissions/tree/3.2)
- [3.3](https://github.com/lauraculma/KubernetesSubmissions/tree/3.3)
- [3.4](https://github.com/lauraculma/KubernetesSubmissions/tree/3.4)
- [3.5](https://github.com/lauraculma/KubernetesSubmissions/tree/3.5)
- [3.6](https://github.com/lauraculma/KubernetesSubmissions/tree/3.6)
- [3.7](https://github.com/lauraculma/KubernetesSubmissions/tree/3.7)
- [3.8](https://github.com/lauraculma/KubernetesSubmissions/tree/3.8)
- [3.9](https://github.com/lauraculma/KubernetesSubmissions/tree/3.9)

## Database Hosting Comparison: Self-Hosted in Kubernetes (StatefulSet) vs. Managed Database (DBaaS / Google Cloud SQL)

| Evaluation Criteria | Self-Hosted in Kubernetes (StatefulSet + PVC) | Cloud Managed Service (e.g., Google Cloud SQL / AWS RDS) |
| :--- | :--- | :--- |
| **Initial Setup & Effort** | **Pros:** No cloud provider account or DBaaS configuration required; fully defined via standard manifests.<br>**Cons:** Requires writing and managing manifests (`StatefulSet`, `Headless Service`, `PVC`, storage classes). | **Pros:** Turnkey provisioning (via UI, CLI, or Terraform) with native security defaults.<br>**Cons:** Requires cloud account configuration, IAM permissions, VPC peering, and Secrets integration. |
| **Direct Costs** | **Pros:** Zero additional license/service cost beyond existing node compute/disk resources.<br>**Cons:** Requires node instance capacity with sufficient persistent disk IOPS and memory. | **Pros:** Predictable operational cost scaling and optional serverless/on-demand tiers.<br>**Cons:** Noticeably more expensive due to managed service markups, egress, and per-instance fees. |
| **Operational Maintenance** | **Pros:** Full access to DB engine configurations, extensions, and logs inside the pod.<br>**Cons:** High operational overhead. Upgrades, failover, node draining, and storage expansion require manual intervention. | **Pros:** Zero-maintenance patching, automatic OS/engine updates, automated point-in-time recovery, and auto-scaling disk.<br>**Cons:** Limited access to low-level OS configuration and proprietary extensions. |
| **High Availability & Failover** | **Pros:** Can achieve HA with specialized operators (e.g., Zalando or CloudNativePG).<br>**Cons:** Basic StatefulSets offer single-node recovery only, which incurs downtime during node failures. | **Pros:** Out-of-the-box multi-zone high availability with automated replica failover.<br>**Cons:** Provider lock-in and potential network hop latency outside of internal VPC peering. |
| **Backups & Restore Ease** | **Pros:** Low tool costs; can script `pg_dump` jobs or PV volume snapshots via CSI drivers.<br>**Cons:** Manual restore verification, complex Point-In-Time-Recovery (PITR), and snapshot orchestration. | **Pros:** Automated daily snapshots, continuous WAL archiving, 1-click PITR restores, and retention policies.<br>**Cons:** Snapshot storage costs accumulate and data extraction can be slow for large volumes. |

### Conclusion
* **Self-hosted (StatefulSet)** is ideal for local development, CI/CD testing pipelines, small non-critical services, or situations where cost optimization is prioritized over operational labor.
* **Managed Database (DBaaS)** is the industry standard for production workloads due to minimal operational risk, automated backup lifecycles, built-in disaster recovery, and high availability guarantees.
