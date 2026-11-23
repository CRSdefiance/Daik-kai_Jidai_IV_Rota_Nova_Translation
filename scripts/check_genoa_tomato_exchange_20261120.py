"""Verify the normal Genoa trigger, the nine speeches, and the forecast and return."""

from PIL import Image, ImageChops, ImageDraw

from scripts import observe_additional_town_visits_20261120 as baseline
from scripts import replay_genoa_tomato_exchange_20261120 as replay
from scripts import stage_genoa_tomato_exchange_20261120 as stage
from scripts.replay_lil_ceramics_wrap_20261111 import body_masks, masks, photos


base = stage.base
PROOF, SHEET = stage.ROOT / 'playback_verified.json', stage.ROOT / 'genoa_actual.png'


def main():
    assert not PROOF.exists() and not SHEET.exists()
    staged = base.load(stage.STORED)
    paths = [(root / 'genoa/capture/capture_report.json') for root in (baseline.ROOT, replay.ROOT)]
    reports = [base.load(p) for p in paths]
    roms = (stage.parent.ROM, stage.ROM)
    evidence = {str(p): base.digest(p) for p in (*paths, stage.STORED, stage.MANUSCRIPT)}
    for path, report, sched in zip(roms, reports, (baseline.schedule, replay.schedule), strict=True):
        inputs, _, end, source, donor = sched('genoa')
        assert report['ROM_sha256'] == base.digest(path) and report['frames'] == end
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
        assert report['scripted_input_schedule'] == inputs
        assert report['battery_save_preloaded']['source_sha256'] == donor['source_sha256'] == base.digest(donor['source'])
        evidence[str(source)] = base.digest(source)
    assert reports[0]['core_DLL_sha256'] == reports[1]['core_DLL_sha256']
    assert reports[0]['core_options'] == reports[1]['core_options']
    assert reports[1]['ROM_sha256'] == staged['candidate_sha256']
    assert reports[0]['ROM_sha256'] == staged['previous_sha256']

    before, after = map(photos, reports)
    rows = [r for r in base.load(stage.MANUSCRIPT)['records'] if r['route'] == 1]
    frames = range(4350, 7951, 400)
    output = []
    contact = Image.new('RGB', (1280, 432), '#252832')
    draw = ImageDraw.Draw(contact)
    for i, (row, frame) in enumerate(zip(rows, frames, strict=True)):
        old_ref, old = before[frame]
        new_ref, new = after[frame]
        diff = ImageChops.difference(old, new).crop((0, 0, 256, 360)).getbbox()
        if row['decision'] == 'revision':
            assert diff and 16 <= diff[0] < diff[2] <= 232 and 296 <= diff[1] < diff[3] <= 360, (row['id'], diff)
            page, = row['after_native']['pages']
            assert body_masks(new) == masks(bytes.fromhex(page['native_plane_hex'])), (row['id'], frame)
        else:
            assert diff is None, (row['id'], frame, diff)
        x, y = i % 5 * 256, i // 5 * 216
        draw.text((x + 4, y + 4), f'{frame}  {row["speaker"]}', fill='white')
        contact.paste(new.crop((0, 192, 256, 384)), (x, y + 22))
        output.append(dict(id=row['id'], frame=frame, before=old_ref, after=new_ref, changed_rectangle=diff))
    returns = (3720, 3950, 8350)
    assert all(ImageChops.difference(before[frame][1], after[frame][1]).getbbox() is None for frame in returns)
    assert sum(r['changed_rectangle'] is not None for r in output) == 4
    contact.save(SHEET)
    base.save(PROOF, dict(candidate_sha256=staged['candidate_sha256'], parent_sha256=staged['previous_sha256'],
        panels=output, matching_town_and_square_transition_frames=list(returns), observed_revisions=4,
        original_square_entrance_ordinary_inputs=True, used_existing_battery_save=True, hardware=False,
        sheet={str(SHEET): base.digest(SHEET)}, evidence=evidence))
    print('The complete ordinary Genoa exchange and forecast match the four native revisions and six retentions.')


if __name__ == '__main__':
    main()
