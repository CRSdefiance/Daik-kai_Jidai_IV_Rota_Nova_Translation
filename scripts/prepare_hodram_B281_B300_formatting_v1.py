"""Prepare fresh paragraph formatting with exact current identities and macro contracts."""
from scripts import prepare_hodram_B251_B280_formatting_v1 as previous
from scripts.review_hodram_B281_B300_contextual_v1 import ROOT,CURRENT,OBJECTS,OUT as PROSE
from scripts.review_hodram_B281_B300_names_v1 import NATIVE as NAMES,REVIEW as NAME_REVIEW,ROLES
from scripts.bind_hodram_B281_B300_terms_v1 import TERMS
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'formatting_v1';FORMATTING=OUT/'formatting_input.json';DOCUMENT=FORMATTING
MACROS=OUT/'native_macro_measurements.json';PREFERENCES=OUT/'initial_preferences.json'
FE_KINDS={}
for row in load(PROSE)['records']:
    if row.get('source_selector')!=254:continue
    if row['english'].startswith('Received '):kind='gold-award'
    elif 'market share' in row['english']:kind='market-share-result'
    elif row['id'] in {'DK4_MES_B291_R0077','DK4_MES_B291_R0119'}:kind='sound-effect'
    elif row['id']=='DK4_MES_B290_R0233':kind='elapsed-time-result'
    else:kind='temporary-condition-result'
    FE_KINDS[row['id']]=kind
assert len(FE_KINDS)==16
source=checked_text(previous.source,{
    "len(prose['records'])==216 and prose['counts']=={'retention':87,'revision':129}":
        "len(prose['records'])==384 and prose['counts']=={'retention':203,'revision':181}",
    "len(macro_rows)==8 and sum(r['kind']=='null-actor-FE' for r in macro_rows)==2":
        "len(macro_rows)==13 and sum(r['kind']=='null-actor-FE' for r in macro_rows)==0",
    "sum(r['kind']=='progressive' for r in rows)==178 and sum(r['kind']=='system-FE' for r in rows)==31":
        "sum(r['kind']=='progressive' for r in rows)==357 and sum(r['kind']=='system-FE' for r in rows)==16",
    "'physical_speech_objects':209,'ordinary_speech_objects':193":"'physical_speech_objects':373,'ordinary_speech_objects':242",
    "'style_physical_speech_objects':16,'style_command_objects':2,'typed_choice_objects':7,'typed_choice_commands':3":
        "'style_physical_speech_objects':131,'style_command_objects':18,'typed_choice_objects':11,'typed_choice_commands':5",
    'Prepared 209 logical bodies/seven captions; eight macro speeches pass both original ABIs in all alignments.':
        'Prepared 373 logical bodies/11 captions; 13 progressive macro speeches pass all four native alignments. No FE body has a substitution.',
})
env={**previous.env,**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-prose-preserving-native-formatting-inputs-new-scope','exec'),env)
if __name__=='__main__':env['main']()
