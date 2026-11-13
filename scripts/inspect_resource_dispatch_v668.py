"""Locate the pinned interpreter's complete original ARM opcode tables."""

import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA, SOURCE
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/resource_dispatch_v668')
ROM = Path('out/all_routes_combined_v666_candidate.nds')


def tables(raw):
    pe = struct.unpack_from('<I', raw, 60)[0]
    base = struct.unpack_from('<Q', raw, pe + 24 + 24)[0]
    size = struct.unpack_from('<H', raw, pe + 20)[0]
    sections = []
    for i in range(struct.unpack_from('<H', raw, pe + 6)[0]):
        at = pe + 24 + size + i * 40
        virtual_size, rva, file_size, offset = struct.unpack_from('<4I', raw, at + 8)
        flags = struct.unpack_from('<I', raw, at + 36)[0]
        sections.append((rva, virtual_size, offset, file_size, flags))

    def va(at):
        return next(base + rva + at - offset for rva, _, offset, count, _ in sections
                    if offset <= at < offset + count)

    def executable(pointer):
        return any(base + rva <= pointer < base + rva + count and flags & 0x20000000
                   for rva, count, _, _, flags in sections)

    # Source indices A00..AFF select B, B00..BFF select BL. Each complete
    # 256-entry family has one handler in each of the two adjacent CPU tables.
    runs, at = [], 0
    while at + 2048 <= len(raw):
        pointer = struct.unpack_from('<Q', raw, at)[0]
        if executable(pointer) and raw[at:at + 2048] == raw[at:at + 8] * 256:
            runs.append(at)
            at += 2048
        else:
            at += 8
    found = []
    for at in runs:
        start = at - 0xA00 * 8
        if start < 0 or start + 8192 * 8 > len(raw):
            continue
        values = struct.unpack_from('<8192Q', raw, start)
        if (all(executable(p) for p in values)
                and all(len(set(values[table * 4096 + family:table * 4096 + family + 256])) == 1
                        for table in (0, 1) for family in (0xA00, 0xB00))
                and values[0xA00] != values[0xB00]
                and values[0xA00] != values[4096 + 0xA00]):
            found.append({'file_offset': start, 'source_VA': va(start), 'RVA': va(start) - base,
                'ARM9_B_handler_RVA': values[0xA00] - base,
                'ARM9_BL_handler_RVA': values[0xB00] - base,
                'all8192_function_pointers_executable': True,
                'table_sha256': sha(raw[start:start + 8192 * 8])})
    assert len(found) == 1, found
    return base, found[0]


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    if not (ROOT / 'preflight.json').exists():
        frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
        save(ROOT / 'preflight.json', {
            'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
            'release_hashes': {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
                ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'),
                Path('out/raphael_natural_v2_accepted_base.nds'))},
            'previous_goal_turn_classification': 'progress: V667 actual Maria Karibib native Town, four terminal attempts and archive',
            'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen}})
    raw = CORE.read_bytes()
    assert sha(raw) == CORE_SHA
    base, table = tables(raw)
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    instruction = struct.unpack_from('<I', arm, 0xD6558)[0]
    assert arm[0xD6558:0xD6720] == NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')[0xD6558:0xD6720]
    index = ((instruction >> 16) & 0xFF0) | ((instruction >> 4) & 15)
    pointer = struct.unpack_from('<Q', raw, table['file_offset'] + index * 8)[0]
    save(ROOT / 'interpreter_table_source.json', {'core': str(CORE), 'core_SHA256': CORE_SHA,
        'source_commit': '95b4d798731caa809125b6c3c11d17cc332ff6ef',
        'source_files': {str(SOURCE / p): sha((SOURCE / p).read_bytes())
            for p in ('armcpu.h', 'armcpu.cpp', 'instructions.h', 'instruction_tabdef.inc', 'saves.cpp')},
        'interpreter_table': table, 'game_resource_getter': 0x020D6558,
        'source_original_first_instruction': instruction, 'source_instruction_index': index,
        'selected_ARM9_handler_RVA': pointer - base,
        'no_native_observer_or_new_gameplay_credit_yet': True, 'full_goal_complete': False})
    print(table, 'resource getter first instruction:', hex(instruction), 'index:', hex(index),
          'handler RVA:', hex(pointer - base))


if __name__ == '__main__':
    main()
