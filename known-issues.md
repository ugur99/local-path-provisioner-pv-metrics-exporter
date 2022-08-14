

## Known Issues

Some of the known issues are listed below:

  * PVC Names should not be contained as a string in each other. For example, if you have a PVC named `pvc-1` and you have another PVC named `pvc-11`, the exporter will not be able to distinguish between them.
    *  Workaround : Use unique PVC names satisfying the condition stated above across the cluster.
  * If you have a PVC on the tainted nodes like controlplane nodes; you should add tolerations to the exporter job templates. Otherwise, the exporter will not be able to get the PV metrics on the tainted nodes.
    *  Workaround : Add tolerations to the exporter job template.

