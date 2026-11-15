"""Bind original actor/table selection to actual duel bitmap and RGB holds."""
import struct
from pathlib import Path
from PIL import Image
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.duel_postmacro_layout_v1134 import layout
from scripts.probe_duel_compiled_fonts_v1136c import expected_plane
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_actual_holds_v1171')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_contact_v1169_1166_compassAttack8')
ROM = Path('out/all_routes_combined_v1166_candidate.nds')
BASE = 0x02000000


def actual_widget(raw):
    candidates = []
    header = raw.find(struct.pack('<3I', 4, 52, 36))
    while header >= 0:
        h = struct.unpack_from('<5I', raw, header)
        pos = raw.find(struct.pack('<I', BASE+header))
        while pos >= 0:
            view = pos-16
            widget = view-0x3C
            if widget >= 0 and struct.unpack_from('<4i', raw, widget+32) == (52, 16, 204, 80) and struct.unpack_from('<2I', raw, view+40) == (208, 36):
                candidates.append((BASE+widget, BASE+widget-0x214, BASE+header, h))
            pos = raw.find(struct.pack('<I', BASE+header), pos+1)
        header = raw.find(struct.pack('<3I', 4, 52, 36), header+1)
    assert len(candidates) == 1
    return candidates[0]


def main():
    assert not ROOT.exists()
    rom = NdsImage.open(ROM)
    digest = sha(ROM.read_bytes())
    assert digest == read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    arm, font, kanji = rom.read_file('/__arm9__.bin'), GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin')), rom.read_file('/GRP/KANJI.FNT')
    records = {r['message_id']: r for r in read('translations/duel_editorial_manuscript_v4.json')['records']}
    cases = []
    ink_color = None
    for number, side, table, frames in ((1932, 0, 0x02117340, (5782, 5792)),
                                        (1939, 1, 0x02117360, (5902, 5912))):
        for frame in frames:
            raw_path, image_path = CAP/f'frame_{frame:06d}_arm9_ram.bin', CAP/f'frame_{frame:06d}_navigation.png'
            raw = raw_path.read_bytes()
            image = Image.open(image_path).convert('RGB')
            widget, controller, header, h = actual_widget(raw)
            assert h[:3] == (4, 52, 36) and h[4] == 40
            cpu, get = get_machine(arm, raw)
            actors = list(struct.unpack('<2I', cpu.mem_read(controller+0x34, 8)))
            actor_IDs = [get(0x7EE08, actor) for actor in actors]
            assert actor_IDs == [1, 32]
            assert get(0x53F4C, actors[side], table) == number
            text = records[number]['english'].encode('ascii')
            name = None
            if b'%s' in text:
                other = actors[1-side]
                other_ID = get(0x7EE08, other)
                vtable = struct.unpack('<I', cpu.mem_read(other, 4))[0]
                offset = 0x24 if 28 <= other_ID < 44 else 0x20
                getter = struct.unpack('<I', cpu.mem_read(vtable+offset, 4))[0]
                pointer = get(getter-BASE, other)
                name = bytes(cpu.mem_read(pointer, 64)).split(b'\0')[0]
                text = text.replace(b'%s', name)
            output, lines = layout(text)
            expected, letters = expected_plane(arm, kanji, font, lines)
            at = header-BASE+h[4]
            packed = raw[at:at+3744]
            native = bytes((v >> shift) & 15 for v in packed for shift in (0, 4))
            assert native == bytes(expected)
            actual_colors = {image.getpixel((56+x, 212+row*20+y)) for row in range(3)
                for y in range(12) for x in range(144) if native[(row*12+y)*208+x]}
            assert len(actual_colors) == 1
            if ink_color is None:
                ink_color = next(iter(actual_colors))
            assert actual_colors == {ink_color} and max(ink_color) < 32
            # Positions are original widget/crop geometry, never fit to letters.
            # Calibrate the displayed ink color only; shape and blank pixels are
            # independently predicted from original source-font bitmaps.
            for row in range(3):
                for y in range(12):
                    for x in range(144):
                        value = native[(row*12+y)*208+x]
                        assert value in (0, 15)
                        assert image.getpixel((56+x, 212+row*20+y)) == (ink_color if value else (255, 255, 255))
            source_ink = sum(bool(v) for v in native)
            visible_ink = sum(bool(native[y*208+x]) for y in range(36) for x in range(144))
            assert source_ink == visible_ink
            cases.append({'message_ID': number, 'frame': frame, 'side': side, 'original_table': table,
                'source_actor_IDs': actor_IDs, 'original_speaker_ID': actor_IDs[side],
                'original_name_hex': name.hex() if name else None, 'expanded_text': text.decode('cp932'),
                'lines': lines, 'source_widget': widget, 'source_controller': controller, 'source_bitmap_header': header,
                'RAM_path': str(raw_path), 'RAM_sha256': sha(raw), 'capture': str(image_path),
                'capture_sha256': sha(image_path.read_bytes()), 'whole208x36_font_plane_sha256': sha(native),
                'full_original_font_plane_and_all_three144x12_RGB_ink_and_blank_masks_exact': True,
                'original_x56_y212_232_252_positions_not_derived_from_glyphs': True,
                'complete_first_last_letters_no_native_crop_ink_loss': True,
                'current_COMMON_carrier1931_does_not_identify_actual_selected_voice': True})
    ROOT.mkdir(parents=True)
    save(ROOT/'original_challenge_acceptance_holds.json', {'candidate': str(ROM), 'candidate_sha256': digest,
        'cases': cases, 'displayed_ink_color_calibrated_only_not_an_independent_palette_decode': list(ink_color),
        'actual_original_challenge1932_and_acceptance1939_two_full_holds_each': True,
        'actual_cache_resident_component_runs_under_original_emulator_not_a_CPU_boundary': True,
        'no_fixtures_after5770_original_duel_trigger_observed5772': True,
        'original_portrait_layout_and_actor_positions_not_reinterpreted_as_speaker_order': True,
        'emulator_currently_paused_pending_original_outcome_and_transitions': True,
        'terminal_fixture_replay_and_source_save_preservation_still_pending': True,
        'no_batch_or_goal_completion_credit': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Actual1932/1939: four complete native font planes and all three crop RGB/blank masks pass; source voices1/32 bound.', flush=True)


if __name__ == '__main__':
    main()
