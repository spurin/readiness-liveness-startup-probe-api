# Readiness Liveness Startup Probe API

## Overview

This repository provides the source code used for the [spurin/readiness-liveness-startup-probe-api](https://hub.docker.com/r/spurin/readiness-liveness-startup-probe-api) container image. Designed to provide behind the scenes information when making use of Kubernetes Startup, Liveness, and Readiness probes. Each probe endpoint can be optionally customised with intentional delays (during which, requests will fail), chaos injection, , timed success/failure intervals and permanent failure after a specified number of calls.

Endpoints are accessible both via `http` and/or via `file` access (for example, by using `cat /healthz` in the running container). Successful operations return OK, failures return ERROR.

This container image was created as Kubernetes Startup, Liveness and Readiness probes operate in a black-box fashion. They're actioned from Kubernetes and unless a probe fails, we have no visibility whether a probe was executed and if it was successful. This container image tracks and logs all probe requests made via `http` and/or via local `file` read access. You're able to see the request that was made, whether it succeeded or failed, the request count and also the number of consecutive successes or failures.

### Example container log output

```
19:45:52 - INFO - Healthz probe successful: request_count:4, consecutive_success:1, consecutive_failures:0
19:45:52 - INFO - Ready probe successful: request_count:5, consecutive_success:3, consecutive_failures:0
19:45:57 - INFO - Ready probe successful: request_count:6, consecutive_success:4, consecutive_failures:0
19:45:57 - INFO - Healthz probe successful: request_count:5, consecutive_success:2, consecutive_failures:0
19:46:02 - INFO - Ready probe successful: request_count:7, consecutive_success:5, consecutive_failures:0
19:46:07 - INFO - Healthz probe successful: request_count:7, consecutive_success:1, consecutive_failures:0
```

## Env Parameters

- `PORT`: Port on which the application will run (default: `8080`)

## Endpoints & Env Parameters

### http:`/startup` file:`/startup`

- **Description**: Simulates the initial startup phase, useful for startup probe testing.
- **Env Parameters**:
  - `STARTUP_DELAY`: Time in seconds to delay and error any startup responses (default: `0`). A value of `0` means no intentional delay.
  - `STARTUP_CHAOS_FREQUENCY`: Number of calls after which a failure is simulated (default: `0`). A value of `0` means the chaos feature is disabled.
  - `STARTUP_PERMANENT_FAILURE_THRESHOLD`: Number of calls after which permanent failure is activated (default: `0`). A value of `0` means this feature is disabled.

### http:`/ready` file:`/ready`

- **Description**: Represents a readiness probe that checks whether the service is ready to handle traffic.
- **Env Parameters**:
  - `READY_DELAY`: Time in seconds to delay and error any readiness responses (default: `0`). A value of `0` means no intentional delay.
  - `READY_CHAOS_FREQUENCY`: Number of calls after which a failure is simulated (default: `0`). A value of `0` means the chaos feature is disabled.
  - `READY_PERMANENT_FAILURE_THRESHOLD`: Number of calls after which permanent failure is activated (default: `0`). A value of `0` means this feature is disabled.
  - `READY_SUCCESS_INTERVAL`: Duration in seconds the readiness probe will report success before failing (default: `0`).
  - `READY_FAILURE_INTERVAL`: Duration in seconds the readiness probe will report failure before returning to success (default: `0`).

### http:`/healthz` file:`/healthz`

- **Description**: Acts as a health check probe to monitor the ongoing status of the application.
- **Env Parameters**:
  - `HEALTHZ_DELAY`: Time in seconds to delay and error any health check responses (default: `0`). A value of `0` means no intentional delay.
  - `HEALTHZ_CHAOS_FREQUENCY`: Number of calls after which a failure is simulated (default: `0`). A value of `0` means the chaos feature is disabled.
  - `HEALTHZ_PERMANENT_FAILURE_THRESHOLD`: Number of calls after which permanent failure is activated (default: `0`). A value of `0` means this feature is disabled.
  - `HEALTHZ_SUCCESS_INTERVAL`: Duration in seconds the health check will report success before failing (default: `0`).
  - `HEALTHZ_FAILURE_INTERVAL`: Duration in seconds the health check will report failure before returning to success (default: `0`).

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

Available as a multi-arch container via Docker Hub at [spurin/readiness-liveness-startup-probe-api](https://hub.docker.com/r/spurin/readiness-liveness-startup-probe-api) - See [Tags](https://hub.docker.com/r/spurin/readiness-liveness-startup-probe-api/tags) for all available architectures.
