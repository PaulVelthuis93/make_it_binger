#!/bin/sh
set -e

# Make sure minikube is running:
if ! minikube status | grep -q 'Running'; then
	minikube start
fi

kubectl config use-context minikube
# eval $(minikube docker-env)

# kubectl create configmap example-redis-config --from-file=redis-config

kubectl apply -f ./redis-pod.yaml --validate=false 
#docker build -t redis . &&
kubectl delete pods -l app=redis

minikube service redis