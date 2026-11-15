"""Archive the complete offline Lil B299–B311 display proof without release credit."""

import ast
import gzip
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_lil278_prose_and_promotion_v1 import (
    ARCHIVE as PRIOR_ARCHIVE, ARCHIVES, BATCH, MANUSCRIPT, NAMES, PACKAGE, PROMOTED, REGISTRY, ROM,
)
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint


ARCHIVE = ARCHIVES / 'Lil278_offline_20261110_v1'
FINAL_PLAN = BATCH / 'plan_visual_final_v1/automatic_plans.json'
APPROVAL = BATCH / 'offline_display_approval_v1.json'
DELTA = BATCH / 'final_layout_delta_v1.json'


def layout_delta():
    final = load(FINAL_PLAN)
    assert not final['failures']
    assert not any(issue['severity'] in {'error', 'warning'}
                   for row in final['records'] for issue in row['base_QA']['issues'])
    counts = {}
    changes = {}
    for version in ('plan_v1', 'plan_v2'):
        before = load(BATCH / version / 'automatic_plans.json')
        delta = []
        for old, new in zip(before['records'], final['records'], strict=True):
            assert (old['id'], old['English'], old['expected_native_pages']) == (
                new['id'], new['English'], new['expected_native_pages'])
            if old['lines'] != new['lines']:
                assert old['encoded_hex'] != new['encoded_hex']
                delta.append(dict(id=new['id'], before=old['lines'], after=new['lines']))
        counts[version] = len(delta)
        changes[version] = delta
    assert counts == {'plan_v1': 25, 'plan_v2': 23}
    by_id = {row['id']: row for row in final['records']}
    assert by_id['DK4_MES_B304_R0051']['lines'][4:] == [
        'Check Market Info if you get stuck.', "I'm counting on you."]
    save(DELTA, dict(
        counts=counts, changes=changes, all_logical_prose_unchanged=True, native_page_count=280,
        rejected_trials={
            'SC2_B299_STYLE_2588_210': 'The attempted regrouping created a one-word opening. The two usable original rows remain.',
            'SC2_B301_STYLE_24_162': 'The attempted regrouping added a row and isolated "for trouble." The original two rows remain.',
        },
        plan=FINAL_PLAN.as_posix(), plan_sha256=digest(FINAL_PLAN),
    ))


def archive_receipts():
    prior = load(PRIOR_ARCHIVE / 'archive_manifest.json')['artifacts']
    artifacts = {}
    for path in sorted(BATCH.rglob('*.json')):
        relative = path.relative_to(BATCH)
        if any(part.endswith('checkpoint_v1') for part in relative.parts):
            continue
        raw = path.read_bytes()
        source_hash = digest(path)
        old = prior.get(str(path))
        if old:
            packed = Path(old['archive'])
            assert source_hash == old['source_sha256'] and digest(packed) == old['archive_sha256']
        else:
            packed = (ARCHIVE / relative).with_suffix('.json.gz')
            packed.parent.mkdir(parents=True, exist_ok=True)
            packed.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
        assert gzip.decompress(packed.read_bytes()) == raw
        artifacts[str(path)] = dict(archive=str(packed), source_sha256=source_hash, archive_sha256=digest(packed))
    assert prior.keys() <= artifacts.keys()
    producers = [Path(__file__), *(Path('scripts') / name for name in (
        'check_editorial_native_explicit_scope_v1.py', 'project_lil278_native_roles_v1.py',
        'check_lil278_menus_v1.py', 'prepare_lil278_native_contacts_v1.py',
        'select_editorial_native_explicit_scope_v1.py', 'approve_lil278_offline_v1.py',
    ))]
    for path in producers:
        ast.parse(path.read_bytes(), filename=str(path))
    manifest = ARCHIVE / 'archive_manifest.json'
    save(manifest, dict(
        artifacts=artifacts, producers={str(path): digest(path) for path in producers},
        all_selected_artifacts_lossless=True, prior_archives_preserved=True,
        exact_previous_artifacts_reused=len(prior), raw_planes_images_RAM_andROMs_preserved_locally=True,
        offline_display_approved=True, storage_gameplay_andregistered_integration_pending=True,
        new_credit=0, full_goal_complete=False,
    ))
    return manifest


