"""Bind every paragraph to its native identity, geometry and distinct macro ABI."""
from scripts import prepare_hodram_B251_B280_formatting_v1 as previous
from scripts.review_hodram_B301_B310_contextual_v1 import ROOT,CURRENT,OBJECTS,OUT as PROSE
from scripts.review_hodram_B301_B310_names_v1 import NATIVE as NAMES,REVIEW as NAME_REVIEW,ROLES
from scripts.bind_hodram_B301_B310_terms_v2 import TERMS
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'formatting_v1';FORMATTING=OUT/'formatting_input.json';DOCUMENT=FORMATTING
MACROS=OUT/'native_macro_measurements.json';PREFERENCES=OUT/'initial_preferences.json'
FE_KINDS={r['id']:('elapsed-time-result' if r['english']=='One day passed.' else 'temporary-condition-result')
    for r in load(PROSE)['records'] if r.get('source_selector')==254}
assert len(FE_KINDS)==8
source=checked_text(previous.source,{
    "len(prose['records'])==216 and prose['counts']=={'retention':87,'revision':129}":
        "len(prose['records'])==234 and prose['counts']=={'retention':107,'revision':127}",
    "len(macro_rows)==8 and sum(r['kind']=='null-actor-FE' for r in macro_rows)==2":
        "len(macro_rows)==5 and sum(r['kind']=='null-actor-FE' for r in macro_rows)==1",
    "sum(r['kind']=='progressive' for r in rows)==178 and sum(r['kind']=='system-FE' for r in rows)==31":
        "sum(r['kind']=='progressive' for r in rows)==217 and sum(r['kind']=='system-FE' for r in rows)==8",
    "'physical_speech_objects':209,'ordinary_speech_objects':193":"'physical_speech_objects':225,'ordinary_speech_objects':73",
    "'style_physical_speech_objects':16,'style_command_objects':2,'typed_choice_objects':7,'typed_choice_commands':3":
        "'style_physical_speech_objects':152,'style_command_objects':23,'typed_choice_objects':9,'typed_choice_commands':4",
    'Prepared 209 logical bodies/seven captions; eight macro speeches pass both original ABIs in all alignments.':
        'Prepared225 logical bodies/nine captions; five macro speeches pass all four native alignments, including one null-actor FE notice.',
})
env={**previous.env,**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-formatting-inputs-and-distinct-native-macro-contracts','exec'),env)
if __name__=='__main__':env['main']()
