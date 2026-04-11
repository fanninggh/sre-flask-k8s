#!/bin/bash
set -e

echo "==> Scanning flask-devops:v1 for HIGH/CRITICAL CVEs..."
trivy image --severity HIGH,CRITICAL --ignore-unfixed flask-devops:v1

echo ""
echo "==> Scanning project files for secrets..."
trivy fs . --scanners secret

echo ""
echo "==> Scanning Python dependencies..."
trivy fs . --scanners vuln

echo ""
echo "==> All scans complete. If no findings above -- you are clean."
