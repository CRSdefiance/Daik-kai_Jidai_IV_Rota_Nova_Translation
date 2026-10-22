"""Disposable file-substitution fixture for the original movie GPU renderer.

Not a playable release, route completion, legitimate unlock or ending trigger.
"""

import argparse
import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

PARENT = Path('out/all_routes_combined_v326_candidate.nds')
ROOT = Path('work/analysis/movie_gpu_fixture_v336')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--movie', default='/FLS/M28.fls')
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    parent = NdsImage.open(PARENT)
    manifest = json.loads(PARENT.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    assert manifest['candidate_sha256'] == sha(PARENT.read_bytes())
    assert len(manifest['batches']) == 470
    source = parent.read_file(args.movie)
    before = {p: raw for _, p, raw in parent.iter_files()} | dict(parent.iter_components())
    fixture = NdsImage.open(PARENT)
    fixture.replace_file('/FLS/M20.fls', source)
    name = Path(args.movie).stem.lower()
    out = ROOT / f'research_only_{name}_through_m20.nds'
    fixture.save(out)
    saved = NdsImage.open(out)
    after = {p: raw for _, p, raw in saved.iter_files()} | dict(saved.iter_components())
    assert before.keys() == after.keys()
    assert [p for p in before if before[p] != after[p]] == ['/FLS/M20.fls']
    assert saved.read_file('/FLS/M20.fls') == source
    assert sha(PARENT.read_bytes()) == manifest['candidate_sha256']
    inputs = json.loads(Path('work/emulation_v193/movie_viewport_v303_rafael/capture_report.json').read_text(encoding='utf-8'))['scripted_input_schedule']
    (ROOT / 'opening_inputs.json').write_text(json.dumps(inputs, indent=2) + '\n', encoding='utf-8')
    proof = {'research_only': True, 'not_registered_playable_or_distribution_candidate': True,
             'parent': str(PARENT), 'parent_sha256': manifest['candidate_sha256'],
             'research_ROM': str(out), 'research_ROM_sha256': sha(out.read_bytes()),
             'original_opening_filename': '/FLS/M20.fls', 'substituted_exact_movie': args.movie,
             'substituted_movie_sha256': sha(source), 'only_changed_internal_file': '/FLS/M20.fls',
             'all_code_other_art_routes_COMMON_HELP_ARM7_and_components_exact_parent': True,
             'no_save_unlock_flags_RAM_injection_or_script_command_change': True,
             'production_parent_unchanged': True,
             'does_not_prove_normal_movie_caller_unlock_or_ending_gameplay': True}
    (ROOT / f'{name}_fixture_manifest.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'research_ROM': str(out), 'movie': args.movie, 'parent_unchanged': True}))


if __name__ == '__main__':
    main()
