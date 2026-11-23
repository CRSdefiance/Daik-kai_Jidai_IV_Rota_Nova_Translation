"""Check the original recommendation, instructions, and farewell in paired replays."""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

from scripts import stage_market_reward_dialogue_20261115 as stage
from scripts.verify_captain_biographies_v1 import captured, shots


base, ROOT = stage.base, stage.ROOT
OUTPUT, SHEET = ROOT / 'gameplay_verification.json', ROOT / 'recommendation_replay.png'
CHAIN = [775, 780, 766]


def read_run(case, sha):
    folder = ROOT / case
    plan_path, terminal_path = (folder / f'{name}.json' for name in ('run_plan', 'terminal'))
    plan, terminal = map(base.load, (plan_path, terminal_path))
    report_path, observed_path = map(Path, (terminal['report'], terminal['observer']))
    report, observed = map(base.load, (report_path, observed_path))
    assert terminal['terminal'] and terminal['ROM_sha256'] == plan['ROM_sha256'] == report['ROM_sha256'] == sha
    assert base.digest(report_path) == terminal['report_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == plan['frames'] == 12001
    assert not observed['errors'] and not observed['mismatches'] and observed['all_host_slots_restored_and_core_file_exact']
    assert base.digest(plan['donor']) == plan['donor_sha256'] == report['battery_save_preloaded']['source_sha256']
    assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    supplied, = observed['synthetic_recommendation_reward_input_fixtures']
    assert [supplied[k] for k in ('supplied_qualification_result', 'supplied_reward_quantity_input',
            'supplied_bonus_flag', 'original_sale_hold_total')] == [2, 16, 1, 2]
    assert supplied['all_other_CPU_WRAM_DTCM_ITCM_bytes_exact'] and supplied == report['synthetic_recommendation_reward_input_fixtures'][0]
    stocks, = report['synthetic_market_display_fixtures']
    assert stocks['frame'] == 3200 and len(stocks['changes']) == 8 and stocks['cargo_product_names'] == ['Tea', 'Rum']
    rows = [row for row in observed['rows'] if row['source_request']['ID'] in CHAIN]
    assert [row['source_request']['ID'] for row in rows] == CHAIN
    paths = (plan_path, terminal_path, report_path, observed_path, folder / 'source_contract.json')
    evidence = {str(path): base.digest(path) for path in paths}
    return report, rows, shots(report), evidence


def main():
    assert not OUTPUT.exists() and not SHEET.exists()
    info, manuscript = map(base.load, (stage.STORED, stage.MANUSCRIPT))
    assert base.digest(stage.ROM) == info['candidate_sha256']
    before = read_run('current', info['previous_sha256'])
    after = read_run('reviewed', info['candidate_sha256'])
    assert before[2].keys() == after[2].keys()
    assert all(before[0][k] == after[0][k] for k in ('scripted_input_schedule', 'core_DLL_sha256', 'core_options'))
    a, b = ({n: captured(row) for n, row in run[2].items()} for run in (before, after))
    evidence = before[3] | after[3]
    evidence.update({row['path']: row['PNG_sha256'] for run in (before, after) for row in run[2].values()})
    assert a[12001].tobytes() == b[12001].tobytes()
    image = base.NdsImage.open(stage.ROM)
    arm, kanji = (image.read_file(name) for name in (stage.ARM, '/GRP/KANJI.FNT'))
    raster, _, _ = stage.font_tools(image)
    records = {row['message_ID']: row for row in manuscript['records']}
    holds = []
    for i, (n, row) in enumerate(zip(CHAIN, after[1], strict=True)):
        r = records[n]
        assert row['bounds'] == [0, 0, 228, 48] and row['text_hex'] == r['native_formatted_hex']
        plane, _ = stage.render_portrait(raster, arm, kanji, bytes.fromhex(row['text_hex']))
        expected = {(16 + j % 228, 296 + j // 228) for j, ink in enumerate(plane) if ink == 1}
        assert expected
        start = row['frame']
        end = after[1][i + 1]['frame'] if i + 1 < len(CHAIN) else max(b)
        matches = []
        for nframe, screen in sorted(b.items()):
            if not start < nframe < end:
                continue
            pixels = {(x, y) for y in range(294, 360) for x in range(16, 244)
                      if screen.getpixel((x, y)) == (0, 8, 0)}
            if pixels == expected:
                matches.append(nframe)
        assert matches, (n, start, end)
        frame = matches[0]
        diff = ImageChops.difference(a[frame], b[frame]).getbbox()
        if n in stage.REVISIONS:
            assert diff and 16 <= diff[0] < diff[2] <= 244 and 294 <= diff[1] < diff[3] <= 360
        else:
            assert diff is None
        holds.append(dict(message_ID=n, frame=frame, complete_ink_pixels=len(expected),
                          matching_frames=matches, changed_bounds=diff, native_plane_sha256=stage.digest(plane)))
    sheet = Image.new('RGB', (1040, 230 * len(holds)), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, hold in enumerate(holds):
        frame, n = hold['frame'], hold['message_ID']
        for column, (label, screens) in enumerate((('Previous', a), ('Revised', b))):
            x, y = column * 520 + 4, i * 230
            draw.text((x, y + 4), f'{n} {label}', fill='white')
            sheet.paste(screens[frame].crop((0, 280, 256, 384)).resize((512, 208), Image.Resampling.NEAREST), (x, y + 18))
    sheet.save(SHEET)
    base.save(OUTPUT, dict(candidate_sha256=info['candidate_sha256'], previous_sha256=info['previous_sha256'],
        original_reward_sequence=CHAIN, held_pages=holds, exact_final_frame=12001, hardware=False,
        supplied_cargo_share_demand_qualification_and_bonus=True, naturally_earned_reward=False,
        offline_only_revisions=sorted((stage.PHRASES.keys() - set(CHAIN))), evidence=evidence, sheet_sha256=base.digest(SHEET)))
    print('Verified the revised recommendation, its instructions, and the original farewell and return.')


if __name__ == '__main__':
    main()
