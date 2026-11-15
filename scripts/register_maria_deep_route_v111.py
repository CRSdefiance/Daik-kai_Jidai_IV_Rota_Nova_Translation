import json
from pathlib import Path
P=Path("translations/release_stack.json");p=json.loads(P.read_text(encoding="utf-8"));b=list(p["profiles"]["maria-deep-route-v110"]["batches"]);b.append("translations/maria_deep_route_v111.json");p["profiles"]["maria-deep-route-v111"]={"status":"experimental","require_screen_entry_layout":True,"batches":b,"note":"Extends Maria V110 with the final 87 untranslated SC3 records across blocks 223-239."};P.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"registered maria-deep-route-v111: {len(b)} batches")
