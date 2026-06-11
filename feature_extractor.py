import hashlib
import numpy as np
from fingerprints import Fingerprint
import cv2

def extract_fingerprint_features(image_path, vector_size=128):
    """
    Extract a fixed length byte vector from a fingerprint image
    Returns a bytes object suitable for hashing
    """
    # Load the fingerprint image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Could not load image at {image_path}")
    # Preprocess the image (e.g., enhance contrast)
    image = cv2.equalizeHist(image)

    # Extract features using SourceAFIS
    fingerprint = Fingerprint(image)
    template = fingerprint.to_template()
    
    # Convert the template to a fixed-length byte vector
    hashed = hashlib.sha256(template).digest()  # Get a 32-byte hash

    if len(hashed) < vector_size:
        # Pad with zeros if the hash is shorter than the desired vector size
        hashed += bytes(vector_size - len(hashed))
    else:        # Truncate if the hash is longer than the desired vector size
        hashed = hashed[:vector_size]
