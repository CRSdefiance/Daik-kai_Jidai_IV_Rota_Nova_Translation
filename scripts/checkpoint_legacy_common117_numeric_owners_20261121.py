"""Classify direct numeric COMMON 117 leads without guessing a display owner."""

from hashlib import sha256
from pathlib import Path
from struct import iter_unpack, pack, unpack_from

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R5,
    UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R11, UC_ARM_REG_SP,
)

from scripts import register_final_early_wrap_leads_20261121 as parent
from scripts.checkpoint_pending_shared_native_20261115 import components
from scripts.probe_button_prompt_native import BASE, STACK, call, machine


stage, base = parent.stage, parent.base
OUTPUT = stage.CHECKPOINTS / 'legacy_common117_numeric_owners_20261121_v1.json'
STILL = 0x021158EC
POINT = 0x02119720
GRID = (0x02119F6C, 0x02119FA4, 0x02119FDC, 0x0211A014)
MOVS = (0x0204A670, 0x02066CB8, 0x02066FE0, 0x02071AB8, 0x0207A7F8)
TEXT_READERS = {0x0205528C, 0x020534F4}
CHECKSUM = Path('releases/all_routes_editorial_20261120_damaged_save_digits_candidate/verification/registered_review.json')
GALLERY = stage.CHECKPOINTS / 'shared_display_owners_20261119_v1.json'
LIMITED_CALL_SCAN = Path('work/analysis/native_common_extended_calls_clean.json')
REGISTER_FLOW = Path('work/current_amsterdam_square_20261114_v1/legacy_register_flow_exploration.json')
ITEM_CONTEXT = stage.CHECKPOINTS / 'figurehead_navigation_gift_advice_context_v2.json'
OBJ, INPUT = 0x02450000, 0x02450100


def inventory(rom):
    words, immediates, literal_loads, thumb_candidates = [], [], [], []
    for name, start, data in components(rom.rom):
        for i, (word,) in enumerate(iter_unpack('<I', data[:len(data) & ~3])):
            at = 4 * i
            pc = start + at
            if word == 117:
                words.append((name, pc))
            if word >> 28 == 15:
                continue
            if word & 0x0FEF0000 == 0x03A00000:
                shift, imm = 2 * ((word >> 8) & 15), word & 255
                if ((imm >> shift) | (imm << (32 - shift))) & 0xFFFFFFFF == 117:
                    immediates.append((name, pc, (word >> 12) & 15))
            if word & 0x0F7F0000 == 0x051F0000:
                relative = word & 0xFFF
                target = at + 8 + (relative if word & 0x800000 else -relative)
                if 0 <= target <= len(data) - 4 and unpack_from('<I', data, target) == (117,):
                    literal_loads.append((name, pc, start + target))
        for i, (half,) in enumerate(iter_unpack('<H', data[:len(data) & ~1])):
            if half & 0xF8FF == 0x2075:
                thumb_candidates.append((name, start + 2 * i, (half >> 8) & 7))
    return dict(aligned_words=words, ARM_mov_immediates=immediates, ARM_literal_loads=literal_loads,
                thumb_mov_halfword_matches=thumb_candidates)


def stopped(cpu, lo, hi, count=80):
    cpu.emu_start(lo, hi, count=count)
    assert cpu.reg_read(UC_ARM_REG_PC) == hi


def gallery(cpu):
    cpu.mem_write(OBJ, bytes(128))
    cpu.reg_write(UC_ARM_REG_R11, OBJ)
    stopped(cpu, 0x02042C74, 0x02042C94, 16)
    cpu.mem_write(OBJ + 0x1C, pack('<I', 2))
    cpu.reg_write(UC_ARM_REG_R5, 0)
    stopped(cpu, 0x02042E5C, 0x02042ED4, 32)
    assert cpu.reg_read(UC_ARM_REG_R9) == 39
    table, = unpack_from('<I', cpu.mem_read(OBJ + 0x14, 4))
    assert table == 0x021158CC and table + 8 * 4 == STILL
    cpu.reg_write(UC_ARM_REG_R7, 8)
    stopped(cpu, 0x02042F58, 0x02042F6C, 8)
    assert cpu.reg_read(UC_ARM_REG_R1) == 117
    args = cpu.reg_read(UC_ARM_REG_R0), cpu.reg_read(UC_ARM_REG_R1)
    results = []

    def boundary(u, pc, _size, _):
        if pc == 0x020D4170:
            assert u.reg_read(UC_ARM_REG_R0) == args[0]
            u.reg_write(UC_ARM_REG_R0, INPUT)
        else:
            assert u.reg_read(UC_ARM_REG_R0) == INPUT
            path = bytes(u.mem_read(u.reg_read(UC_ARM_REG_R1), 32)).split(b'\0')[0]
            results.append(path.decode('ascii'))
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    hooks = [cpu.hook_add(UC_HOOK_CODE, boundary, begin=pc, end=pc) for pc in (0x020D4170, 0x020B7158)]
    try:
        call(cpu, 0x28B74, args)
    finally:
        for hook in hooks:
            cpu.hook_del(hook)
    assert results == ['/evstill/evstill117.pxl']
    return dict(word=STILL, gallery_route_index=2, gallery_entry_index=8, native_filename=results[0],
                selection_call=0x02042F6C, original_filename_formatter=0x02028B74,
                CPU_canvas_and_file_loader_boundaries=True)


