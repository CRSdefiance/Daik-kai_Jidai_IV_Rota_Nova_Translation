"""Original name providers, exhaustive dispatch, and later Tavern word rasters."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.tavern_scheme_context import NAMES, apply_release
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_tavern_addresses_v413 import wrap
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/tavern_schemes_v625')


def dispatches(arm, parent):
    u = machine(arm)
    u.mem_write(STACK + 0x264, struct.pack('<I', parent))
    u.reg_write(UC_ARM_REG_SP, STACK)

    def stop(uc, address, size, data):
        if address in (0x01FFCF78, 0x01FF9EDC):
            uc.emu_stop()

    hook = u.hook_add(UC_HOOK_CODE, stop)
    result = []
    for number in range(3668):
        u.mem_write(STACK + 0x274, struct.pack('<I', number))
        u.emu_start(0x01FFCF3C, 0x01FFD000, count=400)
        assert u.reg_read(UC_ARM_REG_SP) == STACK
        pc = u.reg_read(UC_ARM_REG_PC)
        assert pc in (0x01FFCF78, 0x01FF9EDC)
        result.append(pc)
    u.hook_del(hook)
    return result


def main():
    old_rom = NdsImage.open('out/all_routes_combined_v624_candidate.nds')
    rom = NdsImage.open('out/all_routes_combined_v625_candidate.nds')
    before = old_rom.read_file('/__arm9__.bin')
    common, arm, change = apply_release(old_rom.read_file('/COMMON/MESFILE.DK4'), before,
                                        'translations/tavern_scheme_context_v1.json')
    assert arm == rom.read_file('/__arm9__.bin') and common == rom.read_file('/COMMON/MESFILE.DK4')
    scopes = []
    for parent in (0x02054014, 0x02054044, 0x020546E8):
        old, new = dispatches(before, parent), dispatches(arm, parent)
        changed = [i for i, (a, b) in enumerate(zip(old, new, strict=True)) if a != b]
        assert changed == (list(range(874, 989)) if parent == 0x02054014 else [])
        assert all(old[i] == 0x01FF9EDC and new[i] == 0x01FFCF78 for i in changed)
        scopes.append({'parent': parent, 'all3668_original_and_new_dispatches_executed': True,
                       'newly_wrapped_message_IDs': changed})
    u = machine(arm)
    names = []
    for index, field, old, target, text in NAMES:
        call(u, 0x93D5C, (index,))
        assert u.reg_read(UC_ARM_REG_R0) == target
        assert bytes(u.mem_read(target, len(text) + 1)) == text.encode() + b'\0'
        fake = 0x02450000
        u.mem_write(fake + 4, bytes([index]))
        call(u, 0x93D28, (fake,))
        assert u.reg_read(UC_ARM_REG_R0) == target
        names.append({'scheme_type': index, 'pointer_field': field, 'old_pointer': old,
                      'target_pointer': target, 'complete_name': text,
                      'both_original_native_name_getters_return_complete_English': True})
    # raster() deliberately loads the pinned V255 FNT. Prove that it is still
    # the actual candidate font before crediting its CP932 glyph execution.
    assert rom.read_file('/GRP/KANJI.FNT') == NdsImage.open('out/all_routes_combined_v255_candidate.nds').read_file('/GRP/KANJI.FNT')
    entries = common_message_entries(common, arm, clean=False)
    cases = []
    for number in range(874, 989):
        for long in (False, True):
            template = entries[number].text.rstrip()
            values = [b'Kuala Lumpur' if long else b'Istanbul', b'Albuquerque' if long else b'Castor Co.']
            if 890 <= number <= 896:
                values = [b'9999999999' if long else b'1000']
            if 915 <= number <= 920:
                values = [b'Forge Papers' if long else b'Bribe']
            expanded = template
            for value in values:
                expanded = expanded.replace(b'%s', value, 1)
            assert b'%s' not in expanded
            formatted = wrap(arm, expanded, 0x02054014, number)
            events = []
            pixels = raster(arm, formatted, 0x01FFCE40 - 0x02000000, size=(228, 80),
                            glyph_events=events, instruction_limit=600000)
            visible = [e for e in events if e['code'] not in (32, 10)]
            text = expanded.decode('cp932')
            expected = [int.from_bytes(c.encode('cp932'), 'big') for c in text if not c.isspace()]
            assert [e['code'] for e in visible] == expected, (number, text, formatted)
            offset = 0
            for word in text.split():
                group = visible[offset:offset + len(word)]
                assert len(group) == len(word) and len({e['y'] for e in group}) == 1, (number, word)
                offset += len(word)
            assert b' '.join(formatted.split()) == b' '.join(expanded.split())
            cases.append({'message_id': number, 'long_layout_arguments': long,
                          'expanded': text, 'formatted': formatted.decode('cp932'),
                          'all_native_visible_glyphs_in_order_and_each_word_on_one_row': True,
                          'ink_pixels': sum(bool(p) for p in pixels)})
    save(ROOT / 'native_context_proof.json', {
        'candidate_sha256': sha(rom.source.read_bytes()), 'target_arm9_sha256': sha(arm),
        'transform': change, 'all22008_original_and_new_dispatch_executions': scopes,
        'four_scheme_names_both_original_getters': names, 'all230_later_Tavern_native_layouts': cases,
        'full_FNT_exact_candidate': True,
        'argument_values_are_explicit_layout_contracts_not_native_provider_verification': True,
        'actual_all_four_command_provider_contexts_pending_separate_emulator_proof': True,
        'source_content_followups_897_898_still_split_across_alternative_voice_records': True,
        'full_goal_complete': False, 'script_sha256': sha(Path(__file__).read_bytes())})
    print('V625:22008 dispatches,4 complete names through both source getters,230 full word/glyph layouts pass.')


if __name__ == '__main__':
    main()
