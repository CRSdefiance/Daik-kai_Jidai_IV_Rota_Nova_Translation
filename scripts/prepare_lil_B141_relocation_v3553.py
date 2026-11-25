"""Generate exact one-block relocation and final stored-target proof successors."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/lil_B141_relocation_tools_v3553');assert not root.exists();pairs=[]
    def make(a,b,changes):
        a,b=Path(a),Path(b);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x,y in changes:assert x in t,x;t=t.replace(x,y)
        compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');pairs.append(dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())))
    make('scripts/research_lil_B139_B140_relocation_v3478.py','scripts/research_lil_B141_relocation_v3553.py',[
        ('lil_B139_B140_relocation_v3478','lil_B141_relocation_v3553'),('lil_B139_B140_editorial_manuscript_v6','lil_B141_editorial_manuscript_v6'),('all_routes_combined_v3450','all_routes_combined_v3526'),
        ("len(results)==2 and sum(len(r['text_records']) for r in results)==67","len(results)==1 and sum(len(r['text_records']) for r in results)==14"),
        ("len(r['relative_skip_fixups']) for r in results)==52","len(r['relative_skip_fixups']) for r in results)==13"),
        ("len(r['target_native_skip_cases']) for r in results)==260","len(r['target_native_skip_cases']) for r in results)==65"),
        ("len(r['command_map']) for r in results)==146","len(r['command_map']) for r in results)==37"),
        ('[139,140]','[141]'),('all67speech_and52_relative_operands_preserved','all14speech_and13_relative_operands_preserved'),('all260_relocated_native_skip_cases','all65_relocated_native_skip_cases'),('all334_other_SC2_blocks','all335_other_SC2_blocks'),
        ('146commands/67speech/52spans/260targetskipcases,inversebytes and334otherblocks','37commands/14speech/13spans/65targetskipcases,inversebytes and335otherblocks')])
    make('scripts/prepare_lil_B139_B140_research_v3479.py','scripts/prepare_lil_B141_research_v3554.py',[
        ('Two-block research image and 67 complete final stored paragraph proofs.','One-block research image and14 complete final stored paragraph proofs.'),
        ('scripts.verify_lil_B139_B140_fonts_v3474','scripts.verify_lil_B141_fonts_v3549'),('lil_B139_B140_research_v3479','lil_B141_research_v3554'),('all_routes_combined_v3450','all_routes_combined_v3526'),('lil_B139_B140_V3450','lil_B141_V3526'),('lil_B139_B140_relocation_v3478','lil_B141_relocation_v3553'),('lil_B139_B140_native_approval_v3475/all67','lil_B141_native_approval_v3550/all14'),
        ('all67speech_and52_relative_operands_preserved','all14speech_and13_relative_operands_preserved'),('all260_relocated_native_skip_cases','all65_relocated_native_skip_cases'),('lil_B139_B140_fonts_v3474','lil_B141_fonts_v3549'),('[139,140]','[141]'),('[2,4,9,16,20,21,171]','[2,9,20,171]'),
        ('len(parity)==67 and macro_calls==268','len(parity)==14 and macro_calls==56'),('all334_other','all335_other'),('all67','all14'),('current_final_padded_macro_alignment_cases=268','current_final_padded_macro_alignment_cases=56'),('and268_macro_alignments','and56_macro_alignments'),('actual_selected_B139_B140_IDs','actual_selected_B141_IDs'),
        ('Unregistered V3450-derived two-block','Unregistered V3526-derived one-block'),('Researchimage changesB139/B140only;67final nativeplanes/268macro cases and334otherblocks','Researchimage changesB141only;14final nativeplanes/56macro cases and335otherblocks')])
    root.mkdir(parents=True);save(root/'provenance.json',dict(tools=pairs,all_previous_ROMs_translations_and_producers_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
