"""Keep every provider/target guard; disclose the two known corrupt CP932 baselines."""
from scripts import check_editorial_two_choice_explicit_route_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    '    args.out.mkdir(parents=True);planes=[];pictures=[]':
        '    args.out.mkdir(parents=True);planes=[];pictures=[];unpainted_corrupt_current=[]',
    '    for version in versions[1:]:':
        """    for version in versions[1:]:
        if version['version']=='current-padded-English' and not all(t.isascii() for t in version['cases'][0]['native_VM']['labels']):
            assert [t.strip() for t in version['cases'][0]['native_VM']['labels']]==['産es','札ecline']
            assert version['object_hex']==current.hex()
            unpainted_corrupt_current=[dict(option=i,text=t,CP932_hex=label.hex()) for i,(t,label) in enumerate(zip(version['cases'][0]['native_VM']['labels'],labels(current),strict=True))]
            continue""",
    '        source_font_planes_unchanged_not_replayed=True,bridged_modal_loop_not_actual_controller=True,':
        """        source_font_planes_unchanged_not_replayed=True,bridged_modal_loop_not_actual_controller=True,
        exact_corrupt_current_provider_checked_butnot_ASCII_painted=unpainted_corrupt_current,
        current_font_comparison_not_approved=True,
        reviewed_target_has_four_complete_ASCII_caption_style_planes=len(planes)==4,
        source_current_target_all_six_native_VM_alignment_cases_still_executed=True,""",
})
scope={**previous.main.__globals__,'__file__':__file__}
exec(compile(source,__file__+'::same-provider-target-pixel-rejection-guards-disclosed-corrupt-baseline','exec'),scope)
main=scope['main']
if __name__=='__main__':main()
