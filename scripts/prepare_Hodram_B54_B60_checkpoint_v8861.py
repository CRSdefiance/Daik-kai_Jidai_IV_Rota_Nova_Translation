"""Preserve full editorial scope while recording completed saved evidence and the sealed release closure."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

TEXT="""V8861 continues from independently verified V8843/current registered experimental cumulative V8778. The previous goal turn made verified progress; this turn finishes the saved actual/FE/comparison production readers and seals the release configuration for the pending82 Hodram SC1B54-B60 decisions. All four storylines, earlier translated dialogue, shared town/shop, random scenes, Help/remaining prose, retrospective premature breaks andall207 names/roles/aliases/customnames remain active. Counts remain7,237 completed/7,240 credited source-prose anddrafts/4,492 integrated revisions/2,745 retentions. No new ROM, registration, promotion, separate user package, pruning, commit,push orcredit. Preserve every earlier ROM,translation,draft,producer,proof andfailure.

Reuse all completed clean-first/source/context/prose/five-gate/default-name/native/storage/reference/loader proofs andall14 terminal/reaped gameplay captures. New actual production8847 independently reconstructs12 entire initialized fixtures andtheir whole-ROM inverses,all14 saved runs130,014frames,150 page occurrences and676 complete body-name-orFE-absent-header holds. Every continuation page is checked separately,with original CPU/stream/resident-payload/readonly callback/ordinary controller schedule/unforced selected path/full-end guards. Exactly63 unique utterances are observed;B55 plus18 conditional B58 utterances remain offline-only. All16 changed semantic inputs reject. No new capture,producer replay,natural activation,original location,earned chronology,fullroute orhardware claim.

FE production8851b independently reconstructs2 original paint contexts and6 same-run held snapshots:228x48 logical geometry,288 stride,6x12 metrics,16 physical pitch,current vtables,full palette/header/view,RAM,complete bitmap/VRAM andphysical RGB. Eight semantic defects reject. Preserve stopped8851:all native checks completed before the reconstructed group equality encountered Python RGB tuples versus saved JSON arrays. Qualified modulev2 compares through the original JSON serialization semantics;every native memory,palette,bitmap,VRAM,RGB andreadonly guard remains. Qualification8852 records the original failure andsource-locked successor;no recapture.

Comparison8849b independently recomputes14 complete saved final RAM snapshots,five native components,wholeactors,captain1,rawcalendar andRNG,335 complete later RGBpairs and81 own-language fullmemory/CPU/TCM prefix callbacks. All16 changed inputs reject,including suppressed longB60 actor differences andinvented focused RGB/RNG equality. Main laterRGB differences remain3/22,0/43,0/56,3/77,65/65,61/61;focus remains11/11. Main command differences4/2/5/58/9/10 andduration differences1/0/0/9/2/2 remain. The longB60 persistent actor/wholeactor divergence remains;at focused7001 allfive sampled components/actors/captain/calendar match,with different RNG. No immediate-return mainRAM,causal diagnosis,everyframe orfuture-equivalence claim. Incremental comparison receipts preserve completed cases without replay.

Allnine production validation groups pass886 changed-input rejections:policy625/reconstruction161/references25/native12/controls12/loaders11/actual16/comparison16/liveFE8. Manuscriptv4 preserves all82 five-gate words/bytes/source-current-final references:46 revisions/36 justified retentions,85 English native pages,24 original QAinfos andzero warnings/errors/waivers. Scoped progressive names remain ten approvals/eight actually observed/two offline,with no all207/fullcatalogue/customname approval. Geronimo/Alonso sharedデ full-name ownership/deployment/consumers remain open. Approved Rafael,Hodram,Joakim,Maria,Camille andmixed-width storage remain unchanged.

Seal8855 writes translations/hodram_B54_B60_editorial_release_v1.json andthe source-qualified reference seal. Its3,562 dependency entries preserve all2,468 frozen batch dependencies andevery entry from the complete prior B31/B53 release configuration. CompleteV8778 registered prefix configurations,canonical/clean/current/reference identities,all unowned files/components andmeasured scope remain mandatory. The new atomic planner andlowercase shared adapter are prepared without changing any earlier module,builder orregistry. Wrong-memory8858 rejects all3 genuinely wrong in-memory images withzero commits andall guards active. Atomic positive8857 is running under session14122 fordirect-current andcanonical-source/full-current-memory lifecycles;shared8860 is running under session22682 forone final whole-object commit andlate-target zero-commit rejection. Recheck these specific handles orauthoritative process state;never restart merely because output isquiet orobservation times out. Prepared semantic challenge8859 hasnot yet run. No atomic/shared success is credited before terminal receipts pass.

