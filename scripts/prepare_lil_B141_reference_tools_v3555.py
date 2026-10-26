"""Prepare source/current/relocated loader and fresh executable entry checks."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B141_reference_tools_v3555');assert not root.exists();pairs=[]
    def make(a,b,changes):
        a,b=Path(a),Path(b);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x,y in changes:assert x in t,x;t=t.replace(x,y)
        compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');pairs.append(dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())))
    common=[('scripts.prepare_lil_B139_B140_research_v3479','scripts.prepare_lil_B141_research_v3554'),('lil_B139_B140_research_v3479','lil_B141_research_v3554'),('lil_B139_B140_loader_v3480','lil_B141_loader_v3555'),('whole_SC2_and_two_selected_blocks_initial_entry_proof','whole_SC2_and_B141_initial_entry_proof')]
    make('scripts/verify_lil_B139_B140_loader_v3480.py','scripts/verify_lil_B141_loader_v3555.py',common+[('B139/B140 resizing','B141 resizing'),('two_selected_blocks_fit_original_0x2400_cache','B141_fits_original_0x2400_cache')])
    make('scripts/verify_lil_B139_B140_references_v3481.py','scripts/verify_lil_B141_references_v3556.py',common+[
        ('Fresh shipped entry census and146-command/52-span two-block mapping.','Fresh shipped entry census and37-command/13-span one-block mapping.'),('lil_B139_B140_reference_census_v3481','lil_B141_reference_census_v3556'),('[139,140]','[141]'),
        ("len(r['mapped_commands'])for r in result)==146","len(r['mapped_commands'])for r in result)==37"),
        ("r['typed_relative_span_count']for r in result)==52","r['typed_relative_span_count']for r in result)==13"),
        ("r['target_native_skip_cases']for r in result)==260","r['target_native_skip_cases']for r in result)==65"),
        ('all146_commands52_relative_sites','all37_commands13_relative_sites'),('all146_clean_current_target_commands_and52_relative_sites','all37_clean_current_target_commands_and13_relative_sites'),('all334_other','all335_other'),('native_commands_each=146,relative_sites=52,target_native_skip_cases=260','native_commands_each=37,relative_sites=13,target_native_skip_cases=65')])
    root.mkdir(parents=True);save(root/'provenance.json',dict(tools=pairs,all_previous_artifacts_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
