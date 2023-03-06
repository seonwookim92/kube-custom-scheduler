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
        output = self.strategy.scoring()
        pod = output['pod']
        node_score = output['node_score']
        print(f"pod: {pod}, node_score: {node_score}")
        
        if pod is None:
            return None
        else:
            # Get the node with the highest score
            node = max(node_score, key=node_score.get)
            return (pod, node)
    
    def scheduling(self, pod, node):
        # Binding the pod to the node
        body = client.V1Binding(
            metadata=client.V1ObjectMeta(
                name=pod,
                namespace="default"
            ),
            target=client.V1ObjectReference(
                api_version="v1",
                kind="Node",
                name=node,
                namespace="default"
            )
        )
        self.core_api.create_namespaced_binding(
            body=body,
            namespace="default"
        )
        print(f"Pod {pod} is scheduled to node {node}")