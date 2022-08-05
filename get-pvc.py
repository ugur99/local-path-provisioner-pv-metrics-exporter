from kubernetes import client, config, utils
import time

config.load_kube_config()
v1 = client.CoreV1Api()

# ------------------------------------------------------------ SA Integration
#configuration = client.Configuration()
#configuration.api_key["authorization"] = '<bearer_token>'
#configuration.api_key_prefix['authorization'] = 'Bearer'
#configuration.host = 'https://<ip_of_api_server>'
#configuration.ssl_ca_cert = '<path_to_cluster_ca_certificate>'
#v1 = client.CoreV1Api(client.ApiClient(configuration))
# ------------------------------------------------------------

while True:
  pvcs = v1.list_persistent_volume_claim_for_all_namespaces(watch=False)

  #print("---- PVCs ---")
  #print("%-35s\t%-40s\t%-6s\t%-15s" % ("Name", "Volume", "Size", "Node"))

  for pvc in pvcs.items:
      if pvc.spec.storage_class_name == "local-path":
        #print("%-35s\t%-40s\t%-6s\t%-15s" % (pvc.metadata.name, pvc.spec.volume_name, pvc.spec.resources.requests['storage'],pvc.metadata.annotations['volume.kubernetes.io/selected-node']))

        node_list = []
        node_list += [pvc.metadata.annotations['volume.kubernetes.io/selected-node']]

        test_list = []
        test_list += [pvc.metadata.name]
        persistent_volume_claim_list = ",".join(test_list)


  for node in node_list:
    k8s_client = client.ApiClient()
    yaml_file = 'job.yml'

    fin = open(yaml_file, "rt")
    data = fin.read()
    data = data.replace('NODE', node)
    data = data.replace('CLAIMS', persistent_volume_claim_list)
    fin.close()
    fin = open(yaml_file, "wt")
    fin.write(data)
    fin.close()

    utils.create_from_yaml(k8s_client,yaml_file,verbose=True)
    
    time.sleep(120)


