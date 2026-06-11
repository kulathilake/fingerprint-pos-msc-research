import os
import secrets
import hashlib
import json
import pickle
import requests
from pyshamir import split
from feature_extractor import extract_fixed_vector

# Configuration
COORDINATOR_URL = "http://localhost:6379"   # not used in this script; metadata stored in Redis
NODE_URLS = [
    "http://localhost:5001",
    "http://localhost:5002",
    "http://localhost:5003"
]
VECTOR_LEN = 512   # must match feature_extractor.py

def enroll_user(user_id, fingerprint_vector):
    # 1. Generate random secret (32 bytes = 256 bits)
    secret = secrets.token_bytes(32)

    # 2. Compute the hash that will be used for verification later
    # Hash = SHA256( secret XOR fingerprint_vector )
    xor_data = bytes(a ^ b for a, b in zip(secret, fingerprint_vector))
    h = hashlib.sha256(xor_data).digest().hex()

    # 3. Split secret into 3 shares (threshold = 2)
    # pyshamir.split returns a list of (idx, share_bytes)
    shares = split(secret, num_shares=3, threshold=2)

    # 4. Send each share to a different POS node
    for i, (idx, share_bytes) in enumerate(shares):
        share_hex = share_bytes.hex()
        payload = {
            "user_id": user_id,
            "share_index": idx,
            "share_hex": share_hex,
            "hash_hex": h
        }
        try:
            resp = requests.post(f"{NODE_URLS[i]}/enroll_share", json=payload, timeout=5)
            resp.raise_for_status()
        except Exception as e:
            print(f"Error enrolling share {i} for {user_id}: {e}")
            return False
    # Store the mapping (user → list of nodes) in the coordinator (Redis)
    try:
        mapping = {
            "nodes": NODE_URLS,
            "user_id": user_id,
            "hash": h
        }
        r = requests.post(f"{COORDINATOR_URL}/set/{user_id}", json=mapping, timeout=5)
    except:
        # If coordinator is not used, it's optional; we can rely on a static mapping
        pass
    return True

def batch_enroll(image_folder, user_id_prefix="user"):
    enrolled = 0
    # Collect all TIFF files
    files = sorted([f for f in os.listdir(image_folder) if f.lower().endswith('.tif')])
    if not files:
        print(f"No .tif files found in {image_folder}")
        return

    for idx, fname in enumerate(files[:10]):   # start with 10 users
        full_path = os.path.join(image_folder, fname)
        user_id = f"{user_id_prefix}_{idx}"
        try:
            fp_vec = extract_fixed_vector(full_path, VECTOR_LEN)
            ok = enroll_user(user_id, fp_vec)
            if ok:
                enrolled += 1
                print(f"Enrolled {user_id} ({fname})")
            else:
                print(f"Failed to enroll {user_id} ({fname})")
        except Exception as e:
            print(f"Error processing {fname}: {e}")
    print(f"Enrolled {enrolled} users.")

if __name__ == "__main__":
    # Path to the extracted FVC2002 DB1_B folder
    DB_PATH = "./fvc2002"   # adjust if needed
    batch_enroll(DB_PATH)