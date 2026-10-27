"""Source-locked artwork names and actual native complete caption glyphs.

Research only: append corrected strings to the existing owned pool; retain all
historical release dependencies. No playable ROM or profile is generated.
"""

import json
import re
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, machine
from scripts.probe_common_display_name_hook import branch_link
from scripts.research_online_loader_v190 import resource_call as call
from scripts.verify_ordinary_name_fidelity_research import initialized

ROOT = Path('work/analysis/artwork_name_captions_v283')
ROM = Path('out/all_routes_combined_v275_candidate.nds')
SOURCE_SHA = '5d152c714ab1218e9f3df796c6dfc7c3e58f2ae0fff12cb45c76932605962db0'
NAMES = {'Raphael': 'Rafael', 'Kamil': 'Camille'}


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def raster(arm, pointer, text, x, y, tracking):
    cpu = machine(arm)
    cpu.mem_write(POOL, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    header, view, context = 0x02450000, 0x0245A000, 0x0245B000
    size = 256 * 192 // 2
    raw_header = struct.pack('<5I', 4, 64, 192, 0x0245C000 - header, 20)
    cpu.mem_write(header - 16, b'\xA5' * (size + 52))
    cpu.mem_write(header, raw_header + bytes(size))
    call(cpu, 0xD3D80, (view,))
    cpu.mem_write(STACK, struct.pack('<4I', 256, 192, 0, 0))
    call(cpu, 0xD3AFC, (view, header, 0, 0))
    metrics = struct.unpack_from('<I', arm, 0xD5088)[0]
    cpu.mem_write(metrics + 4, struct.pack('<2I', 6, 16))
    call(cpu, 0xD5160, (context, view, 1))
    cpu.mem_write(context + 28, struct.pack('<i', tracking))
    cpu.mem_write(context + 36, struct.pack('<2I', x, y))
    before = bytes(cpu.mem_read(pointer, len(text) + 1))
    assert before == text.encode('ascii') + b'\0'
    events = []

    def observe(uc, address, size, _):
        if address == BASE + 0xD16B4:
            code, style = struct.unpack('<2I', uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 8))
            events.append((code, style, uc.reg_read(UC_ARM_REG_R2), uc.reg_read(UC_ARM_REG_R3)))

    cpu.hook_add(UC_HOOK_CODE, observe)
    call(cpu, 0xD5404, (context, pointer))
    assert cpu.reg_read(UC_ARM_REG_R0) == pointer + len(text)
    assert bytes(cpu.mem_read(pointer, len(text) + 1)) == before
    assert bytes(cpu.mem_read(header, 20)) == raw_header
    assert bytes(cpu.mem_read(header - 16, 16)) == bytes(cpu.mem_read(header + 20 + size, 16)) == b'\xA5' * 16
    advance = 6 + tracking
    assert [(c, xx, yy) for c, _, xx, yy in events if c != 32] == [
        (ord(c), x + n * advance, y) for n, c in enumerate(text) if c != ' ']
    expected = bytearray(256 * 192)
    font = GameAsciiFont.from_arm9(arm)
    for code, style, xx, yy in events:
        if code == 32:
            continue
        assert 0 <= xx <= 250 and 0 <= yy <= 181
        glyph = font.decode(chr(code))
        for gy in range(11):
            for gx in range(6):
                if glyph.getpixel((gx, gy)):
                    expected[(yy + gy) * 256 + xx + gx] = style
    actual = bytes(n for b in cpu.mem_read(header + 20, size) for n in (b & 15, b >> 4))
    assert actual == expected
    return actual, sum(bool(p) for p in actual)


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    image = NdsImage.open(ROM)
    arm = image.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert sha(arm) == SOURCE_SHA and cache_plan(arm)
    code = MainCodeFile(arm, BASE)
    before = [bytes(s.data) for s in code.sections]
    packed = bytearray(before[3][:-48])
    stored, records = {}, []
    for kind, path in [('scene', 'translations/scene_caption_manuscript_v2.json'),
                       ('gallery', 'translations/gallery_description_manuscript_v1.json')]:
        for row in read(path)['records']:
            old = row['english']
            if not re.search(r'\b(?:Raphael|Kamil)\b', old):
                continue
            text = re.sub(r'\b(?:Raphael|Kamil)\b', lambda m: NAMES[m[0]], old)
            field = row['pointer_field'] if kind == 'scene' else row['source_fields'][0]['field']
            if kind == 'scene':
                assert clean[row['source_offset']:clean.index(0, row['source_offset'])].hex() == row['source_hex']
            else:
                source = row['source_fields'][0]
                at = source['source_pointer'] - BASE
                assert clean[at:clean.index(0, at)].hex() == source['source_hex']
            pointer = struct.unpack_from('<I', arm, field)[0]
            original = bytes(packed[pointer - POOL:]).split(b'\0', 1)[0] if pointer >= POOL else arm[pointer - BASE:arm.index(0, pointer - BASE)]
            assert original.rstrip(b' ') == old.encode('ascii')
            target = text + (' ' if kind == 'gallery' and len(text) % 2 else '')
            if target not in stored:
                packed.extend(bytes(-len(packed) % 4))
                stored[target] = POOL + len(packed)
                packed.extend(target.encode('ascii') + b'\0')
            struct.pack_into('<I', code.sections[0].data, field, stored[target])
            records.append({'id': row['id'], 'kind': kind, 'pointer_field': field,
                            'source_Japanese': row['japanese'], 'prior_english': old,
                            'english': text, 'compiled_text': target, 'target_pointer': stored[target],
                            'source_meaning': row['source_meaning'].replace('Raphael', 'Rafael').replace('Kamil', 'Camille'),
                            'localization_note': 'Apply the locked Rafael/Camille name policy; preserve every other caption word, subject and numbered variant.',
                            'review': dict.fromkeys(('source', 'context', 'localization', 'naturalness', 'formatting'), True)})
    assert len(records) == 16
    packed.extend(bytes(-len(packed) % 32))
    size = len(packed) + 64
    assert POOL + size <= STAGE and STAGE + size + 48 <= 0x023F4000
    packed.extend(wrapper(STAGE + len(packed), STAGE + size, size, arm))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack('<I', size)
    struct.pack_into('<I', code.sections[0].data, 0x8E4, branch_link(BASE + 0x8E4, STAGE + size - 64))
    struct.pack_into('<I', code.sections[0].data, 0xE45DC, POOL + size)
    saved = bytes(code.save())
    restored = bytearray(MainCodeFile(saved, BASE).sections[0].data)
    for field in [r['pointer_field'] for r in records] + [0x8E4, 0xE45DC]:
        restored[field:field + 4] = before[0][field:field + 4]
    at = code.codeSettingsOffs
    restored[at:at + 12] = before[0][at:at + 12]
    assert restored == before[0]
    assert all(bytes(code.sections[i].data) == before[i] for i in (1, 2))
    assert packed[:len(before[3]) - 48] == before[3][:-48]
    cpu = initialized(saved)
    changes = {r['pointer_field']: r for r in records}
    all_caption_selections = 0
    for path in ('translations/scene_caption_manuscript_v2.json',
                 'translations/gallery_description_manuscript_v1.json'):
        for row in read(path)['records']:
            fields = [row['pointer_field']] if 'pointer_field' in row else [r['field'] for r in row['source_fields']]
            for field in fields:
                pointer = struct.unpack('<I', cpu.mem_read(BASE + field, 4))[0]
                if field in changes:
                    selected = changes[field]
                    assert pointer == selected['target_pointer']
                    assert bytes(cpu.mem_read(pointer, len(selected['compiled_text']) + 1)) == selected['compiled_text'].encode('ascii') + b'\0'
                else:
                    assert pointer == struct.unpack_from('<I', arm, field)[0]
                all_caption_selections += 1
    canvas = Image.new('RGB', (768, len(records) * 48), 'white')
    draw = ImageDraw.Draw(canvas)
    for n, row in enumerate(records):
        text = row['compiled_text']
        x, y, tracking = (128 - len(text) * 5 // 2, 70, -1) if row['kind'] == 'scene' else (8, 20, 0)
        pixels, ink = raster(saved, row['target_pointer'], text, x, y, tracking)
        row['native_complete_ink_pixels'] = ink
        row['native_origin'] = [x, y]
        row['all_first_interior_final_letters_and_bounds_exact'] = True
        tile = Image.frombytes('L', (256, 192), bytes(255 if p else 0 for p in pixels))
        canvas.paste(tile.crop((0, y, 256, y + 12)).resize((768, 36)), (0, n * 48 + 12))
        draw.text((0, n * 48), row['id'], fill='black')
    canvas.save(ROOT / 'caption_review.png')
    (ROOT / 'proposed_arm9_research_only.bin').write_bytes(saved)
    document = {'format': 'dk4-artwork-name-caption-review-v283', 'translation_policy': 'natural-dialogue-v2',
                'target_locale': 'en-US', 'source_arm9_sha256': SOURCE_SHA,
                'target_arm9_sha256': sha(saved), 'records': records,
                'source_locked_caption_fields_only_plus_owned_pool_extension': True,
                'all_inherited_pool_bytes_ITCM_DTCM_and_other_main_bytes_preserved': True,
                'pool_payload_bytes': size, 'cache': cache_plan(saved),
                'native_autoload_owned_pool_copy_BSS_and_all16_caption_strings_exact': True,
                'all_caption_pointer_fields_verified': all_caption_selections,
                'playable_ROM_modified': False, 'native_parent_UI_selection_and_live_display_pending': True,
                'full_name_text_art_registered_integration_pending': True, 'full_goal_complete': False}
    (ROOT / 'native_proof.json').write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    Path('translations/artwork_name_caption_review_v283.json').write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(records)} corrected captions; complete native glyph pixels; {size} owned pool bytes; research only.')


if __name__ == '__main__':
    main()
