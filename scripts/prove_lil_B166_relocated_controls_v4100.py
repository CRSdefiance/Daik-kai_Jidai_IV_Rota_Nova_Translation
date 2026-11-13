"""Bind relocated speakers/FI3, Fernando membership, leaves and advice menu getters."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.map_lil_B122_B127_source_v3260c import choice_getters
from scripts.prepare_lil_B166_research_v4095 import ROM, PARENT, PLAN
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B166_relocated_controls_v4100')
DOC = Path('translations/lil_B166_editorial_manuscript_v5.json')
MENU = Path('translations/lil_B166_choice_manuscript_v2.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    doc, plan, menu = map(read, [DOC, PLAN, MENU])
    packet = read(doc['source_context'])
    dp = read(doc['control_contract'])
    cp = read(doc['source_effect_and_predicate_contract'])
    old, new = [IlnkContainer.parse(NdsImage.open(p).read_file('/data/SC2.DK4')).blocks[166] for p in [PARENT, ROM]]
    assert sha(PARENT.read_bytes()) == doc['current_ROM_sha256'] == plan['candidate_sha256']
    namespace = {**dispatch_base.__dict__, 'SOURCE': Path(doc['source_context']), 'CATALOG_LOOKUP': {}}
    for name, text in dp['source_owned_adapters'].items():
        exec(compile(text, __file__ + '::' + name, 'exec'), namespace)
    namespace['CATALOG_LOOKUP'], binding = namespace['bind_current_catalog'](NdsImage.open(ROM))
    ROOT.mkdir(parents=True)
    ctx = CurrentContext(dp['native_input'], packet['historical_snapshot_ROM'], ROOT / 'current_context')
    rows = {r['id']: r for r in doc['records']}
    dispatches, leaves, predicates = [], [], []
    assert len(plan['blocks']) == 1
    spec = plan['blocks'][0]
    assert sha(new) == spec['research_block_sha256'] and sha(old) == spec['source_block_sha256']
    for record in spec['text_records']:
        value = bytes.fromhex(record['target_hex'])
        at = record['new_offset']
        assert new[at:at + len(value)] == value
        result = ctx.execute(namespace['dispatch'], value[0], value[1:])
        ctx.machines.pop()
        assert result['resolved_actor_ID'] == rows[record['id']]['source_selector']
        assert result['registered_catalog_match'] is None
        assert result['boundaries'][1]['text_hex'] == value[1:].replace(b'FI', b'Lil').replace(b'FA', b'Argot').replace(b'FO', b'Argot Co.').hex()
        dispatches.append(dict(id=record['id'], block=166, new_offset=at, stored_target_hex=value.hex(), **result))
    for command in spec['command_map']:
        if command['word'] in [0x4000, 0x100, 0x200, 0x300, 0x400, 0x2100]:
            continue
        a, b = command['old_offset'], command['new_offset']
        previous = old[a:a + command['old_extent']]
        value = new[b:b + command['new_extent']]
        assert previous == value
        leaves.append(dict(block=166, word=command['word'], old_offset=a, new_offset=b, source_current_target_hex=value.hex()))
        if command['word'] == 0x8000:
            current = dict(offset=b, word=command['word'], native_extent=command['new_extent'], whole_command_hex=value.hex())
            result = ctx.execute(probe, new, current)
            ctx.machines.pop()
            before = next(p for p in cp['source_predicate_cases'] if p['offset'] == a)
            assert result['native_result'] == before['native_result']
            assert result['original_event_completion_calls'] == before['original_event_completion_calls']
            predicates.append(dict(block=166, current_source_case=before, relocated_case=result))
    assert len(dispatches) == 42 and len(leaves) == 11 and len(predicates) == 1 and not ctx.machines
    assert sum(c['word'] == 0xA000 for c in leaves) == sum(c['word'] == 0 for c in leaves) == 1
    assert [c['word'] for c in leaves if c['word'] & 0xFF00 == 0x6300] == [0x632B, 0x632C]
    command = next(c for c in spec['command_map'] if c['word'] == 0x2100)
    at = command['new_offset']
    target = dict(offset=at, word=0x2100, native_extent=command['new_extent'], whole_command_hex=new[at:at + command['new_extent']].hex())
    assert target['whole_command_hex'] == menu['records'][0]['typed_target_object_hex']
    getters = choice_getters(NdsImage.open(ROM).read_file('/__arm9__.bin'), target)
    assert len(getters) == 2 and all([r['text'] for r in phase['labels']] == ['Please do', 'Decline'] for phase in getters)
    paths = [DOC, MENU, PLAN, Path(doc['control_contract']), Path(doc['source_effect_and_predicate_contract']), Path(__file__)]
    save(ROOT / 'all42_dispatches_Fernando_predicate11_leaves_and_two_choice_getters.json', dict(
        candidate=str(PARENT), candidate_sha256=sha(PARENT.read_bytes()), research_ROM=str(ROM), research_ROM_sha256=sha(ROM.read_bytes()),
        manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), source_relocation_plan=str(PLAN), source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        relocated_dispatch_cases=dispatches, relocated_predicate_pairs=predicates,
        all11_source_current_target_nonrelative_nonspeech_nonchoice_leaves=leaves,
        relocated_menu_command=target, relocated_choice_getter_phases=getters,
        all42_progressive_consumers_four_static_actors_FI3_exact=True,
        unforced_Fernando_result_matches_source_without_roster_fixture=True,
        all20_resource_boundary_cases_reused_by_exact_words_runtime_and_dispatch=True,
        menu_VM_and_complete_native_planes_reused_by_exact24byte_object=True,
        resource_presentation_and_A000_bodies_not_fully_executed_by_this_probe=True,
        both_advice_paths_rejoin_before_unchanged_recruitment_effect_and_single_end=True,
        older_record_technical_reaudit_still_open=True, choice_outcomes_need_actual_selection=True,
        registered_catalog_binding=binding, native_context_plan=str(ctx.proof_path), native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p): sha(p.read_bytes()) for p in paths}, actual_selected_B166_IDs=[], new_emulator_runs=0,
        no_ROM_registry_ledger_orcompletion_change=True, full_goal_complete=False))
    print('42 relocated speakers/FI3,one source-matched Fernando query,11 exact leaves and two choice getter sets pass.')
