"""Seal the completed static pages and staged ship-label evidence without release credit."""

import gzip
from hashlib import sha256
from pathlib import Path
import xml.etree.ElementTree as ET

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_literal_static_layout_v1 import ROOT as INITIAL
from scripts.preflight_literal_notice_formatting_v1 import ARCHIVE, OUTPUT, TARGET
from scripts.prepare_ship_command_research_v1 import PROOF, WORK
from scripts.refine_literal_notice_layout_v2 import AMENDMENT, ROOT as FINAL
from scripts.stage_ship_command_release_v1 import CANDIDATE, GETTERS, PATCH, PARENT, REGISTRY, STAGED, STARTUP


DEST = ARCHIVE / 'static_notice_and_ship_stage'
DOCUMENT = Path('docs/editorial_shared_static_ship_20261110.md')


def main():
    assert not DEST.exists() and not DOCUMENT.exists()
    parent, staged, startup, getters = map(load, (PARENT, STAGED, STARTUP, GETTERS))
    assert digest(REGISTRY) == parent['registry_sha256'] == staged['predecessor_registry_sha256']
    assert digest(CANDIDATE) == startup['candidate_sha256'] == getters['runtime']['candidate_sha256'] == staged['candidate_sha256']
    assert digest(PATCH) == staged['patch_sha256'] and staged['clean_input_patch_byte_exact']
    assert staged['whole_parent_inverse_exact'] and not staged['own_registered_startup_pending']
    assert staged['actual_menu_approval_pending'] and staged['registration_pending']
    assert getters['both_name_getters_exact_for_all12_protected_actors']
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = load(ledger_path)
    assert ledger['records_editorially_completed'] == 25898 and not ledger['full_goal_complete']
    assert ledger['current_integrated_candidate']['sha256'] == parent['candidate_sha256']
    ledger_sha = digest(ledger_path)
    promoted = digest('translations/promoted_build.json')

    initial, final = map(load, (INITIAL/'layout.json', FINAL/'layout.json'))
    for sheet in initial['sheets']:
        assert digest(sheet['path']) == sheet['sha256']
    assert digest(final['changed_sheet']) == final['changed_sheet_sha256']
    assert (final['final_static_native_pages'], final['fresh_changed_pages'], final['exact_native_page_reuses']) == (19, 4, 15)
    for r in final['records']:
        assert digest(r['preview']) == r['preview_sha256'] and r['complete_words_glyphs_raster_and_guards_verified']
    records = load(OUTPUT)
    assert records['counts'] == {'revision':10, 'retention':20}
    assert load(TARGET)['complete_native_expansion_cases'] == 41
    assert load(AMENDMENT)['fresh_native_expansion_cases'] == 3
    menu = WORK/'native_menu/native_ship_menu.json'
    native_menu = load(menu)
    assert digest(native_menu['sheet']) == native_menu['sheet_sha256']
    assert len(native_menu['captions']) == 4 and native_menu['research']['options'][1]['text'] == 'Abandon Ship'

    first = WORK/'actual_menu_run/terminal.json'
    second = WORK/'actual_menu_live_v2/terminal.json'
    fourth = Path('out/ship_command_menu_capture_20261110_v4/terminal.json')
    observed = []
    for path, key, expected in [(first, 'capture_report', 14300), (second, 'capture_report', 23100), (fourth, 'report', 10600)]:
        status = load(path)
        assert status['terminal_exit_code'] == 0 and status['original_donor_hash_preserved']
        report = load(status[key])
        assert digest(status[key]) == status[key+'_sha256']
        assert report['frames'] == expected and report['ROM_sha256'] == staged['candidate_sha256']
        observed.append(dict(terminal=str(path), terminal_sha256=digest(path), frames=expected,
            localized_ship_menu_observed=False, back_transition_observed=False))
    qa = Path('out/ship_command_repo_qa_v2.xml')
    suites = list(ET.parse(qa).getroot().iter('testsuite'))
    assert sum(int(s.get('tests',0)) for s in suites) == 27
    assert all(int(s.get(k,0)) == 0 for s in suites for k in ['errors','failures','skipped'])
    DEST.mkdir()
    paths = [PROOF, menu, STAGED, STARTUP, GETTERS, INITIAL/'layout.json', FINAL/'layout.json',
        first, second, fourth, qa]
    archived = {}
    for number, path in enumerate(paths, 1):
        source = path.read_bytes()
        label = f'{number:02d}_{path.name}.gz'
        file = DEST/label
        file.write_bytes(gzip.compress(source, compresslevel=9, mtime=0))
        assert gzip.decompress(file.read_bytes()) == source
        archived[path.as_posix()] = dict(archive=file.as_posix(), source_sha256=digest(path), packed_sha256=digest(file))
    index = DEST/'checkpoint.json'
    save(index, dict(archived=archived, contextual_notice_records=30, revisions=10, retentions=20,
        static_pages_native_and_directly_viewed=19, changed_static_pages_directly_viewed=4,
        every_final_static_page_directly_viewed_andbound_to_exact_native_words_glyphs_andbounds=True,
        ship_caption_four_native_planes_directly_viewed=True, own_boot_and_protected_getters_pass=True,
        observed_replays=observed, third_replay_terminal_error='C: filled during navigation journal write',
        fresh_native_template_cases=44, verified_repository_tests=27,
        requested_native_menu_actual_display_andback_still_pending=True, all_ship_registration_pending=True,
        dynamic_notice_layout_allocation_andrepresentative_gameplay_pending=True,
        pending_source_leads_preserved=True, current_registered_candidate_sha256=parent['candidate_sha256'],
        staged_research_candidate_sha256=staged['candidate_sha256'], full_goal_complete=False,
        prior_goal_turn_classification='progress', current_goal_turn_classification='progress',
        no_worker_live=True, new_credit=0, integrated_reviews=25898,
        evidence={str(p):digest(p) for p in [OUTPUT, TARGET, AMENDMENT, Path(__file__)]}))

    summary = ('Thirty shared notices have contextual decisions and native caller bindings. '
        'All 19 static pages passed offline rendering and visual review. '
        'The Abandon Ship successor has an exact clean-input patch and passes its own startup and name checks. '
        'The localized menu and Back transition still need a focused emulator test. Lil261 remains registered.')
    note = f"""# Shared notice formatting and ship command staging

{summary}

The 30 notice decisions contain 10 revisions and 20 justified retentions. Clean and current caller bytes and 31 distinct native lookup or wrapper cases are bound. The restored start-game prompt and system-data fallback explanation occupy separate original consumers. The falling-market-share message retains the player company's possessive because the native caller supplies that company's name. The first I in the trade notice is normalized to ASCII. The three Market replies and the other unmapped branches remain in the source packet. [Review records](../{OUTPUT.as_posix()})

All 41 native varargs samples preserve complete words and argument order, including the fourth stack argument in the date, weather and departure notice. Thirteen messages triggered the first width or row diagnostic. The static set now has 19 directly viewed native pages. Four revised pages were rerendered with complete glyph and pixel checks, and 15 exact pages were reused. The corrected lines keep default system data and the complete access warning together. The dock prompt avoids a one-word final row. The two wording refinements passed three additional native expansion samples. Dynamic layouts and final storage, pagination, allocation and representative gameplay remain pending. [Formatting evidence](../{index.as_posix()})

The ship command changes one owned ARM9 pointer and appends a 16-byte read-only allocation for Abandon Ship. The original Assign option, menu code, Market literal and both Market pointers are preserved. Native geometry widens from 92 to 104 pixels, and all four normal and highlighted caption planes passed pixel and bounds checks and direct review. The staged ROM reconstructs exactly from the clean-input patch and reverses to Lil261. Its own 31,000-frame Maria startup, six captures, 24 protected getters and 27 repository tests passed. Hardware remains unvisited.

The old navigation schedule reached different dialogue on the current build. The extended replay entered combat, where the enemy captured the ships before the forced assignment menu appeared. A third run stopped when C: filled while writing the navigation journal. The E: retry reached an earlier story event and preserved its captures. The label and Back transition remain unobserved in the staged ROM. Use a bounded, source-qualified setup for the original forced-assignment condition next, followed by a fresh live menu and Back check. Reuse the completed offline, startup and patch proofs.

All generated ROMs and evidence remain preserved. C: space was recovered by moving one verified historical Git LFS cache object temporarily to E:, compressing historical copies and restoring the moved object to its original path with identical bytes. Later capture and test output went to E:. The cumulative ledger still credits 25,898 reviews. This checkpoint records per-record work without changing credit or the registry. Main V4701 awaits user acceptance.
"""
    for path, body in [(DOCUMENT, note), *[(Path('docs')/n, None) for n in ('editorial_handoff_current.md','editorial_efficiency_workflow.md','translation_progress.md')]]:
        before = path.read_bytes() if path.exists() else b''
        if body is None:
            body = '# Current editorial checkpoint - 2026-11-10\n\n'+summary+'\n\nContinue from ['+DOCUMENT.stem+']('+DOCUMENT.name+'). Reuse the completed checks; earlier entries below are historical.\n\n'
        pending = path.with_name(path.name+'.shared_static_ship.pending')
        assert not pending.exists()
        pending.write_bytes(body.encode('utf-8')+before)
        assert (path.read_bytes() if path.exists() else b'') == before
        pending.replace(path)
    assert digest(ledger_path) == ledger_sha and digest('translations/promoted_build.json') == promoted
    assert digest(REGISTRY) == parent['registry_sha256']
    print('Sealed 19 directly viewed static notice pages and staged ship-label evidence with zero release credit.')


if __name__ == '__main__':
    main()
