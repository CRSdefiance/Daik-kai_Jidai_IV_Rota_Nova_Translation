"""Resume exact completed static/dynamic blocks after source-scoped FE corrections."""
from scripts import resume_editorial_native_blocks_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    '        assert not any(207<=r[\'source_selector\']<224 for r in expected)':
    '''        role_proof=load(args.role_bindings)
        assert role_proof['runtime']==ctx.receipt()
        role_sources={r['id']:r for r in role_proof['source_records']}
        for original in expected:
            if not 207<=original['source_selector']<224:continue
            source_role=role_sources[original['id']]
            assert original['source_reference']==source_role['source_reference']
            assert original['source_header_hex']==source_role['source_header_hex']
            assert original['source_style_indices']==source_role['source_style_indices']''',
    '    fresh_rows=[r for r in speeches if r[\'id\'] not in reused];assert reused and fresh_rows':
    '''    prior_sheets=[]
    for receipt in block_receipts:
        block=receipt['block']
        total=sum(planned[r['id']]['expected_native_pages'] for r in speeches if r['block']==block)
        files=sorted(args.partial.glob(f'B{block}_part*.png'))
        assert len(files)==(total+11)//12
        for index,path in enumerate(files):
            prior_sheets.append(dict(block=block,path=str(path),sha256=sha(path.read_bytes()),pages=min(12,total-12*index)))
    fresh_rows=[r for r in speeches if r['id'] not in reused];assert reused and fresh_rows''',
    "sum(r['source_macros'][k] for r in fresh_rows)":
    "sum(r.get('source_macros',{}).get(k,0) for r in fresh_rows)",
    'scripts/check_editorial_compiled_pages_v3.py': 'scripts/check_editorial_compiled_pages_v5.py',
    "review_sheets=fresh['review_sheets'],partial_static_run_producer='scripts/check_editorial_compiled_pages_v2.py'":
    "review_sheets=prior_sheets+fresh['review_sheets'],partial_static_run_producer='scripts/check_editorial_compiled_pages_v5.py'",
    'partial_run_ended_only_at_dynamic_identity_equals_prefix_assertion=True':
    'partial_run_ended_at_FE_consumption_assertion=True',
    'exact_same_manuscript_plan_own_runtime_static_prefixes_andplanes_reused=True':
    'exact_per_record_inputs_own_runtime_static_anddynamic_prefixes_andplanes_reused=True',
})
exec(compile(source, __file__ + '::same-runtime-completed-block-reuse-after-FE-corrections', 'exec'), globals())
