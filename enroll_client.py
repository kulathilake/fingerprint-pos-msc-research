import os, secrets, hashlib, requests
from pyshamir import split
from feature_extractor import extract_fixed_vector

NODE_URLS = ["http://localhost:5001", "http://localhost:5002", "http://localhost:5003"]

def enroll_user(user_id, fingerprint_vector):
    secret = secrets.token_bytes(32)
    xor_data = bytes(a ^ b for a, b in zip(secret, fingerprint_vector))
    h = hashlib.sha256(xor_data).digest().hex()
    shares = split(secret, 3, 2)   # returns list of bytearrays

    # for i, share_bytes in enumerate(shares):
    #     payload = {
    #         "user_id": user_id,
    #         "share_index": i,
    #         "share_hex": share_bytes.hex(),
    #         "hash_hex": h
    #     }
    #     resp = requests.post(f"{NODE_URLS[i]}/enroll_share", json=payload, timeout=5)
    #     resp.raise_for_status()
    print(f"Enrolled {user_id}")
    return True

def batch_enroll(folder, limit=10):
    files = sorted([f for f in os.listdir(folder) if f.endswith('.tif')])[:limit]
    for idx, fname in enumerate(files):
        user_id = f"user_{idx}"
        path = os.path.join(folder, fname)
        vec = extract_fixed_vector(path)
        enroll_user(user_id, vec)

if __name__ == "__main__":
    batch_enroll("./fvc2002", limit=10)