"""Record completed information/coordinate samples without premature batch credit."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.register_shared_release_v782 import CONFIG, MANUSCRIPT, ROOT
from scripts.verify_village_wrap_v608 import read, save

LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/shared_dialogue_v782_information_village.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V782 Shared dialogue integration/Information and village tests')
SHOTS = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V782 Shared dialogue')


def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert sha(source.read_bytes()) == sha(target.read_bytes())


def main():
    config = read(CONFIG)
    for path, digest in config['dependencies'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    assert sha(MANUSCRIPT.read_bytes()) == config['manuscript_sha256']
    rom = Path('out/all_routes_combined_v782_candidate.nds')
    digest = sha(rom.read_bytes())
    patch = read(ROOT/'patch_proof.json')
    assert digest == patch['candidate_sha256'] == '9f55817772d2b1e940462f69103536654f0cbedbe959fb42670fc601f2d6e31d'
    assert sha(rom.with_suffix('.xdelta').read_bytes()) == patch['patch_sha256']
    protected = read(ROOT/'checkpoint.json')['protected_files_unchanged']
    for path, expected in protected.items():
        assert sha(Path(path).read_bytes()) == expected, path
    names = ['information_gameplay_verification.json', 'village_casual_gameplay_verification.json', 'village_formal_gameplay_verification.json']
    prior = ['recruit_capacity_gameplay_verification.json', 'recruit_shortfall_gameplay_verification.json', 'warning_gameplay_verification.json']
    new = [read(ROOT/p) for p in names]
    reports = [read(ROOT/p) for p in prior]+new
    assert all(p['candidate_sha256'] == digest and not p['batch_completion_credit'] for p in reports)
    assert [{h['message_id'] for h in p['holds']} for p in new] == [{1020}, {1029}, {1028}]
    assert all(len(p['holds']) == 2 for p in new)
    assert all(h['complete_independent_font_and_blank_paper_exact'] and h['all_other_pixels_exact'] for p in new for h in p['holds'])
    assert new[0]['both_fixture_receipts_reproduced_from_prefixture_RAM_in_both_ROMs']
    assert all(p['fixture_receipt_reproduced_from_prefixture_RAM_in_both_ROMs'] for p in new[1:])
    v3 = read(ROOT/'speaker_metadata_v3_equivalence.json')
    assert v3['all50_complete_encoded_paragraphs_identical'] and v3['registered_metadata_replay_pending']
    assert sha(Path('translations/shared_dialogue_editorial_manuscript_v3.json').read_bytes()) == v3['V3_sha256']
    controls = sum(len(p['whole_screen_controls']) for p in reports)
    states = sum(len(p['paired_state_model_object_task_frames']) for p in reports)
    phases = sum(len(p['original_whole_screen_blink_phase_controls']) for p in reports)
    assert (controls, states, phases) == (289, 285, 2)
    remaining = ['Anchorage/destination fleet1030-1034', 'Private barmaid1049-1069', 'Metadata-only registered replay for corrected role1 First Mate speaker context']
    summary = ('V782 now has12 complete actual holds across six IDs1020/1022/1028/1029/1035/1042;'
               '289 strict whole-screen controls,two original whole-screen phase controls and285 state/model/object/task pairs pass. '
               'Both original village styles preserve the raw coordinate buffer and display N69 E18 cleanly;'
               '14 ordinary Treat Everyone purchases lead through the native gossip chain,with exact costs and town return. '
               'Missing-information uses the native empty-contract-information branch and makes no payment or new job. '
               'A metadata-only V3 corrects1035-1048 to the role1 First Mate speech provider with native officer fallback;'
               'all50 encoded paragraphs remain identical. Fleet/private actual samples and explicit metadata registration remain required. '
               '367 completed,420 source/prose and53 drafts remain unchanged;full editorial goal and separate graphics audit stay open.')
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 367 and ledger['records_with_source_and_prose_pass'] == 420
    assert ledger['records_revised_and_integrated'] == 259 and ledger['retained_wordings_editorially_completed'] == 108
    backup = ROOT/'editorial_ledger_before_information_village.json'
    if not backup.exists():
        save(backup, ledger)
    pending = ledger['pending_integrated_candidate']
    assert pending['sha256'] == digest
    pending.update({'details': str(DOC),
                    'verified_actual_families': ['information1020', 'warning1022', 'village1028-1029', 'required-shortfall1035', 'capacity1042'],
                    'remaining_actual_families': remaining[:2], 'remaining_gates': remaining,
                    'supplemental_verification': str(ROOT/'information_village_checkpoint.json'),
                    'speaker_context_correction': str(ROOT/'role1_speaker_context_correction.json')})
    ledger['active_source_prose_drafts']['status'] = '750-752-context-unmapped;1020-1069-native-reviewed-integrated;five-actual-families-verified;fleet-private-and-metadata-replay-pending'
    ledger['active_source_prose_drafts']['note'] = 'All50 remain drafts until fleet/private actual samples and metadata-only registered replay pass. Frozen V2 mislabeled1035-1048 as Barkeep; V3 corrects the native role1 First Mate provider,including fallback. English bytes unchanged.'
    ledger['coverage_units'][0]['next'] = 'Complete fleet1030-1034 and private-barmaid1049-1069 actual samples;register corrected V3 speaker metadata with exact ROM-byte replay;then close50-entry batch. Continue COMMON1070 onward,resolve750-752,review all routes and remaining prose,and preserve graphics/older-record follow-up.'
    ledger['latest_checkpoint'] = summary
    checkpoint = {'id': 'V782-information-and-village-actual-gameplay', 'documentation': str(DOC),
                  'candidate_sha256': digest, 'new_actual_IDs': [1020, 1028, 1029],
                  'combined_actual_IDs': [1020, 1022, 1028, 1029, 1035, 1042],
                  'new_actual_complete_holds': 6, 'combined_actual_complete_holds': 12,
                  'strict_whole_screen_controls': controls, 'original_whole_screen_phase_controls': phases,
                  'paired_state_model_object_task_frames': states, 'new_editorially_completed': 0,
                  'remaining_gates': remaining, 'full_goal_complete': False}
    if not any(p['id'] == checkpoint['id'] for p in ledger['research_checkpoints']):
        ledger['research_checkpoints'].append(checkpoint)
    save(LEDGER, ledger)
    latest = read('out/editorial_review_latest.json')
    latest.update({'latest_research_checkpoint': str(DOC), 'pending_integrated_candidate': pending})
    save('out/editorial_review_latest.json', latest)
    DOC.write_text('''# V782: missing information and both village rumor styles

Six additional actual holds verify COMMON1020 and both coordinate variants1028/1029.
Combined with the earlier warning and crew samples, twelve holds cover six IDs in
five consumer families. There are289 strict full-screen controls, two complete
original blink-phase controls and285 paired state/model/object/task snapshots.
All six new holds match independent complete native font planes and blank paper;
all other pixels match. Ordinary town returns pass. The ROM and exact clean-input
patch are unchanged. V780 remains the last wholly verified editorial batch.

## Missing contract information

Paired8200-frame cold boots use protected copies of the Istanbul save. The frozen
qualification fixture enables the source Schemes prerequisites. At6600, the original
B50B8 town-information setter clears only the known-information bit for the two
eligible Castor towns. Two bytes change; contracts, shares, cash and code do not.
The original57068 query returns no Castor towns while Pasha retains19/22. Normal
Schemes > Lure Fleet > Castor selection reaches1020. Both7000/7400 holds read:
"We have no information on the towns where that faction has contracts."
Sixteen strict screens and15 state/model/object/task pairs pass. No1000 coins are
charged and no job is scheduled. Normal dismissal returns to town at8200.

## Village coordinates

Four42000-frame cold boots compare both original styles in V780/V782. A disclosed
fixture changes three market bytes to own31/Pasha68 while preserving total99. The
formal variant additionally changes the native regional-standing halfword to3000
using the original3CC38 setter; five bytes total change. Cash, health, cargo,
location, village knowledge, code and all other4MiB bytes are exact at insertion.
These are isolated prerequisites, not earned reputation or village discovery.

The original Treat Everyone information chain is exercised normally. A treasure
hint and fleet reports precede the village fallback; fourteen purchases at314 coins
each reduce cash8371 to3975. No gossip report is suppressed or RNG result forced.
The source flags naturally mark earlier fleet reports as told. Both final styles
reach their village line at40800/41200 and return to town at42000. No job is added.

Casual1029: "Have you heard? There's a village near N69 E18 where you can get
supplies." Formal1028: "Did you know? There's a village near N69 E18 where you can
get supplies." Each uses three clean, aligned rows, with full leading/trailing
letters and complete coordinates. There are212 strict whole-screen controls and
210 paired state/model/object/task snapshots, without an animation exception.

The first verifier expected the source's padded argument in the live expanded
scratch buffer. Inspection showed the scoped formatter already compacts that copy
to N69 E18. The original raw buffer at022A4E78 remains exactly LF-space-N-two-spaces-
69-space-E-two-spaces-18 in both actual V782 captures. Verification now checks the
untouched original argument, the baseline expansion, normalized revised expansion,
original formatter replay from the raw argument, and every displayed glyph. This
corrects the test expectation; no production code or text was changed.

## Speaker-context erratum

Frozen shared manuscriptV2 incorrectly labeled1035-1048 as Barkeep. Original role1
is Japanese副官, localized First Mate. Original825E4 finds no assigned officer in
this save;82478 chooses Charles Rochefort as its native speech fallback. Actual
recruitment captures agree. New manuscriptV3 corrects only speaker/context notes
for these14 records. Every one of the50 encoded paragraphs remains identical.
The existing V782 production dependencies remain frozen. A registered metadata-only
replay is still required before this batch can close; the old label is superseded
as context evidence, not silently rewritten in historical build inputs.

## Remaining work and evidence

Fleet rumors1030-1034 and private barmaid topics1049-1069 still need actual samples.
The50-entry batch receives no completion credit yet. Totals remain367 completed,
420 source/prose reviewed and53 drafts. Wider shared text, all routes, remaining
prose, the separate graphics audit and older-record follow-up remain open.

Full captures, receipts and scripts are on E:/Rota Nova translations, with verified
images under Screenshots/Test fixtures/V782 Shared dialogue. They are targeted
automated emulator tests, without savestates, hardware or full-playthrough claims.
Production dependencies, ROM, patch, clean/canonical inputs and original saves
retain their exact hashes. No new ROM or GitHub push is made in this checkpoint.
''', encoding='utf-8')
    for file in ('docs/todo.md', 'docs/known_issues.md', 'docs/translation_progress.md'):
        path = Path(file)
        text = path.read_text(encoding='utf-8')
        heading = '## V782: missing-information and village-coordinate gameplay'
        if heading not in text:
            path.write_text(text+'\n\n'+heading+'\n\n'+summary+' See [information and village checks](shared_dialogue_v782_information_village.md).\n', encoding='utf-8')
    checkpoint.update({'reports': [{'path': str(ROOT/p), 'sha256': sha((ROOT/p).read_bytes())} for p in names],
                       'ROM_patch_and_frozen_production_dependencies_unchanged': True,
                       'protected_files_unchanged': protected,
                       'previous_goal_turn_classification': 'Progress: exact preserved formatting rechecked for user screenshot; this turn completes three additional actual scene IDs.',
                       'producer_sha256': sha(Path(__file__).read_bytes())})
    save(ROOT/'information_village_checkpoint.json', checkpoint)
    files = [ROOT/p for p in names+['information_village_checkpoint.json', 'village_coordinate_gameplay_verification.json',
             'effective_information_gameplay_verifier.py', 'effective_village_casual_gameplay_verifier.py',
             'effective_village_formal_gameplay_verifier.py', 'role1_speaker_context_correction.json',
             'speaker_metadata_v3_equivalence.json', 'village_fixture_preflight.json', 'missing_information_fixture_preflight.json']]
    files += [Path('scripts')/p for p in ('native_information_fixture_v782.py', 'run_information_capture_v782.py',
              'verify_shared_information_gameplay_v782.py', 'native_village_dialogue_fixture_v782.py',
              'run_village_dialogue_capture_v782.py', 'verify_shared_village_gameplay_v782.py',
              'review_shared_speaker_context_v782.py', 'record_shared_information_village_v782.py')]
    files += [DOC, LEDGER, Path('translations/shared_dialogue_editorial_manuscript_v3.json')]
    for source in files:
        copy(source, ARCHIVE/source.name)
    for report in new:
        for name in report['capture_reports']:
            path = Path(name)
            copy(path, ARCHIVE/path.parent.name/path.name)
        for hold in report['holds']:
            copy(Path(hold['capture']['path']), SHOTS/f'ID{hold["message_id"]}_{hold["frame"]}_V782_VERIFIED_TEST.png')
    save(ROOT/'information_village_archive_receipt.json', {'archive': str(ARCHIVE), 'screenshots': str(SHOTS),
                                                         'every_copy_SHA256_verified': True, 'no_new_completion_credit': True})
    print('Information and both coordinate styles archived;12 combined holds,289 strict screens,285 state pairs. Fleet/private samples and metadata replay remain.', flush=True)


if __name__ == '__main__':
    main()
