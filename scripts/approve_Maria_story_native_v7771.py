"""Approve67 individual prose/display gates; two conditionals remain explicitly offline."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.maria_story_profile_v1 import contract
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Maria_story_final_paths_v7771 import *
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    assert not APPROVAL.parent.exists() and not APPROVED.exists()
    old,policy,stored,actual,view,names,source=map(read,[DRAFT,POLICY,STORED,ACTUAL,VIEW,NAMES,SOURCE])
    bindings=contract()['record_bindings'];positive={r['id']:r for r in policy['positive_cases']}
    assert policy['positive_count']==67 and policy['negative_count']==200
    assert stored['stored_alignment_coverage']==268 and stored['zero_ink_parity_tails']==33 and stored['final_complete_native_pages']==67
    assert view['all130_final_actual_panes_viewed_with_exact_reuse'] and view['complete_body_andheader_holds']==528
    assert actual['total_actual_speech_occurrences']==actual['complete_actual_page_panels']==130 and not actual['unresolved']
    panels={s['id']:s for g in actual['groups'] if g['version']=='English' for s in g['speech_observations']}
    assert len(panels)==65
    offline={'DK4_MES_B108_R0020','DK4_MES_B108_R0125'}
    assert set(bindings)-set(panels)==offline
    doc=deepcopy(old)
    for row in doc['records']:
        ident=row['id'];b=bindings[ident];qa=positive[ident]['qa'];panel=panels.get(ident)
        assert row['english']==b['logical_English'] and row['source_hex']==b['compiler_source_hex']
        assert not row['review']['formatting'] and qa['native_page_count']==1 and not qa['issues'] or not row['review']['formatting'] and qa['native_page_count']==1 and all(i['severity']=='info' for i in qa['issues'])
        name=next(n for n in names['records'] if n['actor_ID']==row['source_selector'])
        speaker=next(v['text'] for v in name['original_getters'] if v['consumer']=='progressive-nameplate')
        row.update(logical_English=row['english'],english=b['planning_record']['english'],route=3,route_identity='Maria',
            speaker=speaker,source_meaning=row['source_gloss'],context=row['full_clean_exchange_context'],
            localization_note=row['decision_reason'],editorial_finding=row['decision_reason'],
            editorial_decision='revise' if row['decision']=='revision' else 'retain-wording',
            retention_reason=row['decision_reason'] if row['decision']=='retention' else None,
            whole_English_exchange_cadence_andemotional_progression_reviewed=True,
            compiled_hex=b['compiled_hex'],formatted_markup=qa['formatted_markup'],base_QA_report=qa,
            qa_waivers=[],qa_waiver_reason=None,row_count_reason=b['row_count_reason'],reviewed_ordinary_boundaries=[],
            native_profile_maximum_total_rows=4,original_physical_native_rows_per_page=4,native_page_count=1,
            actual_record_observed=panel is not None,
            actual_complete_body_andheader_holds=0 if panel is None else sum(len(p['complete_body_andname_holds']) for p in panel['pages']),
            offline_only_reason=None if panel else 'Original Julian-dependent branch not played by the unforced fixture. Exact source/current/target controls,selector/getters,logical/compiled/stored four alignments andcomplete native page areverified;individual conditional visitation isnot required bythe authorized workflow.',
            shared_name_label_semantics_not_approved=row['source_selector']==155,
            registered_integration_pending=True,
            formatting_reason='Complete whole-exchange English isautomatically formatted under the exact file/record/selector scoped216px,four-row profile;FI5/FA2/FO7 measured fromown Maria context. All first/internal/final native glyphs,guarded linebreaks,bounds,canaries,consumption andstored zero-ink tails pass. All67 areone page;22 individual row-count infos,no warnings orwaivers. Paired source/finalEnglish fixtures cover65 distinct speeches each,130complete panes,528complete body+name holds;two Julian conditional speeches remainexplicitly offline. Original branches,setup,witnessed previous-result extents,normal type0 valuecarry andreturns preserved. Native/source-only R65 nineteenth-cell finding isnot anEnglish width change. All measured timing,RNG,actor/component/calendar andlater RGB differences remainbound;no broad simulation/full-effects/everyframe/future claim. Existing system-only unlock isdisclosed,earned=false;initialized background isnot natural optional activation/location. Shared actor155 semantic wording,full207 names/catalogueUI andother consumers remainopen. Atomic production,registered reconstruction,clean-input patch andown-ROM startup remainpending.')
        row['review']['formatting']=True
    assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':48,'retain-wording':19}
    assert [r['logical_English'] for r in doc['records']]==[r['english'] for r in old['records']]
    doc.update(translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        route_identity='Maria',source_ROM=source['source_ROM'],source_ROM_sha256=source['source_ROM_sha256'],
        review_gates=['source','context','localization','naturalness','formatting'],
        previous_manuscript=str(DRAFT),previous_manuscript_sha256=sha(DRAFT.read_bytes()),
        historical_all67_formatting_gates_false=doc.pop('all67_formatting_gates_false'),all67_five_individual_gates_true=True,
        formatting_review_pending=False,actual_objects=65,offline_only_objects=2,offline_only_object_IDs=sorted(offline),
        native_approval=str(APPROVAL),source_prose_or_completion_credit_added=0,
        no_global_name_asset_change_shared155_semantics_open=True,status='67 individual gates approved;reference seal,atomic production andregistered integration pending')
    for key,p in proofs().items():doc[key]=p;doc[key+'_sha256']=sha(Path(p).read_bytes())
    validate_natural_dialogue_batch(doc);save(APPROVED,doc);APPROVAL.parent.mkdir(parents=True)
    save(APPROVAL,dict(manuscript=str(APPROVED),manuscript_sha256=sha(APPROVED.read_bytes()),
        all67_individual_five_gates_approved=True,revision_count=48,retention_count=19,actual_final_pages=130,
        actual_speeches_each_language=65,offline_only_speech_IDs=sorted(offline),complete_body_andheader_holds=528,
        all67_native_stored_pages_complete_andall_original_controls_preserved=True,
        all_measured_late_differences_andnatural_activation_limits_preserved=True,
        full207_names_shared155_semantics_other_consumers_graphics_andlater_audit_open=True,
        source_prose_or_completion_credit_added=0,evidence={str(p):sha(p.read_bytes()) for p in [DRAFT,*map(Path,proofs().values()),Path(__file__)]},full_goal_complete=False))
    print('67individual five-gate decisions approved:48revisions/19retentions;65actual+2offline perlanguage.Preserved namescope/late-state limits.No credit untilregistered release.')
