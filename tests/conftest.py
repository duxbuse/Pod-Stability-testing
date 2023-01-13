import pytest
from kubernetes import client, config
from collections import namedtuple
import time
import os

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
        "--deployment", action="store", help="Name of the kubernetes deployment"
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

    # -------------------------------------------------
    # revert to original state after test is finished
    '''
    We have to resort to calling kubectl commands directly cause the library has some issues documented below
    '''
    og_config_dict = dep_config.to_dict()
    del og_config_dict["metadata"]["creation_timestamp"]
    del og_config_dict["metadata"]["resource_version"]
    del og_config_dict["metadata"]["self_link"]
    del og_config_dict["metadata"]["uid"]

    os.system(f"kubectl --namespace {namespace} apply -f  - {og_config_dict}")
    os.system(f"kubectl --namespace {namespace} wait --for=condition=available --timeout=60s deployment/{dep_config.metadata.name}")


    # -------------------------------------------------
    '''
    This is all we should have to do to reset the state.
    But the `force=true` is only available for `apply-patch` type merges.
    Currently the `patch_namespaced_deployment` does not allow the selection of the patch type https://github.com/kubernetes-client/python/issues/1202
    work around is to execute kubectl commands directly
    '''
    # kube.patch_namespaced_deployment(
    #     name=dep_config.metadata.name,
    #     namespace=namespace,
    #     body=dep_config,
    #     field_manager="application/apply-patch",
    #     force=True
    # )
