"""Freeze two different actual UI contexts for the existing source-bound observer."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_graphic_paints_v669 import ROM
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/graphic_contexts_v670')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'preflight.json').exists()
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    source = Path('work/analysis/graphic_paints_v669/source_contract.json')
    observer = Path('scripts/observe_graphic_paints_v669.py')
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
            ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'),
            Path('out/raphael_natural_v2_accepted_base.nds'))},
        'observer_source': str(observer), 'observer_source_sha256': sha(observer.read_bytes()),
        'observer_contract': str(source), 'observer_contract_sha256': sha(source.read_bytes()),
        'previous_goal_turn_classification': 'progress: V669 full Frame/Marker bindings, three primitives, six terminal runs and archive',
        'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen}})
    cases = {}
    crew_pre = read('work/analysis/crew_policy_matrix_v657/preflight.json')
    crew_old = Path(crew_pre['output']) / 'capture_report.json'
    crew_report = read(crew_old)
    assert crew_report['frames'] == 17500 and not crew_report['callback_errors']
    inputs = Path('work/analysis/crew_policy_matrix_v657/full_inputs.json')
    assert read(inputs) == crew_report['scripted_input_schedule']
    cases['crew'] = {'inputs': str(inputs), 'inputs_sha256': sha(inputs.read_bytes()),
        'donor': crew_pre['donor'], 'donor_sha256': crew_pre['donor_sha256'], 'frames': 17500,
        'capture_frames': sorted({s['frame'] for s in crew_report['frames_captured']}),
        'previous_report': str(crew_old), 'previous_report_sha256': sha(crew_old.read_bytes()),
        'no_gameplay_fixtures': True}
    race_pre = read('work/analysis/race_roster_v661/preflight.json')
    race_old = CAP / 'race_roster_v661_controlled_ring/capture_report.json'
    race_report = read(race_old)
    assert race_report['frames'] == 5000 and not race_report['callback_errors']
    race_inputs = ROOT / 'race_inputs.json'
    save(race_inputs, read('work/analysis/race_roster_v661/controlled_inputs_ring.json'))
    assert read(race_inputs) == race_report['scripted_input_schedule']
    manifest = deepcopy(read('work/analysis/race_roster_v661/current_unlock_manifest.json'))
    manifest.update(production_ROM=str(ROM), production_ROM_sha256=sha(ROM.read_bytes()),
                    current_test_scope='Existing isolated Grand Race four-card receive-ring UI; no wireless or earned unlock claim')
    save(ROOT / 'current_unlock_manifest.json', manifest)
    cases['race'] = {'inputs': str(race_inputs), 'inputs_sha256': sha(race_inputs.read_bytes()),
        'donor': race_pre['donor'], 'donor_sha256': race_pre['donor_sha256'], 'frames': 5000,
        'capture_frames': sorted({s['frame'] for s in race_report['frames_captured']}),
        'previous_report': str(race_old), 'previous_report_sha256': sha(race_old.read_bytes()),
        'receive_ring_and_readiness_UI_fixture': True, 'wireless_peer_test': False,
        'gallery_unlock_manifest': str(ROOT / 'current_unlock_manifest.json')}
    for case in cases.values():
        assert sha(Path(case['donor']).read_bytes()) == case['donor_sha256']
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    reference = NdsImage.open('out/all_routes_combined_v653_candidate.nds').read_file('/__arm9__.bin')
    spans = ((0xF98FC, 0xF9F10), (0xFA5B0, 0xFA6B0), (0xFABB0, 0xFAF00),
             (0xFB528, 0xFB6B0), (0x10C4E8, 0x10C5A0), (0x10CB74, 0x10CE00))
    assert all(arm[a:b] == reference[a:b] for a, b in spans)
    save(ROOT / 'run_cases.json', {'cases': cases,
        'original_race_controller_packet_and_receive_code_exact_V653': [list(s) for s in spans],
        'current_code_diff_only_V666_seven_village_data_repairs': True,
        'full_goal_complete': False})
    print('V670 two frozen schedules/donors and original packet-code guards prepared; no ROM changed.')


if __name__ == '__main__':
    main()
