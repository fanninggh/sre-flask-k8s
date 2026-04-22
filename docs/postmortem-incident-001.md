# Postmortem — Incident 001: GitOps Resilience Validation

**Date:** 2026-04-22
**Author:** Frank Anning
**Severity:** Low (simulated — no user impact)
**Duration:** ~5 minutes

## Summary

A series of deliberate failure injections were performed against the flask-devops
deployment to validate the resilience of the GitOps pipeline. All incidents were
automatically mitigated by ArgoCD before causing user impact.

## Timeline

| Time | Event |
|------|-------|
| T+00 | kubectl scale flask-devops --replicas=0 |
| T+05 | ArgoCD selfHeal restored 2 replicas within 10 seconds |
| T+60 | kubectl set image with non-existent tag |
| T+65 | ArgoCD reverted image to correct tag immediately |
| T+90 | kubectl rollout undo conflicted with ArgoCD sync |
| T+95 | Manual ArgoCD sync forced — all pods healthy |

## Root Cause

Deliberate fault injection. Controlled drill — no actual root cause.

## What Went Well

- ArgoCD selfHeal restored replicas in under 10 seconds
- PDB minAvailable:1 prevented total outage
- Grafana dashboard showed deployment status in real time
- kubectl rollout history provided full audit trail

## Key Learning

Direct kubectl mutations cannot cause permanent damage in a GitOps environment.
ArgoCD continuously reconciles cluster state against Git. To cause a real incident,
a bad commit must reach main — protected by branch rules, CI, and Trivy scan.

## Action Items

| Action | Priority |
|--------|----------|
| Add runbook for CrashLoopBackOff diagnosis | Medium |
| Configure Alertmanager Slack webhook | Medium |
| Add synthetic health check every 60s | Low |

## Blameless Conclusion

No human error. The simulation confirmed GitOps provides strong automatic recovery.
Defence-in-depth: branch protection + CI pipeline + ArgoCD = hard to break production.
