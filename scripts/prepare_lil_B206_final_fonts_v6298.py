"""Rerun only changed compiled planes;reuse old native evidence only after exact source/runtime/byte checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B206_final_font_tools_v6298')
if __name__=='__main__':
    assert not ROOT.exists()
    setup='''    cases=[];reports=[];pictures=[];calls=0;reused_calls=0
    from copy import deepcopy
    priorpath=Path('work/analysis/lil_B206_fonts_v6295/all24_progressive_complete_native_planes192_alignment_cases.json');previous=read(priorpath);old_doc=read(previous['manuscript']);old_rows={r['id']:r for r in old_doc['records']};old_cases={r['id']:r for r in previous['cases']}
    assert previous['ARM9_sha256']==sha(arm) and previous['COMMON_sha256']==sha(ctx.common) and previous['candidate_sha256']==doc['current_ROM_sha256'] and previous['scoped_profile_sha256']==sha(PROFILE.read_bytes())
    assert read(previous['current_context_plan'])['actual_snapshot']['sha256']==sha(ctx.raw)
    for path,digest in previous['evidence'].items():assert sha(Path(path).read_bytes())==digest
    fresh_indices=[];reused_indices=[]'''
    cached='''        assert all(raw[1:].count(m)==logical.count(m)==body.count(m)==0 for m in [b'FI',b'FA',b'FO'])
        old_row=old_rows[row['id']];old_case=old_cases[row['id']]
        assert all(old_row[k]==row[k] for k in ['source_hex','current_hex','source_reference','current_reference','english','source_selector'])
        if old_row['compiled_hex']==row['compiled_hex']:
            assert old_case['encoded_hex']==encoded.encoded.hex() and old_case['expanded_hex']==body.hex() and old_case['complete_native_independent216x64_plane_equal'] and old_case['one_native_page_consumes_complete_target']
            assert sha(Path(old_case['preview']).read_bytes())==old_case['preview_sha256'] and sum(len(v['cases']) for v in old_case['current_native_macro_pipelines'])==8
            assert all(c['output_hex']==body.hex() for p in old_case['current_native_macro_pipelines'] if p['kind']=='compiled-protected' for c in p['cases'])
            case=deepcopy(old_case);case['reviewed_ordinary_boundaries']=qa.get('reviewed_ordinary_boundaries',[]);case['native_evidence_reused_from']=str(priorpath);case['native_evidence_reused_from_sha256']=sha(priorpath.read_bytes());cases.append(case)
            reports.append(dict(id=row['id'],qa=qa,unwaived_issues=issues,documented_rowcount_waivers=row.get('qa_waivers',[])));pictures.append((row['id'],row['speaker'],Image.open(case['preview']).convert('RGB')));reused_calls+=8;reused_indices.append(row['source_record_index']);print(row['id']+' exact native input/plane reuse',flush=True);continue
        fresh_indices.append(row['source_record_index']);pipelines=[]'''
    tools=derive('scripts/verify_lil_B206_fonts_v6295.py','scripts/verify_lil_B206_fonts_v6298.py',{
      'lil_B206_fonts_v6295':'lil_B206_fonts_v6298',
      'lil_B206_editorial_manuscript_v4':'lil_B206_editorial_manuscript_v5',
      'lil_B206_layout_v2':'lil_B206_layout_v3',
      'cases=[];reports=[];pictures=[];calls=0':setup.strip(),
      "        assert all(raw[1:].count(m)==logical.count(m)==body.count(m)==0 for m in [b'FI',b'FA',b'FO']);pipelines=[]":cached,
      "assert len(cases)==24 and calls==192 and not ctx.machines and sum(bool(r['reviewed_ordinary_boundaries']) for r in cases)==2":"assert len(cases)==24 and calls==24 and reused_calls==168 and fresh_indices==[24,53,90] and not ctx.machines and sum(bool(r['reviewed_ordinary_boundaries']) for r in cases)==5",
      'all24_progressive_complete_native_planes192_alignment_cases':'all24_final_progressive_planes24_fresh168_exact_reused_alignment_cases',
      'current_original_macro_alignment_calls=192':'current_original_macro_alignment_calls=24,covered_native_alignment_cases=192,exact_input_byte_identical_reused_native_alignment_cases=168,fresh_plane_indices=fresh_indices,reused_plane_indices=reused_indices',
      'original_alignment_calls=192':'new_original_alignment_calls=24,exact_reused_alignment_cases=168',
    })
    ROOT.mkdir(parents=True);save(ROOT/'three_changed_planes_native_verifier_and_exact_reuse_contract.json',dict(verifier=tools,fresh_plane_indices=[24,53,90],expected_fresh_alignment_calls=24,expected_exact_reused_alignment_cases=168,old_actual_snapshot_ARM9_COMMON_profile_and_complete_font_plane_inputs_must_match=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False));print('Final current-font verifier prepared:3 changed planes/24 fresh calls;21 planes/168 cases reused only after complete exact-input guards.')
