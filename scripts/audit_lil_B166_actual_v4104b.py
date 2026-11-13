"""Scope the resource assertion to B166, preserving B22's original 633D initialization."""
from pathlib import Path
if __name__ == '__main__':
    draft = Path('scripts/audit_lil_B166_actual_v4104.py')
    text = draft.read_text(encoding='utf-8')
    old = "[p['word'] for p in selected if p['word'] & 0xFF00 == 0x6300] == [0x632B,0x632C]"
    new = "[p['word'] for p in selected if p.get('original_source_block') == 166 and p['word'] & 0xFF00 == 0x6300] == [0x632B,0x632C]"
    assert text.count(old) == 1
    text = text.replace(old, new)
    old = "evidence=evidence, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False"
    new = "evidence={**evidence,str(DRAFT):sha(DRAFT.read_bytes())}, preserved_failed_resource_assertion_included_B22_633D_init=True, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False"
    assert text.count(old) == 1
    text = text.replace(old, new)
    exec(compile(text, __file__, 'exec'), dict(__name__='__main__', __file__=__file__, DRAFT=draft))
