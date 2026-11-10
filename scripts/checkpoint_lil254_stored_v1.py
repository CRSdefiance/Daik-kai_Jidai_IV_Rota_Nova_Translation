"""Archive the Lil254 visual and stored checks before gameplay approval."""

import gzip
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_lil254_prose_v1 import ROOT, PROSE, NAMES
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint


ARCHIVE = Path('translations/editorial_checkpoints/Lil254_stored_20261110_v1')
RELEASE = Path('work/lil278_B299_B311_release_v1/registered_release_verification.json')
APPROVAL = ROOT / 'offline_display_approval_v1.json'
STORED = ROOT / 'stored_v1/stored_native_verification.json'
CATALOGUE = ROOT / 'stored_catalogue_all_v1/all_stored_effective_body_bindings.json'
LOADERS = ROOT / 'loaders_v1/verification.json'
PLAN = ROOT / 'plan_v6/automatic_plans.json'
SELECTION = ROOT / 'native_final_selection_v2/resume_selection.json'


def main():
    assert not ARCHIVE.exists()
    approved, stored, catalogue, loaders, plan = map(load, (APPROVAL, STORED, CATALOGUE, LOADERS, PLAN))
    assert approved['all_final_body_pages_directly_viewed'] and approved['all_names_andcaptions_directly_viewed']
    assert (approved['source_objects'], approved['physical_body_candidates'], approved['body_pages']) == (254, 246, 251)
    assert approved['all_fifth_formatting_gates_still_pending'] and not approved['actual_gameplay']
    assert (stored['complete_stored_pages'], stored['fresh_parity_dependent_pages'],
            stored['exact_compiled_pages_reused'], stored['fresh_relocated_native_relative_cases']) == (251, 41, 210, 330)
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert catalogue['body_count'] == 246
    assert (loaders['whole_archive_loads_andcache_hits'], loaders['parent_cases']) == (336, 672)
    earlier = {row['id']: row for row in load(ROOT / 'plan_v2/automatic_plans.json')['records']}
    delta = []
    for row in plan['records']:
        old = earlier[row['id']]
        if old['encoded_hex'] != row['encoded_hex']:
            delta.append(dict(id=row['id'], before=old['lines'], after=row['lines'], prose_changed=old['English'] != row['English']))
    assert [row['id'] for row in delta if row['prose_changed']] == ['DK4_MES_B319_R0008']
    delta_path = ROOT / 'final_layout_delta_v1.json'
    assert not delta_path.exists()
    save(delta_path, dict(changes=delta, changed_records=len(delta), selected_plan_sha256=digest(PLAN),
        FE_blank_row_repaired='DK4_MES_B316_R0205',
        rejected_layouts={'DK4_MES_B315_R0010': 'The sentence-boundary trial broke illustrated map and left day. alone. Retain the fuller viewed rows and connected second page.'}))
    paths = [APPROVAL, STORED, CATALOGUE, LOADERS, PLAN, SELECTION, delta_path,
        ROOT / 'plan_v5/automatic_plans.json', ROOT / 'plan_v6/diagnostics.json',
        ROOT / 'FE_scope_diagnostic_v1.json', ROOT / 'prose_config_v2.json', ROOT / 'prose_gates_v2.json',
        ROOT / 'formatting_v1/FE_and_phrase_preferences_v2.json',
        ROOT / 'formatting_v2/formatting_input.json', ROOT / 'formatting_v2/visual_preferences_v3.json',
        ROOT / 'formatting_v2/visual_preferences_final_v4.json', ROOT / 'formatting_v2/fresh_macro_equivalence.json',
        ROOT / 'reconstruction_v1/reconstruction.json', ROOT / 'body_visual_review_v1.json',
        ROOT / 'final_native_v1.json', ROOT / 'menu_native_approved_v1.json',
        ROOT / 'compiled_styles_v2/compiled_style_objects.json', ROOT / 'display_selection_v1.json',
        ROOT / 'display_fixtures_v1/Lil254_wolf_ruins_trade_fixture.json', ROOT / 'actual_run0_v1/run_plan.json']
    artifacts = {}
    for path in paths:
        raw = path.read_bytes()
        packed = (ARCHIVE / path.relative_to(ROOT)).with_suffix('.json.gz')
        packed.parent.mkdir(parents=True, exist_ok=True)
        packed.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
        assert gzip.decompress(packed.read_bytes()) == raw
        artifacts[path.as_posix()] = dict(archive=packed.as_posix(), source_sha256=digest(path), archive_sha256=digest(packed))
    manifest = ARCHIVE / 'archive_manifest.json'
    save(manifest, dict(artifacts=artifacts, source_objects=254, native_pages=251, offline_and_stored_pass=True,
        gameplay_approval_pending=True, new_credit=0, full_goal_complete=False))
    release = load(RELEASE)
    evidence = {str(p): digest(p) for p in (manifest, APPROVAL, STORED, CATALOGUE, LOADERS, PLAN)}
    prose = PROSE.with_name(PROSE.name.replace('_v1', '_v2'))
    names = NAMES.with_name(NAMES.name.replace('_v1', '_v2'))
    summary = ('Lil B312–B319 passed offline review of all 251 dialogue pages, eight captions and 13 name strings. '
        'The eight groups passed stored reconstruction and the original SC2 loaders. The FE alert blank row and '
        'double period after the company substitution are fixed. Representative gameplay approval and registration remain. '
        'The ledger credits 25,383 reviews.')
    notes = f"""# Lil B312–B319 display and storage checkpoint

{summary}

The eight exchanges retain 151 revisions and 103 justified retentions. Fresh native checks and exact receipt reuse cover all 246 bodies in four alignments each. All 158 alternate bodies and 216 original voice slots pass. Three menus and ten scoped name decisions pass. The formatter preserves native controls, complete glyphs, substitutions, bounds and 251 pages. [Dialogue](../{prose.as_posix()}) · [Names](../{names.as_posix()})

The B316R205 injury notice consumed every byte but inserted a space-only row. The qualified per-record FE reserve keeps the two rows contiguous at the original 228-pixel width. Lil's B319R8 sentence now connects the objection with a comma after the company substitution, whose default text already ends in a period. The final layout keeps phrases including “right away,” “came through,” “cactus spine” and “up front” together. B315's sentence-boundary trial split “illustrated map” and orphaned “day.” The fuller approved layout avoids those problems. [Exact layout changes](../{artifacts[delta_path.as_posix()]['archive']})

Stored checks pass 251 pages, with 41 fresh parity-sensitive renders and 210 exact reuses. All 246 native catalogue lookups, 330 relative branch cases, 336 SC2 loads and cache hits, and 672 parent handoffs pass. Reconstruction changes only the eight owned SC2 blocks and reverses to the exact registered parent. The prepared gameplay fixture combines selected conditional commands in the initialized Lil B22 host and targets both selector-00 headers, all three menus, all seven system alerts, page turns and the host exit. Use the actual emulator evidence before approving gameplay. [Lossless evidence](../{manifest.as_posix()})

Lil278 remains the registered promotion candidate. Lil254 has no new release credit. The full editorial goal remains active, with deferred artwork and the later older-record technical re-audit tracked separately.
"""
    checkpoint(
        mutation=ROOT / 'stored_display_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Lil B312–B319 offline and stored checks',
            current_batch_not_yet_integrated=True, all_current_batch_fifth_gates_pending=True,
            current_batch_evidence=evidence, previous_goal_turn_classification='progress',
            current_goal_turn_classification='progress', guide_photos=False,
            no_batch_worker_live=(ROOT / 'actual_run0_v1/terminal.json').exists(),
            next_action='Finish the Lil254 emulator test and bind pixels, menu and FE returns, page turns and host exit, then register the batch.'),
        additional_updates={'Lil_SC2_B312_B319_clean_20261110': dict(new_credit=0,
            offline_display_approved=True, native_rendering_pending=False, direct_visual_review_pending=False,
            stored_checks_pending=False, completed_native_body_receipts=246, gameplay_pending=True,
            all_fifth_gates_pending=True, registered_integration_pending=True, evidence=evidence)},
        summary=summary, document=Path('docs/editorial_Lil254_stored_20261110.md'), document_text=notes,
        completed=25383, protected={'translations/release_stack.json': release['registry_sha256'],
            'translations/promoted_build.json': digest('translations/promoted_build.json'),
            release['candidate']: release['candidate_sha256'], release['patch']: release['patch_sha256']},
    )
    print(f'Archived {len(artifacts)} receipts and {len(delta)} final layout or prose changes without release credit.')


if __name__ == '__main__':
    main()
