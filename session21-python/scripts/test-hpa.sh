#!/usr/bin/env bash
set -euo pipefail
cleanup() { kubectl -n session21 delete job capstone-load --ignore-not-found; }
trap cleanup EXIT
set -x
kubectl -n session21 get hpa,pods
kubectl -n session21 top pods
kubectl -n session21 create job capstone-load --image=busybox:1.37 -- sh -c '
  for worker in $(seq 1 16); do
    (while true; do wget -qO /dev/null http://backend:8000/api/tasks || exit 1; done) &
  done
  wait
'
scaled=false
for attempt in {1..36}; do
  kubectl -n session21 get hpa
  replicas=$(kubectl -n session21 get deployment homework-backend -o jsonpath='{.spec.replicas}')
  if ((replicas > 2)); then scaled=true; break; fi
  sleep 5
done
[[ "$scaled" == true ]]
kubectl -n session21 rollout status deployment/homework-backend --timeout=120s
kubectl -n session21 get hpa,pods
kubectl -n session21 top pods
kubectl -n session21 describe hpa homework-backend
