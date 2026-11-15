"""Preserve completed native/visual review while storage, gameplay and release stay open."""
import ast
import gzip
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT = Path('work/Lil361_B283_B298_clean_20261110')
ARCHIVE = Path('translations/editorial_checkpoints/Lil361_offline_20261110_v1')


def main():
    assert not ARCHIVE.exists()
    approval = ROOT / 'offline_display_approval_v1.json'
    proof = load(approval)
    assert (proof['source_objects'], proof['physical_body_candidates'], proof['body_pages'],
            proof['selected_alignment_cases']) == (361, 352, 353, 1408)
    assert (proof['source_styles'], proof['choice_captions'], proof['distinct_name_strings']) == (177, 9, 19)
    assert proof['all_final_body_pages_directly_viewed'] and proof['all_names_andcaptions_directly_viewed']
    assert proof['all_native_controls_substitutions_words_glyphs_bounds_andpagination_pass']
    assert proof['all_fifth_formatting_gates_still_pending'] and not proof['actual_gameplay']
    planpath = ROOT / 'plan_v6/automatic_plans.json'
    plan = load(planpath)
    assert not plan['failures']
    assert not [i for r in plan['records'] for i in r['base_QA']['issues'] if i['severity'] in ['error', 'warning']]
    delta = load(ROOT / 'final_layout_delta_v1.json')
    assert delta['changed_layouts'] == 9 and delta['all_logical_prose_unchanged'] and delta['one_FE_blank_row_removed']
    manuscript = Path('translations/lil_B283_B298_contextual_review_v1.json')
    names = Path('translations/lil_B283_B298_scoped_names_v1.json')
    for row in load(manuscript)['records'] + load(names)['records']:
        assert row['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
    oldarchive = Path('translations/editorial_checkpoints/Lil361_prose_plan_20261110_v1/archive_manifest.json')
    prior = load(oldarchive)['artifacts']
    ARCHIVE.mkdir(parents=True)
    artifacts, reused = {}, 0
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or p.suffix not in ['.json', '.txt']:
            continue
        raw, h = p.read_bytes(), digest(p)
        old = prior.get(str(p))
        if old and old['source_sha256'] == h:
            assert digest(old['archive']) == old['archive_sha256']
            assert gzip.decompress(Path(old['archive']).read_bytes()) == raw
            artifacts[str(p)] = {**old, 'reused_from': str(oldarchive)}
            reused += 1
            continue
        destination = (ARCHIVE / p.relative_to(ROOT)).with_suffix(p.suffix + '.gz')
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
        assert gzip.decompress(destination.read_bytes()) == raw
        artifacts[str(p)] = dict(archive=str(destination), source_sha256=h, archive_sha256=digest(destination))
    producers = sorted(set(Path('scripts').glob('*lil361*.py')) | {
        Path('scripts/prepare_editorial_native_resume_v2.py'), Path('scripts/assemble_editorial_native_journals_v1.py'),
        Path('scripts/record_editorial_contact_visual_review_v1.py'), Path('scripts/approve_scoped_clean_offline_v3.py')})
    for p in producers:
        ast.parse(p.read_bytes(), filename=str(p))
    archive = ARCHIVE / 'archive_manifest.json'
    save(archive, dict(artifacts=artifacts, producers={str(p): digest(p) for p in producers},
        all_selected_artifacts_lossless=True, prior_archives_preserved=True, exact_previous_artifacts_reused=reused,
        raw_planes_images_RAM_andROMs_preserved_locally=True, offline_display_approved=True,
        storage_gameplay_andregistered_integration_pending=True, new_credit=0, full_goal_complete=False))
    rp = Path('work/lil269_B243_B282_release_v1/registered_release_verification.json')
    release = load(rp)
    protected = {'translations/release_stack.json': release['registry_sha256'],
        release['candidate']: release['candidate_sha256'], release['manifest']: release['manifest_sha256'],
        release['patch']: release['patch_sha256'], release['canonical_base']: release['canonical_sha256'],
        'work/clean.nds': release['clean_input_sha256'],
        'translations/promoted_build.json': digest('translations/promoted_build.json'),
        'out/promotion_ready_20261110_v4/Translation_DS_All_Routes_20261110_v4_candidate.nds': release['candidate_sha256'],
        str(manuscript): digest(manuscript), str(names): digest(names)}
    summary = ('Lil361 offline display review passes: 352 bodies/353 pages, 1,408 selected native alignments, '
        '177 personality alternatives, nine captions and 19 name strings. Every final page and menu/name sheet is directly viewed. '
        'Nine layouts improve without changing prose, including an observed FE extra blank row; all 178 revisions/183 retentions remain. '
        'Storage, representative gameplay, fifth gates and registered integration remain pending; zero new credit. '
        'Integrated reviews remain 24,744; testing ROM/main unchanged; full goal active; no worker live.')
    document = Path('docs/editorial_Lil361_offline_display_20261110.md')
    text = f'''# Lil361 offline display checkpoint — November 10, 2026

{summary}

The previous goal turn was progress: complete prose review was pushed as `315a0db5582b33eea1ce6194e84449aeacdfac77`. This turn completes native and every-page visual checks. Continue from the exact final `plan_v6/automatic_plans.json`, `final_native_v1.json` and `offline_display_approval_v1.json` under `work/Lil361_B283_B298_clean_20261110`. Do not replay the completed native records. [Earlier source/prose evidence](editorial_Lil361_prose_plan_20261110.md) remains authoritative for the 16 whole exchanges, source-first seals and individual findings.

Every final body page was directly viewed through readable native contact sheets, with individual opening of an ambiguous short alert. Machine checks then bound each viewed tile to its original preview and native plane. The selected evidence covers all 352 bodies/353 pages and four byte alignments per body. There are 221 exact first-run receipt reuses and 131 fresh final records/132 pages. The nine captions in four two/three-choice menus pass 24 provider alignments, 78 bridged modal returns, 36 normal/highlight planes and 216 compiler negatives across the 24 personality objects. Every one of their 192 target slot pointers passes. Fifteen scoped actors have 19 distinct name strings: eight freshly rendered and 11 reused only with exact text, complete ARM9, font and prior visual approval. Both name sheets and all four caption sheets were directly viewed. Catalogue strings are font tests, not full catalogue UI approval.

Native row membership caught a real defect in B292R50: a space-only row appeared between the two planned FE lines. All non-space glyphs were present, so this is an extra-row correction, not a truncation claim. The existing record-specific FE36 guard reserve and a bound phrase preference produce three contiguous complete lines at the unchanged 228px physical width. The native row, glyph, pixel, canary, allocation and consumption checks now pass. The guard was never waived. The first run stopped with exit1 after 228 durable completed receipts; the focused continuation passed with exit0. The initial diagnostic file without a suffix is preserved locally and copied byte-exactly into the archived JSON receipt.

Seven additional wrap changes keep the wine paragraph's last short sentence, get lost, the incredulous question, get moving, gotta go, far too great and find it together. They correct sparse openings and awkward short continuations. The earlier cliff-route page boundary keeps the uncertain Mediterranean map lead together. In total nine layouts differ from the initial plan; all logical prose, native widths, fonts, controls, substitutions and runtime bytes are unchanged, and the page count stays353. One attempted pursuit-clause regrouping was rejected in favor of the original continuous three-row layout because it created an isolated short predicate tail. Earlier warning-producing and superseded plans remain preserved; the final plan has no errors, warnings or failures.

The visual binder correctly rejected an attempt to combine a six-page sheet with a different aggregate-receipt hash. Separate matching 222-record and six-record approvals then passed unchanged guards; the 131-record fresh approval supplies the changed pages. Final selection accepts only exact current compiled bytes and pixels. Historical superseded layouts remain evidence and are not counted twice.

This turn is offline native/visual evidence. It adds no new emulator gameplay, original event activation, branch-result, reward/stat, free-sailing or hardware coverage. The existing startup and source/prose evidence is not relabeled as expedition gameplay. All per-record fifth gates remain false until stored reconstruction and representative transitions pass.

Next, reconstruct the 16 reviewed groups and verify stored bodies, native lookups, branch relocation, archive/serialized-ROM inverses and representative menus, FE returns and pagination. B294 contains 15 newly reviewed speeches plus one earlier credited R73: preserve that context through the qualified `reviewed_credited_context_rebuild_v1.py` path, including the actual clean/current inverses and a frozen pre-integration credit witness. Do not drop, replace or recredit it. Integrate only through a registered cumulative successor, with exact clean-input patch, own startup and protected getters. The new proposals are still excluded from the testing ROM; main requires explicit user acceptance.

[Lossless archive](../{archive.as_posix()}) preserves current JSON/TXT receipts, failed and final plans, all individual native journals, exact visual bindings and earlier source/prose evidence by hash. Raw images, planes, RAM and all ROMs remain local. Integrated credit remains24,744 and native Lil still has1,154 positions pending, including this361-record batch. No worker is live. Keep the full remaining storyline/shared/shop/town/random/player-facing and broader name review active, preserve earlier translations and retentions, and keep guide-photo collection discontinued, artwork and the later older-record technical re-audit separate.
'''
    evidence = {str(p): digest(p) for p in [approval, manuscript, names, archive, planpath,
        ROOT / 'final_layout_delta_v1.json', ROOT / 'display_resolution_v1.json',
        ROOT / 'native_final_selection_v1/resume_selection.json']}
    checkpoint(mutation=ROOT / 'offline_display_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Lil361 complete offline display; storage/gameplay/release pending.',
            current_batch_not_yet_integrated=True, current_batch_registered_andcredited_once=False,
            all_current_batch_fifth_gates_pending=True, current_batch_evidence=evidence, no_batch_worker_live=True,
            previous_goal_turn_classification='progress', current_goal_turn_classification='progress', guide_photos=False,
            next_action='Use plan_v6/final_native_v1; reconstruct16 groups preserving B294 credited context, then stored checks, representative gameplay and registered integration.'),
        additional_updates={'Lil_SC2_B283_B298_clean_20261110': dict(new_credit=0,
            provisional_bodies=352, provisional_pages=353, unresolved_plan_warnings=0,
            completed_native_body_receipts=352, native_rendering_pending=False, direct_visual_review_pending=False,
            all_final_body_pages_directly_viewed=True, offline_display_approved=True,
            confirmed_FE_extra_blank_row_fixed=True, changed_layouts=9, logical_prose_unchanged=True,
            stored_checks_pending=True, gameplay_pending=True, registered_integration_pending=True,
            all_fifth_gates_pending=True, no_batch_worker_live=True, evidence=evidence)},
        summary=summary, document=document, document_text=text, completed=24744, protected=protected)
    for p, item in artifacts.items():
        assert digest(p) == item['source_sha256']
    print(dict(lossless_artifacts=len(artifacts), exact_prior_archives_reused=reused,
        native_bodies=352, pages=353, new_credit=0, registered_candidate_unchanged=True))


if __name__ == '__main__':
    main()
