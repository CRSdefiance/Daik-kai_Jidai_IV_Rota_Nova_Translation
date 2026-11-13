"""Render complete clean-only exchanges,including every actor-style slot alias."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B111_B119_clean_transcripts_v3212')
SOURCE=Path('work/analysis/lil_B111_B119_source_v3210b/complete182_clean_current_native_context.json')
BRANCH=Path('work/analysis/lil_B111_B119_branches_v3211/original_relative_skip_operand_proof.json')
if __name__=='__main__':
    assert not ROOT.exists();source,branch=map(read,[SOURCE,BRANCH]);ROOT.mkdir(parents=True);files=[]
    for b in source['blocks']:
        rows={r['source_reference']['header_offset']:r for r in b['records']};objects={o['command_offset']:o for o in b['actor_style_objects']};choices={o['command_offset']:o for o in b['choices']};lines=[f"B{b['block']} COMPLETE CLEAN JAPANESE ONLY",'Storage/branch structure isnot actual earned progression.',str(b['original_event_source'])]
        for command in b['all_clean_native_commands']:
            at,word=command['offset'],command['word'];lines.append(f"\n@{at:04X} WORD{word:04X} extent{command['native_extent']} ancestors{command['ancestor_0100_offsets']}")
            if at in rows:
                r=rows[at];lines.extend([f"{r['id']} SELECTOR{r['source_presentation_prefix_hex']}",r['source_Japanese']])
            elif at in objects:
                o=objects[at];lines.append('ACTOR-STYLE ALTERNATIVES;NOT PLAYER CHOICES')
                for r in o['records']:lines.extend([f"{r['id']} STYLES{r['style_indices']} SELECTOR{r['source_selector']}",r['source_Japanese']])
            elif at in choices:
                lines.append('THREE-OPTION PLAYER MENU;ORDER0/1/2')
                for r in choices[at]['records']:lines.extend([f"{r['id']} OPTION{r['option_index']}",r['source_Japanese']])
            else:lines.append('SOURCE CONTROL '+command['whole_command_hex'][:96]+('...'if len(command['whole_command_hex'])>96 else ''))
        path=ROOT/f"B{b['block']}_complete_clean_exchange.txt";path.write_text('\n'.join(lines)+'\n',encoding='utf8');files.append(dict(block=b['block'],path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'transcript_provenance.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),branch_proof=str(BRANCH),branch_proof_sha256=sha(BRANCH.read_bytes()),files=files,all148speech_34alternatives_and_nochoices_rendered=True,older_English_excluded=True,complete_reading_context_notes_prose_and_native_display_approval_pending=True,editorial_credit_added=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Nine complete clean-only transcripts;all182objects;no English andno credit.')