Next:finish/reuse terminal atomic8857/shared8860 results;run four genuine semantic precommit challenges8859. Bind the final dependency closure andequal lifecycle reports,then registered cumulative integration/exact clean-input patch/manifest/release checks/regressions/ownstartup andonce-only82 credit. Do not replay the already complete native glyph/source/reference/loader/capture readers unnecessarily. CurrentV8778/647 manifestbatches/114 acceptedlayers/18 releasechecks/110 regressions/exactpatch/ownstartup andMainV4701/canonical baseline remain unchanged. Full unfinished-scope keys/values/leads andall earlier document bytes are retained. Graphics/all18 plaques andthe later older-record technical re-audit remain separate. Roughly20,000 remaining is onlya planning estimate,not an audited denominator. The full goal remains active andincomplete.
"""
EXTRA={
 'actual':'work/analysis/Hodram_B54_B60_actual_validation_v8847/independent_actual_validation.json',
 'comparison':'work/analysis/Hodram_B54_B60_comparison_validation_v8849/independent_comparison_validation.json',
 'FE_actual':'work/analysis/Hodram_B56_FE_production_validation_v8851b/independent_FE_actual_validation.json',
}
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_checkpoint_tools_v8861');assert not root.exists()
    text=Path('scripts/checkpoint_Hodram_B54_B60_v8843.py').read_text(encoding='utf-8')
    node=next(n for n in ast.parse(text).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TEXT' for t in n.targets))
    old_text=ast.get_source_segment(text,node.value)
    producer=derive('scripts/checkpoint_Hodram_B54_B60_v8843.py','scripts/checkpoint_Hodram_B54_B60_v8861.py',{
        'Hodram_B54_B60_checkpoint_v8843':'Hodram_B54_B60_checkpoint_v8861',
        'Hodram_SC1B54_B60_82_production_policy_reconstruction_native_references_controls_loaders_pending_actual_atomic_release_v8843':'Hodram_SC1B54_B60_82_allnine_production_groups_sealed_pending_atomic_registered_v8861',
        "SCOPE='unfinished_editorial_scope_v8843'":"SCOPE='unfinished_editorial_scope_v8861'",old_text:repr(TEXT),
        "if __name__=='__main__':":"PRODUCTION.update("+repr(EXTRA)+")\nEVIDENCE += list(PRODUCTION.values()) + ['translations/hodram_B54_B60_editorial_release_v1.json','work/analysis/Hodram_B54_B60_release_seal_v8855/reference_seal.json','work/analysis/Hodram_B54_B60_release_seal_v8855/configuration_receipt.json','work/analysis/Hodram_B54_B60_wrong_memory_v8858/wrong_memory_rejections.json','work/analysis/Hodram_B56_FE_JSON_qualification_v8852/JSON_tuple_array_qualification.json']\n\nif __name__=='__main__':",
        'production_negative_count=846':'production_negative_count=886',
        'previous_status_turn_no_progress_revalidated=True':'previous_goal_turn_progress_verified_by_V8844=True',
        '82-fivegate-reviewed-policy-reconstruction-native-references-controls-loaders-pass-actual-comparison-atomic-registered-pending':'82-fivegate-reviewed-allnine-production-groups-pass-sealed-atomic-shared-live-semantic-registered-pending',
        "supersedes_only_pending_state_of='Hodram_SC1B54_B60_82_fivegate_reviewed_stored_actual_pending_production_registered_v8827'":"supersedes_only_pending_state_of='Hodram_SC1B54_B60_82_production_policy_reconstruction_native_references_controls_loaders_pending_actual_atomic_release_v8843'",
        "old['unfinished_editorial_scope_v8827']":"old['unfinished_editorial_scope_v8843']",
        'V8843-Hodram-B54-B60-six-production-groups-846-rejections':'V8861-Hodram-B54-B60-nine-production-groups-886-rejections-sealed',
        'editorial_Hodram_B54_B60_v8843.md':'editorial_Hodram_B54_B60_v8861.md',
        'V8843':'V8861',
        'B54-B60:six production groups pass;actual readers andregistered integration pending':'B54-B60:allnine production groups pass andsealed;atomic/shared tests live',
        'previous_goal_turn_was_status_only_no_progress_revalidated_andnew_production_evidence_completed=True':'previous_goal_turn_was_progress_verified_by_V8844_andnew_saved_evidence_readers_completed=True',
    })
    extra_checks="""    assert production['actual']['actual_summary']['whole_actual_frames']==130014 and production['actual']['actual_summary']['complete_actual_holds']==676 and production['actual']['actual_summary']['complete_actual_page_occurrences']==150
    assert production['actual']['actual_summary']['unique_speech_IDs']==63
    assert production['comparison']['comparison_summary']['later_full_RGB_pairs_recomputed']==335
    assert [g['matching_callbacks'] for g in production['comparison']['comparison_summary']['focused_prefix']]==[41,40]
    assert not production['comparison']['comparison_summary']['groups'][5]['whole_actors_equal'] and production['comparison']['comparison_summary']['groups'][6]['whole_actors_equal']
    assert production['FE_actual']['FE_actual_summary']['original_paint_contexts']==2 and production['FE_actual']['FE_actual_summary']['complete_same_run_FE_holds']==6
    conf=read('translations/hodram_B54_B60_editorial_release_v1.json');frozen=read('translations/hodram_B54_B60_native_contract_v1.json');prior=read('translations/hodram_B31_B53_editorial_release_v2.json')
    assert len(conf['dependencies'])==3562 and all(conf['dependencies'][p]==h for p,h in frozen['dependencies'].items()) and all(conf['dependencies'][p]==h for p,h in prior['dependencies'].items())
    from dk4tool.patch.hodram_B54_B60_editorial_v1 import check_dependencies
    check_dependencies(conf)
    wrong=read('work/analysis/Hodram_B54_B60_wrong_memory_v8858/wrong_memory_rejections.json');assert wrong['negative_count']==3 and wrong['no_digest_orsemantic_bypass'] and all(r['rejected'] and r['commit_calls']==0 for r in wrong['cases'])
