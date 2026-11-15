"""Record verified integration and one actual sample without completing the batch."""

import shutil
from dataclasses import asdict
from pathlib import Path

from dk4tool.patch import item_diplomacy_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.register_item_release_v788 import MANUSCRIPT, CONFIG, ROOT
from scripts.verify_item_release_v788 import ROM
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/item_diplomacy_v788_checkpoint.md')
LEDGER = Path('translations/editorial_review_current_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V788 Item and diplomacy integrated candidate')
SUMMARY = (
    'V788 integrates76 source/prose-reviewed item/diplomacy paragraphs(63 revised/13 retained),'
    'six complete nominal document names and the24-cell shared name-width repair. All3592 other '
    'strings,opaque spans,470 batches,114 accepted layers and prior graphics are retained. '
    '7336 full native copies,2774 original-entry layouts,76 independent font planes,1260 Guild '
    'wrapper bindings,ten real role bindings,12 rejection gates and exact clean-input patch pass. '
    'Actual revised1071 has complete glyphs,17 screen controls,14 persistent-state controls and '
    'normal town return;seven ordinary New Game pairs pass. Frozen parser,old configs/producers '
    'and prior profiles remain exact. Bargaining/diplomacy eligibility,economic/document outcomes '
    'and actual SDK/GPU letter-name menus remain open.417 completed,496 source/prose,79 pending; '
    'no new completed-entry credit. Experimental;full editorial and separate graphics goals unfinished.'
)


