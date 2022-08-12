from subprocess import run
from prometheus_client import CollectorRegistry, push_to_gateway
import prometheus_client as prom
import os

directory = '/node/'
registry = CollectorRegistry()

def calculation(dir):
    process = run(['du', '-sb', dir], capture_output=True, text=True)
    size = process.stdout.split()[0]
    return size

for key in os.environ:
    nodeName = os.environ["NODE_NAME"]
    pvc = os.environ["PVC_NAMES"]
    podName = os.environ["POD_NAME"]
    registryUrl = os.environ["PUSHGATEWAY_PROMETHEUS_PUSHGATEWAY_SERVICE_HOST"] + ":" + os.environ["PUSHGATEWAY_PROMETHEUS_PUSHGATEWAY_SERVICE_PORT"]


claims=pvc.split(',')
gauge = prom.Gauge('local_volume_stats_used_bytes', 'local volume storage usage', ['persistentvolumeclaim','node'], registry=registry)

for i in os.listdir(directory):
    for j in range(len(claims)):
        # IF PVC NAMES ARE NOT UNIQUE, THIS WILL NOT WORK
        # TODO: FIX THIS TO HANDLES PVC NAMES WITH CONTAINING THE SAME STRING; E.G. pvc1, pvc11, pvc111
        if claims[j] in i:
            filename=(directory+"/"+i)
            gauge.labels(claims[j],nodeName).set(calculation(filename))
            push_to_gateway(registryUrl, job="projectalpha", registry=registry)
