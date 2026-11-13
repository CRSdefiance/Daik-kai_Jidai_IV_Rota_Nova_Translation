"""Record the reviewed dialogue family and preserve exact release/test provenance."""

from copy import deepcopy
from pathlib import Path
from shutil import copy2

from dk4tool.patch import refit_dialogue_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_refit_release_v834 import ROOT, MANUSCRIPT
from scripts.verify_refit_release_v834 import ROM
from scripts.verify_village_wrap_v608 import read, save

LEDGER = Path('translations/editorial_review_current_v1.json')
REVIEW = Path('translations/refit_dialogue_editorial_final_review_v1.json')
DOC = Path('docs/refit_dialogue_v834_completion.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V834 Refit dialogue completion')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V834 Refit dialogue')
CAP = Path('work/emulation_v193')


def reference(e):
    return {k: getattr(e, k) for k in ('message_id', 'block', 'table_offset', 'block_offset', 'copy_end', 'record_index', 'start', 'end')}


def main():
    assert not REVIEW.exists() and not DOC.exists()
    release, gameplay = [read(ROOT / name) for name in ('registered_release_verification.json', 'actual_gameplay_verification.json')]
    ledger, manuscript = read(LEDGER), read(MANUSCRIPT)
    assert ledger['records_editorially_completed'] == 634 and ledger['records_with_source_and_prose_pass'] == 649
    assert release['candidate_sha256'] == gameplay['candidate_sha256'] == sha(ROM.read_bytes())
    assert len(gameplay['actual_complete_dialogue_holds']) == 10
    assert len({r['message_id'] for r in gameplay['actual_complete_dialogue_holds']} - {1246}) == 6
    assert sha(Path(gameplay['review_sheet']).read_bytes()) == gameplay['review_sheet_sha256']
    # The actual12-screen sheet and individual helper/price/duration/exit frames
    # were opened after the independent glyph/whole-screen checks passed.
    gameplay.update(visual_review_pending=False, visual_review={
        'actual12_screen_sheet_opened_and_reviewed': True,
        'complete_helper_discount_duration_Rename_lines_and_normal_Port_return_reviewed': True,
        'source_hiragana_keyboard_characters_retained_as_selectable_name_input': True,
        'all12_controlled_native_fonts_previously_reviewed_in_V833': True})
    save(ROOT / 'actual_gameplay_verification.json', gameplay)
    release.update(actual_panel_and_startup_verification_pending=False,
                   actual_gameplay_proof=str(ROOT / 'actual_gameplay_verification.json'),
                   actual_gameplay_proof_sha256=sha((ROOT / 'actual_gameplay_verification.json').read_bytes()))
    save(ROOT / 'registered_release_verification.json', release)
    save(ROOT / 'editorial_ledger_before_completion.json', ledger)
    rom = NdsImage.open(ROM)
    common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    entries = owned.current_entries(common, arm)
    fonts = read('work/analysis/refit_dialogue_v833/native_font_proof.json')
    assert not fonts['visual_review_pending'] and not fonts['findings'] and fonts['matrix_case_count'] == 525
    records = []
    existing = {n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs', [])}
    assert not existing.intersection(owned.IDS)
    for r in manuscript['records']:
        n = r['message_id']
        assert entries[n].text == owned.compiled(r) and all(r['review'].values())
        records.append({**deepcopy(r), 'completed_candidate_reference': str(ROM),
                        'before_reference': r['current_reference'], 'before_text_hex': r['current_text_hex'],
                        'current_reference': reference(entries[n]), 'current_text_hex': entries[n].text.hex(),
                        'decision': 'revised-and-integrated' if r['editorial_decision'] == 'revise' else 'retained-and-editorially-reviewed',
                        'generated_native_examples': [p['case'] for p in fonts['complete_native_font_planes'] if p['case']['message_id'] == n],
                        'actual_display_holds': [p for p in gameplay['actual_complete_dialogue_holds'] if p['message_id'] == n],
                        'all_native_quantities_complete_fonts_and_original_loader_coverage': True})
    assert sum(r['editorial_decision'] == 'revise' for r in records) == 11
    final = {'format': 'dk4-editorial-family-final-review-v1',
             'status': '12-source-context-editorial-native-and-representative-actual-verified',
             'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'source_manuscript': str(MANUSCRIPT), 'source_manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
             'registered_release_proof': str(ROOT / 'registered_release_verification.json'),
             'actual_gameplay_proof': str(ROOT / 'actual_gameplay_verification.json'),
             'all7336_original_warm_cold_native_copies_pass': True,
             'all525_native_printf_quantity_paragraph_cases_and26_complete_fonts_pass': True,
             'actual_scope': gameplay['scope'], 'records': records,
             'full_editorial_goal_complete': False, 'separate_graphics_goal_complete': False}
    save(REVIEW, final)
    family = {'id': 'Shared-Refit-helper-discount-Rename-duration1256-1267',
              'native_message_IDs': list(owned.IDS), 'records': records, 'final_review': str(REVIEW),
              'documentation': str(DOC), 'actual_verification_scope': gameplay['scope']}
    ledger['completed_editorial_families'].append(family)
    ledger['records_editorially_completed'] = 646
    ledger['records_revised_and_integrated'] = 467
    ledger['retained_wordings_editorially_completed'] = 179
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4'] = 645
    ledger['reviewed_but_incomplete_COMMON_IDs'] = [750, 751, 752]
    ledger['active_source_prose_drafts'] = {
        'native_message_IDs': [750, 751, 752],
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],
        'status': 'three-older-context-unmapped-drafts',
        'note': 'These are reviewed drafts only,not the full remaining scope. Refit12 completes in V834;unreviewed shared/route/player prose and raw-source coverage stay open.'}
    ledger['previous_current_integrated_candidate_V831'] = deepcopy(ledger['current_integrated_candidate'])
    candidate = {'path': str(ROM), 'sha256': sha(ROM.read_bytes()), 'profile': 'all-routes-unified-v834',
                 'MESFILE_sha256': sha(common), 'ARM9_sha256': sha(arm),
                 'patch': str(ROM.with_suffix('.xdelta')), 'patch_sha256': release['patch_sha256'],
                 'manifest': str(ROM.with_suffix('.manifest.json')),
                 'status': 'experimental-Refit12-editorially-native-and-representative-gameplay-verified',
                 'details': str(DOC), 'full_goal_complete': False}
    ledger['current_integrated_candidate'] = candidate
    ledger['source_pins']['current'] = deepcopy(candidate)
    ledger['next_integrated_profile_for_goal_continuation'] = candidate['profile']
    ledger['native_relocation_reference_before_V834'] = deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_native_relocation_reference'] = {
        'candidate': str(ROM), 'COMMON_sha256': sha(common), 'ARM9_sha256': sha(arm),
        'parser': 'dk4tool.patch.refit_dialogue_editorial.current_entries', 'release_config': owned.CONFIG,
        'source_locked_directory_and_all3668_selections_verified': True}
    ledger['refit_dialogue_v834'] = {k: final[k] for k in ('status', 'actual_scope', 'registered_release_proof', 'actual_gameplay_proof')}
    ledger['refit_dialogue_v834'].update(final_review=str(REVIEW), documentation=str(DOC), full_goal_complete=False)
    for key in ('refit_dialogue_v832', 'refit_dialogue_v833'):
        ledger[key]['superseded_by_completion'] = str(REVIEW)
    ledger['coverage_units'].append({'id': family['id'], 'status': 'completed',
                                     'native_message_IDs': list(owned.IDS), 'final_review': str(REVIEW),
                                     'scope': 'Refit dialogue consumer family;all other shared/route/player prose remain open.'})
    checkpoint = (
        'V834 completes12 Refit dialogue entries1256-1267:11 natural revisions and1 justified retention. '
        'Source208 voice selections and original fallback,10 discount contracts,all256 day quantities,525 native layout/printf cases,26 full glyph planes and7336 warm/cold original copies pass. '
        'Paired18300-frame cold boots use a disclosed three-byte Gerhard room/role fixture:actual6% discount,2000 quote,1880 charge,2 days/96 ticks and normal Port return match. '
        'Ten complete holds cover6 current-family IDs plus earlier1246;all22 helper frames and11 ordinary Rename frames match complete expected models,including original keyboard/cancel,with7 ordinary no-save New Game frames exact. '
        'Registered combined V834 and exact clean-input patch preserve471 batches,114 accepted layers,all3656 other strings,opaque payloads,graphics/scripts and fixed123040 staged bytes. '
        '646 entries complete (467 revised/179 retained),649 source/prose reviewed;three reviewed750-752 drafts and all remaining unreviewed shared/route/player prose/raw coverage remain. '
        'Separate graphics and all18 plaques remain unfinished;older record-based checks remain scheduled after the full goal. Full goal active.')
    ledger['latest_checkpoint'] = checkpoint
    assert sum(ledger['completed_editorial_record_counts_by_file'].values()) == 646
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values()) == 649
    assert ledger['unresolved_graphics_work'] == read(ROOT / 'editorial_ledger_before_completion.json')['unresolved_graphics_work']
    assert not ledger['full_goal_complete']
    save(LEDGER, ledger)
    save('out/editorial_review_latest.json', candidate)
    DOC.write_text(f'''# V834: Refit dialogue editorial completion

All12 shared Refit dialogue entries1256-1267 are reviewed against clean Japanese:
11 revisions and1 justified retention. Exact source/current references, glosses,
voice classes, argument contracts and individual decisions are in `{REVIEW}`.
The source Admiral address and companion voices are preserved. The source IC
first-person pronoun in1257 becomes English I; it is not a deleted character name.
The native missing class1 slot retains its original first-valid1256 fallback.
The percentage discount precedes a separate final-price confirmation.

## Formatting and bounded runtime

Prose is one paragraph without authored alignment or manual breaks. Exact
declared consumers now wrap complete words after substitutions.1263 retains its
single percentage argument/literal percent;1267 receives1 day/plural days through
one additional original Number return. The source runtime tests cover208 actor
selections,10 discount cases,256 duration values,525 layout/printf cases and26
complete native/independent font planes. All were visually reviewed in V833.

The complete late stage is replayed against exact V831. COMMON blocks16-40
repack2467 native selections;all3656 other text strings and opaque payloads stay
exact. All7336 complete original warm/cold copies pass. V833's lossless174-to176
byte dispatch table shares the existing384-byte data allocation with the shorter
ceremony filter;the164-byte gate,104-byte quantity formatter,128-byte modal
wrapper,sections/BSS/cache/arena and123040-byte staged payload do not grow.
All earlier quantity/status/modal/scope and eight-caller reference proofs pass.

## Actual emulator evidence

Two terminal18300-frame cold boots use protected disposable save copies and
identical input schedules. The sole gameplay fixture changes3 bytes to move
existing Gerhard16 from assignment slot7 to an existing empty room18 and give
that room the native role13 type. His real ability31,voice1,HP,XP,money,computed
cost,duration,quests and all other RAM are untouched at insertion. Original
native logic selects1256 and calculates6%. The2000 quote becomes1880;funds
25975→24095 and the calendar6871→6967 match both builds. Actual2 days therefore
consume96 ticks. Normal Refit cancel,Shipwright and Port returns are observed.

Ten complete dialogue holds cover six of the12 family IDs plus earlier1246.
Every actual native glyph,first/final letter,substituted number and blank ink
matches an independent font model. All22 helper frames and11 ordinary Rename
frames match complete two-screen models. Seven ordinary New Game frames with
no save/fixture are exact. The Rename sequence preserves five ship names,Hull,
Crew,money and calendar,including keyboard/cancel. The hiragana keyboard entries
are selectable name-input characters;its English instructions remain intact.
This is representative controlled scene verification,not all voice visits,
earned assignments,a full playthrough or hardware verification.

The12-screen contact sheet and individual helper,discount,price,duration and
exit captures were opened and visually reviewed. One paper position is always
covered by verified ink across all witnesses;its glyph is proved in every model
and no unobserved paper colour is claimed. The Yes/No price footer is kept as an
exact whole-frame control,not used as a plain-paper witness. Rename14000 is the
normal return to revised1264 after cancelling the keyboard,not an animation
exception. Early verifier assumptions were corrected on the same captures;
no successful run was restarted or retimed. Initial fixture slot/voice assumptions
were also rejected before gameplay;the donor's actual slot7,ability31,voice1
and original1256 fallback were used.

## Registered release

- Candidate: `E:/Rota Nova translations/Generated/out/{ROM.name}`
- SHA-256: `{candidate['sha256']}`
- Profile: `{candidate['profile']}` (experimental;canonical not promoted).
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`.
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- All471 inherited batches and114 accepted layers retained,plus the registered late Refit dialogue stage;prior profiles unchanged.
- Changed components relative to V831: `/COMMON/MESFILE.DK4`, `/__arm9__.bin` metadata and bounded runtime.
- Exact clean-input patch: `{ROM.with_suffix('.xdelta').name}`.
- Patch SHA-256: `{release['patch_sha256']}`.
- Clean input SHA-256: `{release['clean_input_sha256']}`.

The release verifier replays exact target bytes,checks inherited manifests and
all graphics/HELP/SC0-SC3/ARM7/overlays,tests wrong sources/stale records/manual
spacing/breaks/format arguments,and reconstructs every ROM byte from the patch.
The screenshot676/677 formatting fix is rechecked in current V831 and V834:
same repaired text,wrapping and complete glyph planes. The earlier V747 actual
shop screenshot remains its scene evidence;no new shop activation is claimed.
Human cold-boot acceptance remains necessary before canonical promotion.

## Progress and storage

{checkpoint}

ROM,patch,reconstruction,proofs and all167 new capture files are on E:. Capture
folders retain local junctions and every moved file hash was verified. Guide
candidates are native256x384 byte-exact copies with fixture/source provenance.
''', encoding='utf-8')
    paragraph = '\n\n## V834: Refit dialogue editorial completion\n\n' + checkpoint + ' See [V834 evidence](refit_dialogue_v834_completion.md).\n'
    for path in ('docs/translation_progress.md', 'docs/editorial_review_goal.md', 'docs/todo.md', 'docs/known_issues.md'):
        with Path(path).open('a', encoding='utf-8') as handle:
            handle.write(paragraph)
    GUIDE.mkdir(parents=True, exist_ok=True)
    guide = []
    for case, frame in [('helper_after', f) for f in (14200, 14700, 15500, 16300)] + [('rename_after', f) for f in (12800, 13400)]:
        source = CAP / f'refit_dialogue_v834_{case}' / f'frame_{frame:06d}_cold_boot.png'
        target = GUIDE / f'{case}_{source.name}'
        copy2(source, target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        guide.append({'case': case, 'frame': frame, 'path': str(target), 'sha256': sha(target.read_bytes())})
    save(GUIDE / 'capture_provenance.json', {
        'candidate': str(ROM), 'candidate_sha256': candidate['sha256'], 'screenshots': guide,
        'source_reports': gameplay['receipts'], 'guide_candidates_only': True,
        'disclosure': 'Native256x384 byte-exact actual cold-boot captures. Helper uses an isolated3-byte room/role assignment fixture;Rename has no new RAM fixture. Both use disposable copies of a preexisting test save. Not earned route/fleet progress.'})
    sources = {Path(__file__), Path('scripts/build_integrated_release.py'), Path(owned.CONFIG), MANUSCRIPT, REVIEW, DOC, LEDGER,
               Path('translations/release_stack.json'), ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
               Path('dk4tool/patch/refit_dialogue_editorial.py'), Path('scripts/verify_refit_release_v834.py'),
               Path('scripts/verify_refit_gameplay_v834.py'), Path('scripts/verify_user_formatting_v834.py'),
               Path('scripts/prepare_refit_release_v834.py'), Path('scripts/run_refit_release_v834.py'),
               Path('scripts/run_refit_fixture_adapter_v834.py'), Path('scripts/native_refit_fixture_v834.py'),
               Path('work/analysis/dialogue_formatting_user_recheck_v834/COMMON676_677.json'),
               *ROOT.glob('*.json'), *ROOT.glob('*.png')}
    sources.update(map(Path, read(owned.CONFIG)['dependencies']))
    sources.update(map(Path, ('docs/translation_progress.md', 'docs/editorial_review_goal.md', 'docs/todo.md', 'docs/known_issues.md')))
    save(ROOT / 'source_program_manifest.json', {str(p): sha(p.read_bytes()) for p in sorted(sources)})
    sources.add(ROOT / 'source_program_manifest.json')
    archived = []
    for source in sorted(sources):
        target = ARCHIVE / source.absolute().relative_to(Path.cwd())
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        archived.append({'source': str(source), 'archive': str(target), 'sha256': sha(target.read_bytes())})
    save(ROOT / 'archive_manifest.json', {'archive': str(ARCHIVE), 'files': archived, 'all_copies_hash_verified': True,
                                        'ROM_already_stored_on_E': str(ROM), 'guide_candidates': guide,
                                        'previous_goal_turn_classification': 'progress:current screenshot fix rechecked and persistent formatting watch updated',
                                        'this_goal_turn_classification': 'progress:registered Refit dialogue ROM/patch,actual scenes and12 entries completed',
                                        'full_goal_complete': False})
    print('V834 recorded:646 completed,467 revised179 retained;649 source/prose reviewed,3 reviewed drafts pending. Full goal and separate graphics remain open.', flush=True)


if __name__ == '__main__':
    main()
