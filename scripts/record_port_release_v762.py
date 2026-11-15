"""Record18 integrated service reviews with explicit family gameplay sampling."""

import ast
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_port_release_v762 import CONFIG, MANUSCRIPT, ROOT
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.record_memory_streams_v682 import copy
from scripts.verify_market_gameplay_v753 import SAVE_SHA, snapshot
from scripts.verify_shipyard_gameplay_v760 import FULL_SAVE_SHA
from scripts.verify_port_gameplay_v762 import ROM, CAP
from scripts.verify_village_wrap_v608 import read, save

LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/port_services_v762_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V762 Port and companion services')
SHOTS = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V762 Port and companion services')


def main():
    assert not ARCHIVE.exists()
    config, manuscript = read(CONFIG), read(MANUSCRIPT)
    manifest, registered, patch, game = [read(p) for p in (ROM.with_suffix('.manifest.json'), ROOT / 'registered_verification.json', ROOT / 'patch_proof.json', ROOT / 'gameplay_verification.json')]
    digest = sha(ROM.read_bytes())
    assert digest == manifest['candidate_sha256'] == registered['candidate_sha256'] == patch['candidate_sha256'] == game['candidate_sha256']
    assert all(manifest['checks'].values()) and all(registered['rejections'].values()) and patch['byte_exact_reconstruction']
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert game['producer_sha256'] == sha(Path('scripts/verify_port_gameplay_v762.py').read_bytes())
    for p, h in config['dependencies'].items(): assert sha(Path(p).read_bytes()) == h, p
    assert sha(MANUSCRIPT.read_bytes()) == config['manuscript_sha256']
    pins = {'out/all_routes_combined_v760_candidate.nds': '4558b145919f4eaa3bd0369cef587dd89f91f880bbc3f2fe5f782ee554793bc0',
        'work/clean.nds': 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',
        'out/raphael_natural_v2_accepted_base.nds': '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        'E:/Rota Nova translations/Saves/hodram-istanbul-golden-cutlass-blue-oak-v474.dsv': SAVE_SHA,
        'E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv': SAVE_SHA,
        'E:/Rota Nova translations/Generated/work/emulation_v193/full_fleet_staffing_v652_actual/saves/all_routes_combined_v651_candidate.dsv': FULL_SAVE_SHA}
    for p, h in pins.items(): assert sha(Path(p).read_bytes()) == h, p
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    water = read(CAP / 'port_services_v762_water_only_762/capture_report.json')
    cpu = machine(arm); cpu.mem_write(BASE, snapshot(water, 7200))
    def get(fn, args=()):
        call(cpu, fn, args); return cpu.reg_read(UC_ARM_REG_R0)
    fleet = get(0xCB1A8) + 4 + get(0x2E58C) * 0x84
    get(0x34EB0, (fleet, 0x02450000)); totals = list(struct.unpack('<2I', cpu.mem_read(0x02450000, 8)))
    assert totals == [350, 350]
    save(ROOT / 'supply_state_verification.json', {'fixture': [0, 700], 'original_native_final_water_food': totals,
        'water_refill_and_excess_food_disposal_complete': True, 'cash_unchanged': 25975,
        'no_earned_supply_fixture_claim': True})
    ledger = read(LEDGER)
    assert (ledger['records_editorially_completed'], ledger['records_revised_and_integrated'], ledger['retained_wordings_editorially_completed']) == (149, 110, 39)
    assert ledger['records_with_source_and_prose_pass'] == 170 and len(ledger['active_source_prose_drafts']['native_message_IDs']) == 21
    save(ROOT / 'editorial_ledger_before_v762.json', ledger)
    save(ROOT / 'editorial_latest_before_v762.json', read('out/editorial_review_latest.json'))
    ids = [r['message_id'] for r in manuscript['records']]
    actual = sorted({r['message_id'] for r in game['eight_complete_actual_dialogue_holds']})
    retained = [807, 809, 815, 819]
    family = 'Port-companion-Tavern-and-shared-price-replies267-805-819-1245-1246'
    ledger['completed_editorial_families'].append({'id': family, 'native_message_IDs': ids,
        'records': [{'message_id': n, 'decision': 'retained-wording-reviewed' if n in retained else 'revised-and-integrated',
            'manuscript': str(MANUSCRIPT), 'complete_source_context_and_native_font_verified': True,
            'actual_display_verified': n in actual} for n in ids], 'integrated_ROM_sha256': digest,
        'proof': str(ROOT / 'proof.json'),
        'gameplay_scope': 'Eight complete actual holds across five IDs267/806/813/819/1245,79 whole-frame controls and seven New Game pairs. Other13 IDs have source/context/native-font coverage with family sampling. No actual companion veto,1246 payment or818 activation claimed.'})
    ledger.update({'records_editorially_completed': 167, 'records_revised_and_integrated': 124, 'retained_wordings_editorially_completed': 43,
        'latest_checkpoint': 'V762 integrates18 service entries:167 reviewed overall (124 revised/43 retained).416 original companion selector cases,40 complete fonts,36680 scope cases,1124 unchanged Yard outputs,7336 copies and exact patch pass. Eight actual holds across five IDs,79 controls,paired native models/states and seven New Game frames pass.750-752 context drafts,820 onward,wider shared/Lil/all routes/other prose and graphics remain open.'})
    ledger['active_source_prose_drafts'] = {'native_message_IDs': [750, 751, 752],
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],
        'status': 'source-prose-only-context-activation-unmapped-not-integrated',
        'note': 'Map actual caller/packed-script context before integration; no absent literal-reference result proves unused text.'}
    ledger['coverage_units'][0]['completed_families'].append(family)
    ledger['coverage_units'][0]['next'] = 'Review820 onward,wider shared prose and remaining750-752 actual context; then Lil/all routes and other player-facing text. Retain the separate graphics audit and older-record follow-up.'
    for finding in ledger['findings']:
        if finding.get('id') in ('COMMON-805-reversed-admiral-captain-warning', 'COMMON-810-811-818-unrelated-trade-placeholders',
            'COMMON-808-substituted-admiral-name-integrity', 'COMMON-267-1245-observed-neighboring-Yard-prose'):
            finding['status'] = 'source-native-reviewed-integrated-with-family-gameplay-samples-V762'
            finding['resolution_proof'] = str(ROOT / 'proof.json')
            finding['actual_display_scope'] = actual
    ledger['current_integrated_candidate'] = {'path': str(ROM), 'sha256': digest, 'profile': manifest['profile'],
        'MESFILE_sha256': config['target_common_sha256'], 'ARM9_sha256': config['target_arm9_sha256'],
        'patch_sha256': patch['patch_sha256'], 'status': 'experimental', 'manifest': str(ROM.with_suffix('.manifest.json')),
        'initial_source_pins_retained_as_V743_reference_not_overwritten': True}
    records = [r for f in ledger['completed_editorial_families'] for r in f['records']]
    assert len(records) == len({r['message_id'] for r in records}) == 167
    assert sum(r['decision'] == 'revised-and-integrated' for r in records) == 124
    assert ledger['full_goal_complete'] is False and ledger['goal_status'] == 'active'
    save(LEDGER, ledger)
    save('out/editorial_review_latest.json', {**ledger['current_integrated_candidate'], 'details': str(DOC), 'full_goal_complete': False})
    controls = sum(map(len, game['all_other_whole_frame_controls'].values()))
    DOC.write_text(f'''# V762: Port, companion and shared service dialogue

Eighteen entries complete editorial review: fourteen revised and four retained (807,809,815,819). Total reviewed is167:124 revised and43 retained. Source/prose coverage170 includes three750-752 drafts whose actual context remains unmapped. The full editorial goal stays active.820 onward,wider shared prose,Lil/all routes,other player-facing text and the separate graphics audit remain unfinished.

## Faithful, natural English

The admiral/captain warning now states the actual objection. Sera's hesitant refusal and Xien's explicit guardian role replace two unrelated fragments of a trade sentence. The polite Tavern billing refusal replaces a third trade placeholder. Guardian does not invent a parent/grandparent relationship. The original selector identifies Claudio,Camille,Gerhard,Sera and Xien through actual current name getters and416 original actor/route cases.

Food and water disposal confirmations remain separate. The water/rest suggestions are conversational; the supply-ratio question explicitly names water and food. The Sell refusal says sell instead of scrap,without inventing an unsupported last-ship rule. Shared prices use gold as a mass currency noun,which is faithful to the gold coins and grammatical with both1 and plural native amounts. Exact numeric/name arguments are preserved. Four already natural lines are retained with generated formatting.

All prose is authored as one logical paragraph. The existing compiler emits guarded breaks for ordinary constant paragraphs; native formatting balances the three substituted messages. First/final letters,whole words,consistent margins,bounds and padding/blank-page risk are checked. The earlier676/677 formatting repair remains byte-identical as one of the3650 unselected strings.

## Runtime and preservation

A96-byte shim handles only direct808/1245 and YesNo1246,then uses the V760 bounded literal formatter. The supplied admiral name cannot be mistaken for FA/FI/FO/FU/IC commands. All36680 parent/ID/table memberships pass;1124 preceding Yard layouts remain identical.

The code uses16 bytes at02132020 and80 at02147C20 within the previously mapped retired source-constant banks. Current ARM9 sections,overlays and ARM7 are scanned for aliases,ARM branches,ADR targets and crossing strings; the preceding unconditional branch,return and literal pool are verified. All57 active replacement strings and their pointers are checked again. Native execution writes no byte into any of the four immutable banks. No section,123040-byte staged payload,cache,startup or allocator grows. The old mutable name region and active Race string remain untouched.

Complete1549 selections164-1712 are repacked in the existing17 blocks2-18 and4096-byte cache. All3650 unselected complete strings and24 other blocks remain exact,including packed payload19 onward. Only gaps proved NUL/ASCII-space are discarded. The strict parser adds one exact verified directory digest. Three explicit replay configs preserve the exact previous Market stock,Market advice and Shipyard stage outputs; frozen originals are archived and unchanged.

## Verification and its scope

- All40 complete native layout/font cases pass independent ASCII/KANJI glyph decoding,guarded buffers and bounds. Eleven supplied names and seven native numeric values per price cover the substitutions. Four contact sheets were inspected. The23-byte name and INT_MAX amounts are supplied stress contracts,not claimed legal edit limits or earned values.
- All7336 distinct warm/cold COMMON copies pass with explicit ARM946 alignment and guarded full output. The harness supplies the file IO boundary; this is not physical hardware IO.
- The final registered ROM passes thirteen malformed-input gates,all eighteen final text comparisons and byte-exact clean-input patch reconstruction.
- Eight actual dialogue holds cover IDs267,806,813,819 and1245. Every foreground glyph matches a complete independently decoded native plane; resident COMMON blocks,printf/wrapped buffers where applicable,untouched paper cells and all pixels outside the text body are checked.
- {controls} other complete two-screen pairs,all sampled active company/fleet/member-ship models and native town/company states match the immediate parent. Refusals leave money unchanged. The water/food test uses the original supply assignment: declared fixture0/700 becomes350/350 after the ordinary refill/disposal confirmations,with money unchanged.
- Seven fixture-free New Game frames match V760 through title,captain selection and intro. Normal dismissal/menu/Town return controls are included. Historical donor saves and the canonical base retain their hashes.

These are targeted automated cold-boot emulator tests,not a hardware test or a complete route playthrough. Temporary zero-money prerequisites use the original company method and change only its money word. The supply fixture uses the original method and changes eleven bytes only in existing member water/food fields. Original saves remain unchanged. Earned supplies/wealth are not claimed. Companion vetoes,818 and1246 have source/context/native-font coverage and family gameplay samples; their individual actual activations are not claimed. Native selector UI calls are intercepted at original boundaries in the context proof. Istanbul's normal Port story event was preserved; Copenhagen's existing save was used for direct service access.

## Experimental combined candidate

- ROM: `{ROM}`; profile `{manifest['profile']}`.
- Candidate SHA-256: `{digest}`.
- COMMON SHA-256: `{config['target_common_sha256']}`.
- ARM9 SHA-256: `{config['target_arm9_sha256']}`.
- Patch SHA-256: `{patch['patch_sha256']}`. Exact reconstruction from clean SHA-256 `{pins['work/clean.nds']}` passes.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `{pins['out/raphael_natural_v2_accepted_base.nds']}`. No promotion.
- All470 batches,114 accepted layers and preceding graphics are preserved. Relative V760 only `/COMMON/MESFILE.DK4` and `/__arm9__.bin` change; ARM7,overlays and other files remain exact.
- Verifiers: `verify_port_storage_v762.py`,`verify_port_owned_native_v762.py`,`verify_port_native_copies_v762.py`,`verify_port_release_v762.py`,`verify_port_gameplay_v762.py`.
- User acceptance remains pending for cold-boot title/New Game/intro,town UI,Port resupply/disposal,Shipyard refusal and Tavern/companion service screens. The goal can continue without additional preview approval.

ROM,manifest,exact patch,evidence and labeled test screenshots are saved on E. The unresolved18 plaque entries,Online-body exclusion,preserved brown marks and later older-record follow-up remain unchanged. Research/build inputs with pending fields are retained as historical snapshots; this final proof supersedes those fields.
''', encoding='utf-8')
    save(ROOT / 'visual_review.json', {'all4_prior_native_contact_sheets_reviewed_and40_owned_planes_identical': True,
        'actual_sale_funds_water_food_Tavern_and_return_views_opened': True,
        'no_new_actual_companion_818_1246_or_hardware_activation_claim': True})
    scripts = [*Path('scripts').glob('*port*v762.py'), Path('dk4tool/patch/port_services_editorial.py')]
    for p in scripts: ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
    reports = [ROOT / p for p in ('owned_storage.json', 'runtime_plan.json', 'owned_native_verification.json', 'common_repack_plan.json',
        'native_integration.json', 'explicit_parser_replays.json', 'registered_verification.json', 'gameplay_verification.json',
        'patch_proof.json', 'supply_state_verification.json', 'visual_review.json')]
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
        'reviewed_IDs': ids, 'retained_IDs': retained, 'actual_display_IDs': actual, 'remaining_context_drafts': [750, 751, 752],
        'reports': {str(p): sha(p.read_bytes()) for p in reports}, 'protected_files': pins,
        'editorial_ledger_sha256': sha(LEDGER.read_bytes()), 'checkpoint_sha256': sha(DOC.read_bytes()),
        'syntax_checked_files': {str(p): sha(p.read_bytes()) for p in scripts}, 'full_goal_complete': False})
    summary = f'\n\n## V762: integrated Port and companion service prose\n\n18 entries complete review:167 total (124 revised/43 retained). Restored three unrelated trade placeholders,the admiral/captain warning and clear resupply/price dialogue. Owned96-byte shim,416 original actor cases,40 complete fonts,36680 scope cases,1124 unchanged Yard outputs,7336 copies and exact clean patch pass. Eight actual holds across five IDs,{controls} complete screen controls,paired native states and seven New Game frames pass. Other13 IDs have source/native/font coverage with family sampling.470/114 layers and preceding graphics remain; only COMMON/ARM9 change.750-752 context,820 onward,wider shared/Lil/all routes/other prose and separate graphics audit stay open. Experimental; canonical/donors unchanged. See [V762 checkpoint](port_services_v762_checkpoint.md).\n'
    for name in ('translation_progress.md', 'todo.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name; text = path.read_text(encoding='utf-8')
        assert '## V762: integrated Port and companion service prose' not in text
        path.write_text(text.rstrip() + summary, encoding='utf-8')
    for mode, frame in (('sell', 4600), ('copy_no_funds', 6400), ('copy_no_funds', 8000), ('tavern_no_money', 4600),
        ('tavern_no_money', 6800), ('water_only', 3400), ('water_only', 3800), ('water_only', 4200)):
        report = read(CAP / f'port_services_v762_{mode}_762/capture_report.json')
        row = next(r for r in report['frames_captured'] if r['frame'] == frame)
        copy(Path(row['path']), SHOTS / f'{mode}_{frame:06d}.png')
    save(SHOTS / 'provenance.json', {'candidate_sha256': digest, 'fixture_supply_finance_vs_ordinary_sale_copy_disclosed': True,
        'test_evidence_not_earned_progress_or_guide_promotion': True, 'proof': str(ROOT / 'gameplay_verification.json'),
        'files': {p.name: sha(p.read_bytes()) for p in SHOTS.glob('*.png')}})
    for p in ROOT.rglob('*'):
        if p.is_file(): copy(p, ARCHIVE / 'evidence' / p.relative_to(ROOT))
    files = [ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'), DOC, LEDGER, CONFIG, MANUSCRIPT,
        Path('translations/release_stack.json'), Path('out/editorial_review_latest.json'), Path('scripts/build_integrated_release.py'),
        Path('dk4tool/script/common_message_table.py'), *scripts,
        *[Path('translations') / p for p in ('market_stock_replay_for_v762.json', 'market_contract_replay_for_v762.json', 'shipyard_replay_for_v762.json')]]
    for p in files: copy(p, ARCHIVE / 'repository' / p.as_posix())
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': digest,
        'files': {p.relative_to(ARCHIVE).as_posix(): sha(p.read_bytes()) for p in ARCHIVE.rglob('*') if p.is_file()}, 'full_goal_complete': False})
    for p, h in read(ARCHIVE / 'provenance.json')['files'].items(): assert sha((ARCHIVE / p).read_bytes()) == h
    print('V762 recorded and hash-archived on E:167 reviewed,124 revised,43 retained;three context drafts and full goal remain open.', flush=True)


if __name__ == '__main__': main()
