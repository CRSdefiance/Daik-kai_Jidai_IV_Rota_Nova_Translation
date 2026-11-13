import json
from pathlib import Path

P = Path("translations/release_stack.json")
payload = json.loads(P.read_text(encoding="utf-8"))
batches = list(payload["profiles"]["maria-deep-route-v88"]["batches"])
batches.append("translations/maria_deep_route_v89.json")
payload["profiles"]["maria-deep-route-v89"] = {
    "status": "experimental",
    "require_screen_entry_layout": True,
    "batches": batches,
    "note": "Extends Maria V88 with all eight companion-specific shark warnings in SC3 block 103.",
}
P.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered maria-deep-route-v89: {len(batches)} batches")
