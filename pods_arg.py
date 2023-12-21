import sys
from kubernetes import client, config

def get_pods(namespace):
    # Load Kubernetes configuration from the default location
    config.load_kube_config()

    # Create a Kubernetes API client
    v1 = client.CoreV1Api()

    # List all pods in the specified namespace
    pod_list = v1.list_namespaced_pod(namespace)

    # Print information about each pod
    print("Pods in namespace {}:".format(namespace))
    for pod in pod_list.items:
        print("Name: {}\tStatus: {}\tContainer Count: {}".format(
            pod.metadata.name,
            pod.status.phase,
            len(pod.spec.containers)
        ))

if __name__ == "__main__":
    # Check if a namespace argument is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <namespace>")
        sys.exit(1)

    namespace_arg = sys.argv[1]
    get_pods(namespace_arg)
