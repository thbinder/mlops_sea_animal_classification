### Install Minikube

To run this kubernetes cluster setup and app deployment you only need to install minikube and run the setup script.

```
https://kubernetes.io/fr/docs/tasks/tools/install-minikube/
```

### Install Kind (Optional)

```
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.16.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

### Install K3ai (Optional)

```
curl -sfL "https://get.k3ai.in" -o k3ai.tar.gz
tar -xvzf k3ai.tar.gz
chmod +x ./k3ai
sudo mv ./k3ai /usr/local/bin
```

### Start Cluster & Install Kubeflow Pipelines (Optional)

If you encounter an issue with no infrastructure enabled, directly modify the init yaml script to use kind.

```
k3ai init --local kind
k3ai apply kubeflow-pipelines
```

Alternatively, directly work with kind
```
kind create cluster --name my-cluster-name
kubectl cluster-info --context kind-my-cluster-name
```

Update/Install Kubeflow pipelines
```
export PIPELINE_VERSION=1.8.5
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"
```

To verify kubeflow pipelines was correctly installed, run the following command and browse to localhost:8080.
```
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
```

To uninstall Kubeflow pipelines
```
export PIPELINE_VERSION=1.8.5
kubectl delete -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"
kubectl delete -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
```

### Local Kubeflow with ZenML (Optional)

Install k3d

```
wget -q -O - https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash
```

Register your stack, update it and build it according to ZenML documentation.
