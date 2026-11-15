"""Fresh resized-archive checks reuse immutable parent proofs only by complete ROM hashes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B226_reference_tools_v7260')
if __name__=='__main__':
    assert not ROOT.exists()
    loader={'B225':'B226','reference_v7215':'reference_v7259','loader_v7216':'loader_v7260','lil_B224_loader_v7151/whole_SC2_and_B224_initial_entry_proof':'lil_B225_loader_v7216/whole_SC2_and_B225_initial_entry_proof','V7168':'V7230','B2251072_bytes_fit':'B2261176_bytes_fit'}
    census={'B225':'B226','reference_v7215':'reference_v7259','reference_census_v7217':'reference_census_v7261','loader_v7216':'loader_v7260','lil_B224_reference_census_v7152/all18_commands_no_relative_or_typed_sites_and_shipped_census':'lil_B225_reference_census_v7217/all16_commands_no_relative_or_typed_sites_and_shipped_census','[225]':'[226]','block=225':'block=226','len(w)==16':'len(w)==22',"len(spec['text_records'])==13":"len(spec['text_records'])==20",'all16_commands':'all22_commands','all16_clean_current_target':'all22_clean_current_target','all16 mapped':'all22 mapped','All16 commands/no relatives or typed controls/630B/A000/normal end':'All22 commands/no relatives or typed controls/A000/normal end'}
    jobs=[('scripts/verify_lil_B225_loader_v7216.py','scripts/verify_lil_B226_loader_v7260.py',loader),('scripts/verify_lil_B225_references_v7217.py','scripts/verify_lil_B226_references_v7261.py',census)]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_resized_archive_andcaller_checks.json',dict(tools=rows,source1196_logical1194_tail2_target1176_no_tail_bound=True,all22_mapped_commands20_preambles_A000_full_end_required=True,parent_V7230_equals_prior_B225_research_by_whole_ROM_hash_not_version_name=True,one_fresh_target_census336_fresh_loads672_fresh_parent_modes=True,strict_all_native_high_constants_andearlier_artifacts_preserved=True,new_credit=0,full_goal_complete=False))
