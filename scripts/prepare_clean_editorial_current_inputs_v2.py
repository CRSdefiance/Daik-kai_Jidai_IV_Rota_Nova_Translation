"""Preserve complete credited context while projecting sealed, uncredited drafts."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/prepare_clean_editorial_current_inputs_v1.py').read_text(encoding='utf-8'), {
    "    for g in groups.values():g['clean_block_sha256']=sha(bytes.fromhex(g['clean_block_hex']))":
    """    for g in groups.values():
        g['clean_block_sha256']=sha(bytes.fromhex(g['clean_block_hex']))
        g.setdefault('complete_clean_context_records',deepcopy(g['records']))
        whole=g['complete_clean_context_records']
        assert {r['id'] for r in g['records']} <= {r['id'] for r in whole}
        assert [r['id'] for r in whole if not r['covered']]==[r['id'] for r in g['records']]
        assert all(r['exact_credited_source_bindings'] for r in whole if r['covered'])""",
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-sealed-draft-guards-complete-context-preserved', 'exec'), globals())
