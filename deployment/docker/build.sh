gcloud container builds submit --async --config flask.yaml --substitutions _IMAGE_LABEL=latest ../../flask
gcloud container builds submit --async --config scraper.yaml --substitutions _IMAGE_LABEL=latest ../../scraper
