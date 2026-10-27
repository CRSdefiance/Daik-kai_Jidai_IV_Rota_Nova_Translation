"""Current ordinary Tavern direct/YesNo displays: full foreground, native returns and state."""
from pathlib import Path
import re, struct
from PIL import Image, ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from scripts.verify_village_wrap_v608 import read, save
from scripts.primary_town_native_font_v2102 import font_tools, glyph_codes
from scripts.verify_shipyard_gameplay_v760 import independent_font, models
from scripts.verify_market_gameplay_v753 import state

ROOT = Path('work/analysis/tavern_actual_verification_v2193')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v2171_candidate.nds')
SPECS = [
    ('direct', 2190, 9201, {821: (5000, 5200), 827: (7000, 7200), 823: (8200, 8400)}, (3200, 5000, 7000, 8200, 9201)),
    ('price', 2191, 6001, {852: (5000, 5200)}, (3200, 5000, 6001)),
]

if __name__ == '__main__':
    assert not ROOT.exists()
    ROOT.mkdir(parents=True)
    rom = NdsImage.open(ROM)
    arm, common = rom.read_file('/__arm9__.bin'), rom.read_file('/COMMON/MESFILE.DK4')
    kanji = rom.read_file('/GRP/KANJI.FNT')
    entries = current_entries(common, arm)
    raster, _, _ = font_tools(rom)
    digest = sha(ROM.read_bytes())
    all_holds, runs, controls = [], [], []
    for mode, version, limit, expected, state_frames in SPECS:
        run = Path(f'work/analysis/tavern_{mode}_actual_v{version}')
        cap = CAP / f'tavern_{mode}_actual_v{version}_V2171'
        plan, terminal, report, obs = [read(p) for p in (run/'run_plan.json', run/'terminal.json', cap/'capture_report.json', cap/'common_observer/requests.json')]
        assert terminal['terminal'] and terminal['all_observer_host_slots_restored']
        assert report['frames'] == limit and report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors'] and not report['hardware_device_verification']
        assert not obs['errors'] and not obs['mismatches'] and obs['all_host_slots_restored_and_core_file_exact']
        assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
        assert report['ROM_sha256'] == plan['candidate_sha256'] == digest
        assert sha(Path(plan['original_genuine_save']).read_bytes()) == plan['donor_sha256'] == 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
        assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
        previous = read(plan['prior_report'])
        assert report['scripted_input_schedule'] == previous['scripted_input_schedule'] and report['core_options'] == previous['core_options']
        frames = {r['frame']: r for r in report['frames_captured']}
        native_path = Path(f'work/analysis/tavern_actual_continuations_v2192_{mode}/actual_snapshot_native_font_continuations.json')
        native = read(native_path)
        assert native['ARM9_sha256'] == sha(arm) and len(native['cases']) == len(obs['rows'])
        for row in obs['rows']:
            n = row['source_request']['ID']
            if n not in expected:
                continue
            assert row['bounds'] == [0, 0, 228, 48] and row['font_input_offset'] in (0, 2)
            full = next(r for r in native['cases'] if r['message_ID'] == n and r['text_hex'] == row['text_hex'])
            assert full['complete_native_return'] and full['SP_preserved'] and full['callee_registers_preserved'] and not full['faults'] and not full['error']
            raw = Path(row['snapshots']['WRAM']['path']).read_bytes()
            assert sha(raw) == row['snapshots']['WRAM']['sha256']
            printf_ptr = struct.unpack_from('<I', arm, 0x5444C)[0]
            printf = raw[printf_ptr-0x02000000:printf_ptr-0x02000000+512].split(b'\0')[0]
            match = re.fullmatch(b'(.*?)'.join(re.escape(p) for p in entries[n].text.split(b'%s')), printf)
            assert match is not None, (n, printf, entries[n].text)
            text = bytes.fromhex(row['text_hex'])
            assert b' '.join(text.split()) == b' '.join(printf.split())
            lines = [s.strip().decode('cp932') for s in text.split(b'\n')]
            events = []
            plane = raster(arm, text, 0x01FFCE40-0x02000000, size=(228, 64), instruction_limit=2000000, glyph_events=events)
            assert plane == independent_font(arm, kanji, lines)
            assert [r['code'] for r in events if r['code'] != 32] == glyph_codes(text)
            assert [r['code'] for r in full['glyph_events'] if r['code'] != 32] == glyph_codes(text)
            assert sorted({r['y'] for r in full['glyph_events']}) == list(range(0, 12*len(lines), 12))
            pixels = {(16+i%228, 296+i//228) for i, value in enumerate(plane) if value == 1}
            for f in expected[n]:
                capture = frames[f]
                image = Image.open(capture['path']).convert('RGB')
                assert sha(Path(capture['path']).read_bytes()) == capture['PNG_sha256']
                actual = {(x, y) for y in range(294, 360) for x in range(16, 244) if image.getpixel((x, y)) == (0, 8, 0)}
                assert actual == pixels, (mode, n, f, len(actual-pixels), len(pixels-actual))
                all_holds.append(dict(mode=mode, message_ID=n, font_frame=row['frame'], hold_frame=f, lines=lines, arguments_hex=[v.hex() for v in match.groups()], formatted_hex=text.hex(), capture=capture['path'], capture_sha256=capture['PNG_sha256'], complete_native_actual_independent_foreground_equal=True))
        snapshots = {r['frame']: r for r in report['read_only_capture_RAM_snapshots']}
        old_snapshots = {r['frame']: r for r in previous['read_only_capture_RAM_snapshots']}
        old_arm = NdsImage.open(previous['ROM']).read_file('/__arm9__.bin')
        model_controls, current_states = [], []
        for f in state_frames:
            raw, old_raw = [Path(q[f]['path']).read_bytes() for q in (snapshots, old_snapshots)]
            assert sha(raw) == snapshots[f]['sha256'] and sha(old_raw) == old_snapshots[f]['sha256']
            new_state, old_state = state(arm, raw), state(old_arm, old_raw)
            assert new_state == old_state, (mode, f, new_state, old_state)
            model_controls.append(dict(frame=f, models=models(arm, raw)))
            current_states.append(dict(frame=f, state=new_state, exact_to_historical_same_ordinary_inputs=True, current_RAM_sha256=sha(raw), reference_RAM_sha256=sha(old_raw)))
        assert all(r['models'] == model_controls[0]['models'] for r in model_controls)
        if mode == 'price':
            assert current_states[0]['state'] == current_states[-1]['state']
        runs.append(dict(mode=mode, frames=limit, source_plan=str(run/'run_plan.json'), source_plan_sha256=sha((run/'run_plan.json').read_bytes()), source_report=str(cap/'capture_report.json'), source_report_sha256=sha((cap/'capture_report.json').read_bytes()), source_observer=str(cap/'common_observer/requests.json'), source_observer_sha256=sha((cap/'common_observer/requests.json').read_bytes()), native_continuation=str(native_path), native_continuation_sha256=sha(native_path.read_bytes()), state_controls=current_states, unchanged_current_ship_models=model_controls, no_savestate_or_fixture=True))
        for f in ((7600, 8600, 9000, 9200) if mode == 'direct' else (5400, 5800, 6001)):
            controls.append(dict(mode=mode, frame=f, capture=frames[f]['path'], capture_sha256=frames[f]['PNG_sha256'], scope='actual-ordinary-menu-return-frame;visual-review-pending'))
    assert len(all_holds) == 8 and {r['message_ID'] for r in all_holds} == {821, 823, 827, 852}
    sheet = Image.new('RGB', (1024, 820), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, r in enumerate(all_holds):
        x, y = i%4*256, i//4*410
        draw.text((x+4, y+4), f"ID{r['message_ID']} frame{r['hold_frame']}", fill='white')
        sheet.paste(Image.open(r['capture']).convert('RGB'), (x, y+22))
    p = ROOT/'eight_ordinary_Tavern_holds.png'
    sheet.save(p)
    returns = Image.new('RGB', (1024, 820), '#263238')
    draw = ImageDraw.Draw(returns)
    for i, r in enumerate(controls):
        x, y = i%4*256, i//4*410
        draw.text((x+4, y+4), f"{r['mode']} frame{r['frame']}", fill='white')
        returns.paste(Image.open(r['capture']).convert('RGB'), (x, y+22))
    q = ROOT/'seven_ordinary_Tavern_returns.png'
    returns.save(q)
    save(ROOT/'ordinary_direct_and_price_foreground_state_transitions.json', dict(candidate=str(ROM), candidate_sha256=digest, actual_holds=all_holds, runs=runs, return_frames=controls, complete_original_direct_and_YesNo_native_font_returns=True, all_eight_actual_full_foregrounds_equal_native_and_independent=True, native_state_controls=8, no_ship_model_changes=True, ordinary_drink_cash_changes_exact_to_historical_source_inputs=True, original_genuine_donor_core_unchanged_and_host_slots_restored=True, no_savestate_or_any_synthetic_fixture=True, production_logical_view=[228,48], production_metrics=[6,12], physical16pixel_oracle_is_not_logical_capacity=True, only821_823_827_852_new_actual_visits_claimed=True, other59_conditions_offline_not_actual=True, visual_review_pending=True, review_sheet=str(p), review_sheet_sha256=sha(p.read_bytes()), returns_sheet=str(q), returns_sheet_sha256=sha(q.read_bytes()), not_full_route_or_hardware_verification=True, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print(dict(holds=8, actual_IDs=[821,823,827,852], state_controls=8, return_frames=7, review_sheet=str(p)))
