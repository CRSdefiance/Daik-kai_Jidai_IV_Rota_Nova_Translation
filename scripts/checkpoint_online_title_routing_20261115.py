"""Bind the original Online and About Extras title routes to their native text owners."""

from pathlib import Path
from struct import pack, unpack, unpack_from

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
    UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_SP,
)

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import checkpoint_pending_shared_native_20261115 as prior
from scripts import register_market_trade_dialogue_20261115 as current
from scripts.probe_button_prompt_native import BASE, STACK, STOP, VIEW, call, machine
from scripts.review_visible_online_captions_v1 import DESCRIPTORS
from scripts.seal_shared_text_source_v1 import reference
from scripts.stage_extras_tie_in_20261114 import TABLE


base, sha = current.base, prior.sha
OUTPUT = prior.ROOT / 'online_title_routing_20261115_v1.json'
IDS = set(range(3289, 3320))
CAPTION = 0x104CD8
DRAW = BASE + 0xD5404
GRAPHIC_HELPERS = {BASE + offset for offset in (0xD393C, 0xD5160, 0xD5140, 0xC9C48, 0x1096F8)}
LOCKS = ((0x104060, 0x1045B4), (0x1045B4, 0x105294), (0x10537C, 0x1053EC), (0x105694, 0x105704))


def set_regs(cpu, values):
    for reg, value in values.items():
        cpu.reg_write(reg, value)


def read_word(cpu, address):
    return unpack('<I', cpu.mem_read(address, 4))[0]


def c_string(arm, pointer):
    start = pointer - BASE
    end = arm.index(0, start)
    return arm[start:end]


