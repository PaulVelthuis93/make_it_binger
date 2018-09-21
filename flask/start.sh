#!/bin/sh
set -e

# Make sure minikube is running:
if ! minikube status | grep -q 'Running'; then
	minikube start
fi

kubectl config use-context minikube
eval $(minikube docker-env)


kubectl apply -f ./flask.yaml --validate=false 
docker build -t binger-api . && kubectl delete pods -l app=binger-api

minikube service binger-api