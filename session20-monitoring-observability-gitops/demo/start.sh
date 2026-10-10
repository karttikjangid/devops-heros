#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
kubectl --context minikube get nodes
kubectl --context minikube create namespace session20-argocd --dry-run=client -o yaml | kubectl --context minikube apply -f -
kubectl --context minikube apply --server-side -k argocd
kubectl --context minikube apply -f project.yaml
kubectl --context minikube apply -f argocd-application.yaml
kubectl --context minikube create namespace session20-monitoring --dry-run=client -o yaml | kubectl --context minikube apply -f -
for name in prometheus blackbox grafana-datasource grafana-provider grafana-dashboard; do
  case "$name" in
    prometheus) files=(--from-file=monitoring/prometheus.yml --from-file=monitoring/alerts.yml) ;;
    blackbox) files=(--from-file=monitoring/blackbox.yml) ;;
    grafana-datasource) files=(--from-file=monitoring/datasource.yml) ;;
    grafana-provider) files=(--from-file=monitoring/provider.yml) ;;
    grafana-dashboard) files=(--from-file=monitoring/dashboard.json) ;;
  esac
  config="$name"
  [[ "$name" == prometheus || "$name" == blackbox ]] && config="$name-config"
  kubectl --context minikube -n session20-monitoring create configmap "$config" "${files[@]}" --dry-run=client -o yaml | kubectl --context minikube apply -f -
done
kubectl --context minikube apply -f monitoring/stack.yaml
