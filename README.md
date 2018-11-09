# make_it_binger
A search engine project


## Deploy to GCP
0. Configure your gcloud: 'gcloud init' --> follow the steps
1. Run the command here below......
2. Set your kubectl to use the correct k8s cluster on GCP: 'gcloud container clusters get-credentials make-it-binger-cluster --zone europe-west1-c - project xomnia-search-engine-training'
3. Set docker images in the GCP container registry: 'sh deployment/docker/build.sh'
4. Deploy all k8s config files: 'sh deployment/deploy.sh'


```
# this is for creating a new k8s cluster....


gcloud beta container --project "xomnia-search-engine-training" clusters create "make-it-binger-cluster-clone-1" --zone "europe-west1-c" --username "admin" --cluster-version "1.9.7-gke.7" --machine-type "n1-standard-4" --image-type "COS" --disk-type "pd-standard" --disk-size "100" --scopes "https://www.googleapis.com/auth/compute","https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --num-nodes "4" --enable-cloud-logging --enable-cloud-monitoring --network "projects/xomnia-search-engine-training/global/networks/default" --subnetwork "projects/xomnia-search-engine-training/regions/europe-west1/subnetworks/default" --enable-autoscaling --min-nodes "1" --max-nodes "4" --addons HorizontalPodAutoscaling,HttpLoadBalancing,KubernetesDashboard --enable-autoupgrade --enable-autorepair

```