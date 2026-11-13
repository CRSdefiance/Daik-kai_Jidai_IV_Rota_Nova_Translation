"""Record the completed 31-entry batch, preserving the full unfinished goal."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/barmaid_integration_v780')
ROM = Path('out/all_routes_combined_v780_candidate.nds')
MANUSCRIPT = Path('translations/barmaid_editorial_manuscript_v2.json')
CONFIG = Path('translations/barmaid_editorial_release_v1.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/barmaid_v780_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V780 Barmaid integrated')
SHOTS = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V780 Barmaid dialogue')


def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert sha(source.read_bytes()) == sha(target.read_bytes())


def main():
    manuscript, config = read(MANUSCRIPT), read(CONFIG)
    for name, pin in config['dependencies'].items():
        assert sha(Path(name).read_bytes()) == pin, name
    assert sha(MANUSCRIPT.read_bytes()) == config['manuscript_sha256']
    game, patch = read(ROOT/'gameplay_verification.json'), read(ROOT/'patch_proof.json')
    release, manifest = read(ROOT/'registered_verification.json'), read(ROM.with_suffix('.manifest.json'))
    watch = read('work/analysis/dialogue_formatting_user_recheck_v780/COMMON676_677.json')
    digest = sha(ROM.read_bytes())
    assert digest == game['candidate_sha256'] == patch['candidate_sha256'] == release['candidate_sha256'] == manifest['candidate_sha256'] == watch['sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes()) == patch['patch_sha256']
    assert patch['byte_exact_reconstruction'] and all(manifest['checks'].values())
    assert release['all470_batches114_accepted_layers_and_graphics_retained'] and release['all7336_complete_native_copies']
    assert all(release['negative_gates'].values()) and release['only_COMMON_ARM9_change_from_V778']
    assert len(manuscript['records']) == 31 and sum(r['decision'] == 'revise' for r in manuscript['records']) == 14
    assert all(all(r['review'].values()) for r in manuscript['records'])
    assert game['actual_IDs'] == [989, 990, 991, 999, 1000, 1014] and game['actual_complete_holds'] == 12
    assert game['whole_screen_controls'] == 355 and game['paired_state_model_object_task_frames'] == 358
    assert game['newgame_whole_frame_pairs'] == 7
    protected = dict(read('work/analysis/barmaid_editorial_v779/checkpoint.json')['protected_files_unchanged'])
    protected.update({
        'E:/Rota Nova translations/Saves/maria-nagasaki-namahage-v514.dsv': 'fbae21aa2c5a695bde0eddfc10a3bbeb80d01478bd6a9ed743d824595dc3096e',
        'E:/Rota Nova translations/Saves/maria-seoul-rested-v514.dsv': '942c74828a7b7396f7567ca2d405ddc4cdd329e4837f591777d35ee458794b0f'})
    for name, pin in protected.items():
        assert sha(Path(name).read_bytes()) == pin, name
    latest = {'path': str(ROM), 'sha256': digest, 'profile': manifest['profile'],
              'MESFILE_sha256': release['COMMON_sha256'], 'ARM9_sha256': release['ARM9_sha256'],
              'patch_sha256': patch['patch_sha256'], 'manifest': str(ROM.with_suffix('.manifest.json')),
              'status': 'experimental', 'details': str(DOC),
              'supplemental_verification': str(ROOT/'gameplay_verification.json'),
              'initial_source_pins_retained_as_V743_reference_not_overwritten': True,
              'remaining_in_this_registered_batch': 'All 31 barmaid entries reviewed. Wider shared text, all routes, other player-facing prose and the separate graphics audit remain unfinished.',
              'full_goal_complete': False}
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] in (336, 367) and ledger['records_with_source_and_prose_pass'] == 370
    if ledger['records_editorially_completed'] == 336:
        save(ROOT/'editorial_ledger_before_v780_release.json', ledger)
    else:
        assert (ROOT/'editorial_ledger_before_v780_release.json').exists()
    family = 'Tavern-barmaid-introductions-ordinary-gifts-and-casual989-1019'
    records = []
    for row in manuscript['records']:
        n = row['message_id']
        records.append({'message_id': n, 'decision': 'revised-and-integrated' if row['decision'] == 'revise' else 'retain-wording',
                        'manuscript': str(MANUSCRIPT), 'source_native_context_and_complete_font_verified': True,
                        'ordinary_actual_display_verified': False,
                        'actual_display_with_disclosed_fixture': n in game['actual_IDs'],
                        'actual_display_scope': 'Six IDs represent all six original consumer types in twelve complete holds. Other 25 entries have source/native/font coverage and family sampling, not individual gameplay activation. 996 is retained latent source speech with original guards unchanged; normal activation is not claimed.',
                        'source_native_arguments': row['source_native_arguments'],
                        'English_argument_source_indices': row['English_argument_source_indices'],
                        'gameplay_evidence': str(ROOT/'gameplay_verification.json')})
    if not any(r['id'] == family for r in ledger['completed_editorial_families']):
        ledger['completed_editorial_families'].append({'id': family, 'native_message_IDs': list(range(989, 1020)), 'records': records})
    if family not in ledger['coverage_units'][0]['completed_families']:
        ledger['coverage_units'][0]['completed_families'].append(family)
    ledger.update({'records_editorially_completed': 367, 'records_revised_and_integrated': 259,
                   'retained_wordings_editorially_completed': 108, 'current_integrated_candidate': latest})
    ledger['active_source_prose_drafts'] = {'native_message_IDs': [750, 751, 752],
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],
        'status': '750-752-context-unmapped', 'note': 'Original caller mapping remains required before native formatting and integration approval.'}
    ledger['coverage_units'][0]['next'] = 'Review COMMON 1020 onward and resolve original contexts for 750-752. Continue wider shared text, all route scenes and other player-facing prose. Preserve the separate graphics audit and the older-record follow-up.'
    ledger['latest_checkpoint'] = 'V780 completes 31 barmaid entries: 14 revised and 17 retained. Overall 367 completed (259 revised/108 retained), 370 source/prose passes and three pending drafts. Production routing, 273 substituted layouts, 7336 complete copies, exact clean patch, twelve actual holds across six consumer types, 355 whole-screen controls, 358 paired state/model/task snapshots, original gift/relationship outcomes, normal returns and seven ordinary New Game frames pass. Other shared/route/player-facing prose and the separate graphics audit remain unfinished.'
    historical = ledger.pop('barmaid_integration_v780_in_progress', None)
    if historical:
        ledger['barmaid_integration_v780_historical_partial_checkpoint'] = dict(historical, superseded_by=str(DOC), historical_record=True)
    checkpoint = {'id': 'V780-barmaid-integrated-and-gameplay-verified', 'documentation': str(DOC),
                  'new_editorially_completed': 31, 'revised': 14, 'retained': 17,
                  'manuscript': str(MANUSCRIPT), 'evidence': str(ROOT/'gameplay_verification.json'),
                  'new_ROM': True, 'experimental': True, 'full_goal_complete': False}
    if not any(r['id'] == checkpoint['id'] for r in ledger['research_checkpoints']):
        ledger['research_checkpoints'].append(checkpoint)
    save(LEDGER, ledger)
    save('out/editorial_review_latest.json', latest)
    DOC.write_text(f'''# V780: barmaid editorial batch completed

31 entries, COMMON 989–1019, complete this editorial batch: 14 revised and 17
retained. Overall, 367 entries are completed: 259 revised and 108 retained.
370 have source/prose review; drafts 750–752 still require original caller mapping.
COMMON 1020 onward, the remaining shared text, every route and other player-facing
prose remain in scope. The full goal is active. The separate graphics audit,
including the 18 original plaques, is still unfinished.

## Natural English and source fidelity

The clean Japanese and original consumers establish introductions, ordinary chat,
gift thanks and city-specific casual speech. Revisions improve conversational
wording while preserving character opinions, family obligations, songs, cultural
references, teasing and hopes for a partner. They do not invent marriage, a death,
an explicit sexual act or a family relationship. Existing natural wording is
retained. All new prose follows natural-dialogue-v2 and American English.

989 supplies barmaid then captain; 990 supplies captain then barmaid. 999 supplies
only the captain's first name. Actual editable first names have a 16-byte limit,
not the different company-name bound. Approved names and existing actor names stay
unchanged. 114 original city lookups, 21 barmaids and 84 provider/caller cases map
the source choices. 996 is a latent original city-58 branch whose initialized lookup
is null. Full caller and guard closure supports retaining it without changing the
catalog or claiming a normal activation. Three apparent address windows are proved
to be original ARM instructions or the complete numeric table; there is no blanket
unaligned-reference exemption. Historical failed research remains preserved.

## Integration and formatting

The private table grows from 110 to 114 bytes inside its existing 128-byte span.
The 140-byte gate stays exact. 34,343 native routing and ABI cases pass. All 273
production layouts match the reviewed source layouts, including legal maximum
ASCII and CP932 first names. Five naive article warnings are exactly bound to
player-name bytes, with a literal-prose negative control. No unresolved layout
finding remains. 52 independent full font planes were visually reviewed in research.

No section, BSS, cache, arena or 123,040-byte staged payload grows. The smallest
fitting contiguous repack uses blocks 12–35. All 3,637 other visible strings, 17
other blocks and both opaque post-NUL payloads remain exact. 7,336 complete native
warm/cold copies pass. The registered builder preserves 470 batches, 114 accepted
layers and earlier graphics. Only COMMON and ARM9 differ from V778. Eleven malformed
release controls are rejected. The clean-input patch reconstructs the full ROM
byte for byte. Source/configuration artifacts remain frozen for reproduction;
their earlier pending-gameplay flags are superseded by this final checkpoint and
the supplemental gameplay proof.

The user's 676/677 repair remains exact in V780's ROM bytes and native wrapping.
The earlier V747 actual cooking screenshot was visually reviewed; no fresh V780
shop activation is claimed. Margins, internal gaps, complete words and letters,
bounds, pagination and dismissal remain checks for every later family.

## Three paired emulator scenarios

Every run cold-boots the actual ROM from a protected donor copy, without a
savestate. The same inputs, core options and disclosed fixtures are replayed on
V778 and V780. All original donors remain unchanged.

- **Donna, Seville:** two complete 989 holds show Donna then Hodram and three aligned
  lines. Three declared coordinate fixtures change only the ship's eight coordinate
  bytes. Original discovery, arrival story, docking, tavern and town return run.
  89 whole-screen controls and 88 state/model/object/task pairs match.
- **Hatra, Sofala:** two holds each cover 990, 1000 and 1014. Maria then Hatra is the
  correct introduction order. A declared Jade Jewel transfer uses the original
  inventory routine; the game's original acceptance consumes it and advances the
  relationship from 0 through 1 to 2. Original chance-based casual speech appears
  without an RNG or relationship fixture. 204 whole-screen controls and 207
  state/model/object/task pairs match, including normal town return.
- **Reika, Seoul:** two 991 holds occur while her requested gift is unavailable.
  A declared transfer then moves Embroidered Carpet 143 from original Basra-38
  stock into inventory. The fixture owns only that item and the history vector.
  Two 999 holds contain the complete first name Maria. Original gift acceptance
  consumes the item and advances the relationship normally. 62 whole-screen
  controls and 63 state/model/object/task pairs match, with normal town return.

Across all three, twelve actual holds cover six original consumer types. Complete
independent font and blank-paper masks verify leading/trailing letters, substituted
names, left margins and bounds. Every other pixel matches the source comparison;
advance-icon crops match original ordinary holds. All 355 whole-screen controls
and 358 paired state/model/object/task snapshots pass. Seven separate ordinary New
Game framebuffer pairs match with no donor or gameplay fixture. The other 25 entries
have complete source/native/font coverage and consumer-family sampling, not
individual gameplay activations. Normal travel, earned item acquisition, a complete
playthrough and physical-hardware verification are not claimed.

## Artifacts and remaining work

- ROM: `{ROM}`
- SHA-256: `{digest}`
- Profile: `{manifest['profile']}` (experimental; no canonical promotion)
- Exact patch: `{ROM.with_suffix('.xdelta')}`
- Patch SHA-256: `{patch['patch_sha256']}`
- Clean-input SHA-256: `{patch['clean_source_sha256']}`
- Canonical base SHA-256: `{patch['canonical_base_sha256']}` (unchanged)
- Gameplay proof: `{ROOT/'gameplay_verification.json'}`

ROMs, patch, archive and screenshots are on E:/Rota Nova translations. Screenshots
are labeled test fixtures and are not promoted to the future guide. Initial
Hamburg and later Seville arrival probes that did not reach the required barmaid
families earn no completion credit. The early Seoul fixture correctly rejected
town stock under its original unowned-only rule; the later bounded exception is
specific to item 143 in original Basra-38 stock. No equipped owner is accepted.

Two additional older route leads have exact Japanese and actual screenshot
references: Maria SC3 B45 R0063 and Hodram SC1 B84 R0158. They remain queued for
full scene review, with no completion credit or new translation claimed here.
The separate graphics audit, Online-body exclusion, preserved brown marks and
older-record follow-up remain intact. No GitHub commit or push was performed.
''', encoding='utf-8')
    heading = '## V780: barmaid dialogue integrated and verified'
    section = f'\n\n{heading}\n\n31 entries completed: 14 revised and 17 retained. Overall 367 complete (259 revised/108 retained), 370 source/prose passes and three drafts 750–752. The registered combined ROM and exact clean patch preserve all prior layers and graphics without allocation growth. 273 production layouts, 7,336 copies, twelve actual holds across six consumer types, 355 whole-screen controls, 358 state/model/task pairs, original gift/relationship outcomes, normal returns and seven ordinary New Game pairs pass. COMMON 1020 onward, wider shared/route/prose work and the separate graphics audit remain open. See [V780 checkpoint](barmaid_v780_checkpoint.md).\n'
    for name in ('translation_progress.md', 'known_issues.md', 'todo.md'):
        path = Path('docs')/name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip()+section, encoding='utf-8')
    provenance = []
    for scenario in game['scenarios']:
        for n in sorted({h['message_id'] for h in scenario['holds']}):
            row = next(h['capture'] for h in scenario['holds'] if h['message_id'] == n)
            target = SHOTS/f'COMMON_{n}_V780_fixture.png'
            copy(Path(row['path']), target)
            provenance.append({'path': str(target), 'source': row, 'ROM_sha256': digest,
                               'unedited_native_capture': True, 'earned_scene_or_guide_publication_claim': False})
    save(SHOTS/'provenance.json', provenance)
    save(ROOT/'checkpoint.json', {'candidate': latest, 'new_completed_IDs': list(range(989, 1020)),
                                  'protected_files_unchanged': protected, 'goal_status': 'active',
                                  'full_goal_complete': False, 'producer_sha256': sha(Path(__file__).read_bytes())})
    for path in ROOT.rglob('*'):
        if path.is_file() and path.suffix.lower() != '.nds':
            copy(path, ARCHIVE/'evidence'/path.relative_to(ROOT))
    paths = [ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'), DOC, LEDGER, MANUSCRIPT, CONFIG,
             Path('translations/release_stack.json'), Path('out/editorial_review_latest.json'),
             Path('dk4tool/patch/barmaid_editorial.py'), Path('dk4tool/patch/barmaid_editorial_runtime.py'),
             Path('dk4tool/script/common_message_table.py'), Path('scripts/build_integrated_release.py')]
    paths += sorted(Path('scripts').glob('*v780*.py')) + sorted(Path('translations').glob('*replay_for_v780.json'))
    for path in paths:
        copy(path, ARCHIVE/path)
    for scenario in game['scenarios']:
        for name in scenario['capture_reports']:
            path = Path(name)
            copy(path, ARCHIVE/'capture_reports'/path.parent.name/path.name)
    for path in SHOTS.iterdir():
        if path.is_file():
            copy(path, ARCHIVE/'fixture_screenshots'/path.name)
    copy(Path('work/analysis/dialogue_formatting_user_recheck_v780/COMMON676_677.json'), ARCHIVE/'user_formatting_watch/COMMON676_677.json')
    files = {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'archive_manifest.json'}
    save(ARCHIVE/'archive_manifest.json', {'candidate': latest, 'files': files, 'full_goal_complete': False})
    assert all(sha((ARCHIVE/p).read_bytes()) == pin for p, pin in files.items())
    print('V780 recorded and archived: 367 completed, three drafts; the wider editorial goal and graphics audit remain active.', flush=True)


if __name__ == '__main__':
    main()
