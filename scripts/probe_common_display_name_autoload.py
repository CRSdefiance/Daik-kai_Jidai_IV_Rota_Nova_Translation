"""Execute the real startup section copier for the extended research ARM9."""

import json
from pathlib import Path

import ndspy.code
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STOP, machine_for
from scripts.probe_common_display_name_hook import prepare


def execute(source):
    loaded = ndspy.code.MainCodeFile(source, BASE)
    sections = [section for section in loaded.sections if not section.implicit]
    machine = machine_for(source)
    machine.mem_map(0x01FF0000, 0x10000)
    machine.mem_write(0x01FF8000, b'\xa5' * 0x8000)
    machine.mem_write(0x027E0000, b'\xa5' * 0x4000)
    writes, hardware_operations = [], []

    def code(uc, address, size, _):
        if not BASE + 0x9E0 <= address < BASE + 0xA5C:
            raise ValueError('Startup copier executes outside mapped native body')
        if address in (BASE + 0xA34, BASE + 0xA38, BASE + 0xA3C):
            # Cache maintenance is a hardware contract; all loads/stores and
            # directory iteration execute unchanged, with no substitute copier.
            hardware_operations.append(address - BASE)
            uc.reg_write(UC_ARM_REG_PC, address + 4)

    def write(uc, access, address, size, value, _):
        if not any(section.ramAddress <= address
                   and address + size <= section.ramAddress + len(section.data) + section.bssSize
                   for section in sections):
            raise ValueError('Autoload writes outside declared sections')
        writes.append((address, size))

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(BASE + 0x9E0, STOP, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP:
        raise ValueError('Startup section copier did not return')
    checks = []
    for section in sections:
        expected = bytes(section.data) + b'\0' * section.bssSize
        actual = bytes(machine.mem_read(section.ramAddress, len(expected)))
        if actual != expected:
            raise ValueError('Actual autoload loses section bytes or BSS')
        checks.append({'ram_address': section.ramAddress, 'bytes': len(expected),
                       'sha256': sha(actual), 'complete_section_exact': True})
    resident = sections[0]
    tail = resident.ramAddress + len(resident.data) + resident.bssSize
    if bytes(machine.mem_read(tail, BASE - tail)) != b'\xa5' * (BASE - tail):
        raise ValueError('Resident copier changes overlay/gap bytes after section end')
    dtcm = sections[1]
    end = dtcm.ramAddress + len(dtcm.data) + dtcm.bssSize
    if bytes(machine.mem_read(end, 0x027E4000 - end)) != b'\xa5' * (0x027E4000 - end):
        raise ValueError('DTCM copier changes bytes after its declared section')
    return {'sections': checks, 'native_memory_writes': len(writes),
            'cache_operations_deferred': len(hardware_operations),
            'overlay_destination_untouched': True, 'dtcm_tail_untouched': True}


def main():
    old = NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')
    new, _ = prepare(old)
    report = {'status': 'pass-native-autoload-copy-hardware-cache-contract',
              'original_arm9_sha256': sha(old), 'research_arm9_sha256': sha(new),
              'original': execute(old), 'research': execute(new),
              'limitations': 'Runs actual 020009E0 startup section load/store/directory instructions. CP15 cache maintenance is skipped and remains a hardware contract. Full cold boot, overlay filesystem loading and game initialization are unproven; no playable ROM is built.'}
    Path('work/analysis/common_display_name_autoload_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('Original and extended ARM9 native autoload copies pass; overlay destinations remain untouched.')


if __name__ == '__main__':
    main()
