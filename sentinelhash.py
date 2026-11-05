#!/usr/bin/env python3
import csv
import hashlib
from pathlib import Path
from datetime import datetime, timezone

HOME = Path.home()
LAB = HOME / "FIM-Lab"
BASELINE = HOME / "baseline.csv"
REPORT = HOME / "change_report.csv"

def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()

def scan_files():
    return {
        str(path): sha256_file(path)
        for path in sorted(LAB.rglob("*"))
        if path.is_file()
    }

def load_baseline():
    with BASELINE.open(newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != ["path", "sha256"]:
            raise ValueError("Invalid baseline CSV format")
        return {
            row["path"]: row["sha256"]
            for row in reader
        }

def main():
    baseline = load_baseline()
    current = scan_files()
    timestamp = datetime.now(timezone.utc).isoformat()
    changes = []

    for path in sorted(set(baseline) | set(current)):
        if path not in baseline:
            status = "ADDED"
        elif path not in current:
            status = "DELETED"
        elif baseline[path] != current[path]:
            status = "MODIFIED"
        else:
            continue

        changes.append({
            "timestamp": timestamp,
            "status": status,
            "path": path,
            "baseline_sha256": baseline.get(path, ""),
            "current_sha256": current.get(path, "")
        })

    with REPORT.open("w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "timestamp", "status", "path",
                "baseline_sha256", "current_sha256"
            ]
        )
        writer.writeheader()
        writer.writerows(changes)

    print("=== SentinelHash File Integrity Monitor ===")
    print(f"Monitored directory: {LAB}")
    print(f"Baseline files: {len(baseline)}")
    print(f"Current files: {len(current)}")
    print(f"Changes detected: {len(changes)}")

    for change in changes:
        print(f"[{change['status']}] {change['path']}")

    print(f"CSV report saved: {REPORT}")

if __name__ == "__main__":
    main()
