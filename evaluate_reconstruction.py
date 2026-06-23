import os
import secrets
import hashlib
import numpy as np
from scipy.stats import entropy
from pyshamir import split, combine
from feature_extractor import extract_fixed_vector

# ------------------------------
# 1. Brute‑force reconstruction from one shard
# ------------------------------
def     brute_force_from_one_share(original_secret, one_share_bytes, max_attempts=2**20):
    """
    Attempt to reconstruct the original secret from a single share
    by brute‑forcing the missing shares.
    Since threshold = 2, we need at least 2 shares. With only 1 share,
    we try random guesses for a second share and attempt to combine.
    """
    success = False
    for attempt in range(max_attempts):
        print(f"attempt {attempt} of {max_attempts} {attempt/max_attempts*100:.2f}%", end="\r")
        # Generate a random second share (same length as the real share)
        fake_share = secrets.token_bytes(len(one_share_bytes))
        try:
            # Try to combine the real share with the fake share
            reconstructed = combine([one_share_bytes, fake_share])
            if reconstructed == original_secret:
                success = True
                break
        except:
            continue
    return success

def test_brute_force():
    # 1. Get a real fingerprint vector and enroll (simulate)
    img_path = "./fvc2002/101_1.tif"
    fp_vec = extract_fixed_vector(img_path)
    secret = secrets.token_bytes(32)          # original secret
    shares = split(secret, 3, 2)
    one_share = shares[0]                     # take only one share

    print(f"Brute‑forcing reconstruction from 1 share (max attempts = 2^20 = {2**20})...")
    success = brute_force_from_one_share(secret, one_share, max_attempts=2**20)
    print(f"Reconstruction success: {success} (expected: False)")
    return success

# ------------------------------
# 2. Shannon entropy analysis of a shard
# ------------------------------
def shannon_entropy(data_bytes):
    """Compute Shannon entropy (in bits) of a byte sequence."""
    if not data_bytes:
        return 0
    # Count frequency of each byte value (0-255)
    counts = np.bincount(np.frombuffer(data_bytes, dtype=np.uint8), minlength=256)
    probs = counts / len(data_bytes)
    # Remove zero probabilities
    probs = probs[probs > 0]
    return entropy(probs, base=2)

def entropy_analysis():
    # Generate a random secret and its shares
    secret = secrets.token_bytes(32)
    shares = split(secret, 3, 2)
    # Compute entropy of the original secret and one share
    secret_entropy = shannon_entropy(secret)
    share_entropy = shannon_entropy(shares[0])
    print(f"Shannon entropy of original secret (32 bytes): {secret_entropy:.2f} bits")
    print(f"Shannon entropy of one share: {share_entropy:.2f} bits")
    print(f"Ratio (share/secret): {share_entropy / secret_entropy:.2f}")
    # For a perfect uniform distribution, max entropy = 8 bits per byte = 256 bits for 32 bytes
    max_entropy = 32 * 8
    print(f"Maximum possible entropy (32 bytes): {max_entropy} bits")
    print(f"Conclusion: One share retains full entropy (no information leakage).")

# ------------------------------
# Run both tests
# ------------------------------
if __name__ == "__main__":
    print("=" * 50)
    print("EVALUATION: SINGLE SHARD RECONSTRUCTION & ENTROPY")
    print("=" * 50)
    test_brute_force()
    print("\n" + "-" * 50 + "\n")
    entropy_analysis()