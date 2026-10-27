"""Create scoped whole-loader and fresh command/reference census successors."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B142_B145_reference_tools_v3598');assert not root.exists();pairs=[]
    def make(a,b,changes):
        a,b=Path(a),Path(b);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x,y in changes:assert x in t,x;t=t.replace(x,y)
        compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');pairs.append(dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())))
    make('scripts/verify_lil_B141_loader_v3555.py','scripts/verify_lil_B142_B145_loader_v3598.py',[('prepare_lil_B141_research_v3554','prepare_lil_B142_B145_research_v3597'),('lil_B141_research_v3554','lil_B142_B145_research_v3597'),('lil_B141_loader_v3555','lil_B142_B145_loader_v3598'),('whole_SC2_and_B141_initial_entry_proof','whole_SC2_and_B142_B145_initial_entry_proof'),('B141_fits_original_0x2400_cache','B142_B145_fit_original_0x2400_cache'),('for B141 resizing','for four B142-B145 resized blocks')])
    make('scripts/verify_lil_B141_references_v3556.py','scripts/verify_lil_B142_B145_references_v3599.py',[('prepare_lil_B141_research_v3554','prepare_lil_B142_B145_research_v3597'),('lil_B141_reference_census_v3556','lil_B142_B145_reference_census_v3599'),('lil_B141_loader_v3555','lil_B142_B145_loader_v3598'),('whole_SC2_and_B141_initial_entry_proof','whole_SC2_and_B142_B145_initial_entry_proof'),('if n not in [141]','if n not in [142,143,144,145]'),("for r in result)==37","for r in result)==91"),("for r in result)==13","for r in result)==25"),("for r in result)==65","for r in result)==125"),('all37_commands13_relative_sites','all91_commands25_relative_sites'),('all335_other_SC2_blocks_preserved','all332_other_SC2_blocks_preserved'),('all37_clean_current_target_commands_and13_relative_sites_reexecuted','all91_clean_current_target_commands_and25_relative_sites_reexecuted'),('native_commands_each=37,relative_sites=13,target_native_skip_cases=65','native_commands_each=91,relative_sites=25,target_native_skip_cases=125'),('37-command/13-span one-block','91-command/25-span four-block')])
    root.mkdir(parents=True);save(root/'provenance.json',dict(successors=pairs,no_native_loader_or_parent_success_stubs_added=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
