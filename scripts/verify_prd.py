#!/usr/bin/env python3
"""PRD acceptance checklist verifier for Smart Data Cleaning API."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

CHECKS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    CHECKS.append((name, ok, detail))


def path_exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def main() -> int:
    # Structure
    required_paths = [
        "app/main.py",
        "app/api/datasets.py",
        "app/api/analysis.py",
        "app/core/config.py",
        "app/core/exceptions.py",
        "app/core/logging.py",
        "app/database/database.py",
        "app/database/models.py",
        "app/schemas/dataset.py",
        "app/schemas/cleaning.py",
        "app/schemas/profile.py",
        "app/schemas/quality.py",
        "app/schemas/analysis.py",
        "app/services/file_handler.py",
        "app/services/profiler.py",
        "app/services/cleaner.py",
        "app/services/validator.py",
        "app/services/analyzer.py",
        "app/services/quality.py",
        "app/services/dataset_service.py",
        "tests/test_upload.py",
        "tests/test_validation.py",
        "tests/test_profiling.py",
        "tests/test_cleaning.py",
        "tests/test_quality.py",
        "tests/test_analysis.py",
        "tests/test_download.py",
        "tests/test_database.py",
        "sample_data/customers_dirty.csv",
        "Dockerfile",
        "docker-compose.yml",
        "pyproject.toml",
        ".env.example",
        ".gitignore",
        "README.md",
        "README.fa.md",
        "LICENSE",
        "screenshots/swagger-overview.png",
        "screenshots/upload.png",
        "screenshots/profile.png",
        "screenshots/cleaning.png",
        "screenshots/quality.png",
        "screenshots/analysis.png",
    ]
    for rel in required_paths:
        check(f"path:{rel}", path_exists(rel), "missing" if not path_exists(rel) else "ok")

    # Endpoints in source
    datasets_src = (ROOT / "app/api/datasets.py").read_text(encoding="utf-8")
    for route in [
        '/upload"',
        '""',
        "/{dataset_id}",
        "/profile",
        "/clean",
        "/quality",
        "/analysis",
        "/download",
    ]:
        # loose presence checks handled below
        pass

    endpoint_markers = [
        ("POST upload", '@router.post(\n    "/upload"'),
        ("GET list", '@router.get(\n    ""'),
        ("GET detail", '@router.get(\n    "/{dataset_id}"'),
        ("GET profile", "/profile"),
        ("POST clean", "/clean"),
        ("GET quality", "/quality"),
        ("GET analysis", "/analysis"),
        ("GET download", "/download"),
        ("DELETE dataset", "@router.delete"),
    ]
    for name, marker in endpoint_markers:
        check(f"endpoint:{name}", marker in datasets_src, "missing marker")

    # README sections
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for section in [
        "Project Overview",
        "Problem Statement",
        "Features",
        "Architecture",
        "Project Structure",
        "Technologies",
        "Installation",
        "Running Locally",
        "Running with Docker",
        "API Documentation",
        "API Endpoints",
        "Example Workflow",
        "Data Cleaning Strategy",
        "Data Quality Score",
        "Sample Dataset",
        "Testing",
        "Screenshots",
        "Error Handling",
        "Future Improvements",
        "License",
    ]:
        check(f"readme:{section}", section in readme)

    # Runtime tests via pytest collection count
    import subprocess

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--collect-only"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    collected = 0
    for line in result.stdout.splitlines():
        if "test session starts" in line:
            continue
        if line.strip().endswith("tests collected"):
            # e.g. "42 tests collected in 0.12s"
            parts = line.strip().split()
            if parts and parts[0].isdigit():
                collected = int(parts[0])
    if collected == 0:
        # fallback parse "======= 42 tests collected"
        import re

        m = re.search(r"(\d+) tests? collected", result.stdout)
        collected = int(m.group(1)) if m else 0
    check("tests:at_least_20", collected >= 20, f"collected={collected}")

    run = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    check("tests:all_pass", run.returncode == 0, run.stdout.strip().splitlines()[-1] if run.stdout else run.stderr[-200:])

    # Live API if available
    try:
        import httpx

        health = httpx.get("http://127.0.0.1:8000/health", timeout=2.0)
        check("live:health", health.status_code == 200 and health.json().get("status") == "healthy")
        if health.status_code == 200:
            sample = ROOT / "sample_data/customers_dirty.csv"
            with sample.open("rb") as fh:
                upload = httpx.post(
                    "http://127.0.0.1:8000/datasets/upload",
                    files={"file": ("customers_dirty.csv", fh, "text/csv")},
                    timeout=30.0,
                )
            check("live:upload", upload.status_code == 201, upload.text[:200])
            if upload.status_code == 201:
                dataset_id = upload.json()["dataset_id"]
                profile = httpx.get(f"http://127.0.0.1:8000/datasets/{dataset_id}/profile", timeout=30.0)
                check("live:profile", profile.status_code == 200)
                clean = httpx.post(
                    f"http://127.0.0.1:8000/datasets/{dataset_id}/clean",
                    json={},
                    timeout=60.0,
                )
                check("live:clean", clean.status_code == 200 and clean.json().get("status") == "CLEANED", clean.text[:200])
                quality = httpx.get(f"http://127.0.0.1:8000/datasets/{dataset_id}/quality", timeout=30.0)
                ok_quality = quality.status_code == 200 and 0 <= quality.json().get("quality_score", -1) <= 100
                check("live:quality", ok_quality, quality.text[:200])
                analysis = httpx.get(f"http://127.0.0.1:8000/datasets/{dataset_id}/analysis", timeout=30.0)
                check("live:analysis", analysis.status_code == 200)
                download = httpx.get(f"http://127.0.0.1:8000/datasets/{dataset_id}/download", timeout=30.0)
                check("live:download", download.status_code == 200 and "text/csv" in download.headers.get("content-type", ""))
    except Exception as exc:  # noqa: BLE001
        check("live:api", False, f"unavailable: {exc}")

    passed = sum(1 for _, ok, _ in CHECKS if ok)
    failed = [c for c in CHECKS if not c[1]]
    report = {
        "passed": passed,
        "failed": len(failed),
        "total": len(CHECKS),
        "failures": [{"name": n, "detail": d} for n, ok, d in failed],
    }
    print(json.dumps(report, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
