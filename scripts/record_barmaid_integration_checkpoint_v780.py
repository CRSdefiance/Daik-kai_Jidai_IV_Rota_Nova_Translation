"""Record verified integration and one paired family; keep the batch unfinished."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/barmaid_integration_v780')
DOC = Path('docs/barmaid_v780_integration_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V780 Barmaid integration in progress')
SHOTS = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V780 Barmaid dialogue')


def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert sha(source.read_bytes()) == sha(target.read_bytes())


def main():
    rom = Path('out/all_routes_combined_v780_candidate.nds')
    digest = sha(rom.read_bytes())
    manifest = read(rom.with_suffix('.manifest.json'))
    patch = read(ROOT/'patch_proof.json')
    release = read(ROOT/'registered_verification.json')
    game = read(ROOT/'seville_intro_gameplay_verification.json')
    boot = read(ROOT/'newgame_regression.json')
    context = read(ROOT/'latent996_caller_closure.json')
    layout = read(ROOT/'scoped_layout_verification.json')
    manuscript = read('translations/barmaid_editorial_manuscript_v2.json')
    assert digest == manifest['candidate_sha256'] == patch['candidate_sha256'] == release['candidate_sha256'] == game['candidate_sha256']
    assert all(manifest['checks'].values()) and patch['byte_exact_reconstruction']
    assert release['all470_batches114_accepted_layers_and_graphics_retained'] and release['all7336_complete_native_copies']
    assert len(manuscript['records']) == 31 and all(all(r['review'].values()) for r in manuscript['records'])
    assert context['retained_latent996_context_classified'] and context['ordinary_996_activation_not_claimed']
    assert layout['count'] == 273 and not layout['unresolved_layout_findings']
    assert len(game['holds']) == 2 and len(game['whole_screen_controls']) == 89
    assert len(game['paired_state_model_object_task_frames']) == 88
    assert len(boot['whole_screen_frame_pairs']) == 7 and boot['all_pixels_exact']
    protected = read('work/analysis/barmaid_editorial_v779/checkpoint.json')['protected_files_unchanged']
    for path, pin in protected.items():
        assert sha(Path(path).read_bytes()) == pin, path
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert ledger['records_editorially_completed'] == 336 and ledger['records_with_source_and_prose_pass'] == 370
    assert ledger['current_integrated_candidate']['profile'] == 'all-routes-unified-v778'
    assert len(ledger['active_source_prose_drafts']['native_message_IDs']) == 34
    checkpoint = {
        'candidate': str(rom), 'candidate_sha256': digest, 'profile': manifest['profile'],
        'manifest': str(rom.with_suffix('.manifest.json')), 'exact_patch': str(ROOT/'patch_proof.json'),
        'source_context_native_formatting_approved_IDs': list(range(989, 1020)),
        'manuscript': 'translations/barmaid_editorial_manuscript_v2.json',
        'registered_verification': str(ROOT/'registered_verification.json'),
        'paired_actual_intro989': str(ROOT/'seville_intro_gameplay_verification.json'),
        'ordinary_newgame_regression': str(ROOT/'newgame_regression.json'),
        'user676_677_formatting_preserved': 'work/analysis/dialogue_formatting_user_recheck_v780/COMMON676_677.json',
        'pending_actual_families': game['other_barmaid_families_pending'],
        'new_editorially_completed': 0, 'latest_pointer_unchanged_until_batch_verification': True,
        'protected_files_unchanged': protected, 'graphics_audit_and18_original_plaques_still_unfinished': True,
        'full_goal_complete': False, 'documentation': str(DOC)}
    save(ROOT/'integration_checkpoint.json', checkpoint)
    ledger['barmaid_integration_v780_in_progress'] = checkpoint
    drafts = ledger['active_source_prose_drafts']
    drafts['status'] = '750-752-context-unmapped;989-1019-source-context-native-formatting-and-registered-integration-verified;actual-intro989-paired;remaining-barmaid-consumer-families-pending'
    drafts['note'] = 'V780 V2 supersedes historical V779 context996 and formatting gates.996 is retained latent source speech with original guard/catalog unchanged;ordinary activation is not claimed. Zero new completion credit until representative actual families and transitions pass.'
    drafts['current_integration_manuscript'] = checkpoint['manuscript']
    ledger['coverage_units'][0]['next'] = 'Finish V780 actual intro990,ordinary chat,name-bearing gift999,other gift reactions and casual chat with disclosed fixtures,paired native/state/pixel checks and normal returns. Then complete batch accounting and continue1020 onward,750-752 contexts,wider shared/all routes/player-facing prose. Preserve separate graphics audit and older-record follow-up.'
    ledger['latest_checkpoint'] = 'V780 registered combined ROM/exact patch verified;31 barmaid entries have approved source/context and273 production layouts. Original996 guard/caller closure is complete as retained latent speech,without ordinary activation.34343 scoped routing and7336 complete copies pass,no allocator/section/payload growth. Two Donna989 holds have complete independent font/blank-paper checks;89 whole controls/88 state-model-task pairs and normal town return pass. Seven ordinary New Game pairs match.336 completed/370 source-prose/34 active drafts and V778 latest remain unchanged;other actual barmaid families,wider prose and graphics remain open.'
    save(ledger_path, ledger)
    DOC.write_text('''# V780: integrated barmaid dialogue, gameplay verification in progress

31 source-reviewed entries989–1019 are in a registered combined experimental ROM.
Fourteen are revised and17 retain their wording. Source/context/native formatting
approval does not yet complete this batch: actual introduction990,ordinary chat,
name-bearing gift999,other gift responses and casual chat remain to be checked.
336 completed(245 revised/91 retained),370 source/prose and34 active drafts remain.
V778 remains the latest verified editorial checkpoint;the full goal is active.

## Integration and formatting

The original996 city58 branch has no initialized barmaid lookup. Full caller/guard
closure retains that latent original speech without inventing an activation or
changing the catalog. Three address-looking scan windows are classified using
unchanged source ARM instructions and the complete4096-pair numeric table;no generic
unaligned-pointer exemption is introduced. Historical V779 failures stay preserved.

The private numeric table grows110 to114 bytes inside its existing128-byte owner;
the140-byte gate is unchanged.34343 exact routing/ABI cases and273 production
layouts pass,including legal16-byte edited first names and CP932 cases. Five naive
article warnings are bound to actual name bytes,with a literal-prose negative.
There are no unresolved layout findings. Existing sections,cache,arena and123040-
byte staged payload do not grow. The smallest fitting contiguous COMMON repack is
blocks12–35;opaque1854/1865 post-NUL tails are preserved.3637 other visible strings
and17 other blocks stay exact.7336 complete warm/cold native copies pass.

The integrated builder retains470 batches/114 accepted layers and earlier graphics.
Only COMMON and ARM9 differ from V778;11 malformed release controls are rejected.
The clean-input xdelta reconstructs every candidate byte. User676/677 repaired
wording and native wrapping remain exact in V780;the earlier actual V747 cooking
capture was visually reviewed,without claiming a fresh V780 shop activation.

## Actual paired evidence

Two37600-frame cold boots load protected copies of the London donor and use three
declared coordinate fixtures to reach Seville. The fixture changes only the active
ship's eight coordinate bytes;original discovery,story and docking logic still run.
No normal voyage or earned unlock is claimed. Original donor hashes remain exact.
An initial Hamburg pilot did not dock and earns no dialogue completion credit.

Actual Donna989 at35600/36000 contains Donna then Hodram,all leading/trailing glyphs,
three aligned lines and exact blank-paper cells. Both complete native font planes
independently match the game font.89 other whole screenshots match V778;88 paired
state/model/object/task snapshots match. Original dismissal,Tavern exit and town
return complete normally. Seven separate ordinary New Game framebuffer pairs match
with no battery save,savestate or gameplay fixture. These are targeted emulator
tests,not a full playthrough or hardware verification.

Bounded future gift fixtures use the original transfer for one of three declared
category7 gifts. Six source/current native cases and invalid-input controls pass;
only the selected item and acquisition-history vector may change.4A224 returns
literal mask4,not boolean1;the first research assertion was corrected without an
extra game-state write. This probe does not establish actual gift conversations.

## Candidate and remaining scope

- ROM: `out/all_routes_combined_v780_candidate.nds`
- SHA256: `16f090605a37ab91f73769b5371d2dfe4a13ad445d7a78940aa404f9bdf495ee`
- Profile: `all-routes-unified-v780` (experimental,incomplete gameplay verification)
- Patch SHA256: `ce60c722242098b5d7c24ab6c1d8be301b9ee7a3f0a954d091b66cba3a3348fd`
- Clean input: `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`
- Canonical base: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`

Finish the remaining original consumer families and paired transitions before
granting31 completed entries or updating the latest verified pointer.750–752,
1020 onward,wider shared/all routes/other prose and the separate graphics audit,
including18 original plaques,remain unfinished. Low-resolution Online bodies remain
excluded;brown marks stay preserved. Revisit older record-based checks when the
full goal completes. No canonical promotion,GitHub commit or push was performed.
Fixture screenshots and provenance are on E and are not promoted to the guide.
''', encoding='utf-8')
    summary = '\n\n## V780: registered barmaid integration and first paired family\n\n31 source/context/native-approved entries,273 production layouts,34343 routing cases,7336 complete copies and exact clean patch pass without section/cache/arena/payload growth. Original996 is retained latent speech after full source guard/caller closure;ordinary activation unclaimed. Two actual Donna989 holds have complete font/paper masks;89 whole controls,88 state/model/task pairs and normal town return pass. Seven ordinary New Game pairs match. Other intro/gift/ordinary/casual families remain required,so336 complete/370 source-prose/34 drafts and V778 latest remain unchanged. Broader prose,18 plaques and separate graphics audit stay open. See [V780 integration checkpoint](barmaid_v780_integration_checkpoint.md).\n'
    for path in map(Path, ('docs/translation_progress.md', 'docs/known_issues.md', 'docs/todo.md')):
        text = path.read_text(encoding='utf-8')
        if '## V780: registered barmaid integration and first paired family' not in text:
            path.write_text(text+summary, encoding='utf-8')
    files = [DOC, ledger_path, rom.with_suffix('.manifest.json'), Path('translations/barmaid_editorial_manuscript_v2.json'),
             Path('translations/barmaid_editorial_release_v1.json'), *ROOT.glob('*.json'),
             Path('scripts/verify_barmaid_gameplay_v780.py'), Path(__file__).resolve().relative_to(Path.cwd().resolve()),
             Path('scripts/run_barmaid_location_capture_v780_v2.py'), Path('scripts/native_barmaid_location_fixture_v780_v2.py'),
             Path('scripts/run_barmaid_gift_capture_v780.py'), Path('scripts/native_barmaid_gift_fixture_v780.py')]
    archived = []
    for source in files:
        target = ARCHIVE/source
        copy(source, target)
        archived.append({'source': str(source), 'target': str(target), 'sha256': sha(source.read_bytes())})
    for hold in game['holds']:
        source = Path(hold['capture']['path'])
        copy(source, SHOTS/f'Donna_intro989_{hold["frame"]}.png')
    save(SHOTS/'provenance.json', {'gameplay': game, 'scope': 'Authorized coordinate fixture;original docking and dialogue;not earned travel or guide promotion.'})
    save(ROOT/'integration_checkpoint_archive.json', {'files': archived, 'full_goal_complete': False})
    print('V780 integrated/partial gameplay checkpoint archived;336 completions and V778 latest unchanged.', flush=True)


if __name__ == '__main__':
    main()
