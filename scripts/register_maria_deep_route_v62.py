from __future__ import annotations
import json
from pathlib import Path
STACK=Path("translations/release_stack.json")
def main()->None:
 payload=json.loads(STACK.read_text(encoding="utf-8"));profiles=payload["profiles"];batches=list(profiles["maria-deep-route-v61"]["batches"]);batches.append("translations/maria_deep_route_v62.json");profiles["maria-deep-route-v62"]={"status":"experimental","require_screen_entry_layout":True,"batches":batches,"note":"Extends Maria V61 with all 55 records in SC3 block 57: Cristina and Mivor's complete London recruitment event."};STACK.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"registered maria-deep-route-v62: {len(batches)} batches")
if __name__=="__main__":main()
