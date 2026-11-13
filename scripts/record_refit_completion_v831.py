"""Record the verified Refit family, integrated candidate and exact evidence."""

from copy import deepcopy
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_help_editorial import CONFIG, current_entries
from dk4tool.rom.nds import NdsImage
from scripts.prepare_refit_editorial_v830 import MANUSCRIPT
from scripts.prepare_refit_release_v831 import ROOT
from scripts.run_refit_release_v831 import CAP
from scripts.verify_refit_release_v831 import ROM
from scripts.verify_village_wrap_v608 import read, save

LEDGER = Path('translations/editorial_review_current_v1.json')
REVIEW = Path('translations/refit_help_editorial_final_review_v1.json')
DOC = Path('docs/refit_editorial_v831_completion.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V831 Refit help completion')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V831 Refit help')


def reference(entry):
    return {k: getattr(entry, k) for k in ('message_id', 'block', 'table_offset', 'block_offset', 'copy_end', 'record_index', 'start', 'end')}


def main():
    assert not REVIEW.exists() and not DOC.exists()
    release, gameplay = read(ROOT / 'registered_release_verification.json'), read(ROOT / 'actual_gameplay_verification.json')
    ledger, manuscript = read(LEDGER), read(MANUSCRIPT)
    assert ledger['records_editorially_completed'] == 603 and ledger['records_with_source_and_prose_pass'] == 637
    assert release['candidate_sha256'] == gameplay['candidate_sha256'] == sha(ROM.read_bytes())
    assert len(gameplay['actual23_help_holds_cover13_distinct_messages']) == 23
    assert len({r['message_id'] for r in gameplay['actual23_help_holds_cover13_distinct_messages']}) == 13
    assert sha(Path(gameplay['review_sheet']).read_bytes()) == gameplay['review_sheet_sha256']
    # The sheet and actual final exit have been opened; all captured fonts also
    # passed independent whole-screen models before this human/model review.
    gameplay.update(visual_review_pending=False, visual_review={
        'all12_screen_context_sheet_opened': True,
        'complete_visible_lines_and_original_help_heading_detail_rows_borders_reviewed': True,
        'normal_Refit_cancel_Shipwright_and_Port_menu_return_reviewed': True,
        'all31_other_controlled_native_planes_previously_reviewed_in_V830': True,
        'no_full_playthrough_hardware_or_all31_actual_visits_claim': True})
    save(ROOT / 'actual_gameplay_verification.json', gameplay)
    release.update(actual_panel_and_startup_verification_pending=False,
                   actual_gameplay_proof=str(ROOT / 'actual_gameplay_verification.json'),
                   actual_gameplay_proof_sha256=sha((ROOT / 'actual_gameplay_verification.json').read_bytes()))
    save(ROOT / 'registered_release_verification.json', release)
    save(ROOT / 'editorial_ledger_before_completion.json', ledger)
    rom = NdsImage.open(ROM)
    common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    entries = current_entries(common, arm)
    records = []
    for r in manuscript['records']:
        n = r['message_id']
        native = next(q for q in read('work/analysis/refit_editorial_v830/native_font_verification.json')['records'] if q['message_id'] == n)
        assert entries[n].text.hex() == native['compiled_hex'][:-2]
        records.append({
            'id': r['id'], 'message_id': n, 'english': r['english'], 'speaker': r['speaker'],
            'context': r['context'], 'source_japanese': r['clean_source_Japanese'],
            'source_hex': r['clean_source_hex'], 'source_meaning': r['source_meaning'],
            'localization_note': r['localization_note'], 'clean_reference': r['clean_reference'],
            'before_candidate': manuscript['current_candidate'], 'before_reference': r['current_reference'],
            'before_text_hex': r['current_text_hex'], 'completed_candidate_reference': str(ROM),
            'current_reference': reference(entries[n]), 'current_text_hex': entries[n].text.hex(),
            'decision': 'revised-and-integrated' if r['editorial_decision'] == 'revise' else 'retained-and-editorially-reviewed',
            'review': r['review'], 'generated_lines': native['lines'],
            'actual_display_frames': [q['frame'] for q in gameplay['actual23_help_holds_cover13_distinct_messages'] if q['message_id'] == n],
            'controlled_native_complete_font_and_loader_coverage': True})
    assert sum(r['decision'] == 'revised-and-integrated' for r in records) == 18
    existing = {i for f in ledger['completed_editorial_families'] for i in f.get('native_message_IDs', [])}
    assert not existing.intersection(r['message_id'] for r in records)
    final = {'format': 'dk4-editorial-family-final-review-v1',
             'status': '31-source-context-editorial-native-and-representative-actual-verified',
             'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'source_manuscript': str(MANUSCRIPT), 'source_manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
             'registered_release_proof': str(ROOT / 'registered_release_verification.json'),
             'actual_gameplay_proof': str(ROOT / 'actual_gameplay_verification.json'),
             'all31_source_glosses_individual_editorial_gates_and_generated_layouts_reviewed': True,
             'all7336_original_warm_cold_native_copies_pass': True,
             'actual_scope': gameplay['scope'], 'records': records,
             'full_editorial_goal_complete': False, 'separate_graphics_goal_complete': False}
    save(REVIEW, final)
    family = {'id': 'Shared-Refit-room-and-equipment-help1247-1255-1268-1289',
              'native_message_IDs': [r['message_id'] for r in records],
              'records': records, 'final_review': str(REVIEW),
              'documentation': str(DOC), 'actual_verification_scope': gameplay['scope']}
    ledger['completed_editorial_families'].append(family)
    ledger['records_editorially_completed'] = 634
    ledger['records_revised_and_integrated'] = 456
    ledger['retained_wordings_editorially_completed'] = 178
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4'] = 633
    ledger['reviewed_but_incomplete_COMMON_IDs'] = [750, 751, 752]
    ledger['active_source_prose_drafts'] = {
        'native_message_IDs': [750, 751, 752],
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],
        'status': 'three-older-context-unmapped-drafts',
        'note': 'Ceremony52 completed in V829 and Refit31 completed in V831;neither remains an active draft.'}
    ledger['previous_current_integrated_candidate_V829'] = deepcopy(ledger['current_integrated_candidate'])
    candidate = {'path': str(ROM), 'sha256': sha(ROM.read_bytes()), 'profile': 'all-routes-unified-v831',
                 'MESFILE_sha256': sha(common), 'ARM9_sha256': sha(arm),
                 'patch': str(ROM.with_suffix('.xdelta')), 'patch_sha256': release['patch_sha256'],
                 'manifest': str(ROM.with_suffix('.manifest.json')),
                 'status': 'experimental-Refit31-editorially-native-and-representative-gameplay-verified',
                 'details': str(DOC), 'full_goal_complete': False}
    ledger['current_integrated_candidate'] = candidate
    ledger['source_pins']['current'] = deepcopy(candidate)
    ledger['next_integrated_profile_for_goal_continuation'] = 'all-routes-unified-v831'
    ledger['native_relocation_reference_before_V831'] = deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_native_relocation_reference'] = {
        'candidate': str(ROM), 'COMMON_sha256': sha(common), 'ARM9_sha256': sha(arm),
        'parser': 'dk4tool.patch.refit_help_editorial.current_entries',
        'release_config': CONFIG, 'source_locked_directory_and_all3668_selections_verified': True}
    ledger['refit_help_editorial_v831'] = {
        'status': final['status'], 'final_review': str(REVIEW), 'documentation': str(DOC),
        'registered_release_proof': final['registered_release_proof'], 'actual_gameplay_proof': final['actual_gameplay_proof'],
        '31_completed_18_revised13_retained': True, 'full_goal_complete': False}
    ledger['refit_help_editorial_v830']['superseded_by_completion'] = str(REVIEW)
    for finding in ledger['findings']:
        if finding['id'] == 'COMMON-Refit-help31-V830-editorial':
            finding.update(status='completed-in-registered-V831', no_completion_credit=False,
                           completion_review=str(REVIEW), proof=str(ROOT / 'actual_gameplay_verification.json'))
    ledger['coverage_units'].append({'id': family['id'], 'status': 'completed',
                                     'native_message_IDs': family['native_message_IDs'],
                                     'final_review': str(REVIEW), 'scope': 'Refit help consumer only;remaining shared and route prose stay open.'})
    ledger['latest_checkpoint'] = (
        'V831 completes the31-entry Refit help editorial family:18 revised wordings and13 justified retentions. '
        'All31 clean/current source references and current native font planes pass;all7336 warm/cold original message copies pass. '
        'Actual23 complete help holds cover13 distinct messages,including9 revised descriptions;all62 whole-screen models,normal cancel/Shipwright/Port return, '
        'six five-ship/funds state checks and seven ordinary no-save New Game pairs pass. '
        'Registered combined V831 and exact clean-input patch preserve471 batches,114 accepted layers,all other strings/opaque payloads/scripts/graphics and original code/memory bounds. '
        '634 entries completed (456 revised/178 retained),637 source-prose reviewed;three older750-752 drafts remain pending. '
        'All remaining shared/route/player prose and raw-source coverage revisit stay open;graphics and all18 plaques remain separately unfinished. Full goal active.')
    assert sum(ledger['completed_editorial_record_counts_by_file'].values()) == 634
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values()) == 637
    assert ledger['unresolved_graphics_work'] == read(ROOT / 'editorial_ledger_before_completion.json')['unresolved_graphics_work']
    save(LEDGER, ledger)
    DOC.write_text(f'''# V831: Refit help editorial completion

All31 help descriptions (1247-1255 and1268-1289) are reviewed against clean
Japanese:18 revised and13 retained. Full source/current references, glosses,
decisions and generated lines are in `{REVIEW}`. Spoken1256-1267 and separate
HELP articles are outside this family and remain part of the wider review.

## Meaning and formatting

The revisions clarify cure versus treatment, slower fatigue, following winds,
alternative stern fittings and the final sail's square-sail identity. All room
limits, equipment names and directional restrictions are preserved. Four initial
single-word tails were resolved through natural prose, without authored breaks
or alignment. All31 current native complete font planes match562464 independent
pixels with complete leading/trailing letters, guarded buffers and blank later
heading/detail rows.

The original block16 would be4098 bytes, four beyond the4096-byte cache bound.
Complete native selections are repacked in existing blocks16-18;403 selections
move,18 text strings change and3650 remain exact. All opaque spans and the other
38 blocks are exact. All7336 native warm/cold copies pass. Only COMMON and ARM9
directory/offset metadata differ from V829. Executable code, fonts, BSS, memory
bounds, caches and the123040-byte late payload remain unchanged. All graphics,
HELP, SC0-SC3 (including the V829 cliff fix), ARM7 and overlays are exact.

## Actual emulator verification

Paired20600-frame cold boots use an unmodified disposable copy of the existing
five-ship Copenhagen test save; no new gameplay RAM/code fixture or savestate.
23 complete help holds cover13 distinct messages, including9 revised texts.
Independent glyph/background models match every pixel of all62 captured screen
pairs. All first/final glyph erasure controls fail as expected. Entry, normal
cancel, Shipwright and Port return pass;five ship models and25975 funds match
at six checkpoints. Seven ordinary4000-frame startup/New Game capture pairs
without a save or fixture match. This is targeted testing, not31 ordinary visits,
a full playthrough or hardware verification. All31 have controlled native tests.
The12-screen actual contact sheet is visually reviewed.

An initial verifier called the fleet helper with the wrong arguments. Its
signature was corrected, capture RAM hashes checked, and verification rerun on
the same terminal captures; no successful emulator run was restarted or retimed.

## Registered release

- Candidate: `E:/Rota Nova translations/Generated/out/{ROM.name}`
- SHA-256: `{candidate['sha256']}`
- Profile: `all-routes-unified-v831` (experimental, not canonically promoted).
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`.
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- All471 batches and114 accepted layers retained; prior profiles untouched.
- Changed internal components relative to V829: `/COMMON/MESFILE.DK4`, `/__arm9__.bin` metadata.
- Exact clean-input patch: `{ROM.with_suffix('.xdelta').name}`.
- Patch SHA-256: `{release['patch_sha256']}`.
- Clean input SHA-256: `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

The registered binary verifier replays the late stage, checks complete preservation
and prior registry ancestry, rejects wrong source COMMON/ARM9 and stale current
records, and reconstructs every candidate byte from the clean-input patch.
The neighboring manifest and `registered_release_verification.json` record the
full stack. Human cold-boot acceptance remains required before canonical promotion.
For that review, inspect New Game and Refit equipment/room descriptions and exit.

## Remaining work

634 completed entries (456 revised/178 retained),637 source/prose reviewed,
three older750-752 drafts pending. Remaining shared, all other route/player prose,
and the raw-source coverage revisit stay open. Graphics and all18 plaques remain
separately unfinished. The older record-based checks must be revisited after the
full goal. Source/manuscript/proofs and guide-candidate captures are archived on E:.
''', encoding='utf-8')
    paragraph = '\n\n## V831: Refit help editorial completion\n\n' + ledger['latest_checkpoint'] + ' See [V831 evidence](refit_editorial_v831_completion.md).\n'
    for path in ('docs/translation_progress.md', 'docs/editorial_review_goal.md', 'docs/todo.md', 'docs/known_issues.md'):
        with Path(path).open('a', encoding='utf-8') as handle:
            handle.write(paragraph)
    GUIDE.mkdir(parents=True, exist_ok=True)
    guide = []
    for frame in (13100, 13400, 14000, 14300, 14900, 15200, 16100, 16400):
        source = CAP / 'refit_editorial_v831_after' / f'frame_{frame:06d}_cold_boot.png'
        target = GUIDE / source.name
        copy2(source, target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        guide.append({'frame': frame, 'path': str(target), 'sha256': sha(target.read_bytes())})
    save(GUIDE / 'capture_provenance.json', {
        'candidate': str(ROM), 'candidate_sha256': candidate['sha256'], 'screenshots': guide,
        'source_report': str(CAP / 'refit_editorial_v831_after/capture_report.json'),
        'disclosure': 'Actual cold-boot Refit screenshots using an isolated five-ship Copenhagen test save. No new gameplay RAM/code fixture;not earned fleet or route progress. Native256x384 captures,byte-exact copies.',
        'guide_candidates_only': True})
    sources = [Path(__file__), Path('scripts/build_integrated_release.py'), Path(CONFIG), MANUSCRIPT, REVIEW, DOC, LEDGER,
               Path('translations/release_stack.json'), ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
               Path('dk4tool/patch/refit_help_editorial.py'),
               *map(Path, ('scripts/prepare_refit_release_v831.py', 'scripts/run_refit_release_v831.py', 'scripts/verify_refit_release_v831.py', 'scripts/verify_refit_gameplay_v831.py')),
               *ROOT.glob('*.json'), *ROOT.glob('*.png')]
    sources += list(map(Path, ('docs/translation_progress.md', 'docs/editorial_review_goal.md', 'docs/todo.md', 'docs/known_issues.md')))
    program = {str(p): sha(p.read_bytes()) for p in sources}
    save(ROOT / 'source_program_manifest.json', program)
    sources.append(ROOT / 'source_program_manifest.json')
    archived = []
    for source in sources:
        target = ARCHIVE / source.absolute().relative_to(Path.cwd())
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        archived.append({'source': str(source), 'archive': str(target), 'sha256': sha(target.read_bytes())})
    save(ROOT / 'archive_manifest.json', {'archive': str(ARCHIVE), 'files': archived, 'all_copies_hash_verified': True,
                                         'ROM_already_stored_on_E': str(ROM), 'guide_candidates': guide,
                                         'previous_goal_turn_classification': 'progress:V830 source/prose/native review of31 Refit messages',
                                         'this_goal_turn_classification': 'progress:registered combined ROM,exact patch,actual panels and31-entry completion'})
    copy2(ROOT / 'archive_manifest.json', ARCHIVE / 'archive_manifest.json')
    print('V831 recorded:634 complete/637 source-prose/3 pending;8 guide captures and archive hashes verified. Goal active.', flush=True)


if __name__ == '__main__':
    main()
