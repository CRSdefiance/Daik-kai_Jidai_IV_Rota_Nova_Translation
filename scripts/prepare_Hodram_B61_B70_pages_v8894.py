"""Prepare fresh complete native pages; no unrelated historical partial reuse."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B61_B70_pages_preparation_v8894')
if __name__=='__main__':
    assert not ROOT.exists()
    plan=read('work/analysis/Hodram_B61_B70_layout_v8893/automatic_plans.json')
    assert len(plan['records'])==224 and not plan['failures']
    assert not any(i['severity'] in ['error','warning'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert sum(p['expected_native_pages'] for p in plan['records'])==229
    assert sum(p['expected_native_pages']==2 for p in plan['records'])==5
    old="""    reuse_path=Path('work/analysis/Hodram_B54_B60_pages_preparation_v8803b/65_complete_rows_andnine_sheets_exact.json');reuse=read(reuse_path)
    assert reuse['manuscript_sha256']==sha(DOC.read_bytes()) and reuse['plan_sha256']==sha(PLAN.read_bytes())
    for path,digest in reuse['files'].items():assert sha(Path(path).read_bytes())==digest
    rows=list(reuse['records']);sheets=list(reuse['sheets']);page_count=reuse['pages']
"""
    changes={
        'Complete native English pages and four compiled alignments for all82 utterances.':'Complete native English pages and four compiled alignments for all224 utterances.',
        'scripts.Hodram_B31_B53_registered_route_context_v8781':'scripts.Hodram_B54_B60_registered_route_context_v8868',
        'scripts.prove_Hodram_B54_B60_logical_v8801':'scripts.prove_Hodram_B61_B70_logical_v8891',
        'work/analysis/Hodram_B54_B60_pages_v8803b':'work/analysis/Hodram_B61_B70_pages_v8894',
        'translations/hodram_B54_B60_editorial_manuscript_v1.json':'translations/hodram_B61_B70_editorial_manuscript_v1.json',
        'work/analysis/Hodram_B54_B60_layout_v8802c/automatic_plans.json':'work/analysis/Hodram_B61_B70_layout_v8893/automatic_plans.json',
        'work/analysis/Hodram_B54_B60_logical_v8801/logical_paragraphs.json':'work/analysis/Hodram_B61_B70_logical_v8891/logical_paragraphs.json',
        'work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json':
            'work/analysis/Hodram_B61_B70_source_display_v8881/224_complete_source_dispatches_alignments_pages_andmacro_binding.json',
        'work/analysis/current_V8778_Hodram_native_v8781/current_native_input.json':'work/analysis/current_V8865_Hodram_native_v8868/current_native_input.json',
        "len(plan['records'])==82":"len(plan['records'])==224",
        old:'    rows=[];sheets=[];page_count=0\n',
        "        if block in reuse['blocks']:continue\n":'',
        'len(rows)==82 and page_count==85':'len(rows)==224 and page_count==229',
        'fresh_compiled_alignment_cases=68,reused_compiled_alignment_cases=260,total_bound_compiled_alignment_cases=328,progressive_alignment_cases=324,FE_null_actor_alignment_cases=4,complete_native_English_pages=85':
            'fresh_compiled_alignment_cases=896,reused_compiled_alignment_cases=0,total_bound_compiled_alignment_cases=896,progressive_alignment_cases=896,FE_null_actor_alignment_cases=0,complete_native_English_pages=229',
        'progressive_pages=84,FE_panels=1':'progressive_pages=229,FE_panels=0',
        'FI3_FA4_FO0_preserved_no_shortening_orprose_manual_wrap':'FI15_FA3_FO0_preserved_no_shortening_orprose_manual_wrap',
        "completed65_reuse=str(reuse_path),completed65_reuse_sha256=sha(reuse_path.read_bytes()),":
            'all224_compiled_paragraphs_executed_fresh_in_ownV8865=True,',
        'all82_formatting_gates_still_false':'all224_formatting_gates_still_false',
        '82 records /85 complete native English pages /328 compiled alignments pass':'224 records /229 complete native English pages /896 compiled alignments pass'
    }
    receipt=derive('scripts/prove_Hodram_B54_B60_pages_v8803b.py','scripts/prove_Hodram_B61_B70_pages_v8894.py',changes)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',dict(derivation=receipt,
        original_full_glyph_codes_native_independent_pixels_bounds_consumption_four_alignments_andcontinuation_guard_checks_preserved=True,
        fresh_scope_224_paragraphs229_pages5_two_page_records_bound_to_complete_current_plans=True,
        no_unrelated65_record_reuse_ornew_gameplay_claim=True,new_credit=0,full_goal_complete=False))
    print('Prepared fresh224 compiled paragraphs/229 native pages/896 alignments; no captures orROM changes.')
