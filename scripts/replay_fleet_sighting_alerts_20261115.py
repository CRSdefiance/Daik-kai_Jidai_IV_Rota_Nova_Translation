"""Verify the ordinary Nagasaki sighting and the surrounding encounter."""

from argparse import ArgumentParser
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw

from scripts import replay_kurushima_encounter_20261115 as previous
from scripts import stage_fleet_sighting_alerts_20261115 as stage
from scripts.verify_captain_biographies_v1 import captured
from scripts.verify_london_stockholm_dialogue_20261115 import BODY, native_hold
from scripts.verify_voyage_rat_and_search_dialogue_20261115 import check_run, nameplate


base, ROOT = stage.base, stage.ROOT
OUTPUT, SHEET = ROOT / 'gameplay_verification.json', ROOT / 'fleet_sighting_comparison.png'


def gameplay():
    FunctionType(previous.gameplay.__code__, vars(previous) | dict(stage=stage, ROOT=ROOT))()


def startup():
    FunctionType(previous.startup.__code__, vars(previous) | dict(stage=stage))()


def verify():
    assert not OUTPUT.exists() and not SHEET.exists()
    staged = base.load(stage.STORED)
    prior = base.load(stage.parent.RELEASE)
    assert base.digest(stage.ROM) == staged['candidate_sha256']
    assert base.digest(stage.parent.ROM) == prior['candidate_sha256'] == staged['previous_sha256']
    old, old_calls, evidence = check_run(previous.ROOT, 'osaka', staged['previous_sha256'])
    new, new_calls, dependencies = check_run(ROOT, 'osaka', staged['candidate_sha256'])
    assert old.keys() == new.keys() and old_calls == new_calls
    assert [row['message_ID'] for row in new_calls[::2]] == [85, 86, 618]
    selected = [row for row in new_calls if row['message_ID'] == 618]
    assert len(selected) == 2 and all(row['caller_LR'] == 0x02053DA4 for row in selected)
    evidence.update(dependencies)
    frame = 5200
    case = next(row for row in staged['native_cases'] if row['message_ID'] == 618
                and row['bearing'] == 'E' and row['company'] == 'Kurushima')
    before, after = (captured(shots[frame]) for shots in (old, new))
    diff = ImageChops.difference(before, after).getbbox()
    assert diff and BODY[0] <= diff[0] < diff[2] <= BODY[2] and BODY[1] <= diff[1] < diff[3] <= BODY[3], diff
    image = base.NdsImage.open(stage.ROM)
    arm, kanji = (image.read_file(path) for path in (stage.ARM, '/GRP/KANJI.FNT'))
    raster, _, _ = stage.font_tools(image)
    font = previous.prior.regional.GameAsciiFont.from_arm9(arm)
    plane, _ = stage.render_portrait(raster, arm, kanji, bytes.fromhex(case['formatted_hex']))
    assert stage.digest(plane) == case['plane_sha256']
    ink = native_hold(after, plane)
    label = nameplate(font, after, 'Sailor')
    assert label == nameplate(font, before, 'Sailor')
    for shots in (old, new):
        evidence[shots[frame]['path']] = shots[frame]['PNG_sha256']
    controls = []
    for frame in (4000, 5000, *previous.prior.NAGASAKI, 6960, 7140):
        assert captured(old[frame]).tobytes() == captured(new[frame]).tobytes(), frame
        controls.append(frame)
        evidence.update({shots[frame]['path']: shots[frame]['PNG_sha256'] for shots in (old, new)})
    assert len(controls) == 12
    sheet = Image.new('RGB', (1024, 234), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, (caption, image) in enumerate((('Previous', before), ('Revised', after))):
        x = i * 512
        draw.text((x + 4, 3), f'618 {caption}', fill='white')
        sheet.paste(image.crop((0, 268, 256, 376)).resize((512, 216), Image.Resampling.NEAREST), (x, 17))
    sheet.save(SHEET)
    base.save(OUTPUT, dict(candidate_sha256=staged['candidate_sha256'], previous_sha256=staged['previous_sha256'],
        ordinary_saved_game=True, injected_location=False, hardware=False, original_requests=new_calls,
        revised_holds=[dict(message_ID=618, frame=5200, display=case['lines'], body_ink_pixels=ink,
                            nameplate=label, changed_bounds=diff)],
        exact_control_frames=controls, unvisited_sighting_messages=sorted(set(stage.IDS) - {618}),
        close_range_and_incoming_checked_offline=True, sheet_sha256=base.digest(SHEET), evidence=evidence))
    print(f'Verified the revised bearing, complete Sailor label and {len(controls)} unchanged frames.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('gameplay', 'startup', 'verify'))
    {'gameplay': gameplay, 'startup': startup, 'verify': verify}[parser.parse_args().mode]()

