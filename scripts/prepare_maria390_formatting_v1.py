"""Prepare373 fresh bodies with exact compatible default macro proof reuse."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/prepare_maria337_formatting_v1.py').read_text(encoding='utf-8'),{
    'scripts.meaning_maria337_clean_v1':'scripts.finalize_maria390_prose_v1',
    'translations/maria_B125_B136_contextual_review_v1.json':'translations/maria_B152_B175_contextual_review_v1.json',
    'work/Maria_B96_B124_clean_20261109/formatting_v1/native_macro_measurements.json':'work/Maria_B137_B151_clean_20261109/formatting_v1/native_macro_measurements.json',
    "len(rows)==337 and sum(r['kind']=='progressive' for r in rows)==329":"len(rows)==390 and sum(r['kind']=='progressive' for r in rows)==341",
    "sum(r['kind']=='system-FE' for r in rows)==6 and sum(r['kind']=='typed-choice-label' for r in rows)==2 and tokens==13":
        "sum(r['kind']=='system-FE' for r in rows)==32 and sum(r['kind']=='typed-choice-label' for r in rows)==17 and tokens==5",
    'all335_speech_selectors_exact_fixed_orFE':'all373_speech_selectors_exact_fixed_orFE',
    "'physical_speech_objects':335,'ordinary_speech_objects':335":"'physical_speech_objects':373,'ordinary_speech_objects':373",
    "'typed_choice_objects':2,'typed_choice_commands':1":"'typed_choice_objects':17,'typed_choice_commands':8",
    'Prepared335 bodies/two captions/13 explicit macros':'Prepared373 bodies/17 captions/five explicit macros',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-current-runtime-source-controls-full-width-andmacro-dependency-contract','exec'),globals())
