"""Bind giveaway drafts to the original role/voice tables and native painter."""

import struct
from copy import deepcopy
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.giveaway_editorial import ANNOUNCE_TABLE, CONFIRM_TABLE, IDS, transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.patch.shop_business_editorial import compile_paragraph
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_common_literal_prefix_native_v255 import expand, setup
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/giveaway_editorial_v746')
MANUSCRIPT = Path('translations/giveaway_editorial_manuscript_v1.json')
CONFIG = Path('translations/giveaway_editorial_release_v1.json')
ROM = Path('out/all_routes_combined_v745_candidate.nds')


def table_selection(arm):
    cpu = machine(arm)
    style = [0]

    def supplied_style(u, address, size, unused):
        if address == BASE + 0x7E988:
            u.reg_write(UC_ARM_REG_R0, style[0])
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    hook = cpu.hook_add(UC_HOOK_CODE, supplied_style)
    rows = []
    try:
        for table, values in ((CONFIRM_TABLE, (659, 660, 661, 0xFFFFFFFF, 662, 663, 664, 665)),
                              (ANNOUNCE_TABLE, tuple(range(666, 674)))):
            assert struct.unpack('<8I', cpu.mem_read(table, 32)) == values
            for index, value in enumerate(values):
                style[0] = index
                executed = call(cpu, 0x53F4C, (0x02450000, table))
                expected = 659 if value == 0xFFFFFFFF else value
                assert cpu.reg_read(UC_ARM_REG_R0) == expected
                rows.append({'table': table, 'supplied_voice_style': index,
                             'native_message': expected, 'original_selector_instructions': len(executed),
                             'missing_confirmation_style3_falls_back_to659': index == 3 and table == CONFIRM_TABLE})
            call(cpu, 0x53F4C, (0, table))
            assert cpu.reg_read(UC_ARM_REG_R0) == values[0]
    finally:
        cpu.hook_del(hook)
    return rows


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not CONFIG.exists() and not MANUSCRIPT.exists()
    ledger = read('translations/editorial_review_current_v1.json')
    assert sha(ROM.read_bytes()) == ledger['current_integrated_candidate']['sha256']
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, common = current.read_file('/__arm9__.bin'), current.read_file('/COMMON/MESFILE.DK4')
    source_arm = clean.read_file('/__arm9__.bin')
    spans = ((0x5ED34, 0x5EE08), (0x53CB0, 0x53D44), (0x53D44, 0x53DC8),
             (0x53F4C, 0x53F9C), (0x7E988, 0x7E9A0), (0x1184A0, 0x1184E0))
    assert all(arm[a:b] == source_arm[a:b] for a, b in spans)
    assert struct.unpack_from('<I', arm, 0x5EDFC)[0] == CONFIRM_TABLE
    assert struct.unpack_from('<I', arm, 0x5EE00)[0] == ANNOUNCE_TABLE
    assert struct.unpack_from('<I', arm, 0x5EE04)[0] == 674
    source_cases = table_selection(source_arm)
    assert table_selection(arm) == source_cases
    entries = common_message_entries(common, arm, clean=False)
    original = read('translations/shop_town_editorial_manuscript_v1.json')
    document = deepcopy(original)
    document['records'] = [deepcopy(r) for r in original['records'] if r['message_id'] in IDS]
    document['status'] = 'native-source-and-font-reviewed-experimental-live-parent-test-pending'
    font = GameAsciiFont.from_arm9(arm)
    cpu = setup(arm)
    cpu.mem_write(POOL, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    assert current.read_file('/GRP/KANJI.FNT') == NdsImage.open('out/all_routes_combined_v255_candidate.nds').read_file('/GRP/KANJI.FNT')
    checks = []
    sheet = Image.new('RGB', (720, 7 * 150), '#30343c')
    draw = ImageDraw.Draw(sheet)
    for slot, row in enumerate(document['records']):
        i = row['message_id']
        compiled, lines = compile_paragraph(row['english'])
        assert expand(cpu, compiled) == compiled
        actual = raster(arm, compiled, 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=1000000)
        expected = bytearray(228 * 64)
        for nline, line in enumerate(lines):
            for n, char in enumerate(line):
                glyph = font.decode(char)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            expected[(nline * 16 + y) * 228 + 6 + n * 6 + x] = 1
        assert actual == bytes(expected)
        preview = Image.new('RGB', (228, 64))
        preview.putdata([(30, 25, 15) if v else (238, 226, 193) for v in actual])
        target = ROOT / f'native_message_{i}.png'
        preview.save(target)
        draw.text((8, slot * 150 + 3), f'{i}: native macro expander + complete painter', fill='white')
        sheet.paste(preview.resize((456, 128), Image.Resampling.NEAREST), (8, slot * 150 + 20))
        table = CONFIRM_TABLE if i < 666 else ANNOUNCE_TABLE
        voice = next(r['supplied_voice_style'] for r in source_cases if r['table'] == table and r['native_message'] == i)
        row['current_text_hex'] = entries[i].text.hex()
        row['speaker'] = f'Assigned Missionary, original voice-style slot {voice}'
        row['context'] = ('Square Distribute Goods; role10 Missionary. Original 53CB0 confirmation uses '
                          'table21184C0 and 53D44 announcement uses21184A0; 53F4C selects the source voice slot. '
                          'Slots are controlled native checks; earned role assignment is not claimed.')
        row['review']['context'] = row['review']['formatting'] = True
        row['localization_note'] += ' Exact native voice table and full font plane verified; generated guarded wraps only.'
        row['status'] = 'native-component-approved-live-fixture-test-pending'
        checks.append({'message_id': i, 'voice_style_slot': voice, 'lines': lines,
                       'compiled_hex': compiled.hex(), 'complete228x64_native_plane_exact': True,
                       'ink_pixels': sum(actual), 'preview': str(target), 'preview_sha256': sha(target.read_bytes())})
    sheet.save(ROOT / 'native_giveaway_previews_2x.png')
    save(MANUSCRIPT, document)
    target_common, target_arm, report = transform(common, arm, document)
    (ROOT / 'research_COMMON.bin').write_bytes(target_common)
    (ROOT / 'research_ARM9.bin').write_bytes(target_arm)
    save(ROOT / 'native_review.json', {
        'source_ROM_sha256': sha(ROM.read_bytes()),
        'unchanged_original_source_spans': [{'start': a, 'end': b, 'sha256': sha(arm[a:b])} for a, b in spans],
        'original_native_voice_selector16_cases_plus2_null_actor_cases_per_ROM': source_cases,
        'style_getter_results_supplied_not_native_actor_acquisition': True,
        'original_role10_confirm_then_cargo_then_announcement_then_customer674_sequence_source_bound': True,
        'complete_native_font_checks': checks, 'repack': report,
        'live_parent_verification_pending': True, 'full_goal_complete': False})
    save(CONFIG, {'format': 'dk4-giveaway-editorial-v1',
        'source_common_sha256': sha(common), 'source_arm9_sha256': sha(arm),
        'target_common_sha256': sha(target_common), 'target_arm9_sha256': sha(target_arm),
        'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'dependencies': {str(p): sha(p.read_bytes()) for p in (
            Path('dk4tool/patch/giveaway_editorial.py'), Path('dk4tool/patch/shop_business_editorial.py'),
            Path('dk4tool/script/common_native_repack.py'), ROOT / 'native_review.json')}})
    path = Path('translations/release_stack.json')
    registry = read(path)
    assert 'all-routes-unified-v746' not in registry['profiles']
    before = deepcopy(registry)
    profile = deepcopy(registry['profiles']['all-routes-unified-v745'])
    profile.update({'giveaway_editorial': str(CONFIG), 'status': 'experimental',
        'description': 'Full V745 plus seven reviewed role10 giveaway confirmation/announcement revisions; live test pending.',
        'note': 'All470 batches114 baked accepted layers preserved; no runtime code or pool growth.'})
    registry['profiles']['all-routes-unified-v746'] = profile
    save(ROOT / 'release_stack_before_V746.json', before)
    save(path, registry)
    assert registry['canonical_baseline'] == before['canonical_baseline'] and registry['accepted_layers'] == before['accepted_layers']
    assert all(registry['profiles'][k] == v for k, v in before['profiles'].items())
    print('V746 registered: seven complete native paragraphs, original voice-slot selection preserved.', flush=True)


if __name__ == '__main__':
    main()
