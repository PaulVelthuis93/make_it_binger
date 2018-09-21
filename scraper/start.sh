#!/bin/sh
set -e

# Make sure minikube is running:
if ! minikube status | grep -q 'Running'; then
	minikube start
fi

kubectl config use-context minikube
eval $(minikube docker-env)


kubectl apply -f kubernetes/
docker build -t scraper-image . && kubectl delete pods -l app=scraper