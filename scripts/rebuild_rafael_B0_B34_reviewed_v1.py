"""Use the qualified compound-capable rebuilder for a speech-only residual batch."""
from pathlib import Path
import sys
from scripts import rebuild_rafael_B301_B320_reviewed_v1 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_rafael_B0_B34_v1 import CURRENT, FORMATTING as MANUSCRIPT, ROOT
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_rafael_B0_B34_visual_v1 import APPROVAL as VISUAL, FINAL as FINAL_NATIVE, PLAN

REGISTRY,TEMPLATE=previous.REGISTRY,previous.TEMPLATE
INPUTS=ROOT/'stored_rebuild_inputs_v1'
MENU=INPUTS/'menu.json'
COMPOUNDS=INPUTS/'styles.json'


def prepare():
    assert not INPUTS.exists()
    doc,native,view=map(load,(MANUSCRIPT,FINAL_NATIVE,VISUAL))
    assert view['all_final_body_caption_and_name_sheets_directly_viewed']
    assert view['native_sha256']==digest(FINAL_NATIVE) and view['plan_sha256']==digest(PLAN)
    assert len(doc['records'])==len(native['records'])==283 and view['body_pages']==284
    assert not any(r['kind']!='progressive' or r.get('native_object_kind') for r in doc['records'])
    assert all(digest(s['path'])==s['sha256'] for s in view['sheets'])
    common=dict(manuscript=str(MANUSCRIPT),manuscript_sha256=digest(MANUSCRIPT),plan=str(PLAN),
        plan_sha256=digest(PLAN),runtime=doc['runtime'],new_credit=0)
    INPUTS.mkdir()
    save(MENU,{**common,'menus':[],'offline_visual_approved':True,'direct_view_pending':False})
    save(COMPOUNDS,{**common,'objects':[],'physical_alternatives':0,'native_target_slot_cases':0,
        'compiler_negatives':[],'source_proven_absence_of_style_objects':True})


source=checked_text(previous.source,{
    '(444,11,0)':'(284,0,0)',
    "len(doc['records'])==453":"len(doc['records'])==283",
    "==len(native['records'])==442":"==len(native['records'])==283",
    '==(297,145,11)':'==(283,0,0)',
    'len(changed)==20':'len(changed)==35',
    'unchanged_control_only_blocks=[],speech_count=297':'unchanged_control_only_blocks=[],speech_count=283',
    'style_physical_speech_count=145,total_rendered_speech_count=442,typed_choice_count=11,compound_objects=24':
        'style_physical_speech_count=0,total_rendered_speech_count=283,typed_choice_count=0,compound_objects=0',
    'Rafael B301–B320 complete source-bound reconstruction':'Rafael B0–B34 complete source-bound reconstruction',
    'ordinary_speeches=297,style_alternatives=145,menu_labels=11,changed_blocks=20':
        'ordinary_speeches=283,style_alternatives=0,menu_labels=0,changed_blocks=35',
})


if __name__=='__main__':
    if sys.argv[1:]==['--prepare']:prepare()
    else:exec(compile(source,__file__+'::same-source-bound-speech-reconstruction','exec'),globals())
