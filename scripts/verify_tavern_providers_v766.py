"""Replay the original provider fragments against the coordinate-safe runtime."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_coordinates_v766')
SOURCE = Path('scripts/verify_tavern_providers_owned_v764.py')


def main():
    prior = read('work/analysis/tavern_storage_v764/owned_provider_fragments.json')
    assert sha(SOURCE.read_bytes()) == prior['producer_sha256']
    text = SOURCE.read_text(encoding='utf-8')
    replacements = {
        'from dk4tool.patch import tavern_editorial_runtime as owned': 'from dk4tool.patch import tavern_coordinate_runtime as owned',
        "ROOT = Path('work/analysis/tavern_storage_v764')": "ROOT = Path('work/analysis/tavern_coordinates_v766')",
        "ROOT / 'owned_storage_and_native_research.json'": "ROOT / 'owned_runtime_plan.json'"}
    for before, after in replacements.items():
        assert text.count(before) == 1
        text = text.replace(before, after)
    exec(compile(text, str(SOURCE), 'exec'), {'__name__': '__main__', '__file__': str(SOURCE.resolve())})
    result = read(ROOT / 'owned_provider_fragments.json')
    assert result['cases'] == prior['cases']
    assert result['all94_global_coordinate_provider_outputs_unchanged'] == prior['all94_global_coordinate_provider_outputs_unchanged']
    result['coordinate_runtime_adapter'] = {'original_source_sha256': sha(SOURCE.read_bytes()),
        'effective_program_sha256': sha(text.encode('utf-8')), 'adapter_sha256': sha(Path(__file__).read_bytes()),
        'runtime_plan_sha256': sha((ROOT / 'owned_runtime_plan.json').read_bytes()), 'all_original_provider_outputs_equal_prior': True}
    save(ROOT / 'owned_provider_fragments.json', result)
    print('All202 original provider fragments and94 global coordinate outputs remain exact.', flush=True)


if __name__ == '__main__': main()
