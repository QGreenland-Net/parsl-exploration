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
> up properly. This may require manual cleanup! TODO: how?
