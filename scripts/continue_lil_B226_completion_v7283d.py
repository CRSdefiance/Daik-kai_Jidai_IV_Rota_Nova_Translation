"""Bind the newly completed source-only B227 gloss without granting new credit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B226_completion_nextsource_v7283d')
if __name__=='__main__':
    assert not ROOT.exists()
    r=derive('scripts/complete_lil_B226_v7283c.py','scripts/complete_lil_B226_v7283d.py',{
        "    paths.append(Path(doc['source_context']))":"    paths.append(Path(doc['source_context']))\n    nextsource=Path('work/analysis/lil_B227_clean_context_v7286/nine_clean_sword_practice_cloth_rumor_glosses_before_old_English.json');assert read(nextsource)['all9_clean_glosses_precede_old_English'] and read(nextsource)['prior_English_unread'];paths.append(nextsource)",
        "    inventory['later_B225_metadata_technical_reaudit_v7283']":"    inventory['next_Lil_B227_source_only_gloss_complete']=dict(source_context=str(nextsource),source_context_sha256=sha(nextsource.read_bytes()),clean_speeches=9,all9_clean_glosses_precede_old_English=True,cloth_rumor_conditional_wish_andteacher_quote_not_item_orfamily_facts=True,three_original_A000_consumers_names_voices_conditions_current_prose_native_actual_andrelease_pending=True,new_credit=0)\n    inventory['later_B225_metadata_technical_reaudit_v7283']"})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_next_source_binding.json',r)
