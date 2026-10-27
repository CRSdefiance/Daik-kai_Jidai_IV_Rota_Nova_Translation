"""Close the seventeen-entry Market packet, preserving wider editorial scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_market_stock_v757 import CONFIG, MANUSCRIPT, ROOT
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v757_candidate.nds')
LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/market_stock_v757_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V757 Market stock and letters')
BALANCED = Path('work/analysis/market_balanced_v757')


def main():
    assert not ARCHIVE.exists()
    registered, game, patch = [read(ROOT / f) for f in ('registered_verification.json', 'gameplay_verification.json', 'patch_proof.json')]
    matrix, abi = [read(BALANCED / f) for f in ('native_layout_matrix_RESEARCH.json', 'ownership_ABI.json')]
    doc, config = read(MANUSCRIPT), read(CONFIG)
    manifest = read(ROM.with_suffix('.manifest.json'))
    digest = sha(ROM.read_bytes())
    assert digest == manifest['candidate_sha256'] == registered['candidate_sha256'] == game['candidate_sha256'] == patch['candidate_sha256']
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['profile'] == 'all-routes-unified-v757' and len(manifest['batches']) == 470
    assert all(manifest['checks'].values()) and all(registered['rejections'].values())
    assert matrix['count'] == 31013 and matrix['layout_findings_count'] == 0
    assert len(abi['all80_non_direct_post_format_output_and_ABI_controls']) == 80
    assert game['all_sampled_frames_and_persistent_models_equal_V756'] and len(game['actual_V757_replays']) == 5
    assert patch['whole_ROM_byte_exact']
    for p, h in config['dependencies'].items():
        assert sha(Path(p).read_bytes()) == h, p
    assert sha(MANUSCRIPT.read_bytes()) == config['manuscript_sha256']
    pins = {
        'work/clean.nds': 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',
        'out/raphael_natural_v2_accepted_base.nds': '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        'E:/Rota Nova translations/Saves/hodram-istanbul-golden-cutlass-blue-oak-v474.dsv': 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132',
        'E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv': 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'}
    for p, h in pins.items():
        assert sha(Path(p).read_bytes()) == h, p
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 103 and ledger['records_revised_and_integrated'] == 69
    assert ledger['retained_wordings_editorially_completed'] == 34
    assert ledger['active_source_prose_drafts']['native_message_IDs'] == list(range(767, 784))
    save(ROOT / 'editorial_ledger_at_V755.json', ledger)
    family = 'Market-stock-and-letter-replies767-783'
    ledger['completed_editorial_families'].append({'id': family, 'native_message_IDs': list(range(767, 784)),
        'records': [{'message_id': r['message_id'], 'decision': 'retained-wording-reformatted' if r['message_id'] in (779, 780) else 'revised-and-integrated',
                     'manuscript': str(MANUSCRIPT), 'source_context_and_complete_native_layout_verified': True,
                     'actual_display_verified': r['message_id'] in (767, 768)} for r in doc['records']],
        'integrated_ROM_sha256': digest, 'proof': str(ROOT / 'proof.json'),
        'gameplay_scope': 'Actual767/768 in three product scenarios; remaining15 source/native font coverage, not all reward activations.'})
    ledger.update({'records_editorially_completed': 120, 'records_revised_and_integrated': 84,
        'retained_wordings_editorially_completed': 36, 'records_with_source_and_prose_pass': 120,
        'records_with_source_prose_drafts': 120,
        'latest_checkpoint': 'V757 completes Market767-783:15 revised,2 retained. Source-faithful prose, caller-scoped balanced layout,7336 native copies and targeted actual trade/reply/New Game verification. Wider shared/routes and graphics audit remain open.'})
    ledger['active_source_prose_drafts'] = {'native_message_IDs': [], 'manuscripts': [],
        'note': 'Market767-783 closed at V757. Further shared/town/route prose remains unreviewed.'}
    ledger['coverage_units'][0]['completed_families'].append(family)
    ledger['coverage_units'][0]['next'] = 'Review Market750-752,754-761 and784 onward, then wider shared prose, Lil and every route. COMMON761 actual argument is Palace (a building/authority), not a city; review source caller before wording.'
    ledger['findings'].extend([
        {'id': 'COMMON-767-783-stock-and-letter-fidelity', 'native_message_ids': list(range(767, 784)),
         'status': 'source-native-family-gameplay-sample-integrated-V757',
         'detail': 'Restored stock/gratitude, hesitation/favor, letter introduction/recommendation/upgrade and location eligibility; seven generic service-price placeholders replaced.779/780 wording retained.'},
        {'id': 'COMMON-768-extra-blank-page', 'native_message_id': 768, 'status': 'resolved-integrated-V757',
         'detail': 'Remove old three blank rows. Actual reply/favor/farewell/Power+2/dismissal verified. Original randomized fleet-footer decrement can differ with changed text timing; same SDK seed produces identical full models and scenes.'},
        {'id': 'COMMON-761-palace-contract-word-split', 'native_message_id': 761, 'status': 'open-source-and-format-review',
         'detail': 'Actual V754 baseline probe at4800 displays Palace and splits first as fir/st. The runtime argument is a building/authority name, not a city. Preserve this evidence for next source/caller review.',
         'evidence': 'E:/Rota Nova translations/Generated/work/emulation_v193/market_v756_trade_baseline_probe/capture_report.json'}])
    ledger['formatting_watchlist']['reference_case'] += ' V757 preservation rechecks676/677 and the complete inherited family; all future batches retain the same visible-margin/word/bounds/pagination checks.'
    ledger['current_integrated_candidate'] = {'path': str(ROM), 'sha256': digest, 'profile': manifest['profile'],
        'MESFILE_sha256': config['target_common_sha256'], 'ARM9_sha256': config['target_arm9_sha256'],
        'patch_sha256': patch['patch_sha256'], 'status': 'experimental', 'manifest': str(ROM.with_suffix('.manifest.json')),
        'initial_source_pins_retained_as_V743_reference_not_overwritten': True}
    save(LEDGER, ledger)
    save('out/editorial_review_latest.json', {**ledger['current_integrated_candidate'], 'details': str(DOC), 'full_goal_complete': False})
    DOC.write_text(f'''# V757: Market stock and letters

Seventeen entries767-783 complete editorial review:15 revised and2 retained wordings779/780. Total120 reviewed,84 revised,36 retained. The editorial goal remains active; further Market/shared dialogue, Lil/all routes, other player-facing prose and the separate graphics audit remain open.

## Faithful prose and readable layout

Clean Japanese and36 original decision/argument fragments distinguish high demand and frequent stockouts, gratitude, hesitation and favorable treatment, introduction versus recommendation letters, letter upgrades and small-town versus any-town eligibility. Seven old generic service-price placeholders are replaced. No new service mechanic is invented. Natural American English retains every source substitution and source tone.

The four dynamic767-770 paragraphs are wrapped after the original commodity substitutions. Bounded retries avoid weak line endings and short final fragments without shortening source meaning. All31013 commodity combinations/static cases preserve complete word bytes, guarded buffers, up to four rows and35 visible characters per row; zero layout findings. All42 complete native font planes are pixel-identical to the previously inspected V756 planes. Thirteen static paragraphs use the established balanced paragraph compiler. No manual alignment or authored line breaks are introduced. The user's cooking-pitch676/677 correction from V747 is preserved, with its earlier actual-frame and V754 native recheck evidence retained. Uneven margins, padding gaps, split words, stray continuations, missing leading/trailing letters, bounds and blank pages remain ongoing checks.

## Scoped runtime and preserved storage

The adapter uses exclusively owned retired Japanese Gallery/item string spans. It checks original direct portrait parent02054014 and exact IDs767-770. Existing code elsewhere, ARM/Thumb saved-register and stack contracts, complete success/failure paths, section sizes,123040-byte staged payload, startup/cache/allocator bounds and fonts are preserved. No memory pool grows. All180 inherited complete output controls,80 explicit non-direct post-format controls,12 original helper ABI/guard cases, Thumb-1 instruction checks, complete unaligned pointer/branch owner scans and18340 dispatcher selections pass. Only the four intended direct selections differ.

Unpublished V756 lacked the full parent guard: queued callers with stale767-770 stack IDs could receive the new retry behavior. V756 is revoked as an unpublished research candidate; its original actual captures remain bound to their hashes. V757 adds the caller guard and relocates the small return stub into another proven retired source slot, preserving the intended direct outputs exactly. It rebuilds the complete V754 stack through the registered workflow.

Faithful prose adds280 bytes. Complete selections767-1712 are repacked across existing COMMON blocks10-18; each stays within4096 bytes. All946 boundaries are remapped, retaining all3651 unselected visible texts and32 other blocks. Only proven NUL/ASCII-space guard gaps are discarded. All7336 guarded warm/cold native copies pass, with the source file boundary supplied by the test harness; this is not a physical device IO claim.470 batches,114 accepted layers and675 inherited graphics remain present. Only COMMON and ARM9 differ from V754.

## Actual gameplay evidence and limits

Original Market transactions run in six paired V754/V756 cold boots using explicitly labeled6/8-byte share/cargo/demand fixtures. Complete native glyphs and blank-paper pixels pass in six actual767/768 holds: long product names and the short Rum/Tea edge case. Actual argument order is verified through the unchanged original caller/getters. All sampled original cash, cargo and market share states match. Old768's extra blank page is removed; favor765, farewell766, Power+2 and normal return are verified.

The one-product natural return differs in an original randomized fleet-footer number:18 versus22. Original source code subtracts2+rand(5); exact UI RNG draw counts are not claimed. This is recorded as a real model value difference, not animation or whole-image equality. A separate late SDK seed3 control gives20 in both, with whole company76/fleet132/ship140 bytes and seven complete return scenes equal. Cost/RNG code is unchanged. Earlier phase-matched controls are explicitly scoped.

Five fresh V757 cold boots replay the three transactions, the same-seed return and ordinary New Game: every sampled whole two-screen image and complete persistent model matches V756. Targeted emulator tests use no savestates, with unmodified original/disposable donor saves verified. New Game uses no save or fixture and covers intro, selection and story. These are targeted automated emulator captures, not a hardware test, full-route playthrough or proof of earned fixture prerequisites. Remaining15 entries have source/native-font coverage, not all actual letter reward activations. Full reward eligibility/effects remain outside this packet's evidence.

## Registered artifacts

- Candidate: `{ROM}`, experimental profile `{manifest['profile']}`.
- SHA256: `{digest}`.
- Patch SHA256: `{patch['patch_sha256']}`. Clean input SHA256: `{pins['work/clean.nds']}`. Full reconstruction is byte-exact.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA256 `{pins['out/raphael_natural_v2_accepted_base.nds']}`; unchanged and not promoted.
- Changed internal files relative V754: `/COMMON/MESFILE.DK4` and `/__arm9__.bin` (owned formatter code/data and COMMON metadata).
- Verifiers: `verify_market_balanced_matrix_v757.py`, `verify_market_balanced_owners_v757.py`, `verify_market_native_copies_v757.py`, `verify_market_stock_release_v757.py`, `verify_market_stock_gameplay_v756.py`, `verify_market_guard_gameplay_v757.py`; all completed with passing scoped evidence.
- ROM, manifest, exact patch, reports and labeled screenshots saved on E. User cold-boot acceptance remains pending; canonical promotion requires explicit acceptance.

Next:750-752,754-761,784 onward. Actual761 says Palace and splits first; do not repeat the earlier city-argument assumption. Wider shared prose, all routes and graphics/original18 audit entries remain open. Online-body exclusion and preserved brown marks remain. Older record-based checks remain a later follow-up.
''', encoding='utf-8')
    reports = [ROOT / n for n in ('visual_review.json', 'user_formatting_reference.json', 'native_integration.json', 'registered_verification.json', 'gameplay_verification.json', 'patch_proof.json')]
    reports += [BALANCED / n for n in ('native_layout_matrix_RESEARCH.json', 'ownership_ABI.json', 'experimental_dispatch.json')]
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
        'reviewed_IDs': list(range(767, 784)), 'revised_IDs': [i for i in range(767, 784) if i not in (779, 780)],
        'retained_wordings': [779, 780], 'reports': {str(p): sha(p.read_bytes()) for p in reports},
        'protected_files': pins, 'editorial_ledger_sha256': sha(LEDGER.read_bytes()), 'checkpoint_sha256': sha(DOC.read_bytes()),
        'full_goal_complete': False, 'canonical_promotion': False})
    summary = '\n\n## V757: Market stock and letters\n\nSeventeen entries complete:15 revised,2 retained;120 reviewed overall (84 revised/36 retained). Faithful source distinctions replace seven generic placeholders. Caller-scoped balanced wrap passes31013 combinations,42 native font planes,80 non-direct controls and7336 copies. Actual767/768 transactions, removed blank page, same-seed original return and New Game pass; five fresh V757 replays match whole V756 frames/models. Unpublished V756 is revoked for a missing parent guard; V757 fixes it. Exact clean patch,470/114 stack and675 graphics preserved. COMMON761 Palace argument/word split, further shared/routes and separate graphics audit remain open. See [V757 checkpoint](market_stock_v757_checkpoint.md).\n'
    for name in ('translation_progress.md', 'todo.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert '## V757: Market stock and letters' not in text
        path.write_text(text.rstrip() + summary, encoding='utf-8')
    shots = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V757 Market stock and letters')
    for mode in ('one', 'two', 'edge'):
        cap = read(Path('E:/Rota Nova translations/Generated/work/emulation_v193') / ('market_v757_' + mode + '_verified') / 'capture_report.json')
        for frame in (6000, 6400, 6800, 7800):
            row = next(r for r in cap['frames_captured'] if r['frame'] == frame)
            copy(Path(row['path']), shots / f'{mode}_{frame:06d}_controlled.png')
    save(shots / 'provenance.json', {'candidate_sha256': digest, 'explicit_share_cargo_demand_testing_fixtures': True,
        'earned_progress_not_claimed': True, 'proof': str(ROOT / 'gameplay_verification.json'),
        'files': {p.name: sha(p.read_bytes()) for p in shots.glob('*.png')}})
    files = [ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'), DOC, LEDGER, MANUSCRIPT, CONFIG,
             ROOT / 'proof.json', ROOT / 'editorial_ledger_at_V755.json', *reports, *ROOT.glob('native_copies_block_*.json'),
             *BALANCED.glob('draft_previews_*.png'), Path('translations/release_stack.json'),
             Path('dk4tool/patch/market_stock_editorial_v2.py'), Path(__file__)]
    files += list(Path('scripts').glob('*market*v757.py'))
    for path in files:
        copy(path, ARCHIVE / path.name)
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': digest,
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name != 'provenance.json'},
        'full_goal_complete': False})
    for name, h in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / name).read_bytes()) == h
    print('V757 recorded and archived:120 reviewed,84 revised,36 retained; full editorial goal remains active.', flush=True)


if __name__ == '__main__':
    main()
