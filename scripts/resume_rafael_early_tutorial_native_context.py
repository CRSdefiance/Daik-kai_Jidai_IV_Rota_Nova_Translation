"""Consolidate both completed blocks; correct a final count without replaying40 native checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/check_rafael_early_tutorial_native_context.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    '    assert not ROOT.exists()':
        "    assert ROOT.exists() and not (ROOT/'40_native_selectors_macros_andcomplete_preamble_bindings.json').exists()",
    '    ROOT.mkdir()':
    """    reused={}
    receipt_paths=[]
    for number in [42,43]:
        path=ROOT/f'B{number}_native_context.json';receipt=load(path)
        assert receipt['runtime']==ctx.receipt()
        receipt_paths.append(path)
        for item in receipt['records']:
            assert item['id'] not in reused
            reused[item['id']]=item
    assert len(reused)==40 and set(reused)==set(drafts)""",
    "            dispatch=ctx.execute(env['dispatch'],current_raw[0],current_raw[1:])":
    """            cached=reused[row['id']]
            assert cached['source_reference']==row['source_reference'] and cached['current_reference']==row['current_reference']
            assert cached['complete_source_andcurrent_preamble_hex']==header.hex() and cached['logical_English']==row['english']
            dispatch=cached['original_current_dispatch']
            assert dispatch['source_selector']==row['source_selector'] and dispatch['all4MiB_actor_role_RNG_input_and_ABI_guards_exact']
            assert dispatch['boundaries'][0]['kind']=='unexecuted-UI-preparation'
            boundary=dispatch['boundaries'][1]
            assert boundary['kind']==('unexecuted-FE-modal-body' if row['source_selector']==254 else 'unexecuted-progressive-body')
            assert boundary['text_hex']==expanded(current_raw[1:]).hex()""",
    "            logical_proof=ctx.execute(fe_env['expand'] if is_FE else progressive_env['expand'],body,*(() if is_FE else (row['source_selector'],)))":
    """            logical_proof=cached['four_native_macro_alignments']
            assert cached['expanded_logical_hex']==expected.hex()
            assert [c['input_alignment'] for c in logical_proof['cases']]==list(range(4))
            if is_FE:
                assert all(c['null_source_actor'] and c['original_macro_ABI_input_output_canaries_and4MiB_exact'] for c in logical_proof['cases'])
            else:
                assert logical_proof['original_selector']==row['source_selector'] and logical_proof['captain']==0
                assert all(c['original_macro_ABI_input_output_canaries_and_all_unowned4MiB_exact'] and c['source_owned_name_ring_restoration_recovers_complete4MiB'] for c in logical_proof['cases'])""",
    "        save(ROOT/f'B{group[\"block\"]}_native_context.json',dict(records=[r for r in rows if r['source_reference']['block']==group['block']],runtime=ctx.receipt(),new_credit=0))":
        "        assert load(ROOT/f'B{group[\"block\"]}_native_context.json')['records']==[r for r in rows if r['source_reference']['block']==group['block']]",
    'assert len(zero)==6':'assert len(zero)==5',
    'fresh_logical_macro_alignments=160,default_measurement_alignments=4,':
        'fresh_logical_macro_alignments=160,default_measurement_alignments=4,same_batch_completed_dispatches_reused=40,same_batch_completed_alignment_cases_reused=160,new_logical_cases_in_resume=0,new_default_measurement_cases_in_resume=4,summary_count_corrected_from6_to5_without_ROM_text_or_native_check_changes=True,',
    '[SOURCE,MANUSCRIPT,PRECEDENT,RELEASE,STARTUP,Path(__file__)]':
        "[SOURCE,MANUSCRIPT,PRECEDENT,RELEASE,STARTUP,Path('scripts/check_rafael_early_tutorial_native_context.py'),*receipt_paths,Path(__file__)]",
})
exec(compile(source,__file__+'::exact-completed-block-reuse-five-real-zero-selectors','exec'),globals())
