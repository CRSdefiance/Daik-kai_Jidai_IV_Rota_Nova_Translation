"""Fresh target references;reuse parent evidence only by complete V7168 ROM identity."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B225_reference_tools_v7200')
if __name__=='__main__':
    assert not ROOT.exists()
    loader={'B224':'B225','reference_v7150':'reference_v7199','loader_v7151':'loader_v7200','B223_loader_v7103/whole_SC2_and_B223_initial_entry_proof':'B224_loader_v7151/whole_SC2_and_B224_initial_entry_proof','V7118':'V7168','B2241040_bytes_fit_original_0x2400_cache':'B2251076_bytes_fit_original_0x2400_cache'}
    census={'B224':'B225','reference_v7150':'reference_v7199','reference_census_v7152':'reference_census_v7201','loader_v7151':'loader_v7200','B223_reference_census_v7104/all22_commands4_relative_sites_typed_alias_predicate_staging_and_shipped_census':'B224_reference_census_v7152/all18_commands_no_relative_or_typed_sites_and_shipped_census','[224]':'[225]','block=224':'block=225','len(w)==18':'len(w)==16',"len(spec['text_records'])==15":"len(spec['text_records'])==13",'all18_commands_no_relative_or_typed_sites':'all16_commands_no_relative_or_typed_sites','all18_clean_current_target_commands':'all16_clean_current_target_commands','all18 mapped commands':'all16 mapped commands','All18 commands':'All16 commands','A000/C200/normal end':'630B/A000/normal end'}
    jobs=[('scripts/verify_lil_B224_loader_v7151.py','scripts/verify_lil_B225_loader_v7200.py',loader),('scripts/verify_lil_B224_references_v7152.py','scripts/verify_lil_B225_references_v7201.py',census)]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_loader_and_reference_census.json',dict(tools=rows,whole_V7168_hash_must_equal_prior_B224_reference_before_parent_reuse=True,fresh336_target_loads672_modes_caller_census_and16_command_walk_required=True,only_B225_script_body_changes_native_high_constants_andall_older_artifacts_preserved=True,new_credit=0,full_goal_complete=False))
