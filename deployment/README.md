## Deployment

As a requirementi you need to have prometheus pushgateway installed in your cluster. You can install it by using the [pushgateway helm chart](https://artifacthub.io/packages/helm/prometheus-community/prometheus-pushgateway). 

You can apply the deployment files in the [deployment](deployment.yaml) page to your cluster. You may want to change the namespace of the resources depending on your cluster configuration/preferences. Some environement variables are defined in the deployment files. You can change them according to your needs.

```
          # If pushgateway helm release name is different from "pushgateway" OR 
          # your puhsgateway deployment is not in the same namespace as this deployment
          # then you should specify pushgateway address as an environment variable
          # TODO: PUSHGATEWAY_URL VARIABLE NAME WILL BE REPLACED BY PUSHGATEWAY_ADDRESS
          - name: PUSHGATEWAY_URL 
            value: "10.99.84.233:9091"

          # If storage class name is different from "local-path" then you 
          # should specify it here
          - name: STORAGE_CLASS_NAME
            value: "local-path"

          # Default Log Level is INFO
          - name: LOG_LEVEL
            value: "INFO"

          # Default Job Log Level is DEBUG
          - name: JOB_LOG_LEVEL
            value: "DEBUG"
```