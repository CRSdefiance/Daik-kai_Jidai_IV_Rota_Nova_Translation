import json
from pathlib import Path
P=Path("translations/release_stack.json");p=json.loads(P.read_text(encoding="utf-8"));b=list(p["profiles"]["maria-deep-route-v77"]["batches"]);b.append("translations/maria_deep_route_v78.json");p["profiles"]["maria-deep-route-v78"]={"status":"experimental","require_screen_entry_layout":True,"batches":b,"note":"Extends Maria V77 with all 10 records in SC3 block 78: Emilio's Hestia's Cauldron rumor."};P.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"registered maria-deep-route-v78: {len(b)} batches")
