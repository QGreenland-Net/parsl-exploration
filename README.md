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

> [!WARNING]
> I'm getting `ModuleNotFoundError: No module named 'kubernetes'` when attempting
> `import kubernetes` and this is causing parsl to fail to speak to the cluster.
> `parsl-with-kubernetes` is included in the environment to resolve this, but that
> doesn't fix the issue! A problem with the feedstock?

> [!NOTE]
> TODO


## Submitting jobs

> [!NOTE]
> TODO
