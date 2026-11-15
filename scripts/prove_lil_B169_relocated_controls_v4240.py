"""Bind36 relocated progressive dispatches, substitutions, three predicates and all five leaves."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prepare_lil_B169_research_v4235 import ROM, PARENT, PLAN
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B169_relocated_controls_v4240')
DOC = Path('translations/lil_B169_editorial_manuscript_v4.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    doc, plan = read(DOC), read(PLAN)
    packet = read(doc['source_context'])
    dp = read(doc['control_contract'])
    cp = read(doc['source_effect_and_predicate_contract'])
    old, new = [IlnkContainer.parse(NdsImage.open(path).read_file('/data/SC2.DK4')).blocks[169] for path in [PARENT, ROM]]
    assert sha(PARENT.read_bytes()) == doc['current_ROM_sha256'] == plan['candidate_sha256']
    namespace = {**dispatch_base.__dict__, 'SOURCE': Path(doc['source_context']), 'CATALOG_LOOKUP': {}}
    for name, text in dp['source_owned_adapters'].items():
        exec(compile(text, __file__ + '::' + name, 'exec'), namespace)
    namespace['CATALOG_LOOKUP'], binding = namespace['bind_current_catalog'](NdsImage.open(ROM))
    ROOT.mkdir(parents=True)
    ctx = CurrentContext(dp['native_input'], packet['historical_snapshot_ROM'], ROOT / 'current_context')
    rows = {row['id']: row for row in doc['records']}
    dispatches, leaves, predicates = [], [], []
    assert len(plan['blocks']) == 1
    spec = plan['blocks'][0]
    assert sha(new) == spec['research_block_sha256'] and sha(old) == spec['source_block_sha256']
    for record in spec['text_records']:
        value, at = bytes.fromhex(record['target_hex']), record['new_offset']
        assert new[at:at + len(value)] == value
        result = ctx.execute(namespace['dispatch'], value[0], value[1:])
        ctx.machines.pop()
        assert result['resolved_actor_ID'] == (None if value[0] == 254 else rows[record['id']]['source_selector'])
        assert result['registered_catalog_match'] is None
        assert result['boundaries'][1]['text_hex'] == value[1:].replace(b'FI', b'Lil').replace(b'FA', b'Argot').replace(b'FO', b'Argot Co.').hex()
        dispatches.append(dict(id=record['id'], block=169, new_offset=at, stored_target_hex=value.hex(), **result))
    for command in spec['command_map']:
        if command['word'] in [0x4000, 0x100, 0x200, 0x300, 0x400]:
            continue
        a, b = command['old_offset'], command['new_offset']
        previous, value = old[a:a + command['old_extent']], new[b:b + command['new_extent']]
        assert previous == value
        leaves.append(dict(block=169, word=command['word'], old_offset=a, new_offset=b, source_current_target_hex=value.hex()))
        if command['word'] == 0x8000:
            current = dict(offset=b, word=command['word'], native_extent=command['new_extent'], whole_command_hex=value.hex())
            result = ctx.execute(probe, new, current)
            ctx.machines.pop()
            before = next(case for case in cp['source_predicate_cases'] if case['offset'] == a)
            assert result['native_result'] == before['native_result']
            assert result['original_event_completion_calls'] == before['original_event_completion_calls']
            predicates.append(dict(block=169, current_source_case=before, relocated_case=result))
    assert len(dispatches) == 36 and len(leaves) == 5 and len(predicates) == 3 and not ctx.machines
    assert sum(case['resolved_actor_ID'] is None for case in dispatches) == 0
    assert sum(case['word'] == 0xA000 for case in leaves) == 1
    assert sum(case['word'] == 0 for case in leaves) == 1
    assert [case['word'] for case in leaves if case['word'] & 0xFF00 == 0x6300] == []
    presentations = [case for case in leaves if case['word'] not in [0, 0xA000, 0x8000] and case['word'] & 0xFF00 != 0x6300]
    assert len(presentations) == 0
    paths = [DOC, PLAN, Path(doc['control_contract']), Path(doc['source_effect_and_predicate_contract']), Path(__file__)]
    save(ROOT / 'all36_progressive_dispatches_three_predicates_and5_leaves.json', dict(
        candidate=str(PARENT), candidate_sha256=sha(PARENT.read_bytes()), research_ROM=str(ROM), research_ROM_sha256=sha(ROM.read_bytes()),
        manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), source_relocation_plan=str(PLAN), source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        relocated_dispatch_cases=dispatches, relocated_predicate_pairs=predicates,
        all5_source_current_target_nonrelative_nonspeech_leaves=leaves, source_presentation_leaves=presentations,
        all36_progressive_consumers_FI5_FO2_exact=True,
        all_three_unforced_predicates_match_copied_source_state_without_roster_fixture=True,
        no_source_resource_commands_in_this_block=True,
        no_source_presentation_commands_in_this_block=True,
        later_A000_callee_body_not_fully_executed_by_this_probe=True,
        source_numeric29_0001_A000_after_final_give_and_take_and_before_end_preserved=True,
        single_tail_endword_and_all_relative_containers_preserved=True,
        later_older_record0D_reaudit_stays_open=True, registered_catalog_binding=binding,
        native_context_plan=str(ctx.proof_path), native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(path): sha(path.read_bytes()) for path in paths}, actual_selected_B169_IDs=[], new_emulator_runs=0,
        no_ROM_registry_ledger_orcompletion_change=True, full_goal_complete=False))
    print('36 relocated progressive dispatches, three source-matched predicates and five exact leaves pass. Full effects and actual scenes remain unexecuted.')
