"""Prepare explicit current-ROM condition matrix, keeping prior audits exact."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_condition_fixture_v637 import ARM_SHA, set_condition
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/condition_matrix_v637')
ROM = Path('out/all_routes_combined_v636_candidate.nds')
DONOR = Path('E:/Rota Nova translations/Saves/maria-nagasaki-namahage-v514.dsv')
CAP = Path('work/emulation_v193/condition_matrix_v637')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes()) == 'c4ff537ddcd4da5eb1743fb28cd0eb160492e9b660af080ddae44e94a9f4d95d'
    assert sha(arm) == ARM_SHA
    assert sha(DONOR.read_bytes()) == 'fbae21aa2c5a695bde0eddfc10a3bbeb80d01478bd6a9ed743d824595dc3096e'
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    windows = [(0x7E070, 0x7E108), (0x80A84, 0x80AD0), (0xCB184, 0xCB190), (0x7F244, 0x7F25C)]
    assert all(arm[a:b] == clean[a:b] for a, b in windows)
    raw = Path('work/emulation_v193/conditions_live_v520/frame_004400_arm9_ram.bin').read_bytes()
    after, fixture = set_condition(arm, raw, {'actor': 3, 'health': 6, 'mood': 5})
    offset = fixture['actor_address'] + 6 - 0x02000000
    assert raw[:offset] == after[:offset] and raw[offset + 2:] == after[offset + 2:]
    rejected = []
    for label, other_arm, other_raw, values in [
        ('wrong_ROM', clean, raw, {'actor': 3, 'health': 0, 'mood': 0}),
        ('wrong_RAM_size', arm, raw[:-1], {'actor': 3, 'health': 0, 'mood': 0}),
        ('unreviewed_actor', arm, raw, {'actor': 0, 'health': 0, 'mood': 0}),
        ('invalid_health', arm, raw, {'actor': 3, 'health': 7, 'mood': 0}),
        ('invalid_mood', arm, raw, {'actor': 3, 'health': 0, 'mood': 6}),
        ('boolean_field', arm, raw, {'actor': 3, 'health': False, 'mood': 0}),
    ]:
        try:
            set_condition(other_arm, other_raw, values)
        except ValueError:
            rejected.append(label)
        else:
            raise AssertionError(label)
    save(ROOT / 'initial_inputs.json', read('work/analysis/conditions_v520/sailor_inputs.json'))
    frame, commands, cases = 4400, [], []
    for actor in (3, 10):
        if actor == 10:
            commands.append({'until': frame + 200, 'buttons': ['B'], 'duration': 8,
                             'condition_fixture': {'actor': 3, 'health': 0, 'mood': 3}})
            frame += 200
            commands.append({'until': frame + 200, 'buttons': ['RIGHT'], 'duration': 8,
                             'condition_fixture': {'actor': 10, 'health': 0, 'mood': 0}})
            frame += 200
            # Already in the crew list, so enter Xien before starting the regular B/A cycle.
            commands.append({'until': frame + 200, 'buttons': ['A'], 'duration': 8})
            frame += 200
        for health in range(7):
            for mood in range(6):
                values = {'actor': actor, 'health': health, 'mood': mood}
                commands.append({'until': frame + 200, 'buttons': ['B'], 'duration': 8,
                                 'condition_fixture': values})
                frame += 200
                commands.append({'until': frame + 200, 'buttons': ['A'], 'duration': 8})
                frame += 200
                cases.append({**values, 'frame': frame, 'fixture_frame': frame - 400})
    commands.append({'stop': True})
    save(ROOT / 'cases.json', cases)
    (ROOT / 'commands.jsonl').write_text(''.join(__import__('json').dumps(c) + '\n' for c in commands), encoding='utf-8')
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    save(ROOT / 'audit_before.json', {name: read(Path('translations') / name) for name in frozen})
    save(ROOT / 'preflight.json', {
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'arm_sha256': sha(arm),
        'profile': 'all-routes-unified-v636', 'donor': str(DONOR), 'donor_sha256': sha(DONOR.read_bytes()),
        'frames': frame + 1, 'last_pause_frame': frame, 'cases': len(cases),
        'each_actor_has_all42_health_mood_combinations': True,
        'original_selector_actor_binding_and_getter_windows_exact': windows,
        'fixture_negative_controls_rejected': rejected,
        'historical_RAM_used_only_for_preflight_never_loaded_into_emulator': True,
        'ROM_patch_registry_and_canonical_hashes': {
            str(p): sha(p.read_bytes()) for p in [ROM, ROM.with_suffix('.xdelta'), ROM.with_suffix('.manifest.json'),
            Path('translations/release_stack.json'), Path('out/raphael_natural_v2_accepted_base.nds')]},
        'scripts': {str(p): sha(p.read_bytes()) for p in [Path(__file__),
            Path('scripts/native_condition_fixture_v637.py'), Path('scripts/headless_desmume_v193.py')]},
        'full_goal_complete': False,
    })
    print(f'Prepared {len(cases)} cases, final pause {frame}, {len(commands)} commands; six negative controls pass.')


if __name__ == '__main__':
    main()
