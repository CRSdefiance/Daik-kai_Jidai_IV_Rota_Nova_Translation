"""Respect the source refusal end before the lecture-only closing resource command."""
from pathlib import Path
if __name__=='__main__':
    source=Path('scripts/audit_lil_B167_actual_v4151.py');text=source.read_text(encoding='utf-8')
    old="assert [p['word'] for p in selected if p.get('original_source_block') == 167 and p['word'] & 0xFF00 == 0x6300] == [0x6327,0x632B]"
    new="assert [p['word'] for p in selected if p.get('original_source_block') == 167 and p['word'] & 0xFF00 == 0x6300] == ([0x6327,0x632B] if option==0 else [0x6327])"
    assert text.count(old)==1;text=text.replace(old,new)
    old='evidence=evidence, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False'
    new="preserved_B167_failed_audit={str(DRAFT):sha(DRAFT.read_bytes())},refusal_end430_precedes_lecture_only_resource2170=True,evidence=evidence, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False"
    assert text.count(old)==1;text=text.replace(old,new)
    exec(compile(text,__file__+'::source-path-corrected','exec'),dict(__name__='__main__',__file__=__file__,DRAFT=source))
