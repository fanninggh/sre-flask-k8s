# sre-flask-k8s

Flask DevOps project — 30-day SRE learning portfolio.

## Stack
- Flask 3.1.3 (Python)
- PostgreSQL 16
- Redis 7

## Run locally
docker compose up -d
curl http://localhost:5000/health

## Images
- GHCR: ghcr.io/fanninggh/flask-devops:latest
- ECR: 779846820095.dkr.ecr.eu-west-1.amazonaws.com/flask-devops:latest

## Security
All images scanned with Trivy before push. Run ./scan.sh to scan locally.
