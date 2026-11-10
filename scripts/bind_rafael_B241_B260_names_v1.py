from scripts.bind_rafael_B221_B240_names_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    "ROOT = A / 'Rafael_B221_B240_current2952_20261106'": "ROOT = Path('work/Rafael_B241_B260_editorial_20261106')",
    "CURRENT = ROOT / 'current_effective.json'": "CURRENT = ROOT / 'current_effective.json/current_effective.json'",
    "PRIOR = [A / p for p in (": "PRIOR = [A / p for p in (\n    'Rafael_B221_B240_current2952_20261106/names_and_terms_v1.json',",
    "assert len(actors) == 26": "assert len(actors) == 20",
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::exact-twenty-public-name-consumers', 'exec'), globals())
