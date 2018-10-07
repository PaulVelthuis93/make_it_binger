#!/bin/sh
set -e

# Make sure minikube is running:
if ! minikube status | grep -q 'Running'; then
	minikube start
fi

kubectl config use-context minikube
eval $(minikube docker-env)

docker build -t frontend . && kubectl delete pods -l app=frontend
kubectl apply -f ./frontend.yaml --validate=false
	
minikube service frontend-service
