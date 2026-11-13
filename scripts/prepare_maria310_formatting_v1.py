"""Use the qualified full-width Maria formatter inputs with310 reviewed bodies."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/prepare_maria286_formatting_v1.py').read_text(encoding='utf-8'),{
    'work/Maria_B37_B50_clean_20261109':'work/Maria_B51_B57_clean_20261109',
    'translations/maria_B37_B50_contextual_review_v1.json':'translations/maria_B51_B57_contextual_review_v1.json',
    'len(rows)==286':'len(rows)==310',
    "row['kind']=='typed-choice-label'":"row['kind']=='typed-choice-label'",
    "sum(r['kind']=='progressive' for r in rows)==269":"sum(r['kind']=='progressive' for r in rows)==279",
    "sum(r['kind']=='system-FE' for r in rows)==13":"sum(r['kind']=='system-FE' for r in rows)==31",
    "sum(r['kind']=='typed-choice-label' for r in rows)==4 and tokens==21":"sum(r['kind']=='typed-choice-label' for r in rows)==0 and tokens==9",
    "'physical_speech_objects':282,'ordinary_speech_objects':282":"'physical_speech_objects':310,'ordinary_speech_objects':310",
    "'typed_choice_objects':4,'typed_choice_commands':2":"'typed_choice_objects':0,'typed_choice_commands':0",
    'Prepared282 bodies/four captions;21 substitutions;':'Prepared310 bodies/no captions;nine substitutions;',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-native-source-owned-progressive-andFE-macro-ABI-full-width-inputs','exec'),globals())
