import pytest
from kubernetes import client, config, utils
from collections import namedtuple
import time

# ------------Global Objects------------
deployment_config_tuple = namedtuple('deployment_config', ['kube', 'config'])




def pytest_addoption(parser):
    parser.addoption(
        "--name", action="store", default="httpbin", help="Name of the kubernetes deployment"
    )


@pytest.fixture
def deployment_name(request):
    return request.config.getoption("--name")

@pytest.fixture()
def load_config(deployment_name):
    namespace = "default"
    config.load_kube_config()
    kube = client.AppsV1Api()

    deployment_config = kube.read_namespaced_deployment(name=deployment_name, namespace=namespace)

    yield deployment_config_tuple(kube, deployment_config)

    # revert to original state after test is finished


    """
    For some reason replacing the whole deployment has the below error. So instead we will just reset the scale.
    
    HTTP response body: {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"Operation cannot be fulfilled on deployments.apps \"httpbin\": the object has been modified; please apply your changes to the latest version and try again","reason":"Conflict","details":{"name":"httpbin","group":"apps","kind":"deployments"},"code":409}
    """
    # kube.replace_namespaced_deployment(
    #     name=deployment_config.metadata.name,
    #     namespace=deployment_config.metadata.namespace,
    #     body=deployment_config
    # )

    kube.patch_namespaced_deployment_scale(
        deployment_config.metadata.name,
        deployment_config.metadata.namespace,
        {'spec': {'replicas': deployment_config.spec.replicas}}
    )

    # Check that its all healthy
    i = 1
    while((kube.read_namespaced_deployment(name=deployment_config.metadata.name, namespace=deployment_config.metadata.namespace).status.ready_replicas or 0) != deployment_config.spec.replicas):
        if(i == 5):
            raise ValueError(f"Resetting original state failed.\n{deployment_config.status.ready_replicas=} != {deployment_config.spec.replicas=}")
        time.sleep(1 * i)
        i += 1