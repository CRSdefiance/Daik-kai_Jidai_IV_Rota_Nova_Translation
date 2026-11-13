"""Use the qualified native paragraph planner for 67 complete Rafael speeches."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.qualify_rafael_B161_B165_terms_and_names_v1 import A, CURRENT, OUT as IDENTITY

PROSE=Path('translations/rafael_B161_B165_contextual_review_v1.json')
TEMPLATE=Path('scripts/plan_rafael_B177_B180_v1.py')
source=checked_text(TEMPLATE.read_text(encoding='utf-8'),{
    'from scripts.write_rafael_B177_B180_contextual_v1 import A, CAPTIONS, CURRENT, IDENTITY, OUT as PROSE':'',
    'rafael_B177_B180_formatting_manuscript_v1.json':'rafael_B161_B165_formatting_manuscript_v1.json',
    'rafael_B177_B180_visual_preferences_v1.json':'rafael_B161_B165_visual_preferences_v1.json',
    "set(tokens) <= {'FI'}":"set(tokens) <= {'FI','FA','FO'}",
    "'extra armor unlock notice'":"'ball impact sound effect'",
    "assert count == 4":"assert count == 7",
    "physical_speech_objects=175, ordinary_speech_objects=175":"physical_speech_objects=67, ordinary_speech_objects=67",
    'typed_choice_objects=8, typed_choice_commands=4, marked_FI_substitutions=count':'typed_choice_objects=0, typed_choice_commands=0, marked_substitutions=count',
    "    current, objects, identity = map(load, [CURRENT, CAPTIONS, IDENTITY])":"    current, identity = map(load, [CURRENT, IDENTITY])",
    "doc['blocks'] == [177, 178, 179, 180]":"doc['blocks'] == [161,162,163,164,165]",
    "identity['runtime'] == objects['runtime']":"identity['runtime']",
    "    assert current['all_source_preambles_andcommand_kinds_preserved']":
        """    assert current['all_source_preambles_andcommand_kinds_preserved']
    assert not any(c['word'] in (0x2100,0x2200,0x4100) for g in current['groups'] for c in g['all_source_commands'])""",
    'len(bindings) == 175':'len(bindings) == 67',
    'same-validated-native-geometry-with-175-new-source-bindings':'same-validated-native-geometry-with-67-new-source-bindings',
    """    ('fernando', 'dias'), ('manuel', 'almeida'), ('cargo', 'holds'), ('supply', 'holds'),
    ('jigger', 'spanker'), ('square', 'sail'), ('lateen', 'sail'), ('two', 'masts'),
    ('three', 'masts'), ('first', "mate's"), ("mate's", 'office'), ('lumber', 'room'),
    ('rear', 'quarter'), ('trade', 'route'), ('naval', 'battle'), ('one', 'percent'),""":
        """    ('patterned','cloth'),('brass','lamp'),('mediterranean','proof'),('proofs','of'),('of','conquest'),
    ('your','majesty'),('his','majesty'),('portuguese','crown'),('spanish','fleet'),
    ('admiral','hayreddin'),("pasha's",'forces'),("didn't",'i'),('would','i'),("isn't",'it'),""",
})
exec(compile(source,__file__+'::same-source-bound-native-wrapping','exec'),globals())
