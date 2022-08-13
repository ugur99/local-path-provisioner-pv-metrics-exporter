

## Known Issues

Some of the known issues are listed below:

  * PVC Names should be contained as a string in other strings. For example, if you have a PVC named `pvc-1` and you have another PVC named `pvc-11`, the exporter will not be able to distinguish between them. This is a known issue and will be fixed in the future.
    *  Workaround : Use unique PVC names across the cluster.
  * If you have a PVC on the tainted nodes; you should add tolerations to the exporter deployment. Otherwise, the exporter will not be able to get the PV metrics on the tainted nodes.
    *  Workaround : Add tolerations to the exporter deployment.
  * Docker Image size should be minimized. Since our loop waits for 30 seconds, if docker images can not be pulled in this range, also depending on network latency, and previous job is not finished, it leads a conflict. It is a problem that we can face with only new image pulling.
    *  Workaround : Once both images pulled, rollout restart to deployment fixes the problem.
  * Currently it is assumed that `/opt/local-path-provisioner` which is the default path is used for the local-path-provisioner. If you use a different path, you should change the path in the job template. It should given as an environment variable.
    *  Workaround : Job template can be manipulated manually.