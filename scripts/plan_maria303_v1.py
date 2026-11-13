"""Reuse the full-width planner with303 exact source/current bindings and12 FE panels."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/plan_maria301_v1.py').read_text(encoding='utf-8'),{
    'work/Maria_B0_B32_clean_20261109':'work/Maria_B58_B70_clean_20261109',
    "doc['blocks']==list(range(15))+list(range(16,33))":"doc['blocks']==[58,59,60,61,62,64,65,66,68,70]",
    "len(bound)==len(original)==len(doc['records'])==301":"len(bound)==len(original)==len(doc['records'])==303",
    "        bindings.append(dict(id=row['id']":
    "        if raw[0]==254:assert row['kind']=='system-FE' and row['FE_is_not_an_ordinary_actor_nameplate']\n        bindings.append(dict(id=row['id']",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-full-width-parity-pagination-andcomplete-current-source-guards303','exec'),globals())
