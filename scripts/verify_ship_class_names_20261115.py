"""Verify the Standard Shipyard list, both detail fields and the native ship catalogue."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import stage_ship_class_names_20261115 as stage
from scripts.stage_special_target_labels_20261115 import c_string
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_plaque_release_v247 import find_mask


base, ROOT = stage.base, stage.ROOT
OUTPUT, SHEET = ROOT / 'shipyard_verification.json', ROOT / 'shipyard_comparison.png'
SELECTED = {5689: 5, 6489: 20, 6809: 22}
DESIGNS = {5: 55, 20: 70, 22: 72}
FIELDS = ((12, 7, 126, 18), (126, 7, 228, 18))
LIST_ROWS = tuple((32, y, 129, y + 11) for y in (209, 245, 281, 317))


def preserve_catalogue(roms, snapshots):
    classes, designs, anchors = {}, {}, {}
    arm9 = [rom.read_file(stage.ARM) for rom in roms]
    for arm, raw in zip(arm9, snapshots, strict=True):
        cpu, get = get_machine(arm, raw)
        class_root, design_root = get(0xCB154), get(0xCB148)
        if anchors:
            assert anchors == dict(class_root=class_root, design_root=design_root)
        anchors.update(class_root=class_root, design_root=design_root)
        mode = len(classes)
        classes[mode] = []
        for i in range(39):
            owner = class_root + 4 + 64 * i
            address = get(0x1FD74, owner)
            assert address == unpack_from('<I', arm, 0x11C7A8 + 56 * i)[0]
            classes[mode].append(c_string(cpu, address, 'ascii'))
        designs[mode] = [bytes(cpu.mem_read(design_root + 4 + 140 * i, 140)) for i in range(155)]
        for cls, index in DESIGNS.items():
            owner = design_root + 4 + 140 * index
            vtable = unpack_from('<I', designs[mode][index])[0]
            getter = unpack_from('<I', raw, vtable + 4 - stage.BASE)[0]
            assert get(getter - stage.BASE, owner) == owner + 8 and get(0x11DB0, owner) == cls
    changes = {n for n, (a, b) in enumerate(zip(*classes.values(), strict=True)) if a != b}
    assert changes == set(DESIGNS)
    changes = {n for n, (a, b) in enumerate(zip(*designs.values(), strict=True)) if a != b}
    assert changes == set(DESIGNS.values())
    observed = []
    for cls, *_, previous, current in stage.RECORDS:
        index = DESIGNS[cls]
        for mode, text in enumerate((previous, current)):
            assert classes[mode][cls]['text'] == text
            assert designs[mode][index][8:27] == text.encode('ascii').ljust(19, b'\0')
        old, new = (designs[mode][index] for mode in (0, 1))
        assert old[:8] + old[27:] == new[:8] + new[27:]
        observed.append(dict(class_id=cls, model_id=index, before=classes[0][cls], after=classes[1][cls],
                             design_runtime_address=anchors['design_root'] + 4 + 140 * index))
    return dict(classes_compared=39, models_compared=155, changed_labels=observed, **anchors)


def strip_owned_text(diff, font, text, im, bounds):
    mask = find_mask(font, text, im, bounds)
    x, y, right, bottom = mask['bounds']
    expected_ink = set()
    for i, char in enumerate(text):
        glyph = font.decode(char)
        expected_ink.update((x + i * 6 + dx, y + dy) for dx in range(6) for dy in range(11)
                            if glyph.getpixel((dx, dy)))
    assert len(expected_ink) == mask['ink_pixels'] and right - x == 6 * len(text) and bottom - y == 11
    for point in expected_ink:
        diff.putpixel(point, (0, 0, 0))
    return mask


def main():
    assert not OUTPUT.exists() and not SHEET.exists()
    stage_info = base.load(stage.STORED)
    paths = (stage.parent.ROM, stage.ROM)
    assert [base.digest(path) for path in paths] == [stage_info[key] for key in ('previous_sha256', 'candidate_sha256')]
    roms = list(map(base.NdsImage.open, paths))
    font = GameAsciiFont.from_arm9(roms[1].read_file(stage.ARM))
    names = {row[0]: row[-2:] for row in stage.RECORDS}
    reports, evidence, ram = [], {}, []
    for version, path in zip(('parent', 'staged'), paths, strict=True):
        folder = ROOT / f'standard_list_{version}'
        report_path = folder / 'capture_report.json'
        report = base.load(report_path)
        assert report['ROM_sha256'] == base.digest(path) and report['frames'] in (9000, 9001)
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not any(v for key, v in report.items() if key.startswith('synthetic_'))
        source = report['battery_save_preloaded']
        assert source['copied_byte_exact_before_cold_boot'] and base.digest(source['source']) == source['source_sha256']
        evidence.update({str(report_path): base.digest(report_path), source['source']: source['source_sha256']})
        rows = shots(report)
        snapshot = next(row for row in report['read_only_capture_RAM_snapshots'] if row['frame'] == 5689)
        data = Path(snapshot['path']).read_bytes()
        assert snapshot['read_only_export'] and stage.sha256(data).hexdigest() == snapshot['sha256']
        evidence[snapshot['path']] = snapshot['sha256']
        ram.append(data)
        reports.append((report, {frame: row for frame, row in rows.items() if 5000 <= frame <= 9000}))
    (a, before), (b, after) = reports
    assert before.keys() == after.keys()
    for key in ('scripted_input_schedule', 'core_DLL_sha256', 'core_options'):
        assert a[key] == b[key]
    assert a['battery_save_preloaded']['source_sha256'] == b['battery_save_preloaded']['source_sha256']
    native = preserve_catalogue(roms, ram)
    details, unchanged, list_names, panels = {}, [], set(), {}
    for frame in sorted(before):
        old, new = [captured(row) for row in (before[frame], after[frame])]
        evidence.update({row['path']: row['PNG_sha256'] for row in (before[frame], after[frame])})
        diff = ImageChops.difference(old, new)
        if not diff.getbbox():
            unchanged.append(frame)
            continue
        locations = []
        for cls, pair in names.items():
            for box in (*FIELDS, *LIST_ROWS):
                if diff.crop(box).getbbox() is None:
                    continue
                try:
                    find_mask(font, pair[0], old, box)
                    find_mask(font, pair[1], new, box)
                except ValueError:
                    continue
                first = strip_owned_text(diff, font, pair[0], old, box)
                last = strip_owned_text(diff, font, pair[1], new, box)
                locations.append(dict(class_id=cls, old=first, new=last, field=list(box)))
                if box in LIST_ROWS:
                    list_names.add(cls)
        assert diff.getbbox() is None, (frame, diff.getbbox())
        details[frame] = locations
        if frame in SELECTED:
            cls = SELECTED[frame]
            assert {tuple(row['field']) for row in locations if row['class_id'] == cls} >= set(FIELDS)
            panels[frame] = old, new
    assert set(SELECTED) == panels.keys() and list_names == set(DESIGNS)
    assert {5000, 8609, 8909, 9000} <= set(unchanged)
    galley = [find_mask(font, 'Galley', captured(after[6649]), box) for box in FIELDS]
    # Include the whole two-screen frame at native size so both detail fields,
    # every visible row and adjacent controls can be reviewed together.
    sheet = Image.new('RGB', (768, 814), '#252830')
    draw = ImageDraw.Draw(sheet)
    for col, (frame, (old, new)) in enumerate(panels.items()):
        for row, image in enumerate((old, new)):
            x, y = col * 256, row * 407
            draw.text((x + 5, y + 3), f'{names[SELECTED[frame]][row]}   {frame}', fill='white')
            sheet.paste(image, (x, y + 18))
    sheet.save(SHEET)
    base.save(OUTPUT, dict(candidate_sha256=stage_info['candidate_sha256'], catalogue=native,
        verified_label_locations=details, adjacent_galley_retention=galley, unchanged_frames=unchanged,
        verified_mast_price_durability_and_navigation_pixels=True, ordinary_standard_list_navigation=True,
        no_purchase=True, hardware=False, sheet_sha256=base.digest(SHEET), evidence=evidence))
    print(f'Verified {sum(map(len, details.values()))} complete label pairs and {len(unchanged)} unchanged control frames.')


if __name__ == '__main__':
    main()
