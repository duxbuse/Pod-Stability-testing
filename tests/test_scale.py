import time
import statistics
from kubernetes import client, config
import pytest
from collections import namedtuple

deployment_config = namedtuple('deployment_config', ['kube', 'config'])

class Timer:    
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter()
        self.interval = self.end - self.start


def scale_up(deployment_config, max_pod_count):
    initial_count = deployment_config.config.spec.replicas
    scale_up_times = []
    scale_down_times = []

    with Timer() as t:
        deployment_config.kube.patch_namespaced_deployment_scale(
            deployment_config.config.metadata.name,
            deployment_config.config.metadata.namespace,
            {'spec': {'replicas': max_pod_count}}
        )
        while(deployment_config.kube.read_namespaced_deployment(name=deployment_config.config.metadata.name, namespace=deployment_config.config.metadata.namespace).status.ready_replicas != max_pod_count):
            time.sleep(1)

    scale_up_times.append(t.interval)

    with Timer() as t:
        deployment_config.kube.patch_namespaced_deployment_scale(
            deployment_config.config.metadata.name,
            deployment_config.config.metadata.namespace,
            {'spec': {'replicas': initial_count}}
        )
        while(deployment_config.kube.read_namespaced_deployment(name=deployment_config.config.metadata.name, namespace=deployment_config.config.metadata.namespace).status.replicas != initial_count):
            time.sleep(1)

    scale_down_times.append(t.interval)
    
    print(statistics.mean(scale_up_times))
    print(statistics.mean(scale_down_times))



@pytest.fixture
def load_config(deployment_name):
    config.load_kube_config()
    kube = client.AppsV1Api()

    config = kube.read_namespaced_deployment(name=deployment_name, namespace="default")

    # return the inital data object for the test. yield is used to indicated there is a tear down step afterwards
    yield deployment_config(kube, config)

    # revert to original state here
    kube.replace_namespaced_deployment(name=config.metadata.name, namespace=config.metadata.namespace)


@pytest.mark.benchmark(
    group="group-name",
    min_time=0.1,
    max_time=0.5,
    min_rounds=5,
    timer=time.time,
    disable_gc=True,
    warmup=False
)
def test_scale_10(load_config, benchmark):
    @benchmark
    def result():
        return scale_up(deployment_config=load_config, max_pod_count=10)

    assert result is None