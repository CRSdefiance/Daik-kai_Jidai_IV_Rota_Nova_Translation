import json
from pathlib import Path

P = Path("translations/release_stack.json")
payload = json.loads(P.read_text(encoding="utf-8"))
batches = list(payload["profiles"]["maria-deep-route-v91"]["batches"])
batches.append("translations/maria_deep_route_v92.json")
payload["profiles"]["maria-deep-route-v92"] = {
    "status": "experimental",
    "require_screen_entry_layout": True,
    "batches": batches,
    "note": "Extends Maria V91 with 34 translations and one preserved control in SC3 blocks 110-112: frightened townsman, Guam castaway, and Southeast Asian Proof-map reveal.",
}
P.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered maria-deep-route-v92: {len(batches)} batches")
