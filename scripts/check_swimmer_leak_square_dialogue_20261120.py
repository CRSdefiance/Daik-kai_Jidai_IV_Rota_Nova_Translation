"""Verify the visible dialogue and transitions on the staged shared-text ROM."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw

from scripts import replay_swimmer_leak_square_dialogue_20261120 as replay
from scripts import stage_swimmer_leak_square_dialogue_20261120 as stage
from scripts.verify_london_stockholm_dialogue_20261115 import native_hold


ROOT = Path('E:/Rota Nova translations/Generated/work/swimmer_leak_square_dialogue_20261120_v2')
PROOF, SHEET = stage.ROOT / 'gameplay.json', stage.ROOT / 'gameplay.png'
HOLDS = {'mermaid': ((9627, 448), (9827, 449)), 'leak': ((9627, 573),),
         'square-war': ((5900, 682),), 'square-sunk': ((5900, 687),)}
TRANSITIONS = {'mermaid': (10027, 'New port sighting'), 'leak': (9827, 'Sailing resumed'),
               'square-war': (6250, 'Returned to Square'), 'square-sunk': (6250, 'Returned to Square')}


def digest(path):
    return stage.digest(Path(path).read_bytes())


def one_frame(report, frame):
    shots = [row for row in report['frames_captured'] if row['frame'] == frame]
    assert shots and len({row['framebuffer_sha256'] for row in shots}) == 1, frame
    shot = shots[0]
    assert digest(shot['path']) == shot['PNG_sha256']
    return shot, Image.open(shot['path']).convert('RGB')


def ram_at(report, frame):
    item, = [item for item in report['read_only_pause_RAM_snapshots'] if item['frame'] == frame]
    ram = Path(item['path']).read_bytes()
    assert len(ram) == 0x400000 and item['read_only_export'] and stage.digest(ram) == item['sha256']
    return item, ram


def main(square_only=False):
    proof_path, sheet_path = ((stage.ROOT / 'square_gameplay.json', stage.ROOT / 'square_gameplay.png')
                              if square_only else (PROOF, SHEET))
    assert not proof_path.exists() and not sheet_path.exists()
    scoped = {case: holds for case, holds in HOLDS.items() if not square_only or case in replay.TOWN}
    stored = stage.load(stage.ROOT / 'staging.json')
    assert digest(stage.ROM) == stored['candidate_sha256']
    image = stage.NdsImage.open(stage.ROM)
    arm, kanji = [image.read_file(path) for path in (stage.ARM, '/GRP/KANJI.FNT')]
    raster, _, _ = stage.font_tools(image)
    input_addr, display_addr = [unpack_from('<I', arm, offset)[0] - 0x02000000 for offset in (0x5444C, 0x54450)]
    source_rows = {row['message_ID']: row for row in stored['records']}
    panel_count = sum(map(len, scoped.values())) + len(scoped)
    sheet = Image.new('RGB', (1040, 405 * ((panel_count + 1) // 2)), '#242932')
    draw = ImageDraw.Draw(sheet)
    count = 0
    evidence = {}
    observations = {}
    square_return = []
    for case, holds in scoped.items():
        folder = ROOT / ('square_retry_v1' if case in replay.TOWN else 'sea_retry_v3') / case
        terminal_path = folder / 'terminal.json'
        terminal = stage.load(terminal_path)
        report_path = Path(terminal['capture'])
        assert digest(report_path) == terminal['capture_sha256']
        report = stage.load(report_path)
        assert report['ROM_sha256'] == terminal['candidate_sha256'] == stored['candidate_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert {k for k, v in report.items() if k.startswith('synthetic_') and v} == {'synthetic_condition_fixtures'}
        donor = report['battery_save_preloaded']
        assert donor['copied_byte_exact_before_cold_boot']
        assert digest(donor['source']) == terminal['save_sha256'] == donor['source_sha256']
        journal_path = report_path.with_name('navigation_command_journal.json')
        journal = stage.load(journal_path)['commands_received']
        assert all(row['validation_passed'] for row in journal)
        source, _, _, end, inputs, commands, _, setter = replay.plan(case, anchored=case not in replay.TOWN)
        assert digest(source) == terminal['prior_capture_sha256']
        assert [x['command'] for x in journal] == list(commands)
        added_inputs = [dict(start=row['frame'] + 1, duration=row['command']['duration'],
                             buttons=row['command']['buttons']) for row in journal if row['command'].get('buttons')]
        assert report['scripted_input_schedule'] == inputs + added_inputs and report['frames'] == end
        fixtures = []
        for command in journal:
            request = command['command'].get('condition_fixture')
            if request is not None:
                frame = command['frame']
                snap, ram = ram_at(report, frame)
                _, body = setter(arm, ram, request)
                fixtures.append(body | {'frame': frame})
                evidence[snap['path']] = snap['sha256']
        assert fixtures == report['synthetic_condition_fixtures']
        evidence.update({str(path): digest(path) for path in (report_path, terminal_path, journal_path)})

        seen = []
        panels = []
        for frame, number in holds:
            row = source_rows[number]
            case_data, = row['native_displays']
            display = bytes.fromhex(case_data['display_hex'])
            if case not in replay.TOWN:
                snap, ram = ram_at(report, frame)
                evidence[snap['path']] = snap['sha256']
                actual = ram[input_addr:input_addr + 256].split(b'\0', 1)[0]
                assert actual.hex() == row['staged_hex']
                assert ram[display_addr:display_addr + 256].split(b'\0', 1)[0] == display
            pixels, glyphs = stage.render_portrait(raster, arm, kanji, display)
            assert stage.digest(pixels) == case_data['complete_ink_sha256'] and len(glyphs) == case_data['glyph_count']
            shot, panel = one_frame(report, frame)
            ink = native_hold(panel, pixels)
            evidence[shot['path']] = shot['PNG_sha256']
            seen.append(dict(message_ID=number, frame=frame, complete_ink_pixels=ink,
                             lines=case_data['visible_lines'], image=shot))
            panels.append((panel, f'{case} / COMMON {number}'))
        frame, label = TRANSITIONS[case]
        shot, panel = one_frame(report, frame)
        evidence[shot['path']] = shot['PNG_sha256']
        if case == 'mermaid':
            snap, ram = ram_at(report, frame)
            assert b' '.join(ram[display_addr:display_addr + 256].split(b'\0', 1)[0].split()) == b"Admiral, we've spotted a port!"
            assert ram[replay.fleet.earlier.FIELD - 0x02000000:][:4] == replay.fleet.earlier.ORIGINAL
            evidence[snap['path']] = snap['sha256']
        elif case == 'leak':
            final = report['read_only_RAM_snapshot']
            ram = Path(final['path']).read_bytes()
            assert stage.digest(ram) == final['sha256']
            assert ram[replay.leak.FIELD - 0x02000000:][:4] == replay.leak.ORIGINAL
            assert not any(panel.getpixel((x, y)) == (0, 8, 0) for x in range(16, 244) for y in range(296, 360))
            evidence[final['path']] = final['sha256']
        else:
            assert fixtures[0]['original_shop_selection'] == holds[0][1]
            square_return.append(panel.crop((0, 217, 256, 384)).tobytes())
        panels.append((panel, f'{case} / {label}'))
        for photo, caption in panels:
            x, y = (count % 2) * 520, (count // 2) * 405
            draw.text((x + 4, y + 3), caption, fill='white')
            sheet.paste(photo.crop((0, 192, 256, 384)).resize((512, 384), Image.Resampling.NEAREST), (x + 4, y + 17))
            count += 1
        observations[case] = dict(holds=seen, transition=dict(label=label, image=shot), fixtures=fixtures)
    assert len(square_return) == 2 and square_return[0] == square_return[1]
    sheet.save(sheet_path)
    evidence[str(sheet_path)] = digest(sheet_path)
    stage.write(proof_path, dict(candidate_sha256=stored['candidate_sha256'], observations=observations,
                                initialized_gameplay=True, natural_condition_selection=False, hardware=False,
                                changed_records_observed=sorted({n for holds in scoped.values() for _, n in holds} & stage.EDITS.keys()),
                                evidence=evidence))
    print(f'{sum(map(len, scoped.values()))} exact body masks and {len(scoped)} scene transitions verified.')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--square-only', action='store_true')
    main(parser.parse_args().square_only)
