"""Source ownership, original native expansion, and complete controlled glyphs.

These are targeted native function tests, not progressive scene/choice playback.
"""

import json
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.dialogue.codec import parse_markup, tokens_to_bytes
from dk4tool.dialogue.layout import format_markup
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.patch.screenshot_text_repairs import apply_release
from dk4tool.rom.nds import NdsImage
from scripts.audit_native_given_name_table import ordinary_getter
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_name_catalog_glyphs_v278 import HEIGHT, WIDTH, expected_pixels, raster
from scripts.verify_ordinary_name_fidelity_research import initialized

ROOT = Path('work/screenshot_text_repairs_20261022')
CONFIG = Path('translations/screenshot_text_repairs_20261022_release_v1.json')


def main():
    parent = NdsImage.open('out/all_routes_combined_v1594_candidate.nds')
    base = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    json.loads(CONFIG.read_text(encoding='utf-8'))
    old_arm, old_common = parent.read_file('/__arm9__.bin'), parent.read_file('/COMMON/MESFILE.DK4')
    proof = apply_release(parent, base, CONFIG)
    arm = parent.read_file('/__arm9__.bin')
    old_cpu, new_cpu = initialized(old_arm), initialized(arm)
    changed_names = []
    for index in range(207):
        names = []
        for data, current_cpu in ((old_arm, old_cpu), (arm, new_cpu)):
            pointer = ordinary_getter(data, index, current_cpu)
            names.append((pointer, bytes(current_cpu.mem_read(pointer, 96)).split(b'\0')[0]))
        assert names[0][0] == names[1][0]
        if names[0][1] != names[1][1]:
            changed_names.append({'index': index, 'pointer': names[0][0],
                                  'before_hex': names[0][1].hex(), 'after_hex': names[1][1].hex()})
    assert len(changed_names) == 1
    assert bytes.fromhex(changed_names[0]['before_hex']) == 'Ｆaticia'.encode('cp932')
    assert bytes.fromhex(changed_names[0]['after_hex']) == b'Faticia'
    # Every native message retains its start, copy extent and all unselected text.
    directory = json.loads(Path('translations/fatigue_status_editorial_release_v1.json').read_text())['directory_sha256']
    before = owned_entries(old_common, old_arm, directory)
    after = owned_entries(parent.read_file('/COMMON/MESFILE.DK4'), arm, directory)
    for a, b in zip(before, after, strict=True):
        assert (a.block, a.block_offset, a.copy_end) == (b.block, b.block_offset, b.copy_end)
        if a.message_id != 3667:
            assert a.text == b.text
    # Fail closed on an out-of-sequence application; the same repair cannot be reapplied.
    try:
        apply_release(parent, base, CONFIG)
    except ValueError as error:
        assert 'exact complete inherited stack' in str(error)
    else:
        raise AssertionError('Repeated application was accepted')
    cpu = machine(arm)
    cpu.mem_write(POOL, bytes(MainCodeFile(arm, 0x02000000).sections[3].data[:-48]))
    macro_cases = []
    rumor = b"I hear it's an enormous spear capable of driving evil away."
    for text in (b'Faticia', b'I hear it', b'Fine', b'I\nhear', rumor):
        src, dst = 0x02430020, 0x02431020
        cpu.mem_write(src - 16, b'\xA5' * 640)
        cpu.mem_write(src, text + b'\0')
        source = bytes(cpu.mem_read(src - 16, 640))
        cpu.mem_write(dst - 16, b'\xA5' * 544)
        call(cpu, 0x53914, (dst, src, 0))
        output = bytes(cpu.mem_read(dst, 512)).split(b'\0')[0]
        assert output == (b'\x96lhear' if text == b'I\nhear' else text)
        assert bytes(cpu.mem_read(src - 16, 640)) == source
        assert bytes(cpu.mem_read(dst - 16, 16)) == bytes(cpu.mem_read(dst + len(output) + 1, 16)) == b'\xA5' * 16
        macro_cases.append({'input_hex': text.hex(), 'output_hex': output.hex()})
    items = [('old I prefix', 'Ｉ hear'.encode('cp932')), ('new I prefix', b'I hear'),
             ('old name', 'Ｆaticia'.encode('cp932')), ('new name', b'Faticia')]
    for row in proof['changed_records']:
        if row['file_path'] == '/data/SC0.DK4':
            raw = bytes.fromhex(row['after_hex'])
            items.append((row['id'], raw[1:] if row['id'].endswith('0144') else raw))
    profile = get_dialogue_profile('raphael-story-live')
    formatted = format_markup(rumor.decode(), profile)
    text = tokens_to_bytes(parse_markup(formatted), guard_linebreaks=True,
                          pair_phase_safe_breaks=True, macro_ascii_lengths=profile.macro_ascii_lengths)
    items.append(('full spear rumor (controlled painter)', text))
    sheet = Image.new('RGB', (WIDTH * 4, 4 * (HEIGHT * 2 + 24)), '#333333')
    draw = ImageDraw.Draw(sheet)
    cases = []
    for n, (label, text) in enumerate(items):
        pixels, events, font = raster(arm, text)
        assert pixels == expected_pixels(arm, font, events)
        semantic = [('ascii', ord(c)) if len(c.encode('cp932')) == 1 else
                    ('cp932', int.from_bytes(c.encode('cp932'), 'big'))
                    for c in text.decode('cp932') if c not in ' \n']
        assert semantic == [(e['kind'], e['code']) for e in events if e['code'] != 32]
        image = Image.new('RGB', (WIDTH, HEIGHT))
        colors = {0: (239, 232, 201), 1: (0, 8, 0), 15: (98, 97, 98)}
        image.putdata([colors.get(v, (255, 0, 255)) for v in pixels])
        x, y = n % 2 * WIDTH * 2, n // 2 * (HEIGHT * 2 + 24)
        draw.text((x + 3, y + 3), label, fill='white')
        sheet.paste(image.resize((WIDTH * 2, HEIGHT * 2), Image.Resampling.NEAREST), (x, y + 24))
        cases.append({'label': label, 'text_hex': text.hex(), 'independent_complete_pixels_and_glyph_order': True,
                          'events': events})
    sheet.save(ROOT / 'native_before_after.png')
    candidate = Path('out/screenshot_text_repairs_20261022_candidate.nds')
    if candidate.exists():
        saved = NdsImage.open(candidate)
        assert dict(saved.iter_components()) == dict(parent.iter_components())
        assert list(saved.iter_files()) == list(parent.iter_files())
    result = {'scope': 'Original native initialization, name getters, expansion and controlled bitmap painting; progressive scene/choice playback unverified.',
                  'config_sha256': sha(CONFIG.read_bytes()), 'producer_sha256': sha(Path(__file__).read_bytes()),
                  'ARM9_sha256': sha(arm), 'macro_cases': macro_cases, 'native_glyph_cases': cases,
                  'all3668_native_copy_boundaries_and3667_other_texts_preserved': True,
                  'repeated_application_rejected': True, 'missing_prompt_transition_verified': False,
                  'all207_original_name_pointers_exact': True, 'only_changed_name': changed_names,
                  'hardware_tested': False}
    (ROOT / 'native_text_proof.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('PASS: 3668 message boundaries; five native expansion cases; seven complete native bitmap cases; buffer guards; repeat rejection.')


if __name__ == '__main__':
    main()
