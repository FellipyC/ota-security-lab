import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

CURRENT_VERSION = "1.0"

SERVER_URL = "http://127.0.0.1:5001"

def check_for_update():

    response = requests.get(
        f"{SERVER_URL}/check-update"
    )

    update_info = response.json()

    latest_version = update_info["version"]
    expected_hash = update_info["sha256"]

    print("Current Version:", CURRENT_VERSION)
    print("Available version:", latest_version)

    if latest_version > CURRENT_VERSION:
        print("[UPDATE AVAILABLE]")
        download_update()
    else:
        print("[NO UPDATE]")

def download_update():

    response = requests.get(
        f"{SERVER_URL}/download"
    )

    update = response.json()

    firmware = update["firmware"]
    signature = bytes.fromhex(update["signature"])

    print("\nFirmware received:")
    print(firmware)

    with open("public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )

    try:
        public_key.verify(
            signature,
            firmware.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        print("[PASS] Firmware signature verified")

        print("\n[INSTALLING UPDATE]")
        print("[UPDATE COMPLETE]")

    except Exception:
        print("[FAIL] Firmware signature verification failed")
        print("[UPDATE REJECTED]")

check_for_update()

