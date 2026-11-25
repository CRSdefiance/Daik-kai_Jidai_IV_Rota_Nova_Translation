"""Bind current source-qualified names and default macros for the new scoped prose."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/bind_maria286_names_macros_v1.py').read_text(encoding='utf-8'),{
    'work/Maria_B37_B50_clean_20261109':'work/Maria_B125_B136_clean_20261109',
    'all286_clean_meanings_andindependent_drafts_v2.json':'all337_contextual_proposals_v1.json',
    "expected={'ハイレディン','バルデス','パシャ','クーン','エスカンテ'}":"expected={'エスカンテ'}",
    'assert len(spoken)==5 and expected==':'assert len(spoken)==1 and expected==',
    'same-original-name-getters-scoped-Maria286':'same-original-name-getters-scoped-Maria337',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-scoped-original-getters-anddefault-macro-ABI','exec'),globals())
