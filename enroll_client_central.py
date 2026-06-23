import os, secrets, hashlib, requests
from feature_extractor import extract_fixed_vector

NODE_URLS = ["http://localhost:3000"]

def enroll_user(user_id, fingerprint_vector):
    secret = secrets.token_bytes(32)
    fingerprint_bytes = fingerprint_vector
    payload = {
            "user_id": user_id,
            "fingerprint_hex": fingerprint_bytes.hex(),
    }
    print(payload)
    resp = requests.post(f"{NODE_URLS[0]}/enroll", json=payload, timeout=5)
    resp.raise_for_status()
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