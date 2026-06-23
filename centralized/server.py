from flask import Flask, request, jsonify
import hashlib, secrets
from feature_extractor import extract_fixed_vector

app = Flask(__name__)
db = {}

@app.route('/enroll', methods=['POST'])
def enroll():
    data = request.json
    uid = data['user_id']
    fp = bytes.fromhex(data['fingerprint_hex'])
    secret = secrets.token_bytes(32)
    xor_data = bytes(a ^ b for a, b in zip(secret, fp))
    h = hashlib.sha256(xor_data).digest().hex()
    db[uid] = (secret.hex(), h)
    return jsonify({"ok": True})

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    uid = data['user_id']
    fp = bytes.fromhex(data['fingerprint_hex'])
    if uid not in db:
        return jsonify({"auth": False})
    secret_hex, stored_hash = db[uid]
    secret = bytes.fromhex(secret_hex)
    xor_data = bytes(a ^ b for a, b in zip(secret, fp))
    h_calc = hashlib.sha256(xor_data).digest().hex()
    return jsonify({"auth": h_calc == stored_hash})

@app.route('/debug/store', methods=['GET'])
def debug_shard_store():
    return jsonify(db)

@app.route('/debug/reset_store', methods=['POST'])
def debug_reset_store():
    db.clear()
    return jsonify({"status": "store cleared"})

@app.route('/eval/fingerprint_ops', methods=['GET'])
def debug_shard_store():
    return jsonify(db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)