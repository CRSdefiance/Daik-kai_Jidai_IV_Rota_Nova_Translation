"""Record the viewed clean exchange and bind its scoped role/mentioned-name components."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B52_source_names_v8630')
DISPLAY=Path('work/analysis/Hodram_B52_source_display_v8626/source_display.json')
VM=Path('work/analysis/Hodram_B52_source_choice_VM_v8628b/source_menu_provider_andresponse_paths.json')
PRIOR=Path('translations/rafael_B46_speaker_name_review_v2.json')
GLOSS=Path('work/analysis/Hodram_B52_clean_gloss_v8617/three_first_clean_glosses_two_choice_labels_anddistinct_terminal_risks.json')

if __name__=='__main__':
    assert not ROOT.exists();display,vm,prior,gloss=map(read,[DISPLAY,VM,PRIOR,GLOSS])
    assert display['current_B52_English_dialogue_bodies_unconsulted'] and vm['current_B52_English_dialogue_andchoice_bodies_still_unconsulted']
    image=NdsImage.open(display['candidate']);clean=NdsImage.open('work/clean.nds')
    assert sha(Path(display['candidate']).read_bytes())==display['candidate_sha256']==vm['candidate_sha256'] and sha(image.read_file('/__arm9__.bin'))==vm['ARM9_sha256']
    sheet=display['review_sheet'];assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    assert display['complete_native_source_page_count']==3 and len(display['records'])==3
    assert sum(len(r['original_four_alignments']['cases']) for r in display['records'])==12
    names=display['scoped_clean_current_one_name_andreused_native_consumers'];assert len(names)==1 and names[0]['actor_ID']==113
    role=names[0];assert role['reused_current_original_style11_plane']['text']=='Port Worker' and len(role['reused_current_original_two_getters'])==2
    fields=[]
    for record in prior['mentioned_Hayreddin_component']:
        arm=clean.read_file('/__arm9__.bin') if record['version']=='clean-source' else image.read_file('/__arm9__.bin')
        at=record['table_field_offset'];pointer=int.from_bytes(arm[at:at+4],'little');value=bytes.fromhex(record['hex']);offset=record['offset']
        assert record['actor_ID']==34 and arm[at:at+4].hex()==record['table_field_hex'] and pointer==record['pointer'] and pointer-0x02000000==offset and arm[offset:offset+len(value)+1]==value+b'\0'
        fields.append(dict(**record,checked_in_current_B52_context_ROM=display['candidate'] if record['version']!='clean-source' else 'work/clean.nds',checked_ARM9_sha256=sha(arm)))
    assert [r['text'] for r in fields]==['ハイレディン','Hayreddin']
    record=gloss['groups'][0]['records'][0]
    assert 'ハイレディン一家' in record['source_Japanese'] and all(r['source_selector']==113 for r in gloss['groups'][0]['records'])
    ROOT.mkdir(parents=True)
    save(ROOT/'three_source_pages_role_andHayreddin_component_review.json',dict(candidate=display['candidate'],candidate_sha256=display['candidate_sha256'],display=str(DISPLAY),display_sha256=sha(DISPLAY.read_bytes()),directly_viewed_sheet=sheet,all_three_complete_Japanese_speech_pages_andone_reused_role_plane_directly_viewed=True,complete_first_internal_final_source_glyphs_bounds_andpagination_pass=True,fresh_native_dispatches=3,fresh_macro_alignments=12,source_voice_classes=[0,0,0],scoped_role_review=dict(actor_ID=113,decision='retain',english='Port Worker',source_andcurrent_fields_andreused_consumers=role,reason='Natural neutral occupational nameplate for the clean 出港所の兄貴 role in this gruff warning and response exchange. Avoid a literal brother relationship, invented personal name or elevated harbormaster rank. The unused ヨーロッパ metadata does not establish a personal surname or biography.',new_name_asset=False,full207_name_orother_contexts_approved=False),mentioned_component_review=dict(actor_ID=34,decision='retain-component',source='ハイレディン',english='Hayreddin',prior_review=str(PRIOR),prior_review_sha256=sha(PRIOR.read_bytes()),exact_clean_andcurrent_pointer_fields=fields,reason='Retain the established reviewed component. Source 一家 denotes the named group/outfit in this exchange; it does not prove blood kinship, government rank, nationality or a full-name/catalogue approval.',source_reference=record['source_reference'],source_hex=record['source_hex'],full_name_oractual_34_header_not_approved=True),source_menu=str(VM),source_menu_sha256=sha(VM.read_bytes()),source_choice_glyphs_controller_backing_andactual_branch_visits_pending=True,all_existing_B52_English_bodies_andchoices_still_unconsulted=True,current_English_contextual_comparison_andprose_all_formatting_actual_release_gates_pending=True,no_ROM_registry_orcompletion_credit_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [DISPLAY,VM,PRIOR,GLOSS,Path(__file__)]}))
    print('B52 source pages directly viewed; Port Worker retained with exact reused role consumers, Hayreddin source/current component fields bound. No kinship/full-name/actual-menu/branch claim. Current English remains unread.')
