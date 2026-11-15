"""Prepare fresh two-block loader and complete entry census proofs."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/lil_B139_B140_reference_tools_v3480');assert not root.exists();pairs=[]
    def make(a,b,changes):
        a,b=Path(a),Path(b);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x,y in changes:assert x in t,x;t=t.replace(x,y)
        compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');pairs.append(dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())))
    common=[('scripts.prepare_lil_B138_research_v3442b','scripts.prepare_lil_B139_B140_research_v3479'),('lil_B138_research_v3442b','lil_B139_B140_research_v3479'),('lil_B138_loader_v3443b','lil_B139_B140_loader_v3480'),('whole_SC2_and_one_selected_block_initial_entry_proof','whole_SC2_and_two_selected_blocks_initial_entry_proof')]
    make('scripts/verify_lil_B138_loader_v3443b.py','scripts/verify_lil_B139_B140_loader_v3480.py',common+[
      ('for B138 resizing','for B139/B140 resizing'),('one_selected_block_fit_original_0x2400_cache','two_selected_blocks_fit_original_0x2400_cache')])
    make('scripts/verify_lil_B138_references_v3444b.py','scripts/verify_lil_B139_B140_references_v3481.py',common+[
      ('Fresh shipped entry census and112-command/24-span two-block mapping.','Fresh shipped entry census and146-command/52-span two-block mapping.'),('lil_B138_reference_census_v3444b','lil_B139_B140_reference_census_v3481'),('if n not in [138]','if n not in [139,140]'),("len(r['mapped_commands'])for r in result)==111","len(r['mapped_commands'])for r in result)==146"),("r['typed_relative_span_count']for r in result)==45","r['typed_relative_span_count']for r in result)==52"),("r['target_native_skip_cases']for r in result)==225","r['target_native_skip_cases']for r in result)==260"),('all111_commands45_relative_sites','all146_commands52_relative_sites'),('all335_other','all334_other'),('all111_clean_current_target_commands_and45_relative_sites','all146_clean_current_target_commands_and52_relative_sites'),('native_commands_each=111,relative_sites=45,target_native_skip_cases=225','native_commands_each=146,relative_sites=52,target_native_skip_cases=260')])
    root.mkdir(parents=True);save(root/'provenance.json',dict(tools=pairs,producer_sha256=sha(Path(__file__).read_bytes()),all_previous_artifacts_preserved=True,full_goal_complete=False))
