import os
import time, secrets, hashlib, requests
from pyshamir import combine
from feature_extractor import extract_fixed_vector

NODE_URLS = ["http://localhost:5001", "http://localhost:5002", "http://localhost:5003"]
USED_NONCES = set()

def verify_user(user_id, probe_vector):
    nonce = secrets.token_hex(16)
    timestamp = int(time.time())
    if nonce in USED_NONCES:
        return False, "Replay: duplicate nonce"
    if abs(timestamp - int(time.time())) > 5:
        return False, "Replay: stale timestamp"
    USED_NONCES.add(nonce)

    shares = []
    stored_hash = None
    for url in NODE_URLS:
        try:
            resp = requests.post(f"{url}/verify_get", json={"user_id": user_id}, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                shares.append(bytes.fromhex(data["share_hex"]))
                stored_hash = data["hash_hex"]
        except:
            continue
    if len(shares) < 2:
        return False, f"Only {len(shares)} shares available"
    secret = combine(shares[:2])
    xor_data = bytes(a ^ b for a, b in zip(secret, probe_vector))
    h_calc = hashlib.sha256(xor_data).digest().hex()
    return (h_calc == stored_hash), "Authenticated" if h_calc == stored_hash else "Mismatch"

def test_verification(folder, limit=10):
    files = sorted([f for f in os.listdir(folder) if f.endswith('.tif')])[:limit]
    for idx, fname in enumerate(files):
        user_id = f"user_{idx}"
        path = os.path.join(folder, fname)
        vec = extract_fixed_vector(path)
        ok, msg = verify_user(user_id, vec)
        print(f"{user_id} (genuine): {msg}")
        # Impostor test: use next user's fingerprint
        if idx+1 < len(files):
            imp_path = os.path.join(folder, files[idx+1])
            imp_vec = extract_fixed_vector(imp_path)
            ok2, msg2 = verify_user(user_id, imp_vec)
            print(f"{user_id} (impostor): {msg2}")

if __name__ == "__main__":
    test_verification("./fvc2002")