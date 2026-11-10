"""Keep every v1 native guard and journal completed records before any later failure."""
from scripts import check_editorial_compiled_pages_static_captain_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous.source,{
    '    args.out.mkdir(parents=True)':
        """    args.out.mkdir(parents=True)
    save(args.out/'native_run_inputs.json',dict(runtime=ctx.receipt(),font_sha256=sha(font),
        manuscript=str(args.manuscript),manuscript_sha256=sha(args.manuscript.read_bytes()),
        plan=str(args.plan),plan_sha256=sha(args.plan.read_bytes()),
        macro_proof=str(args.macro_proof),macro_proof_sha256=sha(args.macro_proof.read_bytes()),
        source_owned_target_page_adapter=adapter,source_owned_progressive_macro_adapter=macro_adapter,
        all_v1_native_assertions_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),
        individual_receipts_do_not_claim_complete_run_orvisual_approval=True,new_credit=0))""",
    "                complete_native_English_display=rendered))":
        """                complete_native_English_display=rendered))
            save(args.out/('complete_'+row['id']+'.json'),dict(
                native_run_inputs=str(args.out/'native_run_inputs.json'),
                native_run_inputs_sha256=sha((args.out/'native_run_inputs.json').read_bytes()),
                record=rows[-1],four_native_alignment_cases_pass=True,
                all_original_native_glyph_pixels_consumption_canaries_bounds_androw_assertions_pass=True,
                direct_visual_review_pending=True,actual_gameplay=False,new_credit=0))""",
})
if __name__=='__main__':
    env={**vars(previous),**globals()}
    exec(compile(source,__file__+'::unchanged-native-checks-append-only-completed-record-receipts','exec'),env)
