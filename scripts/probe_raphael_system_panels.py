"""Execute the native FE dispatcher and modal renderer for all damaged tutorials."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn import UC_ARCH_ARM, UC_HOOK_CODE, UC_MODE_ARM, Uc
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_scene_caption_raster import execute
from scripts.prepare_raphael_system_panel_repair import CONFIG
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels


def dispatch(source, selector):
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.mem_map(0x02000000, 0x800000)
    uc.mem_write(0x02000000, source)
    text, stack, stop = 0x02400000, 0x027F0000, 0x027FFF00
    uc.mem_write(text, b'Ceuta:\0')
    uc.reg_write(UC_ARM_REG_R0, selector); uc.reg_write(UC_ARM_REG_R1, text)
    uc.reg_write(UC_ARM_REG_SP, stack); uc.reg_write(UC_ARM_REG_LR, stop)
    paths = []

    def hook(machine, address, size, data):
        if address == 0x020940B0:  # Existing UI state update contract.
            machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))
        elif address == 0x02053914:  # No-macro string expansion contract for this dispatch fixture.
            if machine.reg_read(UC_ARM_REG_R1) != text:
                raise ValueError('Dispatcher passes the wrong text')
            machine.mem_write(machine.reg_read(UC_ARM_REG_R0), b'Ceuta:\0')
            machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))
        elif address in (0x0205473C, 0x02053AC4):
            if bytes(machine.mem_read(machine.reg_read(UC_ARM_REG_R0), 7)) != b'Ceuta:\0':
                raise ValueError('Dispatcher changes text')
            paths.append(address); machine.emu_stop()

    uc.hook_add(UC_HOOK_CODE, hook)
    uc.emu_start(0x0202425C, stop, count=1000)
    expected = 0x0205473C if selector == 0xFE else 0x02053AC4
    if paths != [expected]:
        raise ValueError('System selector chooses the wrong native consumer')
    return {'selector': selector, 'consumer': expected, 'native_dispatch_executed': True}


def main():
    source = NdsImage.open('out/all_routes_combined_v152_candidate.nds').read_file('/__arm9__.bin')
    config = json.loads(CONFIG.read_text(encoding='utf-8'))
    folder = Path('work/qa/raphael_system_panels'); folder.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (788, 13 * 320), 'white'); draw = ImageDraw.Draw(sheet)
    cases, identifiers = [], []
    for index, record in enumerate(config['records']):
        identifier = f"DK4_MES_B{record['block']:02d}_R{record['segment']:04d}"
        identifiers.append(identifier)
        raw = bytes.fromhex(record['after_hex'])
        if raw[0] != 0xFE:
            raise ValueError('Modal selector missing')
        # The company macro's default expansion is explicit; the native modal consumes this result.
        text = raw[1:].rstrip(b' ').replace(b'FO', b'Castor Co.').decode('ascii')
        for mode in (4, 16):
            native = execute(source, text, modal=True, modal_guarded=True, mode=mode)
            events = [e for e in native['glyph_events'] if e['code'] != 32]
            if [e['code'] for e in events] != [ord(c) for c in text if c not in (' ', '\n')]:
                raise ValueError(f'{identifier}: native modal drops/rearranges text')
            if any(e['x'] < 0 or e['y'] < 0 or e['x'] + 6 > 256 or e['y'] + 12 > 96 for e in events):
                raise ValueError('Tutorial glyph escapes native panel bounds')
            if native['pixels'] != expected_pixels(source, None, native['glyph_events'], mode, background=9):
                raise ValueError('Independent ASCII font pixels differ')
            if not {0x548A8, 0xD5404, 0xD16B4} <= set(native['executed_offsets']):
                raise ValueError('Native modal/glyph pipeline did not execute')
            row_origins = sorted({e['y'] for e in events})
            if len(row_origins) != len(text.split('\n')):
                raise ValueError('Tutorial gains/loses a row')
            cases.append({'id': identifier, 'mode': mode, 'text': text, 'row_origins': row_origins,
                          'pixels_sha256': sha(native['pixels']), 'complete_glyph_order_and_pixels': True})
            if mode == 16:
                pixels = struct.unpack('<49152H', native['pixels'])
                panel = Image.new('RGB', (256, 192))
                panel.putdata([(255, 255, 255) if p == 9 else (0, 0, 0) for p in pixels])
                panel = panel.crop((0, 0, 256, 96)).resize((768, 288), Image.Resampling.NEAREST)
                panel.save(folder / f'{identifier}.png')
                draw.text((10, index * 320 + 5), identifier, fill='black')
                sheet.paste(panel, (10, index * 320 + 24))
    sheet.save(folder / 'native_sheet.png')
    proof = {'renderer_arm9_sha256': sha(source), 'verified_records': identifiers, 'cases': cases,
             'all_glyphs_and_pixels_preserved': True,
             'dispatch': [dispatch(source, selector) for selector in (0xF8, 0xFE)],
             'limitations': 'Separate native dispatch and modal invocations. UI state update, macro expansion, bitmap initialization and physical composition/dismissal are contracts. ASCII glyph requests and independently decoded pixels execute and match. Full emulator frame appearance still requires cold-boot testing.'}
    proof_path = Path(config['native_proof'])
    proof_path.write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    config['native_proof_sha256'] = sha(proof_path.read_bytes())
    CONFIG.write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('13 panels, 26 native modal glyph/pixel cases and FE/F8 dispatcher branches pass.')


if __name__ == '__main__':
    main()
