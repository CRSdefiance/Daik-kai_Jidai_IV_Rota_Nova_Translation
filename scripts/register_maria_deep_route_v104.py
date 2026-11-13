import json
from pathlib import Path
P=Path("translations/release_stack.json");p=json.loads(P.read_text(encoding="utf-8"));b=list(p["profiles"]["maria-deep-route-v103"]["batches"]);b.append("translations/maria_deep_route_v104.json");p["profiles"]["maria-deep-route-v104"]={"status":"experimental","require_screen_entry_layout":True,"batches":b,"note":"Extends Maria V103 with 34 translations and one preserved control in SC3 block 140: Yifa's recruitment."};P.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"registered maria-deep-route-v104: {len(b)} batches")
