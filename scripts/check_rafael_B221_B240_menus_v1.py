"""Run the fresh native caption checks on each exact B221–B240 menu."""
from pathlib import Path
import subprocess
import sys

from scripts.audit_story_glyph_consistency import load, save
from scripts.write_rafael_B221_B240_contextual_v1 import OUT, ROOT, digest

RELEASE = Path('work/analysis/Rafael2952_extended_release_verified_v1_20261106')
OUTPUT = ROOT / 'native_menus_v1'
EXPECTED = {2: {(224, 64), (233, 136)}, 3: {(224, 242)}}
CHECKER = {2: 'scripts.check_rafael_two_choice_batch_v2', 3: 'scripts.check_rafael_three_choice_batch_v1'}


def main():
    doc = load(OUT)
    OUTPUT.mkdir(exist_ok=False)
    for count, keys in EXPECTED.items():
        rows = [row for row in doc['records'] if row['kind'] == 'typed-choice-label'
                and row['source_count'] == count]
        assert {(row['block'], row['source_command_offset']) for row in rows} == keys
        assert len(rows) == count * len(keys)
        path = OUTPUT / f'{count}_caption_objects.json'
        subset = {**doc, 'records': rows, 'blocks': sorted({row['block'] for row in rows}),
                  'typed_choice_objects': len(rows), 'typed_choice_commands': len(keys),
                  'ordinary_speech_objects': 0, 'subset_of': str(OUT), 'subset_of_sha256': digest(OUT)}
        save(path, subset)
        subprocess.run([sys.executable, '-m', CHECKER[count], '--manuscript', str(path),
                        '--release', str(RELEASE / 'registered_release_verification.json'),
                        '--startup', str(RELEASE / 'own_registered_startup_verification.json'),
                        '--out', str(OUTPUT / f'{count}_option_proofs')], check=True)


if __name__ == '__main__':
    main()

