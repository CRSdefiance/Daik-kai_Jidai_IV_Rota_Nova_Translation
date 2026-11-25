"""Revisit the original encounter using the Nagasaki save and controller inputs."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageChops, ImageDraw

from scripts import observe_lisbon_voyage_and_osaka_20261115 as observed
from scripts import replay_embedded_story_roles_20261115 as boot
from scripts import stage_kurushima_encounter_20261115 as stage
from scripts import verify_voyage_rat_and_search_dialogue_20261115 as prior
from scripts.audit_lil_B221_English_paths_v7004 import body_masks
from scripts.replay_lil_ceramics_wrap_20261111 import masks
from scripts.stage_market_conversation_20261115 import COMMON, DIRECTORY_OFFSET, TABLE_OFFSET, owned_entries
from scripts.verify_captain_biographies_v1 import captured


base, ROOT = stage.base, stage.ROOT
OUTPUT, SHEET = ROOT / 'gameplay_verification.json', ROOT / 'encounter_comparison.png'


def gameplay():
    parent = SimpleNamespace(ROM=stage.ROM, RELEASE=stage.STORED)
    env = vars(observed.playback) | dict(ROOT=ROOT, parent=parent, observer=observed.scoped_observer,
        get_schedule=observed.schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(getsource(observed.playback.main), __file__ + '::original-nagasaki-replay', 'exec'), env)
    env['main']('osaka')


def startup():
    FunctionType(boot.startup.__code__, vars(boot) | dict(stage=stage))()


def verify():
    assert not OUTPUT.exists() and not SHEET.exists()
    staged, manuscript = map(base.load, (stage.STORED, stage.MANUSCRIPT))
    observation = base.load(stage.OBSERVATION)
    assert base.digest(stage.OBSERVATION) == staged['observation_sha256']
    assert all(base.digest(path) == value for path, value in observation['evidence'].items())
    assert base.digest(stage.ROM) == staged['candidate_sha256']
    assert base.digest(observed.current.ROM) == observation['candidate_sha256']
    comparison, parent, current = map(base.NdsImage.open, (observed.current.ROM, stage.parent.ROM, stage.ROM))
    a, b, c = map(stage.files, (comparison, parent, current))
    assert a.keys() == b.keys() == c.keys()
    assert {p for p in a if a[p] != b[p]} == {COMMON}
    assert {p for p in b if b[p] != c[p]} == {stage.FILE}
    arm = c[stage.ARM]
    rows_before, rows_after = [owned_entries(raw, arm, stage.digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
                               for raw in (a[COMMON], c[COMMON])]
    assert all(rows_before[n].text == rows_after[n].text for n in (85, 86, 618))
    font = prior.regional.GameAsciiFont.from_arm9(arm)
    old, old_calls, evidence = prior.check_run(observed.ROOT, 'osaka', observation['candidate_sha256'])
    new, new_calls, dependencies = prior.check_run(ROOT, 'osaka', staged['candidate_sha256'])
    assert old_calls == new_calls and old.keys() == new.keys()
    evidence.update(dependencies | {str(stage.OBSERVATION): base.digest(stage.OBSERVATION)})
    holds, controls, gallery = [], [], []
    for row, event in zip(manuscript['records'], observation['nagasaki_encounter'], strict=True):
        assert row['id'] == event['id']
        frame = event['frame']
        before, after = (captured(shot[frame]) for shot in (old, new))
        evidence.update({shot[frame]['path']: shot[frame]['PNG_sha256'] for shot in (old, new)})
        bounds = ImageChops.difference(before, after).getbbox()
        name = prior.nameplate(font, after, row['speaker'])
        assert name == prior.nameplate(font, before, row['speaker'])
        review = row['native_pages']
        revision = row['decision'] == 'revision'
        if revision:
            assert bounds and 16 <= bounds[0] < bounds[2] <= 232 and 296 <= bounds[1] < bounds[3] <= 360
            bindings = ((before, review['before'][0]), (after, review['after'][0]))
        else:
            assert bounds is None
            bindings = ((after, review['retained'][0]),)
        for screen, page in bindings:
            assert page['example'] in ('Maria', 'literal')
            native = bytes.fromhex(page['native_plane_hex'])
            assert stage.digest(native) == page['native_plane_sha256'] and body_masks(screen) == masks(native), (
                row['id'], frame, page['lines'])
        if revision:
            holds.append(dict(id=row['id'], frame=frame, nameplate=name, changed_bounds=bounds,
                              before=review['before'][0]['lines'], after=review['after'][0]['lines']))
            gallery.append((row['id'], before, after))
        else:
            controls.append(dict(id=row['id'], frame=frame, nameplate=name, whole_frame_exact=True))
    for frame in (5000, 5200, 6960, 7140):
        assert captured(old[frame]).tobytes() == captured(new[frame]).tobytes(), frame
        controls.append(dict(frame=frame, whole_frame_exact=True))
        evidence.update({shot[frame]['path']: shot[frame]['PNG_sha256'] for shot in (old, new)})
    assert len(holds) == len(gallery) == 4 and len(controls) == 8
    sheet = Image.new('RGB', (1024, 230 * len(gallery)), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, (label, before, after) in enumerate(gallery):
        for column, screen in enumerate((before, after)):
            x, y = column * 512, i * 230
            draw.text((x + 4, y + 2), f"{label} {'Before' if column == 0 else 'Revised'}", fill='white')
            sheet.paste(screen.crop((0, 271, 256, 376)).resize((512, 210), Image.Resampling.NEAREST), (x, y + 18))
    sheet.save(SHEET)
    base.save(OUTPUT, dict(candidate_sha256=staged['candidate_sha256'], previous_sha256=staged['previous_sha256'],
        comparison_ROM_sha256=observation['candidate_sha256'], ordinary_saved_game=True, injected_location=False,
        original_requests=old_calls, checked_common_alternatives=[85, 86, 618], hardware=False, held_panels=holds,
        exact_control_frames=controls, sheet_sha256=base.digest(SHEET), evidence=evidence))
    print('Verified all eight encounter panels and the four preceding or following control frames.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('gameplay', 'startup', 'verify'))
    {'gameplay': gameplay, 'startup': startup, 'verify': verify}[parser.parse_args().mode]()
