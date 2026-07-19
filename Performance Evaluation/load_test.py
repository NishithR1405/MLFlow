"""
Load Test Script - Replicates Apache JMeter Thread Group configuration:
Number of Threads: 10
Ramp-Up Period: 5 seconds
Loop Count: 20
Target: GET http://127.0.0.1:8000/predict?temp=28
"""
import time
import threading
import requests
import statistics

URL = "http://127.0.0.1:8000/predict"
PARAMS = {"temp": 28}

NUM_THREADS = 10
RAMP_UP_SECONDS = 5
LOOP_COUNT = 20

results = []
errors = 0
lock = threading.Lock()

def worker(thread_id, start_delay):
    global errors
    time.sleep(start_delay)
    for _ in range(LOOP_COUNT):
        start = time.perf_counter()
        try:
            r = requests.get(URL, params=PARAMS, timeout=5)
            elapsed_ms = (time.perf_counter() - start) * 1000
            with lock:
                if r.status_code == 200:
                    results.append(elapsed_ms)
                else:
                    errors += 1
        except Exception:
            with lock:
                errors += 1

def main():
    threads = []
    delay_step = RAMP_UP_SECONDS / NUM_THREADS
    test_start = time.perf_counter()

    for i in range(NUM_THREADS):
        t = threading.Thread(target=worker, args=(i, i * delay_step))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    test_duration = time.perf_counter() - test_start
    total_requests = NUM_THREADS * LOOP_COUNT

    print("===== JMeter-Equivalent Summary / Aggregate Report =====")
    print(f"Total Samples (Requests): {total_requests}")
    print(f"Successful Requests: {len(results)}")
    print(f"Failed Requests (Errors): {errors}")
    print(f"Error %: {round((errors / total_requests) * 100, 2)}%")
    print(f"Test Duration: {round(test_duration, 2)} s")

    if results:
        print(f"Average Latency: {round(statistics.mean(results), 2)} ms")
        print(f"Minimum Response Time: {round(min(results), 2)} ms")
        print(f"Maximum Response Time: {round(max(results), 2)} ms")
        print(f"Median Response Time: {round(statistics.median(results), 2)} ms")
        sorted_r = sorted(results)
        p90 = sorted_r[int(len(sorted_r) * 0.90) - 1]
        print(f"90th Percentile: {round(p90, 2)} ms")
        throughput = total_requests / test_duration
        print(f"Throughput: {round(throughput, 2)} requests/second")

if __name__ == "__main__":
    main()
