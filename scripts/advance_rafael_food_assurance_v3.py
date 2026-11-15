"""Run source-locked incremental stages for one further full-exchange prose finding."""
import argparse
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.source_locked_derivation_v5118 import checked_text

FRESH=Path('work/analysis/Rafael_food_assurance_v3_20261105')
COMPOSITE=Path('work/analysis/Rafael330_food_composite_v3_20261105')
MANUSCRIPT=Path('translations/rafael_B81_B84_contextual_editorial_manuscript_v3.json')
ID='DK4_MES_B81_R0216'

def compose():
    assert not COMPOSITE.exists()
    previous=Path('work/analysis/Rafael330_Emilio_composite_v2_20261105')
    plan,native,fp,fn=map(load,[previous/'plans323.json',previous/'native323.json',
        FRESH/'automatic/automatic_plans.json',FRESH/'native/compiled_native_pages.json'])
    assert fn['runtime']==native['runtime'] and fn['font_sha256']==native['font_sha256']
    assert fn['records'][0]['id']==fp['records'][0]['id']==ID
    assert fn['pages']==1 and not fp['failures']
    assert fn['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert fn['complete_consumption_andpagination_exact']
    COMPOSITE.mkdir()
    approval=FRESH/'direct_visual_approval.json'
    save(approval,dict(fresh_Rafael_native_page_directly_viewed=True,all_one_native_pages_viewed=True,
        complete_nine_speech_Emilio_v2_actual_sheet_directly_viewed=True,
        prior_actual_sheet='work/analysis/Rafael_Emilio_food_actual_sheets_v2_20261105/actual_dialogue_1.png',
        fresh_native=str(FRESH/'native/compiled_native_pages.json'),
        fresh_native_sha256=sha((FRESH/'native/compiled_native_pages.json').read_bytes()),new_credit=0))
    oldnative=deepcopy(native)
    for doc,entry in [(plan,fp['records'][0]),(native,fn['records'][0])]:
        doc['records']=[deepcopy(entry) if r['id']==ID else r for r in doc['records']]
        assert len(doc['records'])==323
        doc.update(manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
            one_fresh_source_prose_record=ID,unchanged322_record_proofs_reused=True,new_credit=0)
    save(COMPOSITE/'plans323.json',plan)
    native.update(plan=str(COMPOSITE/'plans323.json'),plan_sha256=sha((COMPOSITE/'plans323.json').read_bytes()),
        direct_visual_review_pending=False,all323_subset_body_layouts_approved=True,
        current_layout_only_refinements=18,current_separate_food_prose_refinements=2)
    for ident,path in [(ID,FRESH/'native/compiled_native_pages.json'),
            ('DK4_MES_B81_R0220',Path('work/analysis/Rafael_Emilio_food_acceptance_20261105/native_v2/compiled_native_pages.json'))]:
        native['origins'][ident]=dict(native_proof=str(path),native_proof_sha256=sha(path.read_bytes()),
            compiled_bytes_logical_prose_complete_source_preamble_andnative_pages_exact=True,
            direct_visual_review_reused_for_exact_native_page=True)
    native['evidence']={str(p):sha(p.read_bytes()) for p in [previous/'native323.json',previous/'plans323.json',
        FRESH/'native/compiled_native_pages.json',FRESH/'automatic/automatic_plans.json',approval,MANUSCRIPT,Path(__file__)]}
    assert all(a==b for a,b in zip(oldnative['records'],native['records'],strict=True) if a['id']!=ID)
    save(COMPOSITE/'native323.json',native)
    print('One fresh Rafael assurance plus322 exact body proofs;all332 subset pages reviewed.')

def derive_stage(stage):
    extra={}
    if stage=='rebuild':
        from scripts import rebuild_rafael_B81_B84_with_FE_pages_v2 as old
        source=old.source
        changes={'Rafael_B81_B84_rebuilt_v2_20261105':'Rafael_B81_B84_rebuilt_v3_20261105',
            'rafael_B81_B84_contextual_editorial_manuscript_v2.json':'rafael_B81_B84_contextual_editorial_manuscript_v3.json',
            'Rafael330_Emilio_composite_v2_20261105':'Rafael330_food_composite_v3_20261105',
            'rom_retention_pins.Rafael330_research_v2.pending.json':'rom_retention_pins.Rafael330_research_v3.pending.json'}
    elif stage=='inputs':
        from scripts import prepare_rafael330_stored_consumer_inputs_v2 as old
        source=old.source
        changes={'Rafael_B81_B84_rebuilt_v2_20261105':'Rafael_B81_B84_rebuilt_v3_20261105',
            'Rafael330_stored_consumer_inputs_v2_20261105':'Rafael330_stored_consumer_inputs_v3_20261105',
            'Rafael330_Emilio_composite_v2_20261105':'Rafael330_food_composite_v3_20261105'}
    elif stage=='incremental':
        from scripts import prepare_rafael330_incremental_stored_v2 as old
        source=Path(old.__file__).read_text(encoding='utf-8')
        changes={'Rafael330_incremental_stored_v2_20261105':'Rafael330_incremental_stored_v3_20261105',
            "NEW=Path('work/analysis/Rafael330_stored_consumer_inputs_v2_20261105')":
                "NEW=Path('work/analysis/Rafael330_stored_consumer_inputs_v3_20261105')",
            "OLD=Path('work/analysis/Rafael330_stored_consumer_inputs_20261105')":
                "OLD=Path('work/analysis/Rafael330_stored_consumer_inputs_v2_20261105')",
            'Rafael330_stored_native_20261105':'Rafael330_stored_native_v2_20261105',
            'DK4_MES_B81_R0220':ID}
    elif stage=='stored':
        from scripts import check_rafael330_stored_v1 as old
        return old.main()
    elif stage=='complete':
        from scripts import complete_rafael330_incremental_stored_v2 as old
        source=Path(old.__file__).read_text(encoding='utf-8')
        changes={name+'_v2_20261105':name+'_v3_20261105' for name in [
            'Rafael330_stored_native','Rafael330_stored_consumer_inputs','Rafael330_incremental_stored','Rafael330_fresh_Emilio_stored']}
    elif stage=='catalogue':
        from scripts import check_rafael330_stored_catalogue_v2 as old
        source=old.source
        changes={'Rafael330_stored_catalogue_v2_20261105':'Rafael330_stored_catalogue_v3_20261105',
            'Rafael330_stored_native_v2_20261105':'Rafael330_stored_native_v3_20261105'}
    elif stage=='loaders':
        from scripts import check_rafael330_loaders_v2 as old
        source=old.source;extra['parent_adapter']=old.parent_adapter
        changes={'Rafael330_stored_consumer_inputs_v2_20261105':'Rafael330_stored_consumer_inputs_v3_20261105',
            'Rafael330_loaders_20261105/verification.json':'Rafael330_loaders_v2_20261105/verification.json'}
    elif stage=='fixture':
        from scripts import prepare_rafael_Emilio_food_actual_v2 as old
        source=old.source;extra['FOOD_IDS']=old.FOOD_IDS
        changes={'Rafael_Emilio_food_actual_v2_20261105':'Rafael_food_actual_v3_20261105',
            'Rafael330_stored_consumer_inputs_v2_20261105':'Rafael330_stored_consumer_inputs_v3_20261105',
            'Rafael330_stored_native_v2_20261105':'Rafael330_stored_native_v3_20261105',
            'rom_retention_pins.Rafael_Emilio_food_v2.pending.json':'rom_retention_pins.Rafael_food_v3.pending.json'}
    else:raise ValueError(stage)
    derived=checked_text(source,changes)
    receipt=FRESH/(stage+'_derivation.json');assert not receipt.exists()
    save(receipt,dict(stage=stage,source_file=old.__file__,source_file_sha256=sha(Path(old.__file__).read_bytes()),
        original_effective_source_sha256=sha(source.encode()),changes=changes,derived_source=derived,
        native_numbers_andmultiplicity_preserved=True,new_credit=0))
    exec(compile(derived,__file__+'::'+stage+'-same-guards-single-paragraph-successor','exec'),
        {'__name__':'__main__','__file__':__file__,**extra})

if __name__=='__main__':
    import sys
    stage=sys.argv.pop(1)
    if stage=='compose':compose()
    else:derive_stage(stage)
