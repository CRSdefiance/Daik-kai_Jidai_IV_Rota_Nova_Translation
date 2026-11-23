"""Check the complete catalogue and native font for the staged ship names."""

from argparse import ArgumentParser
from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import stage_specialized_ship_labels_20261115 as stage
from scripts.stage_special_target_labels_20261115 import c_string
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_ship_class_names_20261115 import strip_owned_text


base = stage.base
OUTPUT = stage.OUTPUT.with_name('specialized_ship_labels_native_20261115_v1.json')
SHEET = stage.ROOT / 'specialized_ship_native_font.png'
FOCUSED = stage.ROOT / 'focused_shipyard_verification.json'
COMPARISON = stage.ROOT / 'focused_shipyard_comparison.png'


def snapshot(version, identity, arm):
    report = stage.ROOT / f'istanbul_special_{version}' / 'capture_report.json'
    capture = base.load(report)
    assert capture['ROM_sha256'] == identity and capture['cold_boot'] and not capture['savestate_loaded']
    assert not capture['callback_errors'] and capture['frames'] == 9001
    assert not any(value for key, value in capture.items() if key.startswith('synthetic_'))
    donor = capture['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    row = next(entry for entry in capture['read_only_capture_RAM_snapshots'] if entry['frame'] == 5000)
    assert row['read_only_export'] and base.digest(row['path']) == row['sha256']
    return get_machine(arm, Path(row['path']).read_bytes()), capture, {str(report): base.digest(report),
        row['path']: row['sha256'], donor['source']: donor['source_sha256']}


def get_catalogue(machine, arm):
    cpu, get = machine
    classes, designs = get(0xCB154), get(0xCB148)
    class_rows = []
    for index in range(39):
        addr = get(0x1FD74, classes + 4 + 64 * index)
        assert addr == unpack_from('<I', arm, stage.class_field(index))[0]
        class_rows.append(c_string(cpu, addr, 'cp932'))
    raw_designs = [bytes(cpu.mem_read(designs + 4 + 140 * index, 140)) for index in range(155)]
    return class_rows, raw_designs, designs


def native_sheet(arm, rows):
    font = GameAsciiFont.from_arm9(arm)
    image = Image.new('RGB', (384, len(rows) * 45 + 5), '#152029')
    draw = ImageDraw.Draw(image)
    results = []
    for index, row in enumerate(rows):
        text, top = row['english'], 6 + index * 45
        ink = Image.new('1', (len(text) * 6, 11))
        for i, char in enumerate(text):
            glyph = font.decode(char)
            assert char == ' ' or glyph.getbbox()
            ink.paste(glyph.convert('1'), (i * 6, 0))
        assert len(text.encode('ascii')) <= 18
        assert ink.crop((0, 0, 6, 11)).getbbox() and ink.crop((ink.width - 6, 0, ink.width, 11)).getbbox()
        draw.text((4, top), row['id'], fill='#D4E0E5')
        enlarged = ink.resize((ink.width * 2, 22), Image.Resampling.NEAREST)
        image.paste('#FAFAFA', (4, top + 14, 4 + enlarged.width, top + 36), enlarged)
        results.append(dict(id=row['id'], font_width=ink.width, first_and_last_glyph_complete=True,
             native_text_storage_bytes=len(text.encode('ascii')) + 1, single_row_offline_preview=True))
    image.save(SHEET)
    return results


def main():
    assert not OUTPUT.exists() and not SHEET.exists()
    manuscript, release = map(base.load, (stage.OUTPUT, stage.parent.RELEASE))
    before, after = stage.parent.ROM, stage.ROM
    assert base.digest(before) == manuscript['previous_sha256'] == release['candidate_sha256']
    assert base.digest(after) == manuscript['candidate_sha256']
    raw = [base.NdsImage.open(path).read_file(stage.ARM) for path in (before, after)]
    assert stage.sha256(raw[1]).hexdigest() == manuscript['target_ARM9_sha256']
    prior, first, evidence = snapshot('parent', release['candidate_sha256'], raw[0])
    tested, second, dependencies = snapshot('staged', manuscript['candidate_sha256'], raw[1])
    assert first['scripted_input_schedule'] == second['scripted_input_schedule']
    assert first['battery_save_preloaded']['source_sha256'] == second['battery_save_preloaded']['source_sha256']
    assert first['core_DLL_sha256'] == second['core_DLL_sha256']
    pngs = [{row['frame']: row['framebuffer_sha256'] for row in run['frames_captured']} for run in (first, second)]
    assert pngs[0] == pngs[1]
    old_classes, old_designs, old_root = get_catalogue(prior, raw[0])
    classes, models, root = get_catalogue(tested, raw[1])
    assert old_root == root
    assert {i for i, (a, b) in enumerate(zip(old_classes, classes, strict=True)) if a != b} == {15, 32}
    expected = {}
    for row in manuscript['records']:
        name = row['english']
        for ref in row['source_references']:
            offset = ref['pointer_field']
            if stage.class_field(0) <= offset <= stage.class_field(38):
                assert classes[(offset - stage.class_field(0)) // 56]['text'] == name
            else:
                index = 50 + (offset - stage.design_field(50)) // 44
                expected[index] = name
    changed = {i for i, (a, b) in enumerate(zip(old_designs, models, strict=True)) if a != b}
    assert changed == {65, 82, 89, 95, 101, 106, 107, 108, 113, 129}
    for index, label in expected.items():
        a, b = old_designs[index], models[index]
        assert b[8:27] == label.encode('ascii').ljust(19, b'\0')
        assert a[:8] + a[27:] == b[:8] + b[27:]
        table = unpack_from('<I', b)[0]
        getter = unpack_from('<I', tested[0].mem_read(table + 4, 4))[0]
        pointer = tested[1](getter - stage.BASE, root + 4 + index * 140)
        assert c_string(tested[0], pointer, 'ascii')['text'] == label

    previews = native_sheet(raw[1], manuscript['records'])
    base.save(OUTPUT, dict(candidate_sha256=manuscript['candidate_sha256'], previous_sha256=release['candidate_sha256'],
        class_getters_compared=len(classes), initialized_models_compared=len(models), complete_model_labels=expected,
        modified_designs=sorted(changed), modified_classes=[15, 32], unchanged_actual_frame_count=len(pngs[0]),
        matched_cold_boot_special_purchase_entry=True, revised_product_selected_in_gameplay=False,
        offline_previews=previews, sheet=str(SHEET), sheet_sha256=base.digest(SHEET),
        evidence=evidence | dependencies | {str(stage.OUTPUT): base.digest(stage.OUTPUT)}))
    print(f'Verified {len(classes)} class getters, {len(models)} models, {len(previews)} font previews, '
          f'and {len(pngs[0])} control frames.')


def verify_focused():
    assert not FOCUSED.exists() and not COMPARISON.exists()
    native = base.load(OUTPUT)
    assert base.digest(stage.ROM) == native['candidate_sha256']
    font = GameAsciiFont.from_arm9(base.NdsImage.open(stage.ROM).read_file(stage.ARM))
    evidence, verified, omitted = {}, [], []
    for model, attempt in ((65, 1), (82, 1), (107, 2)):
        paths = [stage.ROOT / f'focused_{model}_{version}_{attempt}/capture/capture_report.json'
                 for version in ('parent', 'staged')]
        before, after = map(base.load, paths)
        assert [r['ROM_sha256'] for r in (before, after)] == [native['previous_sha256'], native['candidate_sha256']]
        assert all(r['frames'] == 6500 and r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
                   for r in (before, after))
        for report in (before, after):
            fixture, = report['synthetic_condition_fixtures']
            assert fixture['frame'] == 4500 and fixture['original_catalogue_model'] == model
            assert len(fixture['changes']) == 1
        assert all(before[k] == after[k] for k in ('scripted_input_schedule', 'core_DLL_sha256', 'core_options'))
        evidence.update({str(p): base.digest(p) for p in paths})
        prev, new = map(shots, (before, after))
        assert prev.keys() == new.keys()
        listed = (5209, 5500, 5800)
        for frame in sorted(prev):
            a, b = captured(prev[frame]), captured(new[frame])
            evidence.update({d[frame]['path']: d[frame]['PNG_sha256'] for d in (prev, new)})
            if model != 107 or frame not in listed:
                assert a.tobytes() == b.tobytes(), (model, frame)
                continue
            left, right = 'Transport LgGalley', 'Large Cargo Galley'
            diff = ImageChops.difference(a, b)
            assert diff.getbbox()
            regions = ((0, 0, 126, 24), (29, 190, 237, 209))
            masks = [strip_owned_text(diff, font, text, screen, region)
                     for text, screen in ((left, a), (right, b)) for region in regions]
            assert not diff.getbbox(), (model, frame)
            class_masks = [find_mask(font, 'Large Galley', im, (128, 0, 256, 24)) for im in (a, b)]
            assert class_masks[0] == class_masks[1]
            verified.append(dict(model=model, frame=frame, design_masks=masks, class_mask=class_masks[0]))
            if frame == 5209:
                sheet = Image.new('RGB', (1024, 784), '#263238')
                title = ImageDraw.Draw(sheet)
                title.text((4, 3), 'Previous', fill='white')
                title.text((516, 3), 'Revised', fill='white')
                for i, screen in enumerate((a, b)):
                    sheet.paste(screen.resize((512, 768), Image.Resampling.NEAREST), (i * 512, 16))
                sheet.save(COMPARISON)
        if model != 107:
            omitted.append(model)
    assert len(verified) == 3 and omitted == [65, 82]
    base.save(FOCUSED, dict(candidate_sha256=native['candidate_sha256'], previous_sha256=native['previous_sha256'],
        verified=verified, unlisted_models=omitted, same_pixels_except_complete_design_names=True,
        paired_controlled_model_link_replays=True, ordinary_controller=True, natural_acquisition=False,
        verified_entry_and_returns=True, hardware=False, sheet_sha256=base.digest(COMPARISON), evidence=evidence))
    print('Verified the complete 18-character design name in the Shipyard list and detail heading.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--focused', action='store_true')
    verify_focused() if parser.parse_args().focused else main()
