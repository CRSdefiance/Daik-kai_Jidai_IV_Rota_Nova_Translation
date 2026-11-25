from __future__ import annotations
import json
from pathlib import Path
STACK=Path("translations/release_stack.json")
def main()->None:
 p=json.loads(STACK.read_text(encoding="utf-8"));b=list(p["profiles"]["maria-deep-route-v63"]["batches"]);b.append("translations/maria_deep_route_v64.json");p["profiles"]["maria-deep-route-v64"]={"status":"experimental","require_screen_entry_layout":True,"batches":b,"note":"Extends Maria V63 with all 26 records in SC3 block 59: Gerhard Adernkatz's complete recruitment."};STACK.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"registered maria-deep-route-v64: {len(b)} batches")
if __name__=="__main__":main()
