from kubernetes import client, config
from common.monitor import Monitor
from common.filter import Filter

class FCFS:
    def __init__(self, cfg=None):
        # Load the Kubernetes configuration
        if cfg is None:
            self.config = config.load_kube_config()
        else:
            self.config = cfg

        # Load the Kubernetes API client
        self.core_api = client.CoreV1Api()
        self.monitor = Monitor(cfg=self.config)
        self.filter = Filter()

    def scoring(self):
        # Check if there are pending pods
        # If there are no pending pods, return None
        # If there are pending pods, get the score of the available nodes

        # Get the pending pods
        pending_pods_name, _ = self.monitor.get_pending_pods()
        FCFS_output = {}

        if len(pending_pods_name) == 0:
            FCFS_output['pod'] = None
            FCFS_output['node_score'] = None
            return FCFS_output
        else:
            pod_name = pending_pods_name[0]
            # Get the available nodes
            available_nodes_name = self.filter.get_available_nodes_name(pod_name)
            # Get the score of the available nodes
            # The more running pods a node has, the lower the score
            FCFS_output['pod'] = pod_name
            node_score = {}
            for node in available_nodes_name:
                # Exclude the controlplane node
                if node == "controlplane" or node == "node-0":
                    continue
                node_score[node] = 100 - len(self.monitor.get_running_pods(node))
            FCFS_output['node_score'] = node_score
            
        # Return the node_score dictionary
        return FCFS_output

        