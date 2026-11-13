"""Exact required-crew prompt, isolated fixture provenance and ordinary return."""

import inspect
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import verify_shared_recruit_gameplay_v782 as previous
from scripts.native_recruit_shortfall_fixture_v782 import set_condition
from scripts.verify_village_wrap_v608 import read, save


def load(folder):
    path = previous.capture.__globals__['CAP']/folder/'capture_report.json'
    report = read(path)
    assert report['frames'] == 8800 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
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
    assert len(fixtures) == 1 and fixtures[0]['frame'] == 3200
    _, proof = set_condition(arm, ram[3200], {'mode': 'required-crew-shortfall'})
    assert fixtures[0] == dict(proof, frame=3200)
    adapter = report['controlled_recruitment_adapter']
    assert adapter['original_harness_unchanged'] and adapter['single_import_replacement']
    assert adapter['original_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
    assert adapter['adapter_sha256'] == sha(Path('scripts/run_recruit_shortfall_capture_v782.py').read_bytes())
    assert adapter['fixture_producer_sha256'] == sha(Path('scripts/native_recruit_shortfall_fixture_v782.py').read_bytes())
    return path, report, arm, frames, ram


def main():
    source = inspect.getsource(previous.main)
    a = source.index("    pc, blink, unused_arm, blink_frames = capture(")
    b = source.index("    rom = NdsImage.open(new['ROM'])", a)
    source = source[:a]+'''    pc, blink_report, unused_arm, blink_frames, unused_ram = load('shared_v782_shortfall_highlight_baseline')
    assert blink_report['scripted_input_schedule'] == old['scripted_input_schedule']
    assert blink_report['core_options'] == old['core_options'] and blink_report['ROM_sha256'] == old['ROM_sha256']
'''+source[b:]
    replacements = {
        "'shared_v782_recruit_baseline'": "'shared_v782_shortfall_baseline'",
        "'shared_v782_recruit_live'": "'shared_v782_shortfall_live'",
        'selected = {6800: 1042, 7200: 1042}': 'selected = {6800: 1035, 7200: 1035}',
        "if f == 8000:": "if f == 8000 and diff.getbbox() is not None:",
        "'５１'.encode('cp932')": "'５'.encode('cp932')",
        "ROOT/'recruit_capacity_gameplay_verification.json'": "ROOT/'recruit_shortfall_gameplay_verification.json'",
        "'no_test_fixture_or_earned_unlock_claim'": "'one_declared_crew_halfword_fixture_no_earned_loss_claim'",
        "'required-shortfall1035-1041', ": '',
        'complete1042 holds': 'complete1035 holds',
    }
    for old, new in replacements.items():
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    target = previous.ROOT/'effective_shortfall_gameplay_verifier.py'
    target.write_text(source, encoding='utf-8')
    env = {**previous.__dict__, 'load': load, '__file__': str(Path(__file__).resolve())}
    exec(compile(source, str(target), 'exec'), env)
    env['main']()
    path = previous.ROOT/'recruit_shortfall_gameplay_verification.json'
    proof = read(path)
    proof['original_positive_capacity_count_and_cancellation_then_assign_sailors_flow_verified'] = False
    proof['original_required_shortfall_count_and_cancellation_then_assign_sailors_flow_verified'] = True
    proof['only_declared_ship_crew_halfword_changed_by_fixture'] = True
    proof['fixture_receipt_reproduced_from_prefixture_RAM_in_both_ROMs'] = True
    proof['effective_program_sha256'] = sha(source.encode())
    proof['reused_glyph_state_verifier_sha256'] = sha(Path(previous.__file__).read_bytes())
    save(path, proof)


if __name__ == '__main__':
    main()
