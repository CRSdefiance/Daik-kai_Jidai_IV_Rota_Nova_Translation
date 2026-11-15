"""Archive the remaining Lil prose decisions and qualified display inputs."""

import gzip
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_lil261_prose_layout_v1 import NAMES, PROSE, ROOT
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint


ARCHIVES = Path('translations/editorial_checkpoints')
ARCHIVE = ARCHIVES / 'Lil261_prose_layout_20261110_v1'
PRIOR = ARCHIVES / 'Lil261_clean_20261110_v1/archive_manifest.json'
RELEASE = Path('work/lil254_B312_B319_release_v1/registered_release_verification.json')


def main():
    manifest = ARCHIVE / 'archive_manifest.json'
    assert not manifest.exists()
    proof = load(ROOT / 'prose_gates_v1.json')
    assert (proof['records'], proof['revisions'], proof['retentions'], proof['scoped_name_retentions']) == (261, 198, 63, 9)
    assert proof['first_four_individual_gates_pass'] and proof['all_fifth_gates_false']
    seal = load(ROOT / 'clean_draft_seal_v1.json')
    assert seal['source_glosses_andindependent_drafts_all_saved_before_first_current_story_English_exposure']
    plan_path = ROOT / 'plan_v4/automatic_plans.json'
    plan = load(plan_path)
    assert len(plan['records']) == 255 and sum(r['expected_native_pages'] for r in plan['records']) == 258
    assert not plan['failures'] and not any(i['severity'] in {'error', 'warning'} for r in plan['records'] for i in r['base_QA']['issues'])
    visual = load(ROOT / 'mixed_visual_review_v1.json')
    assert (visual['distinct_name_strings'], visual['captions'], visual['menus']) == (12, 6, 3)
    assert visual['all_names_andcaptions_directly_viewed'] and not visual['actual_gameplay']
    alerts = load(ROOT / 'FE_scope_diagnostic_v1.json')
    assert len(alerts['records']) == 13 and all(r['passed'] for r in alerts['records'])
    styles = load(ROOT / 'compiled_styles_v1/compiled_style_objects.json')
    assert (len(styles['objects']), styles['physical_alternatives'], styles['native_target_slot_cases']) == (18, 119, 144)
    viewed = [ROOT / f'visual_B{block}_v1/contacts/contact_manifest.json' for block in (323, 324)]
    for path, count in zip(viewed, (64, 57), strict=True):
        scope = load(path)
        assert scope['records'] == len(scope['pages']) == count and len(scope['sheets']) == 4
        assert all(digest(row['path']) == row['sha256'] for row in scope['sheets'])
    all_paths = [*(p for p in ROOT.glob('*.json') if p.is_file()), *ROOT.glob('clean_part_B324_B335_v1/*.json'),
        *ROOT.glob('current_inputs_v1/*.json'), ROOT / 'current_v1/current_effective.json',
        ROOT / 'current_objects_v1/current_objects.json', *ROOT.glob('formatting_v1/*.json'),
        *ROOT.glob('plan_v[1234]/*.json'), ROOT / 'menu_native_v1/group_verification.json',
        ROOT / 'name_planes_v1/native_name_planes.json', ROOT / 'compiled_styles_v1/compiled_style_objects.json',
        ROOT / 'scoped_names_macros_reference_v1.json/names.json', ROOT / 'native_body_v1/native_run_inputs.json',
        ROOT / 'visual_B323_v1/projections/B323_checked.json',
        ROOT / 'visual_B324_v1/projections/B324_checked.json', *viewed]
    prior = load(PRIOR)['artifacts']
    artifacts = {}
    for path in sorted(set(all_paths)):
        raw = path.read_bytes()
        archived = prior.get(path.as_posix())
        if archived:
            packed = Path(archived['archive'])
            assert digest(packed) == archived['archive_sha256'] and digest(path) == archived['source_sha256']
        else:
            packed = (ARCHIVE / path.relative_to(ROOT)).with_suffix('.json.gz')
            packed.parent.mkdir(parents=True, exist_ok=True)
            if not packed.exists():
                packed.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
        assert gzip.decompress(packed.read_bytes()) == raw
        artifacts[path.as_posix()] = dict(archive=packed.as_posix(), source_sha256=digest(path), archive_sha256=digest(packed))
    save(manifest, dict(artifacts=artifacts, prior_archive=PRIOR.as_posix(), prior_archive_sha256=digest(PRIOR),
        source_objects=261, first_four_individual_gates_pass=True, all_fifth_gates_pending=True,
        initial_B323_B324_pages_directly_viewed=121, initial_visual_tiles_still_require_final_selection=True,
        new_credit=0, full_goal_complete=False))
    release = load(RELEASE)
    evidence = {str(p): digest(p) for p in (manifest, PROSE, NAMES, plan_path, *viewed)}
    summary = ('Lil B323–B335 has 261 contextual decisions, including 198 revisions and 63 justified retentions. '
        'The four prose gates pass. All six captions and 12 scoped name strings passed native and visual checks. '
        'The final body display and stored checks, focused gameplay, and cumulative registration remain. '
        'The ledger credits 25,637 reviews.')
    notes = f"""# Lil B323–B335 contextual and provisional layout checkpoint

{summary}

The source-first pass covers all 13 exchanges before comparison with the registered English. The revisions clarify the fog and cave choices, preserve individual crew voices and uncertain outcomes, keep the Genoa commission separate from the Havana reward, and preserve the humor and grief in Lil's encounters. The three item names bind to clean and active native pointers for Alchemy Book, Sextant and Ancient City Map. Cocoa, Tobacco, Silver and Tomato were checked, along with the Chapel and Missionary procedure. Nine scoped name retentions include Charles, Samwell, Isabel and separate source Villager selectors. [Dialogue decisions](../{PROSE.as_posix()}) · [Name decisions](../{NAMES.as_posix()})

The provisional v4 plan has 255 bodies, 258 pages and no errors or warnings. It keeps the three multi-page continuations at more coherent sentence boundaries and fixes several phrase splits. All 13 alerts pass the focused original-painter row preflight. The initial style run passes 119 bodies in 144 source voice slots. The three two-choice menus pass all 18 provider alignments and 54 modal return checks. Twelve name strings, all six captions and the 121 initial B323–B324 pages were directly viewed. Layouts changed after that review require fresh rendering. These are offline checks. [Lossless archive](../{manifest.as_posix()})

Continue the initial body run from its existing handle and completed journals. Use the final selected bytes to reuse native and visual proofs, then check stored script behavior and representative gameplay before crediting or shipping any part of this batch. Lil254 remains the registered candidate. The wider editorial scope remains active.
"""
    checkpoint(mutation=ROOT / 'prose_layout_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Lil B323–B335 prose and provisional native layout',
            current_batch_not_yet_integrated=True, current_batch_registered_andcredited_once=False,
            all_current_batch_fifth_gates_pending=True, current_batch_evidence=evidence,
            no_batch_worker_live=False, previous_goal_turn_classification='progress', current_goal_turn_classification='progress',
            next_action='Continue the existing Lil261 native body run and finish the final page, stored and representative checks.', guide_photos=False),
        additional_updates={'Lil_SC2_B323_B335_clean_20261110': dict(new_credit=0, clean_meanings=261,
            independent_drafts=261, remaining_clean_drafts=0, current_English_not_consulted=False,
            first_four_individual_gates_pass=True, all_five_gates_pending=False, all_fifth_gates_pending=True,
            proposed_revisions=198, justified_retentions=63, native_rendering_pending=True,
            provisional_bodies=255, provisional_pages=258, provisional_captions=6,
            menu_and_name_visual_approved=True, initial_B323_B324_pages_directly_viewed=121,
            stored_checks_pending=True, gameplay_pending=True, registered_integration_pending=True, evidence=evidence)},
        summary=summary, document=Path('docs/editorial_Lil261_prose_layout_20261110.md'), document_text=notes,
        completed=25637, protected={'translations/release_stack.json': release['registry_sha256'],
            'translations/promoted_build.json': digest('translations/promoted_build.json'),
            release['candidate']: release['candidate_sha256'], release['patch']: release['patch_sha256']})
    print(f'Archived {len(artifacts)} exact receipts. No new release credit.')


if __name__ == '__main__':
    main()
