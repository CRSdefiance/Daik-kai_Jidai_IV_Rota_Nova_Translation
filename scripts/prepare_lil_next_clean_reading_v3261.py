"""Prepare complete branch proof and clean-only transcripts for the next exchanges."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

SOURCE=Path('work/analysis/lil_B122_B127_source_v3260c/complete159_clean_current_native_context.json')
ROOT=Path('work/analysis/lil_B122_B127_clean_transcripts_v3262')
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE)
    old=Path('scripts/prove_lil_B111_B119_branches_v3211.py');new=Path('scripts/prove_lil_B122_B127_branches_v3261b.py');assert not new.exists()
    t=old.read_text(encoding='utf-8')
    for a,b in [('lil_B111_B119_branches_v3211','lil_B122_B127_branches_v3261b'),('lil_B111_B119_source_v3210b/complete182_clean_current_native_context.json','lil_B122_B127_source_v3260c/complete159_clean_current_native_context.json')]:assert a in t,a;t=t.replace(a,b)
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');ROOT.mkdir(parents=True);files=[]
    for b in source['blocks']:
        byat={r['source_reference']['header_offset']:r for r in b['records']};menus={r['command_offset']:r for r in b['choices']}
        lines=[f"B{b['block']} COMPLETE CLEAN JAPANESE ONLY",'Physical/conditional sequence; not an earned runtime path.',str(b['original_event_source'])];reading=[lines[0],lines[1]]
        for c in b['all_clean_native_commands']:
            at,word=c['offset'],c['word'];lines.append(f"\n@{at:04X} WORD{word:04X} extent{c['native_extent']} ancestors{c['ancestor_0100_offsets']}")
            if at in byat:
                r=byat[at];text=[r['id']+' SELECTOR'+r['source_presentation_prefix_hex'],r['source_Japanese']];lines.extend(text);reading.extend(['',*text])
            elif at in menus:
                text=['TWO-OPTION MENU;SOURCE ORDER0/1']
                for r in menus[at]['records']:text.extend([r['id']+' OPTION'+str(r['option_index']),r['source_Japanese']])
                lines.extend(text);reading.extend(['',*text])
            else:
                lines.append('SOURCE CONTROL '+c['whole_command_hex'][:96]+('...' if len(c['whole_command_hex'])>96 else ''))
                if word in [0x0000,0x0100,0x0200,0x0300,0x0400,0x2000,0x8000,0x8100]:reading.append(f"[SOURCE CONTROL @{at:04X} WORD{word:04X} extent{c['native_extent']} ancestors{c['ancestor_0100_offsets']}]")
        for kind,body in [('complete_clean_exchange',lines),('clean_reading',reading)]:
            p=ROOT/f"B{b['block']}_{kind}.txt";p.write_text('\n'.join(body)+'\n',encoding='utf-8');files.append(dict(block=b['block'],kind=kind,path=str(p),sha256=sha(p.read_bytes())))
    save(ROOT/'transcript_provenance.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),files=files,all155_speeches_and4_source_choice_labels_rendered=True,all312_source_controls_retained_in_complete_transcripts=True,source2000_UI_boundary_explicit_not_proved=True,older_English_excluded=True,complete_reading_context_notes_prose_and_native_display_approval_pending=True,branch_successor=str(new),branch_successor_sha256=sha(new.read_bytes()),branch_predecessor=str(old),branch_predecessor_sha256=sha(old.read_bytes()),source_prose_or_completion_credit_added=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Six complete clean-only exchanges andreading copies prepared:155speech+4choices. Originalbranch successor prepared;zeroeditorialcredit.')
