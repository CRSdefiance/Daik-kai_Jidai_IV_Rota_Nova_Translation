"""Project approved native speech/menu evidence into the existing complete-scene rebuilder."""
import argparse
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ['manuscript','plan','packet','native','menu','visual','out']:
        parser.add_argument('--'+key,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    doc,plan,packet,native,menu,visual=map(load,[args.manuscript,args.plan,args.packet,args.native,args.menu,args.visual])
    digest=sha(args.manuscript.read_bytes())
    assert native['manuscript_sha256']==plan['manuscript_sha256']==menu['manuscript_sha256']==digest
    assert native['plan_sha256']==sha(args.plan.read_bytes()) and not plan['failures']
    assert all(i['severity'] not in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and native['complete_consumption_andpagination_exact']
    assert not native['direct_visual_review_pending'] and not menu['direct_view_pending']
    assert native['runtime']==menu['runtime'] and packet['runtime']['candidate_sha256']==native['runtime']['candidate_sha256']
    assert all(c['word']!=0x4100 for g in packet['groups'] for c in g['all_source_commands'])
    assert all(c['word']!=0x4100 for g in packet['groups'] for c in g['all_current_commands'])
    assert not any(r.get('native_object_kind')=='4100-style-alternative' for r in doc['records'])
    assert visual['all234_current_body_pages_andall_generated_readable_sheets_directly_viewed']
    assert visual['all12_caption_labels_both_native_styles_andboth_sheets_directly_viewed']
    captions=[r for r in doc['records'] if r['kind']=='typed-choice-label']
    assert len(captions)==sum(len(m['record_IDs']) for m in menu['menus'])
    for row in captions:
        assert all(row['review'][k] for k in ['source','context','localization','naturalness']) and not row['review']['formatting']
    args.out.mkdir(parents=True)
    projected=deepcopy(menu)
    projected.update(offline_visual_approved=True,source_visual_approval=str(args.visual),source_visual_approval_sha256=sha(args.visual.read_bytes()),
        projection_not_new_native_execution=True)
    save(args.out/'menu.json',projected)
    save(args.out/'styles.json',dict(manuscript=str(args.manuscript),manuscript_sha256=digest,plan=str(args.plan),plan_sha256=sha(args.plan.read_bytes()),
        runtime=native['runtime'],objects=[],records=[],zero_source_andcurrent_4100_objects_independently_inventoried=True,
        empty_style_view_not_a_new_rendering_orname_proof=True,new_credit=0))
    save(args.out/'qualification.json',dict(no_prose_encoded_bytes_control_refs_orreview_gates_changed=True,
        all_source_current_commands_inventoried_zero_style_objects=True,fifth_gates_stored_actual_andintegration_still_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [args.manuscript,args.plan,args.packet,args.native,args.menu,args.visual,Path(__file__)]},new_credit=0))
    print('Prepared exact approved menu projection andsource-inventoried empty style view;no new checks orcredit claimed.')


if __name__=='__main__':main()
