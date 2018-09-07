#!/bin/sh
set -e

# Make sure minikube is running:
if ! minikube status | grep -q 'Running'; then
	minikube start
fi

kubectl config use-context minikube
eval $(minikube docker-env)


kubectl apply -f ./jupyter-notebook.yaml --validate=false 
docker build -t jupyter-notebook . && kubectl delete pods -l app=jupyter-notebook

minikube service jupyter-notebook