"""Bind relocated FI dispatch, changed predicate alignment, resource42, both UIs and conditional paths."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B190_C200_v5318 import C200
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.prepare_lil_B194_research_v5508 import ROM, PARENT, PLAN
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B194_relocated_controls_v5513')
DOC = Path('translations/lil_B194_editorial_manuscript_v3.json')
CARRY = Path('work/analysis/lil_B194_carried_result_v5495c/all20_C200_and10_end_prior_result_cases.json')


if __name__ == '__main__':
    assert not ROOT.exists()
    doc, plan, carried = map(read, [DOC, PLAN, CARRY])
    packet = read(doc['source_context'])
    dispatch = read(doc['control_contract'])
    control = read(doc['source_effect_and_predicate_contract'])
    images = [NdsImage.open(p) for p in [PARENT, ROM]]
    old, new = [IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[194] for im in images]
    assert sha(PARENT.read_bytes()) == doc['current_ROM_sha256'] == plan['candidate_sha256'] == control['candidate_sha256']
    assert images[0].read_file('/__arm9__.bin') == images[1].read_file('/__arm9__.bin')
    spec = plan['blocks'][0]
    assert sha(old) == spec['source_block_sha256'] and sha(new) == spec['research_block_sha256']
    namespace = {**dispatch_base.__dict__, 'SOURCE': Path(doc['source_context']), 'CATALOG_LOOKUP': {}}
    for name, text in dispatch['source_owned_adapters'].items():
        exec(compile(text, __file__ + '::' + name, 'exec'), namespace)
    namespace['CATALOG_LOOKUP'], binding = namespace['bind_current_catalog'](images[1])
    ui_env = dict(C200.__globals__)
    exec(compile(carried['source_owned_C200_adapter'], __file__ + '::prior-C200', 'exec'), ui_env)
    resource_text = checked_text(control['source_owned_adapters']['resource42'], {
        'def source632A(arm,common,raw,plan,previous,boundary_return):':
        'def target632A(arm,common,raw,plan,block,command,previous,boundary_return):',
        "value=bytes.fromhex('2a63')": "value=block[command['offset']:command['offset']+2];assert value==bytes.fromhex('2a63')",
        "cpu.mem_write(stream-16,b'\\xA5'*34);cpu.mem_write(stream,value)":
        "cpu.mem_write(stream-16,b'\\xA5'*(len(block)+32));cpu.mem_write(stream,block)",
        "struct.pack('<4I',0,stream,0,0)": "struct.pack('<4I',0,stream+command['offset'],0,0)",
        'bytes(cpu.mem_read(stream,2))==value': 'bytes(cpu.mem_read(stream,len(block)))==block',
        'stream+2,result-16': 'stream+len(block),result-16',
    })
    resource_env = dict(resource_base.__dict__)
    exec(compile(resource_text, __file__ + '::full-target-resource42', 'exec'), resource_env)
    ROOT.mkdir(parents=True)
    ctx = CurrentContext(dispatch['native_input'], packet['historical_snapshot_ROM'], ROOT / 'current_context')
    rows = {r['id']: r for r in doc['records']}
    dispatches = []
    for record in spec['text_records']:
        value, at = bytes.fromhex(record['target_hex']), record['new_offset']
        assert new[at:at + len(value)] == value
        result = ctx.execute(namespace['dispatch'], value[0], value[1:])
        ctx.machines.pop()
        assert result['resolved_actor_ID'] == (None if value[0] == 254 else rows[record['id']]['source_selector'])
        assert result['registered_catalog_match'] is None
        assert result['boundaries'][1]['text_hex'] == value[1:].replace(b'FI', b'Lil').hex()
        assert result['source_voice_class'] == {6: 5, 117: 0, 156: 4, 254: None}[value[0]]
        dispatches.append(dict(id=record['id'], block=194, new_offset=at, stored_target_hex=value.hex(), **result))
    old_leaves = {r['offset']: r for r in control['all6_source_current_nonrelative_nonspeech_leaves']}
    leaves, predicates, uis, resources = [], [], [], []
    for command in spec['command_map']:
        if command['word'] in [0x4000, 0x100, 0x200, 0x300, 0x400]:
            continue
        a, b = command['old_offset'], command['new_offset']
        value = new[b:b + command['new_extent']]
        assert old[a:a + command['old_extent']] == value
        assert old_leaves[a]['source_current_hex'] == value.hex()
        leaf = dict(block=194, word=command['word'], old_offset=a, new_offset=b,
                    source_current_target_hex=value.hex())
        leaves.append(leaf)
        cmd = dict(offset=b, word=command['word'], native_extent=command['new_extent'], whole_command_hex=value.hex())
        if command['word'] == 0x8000:
            result = ctx.execute(probe, new, cmd)
            ctx.machines.pop()
            assert result['native_result'] == control['source_predicate_cases'][1]['native_result'] == [2, 0, 0, 0, 0, 0]
            assert not result['original_event_completion_calls']
            writes = result['original_unaligned_operand_read_scratch_writes']
            assert b == 274 and (b + 4) % 4 == 2 and len(writes) == 1
            assert not control['source_predicate_cases'][1]['original_unaligned_operand_read_scratch_writes']
            predicates.append(dict(source_offset=a, target_offset=b, case=result))
        if command['word'] == 0xC200:
            for prior in [0, 1, 2, 3, 0xFFFFFFFF]:
                result = ctx.execute(ui_env['prior_C200'], new, cmd, prior)
                ctx.machines.pop()
                earlier = next(r['case'] for r in carried['C200_cases'] if r['version'] == 'current' and r['source_offset'] == a and r['prior_result'] == prior)
                assert result['native_result'] == [3, prior, 0, 0, 0, 0]
                for key in ['source_owned_UI_request_words', 'source_owned_UI_writes']:
                    assert result[key] == earlier[key]
                uis.append(dict(source_offset=a, target_offset=b, prior_result=prior, case=result))
        if command['word'] == 0x632A:
            for prior in [0, 1, 2, 3, 0xFFFFFFFF]:
                for incidental in [0, 0xFFFFFFFF]:
                    result = ctx.execute(resource_env['target632A'], new, cmd, prior, incidental)
                    ctx.machines.pop()
                    earlier = next(r for r in control['source_resource42_boundary_and_carried_result_cases'] if r['previous_result'] == prior and r['incidental_boundary_return'] == incidental)
                    assert result['native_result'] == earlier['native_result'] == [3, prior, 0, 0, 0, 0]
                    assert result['original_boundary_calls'] == earlier['original_boundary_calls']
                    resources.append(dict(source_offset=a, target_offset=b, case=result))
    assert [(r['word'], r['old_offset'], r['new_offset']) for r in leaves] == [
        (0xA000, 8, 8), (0x8000, 312, 274), (0x632A, 406, 376),
        (0xC200, 494, 464), (0xC200, 534, 508), (0, 536, 510)]
    source_to_target = {r['old_offset']: r['new_offset'] for r in spec['command_map']}
    by_at = {r['new_offset']: r for r in spec['command_map']}
    speech_by_at = {r['new_offset'] - 5: rows[r['id']]['source_record_index'] for r in spec['text_records']}
    paths = []
    for source_path in control['source_structural_predicate0_1_paths']:
        prior, cursor, visited, spoken, controls = source_path['predicate_result'], 8, [], [], []
        for _ in range(30):
            command = by_at[cursor]
            word = command['word']
            visited.append(cursor)
            if word == 0:
                controls.append(cursor)
                break
            if word in [0x100, 0x200, 0x300, 0x400]:
                case = next(c for c in spec['target_native_skip_cases'] if c['new_offset'] == cursor and c['last_result'] == prior)
                cursor += case['native_extent']
                continue
            if word == 0x4000:
                spoken.append(speech_by_at[cursor])
            else:
                controls.append(cursor)
            cursor += command['new_extent']
        else:
            raise AssertionError('Target path did not reach end')
        assert visited == [source_to_target[a] for a in source_path['source_command_offsets']]
        assert controls == [source_to_target[a] for a in source_path['non_speech_non_relative_offsets']]
        assert spoken == source_path['speech_record_indices'] and cursor == 510
        paths.append(dict(predicate_result=prior, target_command_offsets=visited, speech_record_indices=spoken,
                          target_non_speech_non_relative_offsets=controls, target_end_offset=cursor,
                          source_path_isomorphic_via_original_native_skip_results=True, not_actual_VM_or_gameplay=True))
    end_cases = []
    arm = images[1].read_file('/__arm9__.bin')
    for prior in [0, 1, 2, 3, 0xFFFFFFFF]:
        cpu = machine(arm)
        stream, owner, result, length = 0x02660000, 0x02650000, 0x02668000, 0x02668100
        logical = spec['research_logical_end']
        assert logical == 514 and new[510:logical] == bytes(4)
        cpu.mem_write(stream - 16, b'\xa5' * (logical + 48))
        cpu.mem_write(stream, new[:logical])
        cpu.mem_write(owner - 16, b'\xa5' * 64)
        cpu.mem_write(owner, struct.pack('<4I', 0, stream + 510, 0, 0))
        guard = bytes(cpu.mem_read(owner - 16, 64))
        cpu.mem_write(result - 16, b'\xa5' * 80)
        cpu.mem_write(result, struct.pack('<6I', 0, prior, 0, 0, 0, 0))
        cpu.mem_write(length - 16, b'\xa5' * 36)
        cpu.mem_write(length, bytes(4))
        before = bytes(cpu.mem_read(0x02000000, 0x400000))
        call(cpu, 0x2A510, (result, owner, length, prior))
        values = list(struct.unpack('<6I', cpu.mem_read(result, 24)))
        assert values == [0, prior, 0, 0, 0, 0] and struct.unpack('<I', cpu.mem_read(length, 4))[0] == 4
        assert bytes(cpu.mem_read(0x02000000, 0x400000)) == before
        assert bytes(cpu.mem_read(owner - 16, 64)) == guard
        assert bytes(cpu.mem_read(stream, logical)) == new[:logical]
        for at in [stream - 16, stream + logical, result - 16, result + 24, length - 16, length + 4]:
            assert bytes(cpu.mem_read(at, 16)) == b'\xa5' * 16
        end_cases.append(dict(target_offset=510, prior_result=prior, native_result=values,
                              all4MiB_owner_logical_payload_and_ABI_guards_exact=True))
    assert len(dispatches) == 11 and len(leaves) == 6 and len(predicates) == 1
    assert len(uis) == len(resources) == 10 and len(end_cases) == 5 and not ctx.machines
    paths_to_hash = [DOC, PLAN, CARRY, Path(doc['control_contract']), Path(doc['source_effect_and_predicate_contract']), Path(__file__)]
    save(ROOT / 'all11_dispatches_changed_predicate_alignment_resource42_two_UI_and_paths.json', dict(
        candidate=str(PARENT), candidate_sha256=sha(PARENT.read_bytes()), research_ROM=str(ROM), research_ROM_sha256=sha(ROM.read_bytes()),
        manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), source_relocation_plan=str(PLAN), source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        relocated_dispatch_cases=dispatches, all6_source_current_target_nonrelative_nonspeech_leaves=leaves,
        unforced_relocated_predicate_cases=predicates, relocated_C200_prior_result_cases=uis,
        relocated_resource42_prior_result_cases=resources, relocated_end_prior_result_cases=end_cases,
        relocated_structural_predicate0_1_paths=paths, changed_unaligned_operand_scratch_owned_and_restored=True,
        one_FI_default_Lil_and_source_voice5_0_4_and_null_actor_FE_exact=True,
        resource42_full_body_and_UI_preparation_display_bodies_explicitly_bridged_unexecuted=True,
        unchanged_A000_bytes_and_source_structural_decoder_proof_reused_no_body_claim=True,
        no_availability_result_RNG_roster_or_gameplay_state_forced=True,
        full_actual_scene_and_registered_integration_pending=True, registered_catalog_binding=binding,
        source_owned_target_resource_adapter=resource_text,
        native_context_plan=str(ctx.proof_path), native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p): sha(p.read_bytes()) for p in paths_to_hash}, new_emulator_runs=0, new_review_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print(dict(dispatches=11, target_predicate_result=0, owned_unaligned_scratch_writes=1,
               resource42_boundary_cases=10, target_C200_carried_result_cases=10, target_end_carried_result_cases=5,
               structural_path_speeches=[len(p['speech_record_indices']) for p in paths], credit=0))
