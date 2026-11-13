"""Refresh reviewed prose while reusing exact unchanged macro/role preflights."""
import argparse
from copy import deepcopy
from pathlib import Path
import re
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['previous','prose','out']:p.add_argument('--'+name,type=Path,required=True)
    args=p.parse_args();assert not args.out.exists()
    ip=args.previous/'formatting_input.json';mp=args.previous/'native_macro_measurements.json'
    previous,prose,macros=map(load,[ip,args.prose,mp])
    assert digest(mp)==previous['macro_proof_sha256'] and previous['runtime']==prose['runtime']==macros['runtime']
    assert prose['all_individual_four_prose_gates_pass'] and prose['all_fifth_formatting_gates_pending']
    old={r['id']:r for r in previous['records']};new={r['id']:r for r in prose['records']}
    assert len(old)==len(previous['records'])==len(new)==len(prose['records'])
    assert old.keys()==new.keys() and previous['file_path']==prose['file_path'] and previous['blocks']==prose['blocks']
    rows=[];changed=[];tokens=0
    for r in prose['records']:
        before=old[r['id']]
        for key in ['file_path','block','kind','source_hex','source_reference','current_hex','current_reference','source_macros','source_selector']:
            assert r.get(key)==before.get(key),(r['id'],key)
        assert r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        for key in ['source_complete_preamble_hex','source_header_hex','source_style_indices','source_object_hex','source_index','source_word']:
            assert r.get(key)==before.get(key),(r['id'],key)
        row=deepcopy(r);logical=r['english']
        assert logical.isascii() and '\n' not in logical and not any(t in logical for t in ['{LB','{ALIGN','{PAD'])
        row['editorial_logical_English']=logical
        row['english']=re.sub(r'\b(FI|FA|FO|FU)\b',lambda m:'{MACRO:'+m[0]+'}',logical)
        assert re.sub(r'\{MACRO:(FI|FA|FO|FU)\}',lambda m:m[1],row['english'])==logical
        for token,count in row['source_macros'].items():
            assert row['english'].count('{MACRO:'+token+'}')==count;tokens+=count
        if row['kind']!='typed-choice-label':
            row['planned_English_markup']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english']
            row['prior_macro_normalized_comparison']=row['english'] if row['decision']=='retention' else None
            if row.get('native_object_kind')=='4100-style-alternative':
                row['virtual_formatter_prefix_is_not_part_of_stored_alternative_text']=True
                assert row['source_choice_object_hex']==row['source_object_hex']
        if row['english']!=before['english']:changed.append(row['id'])
        rows.append(row)
    assert tokens==previous['source_macro_occurrences']
    result={**deepcopy(previous),**deepcopy(prose),'records':rows,
        'source_full_manuscript':str(args.prose),'source_full_manuscript_sha256':digest(args.prose),
        'macro_proof_sha256':digest(mp),'previous_formatting_input':str(ip),'previous_formatting_input_sha256':digest(ip),
        'exact_macro_preflight_reused_not_new_text_display_approval':True}
    args.out.mkdir(parents=True)
    for name in ['native_macro_measurements.json','role_bindings.json','initial_preferences.json']:
        source=args.previous/name;target=args.out/name;target.write_bytes(source.read_bytes());assert digest(source)==digest(target)
    save(args.out/'formatting_input.json',result)
    save(args.out/'refresh_verification.json',dict(changed_prose_IDs=changed,all_source_controls_substitutions_runtime_andmembership_exact=True,
        unchanged_macro_androle_proofs_reused_byte_exact=True,all_changed_text_requires_fresh_plan_native_pixels_andvisual_review=True,
        new_credit=0,evidence={str(p):digest(p) for p in [ip,mp,args.prose,Path(__file__)]}))
    print('Refreshed',len(rows),'records;',len(changed),'prose amendments;unchanged native macro/role proofs reused.')


if __name__=='__main__':main()
