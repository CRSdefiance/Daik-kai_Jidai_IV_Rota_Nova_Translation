"""Locate actual FE row drift with the unchanged native painter; no formatting approval."""
from pathlib import Path
from types import FunctionType
from PIL import Image, ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.registered_editorial_runtime import RegisteredRuntime
from scripts import square_shopkeeper_font_oracles_v7020 as old_font
from scripts import Rafael_B45_FE_source_painter_v7894 as source_FE

ROOT = Path('work/analysis/Hodram_B171_B190_FE_diagnostic_20261104')
PLAN = Path('work/analysis/Hodram_B171_B190_formatting_20261102/initial/automatic_plans.json')
RELEASE = Path('work/analysis/Hodram_B151_B170_release_verified_20261102/registered_release_verification.json')


if __name__ == '__main__':
    assert not ROOT.exists()
    ctx = RegisteredRuntime(RELEASE, RELEASE.with_name('own_registered_startup_verification.json'))
    ascii_factory = FunctionType(old_font.make_painter.__code__, {**old_font.make_painter.__globals__, 'CURRENT_ARM9': sha(ctx.arm)}, argdefs=old_font.make_painter.__defaults__)
    factory = FunctionType(source_FE.make_source_painter.__code__, {**source_FE.make_source_painter.__globals__, 'CURRENT_ARM9': sha(ctx.arm), 'ASCII_painter': ascii_factory}, argdefs=source_FE.make_source_painter.__defaults__)
    painter, calibration = factory(ctx.image)
    ROOT.mkdir()
    rows, pictures = [], []
    for row in load(PLAN)['records']:
        if row['kind'] != 'system-FE':
            continue
        raw = bytes.fromhex(row['encoded_hex'])[1:]
        expanded = raw.replace(b'FI', b'Hodram').replace(b'FA', b'Bergstrom').replace(b'FO', b'Bergstrom Fleet')
        rendered = painter(expanded)
        target = [line.strip(b' ') for line in expanded.split(b'\n')]
        events = rendered['events']
        assert all(e['kind'] == 'ascii' for e in events)
        ys = sorted({e['y'] for e in events})
        actual = [bytes(e['code'] for e in events if e['y'] == y).strip(b' ') for y in ys]
        matches = ys == list(range(0, 12 * len(target), 12)) and actual == target
        plane = rendered.pop('physical')
        logical = rendered.pop('logical')
        path = ROOT / (row['id'] + '.bin')
        path.write_bytes(plane)
        picture = Image.new('RGB', (228, 64))
        picture.putdata([(0, 8, 0) if v else (239, 232, 201) for v in plane])
        preview = path.with_suffix('.png')
        picture.save(preview)
        pictures.append((row['id'] + (' PASS' if matches else ' ROW DRIFT'), picture))
        rows.append(dict(id=row['id'], planned_rows=[v.decode('ascii') for v in target],
            actual_row_origins=ys, actual_rows=[v.decode('ascii') for v in actual],
            row_membership_matches=matches, native_plane=str(path), native_plane_sha256=sha(plane),
            native_logical_plane_sha256=sha(logical), preview=str(preview), native=rendered))
    sheets = []
    for at in range(0, len(pictures), 12):
        part = pictures[at:at + 12]
        sheet = Image.new('RGB', (912, ((len(part) + 1) // 2) * 160), '#263238')
        draw = ImageDraw.Draw(sheet)
        for i, (label, picture) in enumerate(part):
            x, y = i % 2 * 456, i // 2 * 160
            draw.text((x + 3, y + 3), label, fill='white')
            sheet.paste(picture.resize((456, 128), Image.Resampling.NEAREST), (x, y + 24))
        path = ROOT / f'FE_part{at // 12 + 1}.png'
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=sha(path.read_bytes())))
    failed = [r['id'] for r in rows if not r['row_membership_matches']]
    save(ROOT / 'row_diagnostic.json', dict(records=rows, failed_IDs=failed, runtime=ctx.receipt(),
        calibration=calibration, review_sheets=sheets, native_font_andgeometry_unchanged=True,
        diagnosis_not_fifth_gate_approval=True, actual_gameplay=False, new_credit=0,
        evidence={str(p): sha(p.read_bytes()) for p in [PLAN, Path(__file__)]}))
    print(dict(FE_records=len(rows), row_drift=failed, native_width_228_unchanged=True))
