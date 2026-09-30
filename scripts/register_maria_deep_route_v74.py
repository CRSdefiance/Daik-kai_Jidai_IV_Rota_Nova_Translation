import json
from pathlib import Path
P=Path("translations/release_stack.json")
p=json.loads(P.read_text(encoding="utf-8"));b=list(p["profiles"]["maria-deep-route-v73"]["batches"]);b.append("translations/maria_deep_route_v74.json");p["profiles"]["maria-deep-route-v74"]={"status":"experimental","require_screen_entry_layout":True,"batches":b,"note":"Extends Maria V73 with all 20 records in SC3 block 74: Julio's concern for Christina and Shield of Minerva rumor."};P.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"registered maria-deep-route-v74: {len(b)} batches")
