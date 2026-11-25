"""Verify the route chart and detailed Market Info atlas on the combined ROM."""

from pathlib import Path
from struct import pack, unpack_from

from PIL import Image, ImageChops, ImageDraw
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.city_status_labels import NAMES
from scripts import check_town_chart_native_20261120 as chart
from scripts import stage_market_report_status_20261120 as stage
from scripts.check_swimmer_leak_square_dialogue_20261120 import one_frame, ram_at
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.probe_button_prompt_native import STACK, VIEW
from scripts.stage_town_shortage_20261119 import TOWN_ROW
from scripts.verify_forces_relationships_20261115 import HEADER, font_points
from scripts.verify_personal_gameplay_v841 import get_machine


ROOT = Path('E:/Rota Nova translations/Generated/work/town_chart_punctuation_20261120')
PROOF, SHEET = stage.ROOT / 'verification.json', stage.ROOT / 'town_chart_report.png'
batch, digest = stage.batch, stage.parent.base.digest
BASE, ATLAS_WIDTH, ATLAS_HEIGHT = (chart.BASE, 228, 72)
PIXELS = ATLAS_WIDTH * ATLAS_HEIGHT // 2
CTX, MODEL = STACK + 0x24, 0x02470000
COLOR = (230, 230, 230)
HEADING_COLOR = (197, 198, 197)
REPORTS = (12600, 16100)
CHARTS = (12280, 12980, 14700, 14970, 15260, 15500, 15800, 16420)
CONTROLS = (13280, 13580, 13880, 14030, 14180, 14430)
TERMINAL = 16420


