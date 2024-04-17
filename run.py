"""Example parsl workflow to be executed on kubernetes.

TODO:

* Less printing more logging
"""

import os

from parsl.config import Config
from parsl.executors import HighThroughputExecutor
from parsl.providers import KubernetesProvider
from parsl.addresses import address_by_route
from parsl import python_app, bash_app
import parsl
from parsl.data_provider.files import File
import kubernetes


def get_current_namespace():
    """From: https://github.com/kubernetes-client/python/issues/363#issuecomment-1122471443"""
    ns_path = "/var/run/secrets/kubernetes.io/serviceaccount/namespace"
    if os.path.exists(ns_path):
        with open(ns_path) as f:
            return f.read().strip()
    try:
        _, active_context = kubernetes.config.list_kube_config_contexts()
        return active_context["context"]["namespace"]
    except KeyError:
        return "default"


def get_parsl_config():
    k8s_namespace = get_current_namespace()
    print(f"Current namespace: {k8s_namespace}")

    config = Config(
        executors=[
            HighThroughputExecutor(
                # "htex" = high throughput executor
                label="kube-htex",
                cores_per_worker=1,
                max_workers_per_node=1,
                worker_logdir_root="/tmp/",
                # Address for the pod worker to connect back to the "interchange"
                address=address_by_route(),
                # https://parsl.readthedocs.io/en/stable/stubs/parsl.providers.KubernetesProvider.html#parsl.providers.KubernetesProvider
                provider=KubernetesProvider(
                    namespace=k8s_namespace,
                    # Docker image url to use for pods
                    image="ghcr.io/qgreenland-net/parsl-exploration:v0.1.1",
                    # Command to be run upon pod start, such as:
                    # "module load Anaconda; source activate parsl_env".
                    # or "pip install parsl"
                    # NOTE: parsl needs to be installed or the pod will fail to
                    # start properly and the process will hang.
                    worker_init="",
                    # The secret key to download the image
                    # secret="YOUR_KUBE_SECRET",
                    # Should follow the Kubernetes naming rules
                    pod_name="parsl-exploration",
                    nodes_per_block=1,
                    init_blocks=1,
                    # Maximum number of pods to scale up
                    max_blocks=1,
                    # list of tuples w/ the format: (PVC Name, Mount Directory)
                    persistent_volumes=[("qgnet-pvc-test-1", "/data")],
                ),
            ),
        ]
    )

    return config


# App that generates a random number
@python_app
def generate(limit):
    from random import randint

    return randint(1, limit)


# App that writes a variable to a file
@bash_app
def save_value_to_file(
    *,
    value,
    output_filepath,
    stdout="stdout.txt",  # Requests Parsl to return the stdout
    stderr="stderr.txt",  # Requests Parsl to return the stderr
):
    return f"echo {value} &> {output_filepath}"


@python_app
def read_and_return(fp):
    with open(fp, "r") as f:
        return f.read()


if __name__ == "__main__":
    config = get_parsl_config()
    with parsl.load(config):
        # Generate a random number between 1 and 10
        random = generate(10)
        print(f"Random number: {random.result()}")

        # Save the random number to a file
        output_path = "/data/sequential-output.txt"
        saved = save_value_to_file(
            value=random,
            output_filepath=File(output_path),
        )

        # Wait until `save` completes
        saved.result()

        # Then print the results.
        print("Reading stdout from remote")
        print(read_and_return(saved.stdout).result())
        print()
        print("Reading stderr from remote")
        print(read_and_return(saved.stderr).result())
        print()
        print("Reading file from remote")
        print(read_and_return(output_path).result())
        print()
