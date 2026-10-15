#!/usr/bin/env bash
set -euo pipefail
: "${FRONTEND:?Set FRONTEND to the frontend image built by CI}"
cleanup() {
  kubectl -n session21 delete deployment/taskboard-broken-image service/broken-service --ignore-not-found
}
trap cleanup EXIT
set -x
kubectl apply -f troubleshooting/broken-image.yaml
for attempt in {1..45}; do
  reason=$(kubectl -n session21 get pods -l app=broken-image -o jsonpath='{.items[*].status.containerStatuses[*].state.waiting.reason}')
  if [[ "$reason" == *ImagePullBackOff* || "$reason" == *ErrImagePull* ]]; then break; fi
  sleep 2
done
[[ "$reason" == *ImagePullBackOff* || "$reason" == *ErrImagePull* ]]
kubectl -n session21 describe pods -l app=broken-image
kubectl -n session21 get events --sort-by=.lastTimestamp
kubectl -n session21 set image deployment/taskboard-broken-image frontend="$FRONTEND"
kubectl -n session21 rollout status deployment/taskboard-broken-image --timeout=120s
kubectl apply -f troubleshooting/broken-service.yaml
kubectl -n session21 get endpointslices -l kubernetes.io/service-name=broken-service -o yaml
[[ -z "$(kubectl -n session21 get endpointslices -l kubernetes.io/service-name=broken-service -o jsonpath='{.items[*].endpoints[*].addresses[*]}')" ]]
kubectl -n session21 get pods --show-labels
kubectl -n session21 patch service broken-service --type merge -p '{"spec":{"selector":{"app":"homework-frontend"}}}'
for attempt in {1..20}; do
  addresses=$(kubectl -n session21 get endpointslices -l kubernetes.io/service-name=broken-service -o jsonpath='{.items[*].endpoints[*].addresses[*]}')
  [[ -n "$addresses" ]] && break
  sleep 1
done
[[ -n "$addresses" ]]
kubectl -n session21 get endpointslices -l kubernetes.io/service-name=broken-service -o yaml
kubectl -n session21 exec deployment/homework-frontend -- wget -qO- http://broken-service:8080/
