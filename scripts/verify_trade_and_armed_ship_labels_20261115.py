"""Check every outfitted design and the longest label in the native Shipyard."""

from pathlib import Path
from struct import unpack_from
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import stage_trade_and_armed_ship_labels_20261115 as stage
from scripts import verify_specialized_ship_labels_20261115 as previous
from scripts.stage_special_target_labels_20261115 import c_string
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_ship_class_names_20261115 import strip_owned_text


base, ROOT = stage.base, stage.ROOT
OUTPUT = ROOT / 'design_verification.json'
SHEET = ROOT / 'armed_design_comparison_verified.png'
NATIVE = ROOT / 'armed_design_font.png'
STARTUP = ROOT / 'own_startup_verification.json'
HOLDS = (5209, 5500, 5800)


def startup_machine(arm, report, identity):
    proof = base.load(report)
    assert proof['candidate_sha256'] == identity and proof['cold_boot'] and not proof['savestate']
    snapshot = proof['read_only_snapshot']
    assert snapshot['read_only_export'] and base.digest(snapshot['path']) == snapshot['sha256']
    return get_machine(arm, Path(snapshot['path']).read_bytes()), {
        str(report): base.digest(report), snapshot['path']: snapshot['sha256']}


def verify_catalogue(before, after, prior, staged):
    machines, evidence = [], {}
    for arm, report, identity in ((before, Path(prior['own_registered_startup']), prior['candidate_sha256']),
                                  (after, STARTUP, staged['candidate_sha256'])):
        machine, sources = startup_machine(arm, report, identity)
        machines.append(machine)
        evidence.update(sources)
    a, b = [previous.get_catalogue(machine, arm) for machine, arm in zip(machines, (before, after), strict=True)]
    old_classes, old_designs, old_root = a
    classes, designs, root = b
    assert classes == old_classes and root == old_root
    changed = {i for i, (old, new) in enumerate(zip(old_designs, designs, strict=True)) if old != new}
    assert changed == set(stage.REVISIONS)
    cpu, get = machines[1]
    for row in staged['records']:
        index, name = row['model_id'], row['english']
        old, new = old_designs[index], designs[index]
        assert new[8:27] == name.encode('ascii').ljust(19, b'\0')
        assert old[:8] + old[27:] == new[:8] + new[27:]
        table = unpack_from('<I', new)[0]
        getter = unpack_from('<I', cpu.mem_read(table + 4, 4))[0]
        ptr = get(getter - stage.BASE, root + 4 + 140 * index)
        assert c_string(cpu, ptr, 'ascii')['text'] == name
        assert c_string(cpu, row['target_pointer'], 'ascii')['hex_with_NUL'] == row['target_hex']
    for start, _, expected in stage.NEIGHBORS:
        assert c_string(cpu, stage.BASE + start, 'ascii')['hex_with_NUL'] == expected.hex()
    return dict(catalogue_class_count=len(classes), catalogue_model_count=len(designs),
                changed_models=sorted(changed), reviewed_models=60), evidence