def native_atlas(arm, raw):
    cpu, get = get_machine(arm, raw)
    font = GameAsciiFont.from_arm9(arm)
    header = pack('<5I', 4, ATLAS_WIDTH // 4, ATLAS_HEIGHT, 20, 20)
    cpu.mem_write(HEADER - 16, b'\xa5' * 16 + header + bytes(PIXELS) + b'\xa5' * 16)
    get(0xD3D80, VIEW)
    cpu.mem_write(STACK, pack('<4I', ATLAS_WIDTH, ATLAS_HEIGHT, 0, 0))
    get(0xD3AFC, VIEW, HEADER, 0, 0)
    get(0xD5160, CTX, VIEW, 1)
    assert unpack_from('<7i', arm, TOWN_ROW)[3:] == (120, 12, 48, 12)
    descriptors = stage.headings.rectangles(arm)
    assert descriptors[2][3:] == (120, 12, 48, 12) and descriptors[6][5:] == (0, 0)
    out = []
    for n in (*range(13), 255):
        value = NAMES[n] if n < 13 else 'Normal'
        compact = 'Shortage' if len(value) >= 8 else value
        cpu.mem_write(HEADER + 20, bytes(PIXELS))
        cpu.mem_write(CTX + 0x24, pack('<2I', 84, 60))
        cpu.mem_write(CTX + 0x30, pack('<I', 14))
        get(0xD5404, CTX, BASE + stage.headings.PACKED)
        # The game draws the value into the atlas shared by Town Summary and
        # Market Info. Only the consumer rectangle differs.
        town = bytearray(0x80)
        town[0x6A] = n
        cpu.mem_write(MODEL, bytes(town))
        cpu.mem_write(CTX + 0x30, pack('<I', 1))
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.reg_write(UC_ARM_REG_R8, MODEL)
        cpu.reg_write(UC_ARM_REG_R9, BASE + 0x11A65C)
        cpu.emu_start(0x020B61EC, 0x020B6220, count=100000)
        assert cpu.reg_read(UC_ARM_REG_PC) == 0x020B6220
        actual = bytes(pix for b in cpu.mem_read(HEADER + 20, PIXELS) for pix in (b & 15, b >> 4))
        assert cpu.mem_read(HEADER - 16, 16) == cpu.mem_read(HEADER + 20 + PIXELS, 16) == b'\xa5' * 16
        for i, text in ((2, compact), *enumerate(stage.headings.HEADINGS, 11)):
            _, dx, dy, sx, sy, w, h = descriptors[i]
            assert len(text) * 6 <= w and dx + w <= 256
            expected = font_points(font, text, sx, sy + 1)
            samples = {(x, y) for y in range(sy, sy + h) for x in range(sx, sx + w)
                       if actual[y * ATLAS_WIDTH + x]}
            assert expected == samples, (n, text)
        out.append(dict(original_status_code=n, original_name=value, compact_value=compact,
                        exact_atlas_render_and_copies=True, atlas_sha256=batch.digest(actual)))
    return out


def rect_masks(image, font, frame):
    count = {}

    def check(name, text, x, y, w, color=COLOR):
        count[name] = font_mask(image, font, text, x, y + 1, (x, y, x + w, y + 12), color)

    if frame in REPORTS:
        for name, x, y, w in (('Type', 32, 26, 24), ('Status', 148, 26, 36),
                              ('Growth', 32, 58, 36), ('Arms', 160, 58, 36)):
            check(name, name, x, y, w, HEADING_COLOR)
        if frame == 16100:
            check('Value', 'Normal', 192, 26, 48)
        else:
            assert COLOR not in image.crop((192, 26, 240, 38)).get_flattened_data()
        assert COLOR not in image.crop((152, 112, 224, 124)).get_flattened_data()
        return count
    if frame in (12280, 12980):
        title = 'Lisbon (N38 W8)'
        x = 128 - 3 * len(title)
        check('Coordinates', title, x, 2, 6 * len(title))
        if frame == 12280:
            for y, text in ((96, ' 50%'), (124, ' 20%')):
                check(text, text, chart.SHARE_X, y, 6 * len(text))
        else:
            for x, y in chart.UNKNOWN:
                check(f'Unknown {x}/{y}', ' ? ', x, y, 18)
    return count


def main():
    assert not PROOF.exists() and not SHEET.exists()
    stored = batch.load(stage.PROOF)
    prior, first, middle, final = paths = [ROOT / side / 'capture/capture_report.json'
                                           for side in ('current', 'revised', 'combined', 'final')]
    reports = [batch.load(path) for path in paths]
    arms = [batch.NdsImage.open(p).read_file(batch.ARM)
            for p in (stage.parent.ROM, stage.headings.chart.ROM, stage.headings.ROM, stage.ROM)]
    identities = [stored[k] for k in ('parent_sha256', 'charts_only_sha256', 'charts_and_headings_sha256', 'candidate_sha256')]
    docs = {str(path): digest(path) for path in paths}
    journals, fixture_changes = [], []
    for i, (path, report, identity) in enumerate(zip(paths, reports, identities, strict=True)):
        assert report['ROM_sha256'] == identity and report['frames'] == TERMINAL
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['scripted_input_schedule'] == reports[0]['scripted_input_schedule']
        assert report['core_DLL_sha256'] == reports[0]['core_DLL_sha256'] and report['core_options'] == reports[0]['core_options']
        donor = report['battery_save_preloaded']
        assert donor['copied_byte_exact_before_cold_boot'] and digest(donor['source']) == donor['source_sha256']
        fixture = report['synthetic_condition_fixtures']
        assert [(x['mode'], x['frame']) for x in fixture] == [('conceal', 12280), ('restore', 12980)]
        a, b = [record['changes'][0] for record in fixture]
        assert a == dict(address=b['address'], before=b['after'], after=b['before']) and a['before'] ^ a['after'] == 2
        assert all(len(r['changes']) == 1 and r['only_original_information_condition_changed'] for r in fixture)
        fixture_changes.append([a, b])
        j = path.with_name('navigation_command_journal.json')
        commands = batch.load(j)['commands_received']
        assert all(r['validation_passed'] for r in commands)
        journals.append(commands)
        docs[str(j)] = digest(j)
    assert all(x == journals[0] for x in journals) and all(x == fixture_changes[0] for x in fixture_changes)
    seed, raw = ram_at(reports[-1], 16100)
    docs[seed['path']] = seed['sha256']
    atlas = native_atlas(arms[-1], raw)
    font = GameAsciiFont.from_arm9(arms[-1])
    sheet = Image.new('RGB', (1032, 4 * 206), '#263238')
    draw = ImageDraw.Draw(sheet)
    frames = (12280, 12980, *REPORTS)
    evidence = []
    for frame in sorted(set(CHARTS + REPORTS + CONTROLS)):
        controls = [one_frame(report, frame) for report in reports]
        for sample, _ in controls:
            docs[sample['path']] = sample['PNG_sha256']
        old, chart_only, headings, revised = [im for _, im in controls]
        diff = ImageChops.difference(old, revised)
        if frame in REPORTS:
            assert ImageChops.difference(old, chart_only).getbbox() is None
            assert diff.getbbox()
            for box in ((148, 26, 240, 38), (32, 58, 70, 70), (160, 58, 196, 70), (152, 112, 224, 124)):
                diff.paste((0, 0, 0), box)
        elif frame in CHARTS:
            assert ImageChops.difference(chart_only, headings).getbbox() is None
            assert ImageChops.difference(headings, revised).getbbox() is None
            for box in ((0, 2, 256, 14), (99, 96, 130, 108), (99, 124, 130, 136),
                        *((x, y, x + 24, y + 12) for x, y in chart.UNKNOWN)):
                diff.paste((0, 0, 0), box)
        assert diff.getbbox() is None, (frame, diff.getbbox())
        masks = rect_masks(revised, font, frame)
        if masks:
            evidence.append(dict(frame=frame, masks=masks))
        if frame in frames:
            y = 206 * frames.index(frame)
            for side, screen in enumerate((old, revised)):
                x = side * 516
                caption = ('Previous', 'Revised')[side]
                state = {12280: 'Known town chart', 12980: 'Unknown town chart', 12600: 'Report with information hidden',
                         16100: 'Report with Normal status'}[frame]
                draw.text((x + 5, y + 3), f'{caption}  /  {state}', fill='white')
                panel = screen.crop((0, 0, 256, 124 if frame in REPORTS else 138))
                sheet.paste(panel.resize((335, 182 if frame not in REPORTS else 164), Image.Resampling.NEAREST), (x + 2, y + 19))
    sheet.save(SHEET)
    batch.write(PROOF, dict(candidate_sha256=stored['candidate_sha256'], previous_sha256=stored['parent_sha256'],
        original_stock_status_cases=atlas, actual_emulator_masks=evidence, fixture_only_information_bit=fixture_changes[-1],
        intact_market_and_world_map_returns=CONTROLS, matches_chart_only_stage_on_all_chart_frames=True,
        actual_endpoint=TERMINAL, sheet=str(SHEET), sheet_sha256=digest(SHEET), evidence=docs, hardware=False))
    print('Four paired display states and 14 native status atlas cases passed.')


if __name__ == '__main__':
    main()
