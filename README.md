# parsl-exploration

Exploration of the use of [parsl](https://parsl-project.org/) for data
processing pipelines in k8s:

> Use Parsl to create parallel programs composed of Python functions and
> external components. Execute Parsl programs on any compute resource from
> laptops to supercomputers.


## Configuring Parsl on Kubernetes

The
[Parsl user guide's "Kubernetes Clusters" section](https://parsl.readthedocs.io/en/stable/userguide/configuring.html#kubernetes-clusters)
is a good place to start.


> [!NOTE]
> TODO


## Submitting jobs

First, select the appropriate k8s context. E.g., to run locally:

```
kubectl config use-config rancher-desktop
```

to run on the `dev-qgnet` k8s cluster:

> [!WARNING]
> Deployment to `dev-qgnet` currently does not work. See
> https://github.com/QGreenland-Net/parsl-exploration/issues/3


```
kubectl config use-config dev-qgnet
```


Submit the example job defined in `run.py` with:

```
python run.py
```
> [!NOTE]
> The local version of python and parsl must match the remote version!

> [!WARNING]
> If a run fails, it is possible that a pod will get "stuck" and not get cleaned
> up properly. This may require manual cleanup!


### Submitting jobs on the ADC cluster

Running a Parsl "job" on a remote cluster has a frustrating complexity: The remote
workers need to be able to connect back to the host running the Parsl program. If you're
behind a firewall you don't control, this may not be possible!

The workaround we're using is to submit a Kubernetes Job that runs the Parsl init
program from a ConfigMap. See `run-on-remote-cluster.sh` and `job.yml` for an
example of this.


## Troubleshooting

### Cleaning up failed parsl pods

Some failure states result in pods getting stuck in a restart loop that do not
get cleaned up automatically. To find pods in this state:

```
kubectl get pods
```

To remove a pod that is stuck:

```
kubectl delete pod <pod name>
```


## Setting up `qgnet` user on rancher-desktop

Rancher desktop should be configured to have a `qgnet` service account with
permissions for managing pods (creation/deletion).

First, create a new service account:

```
kubectl create serviceaccount qgnet
```

Then, create a rolebinding for `qgnet` in the default namespace w/ the admin
role:

> [!WARNING]
> the admin role may have more permissions than necessary. TODO: confirm which
> permissions are set on `qgnet` service account associated w/ the `dev-qgnet`
> namespace on the ADC's k8s.

```
kubectl create rolebinding qgnet --clusterrole=admin --serviceaccount=default:qgnet --namespace=default
```
