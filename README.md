# LoadGenerator

## Purpose

I have written this LoadGenerator for showcasing loads in a Kubernetes cluster. Especially i wanted to show graphs in Grafana with load generated on a Kubernetes cluster.

## Arguments

```
usage: load_testing.py [-h] [--max-cpu MAX_CPU] [--max-memory MAX_MEMORY] [--target-ip TARGET_IP] [--target-port TARGET_PORT]
                       [--duration DURATION] [--verbose]

Non-interactive Load Testing Program for Linux. Created by Michael Trip and ChatGPT. Uses iperf3 and stress-ng

options:
  -h, --help            show this help message and exit
  --max-cpu MAX_CPU     Maximum CPU usage percentage during the CPU test
  --max-memory MAX_MEMORY
                        Maximum memory usage in MB during the memory test
  --target-ip TARGET_IP
                        Target IP address for iperf3 network testing. This needs a 3rd party iperf3 server.
  --target-port TARGET_PORT
                        Target port for iperf3 network testing. This needs a 3rd party iperf3 server.
  --duration DURATION   Duration of the load tests in seconds
  --verbose             Display verbose output (iperf3 log)
```

## How to use this

### Docker

```bash
$ docker run -it --rm ghcr.io/michaeltrip/loadtester:latest --help

usage: load_testing.py [-h] [--max-cpu MAX_CPU] [--max-memory MAX_MEMORY] [--target-ip TARGET_IP] [--target-port TARGET_PORT]
                       [--duration DURATION] [--verbose]

Non-interactive Load Testing Program for Linux. Created by Michael Trip and ChatGPT. Uses iperf3 and stress-ng

options:
  -h, --help            show this help message and exit
  --max-cpu MAX_CPU     Maximum CPU usage percentage during the CPU test
  --max-memory MAX_MEMORY
                        Maximum memory usage in MB during the memory test
  --target-ip TARGET_IP
                        Target IP address for iperf3 network testing. This needs a 3rd party iperf3 server.
  --target-port TARGET_PORT
                        Target port for iperf3 network testing. This needs a 3rd party iperf3 server.
  --duration DURATION   Duration of the load tests in seconds
  --verbose             Display verbose output (iperf3 log)

```

### Podman
```bash
$ podman run -it --rm ghcr.io/michaeltrip/loadtester:latest --help

```

### Kubernetes

You can decide what you want to do. You can use this is as a job, as a one time running pod or maybe as a interactive shell for interactive testing.

#### Jobs

The example of a job can be found in the `kubernetes_examples/job.yaml` file

#### Run as a one time pod:

```bash
$ kubectl run loadgenerator-pod --image=ghcr.io/michaeltrip/loadgenerator:latest -- --max-cpu 50 --max-memory 512 --target-ip iperf3test.iperf --port 5301

```
