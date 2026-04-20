# sre-flask-k8s

![CI](https://github.com/fanninggh/sre-flask-k8s/actions/workflows/ci.yml/badge.svg)

Flask DevOps project — 30-day SRE learning portfolio.

## Stack
- Flask 3.1.3 (Python) · PostgreSQL 16 · Redis 7

## Run locally
docker compose up -d
curl http://localhost:5000/health

## Kubernetes
kubectl apply -f k8s/
helm install flask-app ./helm/flask-devops -n flask-app --create-namespace
helm install flask-app ./helm/flask-devops -f helm/flask-devops/values-prod.yaml -n flask-app

## Images
- GHCR: ghcr.io/fanninggh/flask-devops:latest
- ECR: 779846820095.dkr.ecr.eu-west-1.amazonaws.com/flask-devops:latest

## CI/CD Pipeline
Every push: test (3.11+3.12) -> Trivy scan -> build -> push GHCR -> deploy App Runner
Every tag: build versioned image -> GitHub Release with changelog

## K8s Features
- ArgoCD GitOps: auto-sync from k8s/ folder
- Helm chart: install/upgrade/rollback with environment values
- HPA: auto-scale 2-10 pods at 70% CPU
- PDB: minAvailable 1 guaranteed
- RBAC: least-privilege ServiceAccount

## Security
All images scanned with Trivy. Run ./scan.sh to scan locally.
