"""Verify a naturally selected private topic after original gift acceptance."""

import inspect
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import verify_shared_recruit_gameplay_v782 as previous
from scripts.aggregate_barmaid_gameplay_v780 import actual_state
from scripts.native_barmaid_gift_fixture_v783 import transfer
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shared_metadata_v783')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def load(folder):
    path = CAP/folder/'capture_report.json'
    report = read(path)
    assert report['frames'] == 39200 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['hardware_device_verification'] and not report['goal_complete']
    assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
    arm = NdsImage.open(report['ROM']).read_file('/__arm9__.bin')
    donor = report['battery_save_preloaded']
    assert donor['source'] != donor['destination'] and donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256'] == '942c74828a7b7396f7567ca2d405ddc4cdd329e4837f591777d35ee458794b0f'
    assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_inventory_fixtures')
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
    fixtures = report['synthetic_inventory_fixtures']
    assert len(fixtures) == 1 and fixtures[0]['frame'] == 22400
    _, expected = transfer(arm, ram[22400], [143])
    assert fixtures[0] == dict(expected, frame=22400)
    adapter = report['controlled_private_barmaid_adapter']
    assert adapter['original_harness_unchanged'] and adapter['single_inventory_import_replacement']
    assert adapter['original_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
    assert adapter['adapter_sha256'] == sha(Path('scripts/run_private_barmaid_capture_v783.py').read_bytes())
    assert adapter['fixture_producer_sha256'] == sha(Path('scripts/native_barmaid_gift_fixture_v783.py').read_bytes())
    assert adapter['frozen_fixture_producer_sha256'] == sha(Path('scripts/native_barmaid_gift_fixture_v780_v3.py').read_bytes())
    assert adapter['no_location_relationship_rng_or_dialogue_injection']
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
        "'shared_v782_recruit_baseline'": "'shared_v783_private_baseline2'",
        "'shared_v782_recruit_live'": "'shared_v783_private_live2'",
        'selected = {6800: 1042, 7200: 1042}': 'selected = {32000: 1065}',
        "('５１'.encode('cp932'),)": '()',
        "ROOT/'recruit_capacity_gameplay_verification.json'": "ROOT/'private_barmaid_gameplay_verification.json'",
        "'original_positive_capacity_count_and_cancellation_then_assign_sailors_flow_verified'": "'original_gift_acceptance_chance_based_private_chat_and_normal_return_verified'",
        "'normal_town_return_frame': 8800": "'normal_town_return_frame': 39200",
        "'no_test_fixture_or_earned_unlock_claim'": "'declared_gift_inventory_fixture_no_earned_item_acquisition_claim'",
        "'observed_speaker': 'Charles Rochefort'": "'observed_speaker': 'Reika'",
        'complete1042 holds': 'complete private1065 hold',
    }
    for old, new in replacements.items():
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    assert source.count("ROOT/'full_entry_format_case.py'") == 2
    source = source.replace("ROOT/'full_entry_format_case.py'", "FORMAT_ROOT/'full_entry_format_case.py'")
    target = ROOT/'effective_private_barmaid_gameplay_verifier.py'
    target.write_text(source, encoding='utf-8')
    env = {**previous.__dict__, 'load': load, 'ROOT': ROOT, 'FORMAT_ROOT': previous.ROOT, '__file__': str(Path(__file__).resolve())}
    exec(compile(source, str(target), 'exec'), env)
    env['main']()
    path = ROOT/'private_barmaid_gameplay_verification.json'
    proof = read(path)
    outcomes = []
    for folder in ('shared_v783_private_baseline2', 'shared_v783_private_live2'):
        _, report, arm, _, ram = load(folder)
        states = {f: actual_state(arm, ram[f], 57) for f in (3200, 22400, 26000, 26800, 32000, 39200)}
        assert states[3200]['original_relationship_stage'] == 0
        assert states[22400]['original_relationship_stage'] == states[26000]['original_relationship_stage'] == 1
        assert states[3200]['original_gift_owner_kind'] == 4 and states[3200]['original_gift_owner_detail'] == 38
        assert states[26000]['original_gift_owner_kind'] == 0 and states[26000]['gift_availability_mask'] == 4
        for f in (26800, 32000, 39200):
            assert states[f]['original_relationship_stage'] == 2
            assert states[f]['original_gift_owner_kind'] == 6 and states[f]['gift_availability_mask'] == 0
        before, after = [previous.state(arm, ram[f]) for f in (26800, 39200)]
        assert before['cash']-after['cash'] == 4*(5+10)
        assert previous.tasks(arm, ram[26800]) == previous.tasks(arm, ram[39200])
        outcomes.append({'ROM_sha256': report['ROM_sha256'], 'original_relationship_and_gift_states': states,
                         'before_postgift_drinks': before, 'normal_return': after,
                         'four_original_5_plus_10_coin_drink_orders': True, 'no_new_job_scheduled': True})
    proof.update({'gift_fixture_receipt_reproduced_from_prefixture_RAM_in_both_ROMs': True,
                  'original_financial_gift_and_relationship_outcomes': outcomes,
                  'other_shared_families_pending': [], 'private_family_actual_sample_complete': True,
                  'other20_private_topics_have_source_native_matrix_font_and_family_sampling_not_individual_activation': True,
                  'no_location_relationship_rng_or_dialogue_injection': True,
                  'effective_program_sha256': sha(source.encode()),
                  'reused_glyph_state_verifier_sha256': sha(Path(previous.__file__).read_bytes())})
    save(path, proof)


if __name__ == '__main__':
    main()
