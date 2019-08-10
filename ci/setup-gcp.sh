apt-get update
apt-get -y install lsb-release apt-transport-https

# Create an environment variable for the correct distribution
export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"

# Add the Cloud SDK distribution URI as a package source
echo "deb https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import the Google Cloud Platform public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

# Update the package list and install the Cloud SDK
apt-get -y update && apt-get -y install google-cloud-sdk

# Decode the base64 encoded gcloud service key from env var and save to file
echo $GCLOUD_SERVICE_KEY | base64 --decode > ${HOME}/gcloud-service-key.json

# Perform authentication with google cloud 
gcloud auth activate-service-account --key-file ${HOME}/gcloud-service-key.json

# Get kubectl
curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v1.7.0/bin/linux/amd64/kubectl && chmod +x kubectl && sudo mv kubectl /usr/local/bin/
# Get skaffold
curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/v0.30.0/skaffold-linux-amd64 && chmod +x skaffold && sudo mv skaffold /usr/local/bin

# Set project name for gcloud
gcloud config set project $PROJECT_NAME

VERSION=1.5.0
OS=linux  # or "darwin" for OSX, "windows" for Windows.
ARCH=amd64  # or "386" for 32-bit OSs

# curl -fsSL "https://github.com/GoogleCloudPlatform/docker-credential-gcr/releases/download/v${VERSION}/docker-credential-gcr_${OS}_${ARCH}-${VERSION}.tar.gz" \
#   | tar xz --to-stdout ./docker-credential-gcr \
#   > /usr/bin/docker-credential-gcr && chmod +x /usr/bin/docker-credential-gcr

# /usr/bin/docker-credential-gcr configure-docker