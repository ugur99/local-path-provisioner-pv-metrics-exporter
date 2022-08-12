from kubernetes import client, utils
from prometheus_client import CollectorRegistry, push_to_gateway
import prometheus_client as prom
import incluster_config, helper,time, os, shutil, logging


v1 = client.CoreV1Api(client.ApiClient(incluster_config.load_incluster_config()))
registry = CollectorRegistry()

logger = logging.getLogger("exporterLogger")
logger.setLevel(logging.DEBUG)
ConsoleOutputHandler = logging.StreamHandler()
ConsoleOutputHandler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ConsoleOutputHandler.setFormatter(formatter)
logger.addHandler(ConsoleOutputHandler)

pvcs = v1.list_persistent_volume_claim_for_all_namespaces(watch=False)
gauge = prom.Gauge('local_volume_stats_capacity_bytes', 'local volume capacity', ['persistentvolumeclaim','node'], registry=registry)
node_list = []
all_pvc_list = []

try:
  storageClass = os.environ["STORAGE_CLASS_NAME"]
except KeyError:
  logger.warning("STORAGE_CLASS_NAME not set, defaulting to local-path")
else:
  storageClass = "local-path"
try:
  registryUrl = os.environ["PUSHGATEWAY_URL"]
except KeyError:
  logger.warning("PUSHGATEWAY_URL not set, defaulting to PUSHGATEWAY_PROMETHEUS_PUSHGATEWAY_SERVICE_HOST:PUSHGATEWAY_PROMETHEUS_PUSHGATEWAY_SERVICE_PORT")
else:
  registryUrl = os.environ["PUSHGATEWAY_PROMETHEUS_PUSHGATEWAY_SERVICE_HOST"] + ":" + os.environ["PUSHGATEWAY_PROMETHEUS_PUSHGATEWAY_SERVICE_PORT"]


while True:
  logger.info("Sleeping for 30 seconds...")
  time.sleep(30)

  pvcs = v1.list_persistent_volume_claim_for_all_namespaces(watch=False)

  all_pvc_list = []
  all_pvc_list_string = []
  node_list = []
  
  logger.debug("storageClass: " + storageClass + " registryUrl: " + registryUrl)

  for pvc in pvcs.items:
    logger.debug("PVC: " + pvc.metadata.name + " in namespace: " + pvc.metadata.namespace + " has storage class: " + pvc.spec.storage_class_name)
    if pvc.spec.storage_class_name == storageClass:
      if pvc.status.phase == "Bound":

        capacity = helper.convert_size_string_to_bytes(pvc.spec.resources.requests['storage'])
        gauge.labels(pvc.metadata.name,pvc.metadata.annotations['volume.kubernetes.io/selected-node']).set(capacity)
        push_to_gateway(registryUrl, job="projectbeta", registry=registry)
        logger.debug("Pushed to registry: " + registryUrl + " job: projectbeta")
  
        if pvc.metadata.annotations['volume.kubernetes.io/selected-node'] not in node_list:
          node_list += [pvc.metadata.annotations['volume.kubernetes.io/selected-node']]
  
        all_pvc_list += [pvc.metadata.name]
      else:
        logger.debug("Ignored...")
  
  all_pvc_list_string = ",".join(all_pvc_list)
  logger.debug("all_pvc_list_string: " + all_pvc_list_string)
  
  for node in node_list:
  
    k8s_client = client.ApiClient(incluster_config.load_incluster_config())

    # TODO: CREATE A NEW METHOD CALLED create_job instead of applying a template job file.
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
  
    utils.create_from_yaml(k8s_client,yaml_file,namespace="sisyphus")

    # TODO: WRITE A CONTROL BLOCK TO CHECK SUCCESS OF JOB
  
