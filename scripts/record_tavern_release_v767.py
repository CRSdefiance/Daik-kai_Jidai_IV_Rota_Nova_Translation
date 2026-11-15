"""Record31 integrated Tavern editorial reviews with explicit actual-test scope."""

import ast
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_tavern_release_v767 import CONFIG, MANUSCRIPT, ROOT
from scripts.record_memory_streams_v682 import copy
from scripts.verify_tavern_gameplay_v767 import ROM
from scripts.verify_village_wrap_v608 import read, save

LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/tavern_editorial_v767_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V767 Tavern dialogue')
SHOTS = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V767 Tavern dialogue')


def main():
    assert not ARCHIVE.exists() and not SHOTS.exists()
    config, manuscript = read(CONFIG), read(MANUSCRIPT)
    manifest = read(ROM.with_suffix('.manifest.json')); digest = sha(ROM.read_bytes())
    registered, patch, game, extra = [read(ROOT / name) for name in ('registered_verification.json', 'patch_proof.json', 'gameplay_verification.json', 'extra_gameplay_verification.json')]
    assert digest == manifest['candidate_sha256'] == registered['candidate_sha256'] == patch['candidate_sha256'] == game['candidate_sha256'] == extra['candidate_sha256']
    assert all(manifest['checks'].values()) and all(registered['negative_gates'].values()) and patch['byte_exact_reconstruction']
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    for p, h in config['dependencies'].items(): assert sha(Path(p).read_bytes()) == h, p
    assert sha(MANUSCRIPT.read_bytes()) == config['manuscript_sha256']
    for filename, report in (('verify_tavern_gameplay_v767.py', game), ('verify_tavern_extra_gameplay_v767.py', extra)):
        assert report['producer_sha256'] == sha((Path('scripts') / filename).read_bytes())
    protected = {'out/all_routes_combined_v762_candidate.nds': '03056eb9210cfcdc8462af496abade520ccb8d871a611fe29691d7b56c0ec22a',
        'work/clean.nds': 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',
        'out/raphael_natural_v2_accepted_base.nds': '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        'E:/Rota Nova translations/Saves/hodram-istanbul-golden-cutlass-blue-oak-v474.dsv': 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132',
        'E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv': 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132',
        'E:/Rota Nova translations/Generated/work/emulation_v193/full_fleet_staffing_v652_actual/saves/all_routes_combined_v651_candidate.dsv': 'febc859c5af2df6fa8023c349bb7f31b5fc15ea769fb2eea527b3a3f80521731'}
    for p, h in protected.items(): assert sha(Path(p).read_bytes()) == h, p
    ledger = read(LEDGER)
    assert (ledger['records_editorially_completed'], ledger['records_revised_and_integrated'], ledger['retained_wordings_editorially_completed']) == (167, 124, 43)
    assert ledger['records_with_source_and_prose_pass'] == 201
    assert ledger['active_source_prose_drafts']['native_message_IDs'] == [750, 751, 752, *range(820, 851)]
    save(ROOT / 'editorial_ledger_before_v767.json', ledger)
    save(ROOT / 'editorial_latest_before_v767.json', read('out/editorial_review_latest.json'))
    ids = list(range(820, 851)); retained = [822, 824, 825, 827, 834, 839, 846, 847]
    holds = game['six_complete_actual_holds'] + extra['two_additional_complete_actual_holds']
    actual = sorted({r['message_id'] for r in holds}); assert actual == [821, 823, 826, 827, 850]
    family = 'Tavern-rumor-gift-directions-and-trend-replies820-850'
    ledger['completed_editorial_families'].append({'id': family, 'native_message_IDs': ids,
        'records': [{'message_id': n, 'decision': 'retained-wording-reviewed' if n in retained else 'revised-and-integrated',
            'manuscript': str(MANUSCRIPT), 'complete_source_context_and_native_font_verified': True,
            'actual_display_verified': n in actual} for n in ids], 'integrated_ROM_sha256': digest,
        'proof': str(ROOT / 'proof.json'),
        'gameplay_scope': 'Eight complete actual holds across821/823/826/827/850;31 ordinary UI/control pairs with explicitly verified animation phases;19 native state/object pairs;seven New Game frames. Other26 IDs have complete source/native/font coverage and family sampling. Gift transfer and the coordinate hint are not claimed individually activated in-game.'})
    ledger.update({'records_editorially_completed': 198, 'records_revised_and_integrated': 147,
        'retained_wordings_editorially_completed': 51,
        'latest_checkpoint': 'V767 integrates31 Tavern entries:198 reviewed (147 revised/51 retained).38957 native layouts,166 fonts,14400 leader-name layouts,104 whole8MiB coordinate contracts,202 original provider fragments,7336 whole warm/cold copies and exact clean patch pass. Eight actual holds across five IDs,UI/return/native object pairs and seven New Game frames pass.750-752,851 onward,wider shared/Lil/all routes/other prose and graphics remain open.'})
    ledger['active_source_prose_drafts'] = {'native_message_IDs': [750, 751, 752],
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],
        'status': 'source-prose-only-context-activation-unmapped-not-integrated',
        'note': 'Map actual caller/packed-script context before integration;an absent literal reference does not prove unused text.'}
    ledger['coverage_units'][0]['completed_families'].append(family)
    ledger['coverage_units'][0]['next'] = 'Review851 onward and remaining750-752 caller context,then broader shared prose,Lil/all routes and other player-facing text. Preserve the separate graphics audit and older-record follow-up.'
    for finding in ledger['findings']:
        if finding.get('id') in ('COMMON-843-845-untranslated-qualitative-distance-provider', 'COMMON-842-coordinate-argument-leading-LF-and-spacing',
            'COMMON-826-drinking-context-and840-gift-promise', 'COMMON-848-850-commodity-grammar-and-reported-popularity',
            'COMMON-820-821-native-name-role-correction', 'COMMON-842-compass-letter-number-line-split'):
            finding['status'] = 'source-native-reviewed-integrated-with-family-gameplay-samples-V767'
            finding['resolution_proof'] = str(ROOT / 'proof.json'); finding['actual_display_scope'] = actual
    ledger['current_integrated_candidate'] = {'path': str(ROM), 'sha256': digest, 'profile': manifest['profile'],
        'MESFILE_sha256': config['target_common_sha256'], 'ARM9_sha256': config['target_arm9_sha256'],
        'patch_sha256': patch['patch_sha256'], 'status': 'experimental', 'manifest': str(ROM.with_suffix('.manifest.json')),
        'initial_source_pins_retained_as_V743_reference_not_overwritten': True}
    records = [r for f in ledger['completed_editorial_families'] for r in f['records']]
    assert len(records) == len({r['message_id'] for r in records}) == 198
    assert sum(r['decision'] == 'revised-and-integrated' for r in records) == 147
    assert ledger['full_goal_complete'] is False and ledger['goal_status'] == 'active'
    save(LEDGER, ledger)
    save('out/editorial_review_latest.json', {**ledger['current_integrated_candidate'], 'details': str(DOC), 'full_goal_complete': False})
    DOC.write_text(f'''# V767: integrated Tavern editorial review

Thirty-one entries820-850 complete review:23 revised and8 retained (822,824,825,827,834,839,846,847). Total reviewed198:147 revised/51 retained. Source/prose201 includes only the three750-752 drafts awaiting actual caller context. The full editorial goal remains active;851 onward,wider shared dialogue,Lil/all routes,remaining prose and the unresolved graphics audit remain unfinished.

## Faithful natural English and formatting

The review restores complete questions,the gift recipient's promise to treasure the present,reported versus prospective trends and commodity popularity.826 is a teasing response to declining another drink;it does not describe combat ability. Mass/plural goods use natural sales/craze wording. Captain identification/request variants keep their independent native slots. Native person names are preserved:ordinary virtual+24 supplies a surname,not a synthesized full name. Rafael,Joakim,Maria andCamille stay approved.

All prose is one paragraph. Native wrapping preserves complete first/final letters,whole words,consistent margins,four-row bounds,pagination and literal supplied names. Function-local private English providers replace Japanese qualitative distance morphemes without changing shared compass labels. Original direction order and qualitative thresholds remain intact;no miles/days/degrees are invented. Direct842-only post-printf formatting displaysN24 E120 style pairs so a compass letter cannot separate from its number. The global coordinate provider remains unchanged. Original printf output and every non-whitespace coordinate byte are preserved.

## Storage and complete message copies

The existing17-block packing spilled three messages despite sufficient overall byte capacity. The integration uses the existing19 blocks2-20,keeping the same4096-byte cache and41 directory entries. The complete1813-selection map164-1976 preserves all3637 unselected text strings and22 other blocks. Two opaque native copy tails at1854/1865 are copied whole,including post-NUL bytes;none is guessed to be padding. Every one of7336 warm/cold native copies is checked through its entire span,including opaque tails. Only proved NUL/ASCII-space gaps are removed.

The strict parser adds one exact directory digest. Four explicit replay configurations preserve unchanged prior Market stock,Market contract,Shipyard andPort stage outputs;their frozen originals remain intact. All470 batches,114 accepted layers and prior graphics survive. Runtime code/data occupy proved retired source allocations,with all57 active replacements preserved. Native bank write checks,source alias/branch/ADR/cross-string checks,full register/stack contracts and cache/section checks pass. The123040-byte staged payload,startup allocation and cache bounds do not grow.

## Evidence and limits

- 38957 complete native layouts,166 independent full font planes and14400 current-leader-name combinations pass. All14 earlier contact sheets plus four changed coordinate planes were visually reviewed;162 unchanged planes are pixel-identical to the inspected set.
- 104 complete8MiB memory/register comparisons preserve every non-whitespace coordinate byte and every unowned buffer/code/guard byte.202 original provider fragments,94 unchanged global-coordinate outputs and256 profession enums pass.1124 earlier Yard layouts,40 Port cases and180 other native output controls remain exact.
- The final ROM passes13 malformed-input gates,complete source/current/new string comparisons and exact clean-input patch reconstruction.
- Eight complete actual holds cover821,823,826,827 and850. Native printf/wrap buffers,resident blocks,entire independently decoded glyph planes,blank paper and all unmodified pixels are checked. The additional drink-refusal andAthens/Armor rumor branches use ordinary inputs,not RAM fixtures.
- Twenty-four complete screen controls and seven extra UI/return comparisons pass with explicit original animation-phase handling. Nineteen sampled native state/object pairs preserve active company/fleet/ships,all207 ordinary actors/current captain,90 towns,218 items and124 goods/reserved slot. Refusal dismisses normally to the Tavern menu andTown;paid drinks retain the original source behavior.
- The A advance icon can change phase because the revised text has a different duration. Each observed phase is pixel-identical to original captures,outside the full glyph plane. A401-frame Town-return comparison proves the selected Tavern tooltip has exactly the same two original pixel variants,with a three-frame phase offset;every other screen pixel is identical. No altered graphics are waived.
- Seven fixture-free New Game frames match the immediate parent through title,captain selection and intro. Canonical,clean and donor hashes remain unchanged. These are targeted automated cold-boot emulator tests,not a hardware test or full route playthrough. Other26 IDs have source/context/native/font coverage with family sampling;individual actual gift transfers and the coordinate hint are not claimed activated.

## Experimental combined build

- ROM:`{ROM}`;profile`{manifest['profile']}`;candidate SHA-256`{digest}`.
- Canonical base:`out/raphael_natural_v2_accepted_base.nds`,SHA-256`{protected['out/raphael_natural_v2_accepted_base.nds']}`. No promotion.
- COMMON SHA-256`{config['target_common_sha256']}`;ARM9 SHA-256`{config['target_arm9_sha256']}`.
- Exact patch:`{ROM.with_suffix('.xdelta')}`;SHA-256`{patch['patch_sha256']}`. Clean input SHA-256`{protected['work/clean.nds']}`.
- Relative to V762 only`/COMMON/MESFILE.DK4` and`/__arm9__.bin` change;all other files,ARM7 and overlays stay exact.
- Verifiers:`verify_tavern_coordinates_v766.py`,`verify_coordinate_buffers_v766.py`,`verify_tavern_prior_v766.py`,`verify_tavern_providers_v766.py`,`verify_tavern_copies_v767.py`,`verify_tavern_release_v767.py`,`verify_tavern_gameplay_v767.py`,`verify_tavern_extra_gameplay_v767.py`,`verify_town_animation_v767.py`.
- User acceptance remains pending for cold-boot title/New Game,town/Tavern UI,drink refusals,rumors,gifts and location hints. Work can continue without further preview approval.

ROM,manifest,patch,evidence and six native screenshots for possible guide use are saved on E. The original18 plaque entries remain in the separate unfinished audit;Online-body exclusion,preserved brown marks and the later older-record follow-up are unchanged. Thirteen unclassified ordinary name-table slots remain open for consumer/source review.
''', encoding='utf-8')
    summary = '\n\n## V767: integrated Tavern editorial review\n\n31 entries complete:198 reviewed overall (147 revised/51 retained). Private English direction/profession providers and direct842 typed coordinate pairs preserve all source facts/arguments.38957 layouts,166 full fonts,14400 name combinations,104 whole8MiB contracts,7336 whole native copies and exact clean patch pass. Eight actual holds across five IDs,normal returns/native objects and seven New Game frames pass;original advance/tooltip animation variants are explicitly verified. Other26 IDs have source/native/font coverage with family sampling.470/114 layers and prior graphics retained.750-752,851 onward,wider shared/Lil/all routes/other prose and graphics remain open. Experimental;canonical/donors unchanged. See [V767 checkpoint](tavern_editorial_v767_checkpoint.md).\n'
    for filename in ('translation_progress.md', 'todo.md', 'known_issues.md'):
        path = Path('docs') / filename; text = path.read_text(encoding='utf-8')
        assert '## V767: integrated Tavern editorial review' not in text
        path.write_text(text.rstrip() + summary, encoding='utf-8')
    scripts = [*Path('scripts').glob('*tavern*v767.py'), Path('scripts/verify_town_animation_v767.py'),
        Path('dk4tool/patch/tavern_conversations_editorial.py'), Path('dk4tool/patch/tavern_coordinate_runtime.py')]
    for path in scripts: ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    reports = [ROOT / name for name in ('registered_verification.json', 'patch_proof.json', 'gameplay_verification.json',
        'extra_gameplay_verification.json', 'Town_tooltip_animation.json', 'native_integration.json', 'common_repack_plan.json', 'explicit_parser_replays.json')]
    save(ROOT / 'proof.json', {'candidate_sha256': digest, 'completed_total': 198, 'revised': 147, 'retained': 51,
        'new_completed_IDs': ids, 'actual_display_IDs': actual, 'protected_hashes': protected,
        'previous_goal_turn': 'progress: complete native research and typed coordinate fix archived',
        'this_goal_turn': 'progress: full registered ROM/exact patch,whole native copies and actual scene verification complete',
        'report_hashes': {str(path): sha(path.read_bytes()) for path in reports},
        'goal_status': 'active', 'full_goal_complete': False})
    selected_shots = [
        (game['six_complete_actual_holds'][0]['capture'], 'Hayreddin_rumor_V767.png'),
        (next(r['capture'] for r in game['six_complete_actual_holds'] if r['message_id'] == 827), 'Fatica_toast_V767.png'),
        (next(r['capture'] for r in game['six_complete_actual_holds'] if r['message_id'] == 823), 'Nearby_Ragusa_V767.png'),
        (next(r['capture'] for r in extra['two_additional_complete_actual_holds'] if r['message_id'] == 826), 'Declining_another_drink_V767.png'),
        (next(r['capture'] for r in extra['two_additional_complete_actual_holds'] if r['message_id'] == 850), 'Athens_Armor_rumor_V767.png')]
    town_report = read('E:/Rota Nova translations/Generated/work/emulation_v193/tavern_editorial_v767_decline_v767/capture_report.json')
    selected_shots.append((next(r for r in town_report['frames_captured'] if r['frame'] == 10600), 'Istanbul_Tavern_return_V767.png'))
    provenance = []
    for row, filename in selected_shots:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        target = SHOTS / filename; copy(Path(row['path']), target)
        provenance.append({'path': str(target), 'PNG_sha256': row['PNG_sha256'], 'source_capture': row,
            'ROM_sha256': digest, 'native_unedited_capture': True, 'experimental_guide_candidate_not_publication_approval': True})
    save(SHOTS / 'provenance.json', provenance)
    files = [*reports, ROOT / 'proof.json', DOC, LEDGER, CONFIG, MANUSCRIPT, ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'), *scripts]
    files += [ROOT / f'native_copies_block_{k:02d}.json' for k in range(41)]
    for path in files: copy(path, ARCHIVE / path.as_posix())
    for path in game['capture_reports'] + extra['capture_reports']:
        source = Path(path); copy(source, ARCHIVE / 'capture_reports' / source.parent.name / source.name)
    save(ARCHIVE / 'provenance.json', {'files': {p.relative_to(ARCHIVE).as_posix(): sha(p.read_bytes()) for p in ARCHIVE.rglob('*') if p.is_file()},
        'guide_screenshot_provenance': str(SHOTS / 'provenance.json'), 'full_goal_complete': False})
    for path, h in read(ARCHIVE / 'provenance.json')['files'].items(): assert sha((ARCHIVE / path).read_bytes()) == h
    print('V767 ROM/patch/evidence and6 guide screenshots hash-archived on E.198 reviewed;3 drafts;goal active.', flush=True)


if __name__ == '__main__': main()