def main():
    verification = read(ROOT/'registered_verification.json')
    gameplay = read(ROOT/'Guild_gameplay_verification.json')
    patch = read(ROOT/'patch_proof.json')
    assert verification['candidate_sha256'] == gameplay['candidate_sha256'] == patch['candidate_sha256'] == sha(ROM.read_bytes())
    assert all(verification['negative_gates'].values()) and len(verification['negative_gates']) == 12
    assert gameplay['actual_revised_COMMON1071_complete_hold']['frame'] == 7200
    assert len(gameplay['all17_screen_controls']) == 17 and len(gameplay['all14_persistent_state_model_object_controls']) == 14
    assert len(read(ROOT/'newgame_regression.json')['whole_screen_frame_pairs']) == 7
    assert patch['byte_exact_reconstruction']
    for name, expected in read(ROOT/'frozen_prior_dependencies.json').items():
        assert sha(Path(name).read_bytes()) == expected, name
    cfg = read(CONFIG)
    for name, expected in cfg['dependencies'].items(): assert sha(Path(name).read_bytes()) == expected, name
    rom = NdsImage.open(ROM)
    common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    entries = owned.current_entries(common, arm)
    mapping = ROOT/'complete_native_message_map_v788.json'
    save(mapping, {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'COMMON_sha256': sha(common), 'ARM9_sha256': sha(arm), 'directory_sha256': owned.DIRECTORY,
        'exact_versioned_reader': 'dk4tool.patch.item_diplomacy_editorial.current_entries',
        'frozen_shared_parser_does_not_globally_accept_this_directory': True,
        'entries': [{**asdict(e), 'text': e.text.hex()} for e in entries]})

    # A verified actual prompt is useful guide material. It remains a guide
    # candidate, and this single screen does not certify the full76-entry batch.
    capture = Path('E:/Rota Nova translations/Generated/work/emulation_v193/item_v788_guild')
    screenshot = capture/'frame_007200_cold_boot.png'
    guide = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V788 Guild item selection.png')
    guide.parent.mkdir(parents=True, exist_ok=True)
    if guide.exists(): assert guide.read_bytes() == screenshot.read_bytes()
    else: shutil.copy2(screenshot, guide)
    save(ROOT/'guide_candidate_receipt.json', {'source': str(screenshot), 'copy': str(guide),
        'PNG_sha256': sha(screenshot.read_bytes()), 'copy_SHA256': sha(guide.read_bytes()),
        'candidate_sha256': sha(ROM.read_bytes()), 'capture_report': str(capture/'capture_report.json'),
        'capture_report_sha256': sha((capture/'capture_report.json').read_bytes()),
        'actual_unmodified_save_cold_boot_no_fixtures': True, 'actual_frame': 7200,
        'complete_glyph_and_paper_bounds_verified': True, 'whole_batch_completion_claim': False})

    DOC.write_text(f'''# V788: item and diplomacy integration, first actual revised scene

## Status and remaining scope

Experimental registered profile `all-routes-unified-v788` builds all76 reviewed
COMMON1070-1145 paragraphs, including63 revisions and13 retained wordings. The six
nominal diplomatic document names and24-cell shared name-width repair are included.
The full batch remains incomplete: actual buy/sell/bargaining outcomes, diplomatic
entry/eligibility and document lifecycle, remaining name consumers, and actual
SDK/GPU document menus still need verification. No new editorial completion credit
is awarded. Coverage stays417 complete(293 revised/124 retained),496 source/prose,
and79 pending IDs(750-752 and1070-1145). Continue1146 onward and every route/other prose.
The full editorial goal and separate graphics audit remain active and unfinished.

## Source, prose and original consumers

The clean Japanese source, neighbors and exact source/current records remain pinned
in the frozen V784 manuscript. V2 keeps all prose/glosses unchanged and records
completed native formatting with separate pending gameplay gates. Natural American
English preserves the original intents: insufficient-funds1072 is no buy question;
1097 charges a1000-coin service fee;16 older irrelevant faction-choice lines have
their real drafting,absence or submission-warning meaning restored. Roles1/3 are
First Mate/Purser. IC1118/1140 remain original first-person pronouns.

V788 executes1260 original direct Guild wrapper bindings across90 town objects,
ten real role/voice wrappers and a null-actor system control. Distinct two-argument
sentinels prove original ordering; earlier2080 native voice selections bind the
remaining alternatives. Ninety object lookups do not assert that every town has a
Guild or that every faction/amount stress input is eligible. The sole mocked
boundary in these wrapper tests is message loading to exact research entries;
original speaker providers and core branches execute normally.

The first wrapper probe confused an actor index with an actor pointer. It failed
before receiving coverage and was corrected to execute the original sentinel and
index-to-pointer rule. Copy harness arguments0-40 are explicit. The first two
emulator launch attempts rejected capture interval0 before emulator execution;
the completed runs use99999 plus exact capture frames. These failures receive no
gameplay credit.

## Full prose within existing storage

The new paragraphs add788 bytes; existing individual blocks14/15 cannot fit them.
The smallest fitting contiguous window is existing blocks14-40. Complete messages
are repacked without shortening prose. All3592 other text strings, all14 outside
blocks and both opaque native post-NUL spans remain exact. Every one of3668
original selections passes complete cold/warm copies:7336 cases across41 reports.
Existing section sizes,BSS,cache,startup,arena and123040-byte staged payload geometry
do not grow. No new executable storage is taken from unrelated data.

All2774 layouts run through original target01FFCF3C,trampoline and scoped dispatcher.
They exactly match reviewed native prototypes;all76 complete font planes match an
independent font decoder and the reviewed images. Leading/trailing letters,whole
words,substitution order,margins,bounds and guards are checked. Native source calls,
not arbitrary helper selection,determine each dispatch key.

The private selector/status changes and source-owned nominal name placements retain
their V785-V787 ownership,reference and ABI evidence. Complete names are goodwill
letter,pact proposal,pact termination notice,truce proposal,declaration of war and
demand for submission. Types6-9 and all57 earlier village/Deck labels remain exact.
The shared name-width method reports24 cells,including the paired blank cell;
native list geometry and bitmap rows are verified. Actual SDK allocation/GPU menu
and remaining virtual consumers remain open.

## Registered layer and reproducibility

The new stage follows the entire unchanged V783 profile. Its explicit versioned
reader accepts only directory `{owned.DIRECTORY}`;the frozen shared parser and all
prior pinned configs/producers/profiles are unchanged. Future work on this candidate
must use `dk4tool.patch.item_diplomacy_editorial.current_entries`;the global parser
intentionally does not accept this directory. The complete3668 map is recorded in
`work/analysis/item_diplomacy_integration_v788/complete_native_message_map_v788.json`.

Candidate:`{ROM}`
SHA256:`{sha(ROM.read_bytes())}`
COMMON:`{sha(common)}`
ARM9:`{sha(arm)}`
Patch:`{patch['patch']}`
Patch SHA256:`{patch['patch_sha256']}`

The canonical baseline is unchanged:`out/raphael_natural_v2_accepted_base.nds`,
SHA256`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
Clean input SHA256`f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
The exact clean-input patch reconstructs the candidate byte for byte. All470 batches,
114 accepted layers and prior graphics remain. Only `/COMMON/MESFILE.DK4` and
`/__arm9__.bin` differ from V783. Twelve negative review,source,argument,prose and
alignment cases reject invalid inputs. No canonical promotion,commit or push occurs.

## Targeted actual emulator verification

Both DeSmuME/libretro runs are terminal and use the unchanged original harness,
ordinary cold boot, no savestates and no gameplay fixtures. The seven no-save
startup/New Game frames match the earlier reference exactly,including title,
character selection and opening story. This is a targeted test,not a route playthrough
or physical-device verification.

The8400-frame Guild run replays the exact earlier controller/stylus schedule with
an isolated byte-exact Maria Seoul save copy. At7200 the actual Guildmaster displays
the revised1071 `Which one would you like?` with its complete source template,
resident block,printf/wrapped buffers and full independent glyph mask. The prompt,
paper,margins and complete first/last letters were visually inspected. Seventeen
screen controls pass;only the reviewed ink rectangle is excluded at7200. Fourteen
paired financial/model/persistent-object snapshots match. Money stays38816 coins;
cancel returns normally to town at8400 with company,fleet,ships,actors,towns,items
and goods unchanged. Other75 entries receive no actual-hold credit from this scene.

The verified actual screenshot is saved as a guide candidate at `{guide}` with a
source/hash receipt. Native CPU previews are not promoted as gameplay screenshots.

## Earlier formatting and preserved decisions

User-reported676/677 retain exact repaired ROM bytes and original native wrapping.
The V747 actual cooking-pitch capture remains their actual reference;no fresh V788
activation of those shop pitches is claimed. Consistent visible margins,internal
gaps,stray adjacent words,complete letters,bounds,pagination and normal dismissal
remain ongoing checks for every family. All original18 plaques remain open in
the separate graphics audit. Preserve the Online screenshot-body exclusion,brown
comic marks and locked Rafael/Joakim/Maria/Camille decisions. Revisit older
record-based checks after the full editorial goal is complete.

Reproduce with prepare_item_common_v788.py,verify_item_consumers_v788.py,
verify_item_copies_v788.py --first-block 0 --last-block 40,probe_item_production_v788.py,
register_item_release_v788.py and the registered build/verification scripts.
Registration is one-shot;rebuild an existing profile directly through
build_integrated_release.py --profile all-routes-unified-v788 --out <new output>.
''', encoding='utf-8')
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 417 and ledger['records_with_source_and_prose_pass'] == 496
    assert len(ledger['active_source_prose_drafts']['native_message_IDs']) == 79
    save(ROOT/'editorial_ledger_before_v788.json', ledger)
    latest = {'path': str(ROM), 'sha256': sha(ROM.read_bytes()), 'profile': 'all-routes-unified-v788',
        'MESFILE_sha256': sha(common), 'ARM9_sha256': sha(arm), 'patch_sha256': patch['patch_sha256'],
        'manifest': str(ROM.with_suffix('.manifest.json')), 'status': 'experimental', 'details': str(DOC),
        'supplemental_verification': str(ROOT/'Guild_gameplay_verification.json'),
        'remaining_in_this_registered_batch': '; '.join(gameplay['remaining_batch_gates']),
        'full_goal_complete': False, 'latest_research_checkpoint': str(DOC)}
    ledger['previous_whole_batch_verified_candidate_V783'] = ledger['current_integrated_candidate']
    ledger['current_integrated_candidate'] = latest
    ledger['latest_checkpoint'] = SUMMARY
    ledger['current_native_relocation_reference'] = str(mapping)
    ledger['active_source_prose_drafts'].update({'status': '750-752-context-unmapped;1070-1145-native-reviewed-integrated-actual-batch-gameplay-pending',
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json', str(MANUSCRIPT)],
        'note': '76 paragraphs are integrated and native-formatting approved;only1071 has a new actual hold.79 IDs remain pending completion. Six nominal English names and24-cell width are in V788;actual menus and diplomatic eligibility/lifecycle remain open.'})
    ledger['formatting_watchlist']['latest_reference_proof'] = str(ROOT/'user676_677_preserved.json')
    ledger['formatting_watchlist']['reference_case'] += ' V788 exact repaired676/677 ROM bytes and original native wrapping preserved;no new activation of those shop pitches claimed.'
    ledger['coverage_units'][0]['next'] = ('Verify V788 actual buy/sell/bargain economic outcomes,diplomacy eligibility and document lifecycle,actual SDK/GPU nominal-name menus and remaining consumers. Then1146 onward,750-752,all routes and remaining prose;graphics audit and older-record follow-up remain open.')
    checkpoint = {'id': 'V788-item-diplomacy-integrated-first-actual-scene', 'documentation': str(DOC),
        'new_editorially_completed': 0, 'integrated_native_reviewed_records': list(owned.IDS),
        'actual_new_hold_IDs': [1071], 'native_layouts': 2774, 'full_native_copies': 7336,
        'negative_gates': 12, 'remaining_gates': gameplay['remaining_batch_gates'], 'full_goal_complete': False}
    ledger['research_checkpoints'].append(checkpoint)
    ledger['goal_status'] = 'active'
    save(LEDGER, ledger)
    save('out/editorial_review_latest.json', latest)
    heading = '## V788: item and diplomacy integrated; first revised Guild scene verified'
    for name in ('docs/known_issues.md', 'docs/todo.md', 'docs/translation_progress.md', 'docs/editorial_review_goal.md'):
        path = Path(name)
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text+'\n\n'+heading+'\n\n'+SUMMARY+' See [V788 checkpoint](item_diplomacy_v788_checkpoint.md).\n', encoding='utf-8')
    sources = [p for p in ROOT.rglob('*.json') if p.name != 'archive_receipt.json']
    sources += [DOC, LEDGER, CONFIG, MANUSCRIPT, Path('translations/release_stack.json')]
    sources += [Path('scripts')/name for name in ('prepare_item_common_v788.py', 'verify_item_consumers_v788.py',
        'verify_item_copies_v788.py', 'probe_item_production_v788.py', 'register_item_release_v788.py',
        'verify_item_release_v788.py', 'verify_item_gameplay_v788.py', 'record_item_integration_v788.py')]
    sources += [Path('dk4tool/patch/item_diplomacy_editorial.py'), Path('scripts/build_integrated_release.py')]
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    archived = []
    for src in sources:
        destination = ARCHIVE/src
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, destination)
        digest = sha(src.read_bytes())
        assert sha(destination.read_bytes()) == digest
        archived.append({'source': str(src), 'copy': str(destination), 'sha256': digest})
    receipt = {'archive': str(ARCHIVE), 'copies': archived, 'all_copies_SHA256_exact': True}
    save(ROOT/'archive_receipt.json', receipt)
    save(ARCHIVE/'archive_receipt.json', receipt)
    save(ROOT/'checkpoint.json', {**checkpoint, 'candidate': latest, 'completed_records': 417,
        'source_prose_reviews': 496, 'pending_records': 79, 'frozen_prior_dependencies_preserved': True,
        'all_capture_processes_terminal': True, 'graphics_audit_separate_and_unfinished': True,
        'previous_goal_turn_classification': 'progress:verified the reported formatting example against current ROM and actual reference',
        'this_turn_classification': 'progress:registered combined ROM,exact patch,complete native verification and actual revised Guild/startup controls',
        'producer_sha256': sha(Path(__file__).read_bytes()), 'summary': SUMMARY})
    print(f'V788 integration and actual prompt recorded;{len(archived)} artifacts archived and guide candidate saved.417 complete,79 pending;goal active.', flush=True)


if __name__ == '__main__':
    main()
