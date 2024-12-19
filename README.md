# parsl-exploration

This repository has been archived.

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

### `qgnet` Namespace

```bash
kubectl create namespace qgnet
```

Update your config to add a context referencing the new namespace:

```bash
kubectl config --kubeconfig={config-file-path} \
  set-context {context-name} \
  --cluster={cluster-name} \
  --namespace=qgnet \
  --user={user}
```

For a local Rancher Desktop cluster, this looks like:

```bash
kubectl config --kubeconfig="${HOME}/.kube/config" \
  set-context rancher-desktop-qgnet \
  --cluster=rancher-desktop \
  --namespace=qgnet \
  --user=rancher-desktop
```


### `qgnet` ServiceAccount

The target cluster should be configured to have a `qgnet` service account with
permissions for managing pods (creation/deletion).

```bash
kubectl apply -f k8s/serviceaccount.yml
```

> [!NOTE]
> Role bindings are based on
> [DataONE example](https://github.com/DataONEorg/k8s-cluster/tree/main/authorization).


## Submitting jobs

First, select the appropriate k8s context. E.g., to run locally:

```bash
kubectl config use-context rancher-desktop-qgnet
```

To run on the remote `dev-qgnet` k8s cluster:

> [!WARNING]
> Deployment to `dev-qgnet` currently does not work. See
> https://github.com/QGreenland-Net/parsl-exploration/issues/3


```bash
kubectl config use-context dev-qgnet
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


### Submitting jobs to a remote cluster

Running a Parsl "job" on a remote cluster has a frustrating complexity: The remote
workers need to be able to connect back to the host running the Parsl program. If you're
behind a firewall you don't control, this may not be possible!

The workaround we're using is to submit a Kubernetes Job that runs the Parsl init
program from a ConfigMap. See `run-on-remote-cluster.sh` and `job.yml` for an
example of this.

> [!IMPORTANT]
> We currently using our own fork of parsl to add support for getting "in-cluster"
> configuration. See: https://github.com/Parsl/parsl/pull/3357


### Viewing job output file(s)

Check [Inspect a Kubernetes PersistentVolumeClaim by Frank
Sauerburger](https://frank.sauerburger.io/2021/12/01/inspect-k8s-pvc.html) for an
excellent tutorial.

* `kubectl apply -f k8s/pvc-inspector.yml`
    * You may need to wait a few seconds...
* `kubectl exec -it pvc-inspector -- sh`
    * Inspect `/pvc` directory
    * Quit
* `kubectl delete pod pvc-inspector`


## Troubleshooting

### `parsl-init-script` ConfigMap fails to mount

```bash
MountVolume.SetUp failed for volume "parsl-init-script-volume" : object "qgnet"/"parsl-init-script" not registered
```

Does not always occur.

[See related GitHub issue](https://github.com/kubernetes/kubernetes/issues/105204).


### Cleaning up failed parsl pods

Some failure states result in pods getting stuck in a restart loop that do not
get cleaned up automatically. To find pods in this state:

```bash
kubectl get pods
```

To remove a pod that is stuck:

```bash
kubectl delete pod {pod-name}
```


### File not found error starting Rancher Desktop

You must have a valid `$KUBECONFIG` path. Paths including `~` or paths to files which do
not exist will cause Rancher to fail starting the cluster.


## Reference

* The [Parsl user guide's "Kubernetes Clusters" section](https://parsl.readthedocs.io/en/stable/userguide/configuring.html#kubernetes-clusters) is a good place to start.
