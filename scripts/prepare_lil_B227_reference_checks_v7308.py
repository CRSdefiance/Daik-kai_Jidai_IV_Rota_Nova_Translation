"""Fresh resized B227 checks with whole-ROM-bound V7277 parent reuse."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B227_reference_tools_v7308')
if __name__=='__main__':
    assert not ROOT.exists()
    loader={'B226':'B227','reference_v7259':'reference_v7307','loader_v7260':'loader_v7308','lil_B225_loader_v7216/whole_SC2_and_B225_initial_entry_proof':'lil_B226_loader_v7260/whole_SC2_and_B226_initial_entry_proof','V7230':'V7277','B2261176_bytes_fit':'B227708_bytes_fit'}
    census={'B226':'B227','reference_v7259':'reference_v7307','reference_census_v7261':'reference_census_v7309','loader_v7260':'loader_v7308','lil_B225_reference_census_v7217/all16_commands_no_relative_or_typed_sites_and_shipped_census':'lil_B226_reference_census_v7261/all22_commands_no_relative_or_typed_sites_and_shipped_census','[226]':'[227]','block=226':'block=227','len(w)==22':'len(w)==13',"len(spec['text_records'])==20":"len(spec['text_records'])==9",'all22_commands':'all13_commands','all22_clean_current_target':'all13_clean_current_target','all22 mapped':'all13 mapped','All22 commands/no relatives or typed controls/A000/normal end':'All13 commands/no relatives or typed controls/three A000/normal end'}
    jobs=[('scripts/verify_lil_B226_loader_v7260.py','scripts/verify_lil_B227_loader_v7308.py',loader),('scripts/verify_lil_B226_references_v7261.py','scripts/verify_lil_B227_references_v7309.py',census)]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_loader_andcensus.json',dict(tools=rows,source668_logical666_tail2_target708_logical706_tail2_bound=True,all13_commands9_preambles_three_A000_andfull_end_required=True,parent_V7277_equals_prior_B226_research_by_whole_ROM_hash=True,one_fresh_target_census336_fresh_loads672_fresh_parent_modes=True,new_credit=0,full_goal_complete=False))
