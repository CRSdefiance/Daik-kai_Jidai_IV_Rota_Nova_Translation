"""Exercise the complete bounded modal dispatcher and native whole-word raster."""

from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.captain_prompt_wrap import transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import machine
from scripts.probe_regional_policy_wrap_v616 import run
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/captain_prompt_wrap_v651')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open('out/all_routes_combined_v640_candidate.nds')
    source = rom.read_file('/__arm9__.bin')
    target, proof = transform(source)
    old, new = machine(source), machine(target)
    for u, data in ((old, source), (new, target)):
        u.mem_write(POOL, bytes(MainCodeFile(data, 0x02000000).sections[3].data[:-48]))
    text = 'These instructions contain several complete words and preserve every leading and final character.'
    changed, unchanged = [], 0
    for number in range(3668):
        a, aw = run(old, 0x020546E8, number, text)
        b, bw = run(new, 0x020546E8, number, text)
        if 269 <= number <= 272:
            assert not aw and bw and a != b
            assert b' '.join(b.split()) == text.encode('ascii')
            changed.append(number)
        else:
            assert (a, aw) == (b, bw), number
            unchanged += 1
    controls = []
    for parent in (0x0205469C, 0x02054720, 0x02054764, 0x02054014):
        for number in (*range(267, 275), 127, 134, 321, 327):
            assert run(old, parent, number, text) == run(new, parent, number, text)
            controls.append({'parent': parent, 'native_ID': number, 'byte_exact_old_behavior': True})
    entries = common_message_entries(rom.read_file('/COMMON/MESFILE.DK4'), source, clean=False)
    rows = []
    for number in range(269, 273):
        text = entries[number].text.decode('ascii')
        prepared, wrapped = run(new, 0x020546E8, number, text)
        assert wrapped and b' '.join(prepared.split()) == text.encode('ascii')
        glyph_events = []
        indices = raster(target, prepared, 0x01FFCE40 - 0x02000000,
                         size=(228, 48), instruction_limit=400000, glyph_events=glyph_events)
        visible = [g for g in glyph_events if g['code'] != 32]
        assert [g['code'] for g in visible] == [ord(c) for c in text if c != ' ']
        at = 0
        for word in text.split():
            group = visible[at:at + len(word)]
            assert len({g['y'] for g in group}) == 1, (number, word, group)
            at += len(word)
        rows.append({'native_ID': number, 'unchanged_English': text, 'prepared': prepared.decode('ascii'),
                     'complete_native_glyph_order_and_every_word_single_row': True,
                     'native_ink_points': sum(bool(p) for p in indices),
                     'raster_source_and_output_guards_and_ABI_pass': True})
    # Empty/oversized helper-failure cases preserve the original bounded wrapper behavior.
    failures = []
    for text in ('', 'A' * 237, ' '.join(['Extraordinary'] * 25)):
        for number in (127, 321, 327):
            assert run(old, 0x020546E8, number, text) == run(new, 0x020546E8, number, text)
            failures.append({'native_ID': number, 'text_length': len(text), 'old_behavior_exact': True})
    (ROOT / 'research_ARM9.bin').write_bytes(target)
    save(ROOT / 'native_dispatch_proof.json', {'transform': proof,
        'all3668_native_IDs_exercised': True, 'added_exact_scope': changed,
        'unrelated_IDs_byte_exact': unchanged, 'other_parent_controls': controls,
        'existing_wrapper_empty_and_failure_controls': failures,
        'four_complete_native_instruction_rasters': rows,
        'script_sha256': sha(Path(__file__).read_bytes()),
        'actual_emulator_repaired_pixels_pending': True, 'full_goal_complete': False})
    save('translations/captain_prompt_wrap_v1.json', {'format': 'dk4-captain-prompt-wrap-v1', 'proof': proof})
    print('V651 native dispatch:exactly4 added IDs;3664 unchanged;48 wrong-parent controls;four whole-word rasters pass.')


if __name__ == '__main__':
    main()
