from kubernetes import client, config
from common.monitor import Monitor
from common.filter import Filter
from fcfs.strategy import FCFS

class Scheduler:
    def __init__(self, cfg=None, strategy=FCFS()):
        # Load the Kubernetes configuration
        if cfg is None:
            self.config = config.load_kube_config()
        else:
            self.config = cfg

        # Load the Kubernetes API client
        self.core_api = client.CoreV1Api()
        self.monitor = Monitor(cfg=self.config)
        self.filter = Filter()
        self.strategy = strategy

    def decision(self):
        pod, node_score = self.strategy.scoring()
        print(f"pod: {pod}, node_score: {node_score}")
        if pod is None:
            return None
        else:
            # Get the node with the highest score
            node = max(node_score, key=node_score.get)
            return (pod, node)
    
    def scheduling(self, pod, node):
        # Bind the pod to the node
        self.core_api.patch_namespaced_pod(pod, "default", {"spec": {"nodeName": node}})
        print(f"Pod {pod} scheduled on node {node}")
