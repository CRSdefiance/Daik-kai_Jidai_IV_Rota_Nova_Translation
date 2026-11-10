"""Save the complete uncredited prose batch and its unfinished native-display work."""
import ast
import gzip
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT = Path('work/Lil361_B283_B298_clean_20261110')
ARCHIVE = Path('translations/editorial_checkpoints/Lil361_prose_plan_20261110_v1')


def main():
    assert not ARCHIVE.exists()
    manuscript = Path('translations/lil_B283_B298_contextual_review_v1.json')
    names_path = Path('translations/lil_B283_B298_scoped_names_v1.json')
    prose, names = map(load, [manuscript, names_path])
    assert (prose['source_objects'], prose['complete_exchanges'], prose['proposed_revisions'], prose['justified_retentions']) == (361, 16, 178, 183)
    assert names['scoped_actors'] == 15 and names['first_four_gates_pass']
    expected_gates = dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
    assert all(r['review'] == expected_gates for r in prose['records'] + names['records'])
    gates = load(ROOT / 'prose_gates_v1.json')
    assert gates['structural_projection_pass'] and gates['all_fifth_gates_false']
    plan_path = ROOT / 'plan_v2/automatic_plans.json'
    plan = load(plan_path)
    diagnostics = load(ROOT / 'plan_v2/diagnostics.json')
    assert len(plan['records']) == 352 and sum(r['expected_native_pages'] for r in plan['records']) == 353
    assert not plan['failures'] and not [r for r in diagnostics['issues'] if r['severity'] in ['error', 'warning']]
    first = load(ROOT / 'plan_v1/automatic_plans.json')
    changes = []
    for a, b in zip(first['records'], plan['records'], strict=True):
        assert a['id'] == b['id'] and a['English'] == b['English']
        if a['lines'] != b['lines']:
            changes.append(dict(id=a['id'], before=a['lines'], after=b['lines']))
    assert len(changes) == 1 and changes[0]['id'] == 'DK4_MES_B294_R0084'
    assert changes[0]['after'][3] == "once we're up the cliff." and changes[0]['after'][4].startswith('I think you can')
    save(ROOT / 'provisional_layout_findings_v1.json', dict(records=352, pages=353, captions=9,
        errors=0, warnings=0, layout_changes=changes, complete_logical_prose_unchanged=True,
        widths_fonts_andruntime_unchanged=True, native_pixels_visual_storage_andgameplay_pending=True, new_credit=0))
    current = load(ROOT / 'current_v1/current_effective.json')
    objects = load(ROOT / 'current_objects_v1/current_objects.json')
    assert current['records'] == 175 and current['credited_context_speeches_preserved_not_newly_reviewed'] == 1
    assert len(objects['style_records']) == 177 and len(objects['choice_records']) == 9
    assert objects['native_style_getter_cases'] == 192
    bindings = load(ROOT / 'scoped_names_macros_reference_v1.json')
    assert bindings['original_native_name_getters'] == 30
    macros = load(ROOT / 'formatting_v1/native_macro_measurements.json')
    assert macros['fresh20_native_preflight_cases_not_new_renderer_characterization']
    assert macros['macro_ascii_lengths'] == dict(FI=3, FA=5, FO=9, FU=9)
    capture = load(ROOT / 'current_context_v1/capture/capture_report.json')
    selected = [r for r in capture['frames_captured'] if r['frame'] in [180, 2000, 4000, 4001]]
    assert len(selected) == 4 and all(digest(r['path']) == r['PNG_sha256'] for r in selected)
    save(ROOT / 'current_context_v1/direct_visual_review_v1.json', dict(selected_captures=selected,
        all_four_selected_original_captures_directly_viewed=True,
        observed='Koei logo, Lil character confirmation and Lil Amsterdam opening text.',
        scope='Existing registered candidate startup context only; no new361 optional events, full opening or hardware coverage.',
        other_captured_frames_not_given_new_visual_credit=True, new_credit=0))
    prior_archive = load('translations/editorial_checkpoints/Lil361_source_intake_20261110_v1/archive_manifest.json')
    reusable = prior_archive['artifacts']
    files = sorted(p for p in ROOT.rglob('*') if p.is_file() and p.suffix in ['.json', '.txt'])
    ARCHIVE.mkdir(parents=True)
    artifacts = {}
    for p in files:
        raw = p.read_bytes()
        old = reusable.get(str(p)) or reusable.get(str(p).replace('/', '\\'))
        if old and digest(p) == old['source_sha256']:
            assert digest(old['archive']) == old['archive_sha256']
            assert gzip.decompress(Path(old['archive']).read_bytes()) == raw
            artifacts[str(p)] = {**old, 'exact_earlier_archive_reused': True}
            continue
        destination = (ARCHIVE / p.relative_to(ROOT)).with_suffix(p.suffix + '.gz')
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
        assert gzip.decompress(destination.read_bytes()) == raw
        artifacts[str(p)] = dict(archive=str(destination), source_sha256=digest(p), archive_sha256=digest(destination))
    producers = sorted(set(Path('scripts').glob('*lil361*.py')) | {
        Path('scripts/save_clean_editorial_part_v3.py'), Path('scripts/prepare_clean_editorial_current_inputs_v2.py')})
    for p in producers:
        ast.parse(p.read_bytes(), filename=str(p))
    archive_path = ARCHIVE / 'archive_manifest.json'
    save(archive_path, dict(artifacts=artifacts, producers={str(p): digest(p) for p in producers},
        all_selected_artifacts_lossless=True, earlier_source_intake_archive_preserved=True,
        raw_RAM_captures_andROMs_preserved_locally=True, records=361, first_four_gates_pass=True,
        fifth_gates_pending=True, new_credit=0, full_goal_complete=False))
    release_path = Path('work/lil269_B243_B282_release_v1/registered_release_verification.json')
    release = load(release_path)
    protected = {'translations/release_stack.json': release['registry_sha256'],
        release['candidate']: release['candidate_sha256'], release['manifest']: release['manifest_sha256'],
        release['patch']: release['patch_sha256'], release['canonical_base']: release['canonical_sha256'],
        'work/clean.nds': release['clean_input_sha256'],
        'translations/promoted_build.json': digest('translations/promoted_build.json'),
        'out/promotion_ready_20261110_v4/Translation_DS_All_Routes_20261110_v4_candidate.nds': release['candidate_sha256'],
        str(manuscript): digest(manuscript), str(names_path): digest(names_path)}
    evidence = {str(p): digest(p) for p in [manuscript, names_path, archive_path, plan_path,
        ROOT / 'clean_draft_seal_v1.json', ROOT / 'prose_gates_v1.json', ROOT / 'scoped_terms_reference_v1.json',
        ROOT / 'dynamic_roles_current_v1.json', ROOT / 'formatting_v1/native_macro_measurements.json',
        ROOT / 'provisional_layout_findings_v1.json', release_path]}
    summary = ('Lil361 B283–B298 has complete contextual prose decisions:178 proposed revisions,183 justified retentions and15 scoped name reviews. '
        'All first four individual gates pass;fifth gates remain false. Source/current bindings,roles,terms and20 native macro preflights pass. '
        'The provisional352-body/353-page plan has zero errors orwarnings;one page boundary improves without changing prose;nine captions remain separate. '
        'Native/visual/storage/representative gameplay andregistered integration remain. No new ROM orcredit;24,744 integrated. '
        'The pushed v4 testing candidate andmain are unchanged;full goal active,no worker live.')
    document = Path('docs/editorial_Lil361_prose_plan_20261110.md')
    text = f'''# Lil B283–B298 prose and provisional layout — November 10, 2026

{summary}

The previous goal turn was progress: the cumulative v4 testing copy and patch package were prepared and pushed as `9656adf81d8a16d8b430394295b86f2e823d9779`. This turn is progress: all361 source-first meanings/drafts, full contextual comparisons andfirst four prose gates are complete. Keep the full editorial objective active. The testing ROM, registered release andmain stay unchanged; none of the new proposals ships orreceives completion credit yet.

Use [the361-record manuscript](../{manuscript.as_posix()}) and[15 scoped name reviews](../{names_path.as_posix()}). Sixteen complete clean/current SC2 exchanges contain175 ordinary speeches,177 physical personality alternatives in24 eight-slot objects andnine captions in four menus. There are337 progressive and15 FE bodies. B294's earlier credited R73 remains part of the complete16-object context, without a duplicate draft, approval orcredit. The native census remains5,566/6,720 covered, leaving1,154 positions; this pending361 is inside that remainder.

All361 meanings and independent logical-paragraph drafts were sealed before current-English intake. Exact source/current references, individual findings,178 revisions and183 retention reasons are preserved. The source-only D7 warning is admitted only for its exact known bytes andexplicit B283 ID; this does not approve an actor identity. Every ordinary command preamble, style header/alias andmenu index remains bound. Names/roles, conditional outcomes and uncertainty were read in whole exchanges before the final prose decisions. Source files under `sources/` remain untouched.

The prose restores missing nuances in map warnings, danger andfriendly-fire reports, apparent injuries, voice differences andthe fog separation branch. Emilio's play-dead sleep gag andMikhail's unfinished cave joke remain without an invented body part orrelationship. Wordless reactions use consistent ASCII punctuation. The unseen Angkor entity is notassigned a male identity, deity rank orconfirmed power; the existing successful pure-new-star riddle wording is retained. Current Wine quantities,8,000/25,000 gold,share changes,one-day notices andwristband loan remain exact. The explicit source Emperor title is restored during the final read-through, changing the earlier177/184 proposal split to178/183; both earlier decisions andthe amendment remain preserved.

Exact native pointers bind Alchemy Book andHeavenly Wristband, town Istanbul andthe two short Proof UI labels. The unchanged integrated SC3 B53 anchor binds the full story term Proof of Conquest, replacing legacy Proof of Conqueror here. Three stale Constantinople body references are corrected to current/source Istanbul. Native FA expands to Argot, a surname; the independent draft's with-FA affiliation was discarded andits provisional context note corrected explicitly. No sealed draft was rewritten. All15 labels are retained for individual source/context reasons; catalogue UI, hidden metadata,future roles andthe broader207-name review remain separate.

The fresh4,001-frame current-ROM Lil context uses ordinary inputs with no battery,savestate,overlay,RAM/roster/role/RNG oroutcome forcing. Original captain/route getters return2 andthe full123,264-byte staged payload matches. Four original captures were directly viewed:logo,character confirmation andAmsterdam opening. This is existing startup context,notnew expedition gameplay orhardware. Bound native lookups cover175 ordinary records,192 style-slot cases,177 physical alternatives,nine captions,30 name getters andfive dynamic selectors. Selectors208/211/215/216 resolve to the generic151 fallback only in this unassigned startup state; future assignments are unvisited.

Twenty fresh native macro preflights pass with FI/FA/FO/FU lengths3/5/9/9,including the null-actor FE path. The explicit-captain planner freshly checks every source/current body anduses validated216px progressive/228px FE widths with native pair-phase andpagination rules. Planv2 has352 bodies/353 pages,zero errors/warnings/failures andnine separately handled captions. One exact-source/current/English-bound preference keeps B294R84's uncertain Mediterranean map lead together after a complete cliff-route sentence. Allprose is unchanged. This is a provisional layout check,notnative pixel orvisual approval. The failed SC1-only planner invocation andmissing preference-binding attempt are preserved; both rejected before plan output andno guard was waived.

[Lossless evidence archive](../{archive_path.as_posix()}) preserves allJSON/TXT receipts,source/current packets,seals,comparisons,old andnew plans,failed preferences andnative bindings,with exact earlier archive reuse. RawRAM,captures andROMs remain local. No worker is live. Next: render/check all352 bodies/353 pages,nine captions andscoped names; visually inspect every page with readable contact sheets;thenstored reconstruction andrepresentative pagination/menu/FE/gameplay checks before registered integration. Reuse matching proofs;donotrepeat completed Lil269 checks.

Every remaining storyline/contextual pass,earlier translation,shared shop/town exchange,random scene,player-facing prose andbroader name review remains in scope. Keep early Rafael/tutorial priorities,no guide photos,deferred artwork andthe later older-record technical re-audit. Mainpromotion requires the user's cold-boot acceptance;the full goal remains active.
'''
    checkpoint(mutation=ROOT / 'prose_plan_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Lil361 B283-B298 first four prose gates pass; native/visual/storage/gameplay/release pending.',
            current_batch_not_yet_integrated=True, current_batch_registered_andcredited_once=False,
            all_current_batch_fifth_gates_pending=True, proposed_revisions=178, justified_retentions=183,
            current_batch_evidence=evidence, no_batch_worker_live=True, guide_photos=False,
            previous_goal_turn_classification='progress', current_goal_turn_classification='progress',
            next_action='Use plan_v2; finish fresh native andevery-page visual review,caption/name checks,stored reconstruction andrepresentative gameplay before registered integration.'),
        new_entries={'Lil_SC2_B283_B298_clean_20261110': dict(new_credit=0, source_objects=361, complete_exchanges=16,
            blocks=list(range(283, 299)), source_meanings_sealed_before_current_intake=True,
            independent_drafts_sealed_before_current_intake=True, preserved_credited_context_objects=1,
            current_ordinary_bodies_bound=175, current_styles_bound=177, current_captions_bound=9,
            current_scoped_actors_bound=15, current_name_getters_bound=30, contextual_comparison_pending=False,
            names_terms_consumers_pending=False, first_four_individual_gates_pass=True, proposed_revisions=178,
            justified_retentions=183, all_fifth_gates_pending=True, provisional_bodies=352, provisional_pages=353,
            unresolved_plan_warnings=0, native_rendering_pending=True, direct_visual_review_pending=True,
            stored_checks_pending=True, gameplay_pending=True, registered_integration_pending=True,
            no_batch_worker_live=True, evidence=evidence, full_goal_complete=False)},
        summary=summary, document=document, document_text=text, completed=24744, protected=protected)
    for p, row in artifacts.items():
        assert digest(p) == row['source_sha256']
    print('PASS: lossless361-record prose checkpoint;zero new credit;all protected release identities unchanged.')


if __name__ == '__main__':
    main()