def verify_shipyard(font, previous_sha, candidate):
    reports = [ROOT / f'focused_136_{version}_1/capture/capture_report.json' for version in ('parent', 'staged')]
    evidence = {str(p): base.digest(p) for p in reports}
    old, new = map(base.load, reports)
    assert [r['ROM_sha256'] for r in (old, new)] == [previous_sha, candidate]
    assert all(old[k] == new[k] for k in ('scripted_input_schedule', 'core_DLL_sha256', 'core_options'))
    for report in (old, new):
        assert report['frames'] == 6500 and report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors']
        fixture, = report['synthetic_condition_fixtures']
        assert fixture['original_catalogue_model'] == 136 and fixture['frame'] == 4500 and len(fixture['changes']) == 1
    before, after = map(shots, (old, new))
    assert before.keys() == after.keys() and set(HOLDS) <= before.keys()
    labels, controls, highlights = [], [], []
    for frame in sorted(before):
        a, b = captured(before[frame]), captured(after[frame])
        evidence.update({d[frame]['path']: d[frame]['PNG_sha256'] for d in (before, after)})
        if frame not in HOLDS:
            if frame == 6499:
                bounds = ImageChops.difference(a, b).getbbox()
                assert bounds == (104, 238, 152, 258) and a.getpixel((104, 240)) != b.getpixel((104, 240))
                highlights.append(dict(frame=frame, difference_bounds=bounds, area='menu selection'))
                continue
            assert a.tobytes() == b.tobytes(), frame
            controls.append(frame)
            continue
        diff = ImageChops.difference(a, b)
        assert diff.getbbox()
        regions = ((0, 0, 126, 24), (29, 190, 237, 209))
        masks = [strip_owned_text(diff, font, name, screen, region)
                 for (name, screen) in (('Armed LgGalley', a), ('Armed Large Galley', b)) for region in regions]
        remaining = diff.getbbox()
        if frame == 5500:
            assert remaining == (32, 192, 256, 224)
            assert [im.getpixel((255, 209)) for im in (a, b)] == [(0, 165, 172), (24, 48, 57)]
            highlights.append(dict(frame=frame, difference_bounds=remaining, area='design row selection'))
        else:
            assert not remaining, frame
        h = [find_mask(font, 'Large Galley', im, (128, 0, 256, 24)) for im in (a, b)]
        assert h[0] == h[1]
        labels.append(dict(frame=frame, complete_label_masks=masks, unchanged_class=h[0],
                           all_differences_are_label_pixels=not remaining))
        if frame == HOLDS[0]:
            sheet = Image.new('RGB', (1024, 784), '#263238')
            title = ImageDraw.Draw(sheet)
            title.text((4, 3), 'Previous', fill='white')
            title.text((516, 3), 'Revised', fill='white')
            for i, im in enumerate((a, b)):
                sheet.paste(im.resize((512, 768), Image.Resampling.NEAREST), (512 * i, 16))
            sheet.save(SHEET)
    assert sum(row['all_differences_are_label_pixels'] for row in labels) == 2 and 6500 in controls
    return dict(held_labels=labels, exact_control_frames=controls, model_fixture=136,
                hardware=False, natural_acquisition=False, highlight_phase_differences=highlights), evidence


def main():
    assert not any(path.exists() for path in (OUTPUT, SHEET, NATIVE))
    prior, staged = map(base.load, (stage.parent.RELEASE, stage.OUTPUT))
    versions = (stage.parent.ROM, stage.ROM)
    assert [base.digest(p) for p in versions] == [prior['candidate_sha256'], staged['candidate_sha256']]
    assert prior['candidate_sha256'] == staged['previous_sha256']
    arms = [base.NdsImage.open(path).read_file(stage.ARM) for path in versions]
    assert stage.sha256(arms[1]).hexdigest() == staged['target_ARM9_sha256']
    font = GameAsciiFont.from_arm9(arms[1])
    assert font.glyphs == GameAsciiFont.from_arm9(arms[0]).glyphs
    catalogue, evidence = verify_catalogue(*arms, prior, staged)
    focus, captured_evidence = verify_shipyard(font, prior['candidate_sha256'], staged['candidate_sha256'])
    previews = FunctionType(previous.native_sheet.__code__, vars(previous) | {'SHEET': NATIVE})(
        arms[1], [row for row in staged['records'] if row['decision'] == 'revision'])
    assert len(previews) == len(stage.REVISIONS) and max(row['font_width'] for row in previews) == 108
    base.save(OUTPUT, dict(candidate_sha256=staged['candidate_sha256'], previous_sha256=prior['candidate_sha256'],
        catalogue=catalogue, focused_shipyard=focus, changed_label_previews=previews,
        sheet_sha256=base.digest(SHEET), native_sheet_sha256=base.digest(NATIVE),
        evidence=evidence | captured_evidence | {str(stage.OUTPUT): base.digest(stage.OUTPUT)}))
    print('Verified 60 catalogue labels and three complete Shipyard holds for Armed Large Galley.')


if __name__ == '__main__':
    main()
