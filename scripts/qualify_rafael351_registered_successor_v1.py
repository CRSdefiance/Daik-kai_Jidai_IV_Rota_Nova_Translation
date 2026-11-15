"""Qualify the351 shared transaction, style aliases and honest actual/offline scope."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/qualify_plain_SC0_registered_successor_v1.py').read_text(encoding='utf-8'), {
    "('changed-logical-prose','manuscript'),('wrong-control-only-membership',None)":
        "('changed-logical-prose','manuscript'),('changed-style-alias','manuscript'),('stored-virtual-style-prefix','manuscript'),('wrong-control-only-membership',None)",
    "set(config['blocks'])|{89}": "set(config['blocks'])|{130}",
    "doc['offline_only_source_speeches'] = 0": "doc['offline_only_speech_variants'] = 0",
    "            elif kind == 'changed-logical-prose':":
        """            elif kind == 'changed-style-alias':
                row=next(r for r in doc['records'] if len(r.get('source_style_indices',[]))>1)
                row['source_style_indices']=row['source_style_indices'][:1]
            elif kind == 'stored-virtual-style-prefix':
                next(r for r in doc['records'] if r.get('native_object_kind')=='4100-style-alternative')['planned_integrated_reference']['virtual_prefix_not_stored']=False
            elif kind == 'changed-logical-prose':""",
    'assert len(rejections) == 8': 'assert len(rejections) == 10',
    'One shared source-bound transaction/eight semantic andordering rejections pass;all eight final stage contracts exact. Build next.':
        '351 shared source-bound transaction/ten semantic andordering rejections pass;all eight final stage contracts exact. Build next.',
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-pure-transaction-with-style-andactual-scope-negatives', 'exec'), globals())