def graphics(cpu, arm):
    cpu.mem_map(0x04000000, 0x1000)
    table, register = unpack_from('<2I', arm, 0x67590)
    assert (table, register) == (0x0214563C, 0x0400048C)
    params, = unpack_from('<I', arm, table - BASE + 4 * 117)
    writes = []
    handle = cpu.hook_add(UC_HOOK_MEM_WRITE, lambda _, _access, at, size, value, _data: writes.append((at, size, value)),
                          begin=register, end=register + 3)
    outputs = []
    try:
        for pc in MOVS[1:3]:
            writes.clear()
            stopped(cpu, pc, pc + 8, 24)
            assert writes == [(register, 4, params), (register, 4, 0)]
            outputs.append(dict(instruction=pc, original_table_index=117, hardware_register=register, writes=list(writes)))
    finally:
        cpu.hook_del(handle)
    return outputs


def inventory_items(cpu):
    for requested, expected in ((2, 116), (3, 117), (4, 118)):
        call(cpu, 0x4A624, (requested,))
        assert cpu.reg_read(UC_ARM_REG_R0) == expected
        call(cpu, 0x4A6B0, (expected,))
        assert cpu.reg_read(UC_ARM_REG_R0) == requested
    outgoing = []
    for pc in MOVS[3:]:
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        stopped(cpu, pc - 4, pc + 8, 8)
        assert cpu.reg_read(UC_ARM_REG_R0) == 117
        stopped(cpu, 0x0204A810, 0x0204ABA4, 24)
        item_ids = cpu.reg_read(UC_ARM_REG_R0)
        assert bytes(cpu.mem_read(item_ids, 4)) == pack('<I', 117)
        assert cpu.reg_read(UC_ARM_REG_R1) == 1
        outgoing.append(dict(instruction=pc, item_card_entry=0x0204A810, native_items_argument=[117]))
    cpu.mem_write(OBJ + 0x40, pack('<I', INPUT))
    cpu.mem_write(OBJ + 0x48, pack('<I', 0))
    cpu.mem_write(INPUT, pack('<I', 117))
    call(cpu, 0xCB190, ())
    first = cpu.reg_read(UC_ARM_REG_R0) + 4
    call(cpu, 0x4B5A0, (OBJ,))
    item = cpu.reg_read(UC_ARM_REG_R0)
    assert item == first + 20 * 117
    call(cpu, 0x4A53C, (item,))
    name = bytes(cpu.mem_read(cpu.reg_read(UC_ARM_REG_R0), 128)).split(b'\0')[0].decode('cp932')
    return dict(figurehead_slot=3, item_index=117, original_name=name, item_object=item,
                checked_neighbors=[116, 118], direct_item_card_initializers=outgoing,
                original_item_id_to_record=0x0204B5A0, original_item_name_getter=0x0204A53C)


def layout_points(cpu, *, clean):
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_R5, 0x0211970C)
    cpu.reg_write(UC_ARM_REG_R8, 1)
    stopped(cpu, 0x0207FD20, 0x0207FD40)
    x, y = unpack_from('<2I', cpu.mem_read(STACK + 0x18, 8))
    assert (x, y) == (151 if clean else 174, 117) and 0x0211970C + 0x10 + 4 == POINT
    sprite = dict(word=POINT, original_loop=0x0207FD20, slot=1, coordinates=[x, y],
                  virtual_draw_call=0x0207FD54)
    rows = []
    for cell, expected_y in zip(GRID, (72, 92, 112, 132), strict=True):
        index = (cell - 0x02119F54) // 8
        assert 0x02119F54 + index * 8 == cell
        cpu.mem_write(OBJ, bytes(128))
        cpu.reg_write(UC_ARM_REG_R7, OBJ)
        cpu.reg_write(UC_ARM_REG_R8, OBJ)
        cpu.reg_write(UC_ARM_REG_R9, index)
        stopped(cpu, 0x020A02E8, 0x020A032C)
        x, y = unpack_from('<2I', cpu.mem_read(STACK + 0x20, 8))
        assert (x, y) == (117, expected_y)
        rows.append(dict(word=cell, grid_cell_index=index, coordinates=[x, y], original_reader=0x020A02E8))
    return dict(sprite_position=sprite, grid_positions=rows)


