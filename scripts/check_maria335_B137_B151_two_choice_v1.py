"""Check all providers and target pixels; skip only the exact corrupt old refusal font."""
from scripts import check_editorial_two_choice_explicit_route_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    '    args.out.mkdir(parents=True);planes=[];pictures=[]':
        '    args.out.mkdir(parents=True);planes=[];pictures=[];unpainted_corrupt_current=[]',
    '        for index,label in enumerate(vm[\'labels\']):':
        """        if version['version']=='current-padded-English':
            assert [t.strip() for t in vm['labels']]==['Please','丑o'] and version['object_hex']==current.hex()
        for index,label in enumerate(vm['labels']):
            if version['version']=='current-padded-English' and not label.isascii():
                raw=labels(current)[index]
                assert index==1 and label.strip()=='丑o' and raw.hex()=='894e6f2020202020'
                unpainted_corrupt_current.append(dict(option=index,text=label,CP932_hex=raw.hex()))
                continue""",
    '        source_font_planes_unchanged_not_replayed=True,bridged_modal_loop_not_actual_controller=True,':
        """        source_font_planes_unchanged_not_replayed=True,bridged_modal_loop_not_actual_controller=True,
        exact_corrupt_current_provider_checked_butnot_ASCII_painted=unpainted_corrupt_current,
        current_font_comparison_not_approved=True,
        current_valid_ASCII_option_normal_highlight_planes=sum(r['version']=='current-padded-English' for r in planes),
        reviewed_target_has_four_complete_ASCII_caption_style_planes=sum(r['version']=='reviewed-English' for r in planes)==4,
        source_current_target_all_six_native_VM_alignment_cases_still_executed=True,""",
})
scope={**previous.main.__globals__,'__file__':__file__}
exec(compile(source,__file__+'::same-provider-caption-guards-one-source-locked-corrupt-font-exclusion','exec'),scope)
main=scope['main']
if __name__=='__main__':main()
