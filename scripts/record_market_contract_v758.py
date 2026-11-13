"""Record eight integrated reviews and keep three unmapped source drafts open."""

import ast
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.market_contract_editorial import DIRECTORY
from scripts.prepare_market_contract_v758 import CONFIG, MANUSCRIPT
from scripts.record_memory_streams_v682 import copy
from scripts.review_market_contract_v758 import CURRENT, IDS, ROOT
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v758_candidate.nds')
LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/market_contract_v758_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V758 Market advice and contracts')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def main():
    assert not ARCHIVE.exists()
    config, doc, manifest = read(CONFIG), read(MANUSCRIPT), read(ROM.with_suffix('.manifest.json'))
    native, registered, game, patch = [read(ROOT / n) for n in ('native_review_RESEARCH.json', 'registered_verification.json', 'gameplay_verification.json', 'patch_proof.json')]
    digest = sha(ROM.read_bytes())
    assert digest == manifest['candidate_sha256'] == registered['candidate_sha256'] == game['candidate_sha256'] == patch['candidate_sha256']
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert all(manifest['checks'].values()) and all(registered['rejections'].values()) and patch['whole_ROM_byte_exact']
    assert len(manifest['batches']) == 470 and manifest['profile'] == 'all-routes-unified-v758'
    assert [r['message_id'] for r in doc['records']] == list(IDS)
    assert len(native['all9_complete_font_planes']) == 9 and native['all31013_inherited_stock_outputs_equal_V757']
    assert len(game['six_actual_full_dialogue_holds']) == 6
    for p, h in config['dependencies'].items():
        assert sha(Path(p).read_bytes()) == h, p
    assert sha(MANUSCRIPT.read_bytes()) == config['manuscript_sha256']
    pins = {
        str(CURRENT): 'd87d66f81ed3a5034ba4a6d758b70ae973461ae3733c6bd195e5a81139a6e057',
        'work/clean.nds': 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',
        'out/raphael_natural_v2_accepted_base.nds': '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        'E:/Rota Nova translations/Saves/hodram-istanbul-golden-cutlass-blue-oak-v474.dsv': 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132',
        'E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv': 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'}
    for p, h in pins.items():
        assert sha(Path(p).read_bytes()) == h, p
    def directories(p):
        tree = ast.parse(p.read_text(encoding='utf-8'))
        return next(ast.literal_eval(n.value.args[0]) for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'RELOCATED_DIRECTORY_HASHES' for t in n.targets))
    previous_parser = ROOT / 'common_message_table_before_v758.py'
    parser = Path('dk4tool/script/common_message_table.py')
    assert directories(parser) == directories(previous_parser) | {DIRECTORY}
    save(ROOT / 'parser_compatibility.json', {'previous_parser_sha256': sha(previous_parser.read_bytes()), 'current_parser_sha256': sha(parser.read_bytes()),
        'only_one_explicit_verified_directory_added': True, 'function_bodies_and_old_directories_preserved': True,
        'old_V757_config_unchanged_explicit_replay_copy_used_in_V758': True,
        'exact_V757_stage_output_revalidated_by_registered_builder': True})
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 120 and ledger['records_revised_and_integrated'] == 84
    assert ledger['retained_wordings_editorially_completed'] == 36
    save(ROOT / 'editorial_ledger_at_V757.json', ledger)
    family = 'Market-extra-stock-advice-and-contract-refusal754-761'
    ledger['completed_editorial_families'].append({'id': family, 'native_message_IDs': list(IDS),
        'records': [{'message_id': n, 'decision': 'revised-and-integrated', 'manuscript': str(MANUSCRIPT),
                     'complete_source_context_and_native_font_verified': True, 'actual_display_verified': n in (754, 761)} for n in IDS],
        'integrated_ROM_sha256': digest, 'proof': str(ROOT / 'proof.json'),
        'gameplay_scope': 'Actual754 adviser and761 with both full native building arguments; other six advice variants have source/native font evidence.'})
    ledger.update({'records_editorially_completed': 128, 'records_revised_and_integrated': 92,
        'retained_wordings_editorially_completed': 36, 'records_with_source_and_prose_pass': 131, 'records_with_source_prose_drafts': 131,
        'latest_checkpoint': 'V758 completes8 Market advice/contract replies. Native scope/fonts/copies and actual adviser,Palace,Governor office,Investment/New Game controls pass. Three750-752 drafts remain context-unmapped; wider prose/routes/graphics remain open.'})
    ledger['active_source_prose_drafts'] = {'native_message_IDs': [750, 751, 752], 'manuscripts': [str(ROOT / 'unmapped_750_752_prose_DRAFT.json')],
        'status': 'source-prose-only-context-activation-unmapped-not-integrated',
        'note': 'These three source/prose drafts are not completed. Literal searches do not establish that they are unused; map actual callers/packed scripts and presentation context before integration.'}
    ledger['coverage_units'][0]['completed_families'].append(family)
    ledger['coverage_units'][0]['next'] = 'Map750-752 reset/cancellation activation; continue784 onward and the wider shared dialogue inventory, then Lil and all routes. Do not interpret absent simple literal references as unused text.'
    for finding in ledger['findings']:
        if finding.get('id') == 'COMMON-761-palace-contract-word-split':
            finding.update({'status': 'resolved-source-native-actual-both-buildings-integrated-V758',
                'detail': 'Complete return instruction, natural at the building and full Governor\'s Office argument. Exact761 post-printf balancing keeps complete first/final letters and whole words. Six adviser/refusal holds,normal returns and all123 other whole-frame controls pass.'})
    ledger['findings'].append({'id': 'COMMON-754-760-extra-stock-advice-registers', 'native_message_ids': list(range(754, 761)),
        'status': 'source-native-family-gameplay-sample-integrated-V758',
        'detail': 'Preserve seven voice registers, uncertainty,current occasion,larger quantities of certain goods and double payment. Actual Gerhard role3 advice uses source voice1 missing-entry fallback to754. No double-stock purchase effect or earned prerequisite claim.'})
    ledger['current_integrated_candidate'] = {'path': str(ROM), 'sha256': digest, 'profile': manifest['profile'],
        'MESFILE_sha256': config['target_common_sha256'], 'ARM9_sha256': config['target_arm9_sha256'], 'patch_sha256': patch['patch_sha256'],
        'status': 'experimental', 'manifest': str(ROM.with_suffix('.manifest.json')), 'initial_source_pins_retained_as_V743_reference_not_overwritten': True}
    save(LEDGER, ledger)
    save('out/editorial_review_latest.json', {**ledger['current_integrated_candidate'], 'details': str(DOC), 'full_goal_complete': False})
    controls = sum(map(len, game['all_other_whole_frame_controls'].values()))
    DOC.write_text(f'''# V758: Market advice and contract refusal

Eight entries754-761 complete editorial review. Total128 reviewed:92 revised,36 retained. Source/prose work covers131 including three750-752 drafts whose activation/context remains unmapped. Those three are not integrated or completed. The full editorial goal remains active; wider shared prose, Lil/all routes, remaining player-facing prose and separate graphics audit remain open.

## Natural, faithful English

Seven advice registers preserve uncertainty, the current occasion, larger quantities of only certain goods, and double payment. Polite, casual, rough, measured and upbeat source voices are conveyed without assigning unverified character identities or adding old-age/family labels. Actual Gerhard uses native voice1; its missing table entry falls back to754 through the unchanged original selector. The merchant refusal restores the omitted instruction to return and uses a full location name:

> Sorry. Please sign a contract at the %s, then come back.

The argument is a building: Palace or Governor's Office. Source総督府 is not a city. The old Govt abbreviation and fir/st split are removed. The request's natural please preserves its friendly request form. No authored alignment or line breaks are inserted. Generated wrapping checks complete leading/trailing letters, whole words, bounds, weak line endings, orphaned final rows and consistent visible left margins. The earlier676/677 repair and all unselected message bytes are preserved.

## Runtime and owned storage

Only direct portrait761 is newly routed to the existing bounded post-printf balancing routine. All18340 parent/ID selections differ only for761. The private entry now tests exactly761/767/768/769/770, with all3668 ID membership cases and120 full non-direct outputs/ABI controls passing. Its full original-parent guard and Thumb body are unchanged. The entry's literal moves into four proven unused bytes at the end of the retired Lil Gallery description. Current code branch/pointer ownership is fully enumerated; every other section byte restores exactly outside the declared patches.

Five complete source label slots at2157064..2157090 are merged. The full Governor's Office string and identical Investment string occupy32 bytes; a12-byte exact761 dispatch occupies the remainder. All five original pointer owners are checked. Palace,Port andTarget owners point to existing immutable identical strings; Investment's owner follows its moved complete string. All four native printf calls preserve every byte/NUL and guarded buffers, including unaligned immutable suffixes. Their meanings, fonts, geometry and pixels are unchanged. No RTTI,bitmap,palette,border,section,123040-byte staged payload,cache,startup or allocator grows.

The eight faithful paragraphs need more space than the former short/padded drafts. Exact complete native selections344-1712 are repacked across existing blocks5-18; all1369 starts and14 directory rows are remapped within4096-byte bounds. Every discarded gap is proven NUL/ASCII-space. All3660 unselected text byte strings and27 other blocks remain exact, including packed payload blocks19 onward. All7336 guarded warm/cold native copies pass; the harness supplies the file IO boundary, not physical hardware IO.

The strict parser accepts one additional exact directory digest, with old directories and function bodies unchanged. The old V757 config is preserved. An explicit replay config pins the added allowlist entry and rebuilds byte-identical V757 stage output before this new layer. Historical V757 source reconstruction can restore the archived pre-V758 parser; its ROM and patch are unchanged.470 batches,114 accepted layers and675 graphics are retained.

## Native and actual verification

-9 complete native font planes cover all seven advice variants and both full refusal nouns; all previews were visually inspected.
-31013 inherited Market stock layouts remain byte-identical to V757 after the private guard change.
-Three paired cold boots display ordinary Palace refusal, a declared one-bit governor-facility fixture, and a declared Gerhard role/experience/share fixture selecting actual adviser754. Six4600/4800 holds match every glyph and blank-paper cell, with every outside pixel exact. The full resident cache block and original copy buffer are bound to the displayed entry.
-{controls} other complete two-screen pairs, including normal Trade/menu/Town returns and an ordinary Investment amount dialog, are pixel-exact. All sampled whole company/fleet/ship models and town/company states match. No RNG/HUD exception is needed in these pairs.
-Fixture-free4000-frame New Game matches all seven V757 frames through title,selection and story. Original and disposable donor saves retain their exact hashes.

The advice fixture changes8 bytes across a room type,Gerhard assignment/XP and an unused company/share pair; original role/ability/stock predicates remain active. It verifies display under declared prerequisites, not earned role/share/experience or the effect of an actual double-price purchase. The governor fixture changes only facility bit6. Palace/Investment/New Game use no RAM fixture. Other six advice variants have source/native-font evidence, not all actual activations. These are targeted automated emulator tests, not a hardware test or complete route playthrough.

## Registered candidate

-ROM: `{ROM}`; experimental profile `{manifest['profile']}`.
-SHA256: `{digest}`.
-Patch SHA256: `{patch['patch_sha256']}`. Exact reconstruction from clean SHA256 `{pins['work/clean.nds']}` passes.
-Canonical base remains `out/raphael_natural_v2_accepted_base.nds`, SHA256 `{pins['out/raphael_natural_v2_accepted_base.nds']}`; no promotion.
-Changed internal files relative V757: `/COMMON/MESFILE.DK4` and `/__arm9__.bin` (owned text/data,three scoped ARM code spans and native offset/directory metadata).
-Verifiers: `verify_market_contract_native_v758.py`, `verify_contract_native_copies_v758.py`, `verify_market_contract_release_v758.py`, `verify_market_contract_gameplay_v758.py`.
-User cold-boot acceptance remains pending: title/New Game/intro,town UI,the Palace/Governor refusal and adviser/Trade/Investment screens. No additional approval is required to generate previews or continue the goal.

ROM,manifest,patch,evidence and labeled final screenshots are on E. Next: map750-752 callers/packed-script context and review784 onward,wider shared prose,Lil/all routes. No absent literal-reference result is treated as proof that a line is unused. Original18 graphics entries,Online-body exclusion,preserved brown marks and later older-record follow-up remain unchanged.
''', encoding='utf-8')
    reports = [ROOT / n for n in ('native_context.json', 'source_and_neighbors.json', 'native_review_RESEARCH.json',
        'native_repack_and_ownership_RESEARCH.json', 'native_integration.json', 'parser_compatibility.json',
        'registered_verification.json', 'gameplay_verification.json', 'patch_proof.json')]
    save(ROOT / 'visual_review.json', {'all9_native_planes_and_three_actual_new_dialogue_views_opened': True,
        'three_old_dialogue_reference_views_and_actual_new_Investment_amount_view_opened': True,
        'complete_readable_first_last_letters_aligned_lines_and_unchanged_other_UI_observed': True, 'full_goal_complete': False})
    reports.append(ROOT / 'visual_review.json')
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
        'revised_IDs': list(IDS), 'unmapped_drafts_not_completed': [750, 751, 752],
        'reports': {str(p): sha(p.read_bytes()) for p in reports}, 'protected_files': pins,
        'editorial_ledger_sha256': sha(LEDGER.read_bytes()), 'checkpoint_sha256': sha(DOC.read_bytes()), 'full_goal_complete': False})
    summary = '\n\n## V758: complete Market advice and contract locations\n\nEight entries revised/integrated:128 reviewed overall (92 revised/36 retained). Source restores certain-goods/quantity/payment/voice distinctions and the refusal return instruction. Full Governor\'s Office replaces Govt; exact761 balancing fixes whole-word wrapping. Nine native font planes,31013 inherited layouts,3668 private-ID cases,120 non-direct controls and7336 native copies pass. Six actual adviser/refusal holds,123 whole-screen controls,complete sampled models,ordinary Investment caption and7 New Game frames pass. All470/114 layers and675 graphics preserved; exact clean patch verified.750-752 remain context-unmapped drafts (131 source/prose passes including these3);784 onward,wider shared/routes and graphics audit remain open. See [V758 checkpoint](market_contract_v758_checkpoint.md).\n'
    for name in ('translation_progress.md', 'todo.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert '## V758: complete Market advice and contract locations' not in text
        path.write_text(text.rstrip() + summary, encoding='utf-8')
    shots = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V758 Market advice and contracts')
    for mode, frames in (('palace', (4800, 5600)), ('governor', (4800, 5600)), ('advice', (4800, 5200, 6000)), ('investment', (5400,))):
        capture = read(CAP / f'market_contract_v758_{mode}_758/capture_report.json')
        for frame in frames:
            row = next(r for r in capture['frames_captured'] if r['frame'] == frame)
            copy(Path(row['path']), shots / f'{mode}_{frame:06d}.png')
    save(shots / 'provenance.json', {'candidate_sha256': digest, 'ordinary_Palace_and_Investment_controls': True,
        'governor_one_bit_and_advice8_byte_fixtures_disclosed_no_earned_progress_claim': True,
        'proof': str(ROOT / 'gameplay_verification.json'), 'files': {p.name: sha(p.read_bytes()) for p in shots.glob('*.png')}})
    files = [ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'), DOC, LEDGER, CONFIG, MANUSCRIPT,
        Path('translations/market_stock_replay_for_v758.json'), Path('translations/release_stack.json'),
        Path('dk4tool/patch/market_contract_editorial.py'), ROOT / 'proof.json', ROOT / 'editorial_ledger_at_V757.json',
        ROOT / 'common_message_table_before_v758.py', ROOT / 'common_message_table_for_v758.py',
        ROOT / 'unmapped_750_752_prose_DRAFT.json', ROOT / 'all9_native_previews_2x.png', *reports,
        *ROOT.glob('native_copies_block_*.json'), *Path('scripts').glob('*contract*v758.py')]
    for path in files:
        copy(path, ARCHIVE / path.name)
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': digest,
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name != 'provenance.json'}, 'full_goal_complete': False})
    for p, h in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / p).read_bytes()) == h
    print('V758 recorded/archived:128 reviewed,92 revised,36 retained;3 drafts and full goal remain open.', flush=True)


if __name__ == '__main__':
    main()
