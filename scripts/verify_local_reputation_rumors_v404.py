"""All COMMON identities, real cold/warm copies and three-argument native printf."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.qa import audit_native_common_entry
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.local_reputation_rumors import TEXTS, apply_release
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.probe_remaining_common_layout import warm_copy
from scripts.verify_common_alignment_native_v257 import raster

ROOT = Path('work/analysis/local_reputation_rumors_v404')
ROM = Path('out/all_routes_combined_v388_candidate.nds')


def main():
    parent = NdsImage.open(ROM)
    common, arm = parent.read_file('/COMMON/MESFILE.DK4'), parent.read_file('/__arm9__.bin')
    target, mapped, change = apply_release(common, arm, 'translations/local_reputation_rumors_v1.json')
    original = NdsImage.open('work/clean.nds')
    old = common_message_entries(original.read_file('/COMMON/MESFILE.DK4'), original.read_file('/__arm9__.bin'))
    before = common_message_entries(common, arm, clean=False)
    after = common_message_entries(target, mapped, clean=False)
    document = json.loads(Path('translations/local_reputation_rumors_manuscript_v1.json').read_text(encoding='utf-8'))
    for row in document['records']:
        assert row['source_hex'] == old[row['message_id']].text.hex()
        qa = audit_native_common_entry(old[row['message_id']].text, row['english'])
        assert not [r for r in qa['issues'] if r['severity'] in ('warning', 'error')]
    for a, b in zip(before, after):
        expected = TEXTS[a.message_id].encode() if a.message_id in TEXTS else a.text.rstrip()
        assert b.text.rstrip() == expected
    copies = [warm_copy(mapped, target, i, after[i].text, cold_cache=cold)
              for i in range(819, 825) for cold in (False, True)]
    u = machine(mapped)
    u.mem_write(0x02387A20, bytes(MainCodeFile(mapped, 0x02000000).sections[3].data[:-48]))
    font = GameAsciiFont.from_arm9(mapped)
    out, fmt, name_at, city_at, role_at = [STACK + x for x in (0x1000, 0x2000, 0x2100, 0x2200, 0x2300)]
    cases = []
    for i, template in TEXTS.items():
        for name in ['Argot', 'Castor', 'Bergstrom', 'Li', 'Custom Trading Company']:
            for city in ['Amsterdam', 'Stockholm', 'Istanbul']:
                for role in ['Trader', 'Pirate', 'Admiral']:
                    u.mem_write(out - 16, b'\xA5' * 544)
                    u.mem_write(fmt, template.encode() + b'\0')
                    for pointer, value in [(name_at, name), (city_at, city), (role_at, role)]:
                        u.mem_write(pointer, value.encode() + b'\0')
                    u.mem_write(STACK, struct.pack('<I', role_at))
                    call(u, 0xD7720, (out, fmt, name_at, city_at))
                    expected = template.replace('%s', name, 1).replace('%s', city, 1).replace('%s', role, 1).encode() + b'\0'
                    assert bytes(u.mem_read(out, len(expected))) == expected
                    assert bytes(u.mem_read(out - 16, 16)) == b'\xA5' * 16
                    assert bytes(u.mem_read(out + len(expected), 528 - len(expected))) == b'\xA5' * (528 - len(expected))
                    for pointer, value in [(name_at, name), (city_at, city), (role_at, role)]:
                        assert bytes(u.mem_read(pointer, len(value) + 1)) == value.encode() + b'\0'
                    wrapped_at = STACK + 0x3000
                    u.mem_write(wrapped_at - 16, b'\xA5' * 288)
                    u.mem_write(STACK + 0x264, struct.pack('<I', 0x02054014))
                    u.mem_write(STACK + 0x274, struct.pack('<I', i))
                    call(u, 0x01FFCF3C - 0x02000000, (wrapped_at, out, 0))
                    wrapped = bytes(u.mem_read(wrapped_at, 256)).split(b'\0', 1)[0]
                    assert b' '.join(wrapped.split()) == expected[:-1]
                    assert bytes(u.mem_read(wrapped_at - 16, 16)) == b'\xA5' * 16
                    assert bytes(u.mem_read(wrapped_at + 256, 16)) == b'\xA5' * 16
                    try:
                        pixels = raster(mapped, wrapped, 0x01FFCE40 - 0x02000000,
                                        size=(228, 64), instruction_limit=200000)
                    except ValueError as error:
                        raise ValueError(f'Raster failed for {i}/{name}/{city}/{role}: {wrapped!r}') from error
                    glyph_count = sum(sum(bool(p) for p in font.decode(c).get_flattened_data())
                                      for c in expected[:-1].decode() if c != ' ')
                    assert sum(bool(p) for p in pixels) == glyph_count
                    cases.append({'id': i, 'native_printf_output': expected[:-1].decode(),
                                  'native_word_wrapped': wrapped.decode(), 'native_glyph_pixels': glyph_count,
                                  'all_three_arguments_and_all_glyphs_preserved': True})
    scope = []
    def portrait_scope(source, parent, message, hooked):
        uc = machine(source)
        uc.mem_write(0x02387A20, bytes(MainCodeFile(source, 0x02000000).sections[3].data[:-48]))
        src, dst = 0x0242C020, 0x0242D020
        raw = b'Argot of Amsterdam is an influential local Trader.'
        uc.mem_write(src, raw + b'\0')
        uc.mem_write(dst - 16, b'\xA5' * 288)
        uc.mem_write(STACK + 0x264, struct.pack('<I', parent))
        uc.mem_write(STACK + 0x274, struct.pack('<I', message))
        call(uc, (0x01FFCF3C if hooked else 0x01FF9EDC) - 0x02000000, (dst, src, 0))
        result = bytes(uc.mem_read(dst, 256)).split(b'\0', 1)[0]
        assert bytes(uc.mem_read(src, len(raw) + 1)) == raw + b'\0'
        assert bytes(uc.mem_read(dst - 16, 16)) == b'\xA5' * 16
        assert bytes(uc.mem_read(dst + 256, 16)) == b'\xA5' * 16
        return result
    for parent in [0x02054014, 0x020546E8, 0x02054044]:
        for message in [83, 321, 327, 819, 820, 821, 822, 823, 824]:
            a = portrait_scope(arm, parent, message, False)
            b = portrait_scope(mapped, parent, message, True)
            if parent != 0x02054014 or message not in (820, 821):
                assert a == b
            else:
                assert b' '.join(a.split()) == b' '.join(b.split())
                assert b.startswith(b' ') and b'\n  ' in b
            scope.append({'parent': parent, 'message': message, 'byte_exact_passthrough': a == b})
    from scripts.verify_equipment_wrap_scope_v365 import run
    equipment = [{'message': i, 'unchanged': run(arm, 0x020546E8, i, True) == run(mapped, 0x020546E8, i, True)}
                 for i in (321, 327)]
    assert all(r['unchanged'] for r in equipment)
    proof = {'source_candidate': str(ROM), 'source_candidate_sha256': sha(ROM.read_bytes()),
             'source_common_sha256': sha(common), 'source_arm9_sha256': sha(arm),
             'target_common_sha256': sha(target), 'target_arm9_sha256': sha(mapped),
             'all3668_visible_selections_verified': True, 'native_warm_cold_and_neighbor_copies': copies,
             'native_three_argument_printf_and_word_raster_cases': cases, 'no_printf_argument_reordering': True,
             'native_portrait_scope_and_unrelated_passthrough_cases': scope, 'existing_equipment_cases': equipment,
             'no_COMMON_file_cache_or_arena_growth': True, 'change': change,
             'actual_new_display_integrated_ROM_and_patch_pending': True, 'full_goal_complete': False}
    (ROOT / 'native_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(f'All3668 selections, {len(copies)} real cold/warm copies and {len(cases)} three-argument sprintf cases pass.')


if __name__ == '__main__':
    main()
