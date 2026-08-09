import requests
import hashlib

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
        download_update(expected_hash)
    else:
        print("[NO UPDATE]")

def download_update(expected_hash):

    response = requests.get(
        f"{SERVER_URL}/download"
    )

    firmware = response.text

    firmware_hash = hashlib.sha256(
        firmware.encode()
    ).hexdigest()
    
    print("\nFirmware received:")
    print(firmware)

    print("SHA-256:", firmware_hash)

    if firmware_hash == expected_hash:
        print("[PASS] Firmware integrity verified")
    else:
        print("[FAIL] Firmware integrity check failed")
        print("[UPDATE REJECTED]")
        return

    print("\n[INSTALLING UPDATE]")
    print("[UPDATE COMPLETE]")

check_for_update()

