eval $(minikube docker-env)
docker build -t backend ./backend
docker build -t frontend ./frontend
