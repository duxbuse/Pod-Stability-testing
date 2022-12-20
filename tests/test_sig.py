# import time
# import pytest
# from conftest import scale_to
# from kubernetes import config
# from kubernetes.client import Configuration
# from kubernetes.client.api import core_v1_api
# from kubernetes.client.rest import ApiException
# from kubernetes.stream import stream


# def exec_sigint(api_instance):
#     name = 'busybox-test'
#     resp = None
#     try:
#         resp = api_instance.read_namespaced_pod(name=name,
#                                                 namespace='default')
#     except ApiException as e:
#         if e.status != 404:
#             print("Unknown error: %s" % e)
#             exit(1)

#     if not resp:
#         print("Pod %s does not exist. Creating it..." % name)
#         pod_manifest = {
#             'apiVersion': 'v1',
#             'kind': 'Pod',
#             'metadata': {
#                 'name': name
#             },
#             'spec': {
#                 'containers': [{
#                     'image': 'busybox:latest',
#                     'name': 'sleep',
#                     "args": [
#                         "/bin/sh",
#                         "-c",
#                         "while true;do date;sleep 5; done"
#                     ]
#                 }]
#             }
#         }
#         resp = api_instance.create_namespaced_pod(body=pod_manifest,
#                                                   namespace='default')
#         while True:
#             resp = api_instance.read_namespaced_pod(name=name,
#                                                     namespace='default')
#             if resp.status.phase != 'Pending':
#                 break
#             time.sleep(1)
#         print("Done.")

#     # Calling exec and waiting for response
#     exec_command = [
#         '/bin/sh',
#         '-c',
#         'echo This message goes to stderr; echo This message goes to stdout']
#     resp = stream(api_instance.connect_get_namespaced_pod_exec,
#                   name,
#                   'default',
#                   command=exec_command,
#                   stderr=True, stdin=False,
#                   stdout=True, tty=False)
#     print("Response: " + resp)

    
# @pytest.fixture
# def set_to_1(load_config):
#     return scale_to(load_config, 1)

# @pytest.fixture
# def core_v1():
#     config.load_kube_config()
#     k = core_v1_api.CoreV1Api()


# class TestSigInt:
#     def test_sig_int(self, load_config, core_v1, set_to_1):


#     deployment = load_config.config.metadata.name
#     namespace = load_config.config.metadata.namespace

#     pod = core_v1.list_namespaced_pod(namespace=namespace)


# pod = core_api.read_namespaced_pod(name=name, namespace=namespace)
# owner_references = pod.metadata.owner_references
# if isinstance(owner_references, list):
#     owner_name = owner_references[0].name
#     owner_kind = owner_references[0].kind
#     # owner  StatefulSet
#     if owner_kind == 'ReplicaSet':
#         replica_set = apis_api.read_namespaced_replica_set(name=owner_name, namespace=namespace)
#         owner_references2 = replica_set.metadata.owner_references
#         if isinstance(owner_references2, list):
#             print(owner_references2[0].name)
#         else:
#             print(owner_name)
#     # owner Deployment
#     else:
#         print(owner_name)
# print(name)

# exec_commands(core_v1)