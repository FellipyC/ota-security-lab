# Automotive OTA Security Lab

A hands-on cybersecurity lab that simulates an automotive Over-the-Air (OTA) firmware update process and demonstrates how cryptographic signatures can prevent unauthorized firmware from being installed.

## Overview

Modern connected vehicles rely on OTA updates to deliver software and firmware updates to electronic control units (ECUs), infotainment systems, and other vehicle components.

This project simulates a simplified OTA architecture consisting of:

* A firmware server
* A vehicle client
* Firmware version checking
* Firmware downloading
* Cryptographic signature verification
* Tampered firmware detection and rejection

The project was designed to explore the security risks associated with software updates and demonstrate a practical mitigation using public-key cryptography.

## Architecture

```text
              OTA SERVER
                  │
          ┌───────┴────────┐
          │                │
     firmware.txt     firmware.sig
          │                │
          └───────┬────────┘
                  │
                  ▼
              VEHICLE
                  │
          Check new version
                  │
                  ▼
       Download firmware +
           digital signature
                  │
                  ▼
       Verify with public key
                  │
            ┌─────┴─────┐
            │           │
          VALID       INVALID
            │           │
            ▼           ▼
        INSTALL       REJECT
```

## Security Model

The project uses an RSA public/private key pair.

### Private Key

`private_key.pem`

The private key represents the trusted OEM signing authority.

It is used to digitally sign legitimate firmware and must remain confidential.

### Public Key

`public_key.pem`

The public key is distributed to the vehicle and is used to verify that firmware was signed by the trusted authority.

The public key does not need to remain secret.

## OTA Update Process

The simulated vehicle performs the following steps:

1. Requests the latest firmware version from the server.
2. Determines whether an update is available.
3. Downloads the firmware and digital signature.
4. Loads the trusted public key.
5. Verifies the firmware signature.
6. Installs the firmware only if verification succeeds.
7. Rejects the update if signature verification fails.

## Security Testing

### Test 1 — Legitimate Firmware

The original firmware was:

```text
version=1.1
```

The firmware was signed using the private key.

The vehicle successfully verified the signature:

```text
[PASS] Firmware signature verified

[INSTALLING UPDATE]
[UPDATE COMPLETE]
```

### Test 2 — Firmware Tampering

The firmware was modified after signing:

```text
version=1.1
UNAUTHORIZED CHANGE
```

The original signature was intentionally left unchanged.

The vehicle detected the modification:

```text
[FAIL] Firmware signature verification failed
[UPDATE REJECTED]
```

This demonstrates that an attacker cannot modify the firmware without invalidating the existing digital signature.

## Security Finding

An initial version of this project used SHA-256 hash verification.

That implementation demonstrated an important limitation:

> Hash verification can detect changes to downloaded firmware, but it does not establish that the firmware originated from a trusted signing authority if an attacker can control the source and the expected hash.

For example, a compromised server could calculate a new hash for malicious firmware and provide both the modified firmware and matching hash to the vehicle.

The project was therefore upgraded to use digital signatures.

### SHA-256

Provides:

* Data integrity verification
* Detection of unexpected changes

### Digital Signatures

Provide:

* Integrity
* Authenticity
* Verification that firmware was signed by the trusted authority

This distinction was demonstrated experimentally rather than only theoretically.

## Technologies

* Python 3
* Flask
* Requests
* Cryptography
* RSA
* SHA-256
* Digital signatures
* REST APIs
* Git / GitHub

## Project Structure

```text
ota-security-lab/
│
├── server.py
├── vehicle.py
├── firmware.txt
├── firmware.sig
├── public_key.pem
├── requirements.txt
├── README.md
└── .gitignore
```

The private signing key is intentionally excluded from version control.

## Running the Lab

### 1. Clone the repository

```bash
git clone https://github.com/FellipyC/ota-security-lab.git
cd ota-security-lab
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the OTA server

```bash
python3 server.py
```

### 5. Run the vehicle client

In another terminal:

```bash
python3 vehicle.py
```

## Security Demonstration

The primary demonstration is:

```text
Legitimate firmware
        │
        ▼
Valid digital signature
        │
        ▼
UPDATE ACCEPTED
```

versus:

```text
Tampered firmware
        │
        ▼
Invalid digital signature
        │
        ▼
UPDATE REJECTED
```

## Future Improvements

Potential extensions include:

* Firmware version rollback protection
* Certificate-based trust chains
* Secure key management
* Anti-replay protections
* Mutual TLS between vehicle and server
* Firmware encryption
* ECU-specific authorization
* Threat modeling using automotive cybersecurity methodologies
* Alignment with ISO/SAE 21434 concepts
* Secure boot integration

## Disclaimer

This project is an educational simulation designed to demonstrate OTA security concepts. It does not represent a production automotive OTA implementation.
