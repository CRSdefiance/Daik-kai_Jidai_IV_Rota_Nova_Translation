"""Bind both clean Japanese choice labels through original count/pointer getters at both even alignments."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prove_lil_B212_consumers_v6595 import choice_getters
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B52_choice_source_v8627')
SOURCE=Path('work/analysis/Hodram_B52_clean_v8616/complete_clean_SC1_B52_EV1_andcoverage_before_current_English.json')
GLOSS=Path('work/analysis/Hodram_B52_clean_gloss_v8617/three_first_clean_glosses_two_choice_labels_anddistinct_terminal_risks.json')
CONTROLS=Path('work/analysis/Hodram_B52_source_controls_v8620/source_controls.json')
if __name__=='__main__':
    assert not ROOT.exists();source,gloss,controls=map(read,[SOURCE,GLOSS,CONTROLS]);g=source['groups'][0];choice=next(c for c in g['commands'] if c['word']==0x2100);assert choice==gloss['source_typed_choice']['command'] and controls['current_B52_English_dialogue_bodies_still_unconsulted']
    current=NdsImage.open(controls['candidate']);clean=NdsImage.open('work/clean.nds');arm,ja=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin');assert sha(Path(controls['candidate']).read_bytes())==controls['candidate_sha256'] and sha(Path('work/clean.nds').read_bytes())==source['source_ROM_sha256']
    spans=[(0x2A1D8,0x2A414),(0x24048,0x24118)];assert all(arm[a:b]==ja[a:b] for a,b in spans);versions=[]
    for version,code in [('clean_Japanese',ja),('current_unchanged_getter_code',arm)]:
        result=choice_getters(code,choice);assert [r['input_alignment'] for r in result]==[0,2]
        for case in result:
            assert case['count']==2 and case['original_count_pointer_ABI_all4MiB_owner_stream_and_guards_exact']
            for native,label in zip(case['labels'],gloss['source_typed_choice']['labels'],strict=True):
                assert native['text']==label['source_Japanese'] and native['hex']==label['source_hex'] and native['offset']==label['source_reference']['offset']
        versions.append(dict(version=version,alignment_cases=result))
    assert versions[0]['alignment_cases']==versions[1]['alignment_cases'];ROOT.mkdir(parents=True);save(ROOT/'source_choice_getters.json',dict(source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),first_clean_gloss=str(GLOSS),first_clean_gloss_sha256=sha(GLOSS.read_bytes()),source_control_proof=str(CONTROLS),source_control_proof_sha256=sha(CONTROLS.read_bytes()),current_ROM=controls['candidate'],current_ROM_sha256=controls['candidate_sha256'],command=choice,clean_label_references=gloss['source_typed_choice']['labels'],versions=versions,native_count_cases=4,native_label_pointer_cases=8,all_two_source_labels_two_versions_two_even_alignments_exact=True,all4MiB_owner_stream_ABI_andcanary_guards_exact=True,unchanged_source_choice_getter_code_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],source_owned_choice_getters=inspect.getsource(choice_getters),full_UI_renderer_geometry_labels_glyphs_andchoice_result_routing_unexecuted=True,current_B52_English_dialogue_andchoice_bodies_still_unconsulted=True,no_ROM_registry_ledger_orcredit_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,GLOSS,CONTROLS,Path(choice_getters.__code__.co_filename),Path(__file__)]}))
    print('B52 cleanchoice:4native counts/8labelpointer cases,そんな気はない/相手になろう exact atboth evenalignments throughsame clean/currentcode.UIgeometry/glyphs/result routing andEnglish remainpending;no credit.')
