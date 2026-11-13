"""Preserve the failed preflight and remove a template key that no longer exists."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B226_relocation_repair_v7257b')
if __name__=='__main__':
    assert not ROOT.exists() and not any(Path(p).exists() for p in ['scripts/research_lil_B226_relocation_v7257.py','scripts/prove_lil_B226_stored_v7258.py','scripts/create_lil_B226_reference_v7259.py','work/analysis/lil_B226_relocation_tools_v7257'])
    r=derive('scripts/prepare_lil_B226_relocation_v7257.py','scripts/prepare_lil_B226_relocation_v7257b.py',{"'source_v7178/thirteen_clean_current_children_heroes_exchange_source_references':'source_v7240/twenty_clean_current_Attila_armor_exchange_source_references',":'',"lil_B226_relocation_tools_v7257'":"lil_B226_relocation_tools_v7257b'"})
    ROOT.mkdir(parents=True);save(ROOT/'preserved_preflight_failure_andrepair.json',dict(derivation=r,failed_producer='scripts/prepare_lil_B226_relocation_v7257.py',error='Derivation key absent:source_v7178/thirteen_clean_current_children_heroes_exchange_source_references',stopped_before_any_planned_tool_ROM_orproof_write=True,source_context_is_read_from_manuscript_not_hardcoded_in_template=True,new_credit=0,full_goal_complete=False))
