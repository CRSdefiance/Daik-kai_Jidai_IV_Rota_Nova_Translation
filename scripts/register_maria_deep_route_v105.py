import json
from pathlib import Path
P=Path("translations/release_stack.json");p=json.loads(P.read_text(encoding="utf-8"));b=list(p["profiles"]["maria-deep-route-v104"]["batches"]);b.append("translations/maria_deep_route_v105.json");p["profiles"]["maria-deep-route-v105"]={"status":"experimental","require_screen_entry_layout":True,"batches":b,"note":"Extends Maria V104 with all 16 records in SC3 block 143: the Golden Crown of Silla tavern lead."};P.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"registered maria-deep-route-v105: {len(b)} batches")
