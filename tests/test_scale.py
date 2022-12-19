import time
import statistics
from kubernetes import client, config
import pytest

class Timer:    
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter()
        self.interval = self.end - self.start

constants = {
    "num_pods": 10,
    "tries": 5
}

def run(kube, dep_config):
    initial_count = dep_config.spec.replicas
    scale_up_times = []
    scale_down_times = []
    for i in range(constants["tries"]):
        print(f"Test {i + 1}")
        with Timer() as t:
            kube.patch_namespaced_deployment_scale(
                dep_config.metadata.name,
                dep_config.metadata.namespace,
                {'spec': {'replicas': constants["num_pods"]}}
            )
            i = 1
            while(kube.read_namespaced_deployment(name=dep_config.metadata.name, namespace=dep_config.metadata.namespace).status.ready_replicas != constants["num_pods"]):
                #print(f"sleeping: {1 * i} seconds")
                time.sleep(1 * i)
                i += 1
        scale_up_times.append(t.interval)
        with Timer() as t:
            kube.patch_namespaced_deployment_scale(
                dep_config.metadata.name,
                dep_config.metadata.namespace,
                {'spec': {'replicas': initial_count}}
            )
            i = 1
            while(kube.read_namespaced_deployment(name=dep_config.metadata.name, namespace=dep_config.metadata.namespace).status.replicas != initial_count):
                #print(f"sleeping: {1 * i} seconds")
                time.sleep(1 * i)
                i += 1
        scale_down_times.append(t.interval)
    print(statistics.mean(scale_up_times))
    print(statistics.mean(scale_down_times))





@pytest.mark.benchmark(
    group="group-name",
    min_time=0.1,
    max_time=0.5,
    min_rounds=5,
    timer=time.time,
    disable_gc=True,
    warmup=False
)
def test_scale_10(deployment_name, benchmark):
    config.load_kube_config()
    kube = client.AppsV1Api()

    dep_config = kube.read_namespaced_deployment(name=deployment_name, namespace="default")

    @benchmark
    def result():
        return run(kube, dep_config)

    assert result is None