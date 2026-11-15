"""Record all remaining Lil display and storage checks before gameplay approval."""

import gzip
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_lil261_prose_v1 import ARCHIVE as PROSE_ARCHIVE, RELEASE
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_lil261_prose_layout_v1 import NAMES, PROSE, ROOT
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint


ARCHIVE = Path('translations/editorial_checkpoints/Lil261_stored_20261110_v1')
PLAN = ROOT / 'plan_v7/automatic_plans.json'
APPROVAL = ROOT / 'offline_display_approval_v1.json'
STORED = ROOT / 'stored_v1/stored_native_verification.json'
CATALOGUE = ROOT / 'stored_catalogue_all_v1/all_stored_effective_body_bindings.json'
LOADERS = ROOT / 'loaders_v1/verification.json'


def main():
    assert not ARCHIVE.exists()
    approved, stored, catalogue, loaders, plan = map(load, (APPROVAL, STORED, CATALOGUE, LOADERS, PLAN))
    assert (approved['source_objects'], approved['physical_body_candidates'], approved['body_pages']) == (261, 255, 258)
    assert approved['all_final_body_pages_directly_viewed'] and approved['all_names_andcaptions_directly_viewed']
    assert approved['all_fifth_formatting_gates_still_pending'] and not approved['actual_gameplay']
    assert stored['complete_stored_pages'] == 258 and stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert catalogue['body_count'] == 255 and catalogue['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert (loaders['whole_archive_loads_andcache_hits'], loaders['parent_cases']) == (336, 672)
    first = load(ROOT / 'plan_v1/automatic_plans.json')['records']
    delta = []
    for before, after in zip(first, plan['records'], strict=True):
        assert (before['id'], before['English'], before['expected_native_pages']) == (
            after['id'], after['English'], after['expected_native_pages'])
        if before['encoded_hex'] != after['encoded_hex']:
            delta.append(dict(id=after['id'], before=before['lines'], after=after['lines']))
    assert len(delta) == 30
    delta_path = ROOT / 'final_layout_delta_v1.json'
    assert not delta_path.exists()
    save(delta_path, dict(changes=delta, changed_records=len(delta), no_prose_or_page_count_changed=True,
        plan_sha256=digest(PLAN), rejected_preferences={
            'DK4_MES_B335_R0125': 'The three-line regrouping left the preposition with at a line end. Retain the original three readable rows.',
            'DK4_MES_B335_R0132': 'Keep passed away together and retain the original flow into the villager’s reverent description.',
        }))
    assert load(ROOT / 'display_selection_v1.json')['body_pages'] == 61
    prior = PROSE_ARCHIVE / 'archive_manifest.json'
    paths = [APPROVAL, STORED, CATALOGUE, LOADERS, PLAN, delta_path,
        ROOT / 'reconstruction_v1/reconstruction.json', ROOT / 'final_native_v1.json',
        ROOT / 'body_visual_review_v1.json', ROOT / 'menu_native_approved_v1.json',
        ROOT / 'compiled_styles_v2/compiled_style_objects.json', ROOT / 'display_selection_v1.json',
        ROOT / 'display_fixtures_v1/Lil261_fog_cave_commission_alchemy_fixture.json',
        ROOT / 'actual_run0_v1/run_plan.json',
        ROOT / 'native_final_selection_v1/resume_selection.json', ROOT / 'body_visual_original_v1.json',
        ROOT / 'body_visual_refined_v1.json', ROOT / 'body_visual_last_v1.json',
        *ROOT.glob('plan_v[567]/*.json'), *ROOT.glob('formatting_v1/phrase_and_page_preferences_v[45].json'),
        ROOT / 'formatting_v1/phrase_and_page_preferences_final_v6.json']
    artifacts = {}
    for path in paths:
        raw = path.read_bytes()
        packed = (ARCHIVE / path.relative_to(ROOT)).with_suffix('.json.gz')
        packed.parent.mkdir(parents=True, exist_ok=True)
        packed.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
        assert gzip.decompress(packed.read_bytes()) == raw
        artifacts[path.as_posix()] = dict(archive=packed.as_posix(), source_sha256=digest(path), archive_sha256=digest(packed))
    archive = ARCHIVE / 'archive_manifest.json'
    save(archive, dict(artifacts=artifacts, prior_prose_archive=prior.as_posix(), prior_prose_archive_sha256=digest(prior),
        source_objects=261, native_pages=258, offline_and_stored_pass=True,
        gameplay_approval_pending=True, new_credit=0, full_goal_complete=False))
    release = load(RELEASE)
    evidence = {str(p): digest(p) for p in (archive, APPROVAL, STORED, CATALOGUE, LOADERS, PLAN)}
    summary = ('Lil B323–B335 passed offline visual review of all 258 dialogue pages, six captions and 12 name strings. '
        'All 13 exchanges passed stored reconstruction, native catalogue lookups and the original SC2 loaders. '
        'The final plan improves 30 layouts. Focused gameplay and cumulative registration remain. The ledger credits 25,637 reviews.')
    notes = f"""# Lil B323–B335 display and storage checkpoint

{summary}

All 198 revisions, 63 justified retentions and nine scoped name decisions remain bound to the clean source and Lil254. The 255 bodies pass four native alignments each. The final 30 layout changes keep phrases such as “catch on” and “survey party” together, and place the three page turns at complete thoughts. The two rejected trials in the monk exchange would have left a weak line ending or split “passed away.” The approved plan uses the readable original rows for those two lines. All 13 system alerts pass. [Dialogue](../{PROSE.as_posix()}) · [Names](../{NAMES.as_posix()})

Stored verification passes 258 pages, with {stored['fresh_parity_dependent_pages']} fresh parity-sensitive checks and {stored['exact_compiled_pages_reused']} exact reuses. It also passes 255 complete-buffer catalogue lookups, {stored['fresh_relocated_native_relative_cases']} relative branch cases, 336 original SC2 loads and 672 parent handoffs. The rebuilt image changes only the 13 reviewed SC2 blocks and reverses to the exact registered parent. [Lossless evidence](../{archive.as_posix()})

The focused Lil B22 fixture covers 58 dialogue bodies and 61 pages, all 13 system alerts and all three menus. Use the emulator results to verify the selected displays, nameplates, page turns and returns. These checks still need actual observation before the fifth gates and registered release. Lil254 remains the testing candidate. No new review credit was added.
"""
    checkpoint(mutation=ROOT / 'stored_display_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Lil B323–B335 offline and stored checks',
            current_batch_not_yet_integrated=True, all_current_batch_fifth_gates_pending=True,
            current_batch_evidence=evidence, previous_goal_turn_classification='progress',
            current_goal_turn_classification='progress', guide_photos=False,
            no_batch_worker_live=not (ROOT / 'actual_run0_v1/run_plan.json').exists() or (ROOT / 'actual_run0_v1/terminal.json').exists(),
            next_action='Check the Lil261 emulator sample, bind actual display and transitions, then register the batch.'),
        additional_updates={'Lil_SC2_B323_B335_clean_20261110': dict(new_credit=0,
            offline_display_approved=True, native_rendering_pending=False, direct_visual_review_pending=False,
            stored_checks_pending=False, completed_native_body_receipts=255, gameplay_pending=True,
            all_fifth_gates_pending=True, registered_integration_pending=True, evidence=evidence)},
        summary=summary, document=Path('docs/editorial_Lil261_stored_20261110.md'), document_text=notes,
        completed=25637, protected={'translations/release_stack.json': release['registry_sha256'],
            'translations/promoted_build.json': digest('translations/promoted_build.json'),
            release['candidate']: release['candidate_sha256'], release['patch']: release['patch_sha256']})
    print('Archived all Lil261 offline display and stored proofs. No new release credit.')


if __name__ == '__main__':
    main()
