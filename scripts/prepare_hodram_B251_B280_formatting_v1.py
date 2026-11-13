"""Prepare logical bodies with the existing native geometry and distinct macro ABIs."""
import inspect
from scripts import prepare_hodram_B231_B250_formatting_v1 as previous
from scripts.bind_hodram_B251_B280_terms_v1 import PROSE,TERMS
from scripts.review_hodram_B251_B280_contextual_v1 import CURRENT,OBJECTS,ROOT
from scripts.review_hodram_B251_B280_names_v1 import NATIVE as NAMES,REVIEW as NAME_REVIEW,ROLES
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'formatting_v1';FORMATTING=OUT/'formatting_input.json';DOCUMENT=FORMATTING
MACROS=OUT/'native_macro_measurements.json';PREFERENCES=OUT/'initial_preferences.json'
FE_KINDS={}
for row in load(PROSE)['records']:
    if row.get('source_selector')!=254:continue
    if row['speaker'] in ['Wall inscription','Sound effect','Figurehead voice']:
        kind={'Wall inscription':'wall-inscription','Sound effect':'sound-effect','Figurehead voice':'in-world-voice'}[row['speaker']]
    elif "'s Luck" in row['english'] or "'s Charm" in row['english']:kind='permanent-attribute-result'
    elif row['english'].startswith('Received '):kind='gold-award'
    else:
        assert 'market share' in row['english'];kind='market-share-result'
    FE_KINDS[row['id']]=kind
assert len(FE_KINDS)==31
source=checked_text(inspect.getsource(previous.main),{
    "len(prose['records'])==225 and prose['counts']=={'retention':110,'revision':115}":"len(prose['records'])==216 and prose['counts']=={'retention':87,'revision':129}",
    "assert len(macro_rows)==4 and sum(r['kind']=='null-actor-FE' for r in macro_rows)==1":"assert len(macro_rows)==8 and sum(r['kind']=='null-actor-FE' for r in macro_rows)==2",
    "    fe_kinds={'DK4_MES_B242_R0036':'item-handover','DK4_MES_B243_R0163':'permanent-attribute-result',\n        'DK4_MES_B250_R0010':'gold-award','DK4_MES_B250_R0034':'market-share-result'}":"    fe_kinds=FE_KINDS",
    "sum(r['kind']=='progressive' for r in rows)==219 and sum(r['kind']=='system-FE' for r in rows)==4":"sum(r['kind']=='progressive' for r in rows)==178 and sum(r['kind']=='system-FE' for r in rows)==31",
    "save(FORMATTING,{**prose,'records':rows,'runtime':runtime,":"save(FORMATTING,{**prose,'file_path':'/data/SC1.DK4','records':rows,'runtime':runtime,",
    "'physical_speech_objects':223,'ordinary_speech_objects':209":"'physical_speech_objects':209,'ordinary_speech_objects':193",
    "'style_physical_speech_objects':14,'style_command_objects':2,'typed_choice_objects':2,'typed_choice_commands':1":"'style_physical_speech_objects':16,'style_command_objects':2,'typed_choice_objects':7,'typed_choice_commands':3",
    'Prepared 223 logical bodies/two captions; four macro speeches pass both original ABIs in all alignments.':'Prepared 209 logical bodies/seven captions; eight macro speeches pass both original ABIs in all alignments.',
})
env={**vars(previous),**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-prose-preserving-native-formatting-input-contract','exec'),env)
if __name__=='__main__':env['main']()
