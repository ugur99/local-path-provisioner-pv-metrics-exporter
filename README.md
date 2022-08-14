# Local Path Provisioner Metrics Exporter
[![Docker Build](https://github.com/ugur99/local-path-pv-metrics-exporter/actions/workflows/docker-image.yml/badge.svg?branch=main)](https://github.com/ugur99/local-path-pv-metrics-exporter/actions/workflows/docker-image.yml) [![Vulnerability Scanning](https://github.com/ugur99/local-path-pv-metrics-exporter/actions/workflows/scan.yml/badge.svg?branch=main)](https://github.com/ugur99/local-path-pv-metrics-exporter/actions/workflows/scan.yml)

This is a simple metrics exporter for the [local-path-provisioner](https://github.com/rancher/local-path-provisioner) or any `hostPath` typed PersistentVolumes that share the same provisioned path on the hosts. It generates `local_volume_stats_capacity_bytes` and `local_volume_stats_used_bytes` metrics for the persistent volumes `PV`  based on the `hostPath` solution.

## Getting Started

Easy deployment of local-path-provisioner made it one of the most popular dynamic PV provisioning tool, especially used in dev environment. Since the local-path-provisioner is a `hostPath` based solution, It does not support any integrations to generate metrics such `kubelet_volume_stats_used_bytes` or `kubelet_volume_stats_capacity_bytes`. Some use cases and warnings for the `hostPath` solution are listed on the [kubernetes documentation](https://kubernetes.io/docs/concepts/storage/volumes/#hostpath). But since local-path-provisioner provides a dynamic provisioning solution it is a good alternative for development and testing environments in which data loss can be tolerated.

Another alternative is `local` typed ones, but there are some limitations to use `local` type volumes too as stated in [sig-storage-local-static-provisioner best practices](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/best-practices.md). So unless we have seperate partitions for each PV, we cannot use the metrics `kubelet_volume_stats.*` effectively, because it will show the total capacity and used bytes of the whole partition not the PV. Also It does not support `dynamic provisioning` and thats the another critical point for development and testing environments.

## Architecture
We have two main components in this solution:

### lp-exporter
 The first one is the `lp-exporter` which talks to the API Server to get PVC names which used local-path storage class and requested capacities of them respectively. It generates `local_volume_stats_capacity_bytes` metrics and pushes it to [pushgateway](https://github.com/prometheus/pushgateway). To get the used bytes for per PV, it generates a `job` for each different nodes that PVs are provisioned.
 
### lp-exporter-job
Jjob consists of a simple python code blockk to get used bytes for each PVs that are provisioned on that node and it pushes the `local_volume_stats_used_bytes` metrics to the pushgateway.
![mainarchitecture](src/images/architecture-01.png)
>Simple Illustration of the architecture

## Grafana Dashboard && Prometheus Alerts
Take a look [grafana dashboard examples](grafana/README.md) and [alert examples](alertmanager/README.md) rules.

## How to use?

For deployment and usage, please take a look at the [deployment](deployment/README.md) page.

## Known Issues

Some known issues are listed in the [issues](known-issues.md) page.

## Disclaimer

`This is not an official solution. It is just a simple solution to generate metrics for local-path-provisioner by using prometheus/kubernetes python clients and prometheus pushgateway. It is not tested in a production environment.`
