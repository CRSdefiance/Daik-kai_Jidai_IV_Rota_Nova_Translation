"""Verify the ordinary Market opening and Price Info transition on both ROMs."""

from PIL import Image, ImageDraw

from scripts import replay_market_economy_dialogue_20261115 as replay
from scripts import stage_market_economy_dialogue_20261115 as stage
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_london_stockholm_dialogue_20261115 import native_hold


base, ROOT = stage.base, stage.ROOT
OUTPUT, SHEET = ROOT / 'gameplay_verification.json', ROOT / 'market_opening.png'
HOLD = 9150


def read_replay(case, sha):
    folder = ROOT / case
    report_path, trace_path = (folder / name for name in ('capture/capture_report.json', 'requests.json'))
    report, trace = map(base.load, (report_path, trace_path))
    events, frame_numbers, end, _, source = replay.schedule(case)
    assert report['ROM_sha256'] == sha and report['scripted_input_schedule'] == events and report['frames'] == end
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and donor['source_sha256'] == source['source_sha256']
    assert base.digest(donor['source']) == source['source_sha256']
    assert trace['all_host_slots_restored_and_core_file_exact'] and not trace['errors'] and not trace['mismatches']
    requests = trace['source_requests']
    assert [r['message_ID'] for r in requests] == [8, 8, 18, 18]
    assert [r['PC'] for r in requests] == [0x0205528C, 0x020534F4] * 2
    by_frame = shots(report)
    frames = {n: by_frame[n] for n in frame_numbers}
    evidence = {str(path): base.digest(path) for path in (report_path, trace_path, folder / 'source_contract.json')}
    evidence.update({row['path']: row['PNG_sha256'] for row in frames.values()})
    return report, requests, frames, evidence


def main():
    assert not OUTPUT.exists() and not SHEET.exists()
    info = base.load(stage.STORED)
    assert base.digest(stage.ROM) == info['candidate_sha256']
    before = read_replay('market_parent', info['previous_sha256'])
    after = read_replay('market_staged', info['candidate_sha256'])
    assert before[1] == after[1] and before[2].keys() == after[2].keys()
    assert all(before[0][key] == after[0][key] for key in ('core_DLL_sha256', 'core_options'))
    frames = {n: captured(row) for n, row in after[2].items()}
    assert all(captured(before[2][n]).tobytes() == screen.tobytes() for n, screen in frames.items())
    image = base.NdsImage.open(stage.ROM)
    arm, kanji = (image.read_file(name) for name in (stage.ARM, '/GRP/KANJI.FNT'))
    raster, _, _ = stage.font_tools(image)
    case = next(row for row in info['native_cases'] if row['message_ID'] == 8)
    plane, _ = stage.render_portrait(raster, arm, kanji, bytes.fromhex(case['formatted_hex']))
    ink = native_hold(frames[HOLD], plane)
    sheet = Image.new('RGB', (1040, 418), '#263238')
    draw = ImageDraw.Draw(sheet)
    for column, (label, n) in enumerate((('Market greeting', HOLD), ('Price Info town picker', 11000))):
        x = column * 520 + 4
        draw.text((x, 4), label, fill='white')
        sheet.paste(frames[n].crop((0, 192, 256, 384)).resize((512, 384), Image.Resampling.NEAREST), (x, 20))
    sheet.save(SHEET)
    base.save(OUTPUT, dict(candidate_sha256=info['candidate_sha256'], previous_sha256=info['previous_sha256'],
        ordinary_saved_game=True, original_requests=after[1], complete_default_greeting_ink_pixels=ink,
        exact_control_frames=list(frames), offline_only_revisions=[772, 773], hardware=False,
        sheet_sha256=base.digest(SHEET), evidence=before[3] | after[3]))
    print(f'Verified {len(frames)} unchanged Market controls and the full ordinary greeting.')


if __name__ == '__main__':
    main()
