"""Reuse exact compatible macro proofs; freshly prepare all Maria330 paragraph layouts."""
from scripts import prepare_maria328_formatting_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    'from scripts.meaning_maria328_clean_v1 import ROOT':'from scripts.meaning_maria330_clean_v1 import ROOT',
    'translations/maria_B73_B95_contextual_review_v1.json':'translations/maria_B96_B124_contextual_review_v2.json',
    'work/Maria_B58_B70_clean_20261109/formatting_v3/native_macro_measurements.json':'work/Maria_B73_B95_clean_20261109/formatting_v1/native_macro_measurements.json',
    "adapter = checked_text(prior['source_owned_progressive_adapter'], {\n        'assert identity==prefix and captain==3': 'assert captain==3 and identity==(prefix if prefix<207 else DYNAMIC_BINDINGS[prefix])',\n    })":
        "adapter = prior['source_owned_progressive_adapter']\n    assert 'assert captain==3 and identity==(prefix if prefix<207 else DYNAMIC_BINDINGS[prefix])' in adapter",
    'assert len(rows) == 328 and sum(r[\'kind\']==\'progressive\' for r in rows) == 286':
        'assert len(rows) == 330 and sum(r[\'kind\']==\'progressive\' for r in rows) == 320',
    "sum(r['kind']=='system-FE' for r in rows) == 27 and sum(r['kind']=='typed-choice-label' for r in rows) == 15 and tokens == 2":
        "sum(r['kind']=='system-FE' for r in rows) == 8 and sum(r['kind']=='typed-choice-label' for r in rows) == 2 and tokens == 23",
    "'physical_speech_objects':313,'ordinary_speech_objects':289,'style_physical_speech_objects':24,'style_command_objects':4":
        "'physical_speech_objects':328,'ordinary_speech_objects':293,'style_physical_speech_objects':35,'style_command_objects':6",
    "'typed_choice_objects':15,'typed_choice_commands':5":"'typed_choice_objects':2,'typed_choice_commands':1",
    'Prepared313 bodies/15 captions/two FI tokens':'Prepared328 bodies/two captions/23 FI-FA-FO tokens',
})
if __name__=='__main__':exec(compile(source,__file__+'::exact-macro-dependency-reuse-fresh330-paragraph-inputs','exec'),globals())
