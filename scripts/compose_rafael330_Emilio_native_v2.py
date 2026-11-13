"""Replace exactly one fresh plan/plane; retain the other322 qualified body objects."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael330_Emilio_composite_v2_20261105')
BASE=Path('work/analysis/Rafael_B81_B84_formatting_20261105')
FRESH=Path('work/analysis/Rafael_Emilio_food_acceptance_20261105')
ID='DK4_MES_B81_R0220'

def main():
    assert not ROOT.exists()
    oldplan=BASE/'automatic_subset_v5/automatic_plans.json';oldnative=BASE/'combined_native_v5.json'
    newplan=FRESH/'automatic_v2/automatic_plans.json';newnative=FRESH/'native_v2/compiled_native_pages.json'
    approval=Path('work/analysis/Rafael330_actual_progress_20261105/actual_visual_andscope_approval_v1.json')
    assert load(approval)['fresh_Emilio_native_page_directly_viewed']
    plan,native,fplan,fnative=map(load,[oldplan,oldnative,newplan,newnative])
    assert len(fplan['records'])==len(fnative['records'])==1
    assert fplan['records'][0]['id']==fnative['records'][0]['id']==ID
    assert native['runtime']==fnative['runtime'] and native['font_sha256']==fnative['font_sha256']
    assert not fplan['failures'] and fnative['pages']==1 and fnative['complete_consumption_andpagination_exact']
    assert fnative['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    old=next(r for r in native['records'] if r['id']==ID)
    assert len(old['complete_native_English_display']['pages'])==1
    manuscript=Path('translations/rafael_B81_B84_contextual_editorial_manuscript_v2.json')
    row=next(r for r in load(manuscript)['records'] if r['id']==ID)
    assert fnative['records'][0]['logical_English']==row['english']
    ROOT.mkdir()
    p,n=deepcopy(plan),deepcopy(native)
    for doc,replacement in [(p,fplan['records'][0]),(n,fnative['records'][0])]:
        doc['records']=[deepcopy(replacement) if r['id']==ID else r for r in doc['records']]
        assert len(doc['records'])==323
        doc.update(manuscript=str(manuscript),manuscript_sha256=sha(manuscript.read_bytes()),
            one_fresh_source_prose_record=ID,unchanged322_record_proofs_reused=True,new_credit=0)
    save(ROOT/'plans323.json',p)
    n.update(plan=str(ROOT/'plans323.json'),plan_sha256=sha((ROOT/'plans323.json').read_bytes()),
        direct_visual_review_pending=False,all323_subset_body_layouts_approved=True,
        full_330_object_batch_display_complete=False,
        original_FE_pending_metadata_superseded_by_separate_four_page_proof=True,
        evidence={str(p):sha(p.read_bytes()) for p in [oldplan,oldnative,newplan,newnative,approval,manuscript,Path(__file__)]})
    save(ROOT/'native323.json',n)
    assert all(a==b for a,b in zip(native['records'],n['records'],strict=True) if a['id']!=ID)
    save(ROOT/'composition.json',dict(changed_ID=ID,fresh_records=1,exact_reused_records=322,total_records=323,
        fresh_pages=1,exact_reused_pages=331,total_pages=332,all_new_pages_directly_viewed=True,new_credit=0,
        source_manuscript=str(manuscript),source_manuscript_sha256=sha(manuscript.read_bytes()),
        plan=str(ROOT/'plans323.json'),native=str(ROOT/'native323.json')))
    print('One fresh prose plan/plane plus322 exact record proofs;332 subset pages,zero extra credit.')

if __name__=='__main__':main()
