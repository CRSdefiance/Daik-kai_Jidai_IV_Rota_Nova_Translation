"""Publish the verified310-record cumulative release and exact remaining-source checkpoint."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint

ROOT=Path('work/maria310_release_v1')
RESEARCH=Path('work/Maria_B51_B57_clean_20261109')

def main():
    release_path=ROOT/'registered_release_verification.json';release=load(release_path)
    done_path=ROOT/'completion_checkpoint.json';done=load(done_path)
    census_path=Path('work/story_source_coverage_20261109_SC3_v5/coverage.json');census=load(census_path)
    actual_path=RESEARCH/'gameplay_review_v1.json';actual=load(actual_path)
    ready_path=RESEARCH/'research_final_v1/research_completion.json';ready=load(ready_path)
    assert done['new_credit']==310 and done['counts']==dict(completed=20058,revised=12064,retained=7994)
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(713,114,48)
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert release['registered_market_format_andboth_data_pointers_preserved'] and release['source_bound_FE_storage_alignment_andall318_compiled_pages_preserved']
    assert len(census['records'])==5129 and len(census['missing'])==4035
    assert not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    assert (actual['distinct_source_utterances'],actual['distinct_body_pages'],actual['offline_only_source_utterances'])==(64,70,246)
    assert ready['all_individual_five_gates_pass'] and ready['records']==310
    assert digest('translations/release_stack.json')==release['registry_sha256']
    registry=load('translations/release_stack.json');prior=load(ROOT/'release_stack_before_Maria310.json')
    assert registry['latest_promoted_build']==prior['latest_promoted_build'] and registry['accepted_layers']==prior['accepted_layers']
    assert all(registry['profiles'][k]==v for k,v in prior['profiles'].items())
    packet=load(census_path.with_name('residual_clean_source_packet.json'))
    next_groups=[(g['block'],len(g['records'])) for g in packet['groups'][:10]]
    next_root=Path('work/Maria_B58_B70_clean_20261109')
    next_packet=load(next_root/'clean_source_packet.json');next_selection=load(next_root/'source_selection_v1.json')
    assert next_packet['source_only_not_current_English'] and next_packet['records']==next_selection['source_objects']==303
    assert [(g['block'],len(g['records'])) for g in next_packet['groups']]==next_groups
    assert next_selection['no_current_English_read_orapproval'] and next_selection['no_meanings_drafts_orlocalization_approval_yet']
    testing=ROOT/'testing_handoff.md';assert not testing.exists()
    testing.write_text(f'''# Translation DS cumulative test candidate

[ROM](all_routes_maria310_candidate.nds) · [clean-input patch](all_routes_maria310_candidate.xdelta) · [manifest](all_routes_maria310_candidate.manifest.json)

SHA-256 `{release['candidate_sha256']}`. Includes the registered Trade/Goods Info correction and 310 more contextual Maria reviews. Main is unchanged. Use a copy of your existing save with the matching ROM basename; preserve the original save.

Native and representative emulator checks, exact clean-input reconstruction and own startup pass. Original late-event conditions and hardware remain unvisited. [Review and evidence](../../docs/editorial_Maria310_registered_20261109.md).
''',encoding='utf-8',newline='\n')
    summary=('Maria310 is registered and credited once: 184 revisions/126 justified retentions, 15 wrap improvements, five FE row repairs, '
        'three mixed-width letters and one source-bound FE storage fix. All 318 approved pages are preserved; 64 utterances/70 pages '
        'are observed in representative emulator QA. The cumulative 713-entry/114-layer candidate passes 48 checks, exact clean-input '
        'reconstruction, own startup and 24 protected getters. Integrated 20,058; 5,840 native story objects remain. '
        'Next ten exchanges have 303 clean-only objects selected; meanings, drafts and all gates remain pending. Main and full scope unchanged.')
    text=f'''# Maria310 registered checkpoint — November 9, 2026

**310 source reviews are integrated and credited once: 184 revisions and 126 justified retentions.** All five individual gates pass. Fifteen wrap improvements, five FE row repairs, three mixed-width letter corrections and one storage-padding fix preserve all 318 approved pages. The 26 scoped name reviews do not claim completion of the wider name/role review.

Registered cumulative candidate: [all_routes_maria310_candidate.nds](../work/maria310_release_v1/all_routes_maria310_candidate.nds), SHA-256 `{release['candidate_sha256']}`. [Clean-input patch](../work/maria310_release_v1/all_routes_maria310_candidate.xdelta), SHA-256 `{release['patch_sha256']}`, reconstructs that exact ROM from clean `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`. The manifest retains all 712 predecessor entries and 114 accepted layers, adding one reviewed transaction and passing 48 release checks. Its own 31,000-frame Maria/Hangzhou startup, RAM identity and both original getters for 12 protected actors pass. No main promotion or Git push occurred.

Under `work/Maria_B51_B57_clean_20261109`, reuse [the stored checkpoint](editorial_Maria310_stored_20261109.md), `research_final_v1/research_completion.json` and `gameplay_review_v1.json`. The source/prose decisions, all 318 page approvals, 31 name strings, 1,240 selected alignment cases, complete block/archive/ROM inverses, 660 branch cases, all 310 catalogue bodies and 303 loads/606 handoffs remain bound to exact evidence. No completed native inventory was replayed.

Two emulator runs observe **64 utterances/70 pages**: all six distinct two-page layouts, five repaired FE panels, the B54 R507 full panel and ordinary A return without a blank panel, inline Bianca/Angelo voices, FE/named transitions and normal I/F glyphs. All selected pages were directly viewed on six readable sheets; the complete original captures remain. Both hosts reach resupply/departure/sailing. The other 246 bodies remain offline-only. The two B52 town alternatives are conditional display cases, not naturally consecutive events. Existing isolated system unlock is disclosed, not earned. Original story conditions/effects/outcomes, full catalogue UI, full routes and hardware are unvisited. No guide photos.

The registered transaction freshly executes `dk4tool/patch/maria310_release_v1.py`, including the exact owned B54 R507 storage amendment after ordinary reconstruction. It removes the unconsumed parity space and one redundant NUL alignment byte while preserving the compiled paragraph, native control, 318 page pixels and command count. All subsequent offsets, catalogue indices, branches and complete inverses are checked. Four ownership negatives and eight production-scope negatives pass. The original failed ROM, checks and diagnostic alternatives remain preserved. Market pointers/read-only allocation, six-section ARM9, ASCII right-bound repair, source25 guard, earlier translations and all other files/components remain exact.

`translations/maria310_integrated_final_review_v1.json` and `work/maria310_release_v1/exact_integrated_record_bindings.json` bind every clean/current/final reference, finding, revision or retention and review gate. `completion_checkpoint.json` proves once-only credit and preservation of all earlier ledger keys/prefixes. `work/story_source_coverage_20261109_SC3_v5/coverage.json` rechecks all 5,129 original SC3 positions using the existing native inventory: **1,094 covered / 4,035 remaining**, with zero duplicate or unresolved legacy bindings.

Integrated totals are **20,058 = 12,064 revisions + 7,994 retentions**. The historical meaning/prose/draft count remains three higher at 20,061. Remaining native story objects: **5,840 (Lil 1,805 / Maria 4,035)**; shared shop/town/random/UI and other prose remain separately tracked. Main, canonical inputs, all ROMs, prior profiles, translations, drafts, retentions and evidence are preserved. Full unfinished editorial scope remains active, including earlier contextual passes and names. Deferred graphics artwork and the later older-record technical re-audit remain separate.

**Next: 303 clean-only objects are selected in ten complete exchanges** under `work/Maria_B58_B70_clean_20261109/clean_source_packet.json`. Block/count pairs: `{next_groups}`. Their exact source positions and disjoint coverage are checked; no current English, meanings, drafts or approvals are claimed yet. Use `source_selection_v1.json` and preserve source-first meaning/draft order, individual findings and retentions, automatic full-width wrapping and native glyph/control checks. Reuse matching proofs and test changed behavior or concrete risks. Integrate passing batches through this registered successor, including the exact FE storage amendment and market fix. No process is live at this checkpoint.
'''
    evidence={str(p):digest(p) for p in [release_path,done_path,census_path,actual_path,ready_path,testing,
        next_root/'clean_source_packet.json',next_root/'source_selection_v1.json',Path(__file__)]}
    checkpoint(mutation=ROOT/'registered_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria310 registered;next303 clean objects in ten complete exchanges selected.',
            current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=True,proposed_revisions=0,justified_retentions=0,
            native_job_live=False,registered_build_live=False,guide_photos=False,
            next_action='Continue the next substantial disjoint clean-exchange batch from the SC3_v5 residual packet.'),
        additional_updates={'Maria_SC3_B51_B57_clean_20261109':dict(
            all_fifth_formatting_gates_pending=False,stored_andrepresentative_checks_pending=False,
            representative_gameplay_andregistered_integration_pending=False,registered_integration_pending=False,
            current_batch_actual_gameplay_observations=64,current_batch_actual_gameplay_pages=70,
            final_cumulative_integration_complete=True,registered_checkpoint_evidence=evidence),
            'Maria_SC3_B58_B70_clean_20261109':dict(new_credit=0,source_objects=303,complete_exchanges=10,
                source_packet=str(next_root/'clean_source_packet.json'),source_packet_sha256=digest(next_root/'clean_source_packet.json'),
                all_exact_clean_positions_checked=True,source_only_no_current_English_read=True,
                meanings_drafts_contextual_comparisons_andall_five_gates_pending=True,
                native_inventory_compatible_proof_reused_not_replayed=True,actual_gameplay_observations=0,
                registered_integration_pending=True,guide_photos=False)},
        summary=summary,document='docs/editorial_Maria310_registered_20261109.md',document_text=text,completed=20058,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    print('Published Maria310 registered checkpoint;20,058 integrated;5,840 native story objects remain;full scope active.')

if __name__=='__main__':main()
