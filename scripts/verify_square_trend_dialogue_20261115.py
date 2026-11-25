"""Verify the revised Tunis holds and original town transitions."""

from types import FunctionType, SimpleNamespace

from PIL import Image, ImageChops, ImageDraw

from scripts import checkpoint_regional_town_dialogue_20261115 as historical
from scripts import stage_square_trend_dialogue_20261115 as stage
from scripts.verify_captain_biographies_v1 import captured
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_london_stockholm_dialogue_20261115 import BODY, native_hold


base, ROOT = stage.base, stage.ROOT
OUTPUT, SHEET = ROOT / 'gameplay_verification.json', ROOT / 'tunis_comparison.png'
HOLDS = {frame: n for frame, n in historical.TOWNS['tunis'] if n in (654, 732)}


def main():
    assert not OUTPUT.exists() and not SHEET.exists()
    stored = base.load(stage.STORED)
    parent_receipt = base.load(stage.parent.RELEASE)
    prior = base.load(stage.TOWN_PROOF)
    assert base.digest(stage.TOWN_PROOF) == stored['regional_evidence_sha256']
    assert base.digest(stage.ROM) == stored['candidate_sha256']
    assert base.digest(stage.parent.ROM) == stored['previous_sha256'] == parent_receipt['candidate_sha256']
    old_rom, parent_rom, current = map(base.NdsImage.open, (historical.current.ROM, stage.parent.ROM, stage.ROM))
    old_sha = prior['candidate_sha256']
    assert base.digest(historical.current.ROM) == old_sha
    old_files, parent_files = map(stage.files, (old_rom, parent_rom))
    assert old_files.keys() == parent_files.keys()
    assert {p for p in old_files if old_files[p] != parent_files[p]} == {'/data/SC3.DK4'}
    inherited = historical.read_run('tunis', old_sha)
    stage_capture = SimpleNamespace(ROOT=ROOT, schedule=historical.capture.schedule)
    read_staged = FunctionType(historical.read_run.__code__, historical.read_run.__globals__ | {'capture': stage_capture})
    revised = read_staged('tunis', stored['candidate_sha256'])
    assert inherited[1] == revised[1]
    assert set(inherited[0]) == set(revised[0])
    raster, _, _ = stage.font_tools(current)
    font = historical.GameAsciiFont.from_arm9(current.read_file(stage.ARM))
    arm, kanji = (current.read_file(p) for p in (stage.ARM, '/GRP/KANJI.FNT'))
    cases = {row['id']: row for row in stored['native_cases']
             if (row['id'], row['argument']) in ((654, 'Whale Meat'), (732, ''))}
    planes = {}
    for n, row in cases.items():
        plane, _ = stage.render_portrait(raster, arm, kanji, bytes.fromhex(row['formatted_hex']))
        assert stage.digest(plane) == row['native_plane_sha256']
        planes[n] = plane
    evidence, holds, controls, previews = inherited[2] | revised[2], [], [], {}
    for frame in sorted(inherited[0]):
        old_shot, new_shot = inherited[0][frame], revised[0][frame]
        a, b = captured(old_shot), captured(new_shot)
        evidence.update({shot['path']: shot['PNG_sha256'] for shot in (old_shot, new_shot)})
        diff = ImageChops.difference(a, b).getbbox()
        if frame not in HOLDS:
            assert diff is None, (frame, diff)
            controls.append(frame)
            continue
        assert diff and BODY[0] <= diff[0] < diff[2] <= BODY[2] and BODY[1] <= diff[1] < diff[3] <= BODY[3]
        n = HOLDS[frame]
        ink = native_hold(b, planes[n])
        name, bounds = complete_mask(font, 'Shopkeeper', b, 16, 277, (98, 97, 98))
        holds.append(dict(frame=frame, message_ID=n, lines=cases[n]['lines'], body_ink_pixels=ink,
            nameplate_pixels=name, nameplate_bounds=bounds, changed_pixel_bounds=diff, capture=new_shot))
        previews.setdefault(n, (a, b))
    assert [row['frame'] for row in holds] == sorted(HOLDS)
    assert len(previews) == 2 and controls
    sheet = Image.new('RGB', (1024, 474), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, (n, screens) in enumerate(previews.items()):
        for column, (label, screen) in enumerate(zip(('Before', 'Revised'), screens, strict=True)):
            x, y = 512 * column, 237 * i
            draw.text((x + 4, y + 3), f'{n} {label}', fill='white')
            sheet.paste(screen.crop((0, 268, 256, 376)).resize((512, 216), Image.Resampling.NEAREST), (x, y + 18))
    sheet.save(SHEET)
    base.save(OUTPUT, dict(candidate_sha256=stored['candidate_sha256'], comparison_ROM_sha256=old_sha,
        comparison_dependencies_match_parent=True, ordinary_saved_game=True, hardware=False, revised_holds=holds,
        exact_control_frames=controls, original_requests=revised[1], native_only_revisions=[653, 655, 733],
        sheet_sha256=base.digest(SHEET), evidence=evidence))
    print(f'Verified {len(holds)} revised Tunis holds and {len(controls)} unchanged controls.')


if __name__ == '__main__':
    main()
