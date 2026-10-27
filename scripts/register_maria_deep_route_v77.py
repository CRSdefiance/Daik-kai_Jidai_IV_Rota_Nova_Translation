import json
from pathlib import Path
P=Path("translations/release_stack.json");p=json.loads(P.read_text(encoding="utf-8"));b=list(p["profiles"]["maria-deep-route-v76"]["batches"]);b.append("translations/maria_deep_route_v77.json");p["profiles"]["maria-deep-route-v77"]={"status":"experimental","require_screen_entry_layout":True,"batches":b,"note":"Extends Maria V76 with all 11 records in SC3 block 77: the Telescope of Aristarchus rumor."};P.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"registered maria-deep-route-v77: {len(b)} batches")
