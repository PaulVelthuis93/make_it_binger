kubectl apply -f ../redis/k8s/
kubectl apply -f ../elasticsearch/k8s/
kubectl apply -f flask.yaml
kubectl apply -f scraper-deployment.yaml
