"""Reproduce inherited full-wrapper controls for the optimized existing filter."""

from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.probe_button_prompt_native import BASE, machine
from scripts.verify_village_wrap_v608 import save


def main():
    old = NdsImage.open('out/all_routes_combined_v750_candidate.nds').read_file('/__arm9__.bin')
    new = NdsImage.open('out/all_routes_combined_v751_candidate.nds').read_file('/__arm9__.bin')
    section = next(s for s in MainCodeFile(old, BASE).sections if s.ramAddress <= 0x01FF9EDC < s.ramAddress + len(s.data))
    offset = 0x01FF9EDC - section.ramAddress
    entry = bytes(section.data[offset:offset + 52])
    # Unconditional load into r3 precedes the entry's first use of that register.
    assert entry[:8] == bytes.fromhex('64c29de5d8309fe5')
    old_cpu, new_cpu = machine(old), machine(new)
    for arm, cpu in ((old, old_cpu), (new, new_cpu)):
        cpu.mem_write(0x02387A20, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    cases = []
    for i in (*range(457, 481), 801):
        raw = b' Inherited copy and layout behavior stays identical.'
        a = native_layout(old_cpu, raw, i, ())
        b = native_layout(new_cpu, raw, i, ())
        assert a == b
        cases.append({'id': i, 'complete_wrapped_output_and_guards_equal': True, 'formatted_hex': a[0].hex()})
    save('work/analysis/town_responses_v751/legacy_filter_equivalence.json', {
        'source_ARM9_sha256': sha(old), 'target_ARM9_sha256': sha(new),
        'original24_range_plus801_native_complete_output_controls': cases,
        'original_copy_entry_address': 0x01FF9EDC, 'original_copy_entry52_hex': entry.hex(),
        'why': 'The optimized early457-480 branch leaves caller-clobbered r3 as the original ID; the original copy entry overwrites r3 with its internal constant before input use. Other fallback r3 transformation is preserved.',
        'scope_is25_supplied_plaintext_controls_not_all_legacy_translation_variants': True,
        'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('25 inherited full-wrapper controls and original r3 overwrite contract pass.', flush=True)


if __name__ == '__main__':
    main()
