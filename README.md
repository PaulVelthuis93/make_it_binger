# make_it_binger
A search engine project


## Deploy to GCP
0. Configure your gcloud: 'gcloud init' --> follow the steps
1. TODO : COPY COMMAND TO SPIN UP K8S CLUSTER
2. Set your kubectl to use the correct k8s cluster on GCP: 'gcloud container clusters get-credentials make-it-binger-cluster'
3. Set docker images in the GCP container registry: 'sh deployment/docker/build.sh'
4. Deploy all k8s config files: 'sh deployment/deploy.sh'
