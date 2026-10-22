"""Current-ROM complete market pixels and original live-stock getters."""

import json
import struct
from pathlib import Path
from unittest.mock import patch

from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R2,
    UC_ARM_REG_R4,
    UC_ARM_REG_R10,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import verify_market_indicator_v248 as composition
from scripts.probe_button_prompt_native import call, machine

ROOT = Path('work/analysis/market_live_v428')
CAPTURE = Path('work/emulation_v193/market_live_v428')
ROM = Path('out/all_routes_combined_v414_candidate.nds')


def main():
    # Reuse the existing independent source-cell/font composition algorithm.
    # Its cargo fragment remains a supplied-input source geometry test only.
    with patch.object(composition, 'ROOT', ROOT), patch.object(composition, 'CAPTURE', CAPTURE), patch.object(composition, 'ROM', ROM):
        composition.main()
    pixels = json.loads((ROOT / 'proof.json').read_text(encoding='utf-8'))
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    report = json.loads((CAPTURE / 'capture_report.json').read_text(encoding='utf-8'))
    assert report['ROM_sha256'] == sha(ROM.read_bytes()) == '699c19373b11dbbbc91c4ace9a29bde680da424fed92f92451e267b8570fdd0c'
    ram = (CAPTURE / 'final_arm9_ram.bin').read_bytes()
    assert sha(ram) == report['read_only_RAM_snapshot']['sha256']
    state = report['read_only_native_state']
    assert state['serialized_RAM_matches_same_frame_direct_export']
    assert state['main_RAM_unchanged_by_export'] and not state['state_loaded']
    for row in state['regions'].values():
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    ranges = [(0xBCAE8, 0xBCB00), (0xBCADC, 0xBCAE8), (0xC1718, 0xC1730)]
    assert all(arm[lo:hi] == clean[lo:hi] for lo, hi in ranges)
    u = machine(arm)
    u.mem_write(0x02000000, ram)
    view, model = 0x0218F25C, 0x021918C0
    assert struct.unpack('<I', u.mem_read(view, 4))[0] == 0x02158698
    # Runtime type metadata's name pointer establishes CTradingView identity.
    type_info = struct.unpack('<I', u.mem_read(0x02158698 - 4, 4))[0]
    name_pointer = struct.unpack('<I', u.mem_read(type_info + 4, 4))[0]
    assert bytes(u.mem_read(name_pointer, 32)).split(b'\0')[0] == b'12CTradingView'
    assert struct.unpack('<I', u.mem_read(view + 0x5F8, 4))[0] == model
    grade_help = IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/COMMON/HELP.DK4')).blocks[193]
    current_grade_help = IlnkContainer.parse(rom.read_file('/COMMON/HELP.DK4')).blocks[193]
    first_paragraph = grade_help.splitlines()[1].decode('cp932')
    assert first_paragraph == '交易品には１から５級までの等級があります。１級が最高です。'
    assert current_grade_help == grade_help
    before = bytes(u.mem_read(model, 0x610))
    slots = []
    for index, pixel_case in enumerate(pixels['cases']):
        values = []
        for getter in (0xBCAF4, 0xBCAE8, 0xBCADC):
            call(u, getter, (model, index))
            values.append(u.reg_read(UC_ARM_REG_R0))
        assert values == [pixel_case['atlas_index'], pixel_case['indicator_digit'], int(pixel_case['quantity'])]
        u.reg_write(UC_ARM_REG_R10, view)
        u.reg_write(UC_ARM_REG_R4, index)
        u.emu_start(0x020C1718, 0x020C1730, count=32)
        assert u.reg_read(UC_ARM_REG_PC) == 0x020C1730
        source_x = u.reg_read(UC_ARM_REG_R2)
        assert source_x == pixel_case['indicator_source_origin'][0]
        assert bytes(u.mem_read(model, 0x610)) == before
        slots.append({'slot': index, 'goods': values[0], 'indicator': values[1],
                      'quantity': values[2], 'actual_view_model_link': model,
                      'original_stock_getters': [0x020BCAF4, 0x020BCAE8, 0x020BCADC],
                      'original_indicator_argument_source_x': source_x,
                      'complete_visible_pixels_and_native_values_match': True})
    proof = {'format': 'dk4-current-market-live-v428', 'candidate': str(ROM),
             'candidate_sha256': sha(ROM.read_bytes()), 'report': str(CAPTURE / 'capture_report.json'),
             'report_sha256': sha((CAPTURE / 'capture_report.json').read_bytes()),
             'capture': pixels['capture'], 'composition_proof': str(ROOT / 'proof.json'),
             'composition_proof_sha256': sha((ROOT / 'proof.json').read_bytes()),
             'complete_icon_rectangle_pixels': 2880, 'complete_indicator_ink_pixels': 130,
             'unexplained_icon_rectangle_pixels': 0, 'actual_TradingView': view,
             'actual_model': model, 'stock_getter_and_argument_cases': slots,
             'original_model_unchanged_by_queries': True, 'source_exact_code_ranges': ranges,
             'V249_BCC_getters_not_used_for_this_visible_local_stock_row': True,
             'grade_meaning_original_HELP193': {'source_sha256': sha(grade_help),
                                               'source_first_paragraph': first_paragraph,
                                               'grade_range': [1, 5], 'best_grade': 1,
                                               'current_HELP193_still_Japanese_translation_pending': True},
             'scope': 'Ordinary cold-boot Deal screen; complete pixels and same-frame stock values through original getters. Isolated read-only snapshot query of the actual linked CTradingView and original crop argument fragment. Original HELP193 establishes grades1-5 with1 best. No claim of a live instruction trace, quantity transaction arithmetic or every Market variant.',
             'no_fixture_ROM_savestate_or_live_RAM_injection': True,
             'ROM_modified': False, 'all18_plaques_fully_completed': False, 'full_goal_complete': False}
    (ROOT / 'live_stock_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'complete_icon_pixels': 2880, 'indicator_pixels': 130,
                      'live_stock_values_match_all5_slots': True}))


if __name__ == '__main__':
    main()
