"""Bound the remaining original image-opcode modes; no display credit.

Diagnostic operand streams execute the original dispatcher and cleanup. Valid
mode0 stops BEFORE the item-window constructor. Modes1/2 and invalid mode0 stop
before the common frame wait. The snapshot is an explicitly identified V724
research fixture, not an ordinary event reached by gameplay.
"""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, STOP, machine
from scripts.trace_control_aliases_v688 import sections
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/image_modes_v729')
ROM = Path('out/all_routes_combined_v712_candidate.nds')
SNAPSHOT = Path('work/emulation_v193/generic_inventory_v724_12/frame_003900_arm9_ram.bin')
REPORT = SNAPSHOT.parent / 'capture_report.json'
OWNER, STREAM, RESULT, LENGTH = 0x02470000, 0x02470100, 0x02470200, 0x02470220
WIDGET, CONSTRUCT, WAIT = 0x02279448, 0x0204A930, 0x02028A74
SDK = (0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08)
REGS = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'proof.json').exists()
    canonical = Path('out/raphael_natural_v2_accepted_base.nds')
    release = {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
        ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'), canonical)}
    assert release[str(ROM)] == '6534e5619673ea6bdffa3a2342622b99ef393bef52ef58cac131ee94ae0f4030'
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, old = (r.read_file('/__arm9__.bin') for r in (rom, clean))
    ranges = ((0x2A510, 0x2A5C0), (0x29AA0, 0x29AF8), (0x29FFC, 0x2A0F8),
              (0x28A64, 0x28A8C), (0x28E14, 0x29094), (0x4A930, 0x4AA88),
              (0xCB190, 0xCB19C))
    assert all(arm[lo:hi] == old[lo:hi] for lo, hi in ranges)
    raw, capture = SNAPSHOT.read_bytes(), read(REPORT)
    assert len(raw) == 0x400000 and capture['cold_boot'] and not capture['savestate_loaded']
    ram_row = next(r for r in capture['read_only_capture_RAM_snapshots'] if r['frame'] == 3900)
    assert ram_row['sha256'] == sha(raw)
    fixture = Path(capture['ROM'])
    assert sha(fixture.read_bytes()) == capture['ROM_sha256']
    preparation = read('work/analysis/generic_inventory_v724/proof.json')
    assert preparation['candidate_sha256'] == release[str(ROM)]
    parts = sections(rom)
    u = machine(arm)
    executed, source_bytes, events = set(), {}, []

    def hook(cpu, address, size, unused):
        executed.add(address)
        actual = bytes(cpu.mem_read(address, size))
        sources = [(label, data[address - base:address - base + size])
            for label, base, data in parts if base <= address and address + size <= base + len(data)]
        assert any(expected == actual for _, expected in sources), hex(address)
        previous = source_bytes.setdefault(address, actual)
        assert actual == previous
        if address in SDK or address in (0x020470B4, 0x020E5650):
            raise AssertionError(f'Unexpected image loader, SDK access or source assert: {address:#x}')
        if address in (0x02028E14, CONSTRUCT):
            events.append({'PC': address, 'args': [cpu.reg_read(r) for r in REGS]})
        if address == CONSTRUCT:
            cpu.emu_stop()

    handle = u.hook_add(UC_HOOK_CODE, hook)
    cases = []
    try:
        for kind in (0, 1, 2):
            for short in (True, False):
                for index in range(256):
                    u.mem_write(BASE, raw)
                    events.clear()
                    operand = (0x8000 if short else 0) | kind << 8 | index
                    source = struct.pack('<2H', 0x4800, operand)
                    if not short:
                        source += struct.pack('<2H', 0x12, 0x34)
                    u.mem_write(OWNER - 16, b'\xA5' * 64)
                    u.mem_write(OWNER, struct.pack('<4I', 0, STREAM, 0, 0))
                    u.mem_write(STREAM - 16, b'\xA5' * 48)
                    u.mem_write(STREAM, source)
                    u.mem_write(RESULT - 16, b'\xA5' * 80)
                    u.mem_write(LENGTH, bytes(4))
                    for reg, value in zip(REGS, (RESULT, OWNER, LENGTH, 0)):
                        u.reg_write(reg, value)
                    u.reg_write(UC_ARM_REG_SP, STACK)
                    u.reg_write(UC_ARM_REG_LR, STOP)
                    u.emu_start(BASE + 0x2A510, WAIT, count=200000)
                    constructor = kind == 0 and index < 218
                    assert u.reg_read(UC_ARM_REG_PC) == (CONSTRUCT if constructor else WAIT)
                    assert struct.unpack('<I', u.mem_read(LENGTH, 4))[0] == len(source)
                    assert len(events) == (2 if constructor else 1)
                    assert events[0]['PC'] == 0x02028E14 and events[0]['args'][0] == WIDGET
                    if constructor:
                        assert events[1] == {'PC': CONSTRUCT, 'args': [WIDGET + 0x84, index, 101, 0]}
                    fields = struct.unpack('<4I', u.mem_read(WIDGET, 16))
                    assert fields[1:] == (kind, index, 0)
                    assert bytes(u.mem_read(STREAM, len(source))) == source
                    for address, length in ((STREAM - 16, 16), (STREAM + len(source), 16),
                                            (OWNER - 16, 16), (RESULT - 16, 48), (LENGTH + 4, 28)):
                        assert bytes(u.mem_read(address, length)) == b'\xA5' * length
                    assert bytes(u.mem_read(OWNER, 16)) == struct.pack('<4I', 0, STREAM, 0, 0)
                    cases.append({'mode': kind, 'index': index, 'short_form': short,
                        'instruction_hex': source.hex(), 'decoded_length': len(source),
                        'events': list(events), 'stop_PC': u.reg_read(UC_ARM_REG_PC),
                        'widget_type_index_and_cleared_child': list(fields[1:]),
                        'whole_operand_and_neighbor_guards_exact': True})
                print(f'Mode{kind} {"short" if short else "long"}:256 original selector cases pass.', flush=True)
    finally:
        u.hook_del(handle)
    assert len(cases) == 1536
    assert sum(c['stop_PC'] == CONSTRUCT for c in cases) == 436
    assert sum(c['mode'] in (1, 2) for c in cases) == 1024
    assert sum(c['mode'] == 0 and c['stop_PC'] == WAIT for c in cases) == 76
    save(ROOT / 'cases.json', {'cases': cases})
    save(ROOT / 'executed_source.json', {'instructions': [
        {'address': a, 'bytes_hex': source_bytes[a].hex()} for a in sorted(executed)]})
    # Original constructor call sites identify its item-store formatter/resource
    # path. This is classification, not completion of that constructor or display.
    assert arm[0x4A9A4:0x4A9A8] == bytes.fromhex('91 0e 00 eb')
    assert struct.unpack_from('<I', arm, 0xCB198)[0] == 0x022D322C
    proof = {'status': 'pass-scoped-original-selector-and-cleanup',
        'candidate': str(ROM), 'candidate_sha256': release[str(ROM)],
        'snapshot': str(SNAPSHOT), 'snapshot_sha256': sha(raw),
        'capture_report': str(REPORT), 'capture_report_sha256': sha(REPORT.read_bytes()),
        'snapshot_source_is_V724_research_command_fixture': True,
        'snapshot_fixture_ROM_sha256': capture['ROM_sha256'],
        'original_source_exact_ranges': [list(r) for r in ranges],
        'all_executed_instructions_match_current_registered_sections': True,
        'executed_instruction_count': len(executed), 'cases': 1536,
        'mode1_2_cleanup_then_no_child_cases': 1024,
        'mode0_valid0_through217_item_constructor_boundary_cases': 436,
        'mode0_218_through255_no_child_cases': 76,
        'mode0_constructor_args': ['widget+0x84', 'index', 101, 0],
        'mode0_family_source': {'constructor': CONSTRUCT, 'item_formatter_call': 0x0204A9A4,
            'item_formatter': 0x0204E3F0, 'item_store_getter': 0x020CB190,
            'item_store': 0x022D322C, 'item_resource_helper': 0x020477B8},
        'SDK_or_loose_image_loader_calls': 0,
        'cases_file_sha256': sha((ROOT / 'cases.json').read_bytes()),
        'executed_source_sha256': sha((ROOT / 'executed_source.json').read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()),
        'exploratory_full_item_constructor_not_credited': {
            'result': 'Standalone continuation reached unmapped fetch PC E5802000 after item-store getter.',
            'scope': 'Incomplete standalone model; no ROM defect, complete constructor or GPU claim.'},
        'mode3_existing_V538_V724_evidence_not_rerun': True,
        'frame_wait_flags_geometry_import_GPU_ordinary_parent_or_global_unused_proven': False,
        'ROM_modified': False, 'release_hashes_unchanged': release, 'full_goal_complete': False}
    assert SNAPSHOT.read_bytes() == raw
    for path, digest in release.items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'proof.json', proof)
    print('All1536 selectors pass; modes1/2 have no child; mode0 selects item window, not comic loader. No display closure.')


if __name__ == '__main__':
    main()
