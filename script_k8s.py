import sys
from kubernetes import client, config

def list_resources(namespace, resource_type):
    # Load Kubernetes configuration from the default location
    config.load_kube_config()

    # Create Kubernetes API clients
    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()

    if resource_type.lower() == "pod":
        # List pods in the specified namespace
        pod_list = v1.list_namespaced_pod(namespace)
        print("Pods in namespace {}:".format(namespace))
        for pod in pod_list.items:
            print("Name: {}\tStatus: {}\tContainer Count: {}".format(
                pod.metadata.name,
                pod.status.phase,
                len(pod.spec.containers)
            ))
    elif resource_type.lower() == "deployment":
        # List deployments in the specified namespace
        deployment_list = apps_v1.list_namespaced_deployment(namespace)
        print("Deployments in namespace {}:".format(namespace))
        for deployment in deployment_list.items:
            print("Name: {}\tReplicas: {}\tReady Replicas: {}".format(
                deployment.metadata.name,
                deployment.spec.replicas,
                deployment.status.ready_replicas
            ))
    elif resource_type.lower() == "service":
        # List services in the specified namespace
        service_list = v1.list_namespaced_service(namespace)
        print("Services in namespace {}:".format(namespace))
        for service in service_list.items:
            print("Name: {}\tType: {}\tCluster IP: {}".format(
                service.metadata.name,
                service.spec.type,
                service.spec.cluster_ip
            ))
    else:
        print("Invalid resource type. Supported types: 'pod', 'deployment', or 'service'")
        sys.exit(1)

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    print(len(sys.argv))
    if len(sys.argv) != 3:
        print("Usage: python script.py <namespace> <resource_type>")
        sys.exit(1)

    namespace_arg = sys.argv[1]
    resource_type_arg = sys.argv[2]
    list_resources(namespace_arg, resource_type_arg)
