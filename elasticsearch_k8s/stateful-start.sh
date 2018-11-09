gcloud container clusters get-credentials binger --zone europe-west4-a --project xomnia-search-engine-training#!/bin/sh
set -e

# Make sure minikube is running:
if ! minikube status | grep -q 'Running'; then
	minikube start
fi

kubectl config use-context minikube
eval $(minikube docker-env)

kubectl apply -f es-discovery-svc.yaml
kubectl apply -f es-svc.yaml
kubectl apply -f stateful/es-master-stateful.yaml
#kubectl rollout status -f stateful/es-master-stateful.yaml

kubectl apply -f es-ingest-svc.yaml
kubectl apply -f es-ingest.yaml
kubectl rollout status -f es-ingest.yaml

kubectl apply -f stateful/es-data-stateful.yaml
#kubectl rollout status -f stateful/es-data-stateful.yaml