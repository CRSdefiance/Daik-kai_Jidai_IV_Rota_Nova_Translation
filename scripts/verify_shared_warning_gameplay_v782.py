"""Original low-success branch, complete displayed warning and cancellation."""

import inspect
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import verify_shared_recruit_gameplay_v782 as previous
from scripts.native_warning_fixture_v782_v3 import set_condition
from scripts.verify_village_wrap_v608 import read, save

CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def load(folder):
    path = CAP/folder/'capture_report.json'
    report = read(path)
    assert report['frames'] == 13400 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['hardware_device_verification'] and not report['goal_complete']
    assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
    arm = NdsImage.open(report['ROM']).read_file('/__arm9__.bin')
    donor = report['battery_save_preloaded']
    assert donor['source'] != donor['destination'] and donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256'] == 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
    assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_condition_fixtures')
    ram, frames = {}, {}
    for row in report.get('read_only_capture_RAM_snapshots', [])+report['read_only_pause_RAM_snapshots']:
        raw = Path(row['path']).read_bytes()
        assert len(raw) == row['bytes'] == 0x400000 and row['read_only_export'] and sha(raw) == row['sha256']
        if row['frame'] in ram:
            assert ram[row['frame']] == raw
        ram[row['frame']] = raw
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        frames[row['frame']] = row
    fixtures = report['synthetic_condition_fixtures']
    assert [(f['frame'], f['mode']) for f in fixtures] == [(3200, 'enable-schemes'), (9400, 'low-success-warning')]
    for fixture in fixtures:
        _, proof = set_condition(arm, ram[fixture['frame']], {'mode': fixture['mode']})
        assert fixture == dict(proof, frame=fixture['frame'])
    adapter = report['controlled_warning_adapter']
    assert adapter['original_harness_unchanged'] and adapter['single_import_replacement']
    assert adapter['original_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
    assert adapter['adapter_sha256'] == sha(Path('scripts/run_warning_capture_v782_v3.py').read_bytes())
    assert adapter['fixture_producer_sha256'] == sha(Path('scripts/native_warning_fixture_v782_v3.py').read_bytes())
    return path, report, arm, frames, ram


def main():
    source = inspect.getsource(previous.main)
    a = source.index("    pc, blink, unused_arm, blink_frames = capture(")
    b = source.index("    rom = NdsImage.open(new['ROM'])", a)
    source = source[:a]+source[b:]
    a = source.index('            if f == 8000:')
    b = source.index("            assert diff.getbbox() is None, (f, 'unselected full screen'", a)
    source = source[:a]+source[b:]
    replacements = {
        "'shared_v782_recruit_baseline'": "'shared_v782_warning_baseline3'",
        "'shared_v782_recruit_live'": "'shared_v782_warning_live3'",
        'selected = {6800: 1042, 7200: 1042}': 'selected = {12200: 1022, 12600: 1022}',
        "('５１'.encode('cp932'),)": '()',
        "ROOT/'recruit_capacity_gameplay_verification.json'": "ROOT/'warning_gameplay_verification.json'",
        "'original_positive_capacity_count_and_cancellation_then_assign_sailors_flow_verified'": "'original_low_success_warning_and_normal_cancellation_verified'",
        "'normal_town_return_frame': 8800": "'normal_town_return_frame': 13400",
        "'no_test_fixture_or_earned_unlock_claim'": "'two_declared_native_prerequisite_fixtures_no_earned_condition_claim'",
        "'observed_speaker': 'Charles Rochefort'": "'observed_speaker': 'Gerhard'",
        'complete1042 holds': 'complete1022 holds',
    }
    for old, new in replacements.items():
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    target = previous.ROOT/'effective_warning_gameplay_verifier.py'
    target.write_text(source, encoding='utf-8')
    env = {**previous.__dict__, 'load': load, '__file__': str(Path(__file__).resolve())}
    exec(compile(source, str(target), 'exec'), env)
    env['main']()
    path = previous.ROOT/'warning_gameplay_verification.json'
    proof = read(path)
    extra = []
    for folder in ('shared_v782_warning_baseline3', 'shared_v782_warning_live3'):
        _, report, arm, _, ram = load(folder)
        before, after = [previous.state(arm, ram[f]) for f in (11800, 13400)]
        assert before['cash'] == after['cash']
        assert previous.tasks(arm, ram[11800]) == previous.tasks(arm, ram[13400])
        extra.append({'ROM_sha256': report['ROM_sha256'], 'before': before, 'after': after,
                      'no_1000_coin_charge': True, 'no_new_job_scheduled': True})
    proof['original_financial_and_job_cancellation_outcomes'] = extra
    proof['both_fixture_receipts_reproduced_from_prefixture_RAM_in_both_ROMs'] = True
    proof['other_shared_families_pending'] = ['information1020', 'village1028-1029', 'fleet1030-1034', 'private1049-1069']
    proof['effective_program_sha256'] = sha(source.encode())
    proof['reused_glyph_state_verifier_sha256'] = sha(Path(previous.__file__).read_bytes())
    save(path, proof)


if __name__ == '__main__':
    main()
