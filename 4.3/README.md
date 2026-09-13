# Exercise 4.04

## PromQL Query
```promql
kube_pod_info{namespace="prometheus", created_by_kind="StatefulSet"}
```

## Output Sample
```json
{
  "app_kubernetes_io_version": "2.20.0",
  "created_by_kind": "StatefulSet",
  "created_by_name": "prom-alertmanager",
  "helm_sh_chart": "kube-state-metrics-8.4.0",
  "host_ip": "172.18.0.2",
  "host_network": "false",
  "instance": "10.42.0.108:8080",
  "job": "kubernetes-service-endpoints",
  "namespace": "prometheus",
  "node": "k3d-k3s-default-server-0",
  "pod": "prom-alertmanager-0",
  "pod_ip": "10.42.0.112",
  "service": "prom-kube-state-metrics",
  "uid": "a7f0141c-df03-449a-8655-ba44aee9b332"
}
