"""Use the manuscript's exact full-scope field; preserve the rejected v1 compiler."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B223_atomic_field_tools_v7115b')
if __name__=='__main__':
    assert not ROOT.exists()
    jobs=[('dk4tool/patch/lil_B223_editorial_v1.py','dk4tool/patch/lil_B223_editorial_v2.py',{'all207_name_alias_review_and_full_four_storyline_editorial_objective_open':'all207_name_alias_and_full_four_storyline_editorial_objective_open'}),
      ('scripts/validate_lil_B223_atomic_v7115.py','scripts/validate_lil_B223_atomic_v7115b.py',{'lil_B223_editorial_v1 as owned':'lil_B223_editorial_v2 as owned',"ROOT=Path('work/analysis/lil_B223_atomic_v7115')":"ROOT=Path('work/analysis/lil_B223_atomic_v7115b')","    deps.update(doc[k[:-7]]":"    deps.add('work/analysis/lil_B223_atomic_field_tools_v7115b/source_locked_schema_correction.json')\n    deps.update(doc[k[:-7]]"})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_schema_correction.json',dict(tools=rows,failed_v1_and_positive_config_preserved=True,no_native_address_or_evidence_requirement_change=True,source_and_prose_unchanged=True,new_credit=0,full_goal_complete=False))
