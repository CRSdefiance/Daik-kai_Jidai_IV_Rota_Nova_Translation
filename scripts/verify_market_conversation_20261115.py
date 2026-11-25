"""Match the revised price-check prompt and the original town-picker transition."""

from PIL import Image, ImageChops, ImageDraw

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts import replay_market_conversation_20261115 as replay
from scripts import stage_market_conversation_20261115 as stage
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.stage_mutiny_review_v1 import render_portrait
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_london_stockholm_dialogue_20261115 import BODY, native_hold


base, ROOT = stage.base, stage.ROOT
OUTPUT, SHEET = ROOT / 'gameplay_verification.json', ROOT / 'gameplay_comparison.png'
PARENT_CAPTURE = ROOT.with_name('market_conversation_20261115_v1') / 'price_parent'
HOLD = 10690


def read_replay(folder, sha, case):
    report_path, trace_path = (folder / s for s in ('capture/capture_report.json', 'requests.json'))
    report, trace = map(base.load, (report_path, trace_path))
    events, frames, end, _, source = replay.schedule(case)
    assert report['ROM_sha256'] == sha and report['scripted_input_schedule'] == events and report['frames'] == end
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and donor['source_sha256'] == source['source_sha256']
    assert base.digest(donor['source']) == source['source_sha256']
    assert trace['all_host_slots_restored_and_core_file_exact'] and not trace['errors'] and not trace['mismatches']
    assert [r['message_ID'] for r in trace['source_requests']] == [8, 8, 18, 18]
    assert [r['PC'] for r in trace['source_requests']] == [0x0205528C, 0x020534F4] * 2
    assert [r['frame'] for r in trace['source_requests']] == [8820, 8820, 10209, 10209]
    assert all(r['caller_LR'] == 0x02053FF8 for r in trace['source_requests'])
    evidence = {str(p): base.digest(p) for p in (report_path, trace_path, folder / 'source_contract.json')}
    by_frame = shots(report)
    rows = {n: by_frame[n] for n in frames}
    evidence.update({row['path']: row['PNG_sha256'] for row in rows.values()})
    return report, trace, rows, evidence


def main():
    assert not OUTPUT.exists() and not SHEET.exists()
    info = base.load(stage.STORED)
    assert base.digest(stage.ROM) == info['candidate_sha256']
    previous = read_replay(PARENT_CAPTURE, info['previous_sha256'], 'price_parent')
    current = read_replay(ROOT / 'price_staged', info['candidate_sha256'], 'price_staged')
    assert previous[1]['source_requests'] == current[1]['source_requests']
    assert all(previous[0][key] == current[0][key] for key in ('core_DLL_sha256', 'core_options'))
    frames = {n: (captured(previous[2][n]), captured(current[2][n])) for n in replay.FRAMES}
    for n, (old, new) in frames.items():
        diff = ImageChops.difference(old, new).getbbox()
        if n == HOLD:
            assert diff and BODY[0] <= diff[0] < diff[2] <= BODY[2] and BODY[1] <= diff[1] < diff[3] <= BODY[3]
        else:
            assert diff is None, (n, diff)
    image = base.NdsImage.open(stage.ROM)
    arm, kanji = [image.read_file(name) for name in (stage.ARM, '/GRP/KANJI.FNT')]
    raster, _, _ = font_tools(image)
    row = next(r for r in info['native_cases'] if r['n'] == 18)
    plane, _ = render_portrait(raster, arm, kanji, bytes.fromhex(row['native_output_hex']))
    assert stage.digest(plane) == row['native_plane_sha256']
    ink = native_hold(frames[HOLD][1], plane)
    archive = image.read_file(stage.COMMON)
    expected = owned_entries(archive, arm, stage.digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))[18]
    assert expected.text == stage.encoded_changes()[18]
    sheet = Image.new('RGB', (1024, 228), '#263238')
    draw = ImageDraw.Draw(sheet)
    for column, (label, screen) in enumerate(zip(('Before', 'Revised'), frames[HOLD], strict=True)):
        x = column * 512
        draw.text((x + 5, 3), label, fill='white')
        sheet.paste(screen.crop((0, 280, 256, 384)).resize((512, 208), Image.Resampling.NEAREST), (x, 18))
    sheet.save(SHEET)
    base.save(OUTPUT, dict(candidate_sha256=info['candidate_sha256'], message_ID=18, held_frame=HOLD,
        complete_ink_pixels=ink, original_requests=current[1]['source_requests'], original_town_picker=True,
        exact_control_frames=[n for n in frames if n != HOLD], native_only_revisions=[10, 19, 20, 24],
        hardware=False, sheet_sha256=base.digest(SHEET), evidence=previous[3] | current[3]))
    print('Verified the complete revised price-check dialogue and six unchanged Market and town-picker controls.')


if __name__ == '__main__':
    main()
