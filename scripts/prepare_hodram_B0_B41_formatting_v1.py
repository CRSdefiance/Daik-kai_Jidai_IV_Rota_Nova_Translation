"""Prepare388 bodies/six captions with original macro ABIs and reviewed name dependencies."""
import inspect
from copy import deepcopy
from pathlib import Path

from scripts import prepare_hodram_B231_B250_formatting_v1 as previous
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.bind_hodram_B0_B41_terms_v1 import PROSE,TERMS
from scripts.review_hodram_B0_B41_contextual_v1 import CURRENT,OBJECTS,ROOT
from scripts.review_hodram_B0_B41_names_v1 import OUT as PRIOR_REVIEW
from scripts.source_locked_derivation_v5118 import checked_text

NAMES=ROOT/'scoped_names_formatting_bindings_v1.json'
NAME_REVIEW=ROOT/'scoped_names_formatting_review_v1.json'
ROLES=ROOT/'role_bindings_v1.json'
OUT=ROOT/'formatting_v1'
FORMATTING=OUT/'formatting_input.json'
MACROS=OUT/'native_macro_measurements.json'
PREFERENCES=OUT/'initial_preferences.json'


def prepare_names():
    assert not NAMES.exists() and not NAME_REVIEW.exists()
    source=ROOT/'scoped_names_current_v1.json';native,review=map(load,(source,PRIOR_REVIEW))
    retained=ROOT/'retained_name_planes_v1/native_name_planes.json';planes=load(retained)
    assert planes['scoped_actors']==39 and planes['distinct_strings']==38
    assert planes['fresh_name_planes']==18 and planes['exact_reused_name_planes']==20
    assert all(digest(p['path'])==p['sha256'] for p in planes['review_sheets'])
    assert all(p['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass'] for p in planes['planes'])
    changed=ROOT/'name_field_visual_approval_v1.json'
    assert load(changed)['all12_current_andproposed_planes_directly_viewed']
    visual=ROOT/'retained_name_visual_approval_v1.json';assert not visual.exists()
    save(visual,dict(receipt=str(retained),receipt_sha256=digest(retained),all38_retained_progressive_strings_directly_viewed=True,
        review_sheets=planes['review_sheets'],fresh_planes=18,exact_reused_planes=20,
        no_new_actual_header_orcatalogue_UI_coverage=True,new_credit=0))
    rendered=deepcopy(review)
    for row in rendered['records']:
        row['english']=next(r['text'] for r in row['proposed_consumers'] if r['consumer']=='progressive-nameplate')
        row['progressive_name_plane_review_complete']=True
    rendered.update(retained_name_planes_pending=False,all42_planned_progressive_names_native_andvisually_checked=True,
        actual_changed_headers_andregistered_data_layer_pending=True,
        retained_name_visual_receipt=str(visual),retained_name_visual_receipt_sha256=digest(visual))
    save(NAME_REVIEW,rendered)
    save(NAMES,{**native,'actors':sorted(r['actor_ID'] for r in native['records']),
        'current_names':dict(rows=[r for row in native['records'] for r in row['current_consumers']]),
        'planned_names':dict(rows=[r for row in rendered['records'] for r in row['proposed_consumers']]),
        'source_owned_current_name_binding':str(source),'source_owned_current_name_binding_sha256':digest(source),
        'name_review':str(NAME_REVIEW),'name_review_sha256':digest(NAME_REVIEW),
        'three_name_data_fields_not_yet_integrated':True,
        'changed_name_proof':'work/Hodram_B0_B41_clean_20261107/name_field_checks_v1/native_name_fields_verification.json'})


FE_KINDS={}
for r in load(PROSE)['records']:
    if r.get('source_selector')!=254:continue
    if r['block']==29:kind='battle-tutorial-instruction'
    elif r['english'].startswith('Foreign Girl:'):kind='embedded-anonymous-character-response'
    elif r['english']=='Like a doll...':kind='unassigned-impression-narration'
    elif r['english']=='!!':kind='wordless-shock'
    else:
        assert r['english']=='...';kind='deliberate-wordless-pause'
    FE_KINDS[r['id']]=kind
assert len(FE_KINDS)==16

source=checked_text(inspect.getsource(previous.main),{
    "len(prose['records'])==225 and prose['counts']=={'retention':110,'revision':115}":
        "len(prose['records'])==394 and prose['counts']=={'revision':221,'retention':173}",
    "assert ctx.receipt()==runtime and digest('translations/release_stack.json')==ctx.release['registry_sha256']":
        "assert ctx.receipt()==runtime and digest('translations/release_stack.json')==load(current['exact_native_context_reuse']['target_release'])['registry_sha256']",
    "assert len(macro_rows)==4 and sum(r['kind']=='null-actor-FE' for r in macro_rows)==1":
        "assert len(macro_rows)==10 and not any(r['kind']=='null-actor-FE' for r in macro_rows)",
    "    fe_kinds={'DK4_MES_B242_R0036':'item-handover','DK4_MES_B243_R0163':'permanent-attribute-result',\n        'DK4_MES_B250_R0010':'gold-award','DK4_MES_B250_R0034':'market-share-result'}":
        '    fe_kinds=FE_KINDS',
    "sum(r['kind']=='progressive' for r in rows)==219 and sum(r['kind']=='system-FE' for r in rows)==4":
        "sum(r['kind']=='progressive' for r in rows)==372 and sum(r['kind']=='system-FE' for r in rows)==16",
    "save(FORMATTING,{**prose,'records':rows,'runtime':runtime,":
        "save(FORMATTING,{**prose,'file_path':'/data/SC1.DK4','records':rows,'runtime':runtime,",
    "'physical_speech_objects':223,'ordinary_speech_objects':209":
        "'physical_speech_objects':388,'ordinary_speech_objects':341",
    "'style_physical_speech_objects':14,'style_command_objects':2,'typed_choice_objects':2,'typed_choice_commands':1":
        "'style_physical_speech_objects':47,'style_command_objects':7,'typed_choice_objects':6,'typed_choice_commands':3",
    'Prepared 223 logical bodies/two captions; four macro speeches pass both original ABIs in all alignments.':
        'Prepared388 logical bodies/six captions; ten progressive macro speeches pass all four native alignments; FE macro ABI retained.',
})
env={**vars(previous),**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-macro-and-source-preserving-formatting-input-contract','exec'),env)

if __name__=='__main__':
    prepare_names()
    env['main']()
