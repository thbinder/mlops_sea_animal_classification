minikube start
minikube addons enable ingress
sleep 2
kubectl create -f ./resources/deployment.yaml
sleep 2
kubectl create -f ./resources/service.yaml
sleep 10
kubectl create -f ./resources/ingress.yaml
sleep 2
minikube service sea-animals-api-service --url