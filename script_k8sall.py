import sys
from kubernetes import client, config

def load_kube_config():
    try:
        config.load_kube_config()
    except Exception as e:
        print(f"Error loading Kubernetes configuration: {e}")
        sys.exit(1)

def list_pods(namespace):
    load_kube_config()

    # Create a Kubernetes API client
    v1 = client.CoreV1Api()

    # List all pods in the specified namespace
    pod_list = v1.list_namespaced_pod(namespace)
    print("Pods in namespace {}:".format(namespace))
    for pod in pod_list.items:
        print("Name: {}\tStatus: {}\tContainer Count: {}".format(
            pod.metadata.name,
            pod.status.phase,
            len(pod.spec.containers)
        ))

def list_deployments(namespace):
    load_kube_config()

    # Create a Kubernetes API client
    apps_v1 = client.AppsV1Api()

    # List all deployments in the specified namespace
    deployment_list = apps_v1.list_namespaced_deployment(namespace)
    print("\nDeployments in namespace {}:".format(namespace))
    for deployment in deployment_list.items:
        print("Name: {}\tReplicas: {}\tReady Replicas: {}".format(
            deployment.metadata.name,
            deployment.spec.replicas,
            deployment.status.ready_replicas
        ))

def list_services(namespace):
    load_kube_config()

    # Create a Kubernetes API client
    v1 = client.CoreV1Api()

    # List all services in the specified namespace
    service_list = v1.list_namespaced_service(namespace)
    print("\nServices in namespace {}:".format(namespace))
    for service in service_list.items:
        print("Name: {}\tType: {}\tCluster IP: {}".format(
            service.metadata.name,
            service.spec.type,
            service.spec.cluster_ip
        ))

def get_pod_logs(namespace, pod_name, container_name=None):
    load_kube_config()

    # Create a Kubernetes API client
    v1 = client.CoreV1Api()

    # Get logs from a specific pod in the specified namespace
    try:
        logs = v1.read_namespaced_pod_log(name=pod_name, namespace=namespace, container=container_name)
        print("\nLogs from pod {} in namespace {}:".format(pod_name, namespace))
        print(logs)
    except Exception as e:
        print("Error retrieving logs: {}".format(e))

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    print(len(sys.argv))
    if len(sys.argv) < 3:
        print("Usage: python script.py <namespace> <resource_type> [<pod_name> [logs]]")
        sys.exit(1)

    namespace_arg = sys.argv[1]
    resource_type_arg = sys.argv[2]

    # Create a dictionary to map resource types to functions
    resource_functions = {
        'pod': list_pods,
        'deployment': list_deployments,
        'service': list_services,
    }

    # Call the appropriate function based on the resource type
    if resource_type_arg.lower() in resource_functions:
        resource_functions[resource_type_arg.lower()](namespace_arg)

    # Check if an additional argument (pod name) is provided for log retrieval
    if len(sys.argv) == 5 and sys.argv[4].lower() == 'logs':
        pod_name_arg = sys.argv[3]
        get_pod_logs(namespace_arg, pod_name_arg)
    elif len(sys.argv) == 6 and sys.argv[5].lower() == 'logs':
        pod_name_arg = sys.argv[3]
        container_name_arg = sys.argv[4]
        get_pod_logs(namespace_arg, pod_name_arg, container_name_arg)
