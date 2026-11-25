"""Preserve partial Lil display evidence and hand off the tested cumulative ROM."""
import ast
import gzip
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT = Path('work/Lil269_B243_B282_clean_20261110')
ARCHIVE = Path('translations/editorial_checkpoints/Lil269_display_partial_20261110_v2')
PACKAGE = Path('releases/all_routes_promotion_20261110_v2')


def main():
    assert not ARCHIVE.exists()
    release = load('work/lil382_residual_A_release_v1/registered_release_verification.json')
    receipt = load(PACKAGE / 'verification/promotion_v2_reconstruction.json')
    assert receipt['exact_registered_candidate_reconstructed_from_clean_input']
    assert receipt['fresh_repository_tests'] == 27 and receipt['pending_Lil269_excluded']
    assert digest(receipt['candidate']) == release['candidate_sha256']
    for n, h in load(PACKAGE / 'checksums.json').items():
        assert digest(PACKAGE / n) == h
    prose = Path('translations/lil_B243_B282_contextual_review_v3.json')
    names = Path('translations/lil_B243_B282_scoped_names_v3.json')
    doc = load(prose)
    assert (doc['source_objects'], doc['proposed_revisions'], doc['justified_retentions']) == (269, 104, 165)
    assert all(r['review'] == dict(source=True, context=True, localization=True,
        naturalness=True, formatting=False) for r in doc['records'] + load(names)['records'])
    plan = load(ROOT / 'plan_v4/automatic_plans.json')
    assert len(plan['records']) == 262 and not plan['failures']
    assert sum(r['expected_native_pages'] for r in plan['records']) == 264
    assert not [x for x in load(ROOT / 'plan_v4/diagnostics.json')['issues'] if x['severity'] in ['warning', 'error']]
    completed = sorted((ROOT / 'native_body_v1').glob('complete_*.json'))
    assert len(completed) == 56
    ids = {load(p)['record']['id'] for p in completed}
    assert all(load(p)['all_original_native_glyph_pixels_consumption_canaries_bounds_androw_assertions_pass'] for p in completed)
    remaining = [r['id'] for r in plan['records'] if r['id'] not in ids]
    assert remaining[0] == 'DK4_MES_B251_R0009'
    sheets = [ROOT / p for p in [
        'menu_native_v1/B250_C470/native_caption_review.png',
        'menu_native_v1/B251_C270/native_caption_review_1.png',
        'menu_native_v1/B251_C1752/native_caption_review.png',
        'name_planes_v1/names_part1.png', 'name_planes_v1/names_part2.png']]
    save(ROOT / 'mixed_visual_review_v2.json', dict(
        directly_viewed_sheets={str(p): digest(p) for p in sheets},
        all_seven_reviewed_caption_strings_and24_name_strings_readable=True,
        reviewed_captions_centered_complete_no_visible_glyph_anomalies=True,
        name_strings_complete_andconsistent_native_font=True,
        scope='Offline menu/name planes only; no body-page, stored, gameplay or full catalogue UI approval.',
        all_fifth_gates_pending=True, new_credit=0))
    save(ROOT / 'partial_native_status_v2.json', dict(
        completed_native_records=56, completed_native_pages=sum(r['expected_native_pages'] for r in plan['records'] if r['id'] in ids),
        completed_receipts={str(p): digest(p) for p in completed}, remaining_native_record_ids=remaining,
        first_missing_planned_record=remaining[0],
        earlier_native_worker_terminal_exit_code=1,
        earlier_tool_failure='Rafael_B45_FE_source_painter_v7894.paint complete-consumption/string-canary assertion',
        failure_cause_not_yet_diagnosed=True, do_not_waive_native_consumption_guard=True,
        no_body_visual_completion_claim=True, reuse_completed_receipts_when_exact_dependencies_match=True,
        pending_batch_excluded_from_promotion_ROM=True, new_credit=0))
    ARCHIVE.mkdir(parents=True)
    artifacts = {}
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or p.suffix not in ['.json', '.txt']:
            continue
        dest = (ARCHIVE / p.relative_to(ROOT)).with_suffix(p.suffix + '.gz')
        dest.parent.mkdir(parents=True, exist_ok=True)
        raw = p.read_bytes()
        dest.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
        assert gzip.decompress(dest.read_bytes()) == raw
        artifacts[str(p)] = dict(archive=str(dest), source_sha256=digest(p), archive_sha256=digest(dest))
    producers = [Path(__file__), Path('scripts/prepare_promotion_candidate_20261110_v2.py'),
        Path('scripts/prepare_promotion_candidate_20261110_v3.py'),
        Path('scripts/check_editorial_three_choice_explicit_route_v1.py'),
        Path('scripts/check_scoped_clean_menus_v4.py'), Path('scripts/refresh_reviewed_formatting_prose_v1.py')]
    for p in producers:
        ast.parse(p.read_bytes(), filename=str(p))
    archive = ARCHIVE / 'archive_manifest.json'
    save(archive, dict(artifacts=artifacts, producers={str(p): digest(p) for p in producers},
        all_selected_artifacts_lossless=True, prior_archive_preserved=True,
        raw_ROM_RAM_planes_andcaptures_preserved_locally=True, new_credit=0,
        incomplete_batch_not_shipped=True, full_goal_complete=False))
    protected = {'translations/release_stack.json': release['registry_sha256'],
        release['candidate']: release['candidate_sha256'], release['manifest']: release['manifest_sha256'],
        'out/raphael_natural_v2_accepted_base.nds': release['canonical_sha256'],
        'work/clean.nds': release['clean_input_sha256'],
        'translations/promoted_build.json': digest('translations/promoted_build.json')}
    summary = ('Fresh cumulative promotion candidate prepared from the exact clean-input patch: '
        '726 entries, 114 accepted layers, 61 release checks and 27 fresh repository tests pass. '
        'ROM remains byte-identical to registered Lil382; 24,475 integrated. '
        'Pending Lil269 now has a zero-warning 262-body/264-page plan, 56 completed native body receipts, '
        'passing style/menu/name checks and directly viewed menu/name sheets. The B251 FE complete-consumption '
        'failure remains unresolved; body visual/storage/gameplay/release gates stay pending. '
        'Pending work is preserved and excluded from the ROM. No new credit, main promotion or new gameplay claim; full goal active.')
    document = Path('docs/editorial_promotion_candidate_20261110_v2.md')
    text = f'''# Cumulative promotion candidate and saved editorial checkpoint — November 10, 2026

{summary}

Use [Translation_DS_All_Routes_20261110_v2_candidate.nds](../{Path(receipt['candidate']).as_posix()}) with its adjacent manifest. SHA-256: `{release['candidate_sha256']}`. [Standalone clean-input patch and release notes](../{PACKAGE.as_posix()}/README.md). This is a fresh reconstruction of the latest registered release, with no new internal ROM changes. All earlier accepted work is preserved, including Rafael/tutorial localization, Market Trade-screen correction, names and ASCII right bounds. The exact canonical baseline covers all 114 baked accepted layers. The initial packaging guard incorrectly expected them to be repeated in the explicit batch list; the versioned successor checks their registered baked status and exact baseline hash instead. A junction write boundary required an authorized rerun before output creation. Failed producers remain preserved.

All 27 fresh repository tests pass with exit 0; the XML report is packaged. All 61 original release checks remain bound to these exact bytes. Existing cold-boot, protected-name and representative-content proofs are reused. This step adds no gameplay or hardware coverage. See [the Lil382 checkpoint](editorial_Lil382_registered_20261110.md) for observed versus offline-only content and unvisited conditions. Cold-boot the exact new filename and test title/New Game, Rafael/tutorial, town/Market Trade, names, wraps and transitions. Main remains V4701 pending explicit user acceptance.

Resume unfinished Lil269 from `translations/lil_B243_B282_contextual_review_v3.json` and scoped-names v3: 104 revisions, 165 individually justified retentions, 25 names, first four gates true and every fifth gate false. Two older-voice styles use “the ceiling's collapsing” for the same source meaning and escape advice. Formatting v2 preserves the 20 exact macro preflights and controls. Plan v4 has 262 bodies/264 pages, zero errors/warnings/failures; one figurehead page is reclaimed without cutting prose, while expedition/escape clauses remain coherent across two-page boundaries. Earlier failed plans remain preserved.

There are 56 completed native body receipts, including B251R6; reuse exact compatible receipts instead of restarting B243. The first missing planned record is B251R9, the FE ice riddle. The worker terminated at the native painter's complete-consumption/string-canary assertion. Its cause is undiagnosed; do not waive the guard or claim all body pages pass. Two style objects/16 alternatives, three menus/seven captions and 24 distinct name strings pass native checks. All five menu/name sheets were directly viewed: reviewed captions are centered and strings readable with consistent glyphs. These are offline string/plane checks, not stored integration, full catalogue UI or actual event coverage. Body visual review, storage, representative gameplay and registration remain pending. No worker is live.

[Lossless partial-display archive](../{archive.as_posix()}) preserves all source/current bindings, prose, plans, completed journals, failure status and checks. The prior prose archive, earlier translations/retentions, ROMs and evidence are preserved. No pending proposal is shipped or credited. The 269 objects remain inside Lil's 1,423 remaining native positions; integrated count stays 24,475. Every unfinished storyline/contextual pass, shared/shop/town/random exchange, player-facing text and broader name review remains in scope. Keep early Rafael/tutorial priorities, no guide photos, deferred graphics artwork and the later older-record technical re-audit separate. The full goal remains active.
'''
    evidence = {str(p): digest(p) for p in [prose, names, archive,
        PACKAGE / 'verification/promotion_v2_reconstruction.json', ROOT / 'partial_native_status_v2.json', ROOT / 'mixed_visual_review_v2.json']}
    checkpoint(mutation=ROOT / 'promotion_display_checkpoint_v2', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Lil269 partial native display; FE consumption failure pending.',
            current_batch_not_yet_integrated=True, current_batch_registered_andcredited_once=False,
            all_current_batch_fifth_gates_pending=True, current_batch_evidence=evidence,
            no_batch_worker_live=True, guide_photos=False,
            next_action='Diagnose B251 FE complete consumption; reuse56 exact completed receipts and finish remaining display/storage/gameplay gates.'),
        additional_updates={'Lil_SC2_B243_B282_clean_20261110': dict(new_credit=0,
            provisional_bodies=262, provisional_pages=264, unresolved_plan_warnings=0,
            completed_native_body_receipts=56, native_rendering_pending=True,
            direct_visual_review_pending=True, menus_andname_sheets_directly_viewed=True,
            stored_checks_pending=True, gameplay_pending=True, registered_integration_pending=True,
            all_fifth_gates_pending=True, no_batch_worker_live=True, evidence=evidence)},
        summary=summary, document=document, document_text=text, completed=24475, protected=protected)
    for p, v in artifacts.items():
        assert digest(p) == v['source_sha256']
    print('PASS: promotion handoff and partial Lil269 evidence preserved; zero credit and main unchanged.')


if __name__ == '__main__':
    main()
