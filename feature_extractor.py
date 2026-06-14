import hashlib
import cv2
import fingerprint_feature_extractor

def extract_fixed_vector(image_path, vector_length=512):
    """
    Load fingerprint image, extract minutiae, convert to fixed-length byte vector.
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Cannot read {image_path}")

    # 1. Extract minutiae: returns terminations and bifurcations as lists of (x,y)
    terminations, bifurcations = fingerprint_feature_extractor.extract_minutiae_features(img)

    # 2. Convert the minutiae set into a stable string representation
    #    (ensure reproducibility: sort coordinates)
    term_str = str(terminations)
    bif_str = str(bifurcations)
    combined = f"{term_str}{bif_str}".encode('utf-8')

    # 3. Hash to fixed length
    hashed = hashlib.sha256(combined).digest()

    # 4. Trim or pad to exactly `vector_length` bytes
    if len(hashed) > vector_length:
        return hashed[:vector_length]
    else:
        return hashed + b'\x00' * (vector_length - len(hashed))