"""Replay current Amsterdam Square from New Game and verify its shared text."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from scripts import check_town_summary_20261119 as heading
from scripts import checkpoint_amsterdam_square_current_20261114 as earlier
from scripts import register_square_shop_followup_20261119 as square
from scripts import register_town_summary_20261119 as current
from scripts.source_locked_derivation_v5118 import checked_text

base, stage = current.base, current.stage
history = earlier.capture
ROOT = Path('work/amsterdam_town_summary_20261119')
TRACK = Path('translations/editorial_checkpoints/SharedText_20261110_v1')
OUTPUT = TRACK / 'amsterdam_town_summary_20261119_v1.json'


def capture():
    code = checked_text(getsource(history.main), {
        '    env["main"](parser.parse_args().case)': '    env["main"]("square")',
    })
    scope = vars(history) | dict(ROOT=ROOT, current=current, __file__=__file__)
    exec(compile(code, __file__+'::capture', 'exec'), scope)
    scope['main']()


def verify():
    assert not OUTPUT.exists()
    folder = ROOT/'square'
    dependencies = [folder/path for path in ('capture/capture_report.json', 'requests.json', 'terminal.json')]
    report, trace, terminal = map(base.load, dependencies)
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release['candidate_sha256'] == report['ROM_sha256'] == terminal['ROM_sha256']
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    events, frames, end, source, donor = history.schedule('square')
    assert donor is None and report.get('battery_save_preloaded') is None
    assert report['scripted_input_schedule'] == events and report['frames'] == terminal['completed_frames'] == end
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    assert not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
    requests = trace['source_requests']
    panels = ((9701,136), (10901,658), (11701,689), (12501,658), (13301,657), (14501,657), (15301,689))
    assert [r['message_ID'] for r in requests[::2]] == [120, 341, 341, 341, *(n for _, n in panels)]
    for direct, copy in zip(requests[::2], requests[1::2], strict=True):
        assert [direct['PC'], copy['PC']] == [0x0205528C, 0x020534F4]
        assert {key: value for key, value in direct.items() if key != 'PC'} == {
            key: value for key, value in copy.items() if key != 'PC'}
    pending = {r['message_ID'] for r in base.load(stage.PENDING)['records']}
    assert not pending.intersection(row['message_ID'] for row in requests)
    image, clean = map(base.NdsImage.open, (current.ROM, stage.CLEAN))
    arm = image.read_file(stage.ARM)
    directory = current.native.digest(arm[earlier.DIRECTORY_OFFSET:earlier.TABLE_OFFSET])
    installed = earlier.owned_entries(image.read_file(stage.COMMON), arm, directory)
    original = earlier.common_message_entries(clean.read_file(stage.COMMON), clean.read_file(stage.ARM))
    font = heading.GameAsciiFont.from_arm9(arm)
    review = {r['message_ID']: r for r in base.load(square.REVIEW)['records']}
    instructions = next(row for row in base.load(earlier.OUTPUT)['retained'] if row['id'] == 'COMMON_MESSAGE_136')
    captured = heading.shots(report)
    evidence = {str(p): base.digest(p) for p in (*dependencies, source, square.REVIEW, earlier.OUTPUT, current.RELEASE, Path(__file__))}
    observed = []
    for (frame, key), request in zip(panels, requests[8::2], strict=True):
        assert frame in frames and 0 < frame - request['frame'] < 160 and request['message_ID'] == key
        shot = captured[frame]
        photo = heading.captured(shot)
        top = [heading.mask(photo, font, text, box) for text, box in (
            ('Type', (24,48,48,60)), ('Status', heading.STATUS_REGION),
            ('Growth', (140,48,176,60)), ('Arms', (204,48,240,60)))]
        if key == 136:
            source_ref, source_hex = instructions['clean_reference'], instructions['clean_hex']
            current_hex = instructions['current_hex']
            lines = earlier.DECISIONS[136][0]
        else:
            prior = review[key]
            source_ref, source_hex = prior['source_reference'], prior['source_hex']
            current_hex = prior['staged_hex']
            lines = prior['visible_lines']
        assert original[key].text.hex() == source_hex and installed[key].text.hex() == current_hex
        assert earlier.reference(original[key]) == source_ref
        current_ref = earlier.reference(installed[key])
        body = earlier.body_mask(photo, font, lines)
        label = None
        if key != 136:
            ink, bounds = earlier.complete_mask(font, 'Shopkeeper', photo, 16, 277, (98,97,98))
            assert ink == 135
            label = dict(text='Shopkeeper', complete_ink_pixels=ink, bounds=bounds)
        evidence[shot['path']] = shot['PNG_sha256']
        observed.append(dict(frame=frame, COMMON_key=key, heading_masks=top, complete_body=body,
            speaker=label, source_reference=source_ref, current_reference=current_ref,
            capture=shot['path']))
    assert any(row['COMMON_key'] == 657 for row in observed)
    assert not any(row['COMMON_key'] in pending for row in observed)
    base.save(OUTPUT, dict(candidate_sha256=release['candidate_sha256'], ordinary_Amsterdam_from_New_Game=True,
        hardware=False, observed_panels=observed, current_total_requests=len(requests),
        pending_COMMON_requests=0, new_editorial_credit=0, evidence=evidence))
    print(f'Verified complete Town Summary headings and dialogue in {len(observed)} Amsterdam Square holds.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('capture', 'verify'))
    globals()[parser.parse_args().action]()
