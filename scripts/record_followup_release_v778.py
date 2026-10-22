"""Record25 completed entries with explicit fixture and actual voice-sample scope."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_followup_common_v778 import ROOT, MANUSCRIPT
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v778_candidate.nds')
LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/scheme_followup_v778_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V778 Followup integrated')
SHOTS = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V778 Followup dialogue')


def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert sha(source.read_bytes()) == sha(target.read_bytes())


def main():
    game = read(ROOT/'gameplay_verification.json')
    manifest = read(ROM.with_suffix('.manifest.json'))
    patch = read(ROOT/'patch_proof.json')
    registered = read(ROOT/'registered_verification.json')
    watch = read('work/analysis/dialogue_formatting_user_recheck_v778/COMMON676_677.json')
    doc = read(MANUSCRIPT)
    digest = sha(ROM.read_bytes())
    assert digest == game['candidate_sha256'] == manifest['candidate_sha256'] == patch['candidate_sha256'] == registered['candidate_sha256'] == watch['sha256']
    assert all(manifest['checks'].values()) and patch['byte_exact_reconstruction']
    assert len(doc['records']) == 25 and sum(r['decision'] == 'revise' for r in doc['records']) == 10
    assert all(all(r['review'].values()) for r in doc['records'])
    assert game['actual_IDs'] == [965, 972, 973, 979, 984]
    assert sum(len(r['holds']) for r in game['scenarios']) == 10
    assert sum(len(r['whole_screen_controls']) for r in game['scenarios']) == 60
    assert sum(len(r['paired_state_model_object_task_frames']) for r in game['scenarios']) == 61
    protected = read('work/analysis/scheme_followup_editorial_v777/checkpoint.json')['protected_files_unchanged']
    for path, pin in protected.items():
        assert sha(Path(path).read_bytes()) == pin, path
    latest = {'path': str(ROM), 'sha256': digest, 'profile': manifest['profile'],
              'MESFILE_sha256': registered['COMMON_sha256'], 'ARM9_sha256': registered['ARM9_sha256'],
              'patch_sha256': patch['patch_sha256'], 'manifest': str(ROM.with_suffix('.manifest.json')),
              'status': 'experimental', 'details': str(DOC),
              'supplemental_verification': str(ROOT/'gameplay_verification.json'),
              'initial_source_pins_retained_as_V743_reference_not_overwritten': True,
              'remaining_in_this_registered_batch': 'All25 follow-up entries reviewed;wider shared/all-route/player-facing prose and separate graphics audit remain unfinished.',
              'full_goal_complete': False}
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] in (311, 336)
    assert ledger['records_with_source_and_prose_pass'] == 339
    if ledger['records_editorially_completed'] == 311:
        save(ROOT/'editorial_ledger_before_v778.json', ledger)
    else:
        assert (ROOT/'editorial_ledger_before_v778.json').exists()
    records = []
    for row in doc['records']:
        n = row['message_id']
        records.append({'message_id': n, 'decision': 'revised-and-integrated' if row['decision'] == 'revise' else 'retain-wording',
                        'manuscript': str(MANUSCRIPT), 'source_native_context_and_complete_font_verified': True,
                        'ordinary_actual_display_verified': False,
                        'actual_display_with_disclosed_fixture': n in game['actual_IDs'],
                        'actual_display_scope': 'Five IDs represent all five original consumer/table types in ten actual holds;other20 voices have source/native/full-font coverage,not individual gameplay activation. Earned qualifications,crowding,shortage and future scheme outcome are not claimed.',
                        'source_native_arguments': row['source_native_arguments'],
                        'English_argument_source_indices': row['English_argument_source_indices'],
                        'speaker_context_amendment': 'Patron,confirmed by actual unmodified portrait/name label' if n == 972 else None,
                        'gameplay_evidence': str(ROOT/'gameplay_verification.json')})
    family = 'Tavern-scheme-followup-bribe-crowded-and-Patron-rumor964-988'
    if not any(r['id'] == family for r in ledger['completed_editorial_families']):
        ledger['completed_editorial_families'].append({'id': family, 'native_message_IDs': list(range(964, 989)), 'records': records})
    if family not in ledger['coverage_units'][0]['completed_families']:
        ledger['coverage_units'][0]['completed_families'].append(family)
    ledger.update({'records_editorially_completed': 336, 'records_revised_and_integrated': 245,
                   'retained_wordings_editorially_completed': 91, 'current_integrated_candidate': latest})
    ledger['active_source_prose_drafts'] = {'native_message_IDs': [750, 751, 752],
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],
        'status': '750-752-context-unmapped', 'note': 'Caller mapping remains required before formatting/integration approval.'}
    ledger['coverage_units'][0]['next'] = 'Review989 onward and resolve750-752 original contexts;continue wider shared/all routes/remaining player-facing prose. Keep separate graphics audit and older-record follow-up open.'
    ledger['latest_checkpoint'] = 'V778 completes25 followup/bribe/crowd/Patron-rumor entries(10 revised/15 retained).336 complete(245 revised/91 retained),339 source/prose,three drafts750-752.34343 native routing cases,13699 production layouts,7336 complete copies,ten actual holds/five consumer types,60 full-screen controls,61 paired state/model/task frames,normal returns and seven ordinary New Game frames pass. Only COMMON/ARM9 change;470/114 inheritance and exact clean patch preserved. Wider prose and graphics goals remain unfinished.'
    checkpoint = {'id': 'V778-followup-integrated-and-gameplay-verified', 'documentation': str(DOC),
                  'new_editorially_completed': 25, 'revised': 10, 'retained': 15,
                  'manuscript': str(MANUSCRIPT), 'evidence': str(ROOT/'gameplay_verification.json'),
                  'new_ROM': True, 'experimental': True, 'full_goal_complete': False}
    if not any(r['id'] == checkpoint['id'] for r in ledger['research_checkpoints']):
        ledger['research_checkpoints'].append(checkpoint)
    save(LEDGER, ledger)
    save('out/editorial_review_latest.json', latest)
    DOC.write_text(f'''# V778: follow-up,bribe,crowded refusal and Patron rumor verified

25 entries964–988 complete editorial review:10 revised and15 retained. Overall336
entries are complete(245 revised/91 retained),339 source/prose-reviewed. Three
drafts750–752 still need caller mapping.989 onward,other shared text,all routes and
remaining player-facing prose stay open. The separate graphics audit,including18
original plaques,and older-record follow-up remain unfinished. The goal is active.

## Meaning and original consumers

The V777 source/native review establishes four voice tables,160 officer selections,
four null fallbacks,five caller fragments and16 condition branches. Arrangement
replies precede the original charge;they do not announce the future scheme result.
Bribe confirmations preserve TOWN then FACTION and the selected faction's broker.
Crowded refusals preserve seat/privacy distinctions,Admiral where spoken,and
tomorrow only for988.972 preserves the regular monthly run,storm/sinking and hearsay.
Ten revisions improve natural English;the15 already natural wordings are retained.
All use natural-dialogue-v2/en-US;approved names remain unchanged.

Actual972 is spoken by the **Patron**,as shown by the unchanged portrait/name label.
This corrects the earlier barmaid/NPC research label. The native town-NPC getter,
direct972 caller and prose meaning are unchanged. The released manuscript and
preintegration proofs remain frozen for exact reproduction;this checkpoint and
coverage ledger provide the authoritative speaker amendment and gameplay status.

## Production routing and preservation

The private routing table grows100→110 bytes inside its previously owned128-byte
span. The140-byte gate and every other runtime instruction remain exact.34343
native scope/register/SP/LR cases pass,including every numeric ID and all nearby
aligned/unaligned voice-table keys. No section,autoload,BSS,cache,arena or123040-byte
staged payload grows. Six original target-calling paths and20 immutable name
initializers prove Bribe cannot receive the edited player-company name. One false
Thumb scan candidate is source-bound to its executed original ARM thunk;there is
no general reference or layout waiver.

13699 actual production-parent/table layouts exactly match reviewed native printf/
literal outputs,with complete words,guards,ABI and no findings.53 independent full
font planes/five preview sheets were already visually reviewed.7336 complete native
warm/cold copies cover all3668 COMMON entries,including post-NUL structured payloads.
Existing28 blocks2–29 hold all complete paragraphs.3643 other strings,13 other
blocks,the two opaque tails and user676/677 remain exact. Only COMMON and ARM9 differ
from V776;all other files,overlays,ARM7,470 batches,114 accepted layers and graphics
are preserved. Eight explicit parser-dependency replays reproduce prior outputs.
Eleven malformed source/current/policy/layout/argument controls are rejected.

## Three paired automated emulator scenarios

All runs are actual ROM cold boots using protected copies of the London donor,
with no savestate. Original saves remain unchanged. Fixture receipts are reproduced
independently from each pre-insertion RAM snapshot on both ROMs.

- **Bribe,13200 frames:** the mapped three room/assignment bytes,one XP word and
  one calendar word(+11 days) expose the original Schemes menu. Actual973 town
  question,979 London/Clifford confirmation and965 arrangement reply each have two
  complete holds. Original scheduling succeeds and charges40659→39659 gold.
  The original game then advances its day and returns to town normally. No future
  outcome,earned qualification,wealth or campaign progression is claimed.
- **Crowded refusal,7600 frames:** the same qualification fixture plus original
  task setters fill ten declared meeting slots with valid Bribe jobs due365 days
  later.78 declared byte changes are bounded to assignment/XP/date/task fields;
  all other4MiB bytes are exact at insertion. The original free-slot getter returns
  zero and original572F4 emits984 without charging gold. Two complete refusal holds
  and normal return pass. This is an artificial capacity fixture,not an earned
  crowded Tavern or ten successful real missions.
- **Shortage/Patron rumor,30400 frames:** only Amsterdam's status/duration bytes
  become5/30;all other4MiB bytes remain exact at insertion. Original paid-round
  selection supplies condition information and then972,with two complete holds.
  Original NPC portrait/name label is Patron. Funds40659→39402 and normal town
  return match V776. No naturally earned shortage or historical shipwreck is proved.

Across these scenarios,ten actual holds cover all five new consumer types. Complete
independently decoded native glyphs,blank-paper cells,left margins,leading/trailing
letters,arguments and bounds pass. Every outside-text pixel matches the baseline,
including portraits and yes/no controls. Advance crops match original ordinary
holds.60 other entire screen controls and61 paired native state/model/object/all24
task-record snapshots match. No menu-animation exclusion is needed.798 extra
baseline bribe-return captures receive no paired credit. Seven ordinary New Game
screens,without donor or fixture,match V776 exactly. Other20 voices have complete
source/native/font coverage through these consumer-family samples,not individual
gameplay activations. No full-route or physical-hardware claim is made.

## User formatting watch and experimental release

676/677 repaired text and original native wrapping were rechecked again in V778.
The earlier V747 actual cooking screenshot was visually reviewed;no new V778 shop
activation is claimed. The ongoing audit continues to check margins,manual gaps,
whole words,complete letters,bounds,pagination and dismissal for every family.

- Candidate:`{ROM}`;SHA-256:`{digest}`.
- Profile:`{manifest['profile']}`;experimental,not canonically promoted.
- Manifest:`{ROM.with_suffix('.manifest.json')}`.
- Exact patch:`{ROM.with_suffix('.xdelta')}`;SHA-256:`{patch['patch_sha256']}`.
- Clean-input SHA-256:`{patch['clean_source_sha256']}`;whole candidate reconstructs
  byte for byte. Canonical base SHA-256:`{patch['canonical_base_sha256']}`,unchanged.
- Evidence:`{ROOT/'gameplay_verification.json'}`,registered/native/copy/layout/source
  proofs and the adjacent frozen build log. All artifacts are on E: through the
  configured output/analysis junctions. Archive and fixture screenshots are under
  E:/Rota Nova translations. Screenshots are not represented as earned guide scenes.

No GitHub commit/push or canonical acceptance was made by this checkpoint.
''', encoding='utf-8')
    heading = '## V778: follow-up dialogue integrated and verified'
    section = f'\n\n{heading}\n\n25 entries complete(10 revised/15 retained):336 total(245 revised/91 retained),339 source/prose,three750-752 drafts.34343 exact routing cases,13699 production layouts,7336 complete copies,ten actual holds/five consumer types,60 whole-screen controls,61 state/model/task pairs and seven ordinary New Game frames pass. Original bribe scheduling/1000-gold charge,crowded refusal,Patron storm rumor and normal returns are verified with disclosed isolated fixtures. Registered combined ROM/exact clean patch preserves470/114 inheritance and prior graphics.989 onward,wider shared/routes/prose and separate graphics audit remain open. Experimental;canonical and original donors unchanged. See [V778 checkpoint](scheme_followup_v778_checkpoint.md).\n'
    for name in ('translation_progress.md', 'todo.md', 'known_issues.md'):
        path = Path('docs')/name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip()+section, encoding='utf-8')
    amendment = {'message_id': 972, 'speaker': 'Patron', 'gameplay_evidence': str(ROOT/'gameplay_verification.json'),
                 'earlier_barmaid_NPC_label_superseded': True, 'English_prose_and_original_caller_unchanged': True}
    save(ROOT/'speaker_context_amendment.json', amendment)
    provenance = []
    for scenario in game['scenarios']:
        for n in sorted({h['message_id'] for h in scenario['holds']}):
            row = next(h['capture'] for h in scenario['holds'] if h['message_id'] == n)
            target = SHOTS/f'COMMON_{n}_V778_{scenario["kind"]}_fixture.png'
            copy(Path(row['path']), target)
            provenance.append({'path': str(target), 'source': row, 'ROM_sha256': digest,
                               'fixture_kind': scenario['kind'], 'unedited_native_capture': True,
                               'earned_scene_or_guide_publication_claim': False})
    save(SHOTS/'provenance.json', provenance)
    save(ROOT/'checkpoint.json', {'candidate': latest, 'new_completed_IDs': list(range(964, 989)),
                                  'protected_files_unchanged': protected, 'goal_status': 'active',
                                  'full_goal_complete': False, 'producer_sha256': sha(Path(__file__).read_bytes())})
    for path in ROOT.rglob('*'):
        if path.is_file() and path.suffix.lower() != '.nds':
            copy(path, ARCHIVE/'evidence'/path.relative_to(ROOT))
    paths = [ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'), DOC, LEDGER, MANUSCRIPT,
             Path('translations/scheme_followup_editorial_release_v1.json'), Path('translations/release_stack.json'),
             Path('out/editorial_review_latest.json'), Path('dk4tool/patch/scheme_followup_runtime.py'),
             Path('dk4tool/patch/scheme_followup_editorial.py'), Path('dk4tool/script/common_message_table.py'),
             Path('scripts/build_integrated_release.py')]
    paths += sorted(Path('scripts').glob('*v778.py')) + sorted(Path('translations').glob('*replay_for_v778.json'))
    for path in paths:
        copy(path, ARCHIVE/path)
    for scenario in game['scenarios']:
        for report in scenario['capture_reports']:
            path = Path(report)
            copy(path, ARCHIVE/'capture_reports'/path.parent.name/path.name)
    for path in SHOTS.iterdir():
        if path.is_file():
            copy(path, ARCHIVE/'fixture_screenshots'/path.name)
    for name in ('COMMON676_677.json',):
        path = Path('work/analysis/dialogue_formatting_user_recheck_v778')/name
        copy(path, ARCHIVE/'user_formatting_watch'/path.name)
    files = {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
             if p.is_file() and p.name != 'archive_manifest.json'}
    save(ARCHIVE/'archive_manifest.json', {'candidate': latest, 'files': files, 'full_goal_complete': False})
    assert all(sha((ARCHIVE/p).read_bytes()) == h for p, h in files.items())
    print('V778 recorded and archived:336 complete,three drafts;broader editorial and graphics goals remain open.', flush=True)


if __name__ == '__main__':
    main()
