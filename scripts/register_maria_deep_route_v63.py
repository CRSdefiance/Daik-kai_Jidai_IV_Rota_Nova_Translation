from __future__ import annotations
import json
from pathlib import Path
STACK=Path("translations/release_stack.json")
def main()->None:
 payload=json.loads(STACK.read_text(encoding="utf-8"));profiles=payload["profiles"];batches=list(profiles["maria-deep-route-v62"]["batches"]);batches.append("translations/maria_deep_route_v63.json");profiles["maria-deep-route-v63"]={"status":"experimental","require_screen_entry_layout":True,"batches":batches,"note":"Extends Maria V62 with 84 translated records and one preserved nontext control in SC3 block 58: the complete London harbor rescue and Cristina-Mivor follow-up."};STACK.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"registered maria-deep-route-v63: {len(batches)} batches")
if __name__=="__main__":main()
