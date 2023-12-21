#python script that run Flask application and uses html under templates. run this to open web app in browser
from flask import Flask, render_template, request, jsonify
import sys
from kubernetes import client, config
from tabulate import tabulate

app = Flask(__name__)

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

    # Generate a table from the pod data
    table = []
    for pod in pod_list.items:
        table.append([
            pod.metadata.name,
            pod.status.phase,
            len(pod.spec.containers)
        ])

    # Format the table using the tabulate library
    headers = ["Name", "Status", "Container Count"]
    table_str = tabulate(table, headers=headers, tablefmt="html")

    return table_str
def list_deployments(namespace):
    load_kube_config()

    # Create a Kubernetes API client
    apps_v1 = client.AppsV1Api()

    # List all deployments in the specified namespace
    deployment_list = apps_v1.list_namespaced_deployment(namespace)
    #print("\nDeployments in namespace {}:".format(namespace))
    # for deployment in deployment_list.items:
    #     print("Name: {}\tReplicas: {}\tReady Replicas: {}".format(
    #         deployment.metadata.name,
    #         deployment.spec.replicas,
    #         deployment.status.ready_replicas
    #     ))
    table = []
    for deployment in deployment_list.items:
        table.append([
            deployment.metadata.name,
            deployment.spec.replicas,
            deployment.status.ready_replicas
        ])

    # Format the table using the tabulate library
    headers = ["Name", "Replicas", "Ready Replicas"]
    table_str = tabulate(table, headers=headers, tablefmt="html")

    return table_str

def list_services(namespace):
    load_kube_config()

    # Create a Kubernetes API client
    v1 = client.CoreV1Api()

    # List all services in the specified namespace
    service_list = v1.list_namespaced_service(namespace)
    table = []
    for service in service_list.items:
        table.append([
            service.metadata.name,
            service.spec.type,
            service.spec.cluster_ip
        ])

    # Format the table using the tabulate library
    headers = ["Name", "Type", "ClusterIP"]
    table_str = tabulate(table, headers=headers, tablefmt="html")

    return table_str

    # print("\nServices in namespace {}:".format(namespace))
    # for service in service_list.items:
    #     print("Name: {}\tType: {}\tCluster IP: {}".format(
    #         service.metadata.name,
    #         service.spec.type,
    #         service.spec.cluster_ip
    #     ))

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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chatbot", methods=["POST"])
def chatbot():
    message = request.form["message"]

    # Process the user's message and generate a response
    response = process_user_message(message)

    return jsonify({"response": response})

def process_user_message(message):
    # Parse the user's message and determine the appropriate action
    parts = message.lower().split()
    
    if parts[0] == 'list' and len(parts) >= 3:
        resource_type = parts[1]
        namespace = parts[2]
        if resource_type == 'pods':
            return list_pods(namespace)
        if resource_type == 'deployments':
            return list_deployments(namespace)
        if resource_type == 'services':
            return list_services(namespace)
        if resource_type == 'logs':
            return get_pod_logs(namespace)
        # Add conditions for other resource types (e.g., deployments, services) similarly.
    #  
    else:
        return f"Sorry, I couldn't understand the command. Please check the syntax."

if __name__ == "__main__":
    app.run(debug=True)
