import argparse
import subprocess
import time
import multiprocessing
import os

def cpu_load_test(max_cpu_percent, duration_seconds):
    print(f"Starting CPU Load Test with max {max_cpu_percent}% CPU usage for {duration_seconds} seconds.")

    num_threads = int(max_cpu_percent * 0.01 * multiprocessing.cpu_count())

    stress_command = f"stress --cpu {num_threads} --timeout {duration_seconds}s"
    subprocess.Popen(stress_command, shell=True).wait()

    print("CPU Load Test Completed.")

def memory_load_test(max_memory_mb, duration_seconds):
    print(f"Starting Memory Load Test with max {max_memory_mb}MB memory consumption for {duration_seconds} seconds.")

    data = b"1" * (max_memory_mb * 1024 * 1024)  # 1MB data as bytes

    start_time = time.time()
    end_time = start_time + duration_seconds

    while time.time() < end_time:
        with open("/tmp/memory_load_test_file", "wb") as file:
            file.write(data)
        os.remove("/tmp/memory_load_test_file")

    print("Memory Load Test Completed.")

def network_load_test(target_ip, target_port, duration_seconds, verbose):
    log_file = "iperf3_log.txt"

    print(f"Starting Network Load Test to {target_ip}:{target_port} using iperf3 for {duration_seconds} seconds.")

    if verbose:
        iperf3_command = f"iperf3 -c {target_ip} -p {target_port} -t {duration_seconds} -P 10"
        with open(log_file, "w") as log:
            subprocess.Popen(iperf3_command, shell=True, stdout=log, stderr=subprocess.STDOUT).wait()
    else:
        iperf3_command = f"iperf3 -c {target_ip} -p {target_port} -t {duration_seconds} -P 10 > /dev/null 2>&1"
        subprocess.Popen(iperf3_command, shell=True).wait()

    print("Network Load Test Completed.")

    if verbose:
        with open(log_file, "r") as log:
            print("\niperf3 Log:")
            print(log.read())
        os.remove(log_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Non-interactive Load Testing Program for Linux. Created by Michael Trip and ChatGPT. Uses iperf3 and stress-ng")
    parser.add_argument("--max-cpu", type=int, help="Maximum CPU usage percentage during the CPU test")
    parser.add_argument("--max-memory", type=int, help="Maximum memory usage in MB during the memory test")
    parser.add_argument("--target-ip", type=str, help="Target IP address for iperf3 network testing. This needs a 3rd party iperf3 server.")
    parser.add_argument("--target-port", type=int, help="Target port for iperf3 network testing. This needs a 3rd party iperf3 server.")
    parser.add_argument("--duration", type=int, help="Duration of the load tests in seconds")
    parser.add_argument("--verbose", action="store_true", help="Display verbose output (iperf3 log)")
    args = parser.parse_args()

    processes = []

    if args.max_cpu:
        cpu_process = multiprocessing.Process(target=cpu_load_test, args=(args.max_cpu, args.duration))
        processes.append(cpu_process)
    if args.max_memory:
        memory_process = multiprocessing.Process(target=memory_load_test, args=(args.max_memory, args.duration))
        processes.append(memory_process)
    if args.target_ip and args.target_port:
        network_process = multiprocessing.Process(target=network_load_test, args=(args.target_ip, args.target_port, args.duration, args.verbose))
        processes.append(network_process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()