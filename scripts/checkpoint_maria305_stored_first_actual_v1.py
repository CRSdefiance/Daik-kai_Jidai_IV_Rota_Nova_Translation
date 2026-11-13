"""Checkpoint stored proofs and first initialized capture without release credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT = Path('work/Maria_B176_B195_clean_20261110')


def main():
    release_path = Path('work/maria390_B152_B175_release_v1/registered_release_verification.json')
    release = load(release_path)
    reconstruction = load(ROOT/'reconstruction_v1/reconstruction.json')
    stored = load(ROOT/'stored_v1/stored_native_verification.json')
    catalogue = load(ROOT/'stored_catalogue_all_v1/all_stored_effective_body_bindings.json')
    loaders = load(ROOT/'loaders_v1/verification.json')
    terminal = load(ROOT/'display_run_menu0_v1/terminal.json')
    actual = load(ROOT/'display_pixels_menu0_v1/focused_actual_pixels.json')
    assert reconstruction['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    assert reconstruction['source_editorial_objects'] == 305
    assert stored['complete_stored_pages'] == 302
    assert stored['fresh_relocated_native_relative_cases'] == 170
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert catalogue['body_count'] == 294 and catalogue['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert (loaders['fresh_whole_archive_loads_andcache_hits'], loaders['fresh_parent_cases']) == (303, 606)
    assert terminal['terminal'] and terminal['frames'] == actual['frames'] == 28481
    assert (actual['selected_utterances'], actual['selected_pages']) == (73, 74)
    assert actual['all_complete_native_body_andheader_planes_andblank_guards_match']
    assert actual['all_selected_pages_observed_in_exact_fixture_order'] and actual['direct_visual_review_pending']
    assert not actual['complete_scene_commands_retained'] and not actual['natural_activation']
    evidence_paths = [release_path, Path(__file__), *[ROOT/p for p in [
        'reconstruction_v1/reconstruction.json', 'stored_v1/stored_native_verification.json',
        'stored_catalogue_all_v1/all_stored_effective_body_bindings.json', 'loaders_v1/verification.json',
        'display_selection_v1.json', 'display_fixtures_v1/fixtures.json',
        'display_run_menu0_v1/terminal.json', 'display_pixels_menu0_v1/focused_actual_pixels.json']]]
    ledger = load('translations/editorial_review_current_v1.json')
    old = ledger['Maria_SC3_B176_B195_clean_20261110']
    evidence = {**old['evidence'], **{str(p): digest(p) for p in evidence_paths}}
    summary = ('Maria305 B176–B195 passes mixed reconstruction and stored checks:302 pages,294 native effective lookups,'
        '170 relocated branch cases,303 loads and606 parent handoffs. The first initialized emulator run isterminal0:'
        '73 source bodies/74 ordered pages match complete body/header pixels. Direct visual/menu checks andtwo further'
        ' prepared runs remain;all fifth gates andregistered integration staypending. No worker islive. '
        'Integrated22,081,registered48c60d68,main andfull scope areunchanged.')
    document = 'docs/editorial_Maria305_B176_B195_stored_first_actual_20261110.md'
    text = f'''# Maria305 stored and first actual checkpoint — November 10, 2026

{summary}

Continue from [the complete offline checkpoint](editorial_Maria305_B176_B195_offline_20261110.md); retain its exact305 source/current references,205 revisions/100 justified retentions,27 scoped names,302 viewed compiled pages andall existing proof reuse. No new editorial credit orrelease iscreated here. All fifth gates remain false. The full goal remains active.

Under `work/Maria_B176_B195_clean_20261110`, `reconstruction_v1/reconstruction.json` binds all19 changed SC3 blocks,397 commands and34 relative sites. OnlySC3 changes;whole clean/current/block/archive/serialized-ROM inverses recover the registered parent exactly. The research ROM SHA256 is `{reconstruction['research_ROM_sha256']}`;it isnot a testing handoff orregistered candidate. All generated ROMs remain retained.

`stored_v1/stored_native_verification.json` verifies all305 source objects:272 ordinary bodies,22 physical style alternatives and11 captions. All302 stored pages equal the viewed compiled planes:148 parity-dependent pages arefresh and154 exact compiled proofs arereused. All170 native branch cases pass. The repaired FE panel survives storage without another padding amendment. `stored_catalogue_all_v1/all_stored_effective_body_bindings.json` checks all294 original pre-macro lookups with complete buffers/canaries/SP/unowned RAM. `loaders_v1/verification.json` checks303 whole native loads/cache hits and606 parent handoffs/first reads. Other routes areunchanged andnot replayed. These areoffline/native proofs,not original event activation.

`display_selection_v1.json` and `display_fixtures_v1/fixtures.json` prepare three focused initialized runs. Allretain the qualified full host setup/effects/cleanup andoriginal display commands;the sampled story sequences include fragments anddo not retain whole original scene control flow. The system-only unlock remains disclosed/not earned,withall six save slots preserved. No location,roster,money,RNG,event orRAM override isused. Historical worker4423 isterminal0 andmust not berestarted. Its28,481-frame menu0 run is `display_run_menu0_v1/terminal.json`;`display_pixels_menu0_v1/focused_actual_pixels.json` proves73 source bodies/74 pages inexact order,148 complete body and126 complete header planes,blank guards andnormal following nonfixture modal observation. Direct visual approval andactual menu-specific checks arestill pending. Source chronology,original location,event conditions,rewards,full-route andhardware arenot covered.

Next directly review those74 actual pages onlegible sheets andcheck menu intervals/returns. Run the already prepared `Maria305_letters_refusal_menu1_fixture.json` and `Maria305_armor_glyphs_menu2_fixture.json` sequentially through `scripts.run_maria_reviewed_display_v1.py`,using separate run/capture directories. Bind body/header/native/order checks,menu selections,FE andlong-page transitions,then seal allfive gates onlywhen necessary checks pass. Planned union127 bodies/135 pages isnot yet actual coverage. The remaining221 native bodies currently haveoffline proof only. Register the cumulative successor andexact clean-input patch before once-only305 credit. No new main promotion without acceptance.

Registered candidate remains Maria390 `{release['candidate_sha256']}` with719 entries/114 accepted layers/54 checks. Its Market Goods Info correction,ASCII right bounds,six-section ARM9,source25 v2 guard andinherited B164R99 correction remain preserved. The user's identified Rafael2952 November6 candidate has the known Market terminator defect;[the verified Market report](editorial_market_goods_info_fix_20261109.md) binds that exact build/screenshot/native reproduction andcorrected Local/Cargo gameplay. Latest registered Maria390 retains the fix;its ROM hash was rechecked this turn. No promotion,commit,push,cleanup orguide-photo collection occurred. Integrated22,081 andnative remainder3,817 (Maria2,012/Lil1,805) areunchanged;shared/player-facing inventories remain separate. Full editorial/name/wrap/glyph scope,early Rafael/tutorial priority,deferred artwork andlater older-record technical re-audit persist.
'''
    checkpoint(mutation=ROOT/'stored_first_actual_checkpoint_v1',
        batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Maria305:stored complete;first actual pixels pass;visual/menu/two runs/release pending.',
            current_batch_not_yet_integrated=True, current_batch_registered_andcredited_once=False,
            all_current_batch_fifth_gates_pending=True, native_job_live=False, native_sessions=[],
            stored_job_live=False, stored_sessions=[], registered_build_live=False,
            current_batch_evidence=evidence, next_action='Review first actual pages/menu andrun two prepared samples;then registered integration.', guide_photos=False),
        additional_updates={'Maria_SC3_B176_B195_clean_20261110':dict(new_credit=0,
            stored_checks_pending=False, stored_checks_complete=True, stored_body_pages=302,
            effective_native_body_lookups=294, relocated_branch_cases=170, native_loads=303, parent_handoffs=606,
            actual_batch_gameplay_records=73, actual_batch_gameplay_pages=74, actual_direct_visual_review_pending=True,
            actual_menu_checks_pending=True, remaining_prepared_actual_runs=2, all_fifth_gates_pending=True,
            registered_integration_pending=True, no_batch_worker_live=True, evidence=evidence, full_goal_complete=False)},
        summary=summary, document=document, document_text=text, completed=22081,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    save(ROOT/'stored_first_actual_checkpoint.json',dict(document=document,evidence=evidence,new_credit=0,
        no_batch_worker_live=True,all_fifth_gates_pending=True,registered_integration_pending=True,full_goal_complete=False))
    print('Stored andfirst actual checkpoint saved;73 bodies/74 pages,pending visual/menu/two runs;zero credit.')


if __name__ == '__main__':
    main()
