"""Review the whole brought-it follow-up from clean Japanese;retain one wording andrevise two."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B50_prose_v8489')
CURRENT=Path('work/analysis/Hodram_B50_current_v8488/current_effective.json')
GLOSS=Path('work/analysis/Hodram_B50_clean_gloss_v8483/three_first_clean_glosses_gift_andoutgoing_wristband.json')
DISPLAY=Path('work/analysis/Hodram_B50_source_display_v8487/source_display.json')
VIEW=Path('work/analysis/Hodram_B50_source_view_v8487b/source_view.json')
DOC=Path('translations/hodram_B50_editorial_manuscript_v1.json')
NAMES=Path('translations/hodram_B50_speaker_name_review_v1.json')
DECISIONS={
 7:dict(decision='retention',english='You brought it?! Let me see!',
    finding='The existing startled question and immediate request already convey the arrival and her eager interest naturally. The raw authored line breaks still need automatic full-width reflow.',
    rationale='Retain the wording because brought it preserves 持ってきてくれた and the question/request reads naturally as the opening of this excited exchange. Japanese repeats 見せて for emphasis; the quick English request and punctuation carry that eagerness. The context supplies the benefactive force of くれた. The line adds no lateness, search location, hardship, relationship or rank. Remove only legacy ordinary wrapping through the formatter.'),
 10:dict(decision='revision',english='Wow! It really is cute! Here, take this! Yay! Bye!',
    finding='The current line keeps her enthusiasm, offer and farewell. It compresses ホントだ and makes the gift gesture a clipped Take the bow. The bow is supported by the native item148 operand; it is not a fabricated object.',
    rationale='Restore delighted confirmation with It really is cute! and express はい、これあげる as the natural gift offer Here, take this! Preserve the source deictic this and the original item display. Yay! conveys the slang cheer やりー; Bye! keeps the casual farewell. Read with the prior request, this progresses from seeing the item to delight, reciprocal offer, cheer and departure. No power, rarity, price, romance, rank, promise, earned inventory or extra award is added.'),
 13:dict(decision='revision',english='You handed over the Heavenly Wristband.',
    finding='The existing passive item-name-plus-given notice is terse and leaves the handover direction implicit. The clean FE source is byte-identical to the preceding reviewed outgoing-wristband notice.',
    rationale='Make the player-directed outgoing action explicit and use the same approved item wording as B49R81. 渡しました reports handing over the Heavenly Wristband; it does not announce receiving it or a bow reward. Retain the FE system consumer with no personal speaker name. Original item148 display/effects remain separate. This editorial wording makes no claim about legitimately earned possession or original optional-event eligibility.'),
}

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists() and not NAMES.exists();current,gloss,display,view=map(read,[CURRENT,GLOSS,DISPLAY,VIEW]);ledger=read('translations/editorial_review_current_v1.json')
    assert current['all_three_clean_first_whole_exchange_glosses_precede_current_English_exposure'] and gloss['all3_clean_utterances_glossed_before_current_English'] and view['all3_complete_source_pages_directly_viewed']
    assert current['source_gloss_sha256']==sha(GLOSS.read_bytes()) and current['source_display_proof_sha256']==sha(DISPLAY.read_bytes()) and ledger['records_editorially_completed']==7221
    keys={historical_key(r) for f in ledger['completed_editorial_families'] for r in f['records']};assert len(keys)==7221 and not keys&{historical_key(r) for r in current['records']}
    assert len(current['records'])==3 and [r['source_record_index'] for r in current['records']]==[7,10,13]
    rows=[]
    for original in current['records']:
        row=deepcopy(original);choice=DECISIONS[row['source_record_index']];fe=row['source_selector']==254
        if choice['decision']=='retention':assert choice['english']==row['effective_predecessor_paragraph']
        else:assert choice['english']!=row['effective_predecessor_paragraph']
        english=choice['english'];assert not any(x in english for x in ['\n','\r','{LB','{ALIGN','{PAD']) and english==english.strip()
        row.update(english=english,logical_English=english,planned_English_markup=('{SPEAKER:FE}' if fe else '{SPEAKER:02}')+english,speaker='System notice' if fe else 'Lil Argot',
            context='The complete source event50 follow-up explicitly depends on49. Lil reacts to the item being brought to her, asks to see it, confirms its cuteness, offers this, cheers and says goodbye; the following original FE notice reports the outgoing wristband. Native item148 uses layout0 and an original hide boundary. Outer eligibility, scheduler, original location, legitimately earned inventory and chronology beyond the explicit dependency remain unproven.',
            source_meaning=row['first_clean_source_gloss'],source_context_note=row['source_context_note'],localization_note=choice['rationale'],retention_reason=choice['rationale'],decision=choice['decision'],finding=choice['finding'],
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),native_body_consumer='FE-paper' if fe else 'progressive',authored_ordinary_breaks=0,authored_alignment_spaces=0,manual_break_reason='',
            prior_raw_storage_preserved=row['current_raw_storage_English'],prior_effective_paragraph_preserved=row['effective_predecessor_paragraph'],previous_translation_andall_source_current_references_preserved=True,
            source_prose_orcompletion_credit_added=False,formatting_native_stored_actual_policy_atomic_andregistered_integration_pending=True)
        rows.append(row)
    assert Counter(r['decision'] for r in rows)=={'revision':2,'retention':1}
    identity=display['clean_current_Lil_fields'];assert identity['actor_ID']==2 and [f.get('text') for f in identity['clean_fields']]==['リル','アーゴット',None] and [f.get('text') for f in identity['current_fields']]==['Lil','Argot',None]
    reason='リル・アーゴット is the established Lil Argot. Retain the source given/family identity and natural existing full-name header. Both current original getters resolve Lil Argot; the style11 plane and complete leading/trailing glyphs are reused only through identical complete ARM9/COMMON/font and whole current actors. The two original B50 selector02 dispatches resolve actor2/voice3. No new title, kinship, age, marriage, nationality, romance or biographical fact is introduced. FE is a system consumer with no actor254/name.'
    name_row=dict(id='Hodram_B50_actor2_Lil_Argot',actor_ID=2,source='リル・アーゴット',current='Lil Argot',english='Lil Argot',speaker='Lil Argot',context=rows[0]['context'],source_meaning='Given/family name of the same established character speaking the two source selector02 records.',localization_note=reason,retention_reason=reason,decision='retention',review=dict(source=True,context=True,localization=True,naturalness=True,formatting=True),exact_clean_current_fields=identity,original_getters=display['reused_original_Lil_getters'],native_style11_plane=display['reused_original_Lil_style11_plane'],field_andgetter_andplane_binding_reused_not_new_capture_ornew_name_asset=True)
    save(NAMES,dict(format='dk4-speaker-name-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',records=[name_row],scoped_actor_IDs=[2],source_display=str(DISPLAY),source_display_sha256=sha(DISPLAY.read_bytes()),no_new_name_asset_orall207_name_review_credit=True,no_FE_personal_actor_name=True,new_credit=0,full_goal_complete=False))
    doc=dict(format='dk4-script-batch-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),file_path='/data/SC1.DK4',route=1,route_identity='Hodram',blocks=[50],
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_ARM9_sha256=current['current_ARM9_sha256'],current_COMMON_sha256=current['current_COMMON_sha256'],current_archive_sha256=current['current_archive_sha256'],records=rows,revised=2,retained=1,total_editorial_objects=3,physical_speech_objects=3,typed_choice_objects=0,names_packet=str(NAMES),names_packet_sha256=sha(NAMES.read_bytes()),source_context=str(GLOSS),source_context_sha256=sha(GLOSS.read_bytes()),current_packet=str(CURRENT),current_packet_sha256=sha(CURRENT.read_bytes()),source_macro_counts=dict(FI=0,FA=0,FO=0),source_FE_panels=1,all_three_clean_first_glosses_precede_current_English=True,whole_exchange_context_andemotional_progression_reviewed=True,all_three_four_prose_gates_true_formatting_false=True,ordinary_wrapping_owned_by_formatter=True,no_new_ROM_orregistered_stage_orcompletion_credit=True,new_credit=0,full_goal_complete=False)
    save(DOC,doc);ROOT.mkdir(parents=True);save(ROOT/'three_source_current_decisions.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),records=[dict(id=r['id'],source_reference=r['source_reference'],current_reference=r['current_reference'],source_hex=r['source_hex'],current_hex=r['current_hex'],prior=r['effective_predecessor_paragraph'],english=r['english'],decision=r['decision'],finding=r['finding'],reason=r['retention_reason']) for r in rows],revised=2,retained=1,source_first_whole_exchange_prose_review_only=True,all_formatting_gates_false_until_native_fullwidth_completeglyph_bounds_pagination_stored_andactual_checks=True,formal_profile_policy_atomic_andregistered_work_pending=True,no_credit=True,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,GLOSS,DISPLAY,VIEW,DOC,NAMES,Path(__file__)]}))
    for row in rows:print(row['id'],row['decision'],repr(row['english']))
    print('B50prose:two revisions/one justifiedretention;one scoped Lilname retention. Formatting/native/stored/actual/policy/registered gates pending;zero credit.')
