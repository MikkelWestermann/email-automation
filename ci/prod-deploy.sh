#!/bin/bash

# Exit if error occurs
set -e

CLUSTER_NAME=portfolio

gcloud --quiet config set container/cluster $CLUSTER_NAME
gcloud --quiet config set compute/zone ${CLOUDSDK_COMPUTE_ZONE}
gcloud --quiet container clusters get-credentials $CLUSTER_NAME

export GOOGLE_APPLICATION_CREDENTIALS=${HOME}/gcloud-service-key.json

/usr/local/bin/skaffold run -p production