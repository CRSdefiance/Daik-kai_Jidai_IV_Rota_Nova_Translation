"""Seal the extra directly viewed tutorial wrap and reuse exact other object proofs."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Hodram_B0_B41_clean_20261107')
OUT=ROOT/'storage_inputs_v3'

def main():
    assert not OUT.exists()
    old=ROOT/'storage_inputs_v2';source=ROOT/'formatting_v1/formatting_input_v3.json'
    planpath=ROOT/'automatic_plans_v5/automatic_plans.json';nativepath=ROOT/'native_joined_v3/compiled_native_pages.json'
    doc,plan,native=map(load,(old/'storage_manuscript.json',planpath,nativepath))
    assert plan['manuscript_sha256']==native['manuscript_sha256']==digest(source) and native['plan_sha256']==digest(planpath)
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and native['complete_consumption_andpagination_exact']
    oldvisual=ROOT/'offline_visual_approval_v1.json';visual=deepcopy(load(oldvisual))
    ident='DK4_MES_B29_R0059';row=next(x for x in native['records'] if x['id']==ident);page=row['complete_native_English_display']['pages'][0]
    assert digest(page['preview'])==page['preview_sha256']
    original=next(x for x in visual['findings'] if x['id']==ident)
    original.update(disposition='revised-layout',reason='Gameplay contact sheet7 shows All/hands split. The new two-row native page keeps All hands together; no prose change.',
        compiled_hex=row['compiled_hex'],pages=[page],fresh_native_page_directly_viewed=True)
    visual.update(previous_visual_approval=str(oldvisual),previous_visual_approval_sha256=digest(oldvisual),
        native=str(nativepath),native_sha256=digest(nativepath),plan=str(planpath),plan_sha256=digest(planpath),
        visual_wrap_corrections=5,additional_gameplay_wrap=ident,additional_final_native_page_directly_viewed=True,
        all_other388_final_pages_exact_reused=True,actual_new_wrap_gameplay_pending=True)
    view=ROOT/'offline_visual_approval_v2.json';assert not view.exists();save(view,visual)
    doc.update(final_visual_approval=str(view),final_visual_approval_sha256=digest(view))
    OUT.mkdir();document=OUT/'storage_manuscript.json';save(document,doc)
    plan.update(manuscript=str(document),manuscript_sha256=digest(document));newplan=OUT/'compiled_plans.json';save(newplan,plan)
    native.update(manuscript=str(document),manuscript_sha256=digest(document),plan=str(newplan),plan_sha256=digest(newplan),
        original_native_receipt=str(nativepath),original_native_receipt_sha256=digest(nativepath),
        direct_visual_review_pending=False,final_visual_approval=str(view),final_visual_approval_sha256=digest(view))
    save(OUT/'native_pages.json',native)
    planned={x['id']:x for x in plan['records']};styles=load(old/'styles.json')
    for obj in styles['objects']:
        for slot in obj['native_slots']:assert slot['target_hex']==bytes.fromhex(planned[slot['record_id']]['encoded_hex'])[1:].hex()
    for value,name in [(styles,'styles.json'),(load(old/'menus.json'),'menus.json')]:
        value.update(manuscript=str(document),manuscript_sha256=digest(document),
            exact_unchanged_object_inputs_andnative_proofs_reused=True,previous_metadata_bridge=str(old/name),previous_metadata_bridge_sha256=digest(old/name))
        if 'plan' in value:value.update(plan=str(newplan),plan_sha256=digest(newplan))
        save(OUT/name,value)
    save(OUT/'packet.json',load(old/'packet.json'))
    print('Additional All hands wrap approved offline;387 body records andall styles/menus reused exactly. Prose unchanged.')

if __name__=='__main__':main()
