"""Verify the complete retail/business family before registered integration."""

import struct
from copy import deepcopy
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.patch.shop_business_editorial import IDS, compile_paragraph, transform
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_common_literal_prefix_native_v255 import expand, setup
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shop_business_v745')
MANUSCRIPT = Path('translations/shop_business_editorial_manuscript_v1.json')
CONFIG = Path('translations/shop_business_editorial_release_v1.json')
ROM = Path('out/all_routes_combined_v712_candidate.nds')


def selectors(arm):
    u = machine(arm)
    value = [0]
    calls = []

    def getter(cpu, address, size, unused):
        if address != BASE + 0xB2E04:
            return
        calls.append(address)
        cpu.reg_write(UC_ARM_REG_R0, value[0])
        cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))

    hook = u.hook_add(UC_HOOK_CODE, getter)
    rows = []
    try:
        for state, expected in enumerate((682, 683, 684, 685, 686, 687, 687, 687, 687, 687, 687, 687, 658)):
            value[0] = state
            calls.clear()
            executed = call(u, 0x5FA98, (0, 0x02450000))
            assert u.reg_read(UC_ARM_REG_R0) == expected and calls == [BASE + 0xB2E04]
            rows.append({'supplied_town_state': state, 'native_message': expected,
                         'executed_original_instruction_count': len(executed)})
    finally:
        u.hook_del(hook)
    return rows


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not CONFIG.exists() and not MANUSCRIPT.exists()
    ledger = read('translations/editorial_review_current_v1.json')
    assert sha(ROM.read_bytes()) == ledger['source_pins']['current']['sha256']
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, common = current.read_file('/__arm9__.bin'), current.read_file('/COMMON/MESFILE.DK4')
    clean_arm = clean.read_file('/__arm9__.bin')
    assert arm[0x5F9B8:0x5FB54] == clean_arm[0x5F9B8:0x5FB54]
    assert struct.unpack_from('<I', arm, 0x5FA5C)[0] == 657
    assert struct.unpack_from('<I', arm, 0x5FB4C)[0] == 658
    # MOV r1,#656 and the BL to the original portrait COMMON wrapper.
    instruction = struct.unpack_from('<I', arm, 0x5F9F4)[0]
    assert instruction & 0xFFFFF000 == 0xE3A01000
    value, rotate = instruction & 255, ((instruction >> 8) & 15) * 2
    assert ((value >> rotate) | (value << (32 - rotate))) & 0xFFFFFFFF == 656
    source_selectors = selectors(clean_arm)
    assert selectors(arm) == source_selectors
    # The existing painter selects its current alignment helper from this BL.
    word = struct.unpack_from('<I', arm, 0x54924)[0]
    assert word >> 24 == 0xEB
    displacement = word & 0xFFFFFF
    if displacement & 0x800000:
        displacement -= 0x1000000
    paint = 0x54924 + 8 + displacement * 4
    assert BASE + paint == 0x01FFCE40
    assert current.read_file('/GRP/KANJI.FNT') == NdsImage.open('out/all_routes_combined_v255_candidate.nds').read_file('/GRP/KANJI.FNT')
    font = GameAsciiFont.from_arm9(arm)
    native = setup(arm)
    native.mem_write(POOL, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    original = read('translations/shop_town_editorial_manuscript_v1.json')
    document = deepcopy(original)
    document['records'] = [deepcopy(r) for r in original['records'] if r['message_id'] in IDS]
    document['status'] = 'source-context-and-complete-native-font-reviewed-live-release-test-pending'
    checks = []
    sheet = Image.new('RGB', (720, 7 * 150), '#30343c')
    draw = ImageDraw.Draw(sheet)
    for slot, row in enumerate(document['records']):
        i = row['message_id']
        compiled, lines = compile_paragraph(row['english'])
        assert expand(native, compiled) == compiled
        actual = raster(arm, compiled, paint, size=(228, 64), instruction_limit=1000000)
        expected = bytearray(228 * 64)
        for line_index, line in enumerate(lines):
            for n, char in enumerate(line):
                glyph = font.decode(char)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            expected[(line_index * 16 + y) * 228 + 6 + n * 6 + x] = 1
        assert actual == bytes(expected)
        im = Image.new('RGB', (228, 64), '#eee2c1')
        im.putdata([(30, 25, 15) if v else (238, 226, 193) for v in actual])
        target = ROOT / f'native_message_{i}.png'
        im.save(target)
        draw.text((8, slot * 150 + 3), f'{i}: original native macro expander + painter', fill='white')
        sheet.paste(im.resize((456, 128), Image.Resampling.NEAREST), (8, slot * 150 + 20))
        checks.append({'message_id': i, 'lines': lines, 'compiled_hex': compiled.hex(),
                       'all14592_native_plane_indices_exact': True, 'ink_pixels': sum(actual),
                       'preview': str(target), 'preview_sha256': sha(target.read_bytes())})
        row['review']['context'] = True
        row['review']['formatting'] = True
        row['context'] = ('Original Square merchant retail/business portrait family; '
                          'retail657 direct source branch and normal658/event682-687 original native selectors are mapped. '
                          'Controlled selector calls supply only getter results; ordinary live tests pending.')
        row['localization_note'] += (' All generated lines and the complete 228x64 native font plane reviewed; '
                                    'literal I/F expansion remains byte-exact. No authored layout; live parent test remains pending.')
        row['status'] = 'native-component-approved-experimental-live-test-pending'
    sheet.save(ROOT / 'native_business_previews_2x.png')
    save(MANUSCRIPT, document)
    result_common, result_arm, report = transform(common, arm, document)
    (ROOT / 'research_COMMON.bin').write_bytes(result_common)
    (ROOT / 'research_ARM9.bin').write_bytes(result_arm)
    save(ROOT / 'native_review.json', {
        'current_ROM_sha256': sha(ROM.read_bytes()), 'retail_business_code_span': [0x5F9B8, 0x5FB54],
        'retail_business_clean_current_code_sha256': sha(arm[0x5F9B8:0x5FB54]),
        'original_town_selector_controlled_cases_per_ROM': source_selectors,
        'business_selector_658_complete_controlled_case12_per_ROM': True,
        'controlled_model_getter_results_are_not_ordinary_gameplay': True,
        'native_macro_and_full_font_checks': checks, 'repack': report,
        'all_render_calls_completed_with_return_ABI': True,
        'prototype100000_instruction_budget_inadequate_corrected_to1000000': True,
        'prototype_adjacent_lore_helper_and_inverted_default_literals_rejected_by_source_assertions': True,
        'live_gameplay_and_integrated_build_pending': True,
    })
    dependencies = {str(p): sha(p.read_bytes()) for p in (
        Path('dk4tool/patch/shop_business_editorial.py'), Path('dk4tool/script/common_native_repack.py'),
        ROOT / 'native_review.json')}
    save(CONFIG, {'format': 'dk4-shop-business-editorial-v1',
                  'source_common_sha256': sha(common), 'source_arm9_sha256': sha(arm),
                  'target_common_sha256': sha(result_common), 'target_arm9_sha256': sha(result_arm),
                  'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
                  'dependencies': dependencies})
    registry_path = Path('translations/release_stack.json')
    registry = read(registry_path)
    assert 'all-routes-unified-v745' not in registry['profiles']
    before = deepcopy(registry)
    profile = deepcopy(registry['profiles']['all-routes-unified-v712'])
    profile.update({'shop_business_editorial': str(CONFIG), 'status': 'experimental',
                    'description': 'Complete retail/business prose family: seven source-faithful revisions; normal live review pending.',
                    'note': 'All470 registered batches and114 accepted baked layers preserved. Graphics audit separately incomplete; canonical unchanged.'})
    registry['profiles']['all-routes-unified-v745'] = profile
    save(ROOT / 'release_stack_before_V745.json', before)
    save(registry_path, registry)
    assert all(registry[k] == before[k] for k in ('canonical_baseline', 'accepted_layers'))
    assert all(registry['profiles'][k] == v for k, v in before['profiles'].items())
    print('Seven complete native prose planes pass; V745 experimental registered profile prepared.', flush=True)


if __name__ == '__main__':
    main()
