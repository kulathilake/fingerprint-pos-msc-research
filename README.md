# Fingerprint-POS

A privacy-first, secure fingerprint-based point-of-sale payment research system developed for the Master of Science in Computer Science at the University of Colombo School of Computing.

## Overview

This repository contains a prototype research implementation of a biometric POS system that uses fingerprint templates and verification while prioritizing privacy and security.
The system also shards fingerprint data across multiple POS nodes, with each POS node acting as both a payment endpoint and a verification node.

Key goals:
- Preserve biometric privacy with template protection and cache-aware processing
- Support enrollment, verification, and automated evaluation
- Shard fingerprint data across POS nodes for decentralized storage and resilience
- Compare a secure POS-style flow with a centralized baseline system

## Project Structure

```text
fingerprint-pos/
├── docker-compose.yml
├── setup_dataset.sh          Downloads and extracts the fingerprint dataset
├── Dockerfile
├── pos-node/
│   └── app.py                POS node API
├── centralized/
│   └── centralized_app.py    Baseline centralized system
├── feature_extractor.py      Convert fingerprint images to fixed-length vectors
├── enroll_client.py          Enrollment client workflow
├── verify_client.py          Verification client workflow
├── evaluate.py               Automated metrics and attack evaluation
├── fvc2002/                  Fingerprint dataset (download separately)
├── templates_cache/          Cached templates for faster experiments
└── requirements.txt          Python dependencies
```

## Requirements

- Python 3.10+ (recommended)
- `pip` for installing dependencies
- `docker` and `docker-compose` if you want to run the containerized system

## Setup

1. Clone the repository.
2. Run `setup_dataset.sh` to download and extract the fingerprint dataset.
3. Install dependencies:
   ```bash
   chmod +x ./setup_py.sh
   ./setup_py.sh
   ```
4. Optional: run with Docker:
   ```bash
   docker compose up --build
   ```

## Usage

- Enroll fingerprints:
  ```bash
  python enroll_client.py
  ```
- Verify fingerprints:
  ```bash
  python verify_client.py
  ```
- Run evaluation and attack simulations:
  ```bash
  python evaluate.py
  ```

## Dataset

The `fvc2002/` directory should contain the downloaded fingerprint dataset files required for enrollment, verification, and evaluation.

## Notes

- `templates_cache/` is used to store extracted fingerprint templates so repeated experiments run faster.
- Fingerprint templates are sharded and stored across POS nodes, so each POS node also serves as a distributed storage node.
- This repository is intended as a research prototype and may require adaptation for deployment or additional experimentation.
