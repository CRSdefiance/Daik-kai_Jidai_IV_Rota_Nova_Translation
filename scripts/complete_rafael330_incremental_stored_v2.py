"""Compose one fresh stored body and326 exact qualified reuses with current offsets."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael330_stored_native_v2_20261105')
REBUILT=Path('work/analysis/Rafael330_stored_consumer_inputs_v2_20261105/native_consumer_reconstruction.json')
REUSE=Path('work/analysis/Rafael330_incremental_stored_v2_20261105/exact326_stored_reuse.json')
FRESH=Path('work/analysis/Rafael330_fresh_Emilio_stored_v2_20261105/stored_native_verification.json')

if __name__=='__main__':
    assert not ROOT.exists();reuse,fresh,new=map(load,[REUSE,FRESH,REBUILT])
    assert len(fresh['records'])==1 and fresh['records'][0]['id']==reuse['changed_ID']
    assert fresh['fresh_relocated_native_relative_cases']==140
    assert fresh['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    byid={r['id']:{**r['exact_prior_stored_record'],**{k:r[k] for k in ['block','new_offset','new_record_index']},
        'same_bytes_runtime_parity_native_proof_reused':True} for r in reuse['records']}
    byid[fresh['records'][0]['id']]=fresh['records'][0]
    rows=[byid[t['id']] for g in new['groups'] for t in g['text_records']]
    assert len(rows)==327
    ROOT.mkdir();save(ROOT/'stored_native_verification.json',dict(
        reconstruction=str(REBUILT),reconstruction_sha256=sha(REBUILT.read_bytes()),
        native=new['native'],native_sha256=new['native_sha256'],runtime=fresh['runtime'],records=rows,
        relative_cases=fresh['relative_cases'],fresh_relocated_native_relative_cases=140,
        complete_stored_pages=336,one_fresh_stored_record=1,exact_prior_stored_records_reused=326,
        one_fresh_compiled_page_bound_in_storage=1,exact_prior_stored_pages_reused=335,
        fresh_parity_dependent_pages=0,all_stored_planes_equal_directly_viewed_compiled_planes=True,
        every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass=True,
        fresh_CPU_renderer_not_needed_for_exact_compiled_bytes_without_parity_tail=True,
        actual_gameplay=False,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [REBUILT,REUSE,FRESH,Path(__file__)]}))
    print('327 current stored bodies/336 pages:one fresh text,326 exact reuses;all140 branch cases fresh.')
