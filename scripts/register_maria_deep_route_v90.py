import json
from pathlib import Path

P = Path("translations/release_stack.json")
payload = json.loads(P.read_text(encoding="utf-8"))
batches = list(payload["profiles"]["maria-deep-route-v89"]["batches"])
batches.append("translations/maria_deep_route_v90.json")
payload["profiles"]["maria-deep-route-v90"] = {
    "status": "experimental",
    "require_screen_entry_layout": True,
    "batches": batches,
    "note": "Extends Maria V89 with all 48 records in SC3 blocks 104-107: Ceuta deadline, Mao encounter, public-fear confession, Ming recognition, and East Asian Proof-map discovery.",
}
P.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"registered maria-deep-route-v90: {len(batches)} batches")
