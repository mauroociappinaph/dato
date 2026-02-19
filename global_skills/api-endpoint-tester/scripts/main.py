#!/usr/bin/env python3
"""
API Endpoint Tester (v1.0)
REAL - Performs smoke tests and latency audits.
"""

import os
import sys
import time
import requests
import json

def test_endpoint(url, expected_status=200, schema_keys=None):
    print(f"🚀 API Tester: Auditando endpoint -> {url}")
    
    start_time = time.time()
    try:
        response = requests.get(url, timeout=10)
        latency = (time.time() - start_time) * 1000 # in ms
        
        status_ok = response.status_code == expected_status
        latency_ok = latency < 500
        
        results = {
            "url": url,
            "status_code": response.status_code,
            "status_ok": status_ok,
            "latency_ms": round(latency, 2),
            "latency_ok": latency_ok,
            "content_type": response.headers.get('Content-Type', 'unknown')
        }

        # Protocol 2: Schema Check
        if status_ok and "application/json" in results["content_type"]:
            try:
                data = response.json()
                if schema_keys:
                    missing = [k for k in schema_keys if k not in data]
                    results["schema_check"] = "PASS" if not missing else f"FAIL (Missing: {missing})"
                else:
                    results["schema_check"] = "PASS (Basic JSON verified)"
            except Exception:
                results["schema_check"] = "FAIL (Invalid JSON)"
        
        return results

    except Exception as e:
        return {"url": url, "error": str(e), "status_ok": False}

if __name__ == "__main__":
    # Test our own dynamic Command Center health endpoint
    target_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000/api/health"
    
    # Expected keys for the Command Center health check
    keys = ["status", "version", "engine"]
    
    report = test_endpoint(target_url, schema_keys=keys)
    
    print("\n--- 🛡️ API SMOKE TEST REPORT ---")
    print(json.dumps(report, indent=2))
    
    if not report.get("status_ok") or not report.get("latency_ok"):
        print("\n🔴 ALERTA: Endpoint degradado o caído.")
        sys.exit(1)
    else:
        print("\n🟢 SUCCESS: Endpoint certificado.")
