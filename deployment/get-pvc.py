from kubernetes import client, config, utils
import time, os, shutil
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import prometheus_client as prom

config.load_kube_config("templates/kubeconfig")

#configuration = client.Configuration()
#configuration.api_key["authorization"] = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjM3UFI0RTUtWVctTnNQeTZ1ZWU5RndieGtzUUhGODB4SGtYb1dSVTVjYnMifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNjU5ODYwMTk4LCJpYXQiOjE2NTk4NTY1OTgsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJzaXN5cGh1cyIsInNlcnZpY2VhY2NvdW50Ijp7Im5hbWUiOiJleHBvcnRlciIsInVpZCI6ImYzMTcxNTM1LTU0ZTktNGQyNi05NGQwLWE2NjUyNjU5ZTM2NiJ9fSwibmJmIjoxNjU5ODU2NTk4LCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6c2lzeXBodXM6ZXhwb3J0ZXIifQ.mgWh6SFMF3xhFue7Q17Dy2WU0rec04nPIkNpkyvrjDH43Voo30DwJgcc3icyXk5AOJBMxxpDQhLla9950C6TvAuvba7Q1cZgNzdMw7NdN6Dhz7A27haXgW6pZGlCI3qsKVJfLAXoy3aknTI4CUu3N0fV8FoekC5ic3slzgtSlKCi8C344IGmLKaRupJ0dAkKZYYB9igFkS9SLnSizkkI78oVjcoj9dJiHisrsB7k-4NwCiXrhxeZZQcFRemswNPFCxL32d_Va6FBX-BvxDvcCAP78hQE-4k4tO4sHcCiQUKzZOn6cJGxKJEKlbUF-cvaw_eAWgP17VhmnyFepsVV6Q'
#configuration.api_key_prefix['authorization'] = 'Bearer'
#configuration.host = 'https://192.168.0.24:6443'
#configuration.ssl_ca_cert = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'

v1 = client.CoreV1Api()
#v1 = client.CoreV1Api(client.ApiClient(configuration))

registry = CollectorRegistry()
pvcs = v1.list_persistent_volume_claim_for_all_namespaces(watch=False)
gauge = prom.Gauge('local_volume_stats_capacity_bytes', 'local volume capacity', ['persistentvolumeclaim','node'], registry=registry)
node_list = []
all_pvc_list = []


for key in os.environ:
    if os.environ["STORAGE_CLASS_NAME"]:
      storageClass = os.environ["STORAGE_CLASS_NAME"]
    if os.environ["PUSHGATEWAY_PROMETHEUS_PUSHGATEWAY_SERVICE_HOST"]:
      registryUrl = os.environ["PUSHGATEWAY_PROMETHEUS_PUSHGATEWAY_SERVICE_HOST"] + ":" + os.environ["PUSHGATEWAY_PROMETHEUS_PUSHGATEWAY_SERVICE_PORT"]

#registryUrl = "10.99.84.233:9091"

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
        if pvc.status.phase == "Bound":
  
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
  
