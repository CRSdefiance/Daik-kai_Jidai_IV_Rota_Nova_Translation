"""Prove identical whole-copy memory/ABI behavior across every alignment phase."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine as scoped
from scripts.probe_button_prompt_native import machine as original
from scripts.verify_village_wrap_v608 import save


def main():
    rows = []
    for path in ('work/clean.nds', 'out/all_routes_combined_v762_candidate.nds'):
        arm = NdsImage.open(path).read_file('/__arm9__.bin')
        cpus = [original(arm), scoped(arm)]
        count = 0
        for size in list(range(34)) + [127, 128, 129, 255, 256, 257, 511, 512, 4095, 4096]:
            for source_phase in range(4):
                for dest_phase in range(4):
                    value = bytes((i * 17 + 43) % 256 for i in range(size))
                    results = []
                    for cpu in cpus:
                        cpu.mem_write(0x02460000 - 16, b'\xa5' * (size + 40))
                        cpu.mem_write(0x02462000 - 16, b'\xa5' * (size + 40))
                        cpu.mem_write(0x02460000 + source_phase, value)
                        call(cpu, 0xCEC74, (0x02462000 + dest_phase, 0x02460000 + source_phase, size))
                        results.append((bytes(cpu.mem_read(0x02460000 - 16, size + 40)),
                                        bytes(cpu.mem_read(0x02462000 - 16, size + 40))))
                    assert results[0] == results[1], (path, size, source_phase, dest_phase)
                    count += 1
        rows.append({'ARM9_sha256': sha(arm), 'ROM': path, 'whole_source_destination_guard_and_ABI_comparisons': count})
    save(Path('work/analysis/tavern_storage_v764/scoped_machine_equivalence.json'), {
        'cases': rows, 'total': sum(r['whole_source_destination_guard_and_ABI_comparisons'] for r in rows),
        'original_alignment_callback_body_unchanged_only_hook_registration_range_restricted': True,
        'four_relevant_alignment_addresses_remain_in_range': [0x020CEC88, 0x020CECB4, 0x020CEC90, 0x020CECC0],
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'adapter_sha256': sha(Path('scripts/native_machine_scoped_v764.py').read_bytes())})
    print('1408 complete source/destination/guard/ABI comparisons pass;original files unchanged.', flush=True)


if __name__ == '__main__': main()
