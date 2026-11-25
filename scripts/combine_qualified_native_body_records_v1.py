"""Join exact native body records without rerendering compatible pages or granting review gates."""
import argparse
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ['manuscript','plan','out']:parser.add_argument('--'+key,type=Path,required=True)
    parser.add_argument('--proofs',type=Path,nargs='+',required=True)
    args=parser.parse_args();assert not args.out.exists()
    doc,plan=map(load,[args.manuscript,args.plan]);assert plan['manuscript_sha256']==sha(args.manuscript.read_bytes())
    assert not plan['failures'] and not any(i['severity'] in ['error','warning'] for r in plan['records'] for i in r['base_QA']['issues'])
    proofs=[(p,load(p)) for p in args.proofs];runtime=proofs[0][1]['runtime'];font=proofs[0][1]['font_sha256']
    assert runtime['candidate_sha256']==doc['current_ROM_sha256']
    assert all(d['runtime']==runtime and d['font_sha256']==font for _,d in proofs)
    dictionaries=[(p,{r['id']:r for r in d['records']}) for p,d in proofs]
    originals={r['id']:r for r in doc['records'] if r['kind']!='typed-choice-label'}
    assert len(originals)==doc['physical_speech_objects']==len(plan['records'])
    records=[];origins={};counts={str(p):0 for p,_ in proofs}
    for target in plan['records']:
        original=originals[target['id']]
        matches=[(p,rows[target['id']]) for p,rows in dictionaries if target['id'] in rows
            and rows[target['id']]['compiled_hex']==target['encoded_hex']
            and rows[target['id']]['logical_English']==target['logical_English']==original['english']]
        assert matches,target['id'];path,row=matches[0]
        assert row['kind']==original['kind'] and row['source_reference']==original['source_reference'] and row['current_reference']==original['current_reference']
        assert len(row['native_alignment']['cases'])==4
        guard='original_macro_ABI_input_output_canaries_and4MiB_exact' if row['kind']=='system-FE' else 'original_macro_ABI_input_output_canaries_and_all_unowned4MiB_exact'
        assert all(c['output_hex']==row['expanded_native_hex'] and c[guard] for c in row['native_alignment']['cases'])
        display=row['complete_native_English_display']
        if row['kind']=='system-FE':
            assert display['all_first_internal_final_ASCII_CP932_codes_andindependent_logical_plane_exact']
            assert display['planned_native_row_comparison']['complete_glyph_row_membership_exact']
            pages=[display]
        else:
            assert display['all_visible_first_internal_final_characters_in_order'] and display['no_blank_or_overlap_page']
            assert display['complete_consumed_bytes']==len(bytes.fromhex(row['expanded_native_hex']))
            pages=display['pages']
        assert len(pages)==target['expected_native_pages']
        for page in pages:
            for key,digest in [('native_plane','native_plane_sha256'),('preview','preview_sha256')]:assert sha(Path(page[key]).read_bytes())==page[digest]
        records.append(deepcopy(row));counts[str(path)]+=1
        origins[row['id']]=dict(proof=str(path),proof_sha256=sha(path.read_bytes()),
            exact_compiled_source_current_prose_runtime_font_native_pages=True)
    args.out.mkdir(parents=True)
    save(args.out/'compiled_native_pages.json',dict(manuscript=str(args.manuscript),manuscript_sha256=sha(args.manuscript.read_bytes()),
        plan=str(args.plan),plan_sha256=sha(args.plan.read_bytes()),runtime=runtime,font_sha256=font,records=records,
        pages=sum(r['expected_native_pages'] for r in plan['records']),origins=origins,origins_counts=counts,
        all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass=True,complete_consumption_andpagination_exact=True,
        no_native_execution_repeated_by_this_exact_record_join=True,direct_visual_review_pending=True,formatting_gates_still_false=True,
        typed_choice_labels_scoped_names_stored_gameplay_andregistered_integration_separately_pending=True,
        actual_gameplay=False,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [args.manuscript,args.plan,*args.proofs,Path(__file__)]}))
    print(dict(body_records=len(records),native_pages=sum(r['expected_native_pages'] for r in plan['records']),origins=counts,new_credit=0))

if __name__=='__main__':main()
