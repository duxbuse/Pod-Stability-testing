import time
import statistics
from kubernetes import client, config
import pytest
from collections import namedtuple

deployment_config_tuple = namedtuple('deployment_config', ['kube', 'config'])

class Timer:    
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter()
        self.interval = self.end - self.start


def scale_to(deployment_config, pod_count):
    deployment_config.kube.patch_namespaced_deployment_scale(
        deployment_config.config.metadata.name,
        deployment_config.config.metadata.namespace,
        {'spec': {'replicas': pod_count}}
    )
    i = 1
    while(deployment_config.kube.read_namespaced_deployment(name=deployment_config.config.metadata.name, namespace=deployment_config.config.metadata.namespace).status.ready_replicas != pod_count):
        if(i == 5):
            break
        time.sleep(1 * i)
        i += 1


@pytest.fixture
def load_config(deployment_name):
    config.load_kube_config()
    kube = client.AppsV1Api()

    dep_config = kube.read_namespaced_deployment(name=deployment_name, namespace="default")

    # return the inital data object for the test. yield is used to indicated there is a tear down step afterwards
    deployment_config = deployment_config_tuple(kube, dep_config)
    yield deployment_config

    # revert to original state here
    scale_to(deployment_config, dep_config.spec.replicas)

@pytest.fixture
def set_to_10(load_config):
    return scale_to(load_config, 10)

@pytest.fixture
def set_to_0(load_config):
    return scale_to(load_config, 0)


class TestScale:
    @pytest.mark.benchmark(
        group="group-name",
        min_time=0.1,
        max_time=0.5,
        min_rounds=5,
        timer=time.time,
        disable_gc=True,
        warmup=False
    )
    @pytest.mark.dependency()
    def test_scale_10(self, load_config, benchmark, set_to_0):
        @benchmark
        def result():
            return scale_to(deployment_config=load_config, pod_count=10)

        assert result is None

    @pytest.mark.benchmark(
        group="group-name",
        min_time=0.1,
        max_time=0.5,
        min_rounds=5,
        timer=time.time,
        disable_gc=True,
        warmup=False
    )
    @pytest.mark.dependency(depends=["test_scale_10"])
    def test_scale_0(self, load_config, benchmark, set_to_10):
        @benchmark
        def result():
            return scale_to(deployment_config=load_config, pod_count=0)

        assert result is None