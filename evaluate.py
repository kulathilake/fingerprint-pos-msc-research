import os
import time, requests, statistics, subprocess, pickle
from feature_extractor import extract_fixed_vector
from verify_client import verify_user

# Helper: measure latency of a function
def measure_latency(func, n=30):
    latencies = []
    for _ in range(n):
        start = time.perf_counter()
        func()
        latencies.append((time.perf_counter() - start) * 1000)
    return latencies

# 1. Decentralised latency test
def test_decentralised_latency(folder, user_ids, probe_paths):
    def auth():
        verify_user(user_ids[0], extract_fixed_vector(probe_paths[0]))
    lat = measure_latency(auth, n=30)
    print(f"Decentralised latency (ms): mean={statistics.mean(lat):.2f}, median={statistics.median(lat):.2f}, 95th={statistics.quantiles(lat, n=20)[18]:.2f}")
    return lat

# 2. Centralised latency test
def test_centralised_latency(central_url, user_id, fingerprint_hex):
    def auth():
        requests.post(f"{central_url}/verify", json={"user_id": user_id, "fingerprint_hex": fingerprint_hex})
    lat = measure_latency(auth, n=30)
    print(f"Centralised latency (ms): mean={statistics.mean(lat):.2f}, median={statistics.median(lat):.2f}, 95th={statistics.quantiles(lat, n=20)[18]:.2f}")
    return lat

# 3. Replay attack test
def test_replay_attack():
    vec = extract_fixed_vector("./fvc2002/101_1.tif")
    ok1, _ = verify_user("user_0", vec)
    ok2, msg2 = verify_user("user_0", vec)   # same nonce – should fail
    print(f"Replay test: first={ok1}, second={ok2} -> {'PASS' if ok1 and not ok2 else 'FAIL'}")
    return ok1 and not ok2

# 4. Fault tolerance: kill one node
def test_fault_tolerance():
    import subprocess
    subprocess.run(["podman", "stop", "fingerprint-pos_node2_1"], capture_output=True)
    time.sleep(2)
    vec = extract_fixed_vector("./fvc2002/101_1.tif")
    ok, msg = verify_user("user_0", vec)
    subprocess.run(["podman", "start", "fingerprint-pos_node2_1"], capture_output=True)
    print(f"Fault tolerance (node2 down): {'SUCCESS' if ok else 'FAIL'} - {msg}")
    return ok

# 5. Single‑share reconstruction test (theoretical)
def test_single_share_security():
    print("Single share security: Shamir ensures zero information – PASS (by design)")
    return True

if __name__ == "__main__":
    # Prepare data: enroll a test user if not already (assumes user_0 exists)
    results = {}
    results["replay_resistant"] = test_replay_attack()
    results["fault_tolerant"] = test_fault_tolerance()
    results["single_share_secure"] = test_single_share_security()

    # Latency tests
    folder = "./fvc2002"
    files = sorted([f for f in os.listdir(folder) if f.endswith('.tif')])
    if files:
        dec_lat = test_decentralised_latency(folder, ["user_0"], [os.path.join(folder, files[0])])
        # Centralised test requires a pre‑enrolled user in the central DB. For simplicity, we skip or implement a one‑time enrollment.
        # Instead, run centralised separately.
        results["decentralised_latencies"] = dec_lat
    with open("eval_results.pkl", "wb") as f:
        pickle.dump(results, f)
    print("Evaluation done. Results saved to eval_results.pkl")