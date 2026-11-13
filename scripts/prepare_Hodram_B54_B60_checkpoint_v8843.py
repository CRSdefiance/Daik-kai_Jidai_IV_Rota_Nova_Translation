"""Prepare additive production progress and an independent preservation auditor."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

TEXT="""V8843 continues from verified V8827/current registered experimental cumulative V8778. The previous status-answer-only turn added no progress; this continuation completes six production validation groups for the pending82 Hodram SC1B54-B60 decisions. All four storylines, earlier translated dialogue, shared town/shop, random scenes, Help/remaining prose, retrospective premature breaks and all207 names/roles/aliases/customnames remain in scope. No completion credit, new ROM, registry change, promotion, separate user package, pruning, commit or push. Counts remain7,237 completed/7,240 credited source-prose anddrafts/4,492 integrated revisions/2,745 retentions. Preserve every earlier artifact and full unfinished-scope lead.

Metadata8829 adds explicit file/EV1/currentV8778/captain1 route binding in manuscriptv4; every approved record value and byte remains identical to five-gate manuscriptv3. Frozen policy8830 binds all82 individual prose/control/reference decisions,10 scoped progressive names and2,468 immutable dependencies. Production modules enforce exact input prose/bytes, full216px native wrapping, FE and progressive ownership, FI6/FA9/FO15 andsourceFI3/FA4/FO0,85 English pages,24 original QAinfos andzero warnings/errors/waivers without changing the global formatter, font or earlier layers.

Policy8831 reached its final count assertion with an incorrect expected646. Preserve the stopped producer, terminal exit1 and immutable partial80 positive compilers/542 negative cases. Qualification8834 proves the defined count625=82+7*66+16+60+5. Successor8831b reuses that exact partial and executes only2 missing compiler receipts/83 negative cases; all82 compilers/10 names/625 changed-input rejections now pass with all frozen guards active. The original failure remains. Native preparation8837 stopped on a simultaneous-replacement source-key mismatch after two modules were complete; qualified8837b verifies those exact completed outputs and generates only the missing validator. No compiler/native/capture producer is replayed to repair either bookkeeping failure.

Independent production reconstruction8833 binds all7 blocks,152 complete commands,82 six-byte preambles,24 relative sites,6 queries,33 nonprose controls,full four-byte ends,separate tails andclean/currentblock/archive/whole in-memory NDS inverses;all161 changed-input cases reject. References8836 reparses complete clean/current/target command inventories andall82 source/current/final references,including FE/macros/two-page/final-block challenges;25 defects reject. Whole reviewed reference image equality andevery318 unownedblock/otherfile/component/inverse pass without mutating the parent object.

Native8838 independently checks all167 complete source/stored pages:165 progressive pages and2 original FE logical/physical pages,plus10 source-qualified progressive nameplanes. It preserves complete first/internal/final glyphs,original palette indices,216/228 widths,bounds,consumption andthree English two-page records. Twelve changed semantic inputs reject. Pure progressive CPU results are cached within the process only by full exact ARM9/font/body/adapter inputs;each supplied model,plane,metadata andfrozen dependency guard is rechecked on every call,including hits. This cache supplies no gameplay credit andchanges no runtime or historical module.

Controls8840 independently binds82 original final dispatches andvoices,FE null actor/default macros,120 native relative cases/24 sites,6 unforced rawqueries,33 paired structural opaque decodes,175 seeded full normal ends,50 original separate result-channel fragments and13 EV1 getters;12 defects reject. Loaders8842 binds325 complete native loads/cachehits,326 actions and650 parent cases,with14 fresh cases and636 exact prior cases. Every reused case requires exact complete predecessor/runtime/payload andcase equality. The shipped native caller census is independently recomputed;11 defects reject. These are offline production CPU/artifact checks,not new emulator runs or expanded event/plot/effect claims.

Allsix validation groups pass846 total changed-input rejections. The existing14 terminal/reaped initialized-scene runs/130,014frames/676holds/63 unique observed utterances/19 offline-only utterances are reused;no recapture. Retain every main/focused duration,decoded-length,RNG,RGB,following-command andlongB60 actor difference. The7001-frame focused interval agrees onfive components/actors/captain/calendar butstill differs in RNG/11 laterRGBpairs;no immediate-return mainRAM,causal diagnosis,future-equivalence,natural optional activation,earned chronology,fullroute orhardware claim.

