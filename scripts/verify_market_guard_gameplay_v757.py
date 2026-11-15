"""Bind V757 actual replays to the completed V756 semantic/font evidence."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_market_stock_edge_fixture_v757 import assign as edge
from scripts.native_market_stock_fixture_v757 import assign
from scripts.native_market_stock_seed_fixture_v757 import assign as seed
from scripts.verify_market_stock_gameplay_v756 import persistent_models
from scripts.verify_market_gameplay_v753 import SAVE_SHA, snapshot
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/market_stock_release_v757')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v757_candidate.nds')


def checked(folder):
    p = CAP / folder / 'capture_report.json'
    d = read(p)
    assert d['cold_boot'] and not d['savestate_loaded'] and not d['callback_errors']
    assert not d['hardware_device_verification'] and not d['goal_complete']
    assert d['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(d['ROM']).read_bytes()) == d['ROM_sha256']
    rows = {}
    for r in d['frames_captured']:
        assert sha(Path(r['path']).read_bytes()) == r['PNG_sha256']
        rows[r['frame']] = r
    return p, d, rows


def main():
    old_proof = Path('work/analysis/market_stock_release_v756/gameplay_verification.json')
    proof = read(old_proof)
    assert proof['producer_sha256'] == sha(Path('scripts/verify_market_stock_gameplay_v756.py').read_bytes())
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    cases = []
    for mode in ('one', 'two', 'edge', 'seed3', 'newgame'):
        suffix = 'one_seed3_756' if mode == 'seed3' else 'newgame' if mode == 'newgame' else mode + '_756'
        pa, a, before = checked('market_v756_' + suffix)
        pb, b, after = checked('market_v757_' + mode + ('' if mode == 'newgame' else '_verified'))
        assert b['ROM_sha256'] == sha(ROM.read_bytes())
        assert a['frames'] == b['frames'] and a['core_options'] == b['core_options']
        assert a['scripted_input_schedule'] == b['scripted_input_schedule'] and set(before) == set(after)
        matches = []
        for frame in after:
            assert Path(before[frame]['path']).read_bytes() == Path(after[frame]['path']).read_bytes(), (mode, frame)
            matches.append(frame)
        fixtures = b.get('synthetic_market_display_fixtures', [])
        if mode == 'newgame':
            assert not fixtures and not b.get('battery_save_preloaded')
        else:
            donor = b['battery_save_preloaded']
            assert donor['source'] != donor['destination'] and donor['source_sha256'] == SAVE_SHA
            assert sha(Path(donor['source']).read_bytes()) == SAVE_SHA and donor['copied_byte_exact_before_cold_boot']
            assert len(fixtures) == (2 if mode == 'seed3' else 1)
            _, receipt = (edge if mode == 'edge' else assign)(arm, snapshot(b, 3200), {'mode': 'one' if mode == 'seed3' else mode})
            assert fixtures[0]['frame'] == 3200 and receipt == {k: v for k, v in fixtures[0].items() if k != 'frame'}
            if mode == 'seed3':
                _, receipt = seed(arm, snapshot(b, 7200), {'mode': 'rng', 'seed': 3})
                assert fixtures[1]['frame'] == 7200 and receipt == {k: v for k, v in fixtures[1].items() if k != 'frame'}
            adapter = b['controlled_market_harness_adapter']
            path = Path('scripts/run_market_stock_seed_capture_v757.py' if mode == 'seed3' else
                        'scripts/run_market_stock_edge_capture_v757.py' if mode == 'edge' else 'scripts/run_market_stock_capture_v757.py')
            assert adapter['original_harness_file_unchanged'] and adapter['adapter_sha256'] == sha(path.read_bytes())
            assert adapter['unchanged_original_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
            frames = b['exact_requested_capture_frames']
            for frame in frames:
                assert persistent_models(arm, snapshot(a, frame)) == persistent_models(arm, snapshot(b, frame)), (mode, frame)
        cases.append({'scenario': mode, 'baseline_report': str(pa), 'baseline_report_sha256': sha(pa.read_bytes()),
                      'candidate_report': str(pb), 'candidate_report_sha256': sha(pb.read_bytes()),
                      'all_whole_two_screen_frame_matches': matches, 'all_sampled_complete_persistent_models_equal': mode != 'newgame'})
    for path in ('E:/Rota Nova translations/Saves/hodram-istanbul-golden-cutlass-blue-oak-v474.dsv',
                 'E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv'):
        assert sha(Path(path).read_bytes()) == SAVE_SHA
    save(ROOT / 'gameplay_verification.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'prior_semantic_native_font_and_source_state_proof': str(old_proof), 'prior_proof_sha256': sha(old_proof.read_bytes()),
        'actual_V757_replays': cases, 'all_sampled_frames_and_persistent_models_equal_V756': True,
        'actual_stock767_768_not_all17_reward_activations': True,
        'no_hardware_full_route_or_earned_fixture_state_claim': True,
        'source_saves_unchanged_sha256': SAVE_SHA, 'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V757 five complete actual cold-boot replays match V756 frames/models; saves unchanged.', flush=True)


if __name__ == '__main__':
    main()
