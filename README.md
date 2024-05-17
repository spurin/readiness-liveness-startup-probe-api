# Flask Probe Simulation Application

## Overview

This repository contains a Python Flask application designed to demonstrate the use of Kubernetes probes: Startup, Liveness, and Readiness. For each probe, the application supports delays, chaos injection and permanent failure.

## Endpoints

### `/startup`

- **Description**: Simulates the initial startup phase, useful for startup probe testing.
- **Parameters**:
  - `STARTUP_DELAY`: Time in seconds to delay the startup response (default: `0`). A value of `0` means no intentional delay.
  - `STARTUP_CHAOS_FREQUENCY`: Number of calls after which a failure is simulated (default: `0`). A value of `0` means the chaos feature is disabled.
  - `STARTUP_PERMANENT_FAILURE_THRESHOLD`: Number of calls after which permanent failure is activated (default: `0`). A value of `0` means this feature is disabled.

### `/ready`

- **Description**: Represents a readiness probe that checks whether the service is ready to handle traffic.
- **Parameters**:
  - `READY_DELAY`: Time in seconds to delay the readiness response (default: `0`). A value of `0` means no intentional delay.
  - `READY_CHAOS_FREQUENCY`: Number of calls after which a failure is simulated (default: `0`). A value of `0` means the chaos feature is disabled.
  - `READY_PERMANENT_FAILURE_THRESHOLD`: Number of calls after which permanent failure is activated (default: `0`). A value of `0` means this feature is disabled.

### `/healthz`

- **Description**: Acts as a health check probe to monitor the ongoing status of the application.
- **Parameters**:
  - `HEALTHZ_DELAY`: Time in seconds to delay the health check response (default: `0`). A value of `0` means no intentional delay.
  - `HEALTHZ_CHAOS_FREQUENCY`: Number of calls after which a failure is simulated (default: `0`). A value of `0` means the chaos feature is disabled.
  - `HEALTHZ_PERMANENT_FAILURE_THRESHOLD`: Number of calls after which permanent failure is activated (default: `0`). A value of `0` means this feature is disabled.

## Container Image

Available as a multi-arch container via Docker Hub at spurin/readiness-liveness-startup-probe-api
