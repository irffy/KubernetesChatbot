import sys
from kubernetes import client, config

def list_deployments(namespace):
    # Load Kubernetes configuration from the default location
    config.load_kube_config()

    # Create a Kubernetes API client
    apps_v1 = client.AppsV1Api()

    # List all deployments in the specified namespace
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
    # Check if a namespace argument is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <namespace>")
        sys.exit(1)

    namespace_arg = sys.argv[1]
    list_deployments(namespace_arg)
