"""Checkpoint completed runtime research while the full matrices remain active."""

import ast
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_storage_v764')
LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/tavern_runtime_v764_research.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V764 Tavern runtime research')


def main():
    assert not ARCHIVE.exists()
    owned = read(ROOT / 'owned_storage_and_native_research.json')
    providers = read(ROOT / 'owned_provider_fragments.json')
    fonts = read(ROOT / 'complete_font_samples.json')
    inherited = read(ROOT / 'inherited_outputs.json')
    pilot = read(ROOT / 'actual_tavern_pilot_context.json')
    assert not owned['native_writes_into_all_prior_and_new_banks']
    assert len(owned['complete_layout_samples']) == len(fonts['complete_planes']) == 50
    assert fonts['all31_IDs'] == list(range(820, 851)) and len(fonts['sheets']) == 5
    assert len(providers['cases']) == 202 and len(providers['all94_global_coordinate_provider_outputs_unchanged']) == 94
    assert len(inherited['all1124_Yard_outputs']) == 1124
    assert len(inherited['all40_Port_cases']) == 40 and len(inherited['all180_earlier_parent_output_controls']) == 180
    assert pilot['actual_message_ID'] == 821 and pilot['no_synthetic_RAM_fixture_no_savestate']
    latest = Path('out/editorial_review_latest.json').read_bytes()
    registry = Path('translations/release_stack.json').read_bytes()
    assert read('out/editorial_review_latest.json')['sha256'] == owned['source_ROM_sha256']
    protected = {
        'out/raphael_natural_v2_accepted_base.nds': '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        'work/clean.nds': 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',
        'E:/Rota Nova translations/Saves/hodram-istanbul-golden-cutlass-blue-oak-v474.dsv': 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132',
        'E:/Rota Nova translations/Generated/work/emulation_v193/full_fleet_staffing_v652_actual/saves/all_routes_combined_v651_candidate.dsv': 'febc859c5af2df6fa8023c349bb7f31b5fc15ea769fb2eea527b3a3f80521731'}
    for path, expected in protected.items(): assert sha(Path(path).read_bytes()) == expected, path
    scripts = [Path('scripts') / name for name in ('inventory_tavern_storage_v764.py', 'verify_tavern_owned_v764.py',
        'verify_tavern_providers_owned_v764.py', 'render_tavern_owned_v764.py', 'inventory_tavern_people_v764.py',
        'prepare_tavern_manuscript_v764.py', 'verify_tavern_inherited_v764.py', 'inspect_tavern_pilot_v764.py',
        'native_call_abi_v764.py', 'probe_tavern_conversations_v764.py', 'record_tavern_runtime_v764.py')]
    modules = [Path('dk4tool/patch') / name for name in ('tavern_editorial_runtime.py', 'tavern_conversations_editorial.py')]
    for path in (*scripts, *modules): ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    doc = read('translations/tavern_conversations_editorial_manuscript_v2.json')
    assert all(not r['review']['formatting'] for r in doc['records'])
    ledger = read(LEDGER)
    assert (ledger['records_editorially_completed'], ledger['records_with_source_and_prose_pass']) == (167, 201)
    save(ROOT / 'editorial_ledger_before_v764.json', ledger)
    ledger['latest_checkpoint'] = 'V764 runtime research: mapped immutable Tavern resources;36680 earlier plus50 new dispatch contracts,256 profession enums,202 original provider fragments,94 unchanged coordinate outputs,50 visually inspected complete native font planes and1124 Yard/40 Port/180 earlier output controls pass. Actual ordinary V762821 pilot mapped. Full matrices remain active;no new ROM or completion credit. Completed167/source-prose201;goal active.'
    ledger['active_source_prose_drafts']['manuscripts'][-1] = 'translations/tavern_conversations_editorial_manuscript_v2.json'
    ledger['active_source_prose_drafts']['groups'][-1]['remaining'] = 'Finish active full native layout matrices and mapped output replay,resolve findings,register31-entry integration,copies/exact patch and targeted actual scenes/transitions.'
    ledger['active_source_prose_drafts']['note'] = 'V2 corrects native person-name metadata: ordinary virtual+24 reads the surname member;do not synthesize full names. All31 English drafts unchanged. Research does not waive formatting or actual release gates;34 drafts remain incomplete.'
    ledger['research_checkpoints'].append({'id': 'V764-Tavern-owned-runtime-provider-and-native-font-research',
        'documentation': str(DOC), 'source_prose_records': 31, 'new_editorially_completed': 0, 'new_ROM': False,
        'evidence': str(ROOT / 'owned_storage_and_native_research.json'), 'full_matrices_pending': True})
    ledger['findings'].append({'id': 'COMMON-820-821-native-name-role-correction', 'native_message_ids': [820, 821],
        'status': 'ordinary-surname-and20-current-company-leader-provider-resolution-mapped',
        'detail': 'Original virtual+24 ordinarily reads table member+4,surname. Source59C10..59C38 resolves company commander and the current-admiral special object. Preserve native output;V2 replaces the incorrect full-name metadata label without changing English. All20 current leader arguments are printable ASCII;expanded layout matrix is active.'})
    ledger['findings'].append({'id': 'ordinary-name-table13-slots-need-consumer-classification',
        'status': 'inventory-only-not-proven-visible-or-rumor-eligible',
        'detail': '207 ordinary native surname getter results include9 mixed-width/Japanese entries and4 nonresident/null results. These include generic people/placeholders and town labels. Actual20 company-leader arguments are English;do not relabel these13 entries as defects or translate them without source/consumer proof.',
        'evidence': str(ROOT / 'actual_native_person_arguments.json')})
    save(LEDGER, ledger)
    DOC.write_text('''# V764: Tavern runtime and visual research

Completed167 (124 revised/43 retained),source/prose201 and34 unfinished drafts are unchanged. V762 remains the latest combined ROM. The31 Tavern drafts820-850 remain unapproved for release formatting;no new profile,playable ROM or patch is emitted.

## Runtime and source ownership

Five exact retired source banks provide340 new code/data bytes,plus20 bytes of declared call/literal changes. Complete original string allocations,their active replacements and current main/autoload/overlay/ARM7 pointer,branch,ADR and crossing-string exclusions are recorded. Four ambiguous old slots are excluded. All57 prior replacement texts survive. Section sizes,the123040-byte staged payload and cache plan are unchanged. Existing constant banks and new banks have native write watches.

The new gate preserves36680 earlier parent/ID/table cases and50 separate gift/player contracts. Exact direct820-850,Yes/No839,player825 and the two original gift tables enter literal balanced formatting;other calls retain the prior handler. All256 profession enum values pass;only the four valid prose labels change to lowercase. English distance/cardinal tables are private;shared UI arrays and the global coordinate formatter are unchanged.

At mapped source addresses,202 original hint/person/trend fragments and94 byte-exact coordinate outputs pass. Fifty complete native paragraph/font samples cover all31 IDs and match independent entire228x64 planes. All five sheets were visually inspected for complete first/final glyphs,whole words,margins and bounds. These are supplied-value research samples,not50 gameplay observations.1124 previous Yard layouts,40 Port cases (267 unchanged system input;39 native wrap outputs) and180 whole earlier output controls pass.

## Actual person-name contracts

Further source tracing corrects V763's full-name label. Ordinary virtual+24 calls0207EAF4 and reads the surname table member+4. Original59C10..59C38 resolves the20 companies' commanders,using the current admiral's special object when required. All20 current results are printable English surnames. The V2 manuscript records native_person_name and leaves every English paragraph unchanged. It does not invent given names or alter approved naming choices.

An additional207-object inventory finds13 unclassified table slots:9 mixed-width/Japanese strings and4 nonresident/null results. Some are generic people or town/placeholders. They are not established eligible rumor arguments or newly proven visible defects. Preserve them pending source/consumer classification;the20 actual current company-leader names are separate evidence. The earlier full_names inventory filename was a research assumption and is superseded by actual_native_person_arguments.json.

## Actual scene pilot and remaining gates

A terminal6201-frame original V762 cold boot used an unmodified copied Istanbul battery save,ordinary Tavern/Order Drink inputs and no RAM fixture. At5000,the actual resident template,printf/wrap buffers and visually inspected framebuffer show821:Hayreddin of Alexandria is an influential local Pirate. The subsequent original Hodram/barmaid scene is preserved. This maps an actual representative rumor scene;it does not verify the revised text or a new ROM.

The first long scratch matrix terminated in a native Unicorn host access violation during843 after no recorded earlier layout findings. Its producer and log are retained. The retry preserves bounded native calls and every callee-saved register/SP check,removes unused per-instruction Python coverage collection and refreshes initialized CPU instances every64 cases. Explicit dispatcher/provider boundary hooks remain. Full31-entry supplied-value wrapping and all20 leader-name combinations are still active;their final reports are not counted as passed.

Finish those runs,resolve findings,replay every whole output at mapped resource addresses,review the full preview set,then integrate through a registered profile. All native COMMON copies,exact clean-input patch reconstruction,cold-boot New Game and paired changed Tavern scenes/transitions remain required. The earlier676/677 formatting repair is independently preserved in V762.750-752,851 onward,all routes,other player-facing prose and the separate unresolved graphics audit remain open.
''', encoding='utf-8')
    paragraph = '\n\n## V764 research: Tavern runtime and scene pilot\n\nMapped immutable resources pass36680+50 scope cases,256 profession values,202 original provider fragments,94 unchanged coordinate outputs,50 independent full font planes (five sheets reviewed),1124 prior Yard layouts,40 Port cases and180 earlier output controls. Ordinary V762821 pilot confirms an actual rumor hold;native surname metadata corrected in unchanged-English V2 drafts. Full matrices/replay,registered integration,copies/patch and revised actual scenes remain pending. No new ROM/completion credit;167 completed and201 source/prose stay unchanged. Wider shared/routes/prose and graphics remain open. See [V764 research](tavern_runtime_v764_research.md).\n'
    for name in ('translation_progress.md', 'todo.md', 'known_issues.md'):
        path = Path('docs') / name; text = path.read_text(encoding='utf-8')
        assert '## V764 research: Tavern runtime and scene pilot' not in text
        path.write_text(text.rstrip() + paragraph, encoding='utf-8')
    assert Path('out/editorial_review_latest.json').read_bytes() == latest
    assert Path('translations/release_stack.json').read_bytes() == registry
    evidence_paths = [ROOT / name for name in ('retired_source_inventory.json', 'owned_storage_and_native_research.json',
        'owned_provider_fragments.json', 'complete_font_samples.json', 'actual_native_person_arguments.json',
        'inherited_outputs.json', 'actual_tavern_pilot_context.json', 'drink_pilot_inputs.json', 'live_jobs_at_checkpoint.json')]
    save(ROOT / 'checkpoint_proof.json', {'previous_goal_turn': 'progress: V762 user-photo native recheck and persistent formatting watchlist refreshed',
        'this_goal_turn': 'progress: exact source ownership,providers,fonts,prior outputs,person-name contract correction and actual baseline scene mapped',
        'completed': 167, 'source_prose_total': 201, 'active_drafts': 34, 'goal_status': 'active',
        'no_new_ROM_or_patch': True, 'unchanged_registry_sha256': sha(registry), 'protected_hashes': protected,
        'evidence_hashes': {str(p): sha(p.read_bytes()) for p in evidence_paths}, 'full_goal_complete': False})
    # Freeze only complete evidence. Active logs and eventual matrices are not
    # snapshotted as final artifacts; their current live observation is separate.
    files = [*evidence_paths, ROOT / 'checkpoint_proof.json', DOC, LEDGER,
             Path('translations/tavern_conversations_editorial_manuscript_v2.json'), *scripts, *modules]
    files += [Path(r['path']) for r in fonts['complete_planes']] + [Path(r['path']) for r in fonts['sheets']]
    files += list((Path('work/analysis/tavern_conversations_v764/failed_host_session_1')).glob('*'))
    for path in files: copy(path, ARCHIVE / path.as_posix())
    save(ARCHIVE / 'provenance.json', {'files': {p.relative_to(ARCHIVE).as_posix(): sha(p.read_bytes()) for p in ARCHIVE.rglob('*') if p.is_file()},
        'scope': 'Completed V764 research snapshot;active full matrices,registered integration and revised actual scenes remain pending.'})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items(): assert sha((ARCHIVE / path).read_bytes()) == digest
    print('V764 completed research hash-archived on E;167 completed/201 source-prose unchanged;goal active.', flush=True)


if __name__ == '__main__': main()
