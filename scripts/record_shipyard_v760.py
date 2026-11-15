"""Record the integrated Shipyard editorial family and archive scoped evidence."""

import ast
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_shipyard_release_v760 import CONFIG, MANUSCRIPT, ROOT
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.record_memory_streams_v682 import copy
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_shipyard_gameplay_v760 import CAP, FULL_SAVE_SHA, ROM, SAVE_SHA
from scripts.verify_village_wrap_v608 import read, save

LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/shipyard_editorial_v760_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V760 Shipyard dialogue')
SHOTS = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V760 Shipyard dialogue')


def main():
    assert not ARCHIVE.exists()
    config, manuscript, manifest = read(CONFIG), read(MANUSCRIPT), read(ROM.with_suffix('.manifest.json'))
    native, registered, game, patch = [read(ROOT / n) for n in ('native_owned/verification.json', 'registered_verification.json', 'gameplay_verification.json', 'patch_proof.json')]
    digest = sha(ROM.read_bytes())
    assert digest == manifest['candidate_sha256'] == registered['candidate_sha256'] == game['candidate_sha256'] == patch['candidate_sha256']
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['profile'] == 'all-routes-unified-v760' and len(manifest['batches']) == 470 and all(manifest['checks'].values())
    assert patch['byte_exact_reconstruction'] and all(registered['rejections'].values())
    assert len(native['all1124_complete_native_layouts_equal_verified_prototype']) == 1124
    assert len(native['all68_complete_font_planes_equal_independent_rasters_and_prior_reviewed_previews']) == 68
    assert not native['constant_bank_writes'] and len(game['actual_complete_dialogue_holds']) == 31
    assert game['producer_sha256'] == sha(Path('scripts/verify_shipyard_gameplay_v760.py').read_bytes())
    for p, h in config['dependencies'].items():
        assert sha(Path(p).read_bytes()) == h, p
    assert sha(MANUSCRIPT.read_bytes()) == config['manuscript_sha256']
    assert [r['message_id'] for r in manuscript['records']] == list(range(784, 805))
    pins = {'out/all_routes_combined_v758_candidate.nds': '40acbf6bd11d40a99186d078c4671470e4ef1129515a854f67e6c4c09115c302',
        'work/clean.nds': 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',
        'out/raphael_natural_v2_accepted_base.nds': '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        'E:/Rota Nova translations/Saves/hodram-istanbul-golden-cutlass-blue-oak-v474.dsv': SAVE_SHA,
        'E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv': SAVE_SHA,
        'E:/Rota Nova translations/Generated/work/emulation_v193/full_fleet_staffing_v652_actual/saves/all_routes_combined_v651_candidate.dsv': FULL_SAVE_SHA}
    for p, h in pins.items():
        assert sha(Path(p).read_bytes()) == h, p
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    transactions = []
    for item in game['sampled_native_models_states_and_loaded_main_RAM_patches']:
        mode = item['mode']
        states = item['paired_native_models_and_town_company_states_exact']
        for row in states:
            frame = row['frame']
            if mode == 'repair_applied':
                expected = 8371 if frame < 5800 else 8343
            elif mode == 'repair_pair':
                expected = 25975 if frame < 5000 else 25915
            elif mode.startswith('copy_'):
                expected = 8371 if frame == 3200 else 100000
            elif mode == 'repair_pair_no_funds':
                expected = 25975 if frame == 3200 else 0
            else:
                expected = 25975
            assert row['state']['cash'] == expected, (mode, frame)
        if mode in ('repair_applied', 'repair_pair', 'repair_menu_quote'):
            report = read(CAP / f'shipyard_v760_{mode}_760/capture_report.json')
            late = snapshot(report, states[-1]['frame'])
            receipt = report['synthetic_shipyard_repair_fixtures'][0]
            ships = receipt.get('ships', [{'ship': receipt.get('native_ship'), 'maximum_HP': receipt.get('maximum_durability')}])
            u = machine(arm); u.mem_write(BASE, late)
            current = []
            for ship in ships:
                ptr = ship['ship']; vt = struct.unpack('<I', u.mem_read(ptr, 4))[0]
                getter = struct.unpack('<I', u.mem_read(vt + 0x24, 4))[0]
                call(u, getter - BASE, (ptr,)); hp = u.reg_read(UC_ARM_REG_R0)
                expected = ship['maximum_HP'] - (3 if mode == 'repair_menu_quote' else 0)
                assert hp == expected
                current.append({'ship': ptr, 'HP': hp, 'maximum_HP': ship['maximum_HP']})
            transactions.append({'mode': mode, 'final_native_HP': current, 'final_cash': states[-1]['state']['cash']})
    save(ROOT / 'transaction_states.json', {'all_sampled_expected_cash_values_exact': True,
        'helper_repair_original28_coin_charge_full_pair_original60_coin_charge': True,
        'declined_repair_preserves_damage_and_funds': True, 'declined_sale_and_copy_preserve_funds': True,
        'final_repair_states': transactions, 'no_special_order_purchase_or_earned_prerequisite_claim': True})
    def directories(path):
        tree = ast.parse(path.read_text(encoding='utf-8'))
        return next(ast.literal_eval(n.value.args[0]) for n in tree.body if isinstance(n, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == 'RELOCATED_DIRECTORY_HASHES' for t in n.targets))
    previous_parser = ROOT / 'common_message_table_before_v760.py'
    parser = Path('dk4tool/script/common_message_table.py')
    assert directories(parser) == directories(previous_parser) | {'7e2fc3325ac41442354ecb8547c6cf85a74bd14d05bd19ff39ec93d18c78cfd5'}
    copy(parser, ROOT / 'common_message_table_for_v760.py')
    ledger = read(LEDGER)
    assert (ledger['records_editorially_completed'], ledger['records_revised_and_integrated'], ledger['retained_wordings_editorially_completed']) == (128, 92, 36)
    save(ROOT / 'editorial_ledger_at_V759.json', ledger)
    save(ROOT / 'editorial_latest_at_V758.json', read('out/editorial_review_latest.json'))
    family = 'Shipyard-copy-sale-repair-and-volunteer-replies784-804'
    actual = {r['message_id'] for r in game['actual_complete_dialogue_holds']}
    retained = {787, 790, 801}
    ledger['completed_editorial_families'].append({'id': family, 'native_message_IDs': list(range(784, 805)),
        'records': [{'message_id': n, 'decision': 'retained-wording-reviewed' if n in retained else 'revised-and-integrated',
            'manuscript': str(MANUSCRIPT), 'complete_source_context_and_native_font_verified': True,
            'actual_display_verified': n in actual} for n in range(784, 805)], 'integrated_ROM_sha256': digest,
        'proof': str(ROOT / 'proof.json'), 'gameplay_scope': '31 full holds across11 actual message IDs; remaining10 entries have source/native/font coverage with family gameplay samples. Eight paired Yard cold boots and seven matched New Game frames; no all-branch or hardware claim.'})
    ledger.update({'records_editorially_completed': 149, 'records_revised_and_integrated': 110,
        'retained_wordings_editorially_completed': 39, 'records_with_source_and_prose_pass': 152, 'records_with_source_prose_drafts': 152,
        'latest_checkpoint': 'V760 integrates21 Shipyard entries:149 reviewed overall (110 revised/39 retained). Owned storage, native copies/full fonts/exact patch and31 actual full holds across11 IDs pass. Three750-752 context drafts,805 onward,wider shared/Lil/all routes/other prose and graphics audit remain open.'})
    ledger['active_source_prose_drafts'] = {'native_message_IDs': [750, 751, 752],
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],
        'status': 'source-prose-only-context-activation-unmapped-not-integrated',
        'note': 'Map actual callers/packed-script presentation before integration. No absent-literal result proves unused text.'}
    ledger['coverage_units'][0]['completed_families'].append(family)
    ledger['coverage_units'][0]['next'] = 'Map750-752 actual callers; review805 onward and observed267/1245 neighboring Yard prose, wider shared dialogue, then Lil/all routes and other player-facing prose.'
    ledger['formatting_watchlist']['latest_reference_proof'] = str(ROOT / 'user_photo_formatting_preserved.json')
    ledger['formatting_watchlist']['reference_case'] += ' V760 exact repaired676/677 bytes also preserved; no new V760 actual activation of those shop pitches claimed.'
    for finding in ledger['findings']:
        if finding.get('id') in ('COMMON-788-789-cross-selection-sale-prompt', 'COMMON-796-798-repair-volunteer-discount-placeholders', 'COMMON-post-printf-macro-like-ship-name-data'):
            finding['status'] = 'source-native-family-gameplay-integrated-V760'
            finding['resolution_proof'] = str(ROOT / 'proof.json')
    ledger['findings'].append({'id': 'COMMON-267-1245-observed-neighboring-Yard-prose', 'native_message_ids': [267, 1245],
        'status': 'observed-not-editorially-completed', 'detail': 'Ordinary Sell with only one ship shows No more ships can be scrapped!; a Special order with insufficient funds shows Need ... coins. You are short. Review exact clean source/callers before changing either; these are outside784-804.'})
    ledger['current_integrated_candidate'] = {'path': str(ROM), 'sha256': digest, 'profile': manifest['profile'],
        'MESFILE_sha256': config['target_common_sha256'], 'ARM9_sha256': config['target_arm9_sha256'],
        'patch_sha256': patch['patch_sha256'], 'status': 'experimental', 'manifest': str(ROM.with_suffix('.manifest.json')),
        'initial_source_pins_retained_as_V743_reference_not_overwritten': True}
    save(LEDGER, ledger)
    save('out/editorial_review_latest.json', {**ledger['current_integrated_candidate'], 'details': str(DOC), 'full_goal_complete': False})
    DOC.write_text(f'''# V760: Shipyard dialogue and native runtime values

Twenty-one entries784-804 complete editorial review:18 revised and3 retained (787,790,801). Total149 reviewed:110 revised,39 retained. Source/prose coverage152 includes three750-752 drafts whose activation/context remains unmapped. The full editorial goal stays active;805 onward,wider shared prose,Lil/all routes,other player-facing prose and the separate graphics audit remain unfinished.

## Source and natural English

The independent ship-selection question and price confirmation no longer form the old broken cross-selection sentence. Seven repair volunteers preserve their voices; unrelated trade placeholders in796-798 are replaced with the actual repair offer and helper discount. Source IC in792 is a first-person pronoun, localized as I; it is not a missing name.803 means a new ship matching the named design. The duration is preparation time, not a invented voyage. Six price arguments now contain native full-width digits plus gold coin/coins; the duration argument supplies day/days. Percent and mast/durability retain their separate native numeric contracts.

All prose is one logical paragraph. The formatter handles indentation and line breaks after substitutions. Complete letters,whole words,consistent left margins,four-row bounds,short final rows and weak line endings are checked. Native whole-word wrapping may break between words of a quantity phrase; no word or character is dropped. Earlier676/677 cooking/fashion pitch bytes remain exact in this candidate; their actual V747 screenshot and V758 native formatting proof remain the reference, not a new V760 activation claim.

## Runtime ownership and preservation

The original post-printf parser expands macro-like FA/FI/FO/FU/IC inside supplied ship-name data. A family-scoped literal path preserves those bytes. Exact direct/YesNo IDs and the original queued volunteer table gate this behavior; source macros elsewhere remain active. All36680 scope cases and180 inherited full outputs/ABI controls pass.

660 executable/data bytes occupy21 retired source constant-string allocations in four immutable banks:02131F48..02132044,02147AE4..02147B80,02147B98..02147C70 and02147E54..02147F00 (exclusive ends). All54 replacement village strings and3 Deck strings have verified active owners. Every current unaligned pointer/ARM branch/ADR/crossing string is checked. The live Race string starting02138162,adjacent pointer tables/RTTI and mutable02171E48..02172464 are preserved. Zero native writes enter the selected banks. No section,123040-byte staged payload,cache,startup or allocator grows.

The full1549 selections164-1712 are repacked in the existing17 blocks2-18 and fixed4096-byte native cache. All3647 unselected complete strings and24 other blocks remain exact,including packed payload19 onward. Only padding proved NUL/ASCII-space is discarded. The strict parser adds one exact directory digest; frozen V757/V758 configs are preserved and explicit replay copies prove identical earlier stage output.

## Verification

-1124 complete supplied-value layouts and68 independently decoded whole ASCII/KANJI font planes match the reviewed V759 prototype; six preview sheets were reviewed. Native numbers are full-width2-byte/12-pixel digits.105 typed quantity contracts,77 whole4MiB buffer comparisons,24 original copy-argument fragments and180 inherited outputs pass. The23-byte names and INT_MAX amounts in stress tests are supplied contracts, not claimed legal edit limits or earned values.
-7336 warm/cold native COMMON copies and nine malformed-input rejection controls pass. The file-IO boundary is supplied by the harness; this is not hardware IO verification.
-Eight paired targeted cold boots produce31 full dialogue holds across IDs{','.join(map(str, sorted(actual)))}. Every foreground glyph equals an independent complete native font plane; resident COMMON blocks,printf/wrapped buffers,paper cells outside old/new glyph shadows and all pixels outside the body match.105 other two-screen pairs are entirely pixel-exact. Main-RAM runtime patch spans are verified loaded; the4MiB exports do not directly export ITCM.
-All sampled active company/fleet/member-ship models and town/company states match the immediate parent. Original repairs charge28 coins with the qualified helper and60 for the two-ship automatic offer,restoring native HP. Declining the ordinary repair preserves damage/funds; declined sale and special orders preserve money. The return-to-Yard/Town frames are checked. Stale post-dismissal message buffers are not counted as visible text.
-Fixture-free New Game matches all seven V758 frame pairs through title,captain selection and intro. Original/disposable Istanbul and Copenhagen donors retain their hashes.

The fixtures use cold boots with battery saves,never savestates. Repair-helper prerequisites change4 bytes,using existing Gerhard level39 and the original HP setter; no XP is granted. Two-ship repair changes2 durability bytes,or4 total including the zero-funds word. Special-order fixtures rename the existing eight-letter name to six-letter FALCON/ICARUS and grant100000 through the original money method. Zero/one-day variants derive room/sail/end properties from the original catalogue and execute the unchanged preparation algorithm; no computed result/branch is overridden. They verify declared display prerequisites,not earned wealth/damage/design,normal acquisition,a purchase,all seven actual volunteer activations,hardware or a full playthrough. Remaining10 message IDs have source/native/font coverage and family gameplay samples.

## Registered experimental ROM

-Candidate: `{ROM}`; profile `{manifest['profile']}`.
-SHA256: `{digest}`.
-COMMON: `{config['target_common_sha256']}`; ARM9: `{config['target_arm9_sha256']}`.
-Patch SHA256: `{patch['patch_sha256']}`; byte-exact reconstruction from clean SHA256 `{pins['work/clean.nds']}`.
-Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA256 `{pins['out/raphael_natural_v2_accepted_base.nds']}`. It is unchanged and is not promoted.
-All470 batches,114 accepted layers and675 graphics remain. Relative V758 only `/COMMON/MESFILE.DK4` and `/__arm9__.bin` change. ARM7,overlays and all other files are exact.
-Verifiers: `verify_shipyard_storage_v760.py`, `verify_shipyard_owned_runtime_v760.py`, `verify_shipyard_native_copies_v760.py`, `verify_shipyard_release_v760.py`, `verify_shipyard_gameplay_v760.py`. Historical pending fields in frozen research/build inputs are superseded by the final proof.
-User acceptance remains pending: cold-boot title/New Game/intro,town UI,Shipyard sell/copy/repair screens and return states. Continue the goal without waiting for extra preview permission.

ROM,manifest,exact patch,evidence and clearly labeled test screenshots are saved on E. The original18 plaque entries,Online-body exclusion,preserved brown marks and later older-record follow-up are retained.267/1245 observed neighboring Yard prose still needs source/editorial review.
''', encoding='utf-8')
    save(ROOT / 'visual_review.json', {'actual_sell_helper_discount_repair_prices_low_funds_copy_zero_one_five_day_and_return_views_opened': True,
        'earlier_six_native_research_sheets_reviewed_and_all68_owned_planes_equal': True,
        'complete_readable_letters_aligned_rows_no_internal_padding_or_stray_fragments_observed': True,
        'ordinary_word_wrap_can_separate_quantity_words': True, 'all_route_and_hardware_verification_not_claimed': True})
    reports = [ROOT / p for p in ('owned_source_storage.json', 'runtime_plan.json', 'common_repack_plan.json',
        'common_preservation.json', 'explicit_parser_replay.json', 'native_integration.json', 'native_owned/verification.json',
        'registered_verification.json', 'gameplay_verification.json', 'patch_proof.json', 'transaction_states.json',
        'visual_review.json', 'user_photo_formatting_preserved.json')]
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
        'revised_IDs': [n for n in range(784, 805) if n not in retained], 'retained_IDs': sorted(retained),
        'actual_display_IDs': sorted(actual), 'unmapped_drafts_not_completed': [750, 751, 752],
        'reports': {str(p): sha(p.read_bytes()) for p in reports}, 'protected_files': pins,
        'editorial_ledger_sha256': sha(LEDGER.read_bytes()), 'checkpoint_sha256': sha(DOC.read_bytes()), 'full_goal_complete': False})
    summary = '\n\n## V760: integrated Shipyard prose and literal runtime values\n\n21 entries784-804 complete review:149 total (110 revised/39 retained). Independent sale prompts,repair voices/discount and typed price/duration grammar are restored; literal ship names survive native macro parsing. Owned immutable banks,1124 layouts,68 full font planes,7336 copies and exact clean patch pass.31 actual holds across11 IDs,105 entire-screen controls,all sampled active models/states and7 New Game pairs pass. Only COMMON/ARM9 change;470 batches,114 accepted layers and675 graphics remain. Three750-752 drafts,805 onward,observed267/1245,wider shared/Lil/all routes/other prose and separate graphics audit remain open. Experimental; canonical and donors unchanged. See [V760 checkpoint](shipyard_editorial_v760_checkpoint.md).\n'
    for name in ('translation_progress.md', 'todo.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name; text = path.read_text(encoding='utf-8')
        assert '## V760: integrated Shipyard prose and literal runtime values' not in text
        path.write_text(text.rstrip() + summary, encoding='utf-8')
    selected_shots = [('sell_quote', 5600), ('repair_applied', 3800), ('repair_applied', 4800), ('repair_applied', 5200),
        ('repair_pair_no_funds', 5200), ('repair_menu_quote', 5400), ('copy_funded_FALCON', 6400),
        ('copy_preparation_0', 6400), ('copy_preparation_1', 6400), ('copy_preparation_0', 7800)]
    for mode, frame in selected_shots:
        report = read(CAP / f'shipyard_v760_{mode}_760/capture_report.json')
        row = next(r for r in report['frames_captured'] if r['frame'] == frame)
        copy(Path(row['path']), SHOTS / f'{mode}_{frame:06d}.png')
    save(SHOTS / 'provenance.json', {'candidate_sha256': digest, 'ordinary_sale_no_RAM_fixture': True,
        'repair_and_special_order_synthetic_prerequisites_disclosed': True, 'earned_or_guide_promotion_not_claimed': True,
        'proof': str(ROOT / 'gameplay_verification.json'), 'files': {p.name: sha(p.read_bytes()) for p in SHOTS.glob('*.png')}})
    for path in ROOT.rglob('*'):
        if path.is_file():
            copy(path, ARCHIVE / 'evidence' / path.relative_to(ROOT))
    files = [ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'), DOC, LEDGER, CONFIG, MANUSCRIPT,
        Path('translations/release_stack.json'), Path('translations/market_stock_replay_for_v760.json'),
        Path('translations/market_contract_replay_for_v760.json'), Path('out/editorial_review_latest.json'),
        parser, Path('scripts/build_integrated_release.py'), *Path('scripts').glob('*shipyard*v760.py'),
        Path('dk4tool/patch/shipyard_editorial.py'), Path('dk4tool/patch/shipyard_common.py'),
        Path('dk4tool/patch/shipyard_editorial_release.py')]
    for path in files:
        copy(path, ARCHIVE / 'repository' / path.as_posix())
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': digest,
        'files': {p.relative_to(ARCHIVE).as_posix(): sha(p.read_bytes()) for p in ARCHIVE.rglob('*') if p.is_file() and p != ARCHIVE / 'provenance.json'},
        'full_goal_complete': False})
    for p, h in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / p).read_bytes()) == h
    print('V760 recorded and hash-checked on E:149 completed,110 revised,39 retained;3 drafts and full goal remain open.', flush=True)


if __name__ == '__main__':
    main()