Next:adapt andvalidate the production saved-capture/fixture reader for all12 main runs,FE andmultipage behavior plus2 focused runs;independently bind comparisons andall measured limits. Then seal all current/prior release dependencies,verify one whole-NDS atomic commit in both supported lifecycles andshared registered hook,build registered cumulative candidate/exact reconstructable clean-input patch/checks/ownstartup,andcredit82 once only. Reuse all completed source/editorial/native/storage/reference/loader/gameplay checks. CurrentV8778/647 manifestbatches/114 acceptedlayers/18 releasechecks/110 regressions/exactpatch/ownstartup andMainV4701/canonical baseline remain unchanged.

The Geronimo/Alonso sharedデ full-name field,all207/fullcatalogue/customnames andwider role contexts remain open. Preserve Rafael,Hodram,Joakim,Maria,Camille andcurrent mixed-width storage. Every prior unfinished-scope key/value andlead is retained by whole-ledger/scope inverse anddocument suffix checks. Graphics/all18 plaques andthe later older-record technical re-audit remain separate. Roughly20,000 remaining is a planning estimate,not an audited denominator. The full goal remains active andincomplete.
"""
PRODUCTION={
 'policy':'work/analysis/Hodram_B54_B60_policy_validation_v8831b/policy_validation.json',
 'reconstruction':'work/analysis/Hodram_B54_B60_reconstruction_validation_v8833/independent_reconstruction_validation.json',
 'references':'work/analysis/Hodram_B54_B60_reference_validation_v8836/independent_reference_validation.json',
 'native':'work/analysis/Hodram_B54_B60_native_validation_v8838/independent_native_validation.json',
 'controls':'work/analysis/Hodram_B54_B60_controls_validation_v8840/independent_controls_validation.json',
 'loaders':'work/analysis/Hodram_B54_B60_loader_validation_v8842/independent_loader_validation.json',
}
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_checkpoint_tools_v8843');assert not root.exists()
    source=Path('scripts/checkpoint_Hodram_B54_B60_v8827.py').read_text(encoding='utf-8')
    node=next(n for n in ast.parse(source).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TEXT' for t in n.targets))
    old_text=ast.get_source_segment(source,node.value)
    producer=derive('scripts/checkpoint_Hodram_B54_B60_v8827.py','scripts/checkpoint_Hodram_B54_B60_v8843.py',{
        'Hodram_B54_B60_checkpoint_v8827':'Hodram_B54_B60_checkpoint_v8843',
        'Hodram_SC1B54_B60_82_fivegate_reviewed_stored_actual_pending_production_registered_v8827':'Hodram_SC1B54_B60_82_production_policy_reconstruction_native_references_controls_loaders_pending_actual_atomic_release_v8843',
        "SCOPE='unfinished_editorial_scope_v8827'":"SCOPE='unfinished_editorial_scope_v8843'",
        'translations/hodram_B54_B60_editorial_manuscript_v3.json':'translations/hodram_B54_B60_editorial_manuscript_v4.json',
        old_text:repr(TEXT),
        "if __name__=='__main__':":"PRODUCTION="+repr(PRODUCTION)+"\nEVIDENCE += list(PRODUCTION.values()) + ['translations/hodram_B54_B60_native_contract_v1.json','work/analysis/Hodram_B54_B60_metadata_v8829/explicit_route_binding.json','work/analysis/Hodram_B54_B60_policy_count_v8834/terminal_failure_and_count_qualification.json','work/analysis/Hodram_B54_B60_native_tools_v8837b/source_locked_native_evidence.json']\n\nif __name__=='__main__':",
        "pending=dict(status='82-fivegate-reviewed-production-atomic-registered-cleanpatch-startup-andonceonly-credit-pending',":"pending=dict(status='82-fivegate-reviewed-policy-reconstruction-native-references-controls-loaders-pass-actual-comparison-atomic-registered-pending',production_proofs=PRODUCTION,production_negative_count=846,previous_status_turn_no_progress_revalidated=True,",
        "supersedes_only_pending_state_of='Hodram_SC1B54_B60_82_contextual_prose_native_display_pending_storage_actual_release_v8806'":"supersedes_only_pending_state_of='Hodram_SC1B54_B60_82_fivegate_reviewed_stored_actual_pending_production_registered_v8827'",
        "old['unfinished_editorial_scope_v8806']":"old['unfinished_editorial_scope_v8827']",
        "id='V8827-Hodram-B54-B60-82-fivegates-stored-actual'":"id='V8843-Hodram-B54-B60-six-production-groups-846-rejections'",
        'editorial_Hodram_B54_B60_v8827.md':'editorial_Hodram_B54_B60_v8843.md',
        'V8827':'V8843',
        'B54-B60:82 five-gate reviews/storage/actual pass;production andregisteredintegration pending':'B54-B60:six production groups pass;actual readers andregistered integration pending',
        'previous_goal_turn_was_progress_verified_by_V8807=True':'previous_goal_turn_was_status_only_no_progress_revalidated_andnew_production_evidence_completed=True',
    })
    checks="""    production={k:read(p) for k,p in pending['production_proofs'].items()}
    assert set(production)=={'policy','reconstruction','references','native','controls','loaders'}
    assert [production[k]['negative_count'] for k in ['policy','reconstruction','references','native','controls','loaders']]==[625,161,25,12,12,11]
    assert sum(p['negative_count'] for p in production.values())==pending['production_negative_count']==846
    assert len(production['policy']['positive_speech_compilers'])==82 and production['policy']['reused_positive_compilers']==80 and production['policy']['fresh_positive_compilers']==2
    assert production['policy']['reused_negative_cases']==542 and production['policy']['fresh_negative_cases']==83
    assert len(production['reconstruction']['positive_blocks'])==7 and production['reconstruction']['positive_complete_archive_andwhole_NDS']
    assert production['references']['reference_summary']['editorial_references']==82 and production['references']['reference_summary']['commands']==152
    assert production['native']['native_summary']['native_body_pages_recomputed']==167 and production['native']['native_summary']['scoped_style11_nameplanes_recomputed']==10
    assert [production['controls']['native_control_summary'][k] for k in ['independent_final_dispatches','relative_sites','native_relative_cases','raw_query_cases','original_EV1_entries','opaque_structural_decode_pairs','normal_seeded_ends','original_result_channel_cases']]==[82,24,120,6,13,33,175,50]
    assert [production['loaders']['loader_summary'][k] for k in ['native_whole_loads_cache_hits_bound','initial_parent_modes_bound','fresh_parent_cases','exact_reused_parent_cases','original_EV1_actions_bound']]==[325,650,14,636,326]
    for p in production.values():
        assert not p['new_credit'] and not p['full_goal_complete']
        assert all(c['actual_changed_input'] and c['rejected'] and c['diagnostic'] for c in p['negative_cases'])
    from dk4tool.dialogue.hodram_B54_B60_profile_v1 import validate_approved_batch
    validate_approved_batch(doc)
"""
    auditor=derive('scripts/audit_Hodram_B54_B60_checkpoint_v8828.py','scripts/audit_Hodram_B54_B60_checkpoint_v8844.py',{
        'Hodram_B54_B60_checkpoint_v8827':'Hodram_B54_B60_checkpoint_v8843',
        'Hodram_SC1B54_B60_82_fivegate_reviewed_stored_actual_pending_production_registered_v8827':'Hodram_SC1B54_B60_82_production_policy_reconstruction_native_references_controls_loaders_pending_actual_atomic_release_v8843',
        "SCOPE='unfinished_editorial_scope_v8827'":"SCOPE='unfinished_editorial_scope_v8843'",
        "    report=dict(stage_manifest_sha256=":checks+"    report=dict(six_production_groups_846_actual_changed_input_rejections_verified=True,stage_manifest_sha256=",
        'editorial_Hodram_B54_B60_v8827.md':'editorial_Hodram_B54_B60_v8843.md',
        'verified_handoff_v8828.json':'verified_handoff_v8844.json','V8827':'V8843',
    })
    root.mkdir(parents=True);save(root/'source_locked_checkpoint_tools.json',dict(producer=producer,auditor=auditor,new_credit=0,full_goal_complete=False))
