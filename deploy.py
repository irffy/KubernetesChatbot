from kubernetes import client, config

def list_deployments():
    # Load Kubernetes configuration from the default location
    config.load_kube_config()

    # Create a Kubernetes API client
    apps_v1 = client.AppsV1Api()

    # List all deployments in the "default" namespace
    namespace = "default"
    deployment_list = apps_v1.list_namespaced_deployment(namespace)

    # Print information about each deployment
    print("Deployments in namespace {}:".format(namespace))
    for deployment in deployment_list.items:
        print("Name: {}\tReplicas: {}\tReady Replicas: {}".format(
            deployment.metadata.name,
            deployment.spec.replicas,
            deployment.status.ready_replicas
        ))

if __name__ == "__main__":
    list_deployments()
