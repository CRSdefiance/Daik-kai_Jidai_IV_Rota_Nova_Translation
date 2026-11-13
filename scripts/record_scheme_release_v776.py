"""Record the verified scheme family without granting broader goal completion."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_schemes_integration_v776')
ROM = Path('out/all_routes_combined_v776_candidate.nds')
MANUSCRIPT = Path('translations/tavern_schemes_editorial_manuscript_v4.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/tavern_schemes_v776_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V776 Schemes')
SHOTS = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V776 Scheme dialogue')


def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert sha(source.read_bytes()) == sha(target.read_bytes())


def main():
    game = read(ROOT / 'gameplay_verification.json')
    manifest = read(ROM.with_suffix('.manifest.json'))
    patch = read(ROOT / 'patch_proof.json')
    registered = read(ROOT / 'registered_verification.json')
    layout = read(ROOT / 'scoped_layout_verification.json')
    inputs = read(ROOT / 'input_contract.json')
    watch = read('work/analysis/dialogue_formatting_user_recheck_v776/COMMON676_677.json')
    doc = read(MANUSCRIPT)
    digest = sha(ROM.read_bytes())
    assert digest == game['candidate_sha256'] == manifest['candidate_sha256'] == patch['candidate_sha256'] == registered['candidate_sha256'] == watch['sha256']
    assert patch['byte_exact_reconstruction'] and all(manifest['checks'].values())
    assert len(doc['records']) == 56 and sum(r['decision'] == 'revise' for r in doc['records']) == 44
    assert all(all(r['review'].values()) for r in doc['records'])
    assert game['actual_IDs'] == [909, 915, 921, 927, 933, 941, 949, 957]
    assert game['ordinary_town_return_frame'] == 31200 and len(game['actual_scheme_holds']) == 22
    assert layout['all39730_outputs_equal_reviewed_literal_layouts_without_findings']
    assert inputs['editable_company_name_does_not_reach_these_original_scheme_consumers']
    protected = read('work/analysis/recruitment_owned_v772/research_checkpoint.json')['protected_files_unchanged']
    protected.update({
        'out/all_routes_combined_v773_candidate.nds': '4b799e769123620bd4574b2dd6fc10ea38ce87d3d28ebc797a78349b1897415b',
        'E:/Rota Nova translations/Saves/hodram-london-rested-minimum-crew-v464.dsv': '05fa512b078fd01a8f6bee605254e9f72bfe3453c0ea098d977c87d86b6b693e'})
    for path, pin in protected.items():
        assert sha(Path(path).read_bytes()) == pin, path
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] in (255, 311)
    if ledger['records_editorially_completed'] == 255:
        save(ROOT / 'editorial_ledger_before_v776.json', ledger)
    else:
        assert (ROOT / 'editorial_ledger_before_v776.json').exists()
    latest = {
        'path': str(ROM), 'sha256': digest, 'profile': manifest['profile'],
        'MESFILE_sha256': registered['COMMON_sha256'], 'ARM9_sha256': registered['ARM9_sha256'],
        'patch_sha256': patch['patch_sha256'], 'status': 'experimental',
        'manifest': str(ROM.with_suffix('.manifest.json')), 'details': str(DOC),
        'initial_source_pins_retained_as_V743_reference_not_overwritten': True,
        'remaining_in_this_registered_batch': 'All56 scheme entries reviewed; wider shared/all-route/player-facing editorial and separate graphics audit remain unfinished.',
        'supplemental_verification': str(ROOT / 'gameplay_verification.json'), 'full_goal_complete': False}
    family = 'Tavern-eight-scheme-voice-tables908-963'
    records = []
    for row in doc['records']:
        n = row['message_id']
        records.append({
            'message_id': n, 'decision': 'revised-and-integrated' if row['decision'] == 'revise' else 'retain-wording',
            'manuscript': str(MANUSCRIPT), 'source_native_context_and_complete_font_verified': True,
            'ordinary_actual_display_verified': False,
            'actual_display_with_disclosed_qualification_fixture': n in game['actual_IDs'],
            'actual_display_scope': 'Eight original Gerhard voice selections cover all eight consumer tables; other48 voices have native selection/layout/font coverage, not individual gameplay activation. No earned qualifications or scheme outcomes claimed.',
            'English_argument_source_indices': row.get('English_argument_source_indices', []),
            'gameplay_evidence': str(ROOT / 'gameplay_verification.json')})
    if not any(r['id'] == family for r in ledger['completed_editorial_families']):
        ledger['completed_editorial_families'].append({'id': family, 'native_message_IDs': list(range(908, 964)), 'records': records})
    if family not in ledger['coverage_units'][0]['completed_families']:
        ledger['coverage_units'][0]['completed_families'].append(family)
    ledger.update({'records_editorially_completed': 311, 'records_revised_and_integrated': 235,
                   'retained_wordings_editorially_completed': 76, 'records_with_source_and_prose_pass': 314,
                   'records_with_source_prose_drafts': 314, 'current_integrated_candidate': latest})
    ledger['active_source_prose_drafts'] = {
        'native_message_IDs': [750, 751, 752],
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],
        'status': '750-752-context-unmapped', 'note': 'Caller mapping remains required before formatting approval or integration.'}
    ledger['coverage_units'][0]['next'] = 'Review964 onward, resolve750-752 native contexts, then wider shared/all routes/other player-facing prose. Keep separate graphics audit and older-record follow-up open.'
    ledger['latest_checkpoint'] = 'V776 completes56 scheme entries(44 revised/12 retained);311 total(235 revised/76 retained),314 source/prose,three active drafts750-752.39730 original-catalog layouts,7336 complete native copies,eight actual voice-table samples/22 holds,paired states,three cancellations,town return and seven ordinary New Game frames pass. Registered combined ROM/exact clean patch verified. Wider prose and graphics remain unfinished.'
    ledger['formatting_watchlist']['latest_scheme_research'] = {
        'proof': str(ROOT / 'scoped_layout_verification.json'),
        'source_input_contract': str(ROOT / 'input_contract.json'),
        'gameplay': str(ROOT / 'gameplay_verification.json'), 'formatting_approval': True,
        'scope': 'Only eight original scheme consumers with fixed nonplayer faction names. Edited-player-name stress warnings remain research for other consumers and are not globally waived.'}
    checkpoint = {'id': 'V776-schemes-integrated-and-gameplay-verified', 'documentation': str(DOC),
                  'new_editorially_completed': 56, 'revised': 44, 'retained': 12,
                  'manuscript': str(MANUSCRIPT), 'evidence': str(ROOT / 'gameplay_verification.json'),
                  'new_ROM': True, 'experimental': True, 'full_goal_complete': False}
    if not any(r['id'] == checkpoint['id'] for r in ledger['research_checkpoints']):
        ledger['research_checkpoints'].append(checkpoint)
    save(LEDGER, ledger)
    save('out/editorial_review_latest.json', latest)
    text = f'''# V776: eight scheme dialogue families integrated and verified

56 entries908–963 complete editorial review:44 revised and12 retained. Overall311
entries are complete(235 revised/76 retained),314 source/prose-reviewed. Three
drafts750–752 still require caller mapping.964 onward,other shared text,all routes
and other player-facing prose remain open. The separate graphics audit,including
the18 original plaques,is unfinished. The editorial goal remains active.

## Meaning and source inputs

Eight original voice tables preserve the Strategist role,all voices and correct
arguments. Lure Fleet confirms FACTION then TOWN;Forge Papers confirms two distinct
factions;Bad Rumors confirms TOWN then FACTION. Original target selectors exclude
the current faction at both steps. All20 nonplayer names come from immutable
information rows through original constructors and are not serialized as editable
names. Full caller/reference closure proves edited player-company names cannot
reach these consumers. Their stress-layout warnings remain applicable research
for other consumers;no global waiver is made. Natural-dialogue-v2 paragraphs
restore complete questions,hostile-rumor meaning and the original factual scope.
Rafael,Joakim,Maria and Camille remain the approved names.

## Runtime,layout and inheritance

A100-byte packed contract table and140-byte gate fit their existing128/144-byte
private spans.34343 selector/register/SP/LR cases pass at actual addresses. No
section,autoload,BSS,arena,cache or123040-byte staged payload grows. The original
font and formatter remain unchanged. Only COMMON and ARM9 differ from V773.
All470 batches,114 accepted layers,other ROM files and graphics remain exact.
Eleven malformed source/current/policy/layout/argument controls are rejected.

39730 complete original-catalog layouts pass through the production parent/table
dispatcher,matching the reviewed native outputs. Prior complete independent font
planes and visual previews cover all56 voice records.7336 complete warm/cold native
copies cover all3668 COMMON entries. Blocks2–29 are repacked within existing space;
the two structured opaque tails remain exact.3612 other strings,including the
user's repaired676/677,are unchanged. The earlier smaller range failed capacity
by42 bytes;the prose was preserved by using the smallest fitting block range.

## Actual automated emulator scope

Paired31200-frame cold boots compare V773 with V776 using copies of the protected
London donor. A bounded disclosed fixture changes three room/assignment bytes,
one experience word and one calendar word(+11 days). All other4MiB RAM bytes are
exact at insertion. Original eligibility logic exposes Schemes;no menu flags,
inventory,health,funds,location or code are injected. Gerhard's actual voice is1.
This does not claim earned qualifications,time progression,travel or story events.

22 actual holds cover909,915,921,927,933,941,949 and957:all eight original table
types. Complete independent native glyphs,blank paper,left margins,leading/trailing
letters,substitutions and bounds pass. All outside-dialogue pixels match;stock
advance phases match original ordinary-dialogue holds. Four menu-highlight phase
differences are separately matched to complete original baseline crops without
waiving glyphs. An additional original-baseline run captures those menu phases.
{len(game['whole_screen_controls'])} other complete screen controls and
{len(game['paired_state_model_object_frames'])} paired state/model/object frames
pass. Seven ordinary fixture-free New Game frames match V773.

Each scheme is cancelled through the normal No choice. The original no-contract
guard also remains unchanged. Funds40659→40644 reflect two ordinary drinks;no
scheme charge is committed. Normal town return appears at31200. Successful scheme
outcomes,all individual voice activations,full-route playthrough and physical
hardware verification are not claimed. Source/native/full-font coverage supports
the other48 voice records through the same verified consumer families.

The original assignment-only and early expert probes left Schemes hidden. They
remain research-only;the source-qualified V2 fixture resolves the original London
calendar/Speech threshold. Stale template RAM after dismissal is never counted as
a visible dialogue. One baseline run has seven extra prefixture boot captures;
they receive no paired credit. Frozen production manuscript/configuration pins
remain unchanged;this checkpoint supplies completed gameplay status separately.

## User formatting example and experimental candidate

The photographed676/677 cooking/fashion pitches were corrected in V747. The large
manual gap and stray Discover were removed. V776 ROM bytes and original native
wrapping remain exact;the earlier actual V747 cooking framebuffer was visually
reviewed. No fresh V776 activation of that shop scene is claimed. The ongoing
watchlist checks visible left margins,manual padding,full words,complete leading
and trailing letters,bounds,pagination and normal dismissal for every family.

- ROM:`{ROM}`;SHA-256:`{digest}`.
- Profile:`{manifest['profile']}`;experimental,not canonically promoted.
- Manifest:`{ROM.with_suffix('.manifest.json')}`.
- Patch:`{ROM.with_suffix('.xdelta')}`;SHA-256:`{patch['patch_sha256']}`.
- Clean input SHA-256:`{patch['clean_source_sha256']}`;whole ROM reconstructs exactly.
- Canonical base SHA-256:`{patch['canonical_base_sha256']}`;unchanged.
- Evidence:`{ROOT / 'gameplay_verification.json'}` and neighboring source/native/
  layout/copy/patch proofs. Original donor saves remain unchanged.

ROM,patch,manifest,evidence and disclosed test-fixture screenshots are archived on
E:/Rota Nova translations. Screenshots are not represented as earned guide scenes.
No GitHub commit/push or canonical acceptance was made by this checkpoint.
'''
    DOC.write_text(text, encoding='utf-8')
    heading = '## V776: scheme dialogue integrated and verified'
    section = f'\n\n{heading}\n\n56 entries complete(44 revised/12 retained):311 total(235 revised/76 retained),314 source/prose. Three drafts750-752 remain;964 onward,wider shared/routes/prose and separate graphics audit remain open.39730 source-catalog layouts,7336 native copies,22 actual holds/eight tables,paired states,three cancellations,town return and seven ordinary New Game frames pass. Registered combined ROM/exact clean patch preserves470/114 inherited layers and repaired676/677. Experimental;canonical and original saves unchanged. See [V776 checkpoint](tavern_schemes_v776_checkpoint.md).\n'
    for name in ('translation_progress.md', 'todo.md', 'known_issues.md'):
        path = Path('docs') / name
        prior = path.read_text(encoding='utf-8')
        if heading not in prior:
            path.write_text(prior.rstrip() + section, encoding='utf-8')
    provenance = []
    for n in game['actual_IDs']:
        row = next(r['capture'] for r in game['actual_scheme_holds'] if r['message_ID'] == n)
        target = SHOTS / f'COMMON_{n}_V776_fixture.png'
        copy(Path(row['path']), target)
        provenance.append({'path': str(target), 'source': row, 'ROM_sha256': digest,
                           'unedited_native_capture': True, 'qualification_fixture': True,
                           'earned_scene_or_guide_publication_claim': False})
    save(SHOTS / 'provenance.json', provenance)
    save(ROOT / 'checkpoint.json', {'candidate': latest, 'new_completed_IDs': list(range(908, 964)),
                                   'protected_files_unchanged': protected, 'goal_status': 'active',
                                   'full_goal_complete': False, 'producer_sha256': sha(Path(__file__).read_bytes())})
    for path in ROOT.rglob('*'):
        if path.is_file() and path.suffix.lower() != '.nds':
            copy(path, ARCHIVE / 'evidence' / path.relative_to(ROOT))
    paths = [ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'), DOC, LEDGER,
             MANUSCRIPT, Path('translations/tavern_schemes_editorial_release_v1.json'),
             Path('translations/release_stack.json'), Path('out/editorial_review_latest.json'),
             Path('dk4tool/patch/tavern_schemes_runtime.py'), Path('dk4tool/patch/tavern_schemes_editorial.py'),
             Path('dk4tool/script/common_message_table.py'), Path('scripts/build_integrated_release.py')]
    paths += sorted(Path('scripts').glob('*v776*.py'))
    paths += sorted(Path('translations').glob('*replay_for_v776.json'))
    for path in paths:
        copy(path, ARCHIVE / path)
    for path in SHOTS.iterdir():
        if path.is_file():
            copy(path, ARCHIVE / 'fixture_screenshots' / path.name)
    for report in game['capture_reports']:
        path = Path(report)
        copy(path, ARCHIVE / 'capture_reports' / path.parent.name / path.name)
    files = {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
             if p.is_file() and p.name != 'archive_manifest.json'}
    save(ARCHIVE / 'archive_manifest.json', {'candidate': latest, 'files': files, 'full_goal_complete': False})
    assert all(sha((ARCHIVE / p).read_bytes()) == h for p, h in files.items())
    print('V776 recorded and archived:311 complete,three drafts;broader editorial and graphics work open.', flush=True)


if __name__ == '__main__':
    main()
