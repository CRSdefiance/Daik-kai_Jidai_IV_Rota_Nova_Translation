"""Extend only ordinary A inputs/capture time to investigate the unobserved QA-host exit."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil361_B283_B298_clean_20261110')


def main():
    out = ROOT / 'extended_tail_v1'
    assert not out.exists()
    parent = ROOT / 'display_fixtures_v1/Lil361_forest_London_fixture.json'
    fixture = load(parent)
    assert digest(fixture['research_ROM']) == fixture['research_ROM_sha256']
    original = load(fixture['inputs'])
    assert digest(fixture['inputs']) == fixture['inputs_sha256']
    inputs = deepcopy(original)
    end = fixture['frames'] + 6000
    last = max(row['start'] for row in original)
    for frame in range(last + 240, end - 100, 240):
        inputs.append(dict(start=frame, duration=16, buttons=['A']))
    assert inputs[:len(original)] == original
    assert all(row['buttons'] == ['A'] and row['duration'] == 16 for row in inputs[len(original):])
    out.mkdir()
    inputpath = out / 'ordinary_inputs.json'
    save(inputpath, inputs)
    updated = {**fixture, 'inputs': str(inputpath), 'inputs_sha256': digest(inputpath), 'frames': end}
    save(out / 'fixture.json', updated)
    assert all(updated[k] == v for k, v in fixture.items() if k not in ['inputs', 'inputs_sha256', 'frames'])
    save(out / 'extension.json', dict(original_fixture=str(parent), original_fixture_sha256=digest(parent),
        original_frames=fixture['frames'], extended_frames=end, original_input_prefix_exact=True,
        ROM_all_commands_controls_setup_andexit_unchanged=True, no_memory_save_orstate_override=True,
        purpose='Investigate missing post-dialogue native host transition with a longer ordinary-input tail.',
        new_credit=0, guide_photos=False))
    print('Prepared unchanged-ROM fixture with6000 extra ordinary-input frames.')


if __name__ == '__main__':
    main()
