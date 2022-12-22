import pytest
import time
from conftest import scale_to
from kubernetes import config
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream


def exec_sig_pid1(api_instance, pod_name, namespace, signal):
    try:
        resp = api_instance.read_namespaced_pod(name=pod_name,
                                                namespace=namespace)
    except ApiException as e:
        if e.status != 404:
            print("Unknown error: %s" % e)
            exit(1)

    # Calling exec and waiting for response
    # kill -SIGINT 1
    exec_command = [
        'kill',
         f'-{signal}',
         '1']

    resp = stream(api_instance.connect_get_namespaced_pod_exec,
                  pod_name,
                  namespace,
                  command=exec_command,
                  stderr=True, stdin=False,
                  stdout=True, tty=False)
                  
    return resp

def read_restart_count(core_v1, name, namespace):
    return core_v1.read_namespaced_pod(name=name, namespace=namespace).status.container_statuses[0].restart_count
        

def check_pod_restarted(core_v1, name, namespace, initial_restart_count) -> bool:
    i = 1

    while(read_restart_count(core_v1, name, namespace) != initial_restart_count+1):
        if(i == 8): #Wait roughly 30 seconds
            return False
        time.sleep(1 * i)
        i += 1
    return True
    
@pytest.fixture
def set_to_1(load_config):
    return scale_to(load_config, 1)

@pytest.fixture
def core_v1():
    config.load_kube_config()
    k =  core_v1_api.CoreV1Api()
    return k


class TestSIGINT:
    def test_bash_sig_int(self, load_config, core_v1, set_to_1):

        deployment = load_config.config.metadata.name
        namespace = load_config.config.metadata.namespace

        pod_yaml = core_v1.list_namespaced_pod(namespace=namespace)

        pod_names = [x.metadata.name for x in pod_yaml.items if x.metadata.labels["app"] == deployment]
        
        if pod_names:
            #get 1st pod's name
            pod_name = pod_names.pop()

            # get current restart count
            pre_count = read_restart_count(core_v1=core_v1, name=pod_name, namespace=namespace)

            #issue SIGINT
            resp = exec_sig_pid1(api_instance=core_v1, pod_name=pod_name, namespace=namespace, signal="SIGINT")

            #check it restarted
            assert check_pod_restarted(core_v1=core_v1, name=pod_name, namespace=namespace, initial_restart_count=pre_count)
            

        else:
            raise ValueError(f"No pods running for {deployment}")

class TestSIGTERM:
    def test_bash_sig_term(self, load_config, core_v1, set_to_1):

        deployment = load_config.config.metadata.name
        namespace = load_config.config.metadata.namespace

        pod_yaml = core_v1.list_namespaced_pod(namespace=namespace)

        pod_names = [x.metadata.name for x in pod_yaml.items if x.metadata.labels["app"] == deployment]
        
        if pod_names:
            #get 1st pod's name
            pod_name = pod_names.pop()

            # get current restart count
            pre_count = read_restart_count(core_v1=core_v1, name=pod_name, namespace=namespace)

            #issue SIGINT
            resp = exec_sig_pid1(api_instance=core_v1, pod_name=pod_name, namespace=namespace, signal="SIGTERM")

            #check it restarted
            assert check_pod_restarted(core_v1=core_v1, name=pod_name, namespace=namespace, initial_restart_count=pre_count)
            

        else:
            raise ValueError(f"No pods running for {deployment}")