import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# In‑memory storage for this node's shares (for demonstration only).
# In a production system you would use a persistent database.
shard_store = {}

@app.route('/enroll_share', methods=['POST'])
def enroll_share():
    """Store one share and its corresponding hash for a user."""
    data = request.json
    user_id = data['user_id']
    share_idx = data['share_index']    # e.g., 0,1,2 for a 3‑share scheme
    share_hex = data['share_hex']      # Shamir share in hex
    hash_hex = data['hash_hex']        # stored hash (same across all nodes)

    shard_store[user_id] = {
        "share_idx": share_idx,
        "share_hex": share_hex,
        "hash_hex": hash_hex
    }
    return jsonify({"status": "ok", "node_id": os.getenv("NODE_ID", "unknown")})

@app.route('/verify_get', methods=['POST'])
def verify_get():
    """Return the share and hash for a user (used during verification)."""
    data = request.json
    user_id = data['user_id']
    entry = shard_store.get(user_id)
    if entry is None:
        return jsonify({"error": "user not found"}), 404
    return jsonify({
        "share_hex": entry["share_hex"],
        "hash_hex": entry["hash_hex"],
        "node_id": os.getenv("NODE_ID", "unknown")
    })

@app.route('/health', methods=['GET'])
def health():
    return "OK"

@app.route('/debug/shard_store', methods=['GET'])
def debug_shard_store():
    return jsonify(shard_store)

@app.route('/debug/reset_store', methods=['POST'])
def debug_reset_store():
    shard_store.clear()
    return jsonify({"status": "shard store cleared"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)