"""Exercise actual queued voice-table dispatch and every scheme voice template."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.tavern_strategist_wrap import TABLES, apply_release
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_tavern_scheme_native_v625 import dispatches
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/tavern_schemes_v626')


def queued_wrap(arm, text, parent, table):
    u = machine(arm)
    u.mem_write(0x02387A20, bytes(MainCodeFile(arm, 0x02000000).sections[3].data[:-48]))
    source, dest = 0x0242C020, 0x0242D020
    u.mem_write(source - 16, b'\xA5' * 16 + text + b'\0' + b'\xA5' * 16)
    u.mem_write(dest - 16, b'\xA5' * 288)
    u.mem_write(STACK + 0x264, struct.pack('<I', parent))
    u.mem_write(STACK + 0x274, bytes(4))
    u.mem_write(STACK + 0x27C, struct.pack('<I', table))
    call(u, 0x01FFCF3C - 0x02000000, (dest, source, 0))
    result = bytes(u.mem_read(dest, 256)).split(b'\0', 1)[0]
    assert bytes(u.mem_read(source, len(text) + 1)) == text + b'\0'
    assert bytes(u.mem_read(dest - 16, 16)) == bytes(u.mem_read(dest + 256, 16)) == b'\xA5' * 16
    return result


def table_scopes(arm, parent, tables):
    u = machine(arm)
    u.mem_write(STACK + 0x264, struct.pack('<I', parent))
    u.reg_write(UC_ARM_REG_SP, STACK)

    def stop(uc, address, size, data):
        if address in (0x01FFCF78, 0x01FF9EDC):
            uc.emu_stop()

    hook = u.hook_add(UC_HOOK_CODE, stop)
    result = []
    for table in tables:
        u.mem_write(STACK + 0x27C, struct.pack('<I', table))
        u.emu_start(0x01FFCF3C, 0x01FFD000, count=400)
        assert u.reg_read(UC_ARM_REG_SP) == STACK
        result.append(u.reg_read(UC_ARM_REG_PC))
    u.hook_del(hook)
    return result


def main():
    rom = NdsImage.open('out/all_routes_combined_v626_candidate.nds')
    old_rom = NdsImage.open('out/all_routes_combined_v625_candidate.nds')
    before = old_rom.read_file('/__arm9__.bin')
    arm, change = apply_release(before, 'translations/tavern_strategist_wrap_v1.json')
    assert arm == rom.read_file('/__arm9__.bin')
    assert rom.read_file('/COMMON/MESFILE.DK4') == old_rom.read_file('/COMMON/MESFILE.DK4')
    numeric = []
    for parent in (0x02054014, 0x02054044, 0x020546E8):
        assert dispatches(before, parent) == dispatches(arm, parent)
        numeric.append({'parent': parent, 'all3668_old_new_numeric_dispatches_exact': True})
    # Include both old SeaFoam tables and nearby excluded/misaligned addresses.
    tables = list(TABLES) + [0, 0x021182E0, 0x021181C0, 0x02118360,
                            0x02117B44, 0x021181E1, 0x02118321,
                            0x02118800, 0x02118820, 0x02118840, 0x02116730]
    scope = []
    for parent in (0x02053DB8, 0x02053D24, 0x02053C14, 0x02053C5C, 0x02054044):
        old = table_scopes(before, parent, tables)
        new = table_scopes(arm, parent, tables)
        for table, a, b in zip(tables, old, new, strict=True):
            if parent in (0x02053DB8, 0x02053D24) and table in TABLES:
                assert a == 0x01FF9EDC and b == 0x01FFCF78
            else:
                assert a == b
            scope.append({'parent': parent, 'table': table, 'old_PC': a, 'new_PC': b})
    entries = common_message_entries(rom.read_file('/COMMON/MESFILE.DK4'), arm, clean=False)
    assert rom.read_file('/GRP/KANJI.FNT') == NdsImage.open('out/all_routes_combined_v255_candidate.nds').read_file('/GRP/KANJI.FNT')
    cases = []
    for table in TABLES:
        ids = struct.unpack_from('<8I', before, table - 0x02000000)
        for number in sorted(set(ids) - {0xFFFFFFFF}):
            for parent in (0x02053DB8, 0x02053D24):
                template = entries[number].text.rstrip()
                values = [b'Forge Papers'] if 915 <= number <= 920 else [b'Kuala Lumpur', b'Albuquerque']
                expanded = template
                for value in values:
                    expanded = expanded.replace(b'%s', value, 1)
                assert b'%s' not in expanded
                formatted = queued_wrap(arm, expanded, parent, table)
                assert b' '.join(formatted.split()) == b' '.join(expanded.split())
                events = []
                pixels = raster(arm, formatted, 0x01FFCE40 - 0x02000000, size=(228, 80),
                                glyph_events=events, instruction_limit=600000)
                visible = [e for e in events if e['code'] not in (32, 10)]
                text = expanded.decode('cp932')
                expected = [int.from_bytes(c.encode('cp932'), 'big') for c in text if not c.isspace()]
                assert [e['code'] for e in visible] == expected
                offset = 0
                for word in text.split():
                    group = visible[offset:offset + len(word)]
                    assert len(group) == len(word) and len({e['y'] for e in group}) == 1
                    offset += len(word)
                cases.append({'parent': parent, 'table': table, 'message_id': number,
                              'expanded': text, 'formatted': formatted.decode('cp932'),
                              'all_visible_glyphs_in_order_and_each_word_on_one_row': True,
                              'ink_pixels': sum(bool(p) for p in pixels)})
    save(ROOT / 'queued_native_proof.json', {
        'candidate_sha256': sha(rom.source.read_bytes()), 'target_arm9_sha256': sha(arm),
        'transform': change, 'all22008_numeric_dispatch_executions_exact': numeric,
        'original_table_parent_and_excluded_table_scope_cases': scope,
        'all_original_scheme_voice_templates_through_both_queued_parent_formats': cases,
        'supplied_substitutions_are_layout_contracts_not_native_provider_verification': True,
        'original_expander_ABI_text_buffers_and_guard_extents_preserved': True,
        'all18_original_plaques_remain_incomplete': True, 'full_goal_complete': False,
        'script_sha256': sha(Path(__file__).read_bytes())})
    print(f'V626:22008 unchanged numeric dispatches,{len(scope)} table/parent scopes,{len(cases)} queued voice word/glyph layouts pass.')


if __name__ == '__main__':
    main()
