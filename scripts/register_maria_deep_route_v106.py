import json
from pathlib import Path
P=Path("translations/release_stack.json");p=json.loads(P.read_text(encoding="utf-8"));b=list(p["profiles"]["maria-deep-route-v105"]["batches"]);b.append("translations/maria_deep_route_v106.json");p["profiles"]["maria-deep-route-v106"]={"status":"experimental","require_screen_entry_layout":True,"batches":b,"note":"Extends Maria V105 with 14 optional companion records in SC3 blocks 147-148."};P.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"registered maria-deep-route-v106: {len(b)} batches")
