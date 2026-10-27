"""Two-byte controlled native actor/nameplate probe; never a playable release."""

import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/held_actor_v295')
ROM = Path('out/all_routes_combined_v275_candidate.nds')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert sha(ROM.read_bytes()) == '94fa82c8edd99de4f21829bc94b1b98013929f98cc1378c73fe0768e1d1caddf'
    image = NdsImage.open(ROM)
    source = image.read_file('/data/SC0.DK4')
    container = IlnkContainer.parse(source)
    records = container.blocks[44].split(b'\0')
    changed = []
    for index, actor in ((179, 10), (187, 151)):
        old = records[index]
        assert old[0] == 6
        records[index] = bytes([actor]) + old[1:]
        changed.append({'record': f'DK4_MES_B44_R{index:04d}', 'old_actor': 6,
                        'probe_actor': actor, 'old_hex': old.hex(), 'target_hex': records[index].hex()})
    container.blocks[44] = b'\0'.join(records)
    target = container.to_bytes()
    assert len(source) == len(target)
    assert sum(a != b for a, b in zip(source, target, strict=True)) == 2
    image.replace_file('/data/SC0.DK4', target)
    fixture = ROOT / 'actor0A_actor97_research_only.nds'
    image.save(fixture)
    saved = NdsImage.open(fixture)
    original = NdsImage.open(ROM)
    assert {p: bytes(d) for _, p, d in saved.iter_files() if p != '/data/SC0.DK4'} == {
        p: bytes(d) for _, p, d in original.iter_files() if p != '/data/SC0.DK4'}
    schedule = json.loads(Path('work/emulation_v193/dialogue_pagination_v288/capture_report.json').read_text(encoding='utf-8'))['scripted_input_schedule']
    schedule += [{'start': 10841, 'duration': 8, 'buttons': ['A']},
                 {'start': 11241, 'duration': 8, 'buttons': ['A']}]
    (ROOT / 'probe_inputs.json').write_text(json.dumps(schedule, indent=2) + '\n', encoding='utf-8')
    manifest = {'format': 'dk4-held-actor-controlled-probe-v295',
                'source_ROM': str(ROM), 'source_ROM_sha256': sha(ROM.read_bytes()),
                'research_ROM': str(fixture), 'research_ROM_sha256': sha(fixture.read_bytes()),
                'changed_file': '/data/SC0.DK4', 'changed_bytes': 2, 'changed_records': changed,
                'all_other_files_native_code_graphics_and_allocations_exact': True,
                'ordinary_input_cold_boot_actual_actor_effect_pending': True,
                'not_original_held_scene_locations': True, 'not_for_playable_handoff': True,
                'full_goal_complete': False}
    (ROOT / 'fixture_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print('Two speaker bytes changed in controlled prompts; all code/graphics/allocations exactV275.')


if __name__ == '__main__':
    main()
