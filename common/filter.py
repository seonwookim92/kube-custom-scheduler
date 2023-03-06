from kubernetes import client, config
from common.monitor import Monitor
from common.utils import convert_unit

class Filter:
    def __init__(self):
        # Load the Kubernetes configuration
        self.config = config.load_kube_config()
        self.monitor = Monitor(cfg=self.config)
        self.pending_pods = self.monitor.get_pending_pods()
        self.running_pods = self.monitor.get_pods("Running")
        self.nodes = self.monitor.get_nodes()

    def check_available(self, pod_name, node_name):    
        # Get the node resources
        node_rsrc = self.monitor.get_node_rsrc(node_name)

        # Get the pod requests
        pod_rqsts = self.monitor.get_pod_rqsts(pod_name)

        # Check if the node has enough resources to run the pod
        cpu_check = int(node_rsrc["cpu"][0].split("m")[0]) >= int(pod_rqsts["cpu"].split("m")[0])
        memory_check = convert_unit(node_rsrc["memory"][0]) >= convert_unit(pod_rqsts["memory"])
        pod_cap_check = int(node_rsrc["pod_cap"][0]) >= 1

        return cpu_check and memory_check and pod_cap_check
    
    def get_available_nodes_name(self, pod_name):
        # Get all the nodes that have enough resources to run the pod
        # Return a list of nodes that have enough resources to run the pod
        nodes_name, _ = self.monitor.get_nodes()
        available_nodes_name = []
        for node_name in nodes_name:
            if self.check_available(pod_name, node_name):
                available_nodes_name.append(node_name)
        return available_nodes_name
