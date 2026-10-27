import json
from pathlib import Path
P=Path("translations/release_stack.json")
p=json.loads(P.read_text(encoding="utf-8"));b=list(p["profiles"]["maria-deep-route-v75"]["batches"]);b.append("translations/maria_deep_route_v76.json");p["profiles"]["maria-deep-route-v76"]={"status":"experimental","require_screen_entry_layout":True,"batches":b,"note":"Extends Maria V75 with all 15 records in SC3 block 76: Samwell's Vest of the Jaguar God rumor."};P.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"registered maria-deep-route-v76: {len(b)} batches")
