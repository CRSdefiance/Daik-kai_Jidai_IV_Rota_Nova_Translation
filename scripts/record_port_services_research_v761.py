"""Archive18 source/native reviews without claiming integration or completion."""

import ast
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.review_port_services_v761 import CURRENT, IDS, MANUSCRIPT, ROOT
from scripts.verify_village_wrap_v608 import read, save

LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/port_services_v761_research.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V761 Port services research')


def main():
    assert not ARCHIVE.exists()
    native, context, manuscript = read(ROOT / 'native_RESEARCH/verification.json'), read(ROOT / 'native_context.json'), read(MANUSCRIPT)
    assert native['source_ROM_sha256'] == sha(CURRENT.read_bytes()) == read('out/editorial_review_latest.json')['sha256']
    assert native['manuscript_sha256'] == sha(MANUSCRIPT.read_bytes())
    assert len(native['complete_native_font_cases']) == 40 and native['dispatch']['count'] == 36680
    assert len(context['all416_original_companion_actor_flag_cases']) == 416
    assert native['all1124_prior_Yard_layouts_identical'] and native['actual_gameplay_pending']
    assert tuple(r['message_id'] for r in manuscript['records']) == IDS
    assert all(r['review']['source'] and r['review']['context'] and r['review']['localization'] and r['review']['naturalness']
        and not r['review']['formatting'] for r in manuscript['records'])
    scripts = [Path('scripts') / p for p in ('review_port_services_v761.py', 'probe_port_services_v761.py', 'record_port_services_research_v761.py')]
    for p in scripts: ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
    for row in native['complete_native_font_cases']:
        assert not row['findings'] and sha(Path(row['preview']).read_bytes()) == row['preview_sha256']
    for row in native['preview_sheets']: assert sha(Path(row['path']).read_bytes()) == row['sha256']
    save(ROOT / 'visual_review.json', {'all4_preview_sheets_opened_and_all40_native_panels_inspected': True,
        'three_unrelated_trade_fragments_replaced_with_actual_companion_and_payment_prose': True,
        'complete_first_last_letters_whole_words_aligned_dialogue_rows_and_readable_bounds_observed': True,
        'source267_separate_system_consumer_has_no_portrait_indent': True,
        'all_substituted_names_preserved_in_research_formatter': True,
        'native_layout_not_actual_ROM_scene_or_ownership_approval': True})
    ledger = read(LEDGER)
    assert (ledger['records_editorially_completed'], ledger['records_revised_and_integrated'], ledger['retained_wordings_editorially_completed']) == (149, 110, 39)
    assert ledger['records_with_source_and_prose_pass'] == 152 and ledger['active_source_prose_drafts']['native_message_IDs'] == [750, 751, 752]
    save(ROOT / 'editorial_ledger_at_V760.json', ledger)
    old_latest = Path('out/editorial_review_latest.json').read_bytes()
    old_registry = Path('translations/release_stack.json').read_bytes()
    ledger['records_with_source_and_prose_pass'] = ledger['records_with_source_prose_drafts'] = 170
    ledger['active_source_prose_drafts'] = {'native_message_IDs': [750, 751, 752, *IDS],
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json', str(MANUSCRIPT)],
        'status': '21-source-prose-drafts-not-completed',
        'groups': [{'IDs': [750, 751, 752], 'remaining': 'Actual activation/context mapping'},
            {'IDs': list(IDS), 'remaining': 'Prove production storage/formatting ownership, register complete integration, verify all native copies/exact patch and actual Port/Tavern/companion/price screens.'}],
        'note': 'The new18 have source/context/prose and native research coverage. CPU-only dispatch writes do not establish production ownership or ROM loading. None receives completed/integrated credit.'}
    ledger['latest_checkpoint'] = 'V761 research reviews18 additional Port/companion/Tavern/price drafts.416 original actor/route selector cases,40 complete font/layout previews,36680 scope cases and1124 unchanged prior Yard outputs pass.170 source/prose entries include21 active drafts;149 completed unchanged. V760 remains latest; all broader prose/routes/graphics scope stays open.'
    ledger['research_checkpoints'].append({'id': 'V761-port-companion-and-price-native-research', 'documentation': str(DOC),
        'manuscript': str(MANUSCRIPT), 'source_prose_records': 18, 'new_editorially_completed': 0, 'new_ROM': False,
        'evidence': str(ROOT / 'native_RESEARCH/verification.json')})
    ledger['coverage_units'][0]['next'] = 'Integrate all18 Port/companion/Tavern/price entries267,805-819,1245-1246 with owned storage,complete copies,exact patch and actual scenes. Map750-752 actual callers; continue820 onward,wider shared prose,Lil/all routes and other player-facing text.'
    ledger['findings'].append({'id': 'COMMON-805-reversed-admiral-captain-warning', 'native_message_ids': [805],
        'status': 'source-context-prose-native-research-integration-pending',
        'detail': 'Original check finds no ship captained by the admiral. Restore that requirement instead of asking whether the admiral will serve as captain.'})
    ledger['findings'].append({'id': 'COMMON-810-811-818-unrelated-trade-placeholders', 'native_message_ids': [810, 811, 818],
        'status': 'source-context-prose-native-research-integration-pending',
        'detail': '810/811 are Sera/Xien reassignment vetoes,not adjacent trade fragments.818 is a polite Tavern payment refusal. Source restoration remains draft until registered/actual verification.'})
    ledger['findings'].append({'id': 'COMMON-808-substituted-admiral-name-integrity', 'native_message_ids': [808],
        'status': 'source-context-and-scoped-native-prototype-verified-production-gameplay-pending',
        'detail': 'Original selector supplies current admiral short name through its virtual getter. Exact direct808/1245 and YesNo1246 shim preserves literal name data and bounded runtime wrapping. Eleven supplied names,including FA/FI/FO/FU/IC pairs,render completely;production storage and actual loading are still unproven.'})
    for finding in ledger['findings']:
        if finding.get('id') == 'COMMON-267-1245-observed-neighboring-Yard-prose':
            finding.update({'status': 'source-context-prose-native-research-integration-pending',
                'detail': '267 is the original Sell refusal,not scrap.1245 is a shared native numeric funds refusal with a second generic-script caller;1246 is its YesNo price counterpart. All are reviewed drafts,not integrated/completed.'})
    save(LEDGER, ledger)
    DOC.write_text('''# V761 research: Port services, companions and shared prices

Eighteen new entries have a clean-source/context/prose review:267,805-819 and1245-1246. Four existing wordings are retained (807,809,815,819); fourteen are revised drafts. Completed remains149 (110 revised,39 retained). Source/prose coverage is170,including21 unfinished drafts:these18 and750-752. V760 remains the latest combined ROM. No new ROM,patch or release profile is emitted here.

## Source corrections

-805 objects to leaving the fleet without an admiral serving as captain. The old question asked whether the admiral would serve as captain,which reversed the warning.
-810 and811 are separate companion objections,not two pieces of a trade sentence. Sera hesitantly refuses to leave; Xien explicitly invokes his role as guardian. No father/grandfather relationship is added.
-818 is a polite refusal citing clear billing. The draft says: “I'm sorry,but we're quite clear about our prices...” It invents no posted prices,customer gender or charity claim.
-806/812 keep food and water disposal confirmations independent.813/814 restore natural resupply/rest suggestions.817 explicitly identifies the water/food ratio.
-267 is shown from the original Sell caller when the sellable list is empty. That list excludes the admiral's ship and can include docked ships; the draft does not invent a simplistic last-ship rule.
-1245/1246 are shared numeric cost/refusal prompts. Gold is used as a mass currency noun,remaining faithful to gold coins while keeping grammar correct for1 and plural amounts. Original numeric arguments/callers are preserved.

All authored prose is one logical paragraph,with no hand-positioned spaces or breaks. Proper names remain Rafael,Joakim,Maria and Camille. The full objective still covers wider shared prose,Lil and all routes,help/other player-facing text and separate unfinished graphics work.

## Original context evidence

Exact original ID loads and consumer calls are checked against clean/current ARM9. The original companion selector runs416 supplied actor/route cases:208 actors under selectors0 and1. It binds Claudio to807,Camille to808,Xien to811,Sera to810 and Gerhard to809 in the qualifying route. Actual current name getters establish these identities. The source passes the current admiral's short name into808; the initialized donor supplies Hodram.

The source selector reads a route selector,not a free-standing Boolean. The original admiral's special272/273 confirmation pair remains distinct from these five companion vetoes. UI calls are intercepted at their original boundaries; the tests do not load a complete alternate route or prove an earned reassignment. The generic script-cost and Yard insufficient-funds fragments remain byte-identical to the clean source.

## Native formatting research

Forty complete native layout/font cases cover every paragraph,eleven supplied names and seven numeric values for each shared price message. ASCII/KANJI glyph planes are compared with independent decoders. The separate system consumer for267 is tested with its original unindented painter; portrait messages use the established guarded/aligned painter. All four contact sheets and40 panels were visually inspected. First/final letters,whole words,visible margins,bounds and native guarded buffers pass.

The original post-printf macro parser changes command-like letter pairs inside name data. A96-byte CPU-only shim routes only direct808/1245 and YesNo1246 to the existing bounded literal formatter. It forwards every other call through the original V760 dispatcher with its original saved stack/register contract. All36680 parent/ID/table cases pass; all1124 preceding Yard layouts remain byte-identical.

Two unused-looking areas within the former V760 banks are candidate placements only. Research writes16 bytes at02132020 and80 at02147C20,plus the dispatcher branch,in disposable Unicorn memory. The prior ownership proof is a lead; current aliases,instruction fallthrough,crossing strings,write behavior and source section bounds must be independently rechecked before production use. No ROM image is emitted from these writes. The23-byte name and INT_MAX price are supplied stress contracts,not claimed legal edit limits or earned values.

## Remaining gates

Prove current production ownership; integrate all18 through a registered profile; preserve every unselected string/packed payload and all preceding layers; run the full native COMMON copy/guard checks; verify exact clean-input patch reconstruction and targeted actual Port,Tavern,companion and shared-price scenes with normal dismissal/returns. Only then award completion credit. Keep750-752 actual context mapping,820 onward,wider shared/routes/other prose and graphics audit open. V760 and its canonical parent,donor saves and graphics remain unchanged.
''', encoding='utf-8')
    summary = '\n\n## V761 research: Port services and companion objections\n\n18 clean-source/context/prose drafts restore three unrelated trade placeholders,the admiral/captain warning,water/food prompts and shared price/refusal wording.416 original companion selector cases,40 complete native font/layout cases,36680 exact scope cases and1124 unchanged prior Yard outputs pass; all4 sheets reviewed. These are research results:production ownership,registered copies/patch and actual scenes remain pending.170 source/prose entries include21 active drafts;149 completed (110 revised/39 retained) is unchanged. V760 remains latest.750-752,820 onward,wider shared/Lil/all routes/other prose and separate graphics audit stay open. See [V761 research](port_services_v761_research.md).\n'
    for name in ('translation_progress.md', 'todo.md', 'known_issues.md'):
        p = Path('docs') / name; text = p.read_text(encoding='utf-8')
        assert '## V761 research: Port services and companion objections' not in text
        p.write_text(text.rstrip() + summary, encoding='utf-8')
    assert Path('out/editorial_review_latest.json').read_bytes() == old_latest
    assert Path('translations/release_stack.json').read_bytes() == old_registry
    save(ROOT / 'proof.json', {'research_only': True, 'source_prose_IDs': list(IDS), 'new_completed_records': 0,
        'records_editorially_completed': 149, 'source_prose_total': 170, 'active_drafts': 21,
        'unchanged_latest_ROM_sha256': sha(CURRENT.read_bytes()), 'unchanged_registry_sha256': sha(old_registry),
        'reports': {str(p): sha(p.read_bytes()) for p in (MANUSCRIPT, ROOT / 'native_context.json', ROOT / 'source_and_neighbors.json',
            ROOT / 'native_RESEARCH/verification.json', ROOT / 'visual_review.json', DOC, LEDGER)},
        'syntax_checked_scripts': {str(p): sha(p.read_bytes()) for p in scripts}, 'full_goal_complete': False})
    for p in ROOT.rglob('*'):
        if p.is_file(): copy(p, ARCHIVE / 'evidence' / p.relative_to(ROOT))
    for p in [MANUSCRIPT, LEDGER, DOC, *scripts]: copy(p, ARCHIVE / 'repository' / p.as_posix())
    save(ARCHIVE / 'provenance.json', {'files': {p.relative_to(ARCHIVE).as_posix(): sha(p.read_bytes()) for p in ARCHIVE.rglob('*') if p.is_file()},
        'no_new_ROM_or_completion_credit': True})
    for p, h in read(ARCHIVE / 'provenance.json')['files'].items(): assert sha((ARCHIVE / p).read_bytes()) == h
    print('V761 research archived with hashes:18 new reviewed drafts,170 source/prose,149 completed unchanged;full goal active.', flush=True)


if __name__ == '__main__':
    main()
