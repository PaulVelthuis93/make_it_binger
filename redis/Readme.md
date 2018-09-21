
# Installing Redis on Kubernetes instructions

The inspiration is gained from:
https://kubernetes.io/docs/tutorials/configuration/configure-redis-using-configmap/


Commands:
curl -OL https://k8s.io/examples/pods/config/redis-config
kubectl create configmap example-redis-config --from-file=redis-config

kubectl create -f https://k8s.io/examples/pods/config/redis-pod.yaml

Redis can be started via the command:

kubectl exec -it redis redis-cli


# Pub sub inspiration for redis

Redis can use pub sub mechanism, with several consumers and producers
Inspiration for this mechanism can be found on:
https://redis.io/topics/pubsub

 