def route_cases(arm):
    cpu = machine(arm)
    observed, requested_descriptors = [], []

    def observe(u, address, _size, _data):
        assert address not in prior.ENTRY_POINTS, f'Unexpected COMMON request through {address:#x}'
        if address == STOP:
            u.emu_stop()
        elif address in GRAPHIC_HELPERS:
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
        elif address == DRAW:
            state = u.reg_read(UC_ARM_REG_R0)
            pointer = u.reg_read(UC_ARM_REG_R1)
            x, y = unpack('<2I', u.mem_read(state + 0x24, 8))
            style = read_word(u, state + 0x30)
            payload = c_string(arm, pointer)
            assert bytes(u.mem_read(pointer, len(payload) + 1)) == payload + b'\0'
            observed.append(dict(pointer=pointer, exact_null_terminated_hex=(payload + b'\0').hex(), x=x, y=y, style=style))
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
        elif address == BASE + 0x1045B4:
            requested_descriptors.append(u.reg_read(UC_ARM_REG_R0))
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    hook = cpu.hook_add(UC_HOOK_CODE, observe)
    categories, guide, motion, extras = [], [], [], []
    try:
        for number in (0, 1, 2, 3, 4, 0xFFFFFFFF):
            cpu.mem_write(STACK + 0x15C, pack('<I', VIEW + 0x100))
            cpu.mem_write(VIEW + 0xF0, pack('<I', 0))
            set_regs(cpu, {UC_ARM_REG_SP: STACK, UC_ARM_REG_R6: VIEW, UC_ARM_REG_R7: 0, UC_ARM_REG_R9: number})
            cpu.emu_start(BASE + 0x104320, BASE + 0x10435C, count=32)
            assert cpu.reg_read(UC_ARM_REG_PC) == BASE + 0x10435C
            descriptor = BASE + DESCRIPTORS[number] if number in range(4) else None
            assert requested_descriptors == ([descriptor] if descriptor else [])
            categories.append(dict(menu_result=number, descriptor=descriptor))
            requested_descriptors.clear()

        for category, descriptor in enumerate(DESCRIPTORS):
            data, pointers, count = unpack_from('<3I', arm, descriptor)
            assert count == (4, 4, 2, 3)[category]
            for page in range(count):
                call(cpu, CAPTION, (page, BASE + descriptor, VIEW, 0), instruction_limit=4096)
                event, = observed
                observed.clear()
                pointer = read_word(cpu, pointers + 4 * page)
                assert event['pointer'] == pointer
                assert event['x'] == 128 - 3 * len(c_string(arm, pointer))
                assert (event['y'], event['style']) == (12, 15)
                guide.append(event | dict(category=category, page=page, descriptor=BASE + descriptor,
                                          pointer_field=pointers + 4 * page))
                for direction, start, after_store in (('back', 0x104D30, 0x104D98), ('forward', 0x104FD8, 0x105030)):
                    cpu.mem_write(VIEW, pack('<2I', page, 0xFFFFFFFF))
                    cpu.mem_write(STACK, pack('<I', VIEW))
                    set_regs(cpu, {UC_ARM_REG_SP: STACK, UC_ARM_REG_LR: STOP, UC_ARM_REG_R0: VIEW,
                                   UC_ARM_REG_R1: VIEW + 4, UC_ARM_REG_R2: count, UC_ARM_REG_R3: data})
                    cpu.emu_start(BASE + start, BASE + after_store, count=64)
                    cursor, subimage = unpack('<2I', cpu.mem_read(VIEW, 8))
                    edge = page == (0 if direction == 'back' else count - 1)
                    if edge:
                        assert cpu.reg_read(UC_ARM_REG_PC) == STOP and cpu.reg_read(UC_ARM_REG_R0) == 0
                        assert cursor == page and subimage == 0xFFFFFFFF and cpu.reg_read(UC_ARM_REG_SP) == STACK
                    else:
                        assert cpu.reg_read(UC_ARM_REG_PC) == BASE + after_store
                        assert cursor == page + (-1 if direction == 'back' else 1)
                        assert subimage == (read_word(cpu, data + 16 * cursor + 12) - 1 if direction == 'back' else 0)
                    assert not observed
                    motion.append(dict(category=category, old_page=page, new_page=cursor, direction=direction, edge=edge))

        for old_page in range(-1, 6):
            opened = old_page < 0
            closing = old_page == 5
            start = 0x1040DC if opened else 0x1041C8
            end = 0x104100 if opened else 0x10408C if closing else 0x10410C
            set_regs(cpu, {UC_ARM_REG_SP: STACK, UC_ARM_REG_R5: 1, UC_ARM_REG_R6: VIEW, UC_ARM_REG_R7: 0,
                           UC_ARM_REG_R8: 2, UC_ARM_REG_R9: max(old_page, 0), UC_ARM_REG_R10: 15, UC_ARM_REG_R11: 32})
            cpu.emu_start(BASE + start, BASE + end, count=256)
            assert cpu.reg_read(UC_ARM_REG_PC) == BASE + end and cpu.reg_read(UC_ARM_REG_SP) == STACK
            if closing:
                assert not observed and cpu.reg_read(UC_ARM_REG_R9) == 6
                extras.append(dict(previous_page=old_page, returned_to_extras_without_text=True))
            else:
                event, = observed
                observed.clear()
                n = old_page + 1
                field = BASE + TABLE + n * 4
                assert event['pointer'] == read_word(cpu, field)
                assert (event['x'], event['y'], event['style']) == (0, 0, 15)
                extras.append(event | dict(previous_page=old_page, page=n, pointer_field=field))
    finally:
        cpu.hook_del(hook)
    return dict(categories=categories, guide_draws=guide, guide_motion=motion, extras=extras)


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(current.ROM) == release['candidate_sha256']
    assert base.digest(current.stage.CLEAN) == release['clean_input_sha256']
    clean, active = map(base.NdsImage.open, (current.stage.CLEAN, current.ROM))
    ja, en = (rom.read_file(current.stage.ARM) for rom in (clean, active))
    earlier_release = base.load(prior.current.RELEASE)
    assert sha(en) == release['target_ARM9_sha256'] == earlier_release['target_ARM9_sha256']
    assert all(ja[a:b] == en[a:b] for a, b in LOCKS)
    a, b = map(route_cases, (ja, en))
    assert a['categories'] == b['categories'] and a['guide_motion'] == b['guide_motion']
    assert len(b['guide_motion']) == 26 and len(b['guide_draws']) == 13 and len(b['extras']) == 7
    earlier = base.load(prior.OUTPUT)
    historical_menu = earlier['carried_forward_observed_menu_pages']
    pointers = {row['current_pointer']: row['current_text_sha256'] for row in historical_menu}
    assert len(pointers) == 19
    for row in b['guide_draws'] + b['extras'][:-1]:
        assert sha(bytes.fromhex(row['exact_null_terminated_hex'])) == pointers[row['pointer']]

    src_common, common = (rom.read_file(current.stage.COMMON) for rom in (clean, active))
    source = common_message_entries(src_common, ja)
    stored = owned_entries(common, en, sha(en[DIRECTORY_OFFSET:TABLE_OFFSET]))
    old_rows = {r['message_ID']: r for r in earlier['records'] if r['message_ID'] in IDS}
    assert old_rows.keys() == IDS
    rows = []
    for n, row in sorted(old_rows.items()):
        assert source[n].text == stored[n].text == bytes.fromhex(row['stored_hex'])
        assert reference(source[n]) == row['source_reference']
        rows.append(dict(message_ID=n, source_reference=reference(source[n]), current_reference=reference(stored[n]),
                         exact_stored_sha256=sha(stored[n].text), editorial_work=row['editorial_work'],
                         wording_decision=row['wording_decision'], review_gates=row['review_gates'],
                         active_menu_owner=row['independent_display_evidence'],
                         stored_record_requested_by_these_selectors=False, other_caller_classification='open'))

    ledger = base.load(base.LEDGER)
    pending = ledger['pending_shared_consumer_checkpoint_20261114']
    assert pending['candidate_sha256'] == release['candidate_sha256'] and pending['remaining_total'] == 276
    base.save(OUTPUT, dict(candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        candidate_COMMON_sha256=sha(common), parent_native_span_locks=[dict(start=a, end=b, sha256=sha(en[a:b])) for a, b in LOCKS],
        clean_routing=a, current_routing=b, records=rows, earlier_actual_pages=historical_menu,
        original_text_renderer_entry=DRAW, supplied_graphics_context_and_draw_support=True,
        new_gameplay_runs=0, new_editorial_credit=0, remaining_shared_keys=pending['remaining_total'],
        other_possible_stored_consumers_open=True, full_goal_complete=False,
        evidence={str(path): base.digest(path) for path in (current.RELEASE, prior.OUTPUT, prior.ONLINE, Path(__file__))}))
    print('Verified 13 Online text draws, 26 guide moves and six About Extras text draws and exit in both ROMs.')


if __name__ == '__main__':
    main()
