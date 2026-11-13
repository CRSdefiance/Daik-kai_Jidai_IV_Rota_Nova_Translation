from __future__ import annotations
import json
from pathlib import Path
STACK=Path('translations/release_stack.json')
def main()->None:
 payload=json.loads(STACK.read_text(encoding='utf-8'));profiles=payload['profiles'];batches=list(profiles['maria-deep-route-v57']['batches']);batches.append('translations/maria_deep_route_v58.json');profiles['maria-deep-route-v58']={'status':'experimental','require_screen_entry_layout':True,'batches':batches,'note':'Extends Maria V57 with 58 translated records and one preserved nontext control in SC3 blocks 51-53: Richard\'s defeat, the Hangzhou return, every Proof assembled, and the philosophical route epilogue.'};STACK.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'registered maria-deep-route-v58: {len(batches)} batches')
if __name__=='__main__':main()
