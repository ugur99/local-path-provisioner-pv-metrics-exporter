from logger import get_logger
from subprocess import run
from prometheus_client import CollectorRegistry, push_to_gateway
import prometheus_client as prom
import os

directory = '/node/'
registry = CollectorRegistry()
logger = get_logger()

def calculation(dir):
    process = run(['du', '-sb', dir], capture_output=True, text=True)
    size = process.stdout.split()[0]
    return size


try:
  os.environ["NODE_NAME"]
  nodeName = os.environ["NODE_NAME"]
  logger.debug("Node name: %s", nodeName)
except KeyError:
  logger.error("NODE_NAME was not set, please check the env variables.")
  exit(1)

try:
  os.environ["PUSHGATEWAY_ADDRESS"]
except KeyError:
  try:
     os.environ["PUSHGATEWAY_PROMETHEUS_PUSHGATEWAY_SERVICE_HOST"]
     logger.warning("PUSHGATEWAY_ADDRESS was not set, defaulting to PUSHGATEWAY_PROMETHEUS_PUSHGATEWAY_SERVICE_HOST:PUSHGATEWAY_PROMETHEUS_PUSHGATEWAY_SERVICE_PORT")
     registryAddress = os.environ["PUSHGATEWAY_PROMETHEUS_PUSHGATEWAY_SERVICE_HOST"] + ":" + os.environ["PUSHGATEWAY_PROMETHEUS_PUSHGATEWAY_SERVICE_PORT"]
  except KeyError:
    logger.error("PUSHGATEWAY_ADDRESS and PUSHGATEWAY_PROMETHEUS_PUSHGATEWAY_SERVICE_HOST were not set, exiting") 
    exit(1)
else:
  registryAddress = os.environ["PUSHGATEWAY_ADDRESS"]
  logger.debug("Pushgateway address: %s", registryAddress)  

try:
  os.environ["PVC_NAMES"]
  pvc = os.environ["PVC_NAMES"]
  logger.debug("PVC names: %s", pvc)
except KeyError:
  logger.error("PVC_NAMES was not set, please check the env variables.")
  exit(1)

try:
  os.environ["POD_NAME"]
  podName = os.environ["POD_NAME"]
  logger.debug("Pod name: %s", podName)
except KeyError:
  logger.error("POD_NAME was not set, please check the env variables.")
  exit(1)


claims=pvc.split(',')
logger.debug("PVC_NAMES: " + str(claims))
gauge = prom.Gauge('local_volume_stats_used_bytes', 'local volume storage usage', ['persistentvolumeclaim','node'], registry=registry)

for i in os.listdir(directory):
    for j in range(len(claims)):
        # IF PVC NAMES ARE NOT UNIQUE, THIS WILL NOT WORK
        # TODO: FIX THIS TO HANDLES PVC NAMES WITH CONTAINING THE SAME STRING; E.G. pvc1, pvc11, pvc111
        if claims[j] in i:
            filename=(directory+"/"+i)
            logger.debug("Found PVC: " + claims[j] + " in directory: " + filename)
            gauge.labels(claims[j],nodeName).set(calculation(filename))
            #push_to_gateway(registryAddress, job="projectalpha", registry=registry)
            jobName = nodeName + "_" + "usage_metrics" 
            push_to_gateway(registryAddress, job=jobName, registry=registry)
            logger.debug("Pushed metrics to registry: " + registryAddress)
