"""Prepare complete linear relocation and stored native text verification."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B192_relocation_tools_v5420')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B188_relocation_v5246.py','scripts/research_lil_B192_relocation_v5420.py',{
        'B188':'B192','relocation_v5246':'relocation_v5420','combined_v5219':'combined_v5396','all11':'all8','preserve10 progressive':'preserve7 progressive',
        'len(source)==484 and old_end==482':'len(source)==404 and old_end==402',"len(spec['all_current_native_commands'])==14":"len(spec['all_current_native_commands'])==11",
        "sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==11":"sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==8",
        'number==188':'number==192','==[478]':'==[398]',"sum(len(r['text_records']) for r in results)==11":"sum(len(r['text_records']) for r in results)==8",
        "sum(len(r['command_map']) for r in results)==14":"sum(len(r['command_map']) for r in results)==11",'not in [188]':'not in [192]','14structural commands/11speech/10progressive':'11structural commands/8speech/7progressive',
    })]
    rows.append(derive('scripts/prove_lil_B190_stored_v5329.py','scripts/prove_lil_B192_stored_v5421.py',{
        'B190':'B192','stored_v5329':'stored_v5421','relocation_v5328':'relocation_v5420','voices_v5315':'voices_v5407','[119,159,254]':'[115,153,254]',
        'len(cases)==17':'len(cases)==8','fresh+reused==68':'fresh+reused==32','all17':'all8','targets68_macro':'targets32_macro','current_final_stored_macro_alignment_cases=68':'current_final_stored_macro_alignment_cases=32',
        'stored_targets=17,progressive=16':'stored_targets=8,progressive=7','macro_cases=68':'macro_cases=32','actual_selected_B190_scene_predicate_three_alternatives_C200_and_end_reachability_unexecuted':'actual_selected_B192_linear_A000_C200_and_end_reachability_unexecuted',
    }))
    ROOT.mkdir(parents=True);font=Path('work/analysis/lil_B192_fonts_v5418/all8_progressive_FE_native_planes_and64_alignment_cases.json')
    save(ROOT/'viewed_layout_retention_reasons.json',dict(native_font_proof=str(font),native_font_proof_sha256=sha(font.read_bytes()),
        all8_panels_on_one_native_sheet_viewed_after_image_return=True,
        retained_layouts=[dict(id='DK4_MES_B192_R0016',reason='Three substantial rows keep the astonished popularity reaction and probably-only-person hyperbole complete. No words were shortened or isolated to obtain a row count.'),
            dict(id='DK4_MES_B192_R0023',reason='Two substantial native rows preserve the affirmative,decision,offer to try and follow-me instruction. The ordinary object continuation some is joined to the following complete invitation;no orphan or extra page.')],
        no_record_specific_boundary_exception_or_font_metric_guard_width_change=True,no_credit=True,full_goal_complete=False))
    save(ROOT/'prepared_linear_relocation_and_stored_checks.json',dict(tools=rows,source_stored=404,source_logical=402,source_tailzeros=2,source_commands=11,speeches=8,
        expected_stored_cases=32,all_target_extents_to_be_measured=True,no_ROM_registry_or_credit_change=True,full_goal_complete=False))
