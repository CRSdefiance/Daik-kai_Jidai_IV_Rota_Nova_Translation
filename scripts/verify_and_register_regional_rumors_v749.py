"""Bind all regional_rumors choices to original selection and complete native font planes."""

import argparse
from copy import deepcopy
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.regional_rumors import IDS, compile_paragraph, transform
from dk4tool.rom.nds import NdsImage
from scripts.prepare_product_pitches_v747 import native_layout, wrapper_dispatch
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/regional_rumors_v749')
MANUSCRIPT = Path('translations/regional_rumors_manuscript_v1.json')
CONFIG = Path('translations/regional_rumors_release_v1.json')
ROM = Path('out/all_routes_combined_v748_candidate.nds')


def selector(arm):
    cpu = machine(arm)
    state, region = [0], [0]

    def supplied(u, address, size, unused):
        if address == BASE + 0xB4A88:
            value = state[0]
        elif address == BASE + 0xB51B4:
            value = region[0]
        else:
            return
        u.reg_write(UC_ARM_REG_R0, value)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    hook = cpu.hook_add(UC_HOOK_CODE, supplied)
    rows = []
    try:
        for flag in (0, 1, 2):
            state[0] = flag
            for n in range(21):
                region[0] = n
                call(cpu, 0x5FA60, (0, 0x02450000))
                selected = cpu.reg_read(UC_ARM_REG_R0)
                assert selected == (688 if flag else 709) + n
                rows.append({'supplied_town_flag': flag, 'supplied_region': n, 'original_selected_message': selected})
    finally:
        cpu.hook_del(hook)
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--refine-unpublished', action='store_true')
    args = parser.parse_args()
    assert CONFIG.exists() == args.refine_unpublished
    doc = read(MANUSCRIPT)
    current = NdsImage.open(ROM)
    common, arm = current.read_file('/COMMON/MESFILE.DK4'), current.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = ((0x5F9B8, 0x5FB54), (0xB4A88, 0xB4AD4), (0xB51B4, 0xB51CC))
    assert all(arm[a:b] == clean[a:b] for a, b in spans)
    cases = selector(arm)
    assert selector(clean) == cases
    for row in doc['records']:
        row['review']['context'] = row['review']['formatting'] = True
        row['status'] = 'native-source-and-font-reviewed-gameplay-pending'
    target_common, target_arm, repack = transform(common, arm, doc)
    before, after = wrapper_dispatch(arm), wrapper_dispatch(target_arm)
    assert [i for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b] == list(IDS)
    cpu = machine(target_arm)
    cpu.mem_write(0x02387A20, bytes(MainCodeFile(target_arm, BASE).sections[3].data[:-48]))
    font = GameAsciiFont.from_arm9(target_arm)
    checks = []
    sheets = [Image.new('RGB', (730, count * 150), '#30343c') for count in (11, 10)]
    for n, row in enumerate(doc['records']):
        i = row['message_id']
        text = compile_paragraph(row['english'])
        formatted, lines = native_layout(cpu, text, i, ())
        pixels = raster(target_arm, formatted, 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=1000000)
        expected = bytearray(228 * 64)
        for line_no, line in enumerate(lines):
            for column, char in enumerate(line):
                glyph = font.decode(char)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            expected[(16 * line_no + y) * 228 + 6 + column * 6 + x] = 1
        assert pixels == bytes(expected), (i, lines)
        preview = ROOT / f'native_{i}.png'
        Image.frombytes('L', (228, 64), bytes(0 if p else 255 for p in pixels)).save(preview)
        sheet, index = (sheets[0], n) if n < 11 else (sheets[1], n - 11)
        ImageDraw.Draw(sheet).text((8, index * 150), f'{i}: {row["decision"]}', fill='white')
        sheet.paste(Image.open(preview).convert('RGB').resize((456, 128), Image.Resampling.NEAREST), (8, index * 150 + 18))
        checks.append({'message_id': i, 'lines': lines, 'runtime_formatted_hex': formatted.hex(),
                       'complete228x64_native_plane_and_all_blank_cells_exact': True,
                       'preview': str(preview), 'preview_sha256': sha(preview.read_bytes())})
    for n, sheet in enumerate(sheets):
        sheet.save(ROOT / f'native_previews_{n + 1}_2x.png')
    doc['status'] = 'native-source-and-font-reviewed-experimental-gameplay-pending'
    save(MANUSCRIPT, doc)
    (ROOT / 'research_COMMON.bin').write_bytes(target_common)
    (ROOT / 'research_ARM9.bin').write_bytes(target_arm)
    save(ROOT / 'native_review.json', {
        'source_ROM_sha256': sha(ROM.read_bytes()),
        'original_source_spans': [{'start': a, 'end': b, 'sha256': sha(arm[a:b])} for a, b in spans],
        'original_selector63_cases_each_clean_and_current': cases,
        'supplied_getter_contracts_not_earned_town_flag_or_travel': True,
        'all18340_dispatch_cases_preserved_except21_regional_rumor_direct_cases': True,
        'all21_native_printf_macro_wrap_and_complete_font_planes': checks,
        'revised_IDs': [r['message_id'] for r in doc['records'] if r['decision'] == 'revise'],
        'retained_wording_IDs': [r['message_id'] for r in doc['records'] if r['decision'] == 'retain-wording'],
        'repack': repack, 'gameplay_pending': True, 'full_goal_complete': False})
    save(CONFIG, {'format': 'dk4-regional-rumors-v1',
        'source_common_sha256': sha(common), 'source_arm9_sha256': sha(arm),
        'target_common_sha256': sha(target_common), 'target_arm9_sha256': sha(target_arm),
        'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'dependencies': {str(p): sha(p.read_bytes()) for p in (
            Path('dk4tool/patch/regional_rumors.py'), Path('dk4tool/script/common_native_repack.py'), ROOT / 'native_review.json')}})
    path = Path('translations/release_stack.json')
    registry = read(path)
    assert ('all-routes-unified-v749' in registry['profiles']) == args.refine_unpublished
    if not args.refine_unpublished:
        save(ROOT / 'release_stack_before_V749.json', registry)
    profile = deepcopy(registry['profiles']['all-routes-unified-v748'])
    profile.update({'regional_rumors': str(CONFIG), 'status': 'experimental',
                    'description': 'Complete V748 plus source-reviewed21 regional faction/person rumors with existing bounded portrait wrapping; gameplay pending.'})
    registry['profiles']['all-routes-unified-v749'] = profile
    save(path, registry)
    print('V749 registered:21 complete source/native paragraphs;12 revisions and9 retained wordings.', flush=True)


if __name__ == '__main__':
    main()
