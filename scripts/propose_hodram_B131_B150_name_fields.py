"""Qualify the two explicit katakana de components; retain all prior name repairs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original = Path('scripts/propose_editorial_name_fields.py')
source = original.read_text(encoding='utf-8')
start = source.index('    specs=[')
end = source.index('\n    for actor,column,old,new,kind,reason in specs:', start)
source = checked_text(source, {
    "ROOT=Path('work/analysis/Hodram_B91_B110_name_fields_20261101')":
    "ROOT=Path('work/analysis/Hodram_B131_B150_name_fields_20261102')",
    'Hodram_B81_B89_release_verified_20261101': 'Hodram_B111_B130_release_verified_20261102',
    "SOURCE=Path('work/analysis/Hodram_B91_B110_clean_20261101/clean_name_fields.json')":
    "SOURCE=Path('work/analysis/Hodram_B131_B150_two_name_sources_20261102/clean_name_fields.json')",
    source[start:end]:
    """    specs=[(36,8,'デ','de','source-name-component-romanization',
        'Render the explicit clean component デ as de in Geronimo de Espinosa. Retain progressive Geronimo Espinosa; infer no new title, rank or biography.'),
        (42,8,'デ','de','source-name-component-romanization',
        'Render the explicit clean component デ as de in Vasquez de Maldonado. Retain progressive Vasquez Maldonado; infer no new title, rank or biography.')]""",
})
exec(compile(source, __file__ + '::two-exact-source-de-fields', 'exec'), globals())
