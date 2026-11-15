"""Author the entire B204 exchange with individual revisions and justified retentions."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from scripts.lil_B204_prose_v6120 import REVISIONS,RETAIN_NOTES,CONTEXT
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B204_prose_v6120');OUT=Path('translations/lil_B204_editorial_manuscript_v1.json')
SOURCE=Path('work/analysis/lil_B204_current_v6118/all20_clean_current_complete_context.json')
FINDINGS=Path('work/analysis/lil_B204_contextual_findings_v6088/twenty_source_current_findings_eight_proposed_retentions_twelve_revisions.json')
CONTROL=Path('work/analysis/lil_B204_dispatches_v6119b/all20_source_current_dispatches_four_FE_letters_no_macros_and6_control_leaves.json')
NAMES=Path('work/analysis/lil_B204_source_names_v6065/five_exact_source_name_fields_voices_and_distinct_name_consumers.json')
VIEW=Path('work/analysis/lil_B204_source_view_v6077/complete_source_scenes_and_return_visual_review.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists();packet,findings,control,names,view=map(read,[SOURCE,FINDINGS,CONTROL,NAMES,VIEW])
    assert set(REVISIONS).isdisjoint(RETAIN_NOTES) and set(REVISIONS)|set(RETAIN_NOTES)=={r['source_record_index'] for r in packet['records']}
    assert view['all20_Japanese_objects_four_FE_letter_parts_and_full_signature_viewed'] and len(control['speech_dispatch_cases'])==40 and len(control['source_current_opaque_nonrelative_control_leaves'])==6
    prior={r['source_record_index']:r for r in findings['records']};actors={2:'Lil',11:'Jam',124:'Guard',130:'Daimyo',145:'Innkeeper',254:'Jam (written letter)'};rows=[]
    catalog=read(control['registered_catalog_binding'])['records'];matches=[]
    for original in packet['records']:
        r=deepcopy(original);index=r['source_record_index'];raw=bytes.fromhex(r['current_hex']);previous=' '.join(raw[1:].decode('ascii').split())
        assert previous==' '.join(prior[index]['older_English'].split()) and r['source_hex']==prior[index]['source_hex']
        for c in catalog:
            if bytes.fromhex(c['key_hex'])==raw[1:] and c['route_mask']&4:matches.append(dict(id=r['id'],catalogue=c))
        revise=index in REVISIONS;body,note=REVISIONS[index] if revise else (previous,RETAIN_NOTES[index])
        assert body==body.strip() and '\n' not in body and '\0' not in body and '{' not in body and '  ' not in body and (body!=previous)==revise
        assert not any(m in body for m in ['FI','FA','FO'])
        r.update(english='{SPEAKER:'+format(r['source_selector'],'02X')+'}'+body,speaker=actors[r['source_selector']],source_meaning=r['fresh_source_gloss'],context=CONTEXT,localization_note=note,editorial_decision='revise' if revise else 'retain-wording',effective_predecessor_paragraph=previous,previous_raw_storage_body=raw[1:].decode('ascii'),previous_effective_runtime_paragraph=previous,registered_runtime_catalogue_match=None,whole_exchange_finding=prior[index]['whole_exchange_finding'],full_clean_context_precedes_comparison=True,editorial_predecessor_English_comparison_pending=False,current_native_voice_macro_entry_and_context_pending=False,current_macro_dispatch_bound=True,current_complete_native_display_pending=True,current_native_UI_body_explicit_unexecuted_boundary=True,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status='source-prose-approved-native-format-relocation-actual-release-pending',prose_author_module='scripts/lil_B204_prose_v6120.py',record_index=r['current_record_index'])
        if not revise:r['fresh_retained_wording_justification']=note
        rows.append(r)
    assert not matches and Counter(r['editorial_decision'] for r in rows)=={'revise':12,'retain-wording':8}
    doc=dict(format='dk4-editorial-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],source_ROM=packet['source_ROM'],source_ROM_sha256=packet['source_ROM_sha256'],required_runtime_ARM9_sha256=packet['current_ARM9_sha256'],current_COMMON_sha256=packet['current_COMMON_sha256'],current_strict_native_input=packet['current_strict_native_input'],current_strict_native_input_sha256=packet['current_strict_native_input_sha256'],source_prose_or_completion_credit_added=0,formatting_review_pending=True,status='source-prose-approved-native-format-relocation-actual-release-pending',whole_exchange_context=CONTEXT,records=rows,revised=12,retained=8,all20_source_objects_observed_in_disclosed_content_fixture=True,no_natural_event_original_location_earned_inventory_or_full_effect_claim=True,no_authored_breaks_alignment_spaces_or_fit_driven_prose_shortening=True,five_source_actors16_progressive_four_FE_letters_six_leaves_no_macros_choices_predicates_or_relative_sites=True,source_name_fields_and_progressive_catalogue_distinction_preserved=True,contextual_name_decisions=deepcopy(view['nameplate_decisions']),coordinated_item116_already_integrated_V6110_no_duplicate_item_or_name_credit=True,broader207_name_role_alias_review_and_all_editorial_scope_remain_open=True,full_goal_complete=False)
    for key,p in [('source_context',SOURCE),('effective_current_comparison',FINDINGS),('control_contract',CONTROL),('actor_terminology_reconciliation',NAMES),('actual_source_visual_review',VIEW),('source_prose_module',Path('scripts/lil_B204_prose_v6120.py'))]:doc[key]=str(p);doc[key+'_sha256']=sha(p.read_bytes())
    save(OUT,doc);ROOT.mkdir(parents=True);save(ROOT/'twenty_uncredited_contextual_prose_decisions.json',dict(manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),revised=12,retained=8,all20_have_four_prose_gates_true_formatting_false=True,all20_source_objects_and_complete_letter_reviewed=True,no_registered_runtime_catalogue_matches=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,FINDINGS,CONTROL,NAMES,VIEW,Path(__file__),Path('scripts/lil_B204_prose_v6120.py')]}));print('B20420 whole-exchange decisions:12 revisions/8 individually justified retentions. Four prose gates;native,actual,release and credit pending.')
