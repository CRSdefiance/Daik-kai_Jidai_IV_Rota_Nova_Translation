"""Author all17 source-bound objects with four individual prose gates and exact echo links."""
from copy import deepcopy
from pathlib import Path
from collections import Counter
from scripts.review_lil_B205_contextual_findings_v6185 import RETAIN
from scripts.lil_B205_prose_v6186 import REVISIONS,CONTEXT
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B205_prose_v6186');OUT=Path('translations/lil_B205_editorial_manuscript_v1.json')
SOURCE=Path('work/analysis/lil_B205_source_v6172/all17_clean_current_complete_context.json')
FINDINGS=Path('work/analysis/lil_B205_contextual_findings_v6185/seventeen_source_current_findings_nine_retentions_eight_revisions.json')
CONTROL=Path('work/analysis/lil_B205_dispatches_v6176/all17_source_current_dispatches_seven_FE_sounds_echoes_no_macros_and8_control_leaves.json')
NAMES=Path('work/analysis/lil_B205_source_names_v6175/two_exact_source_name_fields_voices_and_distinct_name_consumers.json')
VIEW=Path('work/analysis/lil_B205_source_view_v6184/complete_source_scenes_and_return_visual_review.json')
NATIVE=Path('work/analysis/current_V6160_native_v6168/current_native_input.json')
PROSE=Path('scripts/lil_B205_prose_v6186.py')
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists();packet,findings,control,names,view=map(read,[SOURCE,FINDINGS,CONTROL,NAMES,VIEW]);prior={r['source_record_index']:r for r in findings['records']}
    assert set(REVISIONS).isdisjoint(RETAIN) and set(REVISIONS)|set(RETAIN)==set(prior) and len(prior)==17
    assert view['all17_Japanese_objects_five_FE_echoes_and_two_sound_captions_viewed'] and len(control['speech_dispatch_cases'])==34 and len(control['source_current_opaque_nonrelative_control_leaves'])==8
    rows=[];targets={}
    for original in packet['records']:
        r=deepcopy(original);i=r['source_record_index'];previous=prior[i]['older_effective_runtime_paragraph'];revise=i in REVISIONS
        body,note=REVISIONS[i] if revise else (previous,RETAIN[i]);assert (body!=previous)==revise and body==body.strip() and all(x not in body for x in ['\n','\0','{','  '])
        assert r['source_hex']==prior[i]['source_hex'] and r['current_hex']==prior[i]['current_hex'];selector=r['source_selector'];speaker={2:'Lil',15:'Angelo'}.get(selector,'Sound caption' if i in [5,51] else 'Parrot (mimicked words)')
        targets[i]=body
        r.update(english='{SPEAKER:'+format(selector,'02X')+'}'+body,speaker=speaker,source_meaning=r['fresh_source_gloss'],context=CONTEXT,localization_note=note,editorial_decision='revise' if revise else 'retain-wording',effective_predecessor_paragraph=previous,previous_raw_storage_body=prior[i]['older_English'],previous_effective_runtime_paragraph=previous,registered_runtime_catalogue_match=None,whole_exchange_finding=prior[i]['whole_exchange_finding'],full_clean_context_precedes_comparison=True,editorial_predecessor_English_comparison_pending=False,current_native_voice_macro_entry_and_context_pending=False,current_macro_dispatch_bound=True,current_complete_native_display_pending=True,current_native_UI_body_explicit_unexecuted_boundary=True,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status='source-prose-approved-native-format-relocation-actual-release-pending',prose_author_module=str(PROSE),record_index=r['current_record_index'])
        if not revise:r['fresh_retained_wording_justification']=note
        rows.append(r)
    echoes=[(9,13,"What's that?!"),(17,20,'You can talk?!'),(28,32,'A parrot, eh?'),(36,40,'Stop copying me!'),(59,63,'Well? Had enough?')]
    echo_proof=[]
    for spoken,echo,clause in echoes:
        assert clause in targets[spoken] and targets[echo].rstrip('!?').casefold()==clause.rstrip('!?').casefold()
        echo_proof.append(dict(spoken_index=spoken,echo_index=echo,localized_clause=clause,localized_echo=targets[echo],all_words_identical_case_and_source_flat_terminal_punctuation_only=True))
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':8,'retain-wording':9}
    doc=dict(format='dk4-editorial-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],source_ROM=packet['source_ROM'],source_ROM_sha256=packet['source_ROM_sha256'],required_runtime_ARM9_sha256=packet['current_ARM9_sha256'],current_COMMON_sha256=packet['current_COMMON_sha256'],current_strict_native_input=str(NATIVE),current_strict_native_input_sha256=sha(NATIVE.read_bytes()),source_prose_or_completion_credit_added=0,formatting_review_pending=True,status='source-prose-approved-native-format-relocation-actual-release-pending',whole_exchange_context=CONTEXT,records=rows,revised=8,retained=9,five_exact_localized_echo_pairs=echo_proof,all17_source_objects_observed_in_disclosed_content_fixture=True,no_natural_event_original_location_earned_inventory_or_full_effect_claim=True,no_authored_breaks_alignment_spaces_or_fit_driven_prose_shortening=True,two_source_actors10_progressive_seven_FE_objects_eight_leaves_no_macros_choices_predicates_or_relative_sites=True,source_name_fields_and_progressive_catalogue_distinction_preserved=True,contextual_name_decisions=[dict(label='Lil Argot',reason='Established source-owned リル/アーゴット fields and voice3;progressive and full catalogue agree.'),dict(label='Angelo Puccini',reason='Established source-owned アンジェロ/プッチーニ fields and voice4;progressive and full catalogue agree. Mamma mia is source dialogue,not an invented biography.'),dict(label='No added FE actor label',reason='Two sound captions and five bird echoes use the original null actor consumer. Review metadata does not create a runtime nameplate.')],item147_Rainbow_Parrot_retention_source_and_widget_evidence=str(VIEW),no_duplicate_item_name_or_dialogue_credit=True,broader207_name_role_alias_review_and_all_editorial_scope_remain_open=True,full_goal_complete=False)
    for key,p in [('source_context',SOURCE),('effective_current_comparison',FINDINGS),('control_contract',CONTROL),('actor_terminology_reconciliation',NAMES),('actual_source_visual_review',VIEW),('source_prose_module',PROSE)]:doc[key]=str(p);doc[key+'_sha256']=sha(p.read_bytes())
    save(OUT,doc);ROOT.mkdir(parents=True);save(ROOT/'seventeen_uncredited_contextual_prose_decisions.json',dict(manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),revised=8,retained=9,five_localized_echo_pairs=echo_proof,all17_have_four_prose_gates_true_formatting_false=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,FINDINGS,CONTROL,NAMES,VIEW,PROSE,Path(__file__)]}));print('B20517 whole-exchange prose decisions:8 revisions/9 justified retentions;five word-exact echo pairs;native/relocation/actual/release and credit pending.')
