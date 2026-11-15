"""Prepare333 fresh bodies with exact compatible default macro proof reuse."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/prepare_maria337_formatting_v1.py').read_text(encoding='utf-8'),{
    'scripts.meaning_maria337_clean_v1':'scripts.meaning_maria335_B137_B151_v1',
    'translations/maria_B125_B136_contextual_review_v1.json':'translations/maria_B137_B151_contextual_review_v1.json',
    'work/Maria_B96_B124_clean_20261109/formatting_v1/native_macro_measurements.json':'work/Maria_B125_B136_clean_20261109/formatting_v1/native_macro_measurements.json',
    "len(rows)==337 and sum(r['kind']=='progressive' for r in rows)==329":"len(rows)==335 and sum(r['kind']=='progressive' for r in rows)==315",
    "sum(r['kind']=='system-FE' for r in rows)==6":"sum(r['kind']=='system-FE' for r in rows)==18",
    'and tokens==13':'and tokens==21',
    'all335_speech_selectors_exact_fixed_orFE':'all333_speech_selectors_exact_fixed_orFE',
    "'physical_speech_objects':335,'ordinary_speech_objects':335":"'physical_speech_objects':333,'ordinary_speech_objects':333",
    'Prepared335 bodies/two captions/13 explicit macros':'Prepared333 bodies/two captions/21 explicit macros',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-current-runtime-full-width-source-control-andmacro-dependency-contract','exec'),globals())
