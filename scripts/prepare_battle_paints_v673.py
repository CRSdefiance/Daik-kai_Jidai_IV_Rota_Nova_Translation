"""Freeze an existing complete encounter/victory schedule for image observation."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_graphic_paints_v669 import ROM
from scripts.native_battle_proximity_v673 import apply_fixture
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_paints_v673')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'preflight.json').exists()
    old_path = Path('work/analysis/full_fleet_victory_v654/replay_preflight.json')
    old = read(old_path)
    old_commands = read(old['commands'])
    commands = [{k: v for k, v in row.items() if k != 'export_native_state'} for row in old_commands]
    assert len(commands) == 79 and commands[-1] == {'stop': True}
    save(ROOT / 'commands.json', commands)
    old_report_path = Path(old['output']) / 'capture_report.json'
    old_report = read(old_report_path)
    assert old_report['frames'] == 28400 and not old_report['callback_errors']
    assert sha(Path(old['donor']).read_bytes()) == old['donor_sha256']
    raw_path = Path(old['output']) / 'frame_004800_arm9_ram.bin'
    raw = raw_path.read_bytes()
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    _, receipt = apply_fixture(arm, raw, 'approach')
    rejected = []
    for label, other_arm, other_raw, action in (
        ('wrong_ARM', NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'), raw, 'approach'),
        ('recovery_not_permitted', arm, raw, 'recover'), ('wrong_RAM_size', arm, raw[:-1], 'approach'),
    ):
        try:
            apply_fixture(other_arm, other_raw, action)
        except ValueError:
            rejected.append(label)
        else:
            raise AssertionError(label)
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    observer, contract = Path('scripts/observe_graphic_paints_v669.py'), Path('work/analysis/graphic_paints_v669/source_contract.json')
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
            ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'),
            Path('out/raphael_natural_v2_accepted_base.nds'))},
        'old_preflight': str(old_path), 'old_preflight_sha256': sha(old_path.read_bytes()),
        'previous_report': str(old_report_path), 'previous_report_sha256': sha(old_report_path.read_bytes()),
        'donor': old['donor'], 'donor_sha256': old['donor_sha256'],
        'inputs': old['inputs'], 'inputs_sha256': sha(Path(old['inputs']).read_bytes()),
        'commands': str(ROOT / 'commands.json'), 'commands_sha256': sha((ROOT / 'commands.json').read_bytes()),
        'original_commands': old['commands'], 'original_commands_sha256': sha(Path(old['commands']).read_bytes()),
        'only_read_only_native_export_requests_removed_from_original_commands': True,
        'observer': str(observer), 'observer_sha256': sha(observer.read_bytes()),
        'observer_contract': str(contract), 'observer_contract_sha256': sha(contract.read_bytes()),
        'fixture_wrapper': 'scripts/native_battle_proximity_v673.py',
        'fixture_wrapper_sha256': sha(Path('scripts/native_battle_proximity_v673.py').read_bytes()),
        'preflight_original_historical_RAM_never_loaded_into_emulator': True,
        'fixture_contract': receipt, 'rejected_fixture_controls': rejected,
        'previous_goal_turn_classification': 'progress: V672 complete controlled embedded paints and exact held-out palette correspondence, archived and audited',
        'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
        'full_goal_complete': False})
    print('V673 battle/victory schedule and coordinate-only fixture locked; three rejection controls pass.')


if __name__ == '__main__':
    main()
