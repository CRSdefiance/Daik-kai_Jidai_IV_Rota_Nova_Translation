"""Reuse the exact name-getter binding workflow for the 41 scoped selectors."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

parent=Path(__file__).with_name('bind_rafael_B181_B200_names_v1.py')
source=checked_text(parent.read_text(encoding='utf-8'),{
    'Rafael_B181_B200_current2165_20261106': 'Rafael_B201_B220_current2549_20261106',
    "PRIOR = [A / p for p in (": "PRIOR = [A / p for p in (\n    'Rafael_B181_B200_current2165_20261106/names_and_terms_v1.json',",
    'assert len(actors) == 29': 'assert len(actors) == 41',
})
if __name__ == '__main__':
    exec(compile(source,__file__+'::same-exact-scoped-getters-with-prior-reuse', 'exec'),globals())
