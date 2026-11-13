import json
from pathlib import Path

P = Path("translations/release_stack.json")
payload = json.loads(P.read_text(encoding="utf-8"))
batches = list(payload["profiles"]["maria-deep-route-v90"]["batches"])
batches.append("translations/maria_deep_route_v91.json")
payload["profiles"]["maria-deep-route-v91"] = {
    "status": "experimental",
    "require_screen_entry_layout": True,
    "batches": batches,
    "note": "Extends Maria V90 with all 57 records in SC3 blocks 108-109: Kuen's defector and Argot deception, Maria's maritime mission, and the companion pledges.",
}
P.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered maria-deep-route-v91: {len(batches)} batches")
