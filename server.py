from flask import Flask, jsonify
import os
import hashlib

app = Flask(__name__)

# Simulated firmware information
firmware = { 
    "version": "1.1",
    "file": "firmware.txt"
}

def calculate_firmware_hash():
    firmware_path = os.path.join(
        os.path.dirname(__file__),
        "firmware.txt"
    )

    with open(firmware_path, "rb") as file:
        firmware_data = file.read()

    return hashlib.sha256(firmware_data).hexdigest()

@app.route("/check-update", methods=["GET"])
def check_update():
    firmware_info = {
        "version": firmware["version"],
        "file": firmware["file"],
        "sha256": calculate_firmware_hash()
    }

    return jsonify(firmware_info)

@app.route("/download", methods=["GET"])
def download_firmware():
    firmware_path = os.path.join(
        os.path.dirname(__file__),
        "firmware.txt"
    )

    signature_path = os.path.join(
        os.path.dirname(__file__),
        "firmware.sig"
    )

    with open(firmware_path, "r") as file:
        firmware_data = file.read()

    with open(signature_path, "rb") as file:
        signature_data = file.read()

    return jsonify({
        "firmware": firmware_data,
        "signature": signature_data.hex()
    })
    
if __name__ == "__main__":
    app.run(port=5001)