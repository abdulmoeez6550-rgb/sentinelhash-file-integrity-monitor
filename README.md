cat > README.md <<'EOF'
# SentinelHash — File Integrity Monitor

A Python-based cybersecurity lab that uses SHA-256 hashing to detect file integrity changes.

## Project Objective

Detect added, modified, and deleted files by comparing the current file state against a trusted baseline.

## Lab Environment

- Ubuntu 26.04.1 LTS (WSL)
- Python 3.14.4
- SHA-256 hashing
- CSV baseline and change reports

## How It Works

1. Create a baseline containing file paths and SHA-256 hashes.
2. Scan the monitored directory.
3. Compare current files against the original baseline.
4. Classify differences as ADDED, MODIFIED, or DELETED.
5. Export the findings to a CSV report.

## Test Results

| Test | File | Result |
|------|------|--------|
| Modified | critical.txt | PASS |
| Added | new.txt | PASS |
| Deleted | readme.txt | PASS |

All three simulated file changes were successfully detected.

## Running the Monitor

The script expects:

- A directory at ~/FIM-Lab
- A baseline at ~/baseline.csv

Run:

python3 sentinelhash.py

Note: The script uses paths relative to the user's home directory. The provided CSV files are evidence from the completed lab.

## Limitations

This is an educational prototype, not a production security agent.

It does not provide real-time monitoring, prevent unauthorized changes, or protect the baseline against tampering.

## Security Improvement

Store the trusted baseline in a protected location with restricted write access and forward alerts to centralized monitoring.

## Evidence

The screenshots folder contains terminal evidence of the baseline, clean scan, and three change-detection tests.

## Ethical Use

All tests were performed on local sample files in an authorized lab environment.
EOF
