from __future__ import annotations
import json
from pathlib import Path
STACK=Path('translations/release_stack.json')
def main()->None:
 payload=json.loads(STACK.read_text(encoding='utf-8'));profiles=payload['profiles'];batches=list(profiles['maria-deep-route-v58']['batches']);batches.append('translations/maria_deep_route_v59.json');profiles['maria-deep-route-v59']={'status':'experimental','require_screen_entry_layout':True,'batches':batches,'note':'Extends Maria V58 with 75 translated records and one preserved nontext control in SC3 block 54: the complete alternate ending, public Ming fleet review, companion comedy, and historical narration.'};STACK.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'registered maria-deep-route-v59: {len(batches)} batches')
if __name__=='__main__':main()
