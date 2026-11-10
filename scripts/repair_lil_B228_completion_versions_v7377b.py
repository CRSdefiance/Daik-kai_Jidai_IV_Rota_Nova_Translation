"""Preserve rejected preparation; omit only absent version-only substitutions before deriving."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B228_completion_repair_v7377b')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('scripts/complete_lil_B228_v7377.py').exists()
    old="    rows=[derive('scripts/complete_lil_B227_v7330b.py','scripts/complete_lil_B228_v7377.py',changes)]"
    new="    changes={k:v for k,v in changes.items() if not(k.startswith('v') and k[1:].isdigit() and k not in src)}\n"+old
    r=derive('scripts/prepare_lil_B228_completion_v7377.py','scripts/prepare_lil_B228_completion_v7377b.py',{old:new,'completion_tools_v7377':'completion_tools_v7377b'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_completion_preflight_repair.json',dict(tool=r,original_preparation_failed_before_output_orledger_mutation=True,only_unused_version_substitution_keys_omitted=True,all_semantic_replacement_keys_andnative_number_guards_still_required=True,full_goal_complete=False))
