# Flask Probe Simulation Application

## Overview

This repository contains a Python Flask application designed to demonstrate the use of Kubernetes probes: Startup, Liveness, and Readiness. For each probe, the application supports delays, chaos injection and permanent failure.

Endpoints can be accessed via http or via files (for example, cat /healthz). Successful operations result in OK, failures will return ERROR.

Request information and status provided as logs in the running container, allowing you to see the probes being actioned from the container view.

## Env Parameters

- `PORT`: Port on which the Flask application will run (default: `8080`)

## Endpoints & Env Parameters

### http:`/startup` file:`/startup`

- **Description**: Simulates the initial startup phase, useful for startup probe testing.
- **Env Parameters**:
  - `STARTUP_DELAY`: Time in seconds to delay the startup response (default: `0`). A value of `0` means no intentional delay.
  - `STARTUP_CHAOS_FREQUENCY`: Number of calls after which a failure is simulated (default: `0`). A value of `0` means the chaos feature is disabled.
  - `STARTUP_PERMANENT_FAILURE_THRESHOLD`: Number of calls after which permanent failure is activated (default: `0`). A value of `0` means this feature is disabled.

### http:`/ready` file:`/ready`

- **Description**: Represents a readiness probe that checks whether the service is ready to handle traffic.
- **Env Parameters**:
  - `READY_DELAY`: Time in seconds to delay the readiness response (default: `0`). A value of `0` means no intentional delay.
  - `READY_CHAOS_FREQUENCY`: Number of calls after which a failure is simulated (default: `0`). A value of `0` means the chaos feature is disabled.
  - `READY_PERMANENT_FAILURE_THRESHOLD`: Number of calls after which permanent failure is activated (default: `0`). A value of `0` means this feature is disabled.

### http:`/healthz` file:`/healthz`

- **Description**: Acts as a health check probe to monitor the ongoing status of the application.
- **Env Parameters**:
  - `HEALTHZ_DELAY`: Time in seconds to delay the health check response (default: `0`). A value of `0` means no intentional delay.
  - `HEALTHZ_CHAOS_FREQUENCY`: Number of calls after which a failure is simulated (default: `0`). A value of `0` means the chaos feature is disabled.
  - `HEALTHZ_PERMANENT_FAILURE_THRESHOLD`: Number of calls after which permanent failure is activated (default: `0`). A value of `0` means this feature is disabled.

## Example usage with a Liveness Probe in Kubernetes

### httpGet

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  periodSeconds: 5
  timeoutSeconds: 1
  initialDelaySeconds: 10
  failureThreshold: 15
```

### exec (file based, checking file for OK status)

```yaml
livenessProbe:
  exec:
    command:
    - /bin/sh
    - -c
    - 'grep -q "OK" /healthz'
  periodSeconds: 5
  timeoutSeconds: 1
  initialDelaySeconds: 10
  failureThreshold: 15
```

## Container Image

Available as a multi-arch container via Docker Hub at [spurin/readiness-liveness-startup-probe-api](https://hub.docker.com/r/spurin/readiness-liveness-startup-probe-api)
