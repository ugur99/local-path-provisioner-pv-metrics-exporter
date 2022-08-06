from kubernetes import client, config, utils
import time, os, shutil
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import prometheus_client as prom

config.load_kube_config("templates/kubeconfig")
v1 = client.CoreV1Api()
registry = CollectorRegistry()
pvcs = v1.list_persistent_volume_claim_for_all_namespaces(watch=False)
gauge = prom.Gauge('local_volume_stats_capacity_bytes', 'local volume capacity', ['persistentvolumeclaim','node'], registry=registry)
node_list = []
all_pvc_list = []

# ------------------------------------------------------------ SA Integration
#configuration = client.Configuration()
#configuration.api_key["authorization"] = '<bearer_token>'
#configuration.api_key_prefix['authorization'] = 'Bearer'
#configuration.host = 'https://<ip_of_api_server>'
#configuration.ssl_ca_cert = '<path_to_cluster_ca_certificate>'
#v1 = client.CoreV1Api(client.ApiClient(configuration))
# ------------------------------------------------------------


for key in os.environ:
    if os.environ["STORAGE_CLASS_NAME"]:
      storageClass = os.environ["STORAGE_CLASS_NAME"]
    if os.environ["PROMETHEUS_PUSHGATEWAY_URL"]:
      registryUrl = os.environ["PROMETHEUS_PUSHGATEWAY_URL"]


def convert_size_string_to_bytes(size):
    unit = size[-2:]
    sz = float(size[:-2])
    if unit == 'bi':
        return sz
    elif unit == 'Ki':
        return sz * 1024**1
    elif unit == 'Mi':
        return sz * 1024**2
    elif unit == 'Gi':
        return sz * 1024**3
    elif unit == 'Ti':
        return sz * 1024**4
    elif unit == 'Pi':
        return sz * 1024**5
    elif unit == 'Ei':
        return sz * 1024**6
    else:
        exit(1)

while True:
  time.sleep(30)
  pvcs = v1.list_persistent_volume_claim_for_all_namespaces(watch=False)
  
  for pvc in pvcs.items:
  
      if pvc.spec.storage_class_name == storageClass:
  
        capacity = convert_size_string_to_bytes(pvc.spec.resources.requests['storage'])
        gauge.labels(pvc.metadata.name,pvc.metadata.annotations['volume.kubernetes.io/selected-node']).set(capacity)
        push_to_gateway(registryUrl, job="projectbeta", registry=registry)
  
        if pvc.metadata.annotations['volume.kubernetes.io/selected-node'] not in node_list:
          node_list += [pvc.metadata.annotations['volume.kubernetes.io/selected-node']]
  
        all_pvc_list += [pvc.metadata.name]
        all_pvc_list_string = ",".join(all_pvc_list)
  
  for node in node_list:
  
    k8s_client = client.ApiClient()
  
    shutil.copyfile("templates/job.yaml","job.yaml")
  
    yaml_file = 'job.yaml'
  
    fin = open(yaml_file, "rt")
    data = fin.read()
    data = data.replace('NODES', node)
    data = data.replace('CLAIMS', all_pvc_list_string)
    fin.close()
    fin = open(yaml_file, "wt")
    fin.write(data)
    fin.close()
  
    utils.create_from_yaml(k8s_client,yaml_file,namespace="sisyphus",verbose=True)
    time.sleep(30)
  

