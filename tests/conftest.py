import pytest
from kubernetes import client, config
from collections import namedtuple
import time

# ------------Global Objects------------
deployment_config_tuple = namedtuple('deployment_config', ['kube', 'config'])

def scale_to(deployment_config, pod_count):
    deployment_config.kube.patch_namespaced_deployment_scale(
        deployment_config.config.metadata.name,
        deployment_config.config.metadata.namespace,
        {'spec': {'replicas': pod_count}}
    )
    i = 1
    while(
            (ready_replicas:=deployment_config.kube.read_namespaced_deployment(
                name=deployment_config.config.metadata.name,
                namespace=deployment_config.config.metadata.namespace
            ).status.ready_replicas or 0) != pod_count
        ):
        if(i == 8): #exponential back off following 'N*(N+1)/2'; N=7 results in roughly 30sec
            raise ValueError(f"Scaling Failed.\n{ready_replicas=} != {pod_count=}")
        time.sleep(1 * i)
        i += 1
    return True


def pytest_addoption(parser):
    parser.addoption(
        "--deployment", action="store", default="httpbin", help="Name of the kubernetes deployment"
    )
    parser.addoption(
        "--namespace", action="store", default="default", help="Name of the kubernetes namespace"
    )


# ------------Global Fixtures------------

@pytest.fixture
def deployment_name(request):
    return request.config.getoption("--deployment")

@pytest.fixture
def namespace(request):
    return request.config.getoption("--namespace")

@pytest.fixture()
def load_config(deployment_name, namespace):
    config.load_kube_config()
    kube = client.AppsV1Api()
    dep_config = kube.read_namespaced_deployment(name=deployment_name, namespace=namespace)

    deployment_config = deployment_config_tuple(kube, dep_config)

    yield deployment_config

    # revert to original state after test is finished


    """
    For some reason replacing the whole deployment has the below error. So instead we will just reset the scale.

    HTTP response body: {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"Operation cannot be fulfilled on deployments.apps \"httpbin\": the object has been modified; please apply your changes to the latest version and try again","reason":"Conflict","details":{"name":"httpbin","group":"apps","kind":"deployments"},"code":409}
    """
    # kube.replace_namespaced_deployment(
    #     name=deployment_config.metadata.name,
    #     namespace=namespace,
    #     body=deployment_config
    # )

    scale_to(deployment_config=deployment_config, pod_count=dep_config.spec.replicas)