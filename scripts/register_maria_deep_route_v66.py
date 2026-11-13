from __future__ import annotations
import json
from pathlib import Path
P=Path("translations/release_stack.json")
def main()->None:
 p=json.loads(P.read_text(encoding="utf-8"));b=list(p["profiles"]["maria-deep-route-v65"]["batches"]);b.append("translations/maria_deep_route_v66.json");p["profiles"]["maria-deep-route-v66"]={"status":"experimental","require_screen_entry_layout":True,"batches":b,"note":"Extends Maria V65 with all 29 records in SC3 block 61: Charles Jean Rochefort's complete recruitment."};P.write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(f"registered maria-deep-route-v66: {len(b)} batches")
if __name__=="__main__":main()
