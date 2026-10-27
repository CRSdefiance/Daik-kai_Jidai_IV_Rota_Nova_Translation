"""Read bounded complete-conversation portions, without changing source evidence."""
import json
import sys
from pathlib import Path

if __name__ == '__main__':
    d=json.loads(Path('work/analysis/lil_London_source_v1879b/all111_clean_current_native_source_context.json').read_text(encoding='utf-8'))
    start=int(sys.argv[1]) if len(sys.argv)>1 else 0
    end=int(sys.argv[2]) if len(sys.argv)>2 else 56
    for i,r in enumerate(d['records'][start:end],start):
        print(json.dumps(dict(index=i,id=r['id'],speaker=r['speaker'],prefix=r['source_presentation_prefix_hex'],
            Japanese=r['source_Japanese'],current_English=r['current_native_macro_English'],ancestors=r['ancestor_0100_offsets']),ensure_ascii=False))
    if start==0:
        print('EVENT',json.dumps(d['source_event26'],ensure_ascii=False))
        print('CONTEXT',json.dumps(d['offline_original_London_context'],ensure_ascii=False))
