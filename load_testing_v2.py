import argparse
import subprocess
import time
import multiprocessing
import os
import random

def random_cpu_load(duration_seconds):
    start_time = time.time()
    end_time = start_time + duration_seconds

    while time.time() < end_time:
        # Generate a random CPU load between 10% and 90%
        cpu_load_percent = random.uniform(10, 90)
        num_threads = int(cpu_load_percent * 0.01 * multiprocessing.cpu_count())

        stress_command = f"stress-ng --cpu {num_threads} --timeout 1s"
        subprocess.Popen(stress_command, shell=True).wait()

def random_memory_load(max_memory_mb, duration_seconds):
    start_time = time.time()
    end_time = start_time + duration_seconds

    while time.time() < end_time:
        # Generate a random memory load between 10% and 90% of max_memory_mb
        memory_load_mb = random.uniform(max_memory_mb * 0.1, max_memory_mb * 0.9)
        data = b"1" * int(memory_load_mb * 1024 * 1024)  # Convert to bytes

        with open("/tmp/memory_load_test_file", "wb") as file:
            file.write(data)

        time.sleep(1)  # Sleep for 1 second to control memory load

def random_network_load(target_ip, target_port, duration_seconds, max_mbps, verbose):
    log_file = "iperf3_log.txt" if verbose else "/dev/null"

    start_time = time.time()
    end_time = start_time + duration_seconds

    print(f"Starting Random Network Load Test to {target_ip}:{target_port} using iperf3 for {duration_seconds} seconds.")

    while time.time() < end_time:
        # Generate a random network load between 10% and 90% of max_mbps
        network_load_mbps = random.uniform(max_mbps * 0.1, max_mbps * 0.9)

        iperf3_command = f"iperf3 -c {target_ip} -p {target_port} -t 1 -P 10 -b {network_load_mbps}M >> {log_file}"
        subprocess.Popen(iperf3_command, shell=True).wait()

    print("Random Network Load Test Completed.")

    if verbose:
        with open(log_file, "r") as log:
            print("\niperf3 Log:")
            print(log.read())
        os.remove(log_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Non-interactive Load Testing Program for Linux")
    parser.add_argument("--max-cpu", type=int, help="Maximum CPU usage percentage during the CPU test")
    parser.add_argument("--max-memory", type=int, help="Maximum memory usage in MB during the memory test")
    parser.add_argument("--target-ip", type=str, help="Target IP address for iperf3 network testing")
    parser.add_argument("--target-port", type=int, help="Target port for iperf3 network testing")
    parser.add_argument("--duration", type=int, help="Duration of the load tests in seconds")
    parser.add_argument("--max-mbps", type=int, help="Maximum network bandwidth in Mbps for network testing")
    parser.add_argument("--verbose", action="store_true", help="Display verbose output (iperf3 log)")
    args = parser.parse_args()

    processes = []

    if args.max_cpu:
        cpu_process = multiprocessing.Process(target=random_cpu_load, args=(args.duration,))
        processes.append(cpu_process)
    if args.max_memory:
        memory_process = multiprocessing.Process(target=random_memory_load, args=(args.max_memory, args.duration))
        processes.append(memory_process)
    if args.target_ip and args.target_port and args.max_mbps:
        network_process = multiprocessing.Process(target=random_network_load, args=(args.target_ip, args.target_port, args.duration, args.max_mbps, args.verbose))
        processes.append(network_process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()
