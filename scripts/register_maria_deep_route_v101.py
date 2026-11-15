import json
from pathlib import Path
P=Path("translations/release_stack.json");p=json.loads(P.read_text(encoding="utf-8"));b=list(p["profiles"]["maria-deep-route-v100"]["batches"]);b.append("translations/maria_deep_route_v101.json");p["profiles"]["maria-deep-route-v101"]={"status":"experimental","require_screen_entry_layout":True,"batches":b,"note":"Extends Maria V100 with all 31 records in SC3 block 138: Manuel's recruitment and ship-room tutorial."};P.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"registered maria-deep-route-v101: {len(b)} batches")