"""
    auditor=derive('scripts/audit_Hodram_B54_B60_checkpoint_v8844.py','scripts/audit_Hodram_B54_B60_checkpoint_v8862.py',{
        'Hodram_B54_B60_checkpoint_v8843':'Hodram_B54_B60_checkpoint_v8861',
        'Hodram_SC1B54_B60_82_production_policy_reconstruction_native_references_controls_loaders_pending_actual_atomic_release_v8843':'Hodram_SC1B54_B60_82_allnine_production_groups_sealed_pending_atomic_registered_v8861',
        "SCOPE='unfinished_editorial_scope_v8843'":"SCOPE='unfinished_editorial_scope_v8861'",
        "{'policy','reconstruction','references','native','controls','loaders'}":"{'policy','reconstruction','references','native','controls','loaders','actual','comparison','FE_actual'}",
        "['policy','reconstruction','references','native','controls','loaders']]==[625,161,25,12,12,11]":"['policy','reconstruction','references','native','controls','loaders','actual','comparison','FE_actual']]==[625,161,25,12,12,11,16,16,8]",
        "pending['production_negative_count']==846":"pending['production_negative_count']==886",
        '    report=dict(six_production_groups_846_actual_changed_input_rejections_verified=True,':extra_checks+'    report=dict(nine_production_groups_886_actual_changed_input_rejections_sealed3562dependencies_and3wrongmemory_cases_verified=True,',
        'editorial_Hodram_B54_B60_v8843.md':'editorial_Hodram_B54_B60_v8861.md',
        'verified_handoff_v8844.json':'verified_handoff_v8862.json','V8843':'V8861',
    })
    root.mkdir(parents=True);save(root/'source_locked_checkpoint_tools.json',dict(producer=producer,auditor=auditor,full_historical_ledger_scope_anddocument_inverses_preserved=True,new_credit=0,full_goal_complete=False))
