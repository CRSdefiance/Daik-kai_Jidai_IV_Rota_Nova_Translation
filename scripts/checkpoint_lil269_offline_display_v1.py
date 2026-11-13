"""Preserve complete offline display approval without crediting unfinished integration."""
import ast
import gzip
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT = Path('work/Lil269_B243_B282_clean_20261110')
ARCHIVE = Path('translations/editorial_checkpoints/Lil269_offline_20261110_v3')


def main():
    assert not ARCHIVE.exists()
    approval = ROOT / 'offline_display_approval_v1.json'
    proof = load(approval)
    assert (proof['source_objects'], proof['physical_body_candidates'], proof['body_pages'],
            proof['selected_alignment_cases']) == (269, 262, 264, 1048)
    assert proof['all_final_body_pages_directly_viewed'] and proof['all_names_andcaptions_directly_viewed']
    assert proof['all_native_controls_substitutions_words_glyphs_bounds_andpagination_pass']
    assert proof['all_fifth_formatting_gates_still_pending'] and not proof['actual_gameplay']
    assert (proof['source_styles'], proof['choice_captions'], proof['distinct_name_strings']) == (16, 7, 24)
    planpath = ROOT / 'plan_v13/automatic_plans.json'
    plan = load(planpath)
    assert not plan['failures']
    assert not [i for r in plan['records'] for i in r['base_QA']['issues'] if i['severity'] in ['error', 'warning']]
    manuscript = Path('translations/lil_B243_B282_contextual_review_v3.json')
    names = Path('translations/lil_B243_B282_scoped_names_v3.json')
    for row in load(manuscript)['records'] + load(names)['records']:
        assert row['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
    oldarchive = Path('translations/editorial_checkpoints/Lil269_display_partial_20261110_v2/archive_manifest.json')
    prior = load(oldarchive)['artifacts']
    ARCHIVE.mkdir(parents=True)
    artifacts, reused = {}, 0
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or p.suffix not in ['.json', '.txt']:
            continue
        raw = p.read_bytes()
        h = digest(p)
        previous = prior.get(str(p))
        if previous and previous['source_sha256'] == h:
            assert digest(previous['archive']) == previous['archive_sha256']
            assert gzip.decompress(Path(previous['archive']).read_bytes()) == raw
            artifacts[str(p)] = {**previous, 'reused_from': str(oldarchive)}
            reused += 1
        else:
            dest = (ARCHIVE / p.relative_to(ROOT)).with_suffix(p.suffix + '.gz')
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
            assert gzip.decompress(dest.read_bytes()) == raw
            artifacts[str(p)] = dict(archive=str(dest), source_sha256=h, archive_sha256=digest(dest))
    producers = sorted(set(Path('scripts').glob('*lil269*.py')) | {
        Path(__file__), Path('scripts/assemble_editorial_native_journals_v1.py'),
        Path('scripts/approve_scoped_clean_offline_v3.py')})
    for p in producers:
        ast.parse(p.read_bytes(), filename=str(p))
    archive = ARCHIVE / 'archive_manifest.json'
    save(archive, dict(artifacts=artifacts, exact_prior_artifacts_reused=reused,
        previous_archive=str(oldarchive), previous_archive_sha256=digest(oldarchive),
        producers={str(p): digest(p) for p in producers}, all_selected_artifacts_lossless=True,
        raw_ROM_RAM_planes_andcaptures_preserved_locally=True,
        no_prior_archive_orROM_deleted=True, new_credit=0, full_goal_complete=False))
    rp = Path('work/lil382_residual_A_release_v1/registered_release_verification.json')
    release = load(rp)
    assert digest('translations/release_stack.json') == release['registry_sha256']
    protected = {'translations/release_stack.json': release['registry_sha256'],
        release['candidate']: release['candidate_sha256'], release['manifest']: release['manifest_sha256'],
        'out/raphael_natural_v2_accepted_base.nds': release['canonical_sha256'],
        'work/clean.nds': release['clean_input_sha256'],
        'translations/promoted_build.json': digest('translations/promoted_build.json'),
        'out/promotion_ready_20261110_v2/Translation_DS_All_Routes_20261110_v2_candidate.nds': release['candidate_sha256']}
    summary = ('Lil269 offline display review passes: 262 bodies/264 pages, 1,048 selected alignments, '
        '16 style alternatives, seven captions and 24 name strings. Every final page and menu/name sheet is directly viewed. '
        'The B251 riddle truncation is fixed with the qualified source-scoped FE reserve; '
        '16 final layouts change and one page is reclaimed. All 269 contextual prose decisions remain 104 revisions/165 retentions. '
        'Storage, representative gameplay, fifth gates and registered integration remain pending; zero new credit. '
        'Integrated24,475; testing ROM/main unchanged; full goal active; no worker live.')
    document = Path('docs/editorial_Lil269_offline_display_20261110.md')
    text = f'''# Lil269 complete offline display checkpoint — November 10, 2026

{summary}

The previous goal turn was progress: the exact registered cumulative testing ROM and reconstructable patch were packaged and pushed at `3a304b0b2fae49323aa7747928ec8862210f4fa4`. This turn is progress: all remaining native body checks and every-page visual review are complete. No new ROM, registration, editorial credit or promotion is claimed. Keep the full editorial objective active.

Continue from `{approval.as_posix()}` and `final_native_v1.json`. The authoritative prose remains `translations/lil_B243_B282_contextual_review_v3.json` and scoped-names v3, with all first four gates true and all fifth gates false. The 40 complete SC2 B243–B282 groups contain 269 source objects: 246 ordinary bodies, 16 physical personality alternatives and seven captions. Source/current references, individual findings, 104 revisions, 165 justified retentions, 25 scoped actors, terms and role bindings remain preserved. Source meanings/drafts were sealed before current-English intake in earlier turns; do not restart that completed contextual pass.

The exact read-only FE return observer reproduced B251R9 consuming108 of125 bytes, inserting a blank row and omitting the final question. The existing record-scoped FE36 reserve fixes it with no prose, font, code or physical228px change. B251R165 receives the same qualified reserve for its matching long-row risk; no independent observed truncation of that second record is claimed. Both final pages pass complete consumption, row membership, glyph sequence, independent pixels and canaries. Later phrase trials added weak with/the endings; those failed plans are preserved and unwaived. The directly viewed complete single-page riddle is retained with its full question readable across the last two rows, rather than shortening its prose or adding a page.

Final plan is `plan_v13/automatic_plans.json`: 262 bodies/264 pages, zero errors, warnings or failures. Compared with the initial plan, 16 final byte layouts change: 14 preserve identical prose and two retain the already reviewed longer collapsing synonym for the older voice. One figurehead page is reclaimed. The expedition directions and stolen-ship report retain coherent two-page boundaries. Direct views keep the New World, Jacks Bloom, Plett Perrault and Forbidden City names intact, attach short question tags, join along with/up in/worth your while, and improve the sailor opening. A fresh intermediate sailor trial made the opening sparser; the final subject/verb constraint corrects it. Earlier rejected/superseded plans and images remain preserved. No good prose is shortened for fit.

All 262 selected native records pass 1,048 placement alignments. Selection reuses53 unchanged prior body journals and209 exact final records checked this turn; superseded fresh cases remain preserved. Completed original receipts were not restarted. Every final page is bound to directly viewed exact 2x contact tiles, selecting among20 reviewed body sheets. Menus pass three objects/seven captions/18 provider alignments/60 bridged modal returns/28 normal-highlight planes/22 compiler negatives. Two source style objects preserve all16 native slots/18 negatives. Names retain25 actors/50 getter bindings and24 distinct string planes (11 fresh/13 prior exact reuse). Exact menu/name sheets were already directly viewed and their dependencies match. These are offline planes, not full catalogue UI or actual event coverage.

Use the versioned `scripts/approve_scoped_clean_offline_v3.py` for an explicit immutable formatting directory. It preserves every earlier source/current/style/menu/name/visual/native guard, selecting `formatting_v2` rather than overwriting formatting_v1. The journal assembler aggregates exact completed receipts with all native assertions and source/current/runtime/font/macro dependencies checked; it claims no fresh monolithic run. The final style/menu objects are recompiled against the selected plan before their unchanged native proofs are reused.

Next rebuild all40 reviewed blocks through `rebuild_reviewed_editorial_batch_v6`, then complete stored/native alignment, relative-reference, loader/allocation/inverse checks and representative initialized gameplay. Cover the repaired FE riddle and its three-choice transition, style selection, page turns and host returns. Keep ordinary observed gameplay distinct from focused initialized samples and offline-only/unvisited alternatives. No exhaustive natural playthrough or guide photos are required. Only after those checks pass, finalize fifth gates and integrate the269 batch once through a registered cumulative successor, with exact clean-input patch and own startup. Preserve the entire registered726-entry prefix,114 accepted layers,Market format/both pointers,six-section ARM9,ASCII right bounds,source25v2 andB164R99 correction. Main requires user acceptance.

The registered/testing candidate remains `{release['candidate_sha256']}`. Integrated credit remains24,475; all269 proposals are still within Lil's1,423 remaining native positions. Native Maria remains5,129/5,129. Every unfinished storyline/contextual pass, earlier translation, shared/shop/town/random dialogue, player-facing text and broader names remain in scope. Preserve early Rafael/tutorial priority, all translations/retentions, ROMs and evidence; keep deferred graphics artwork and the later older-record technical re-audit separate. [Lossless evidence archive](../{archive.as_posix()}) stores all current JSON/TXT evidence, reusing exact earlier compressed artifacts where hashes match. Raw images/planes/RAM/ROMs remain preserved locally. No worker is live.
'''
    evidence = {str(p): digest(p) for p in [approval, manuscript, names, archive, planpath,
        ROOT / 'final_layout_delta_v1.json', ROOT / 'native_final_selection_v1/resume_selection.json']}
    checkpoint(mutation=ROOT / 'offline_display_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Lil269 complete offline display; storage/gameplay/release pending.',
            current_batch_not_yet_integrated=True, current_batch_registered_andcredited_once=False,
            all_current_batch_fifth_gates_pending=True, current_batch_evidence=evidence, no_batch_worker_live=True,
            previous_goal_turn_classification='progress', current_goal_turn_classification='progress', guide_photos=False,
            next_action='Rebuild all40 blocks, complete stored/native/inverse checks and representative FE/menu/style/page transitions, then registered integration.'),
        additional_updates={'Lil_SC2_B243_B282_clean_20261110': dict(new_credit=0,
            provisional_bodies=262, provisional_pages=264, unresolved_plan_warnings=0,
            completed_native_body_receipts=262, native_rendering_pending=False, direct_visual_review_pending=False,
            all_final_body_pages_directly_viewed=True, offline_display_approved=True,
            confirmed_FE_truncation_fixed=True, stored_checks_pending=True, gameplay_pending=True,
            registered_integration_pending=True, all_fifth_gates_pending=True, no_batch_worker_live=True, evidence=evidence)},
        summary=summary, document=document, document_text=text, completed=24475, protected=protected)
    for p, v in artifacts.items():
        assert digest(p) == v['source_sha256']
    print(dict(lossless_artifacts=len(artifacts), exact_prior_archives_reused=reused,
        native_bodies=262, pages=264, new_credit=0, registered_candidate_unchanged=True))


if __name__ == '__main__':
    main()
