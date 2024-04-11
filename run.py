import os

from parsl.config import Config
from parsl.executors import HighThroughputExecutor
from parsl.providers import KubernetesProvider
from parsl.addresses import address_by_route
from parsl import python_app, bash_app
import parsl
from parsl.data_provider.files import File


config = Config(
    executors=[
        HighThroughputExecutor(
            # "htex" = high throughput executor
            label="kube-htex",
            cores_per_worker=1,
            max_workers_per_node=1,
            worker_logdir_root="/tmp/",

            # Address for the pod worker to connect back
            address=address_by_route(),
            provider=KubernetesProvider(
                namespace="default",

                # Docker image url to use for pods
                image="python",

                # Command to be run upon pod start, such as:
                # "module load Anaconda; source activate parsl_env".
                # or "pip install parsl"
                worker_init="pip install parsl",

                # The secret key to download the image
                # secret="YOUR_KUBE_SECRET",

                # Should follow the Kubernetes naming rules
                pod_name="new-pod-name",

                nodes_per_block=1,
                init_blocks=1,
                # Maximum number of pods to scale up
                max_blocks=10,
            ),
        ),
    ]
)

# App that generates a random number
@python_app
def generate(limit):
      from random import randint
      return randint(1,limit)

# App that writes a variable to a file
@bash_app
def save(variable, outputs=[]):
      return 'echo %s &> %s' % (variable, outputs[0])

with parsl.load(config):
    # Generate a random number between 1 and 10
    random = generate(10)
    print('Random number: %s' % random.result())

    # Save the random number to a file
    saved = save(random, outputs=[File(os.path.join(os.getcwd(), 'sequential-output.txt'))])

    # Print the output file
    with open(saved.outputs[0].result(), 'r') as f:
          print('File contents: %s' % f.read())