def check(image, *, clean):
    arm = image.read_file(stage.ARM)
    hits = inventory(image)
    established = [('ARM9 section 0', pc) for pc in (STILL, POINT, *GRID)]
    assert all(match in hits['aligned_words'] for match in established)
    extra_words = [match for match in hits['aligned_words'] if match not in established]
    if clean:
        assert not extra_words
    else:
        assert len(extra_words) == 6
    assert hits['ARM_mov_immediates'] == [('ARM9 section 0', pc, 0) for pc in MOVS]
    assert not hits['ARM_literal_loads']
    cpu = machine(arm)
    calls_to_lookup = []

    def reject_text_lookup(_, pc, _size, _data):
        calls_to_lookup.append(pc)
        raise AssertionError(f'Unexpected COMMON access at {pc:#x}')

    for pc in TEXT_READERS:
        cpu.hook_add(UC_HOOK_CODE, reject_text_lookup, begin=pc, end=pc)
    files = gallery(cpu)
    props = graphics(cpu, arm)
    items = inventory_items(cpu)
    coords = layout_points(cpu, clean=clean)
    assert not calls_to_lookup
    return dict(candidates=hits, additional_registered_word_matches=extra_words,
                gallery=files, graphics=props, items=items, layout=coords,
                observed_COMMON_calls=calls_to_lookup)


def main():
    assert not OUTPUT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(stage.CLEAN) == release['clean_input_sha256']
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    worklist = base.load(stage.PENDING)
    rows = {row['message_ID']: row for row in worklist['records'] if row['kind'] == 'legacy'}
    assert len(rows) == 31 and 117 in rows
    source, current = map(base.NdsImage.open, (stage.CLEAN, parent.ROM))
    assert sha256(current.read_file(stage.ARM)).hexdigest() == release['target_ARM9_sha256']
    result, installed = check(source, clean=True), check(current, clean=False)
    for method in ('gallery', 'graphics'):
        assert result[method] == installed[method]
    assert result['layout']['grid_positions'] == installed['layout']['grid_positions']
    assert result['items']['original_name'] != installed['items']['original_name']
    assert installed['items']['original_name'] == 'White Whale Figurehead'
    assert result['items'] | {'original_name': 'White Whale Figurehead'} == installed['items']
    assert base.load(CHECKSUM)['common_117_pending']
    sink = base.load(GALLERY)['legacy_save_diagnostic_sink']
    assert set(sink['common_getter_calls'].values()) == {111, 112}
    assert not any(r['native_id_constant'] == 117 for r in base.load(LIMITED_CALL_SCAN)['candidates'])
    draft_entry, = [r for r in base.load(ITEM_CONTEXT)['records'] if r['item_ID'] == 117]
    assert draft_entry['item_name'] == installed['items']['original_name']
    proof = dict(candidate_sha256=release['candidate_sha256'], source_sha256=release['clean_input_sha256'],
                 message_ID=117, legacy_record=rows[117], clean=result, registered=installed,
                 classification='Six aligned words and five ARM MOV sites from the clean ROM belong to graphics or items.',
                 scan_limit='Additional registered payload word matches and raw Thumb halfword matches are inventoried without assigning owners.',
                 previous_Continue_path='The displayed checksum failure uses its own ARM9 notice.',
                 other_COMMON_paths_remain_unverified=True, complete_display_owner_search=False,
                 revised_ROM=False, fresh_gameplay=False, new_editorial_credit=0,
                 evidence={str(p): base.digest(p) for p in (
                     parent.RELEASE, stage.PENDING, CHECKSUM, GALLERY, LIMITED_CALL_SCAN, REGISTER_FLOW, ITEM_CONTEXT, Path(__file__))})
    base.save(OUTPUT, proof)
    print('Six aligned words and five ARM MOV references to 117 classified on both ROMs. The COMMON notice owner remains unconfirmed.')


if __name__ == '__main__':
    main()

