# parsl-exploration

Exploration of the use of [parsl](https://parsl-project.org/) for data
processing pipelines in k8s:

> Use Parsl to create parallel programs composed of Python functions and
> external components. Execute Parsl programs on any compute resource from
> laptops to supercomputers.


## Cluster setup

The following need to be set up on the target cluster to make this work.

> [!NOTE]
> Some of this may be "done for you" on the ADC cluster, but you'll still need to set up
> your local (e.g. Rancher Desktop) cluster.

### `qgnet` ServiceAccount

The target cluster should be configured to have a `qgnet` service account with
permissions for managing pods (creation/deletion).

First, create a new service account:

```bash
kubectl create serviceaccount qgnet
```

Then, create a rolebinding for `qgnet` in the default namespace w/ the admin
role:

> [!WARNING]
> The admin role has more permissions than necessary.
> TODO: confirm which permissions are set on `qgnet` service account associated w/ the
> `dev-qgnet` namespace on the ADC's k8s.

```bash
kubectl create rolebinding qgnet --clusterrole=admin --serviceaccount=default:qgnet --namespace=default
```


## Submitting jobs

First, select the appropriate k8s context. E.g., to run locally:

```bash
kubectl config use-config rancher-desktop
```

To run on the remote `dev-qgnet` k8s cluster:

> [!WARNING]
> Deployment to `dev-qgnet` currently does not work. See
> https://github.com/QGreenland-Net/parsl-exploration/issues/3


```bash
kubectl config use-config dev-qgnet
```


Submit the example job defined in `run.py` with:

```bash
python run.py
```

> [!NOTE]
> The local version of python and parsl must match the remote version!

> [!WARNING]
> If a run fails, it is possible that a pod will get "stuck" and not get cleaned
> up properly. This may require manual cleanup!


### Submitting jobs to `dev-qgnet` cluster

Running a Parsl "job" on a remote cluster has a frustrating complexity: The remote
workers need to be able to connect back to the host running the Parsl program. If you're
behind a firewall you don't control, this may not be possible!

The workaround we're using is to submit a Kubernetes Job that runs the Parsl init
program from a ConfigMap. See `run-on-remote-cluster.sh` and `job.yml` for an
example of this.

> [!IMPORTANT]
> We currently using our own fork of parsl to add support for getting "in-cluster"
> configuration. See: https://github.com/Parsl/parsl/pull/3357


## Troubleshooting

### Cleaning up failed parsl pods

Some failure states result in pods getting stuck in a restart loop that do not
get cleaned up automatically. To find pods in this state:

```bash
kubectl get pods
```

To remove a pod that is stuck:

```bash
kubectl delete pod <pod name>
```


## Reference

* The [Parsl user guide's "Kubernetes Clusters" section](https://parsl.readthedocs.io/en/stable/userguide/configuring.html#kubernetes-clusters) is a good place to start.
