# sre-flask-k8s

![CI](https://github.com/fanninggh/sre-flask-k8s/actions/workflows/ci.yml/badge.svg)

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

## CI Pipeline
Every push triggers: test (3.11/3.12) -> Trivy scan -> build -> push to GHCR

## Security
All images scanned with Trivy. Run ./scan.sh to scan locally.
