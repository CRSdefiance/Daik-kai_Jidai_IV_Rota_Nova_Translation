"""Bind an exact original Julio recruitment command as disclosed test setup, not earned progress."""
import inspect
import struct
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B194_recruitment_binding_v5518')
DOC = Path('translations/lil_B194_editorial_manuscript_v3.json')
ENTRY = Path('work/analysis/lil_B165_entry_v4014/source_EV2_B165_action_dependency_and_native_getter_binding.json')


def getters(arm, common, raw, plan):
    cpu, get, provider = machine(arm, common, raw, plan)
    before = bytes(cpu.mem_read(0x02000000, 0x400000))
    root, captain = get(0xCB184), get(0x7F244)
    current_company = get(0x397D8, get(0xCB160))
    actor = root + 4 + 6 * 32
    slot17 = get(0x7B60, 17)
    actor_company = get(0x7E958, actor)
    availability = get(0x7DB14, actor)
    assert (captain, current_company, actor_company, availability, slot17) == (2, 1, 21, 0, 24)
    assert bytes(cpu.mem_read(0x02000000, 0x400000)) == before
    return dict(captain=captain, current_company=current_company, actor6_company=actor_company,
                original_actor6_availability=availability, original_slot17_value=slot17,
                original_slot24_sentinel_skips_optional_fleet_assignment=True,
                all4MiB_and_ABI_exact_no_recruitment_or_state_forced=True,
                current_executed_instruction_addresses=len(provider.executed_current))


if __name__ == '__main__':
    assert not ROOT.exists()
    doc, entry = read(DOC), read(ENTRY)
    current, clean = NdsImage.open(doc['current_ROM']), NdsImage.open('work/clean.nds')
    assert sha(Path(doc['current_ROM']).read_bytes()) == doc['current_ROM_sha256']
    arm, source_arm = [im.read_file('/__arm9__.bin') for im in [current, clean]]
    ev = current.read_file('/data/EV2.DK4')
    assert ev == clean.read_file('/data/EV2.DK4') and sha(ev) == entry['EV2_sha256']
    chosen = entry['selected_B165_source_events']
    assert len(chosen) == 1
    event = chosen[0]
    assert (event['event_ID'], event['action_index'], event['script_block']) == (165, 166, 165)
    assert not event['must_be_completed'] and not event['must_not_be_completed']
    at = 96 + event['body_offset']
    assert ev[at:at + event['source_record_bytes']].hex() == event['source_hex']
    action_start = 96 + struct.unpack_from('<I', ev, 0x4C)[0]
    assert struct.unpack_from('<H', ev, action_start + 2 * event['action_index'])[0] == event['native_action_word']
    inventory, _, _ = scoped_inventory()
    versions = []
    command = bytes.fromhex('00a0ffff06100120')
    for label, image in [('clean', clean), ('current', current)]:
        block = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[165]
        commands, _ = inventory(image.read_file('/__arm9__.bin'), block)
        effects = [c for c in commands if c['word'] == 0xA000]
        assert len(effects) == 1 and effects[0]['whole_command_hex'] == command.hex()
        assert effects[0]['native_extent'] == 8
        if label == 'clean':
            assert effects[0]['offset'] == 1532 and block[1540:1544] == bytes(4)
        isolated = b'CS\0\1' + struct.pack('<H', 8) + bytes(2) + command
        result = walk(image.read_file('/__arm9__.bin'), isolated)
        assert result['error'] is None and result['stopped_offset'] == result['logical_end'] == 16
        assert len(result['opaque_effect_bridges']) == 1
        assert result['opaque_effect_bridges'][0]['PC'] == 0x0202BE8C
        versions.append(dict(version=label, original_offset=effects[0]['offset'], command_hex=command.hex(),
                             original_structural_decode=result, full_body_unexecuted_by_this_structural_probe=True))
    packed = int.from_bytes(command[4:], 'little')
    assert packed >> 28 == 2 and packed & 255 == 6 and (packed >> 16) & 1 == 1
    slot = (packed >> 8) & 31
    assert slot == 16
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    spans = [(0x2A510, 0x2A600), (0x2BE8C, 0x2BF84), (0x2BB18, 0x2BDC8),
             (0x7B60, 0x7C80), (0x7E950, 0x7E960), (0x7DB14, 0x7DC00)]
    disassembly, source_spans = [], []
    for start, end in spans:
        assert arm[start:end] == source_arm[start:end]
        source_spans.append(dict(start=start, end=end, source_current_sha256=sha(arm[start:end])))
        disassembly.extend(f'{x.address:08X} {x.bytes.hex()} {x.mnemonic} {x.op_str}'
                           for x in decoder.disasm(arm[start:end], 0x02000000 + start))
    # Independent exact branch/call checks: packed type2, original actor6 and join-bit parsing,
    # slot16 remap to17, native company setter, status initializer, resource48 and modal body.
    instructions = {x.address - 0x02000000: x for x in decoder.disasm(arm[0x2BB18:0x2BDC8], 0x0202BB18)}
    for site, target in [(0x2BB38, 0x7B60), (0x2BB54, 0x2BB5C), (0x2BB80, 0xCB184),
                         (0x2BBA0, 0xCB160), (0x2BBA4, 0x397D8), (0x2BBB0, 0x7E950),
                         (0x2BBC0, 0x7DAF0), (0x2BC40, 0x1096F8), (0x2BC54, 0x5473C)]:
        ins = instructions[site]
        assert ins.mnemonic == 'bl' and int(ins.op_str.lstrip('#'), 16) == 0x02000000 + target
    ROOT.mkdir(parents=True)
    text = ROOT / 'source_exact_setup_decoder_and_original_recruitment_body.txt'
    text.write_text('\n'.join(disassembly) + '\n', encoding='utf-8')
    ctx = CurrentContext('work/analysis/lil_B194_voices_v5490/current_native_input.json', doc['current_ROM'], ROOT / 'current_context')
    values = ctx.execute(getters)
    ctx.machines.pop()
    assert not ctx.machines
    save(ROOT / 'source_B165_Julio6_recruitment_initializer_disclosed_for_conditional_test.json', dict(
        candidate=doc['current_ROM'], candidate_sha256=doc['current_ROM_sha256'],
        original_command_hex=command.hex(), source_block=165, source_offset=1532, source_native_extent=8,
        source_current_command_versions=versions, source_event=event, original_EV2_sha256=sha(ev),
        source_entry_proof=str(ENTRY), source_entry_proof_sha256=sha(ENTRY.read_bytes()),
        decoded_packed_kind=2, decoded_actor=6, decoded_join_bit=1, decoded_slot_field=16,
        original_slot16_remapped_to17=True, original_current_getters=values, exact_native_handler_spans=source_spans,
        source_joins_actor_company_to_current_company_and_calls_original_status_initializer=True,
        optional_fleet_assignment_skipped_for_measured_slot24=True,
        original_recruitment_resource48_and_modal_body_will_execute_normally_in_fixture=True,
        full_recruitment_effect_body_not_executed_by_this_readonly_binding=True,
        B165_outer_scheduler_conditions_and_earned_recruitment_not_claimed=True,
        original_B194_availability_to_be_observed_without_result_or_RNG_forcing=True,
        disassembly=str(text), disassembly_sha256=sha(text.read_bytes()), source_owned_getter=inspect.getsource(getters),
        native_context_plan=str(ctx.proof_path), native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        new_emulator_runs=0, new_review_credit=0, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print('Original B165 actor6 join initializer,source event and native body bound;readonly current slot17 returns24. Full effect/conditional display remains actual-test work.')
