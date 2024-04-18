#!/usr/bin/env bash
set -euo pipefail

# Send our Parsl init script to the cluster. This will update the ConfigMap if
# there are any changes. Note that "age" represents the time since the
# ConfigMap was created, not since it was last updated.
kubectl create configmap parsl-init-script --from-file run.py \
    -o yaml --dry-run=client \
    | kubectl apply -f -

# Submit a "Job" to the cluster which runs our script
# TODO: Should we delete any pre-existing job? We're manually doing `kubectl delete` now.
kubectl apply -f k8s/job.yml


# TODO: Can we also attach to monitor `kubectl describe job` or something?