def main():
    assert not ARCHIVE.exists() and not DELTA.exists()
    proof = load(APPROVAL)
    assert (proof['source_objects'], proof['physical_body_candidates'], proof['body_pages'],
            proof['selected_alignment_cases']) == (278, 272, 280, 1088)
    assert (proof['source_styles'], proof['style_slot_cases'], proof['choice_captions'],
            proof['distinct_name_strings']) == (139, 144, 6, 11)
    assert proof['all_final_body_pages_directly_viewed'] and proof['all_names_andcaptions_directly_viewed']
    assert proof['all_native_controls_substitutions_words_glyphs_bounds_andpagination_pass']
    assert proof['all_fifth_formatting_gates_still_pending'] and not proof['actual_gameplay']
    for row in load(MANUSCRIPT)['records'] + load(NAMES)['records']:
        assert row['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
    layout_delta()
    archive = archive_receipts()

    release = load(PACKAGE / 'verification/registered_release_verification.json')
    protected = {
        str(REGISTRY): release['registry_sha256'], str(PROMOTED): digest(PROMOTED),
        str(ROM): release['candidate_sha256'], release['candidate']: release['candidate_sha256'],
        release['manifest']: release['manifest_sha256'], release['patch']: release['patch_sha256'],
        release['canonical_base']: release['canonical_sha256'], 'work/clean.nds': release['clean_input_sha256'],
        str(MANUSCRIPT): digest(MANUSCRIPT), str(NAMES): digest(NAMES),
    }
    summary = ('Lil B299–B311 passed offline display review for 272 bodies, 280 pages, six menu captions and 11 '
               'name strings. The final plan improves 25 layouts from the first pass and preserves all prose. '
               'Stored reconstruction, representative gameplay and registration remain pending. '
               'The integrated total remains 25,105 and Lil361 is still the promotion candidate.')
    notes = f"""# Lil B299–B311 offline display checkpoint

{summary}

The previous turn prepared and pushed the promotion candidate handoff and the 278-record prose checkpoint in commit `c3fe3e10`. This turn completes the offline display checks. Continue from `plan_visual_final_v1/automatic_plans.json`, `final_native_v1.json` and `offline_display_approval_v1.json` under `{BATCH.as_posix()}`. The 170 revisions, 108 individual retentions and ten scoped name decisions remain bound to the clean Japanese and the registered Lil361 text. [Prose checkpoint](editorial_Lil361_promotion_Lil278_prose_20261110.md)

The initial renderer defaulted to Hodram. The explicit Lil runner checks that all 13 current blocks, ARM9, COMMON, font and runtime payload match the qualified Lil startup dependencies. The old dispatch receipt covers 141 bodies. Its role bindings now also prove the full clean preambles of two ordinary speeches and the full headers and aliases of 139 personality alternatives. The selected 1,088 native alignment cases pass controls, substitutions, full glyphs, bounds, page consumption and pagination. All eight FE alerts match their planned native rows.

Every final body page was directly viewed at readable scale. Seventeen original sheets cover all 280 pages. Twenty-three records were rendered again after the visual pass, and their 28 pages were viewed separately. Final selection reuses 249 receipts only where the compiled bytes and native pixels match. The Basra Market Info instruction and the following sentence now share a page. Other wraps keep “set off,” “hang on,” “log bridge,” and a short question tag together. Two regrouping trials were dropped because they introduced an isolated opening or a new short tail. The final plan has zero warnings or errors and keeps the 280-page total. [Exact layout differences](../{archive.parent.as_posix()}/final_layout_delta_v1.json.gz)

All 18 personality tables, 144 original slot cases and 162 compiler rejections pass on the final plan. Three menus pass 18 native provider alignments, 54 bridged returns and 21 compiler rejections. The four menu and name sheets were directly viewed. Four name strings were rendered fresh and seven match earlier approved planes by exact text, ARM9 and font. The name tests cover glyphs and the bound consumers. Full catalogue display, later role assignments and controller transitions still need their own evidence.

Next, rebuild the 13 reviewed groups against clean and current input, check stored bytes, branch targets, loaders and exact inverse reconstruction, then test representative menus, FE returns, page turns and host exit in gameplay. Optional event activation and hardware remain unvisited for this batch. All fifth gates and new coverage credit remain pending. Preserve all registered layers, the Market fix and ASCII right bounds when building the successor. Earlier translations and ROMs remain available. [Lossless evidence archive](../{archive.as_posix()})
"""
    evidence = {str(path): digest(path) for path in [APPROVAL, DELTA, FINAL_PLAN, archive, MANUSCRIPT, NAMES]}
    checkpoint(
        mutation=BATCH / 'offline_display_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Lil B299–B311 complete offline display review',
                           current_batch_not_yet_integrated=True, current_batch_registered_andcredited_once=False,
                           all_current_batch_fifth_gates_pending=True, current_batch_evidence=evidence,
                           no_batch_worker_live=True, previous_goal_turn_classification='progress',
                           current_goal_turn_classification='progress', guide_photos=False,
                           next_action='Reconstruct the 13 reviewed groups and verify stored bytes and representative gameplay.'),
        additional_updates={'Lil_SC2_B299_B311_clean_20261110': dict(
            new_credit=0, completed_native_body_receipts=272, native_rendering_pending=False,
            direct_visual_review_pending=False, all_final_body_pages_directly_viewed=True,
            offline_display_approved=True, changed_layouts=25, logical_prose_unchanged=True,
            stored_checks_pending=True, gameplay_pending=True, registered_integration_pending=True,
            all_fifth_gates_pending=True, no_batch_worker_live=True, evidence=evidence)},
        summary=summary, document=Path('docs/editorial_Lil278_offline_display_20261110.md'),
        document_text=notes, completed=25105, protected=protected,
    )
    print('Archived offline display approval and preserved registered build and coverage identities.')


if __name__ == '__main__':
    main()
