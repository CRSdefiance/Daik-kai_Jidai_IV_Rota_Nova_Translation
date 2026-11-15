"""Seal source-first drafts for complete B249–B260 exchanges."""
from pathlib import Path
import sys

from scripts.seal_clean_independent_drafts_v1 import seal

ROOT = Path('work/analysis/Rafael_B241_B260_clean_20261106')
OUT = Path('work/Rafael_B241_B260_editorial_20261106')
PARTS = {'249_252': 98, '253_256': 62, '257_260': 38}


def main(part):
    contexts, ordinary, choices = {}, {}, {}
    path = Path(f'translations/rafael_B{part.replace("_", "_B")}_clean_drafts_v1.txt')
    for line in path.read_text(encoding='utf-8').splitlines():
        if not line or line.startswith('#'):
            continue
        key, meaning, english = line.split('|', 2)
        if key.startswith('@'):
            assert not english
            block = int(key[1:])
            assert block not in contexts
            contexts[block] = meaning
            ordinary[block] = {}
        elif key.startswith('C'):
            index = int(key[1:])
            assert (block, index) not in choices
            choices[block, index] = meaning, english
        else:
            index = int(key)
            assert index not in ordinary[block]
            ordinary[block][index] = meaning, english
    OUT.mkdir(exist_ok=True)
    target = OUT / (path.stem + '.json')
    seal(ROOT, target.resolve(), ordinary, contexts, choices, path, PARTS[part])


if __name__ == '__main__':
    main(sys.argv[1])

