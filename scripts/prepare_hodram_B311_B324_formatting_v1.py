"""Prepare all387 logical bodies and13 captions with existing native consumer contracts."""
from scripts import prepare_hodram_B251_B280_formatting_v1 as previous
from scripts.review_hodram_B311_B324_contextual_v1 import ROOT, CURRENT, OBJECTS, OUT as PROSE
from scripts.review_hodram_B311_B324_names_v1 import NATIVE as NAMES, REVIEW as NAME_REVIEW, ROLES
from scripts.bind_hodram_B311_B324_terms_v1 import TERMS
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text

OUT = ROOT / 'formatting_v1'
FORMATTING = OUT / 'formatting_input.json'
DOCUMENT = FORMATTING
MACROS = OUT / 'native_macro_measurements.json'
PREFERENCES = OUT / 'initial_preferences.json'
FE_KINDS = {}
for row in load(PROSE)['records']:
    if row.get('source_selector') != 254:
        continue
    text = row['english']
    if text == 'One day passed.':
        kind = 'elapsed-time-result'
    elif text == 'Thud!':
        kind = 'sound-effect'
    elif text in ['...', '......']:
        kind = 'deliberate-wordless-pause'
    elif 'handed over' in text:
        kind = 'item-handover'
    elif text.startswith('You provided '):
        kind = 'outgoing-expedition-funding'
    else:
        kind = 'temporary-condition-result'
    FE_KINDS[row['id']] = kind
assert len(FE_KINDS) == 14
source = checked_text(previous.source, {
    "len(prose['records'])==216 and prose['counts']=={'retention':87,'revision':129}":
        "len(prose['records'])==400 and prose['counts']=={'retention':225,'revision':175}",
    "len(macro_rows)==8 and sum(r['kind']=='null-actor-FE' for r in macro_rows)==2":
        "len(macro_rows)==3 and sum(r['kind']=='null-actor-FE' for r in macro_rows)==1",
    "sum(r['kind']=='progressive' for r in rows)==178 and sum(r['kind']=='system-FE' for r in rows)==31":
        "sum(r['kind']=='progressive' for r in rows)==373 and sum(r['kind']=='system-FE' for r in rows)==14",
    "'physical_speech_objects':209,'ordinary_speech_objects':193":
        "'physical_speech_objects':387,'ordinary_speech_objects':151",
    "'style_physical_speech_objects':16,'style_command_objects':2,'typed_choice_objects':7,'typed_choice_commands':3":
        "'style_physical_speech_objects':236,'style_command_objects':38,'typed_choice_objects':13,'typed_choice_commands':6",
    'Prepared 209 logical bodies/seven captions; eight macro speeches pass both original ABIs in all alignments.':
        'Prepared387 logical bodies/13 captions; three macro speeches pass all four native alignments, including one null-actor FE notice.',
})
env = {**previous.env, **globals(), '__file__': __file__}
exec(compile(source, __file__ + '::same-native-formatting-and-distinct-macro-contracts-new-scope', 'exec'), env)
if __name__ == '__main__':
    env['main']()
