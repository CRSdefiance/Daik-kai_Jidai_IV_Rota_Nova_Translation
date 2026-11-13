"""Prepare reversible linear relocation with original alignment padding retained."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B188_relocation_tools_v5246')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B187_relocation_v5202.py','scripts/research_lil_B188_relocation_v5246.py',{
        'B187':'B188','relocation_v5202':'relocation_v5246','combined_v5177':'combined_v5219',
        'Relocate all16':'Relocate all11','preserve15 progressive':'preserve10 progressive',
        'len(source)==680 and old_end==678':'len(source)==484 and old_end==482',
        "len(spec['all_current_native_commands'])==19":"len(spec['all_current_native_commands'])==14",
        "sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==16":"sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==11",
        'number==187':'number==188','==[674]':'==[478]',"sum(len(r['text_records']) for r in results)==16":"sum(len(r['text_records']) for r in results)==11",
        "sum(len(r['command_map']) for r in results)==19":"sum(len(r['command_map']) for r in results)==14",'not in [187]':'not in [188]','all16speech':'all11speech',
        '19structural commands/16speech/15progressive':'14structural commands/11speech/10progressive'} )]
    rows.append(derive('scripts/prove_lil_B187_stored_v5203.py','scripts/prove_lil_B188_stored_v5247.py',{
        'B187':'B188','stored_v5203':'stored_v5247','relocation_v5202':'relocation_v5246','voices_v5189':'voices_v5233','Verify all16':'Verify all11',
        '[87,155,254]':'[130,150,254]','len(cases)==16':'len(cases)==11','fresh+reused==64':'fresh+reused==44',
        'all16_final_stored_targets64_macro_cases':'all11_final_stored_targets44_macro_cases','current_final_stored_macro_alignment_cases=64':'current_final_stored_macro_alignment_cases=44',
        'all16_final_targets':'all11_final_targets','stored_targets=16,progressive=15':'stored_targets=11,progressive=10','macro_cases=64':'macro_cases=44'}))
    ROOT.mkdir(parents=True)
    font=Path('work/analysis/lil_B188_fonts_v5244/all11_progressive_FE_native_planes_and88_alignment_cases.json');f=read(font)
    save(ROOT/'viewed_layout_retention_reasons.json',dict(native_font_proof=str(font),native_font_proof_sha256=sha(font.read_bytes()),
        all11_panels_on_two_native_sheets_viewed_after_image_return=True,
        retained_layouts=[dict(id='DK4_MES_B188_R0022',reason='Hmm. I had no idea / these were in fashion. keeps the introductory realization and its complete complement as two coherent parts. The two native rows are complete and balanced;no extra row,orphaned final word or wasted third row is created. Moving more words to the first row is not required by the full-width rule. Preserve all words and source controls without a special boundary exception.'),
            dict(id='DK4_MES_B188_R0038',reason='Good! I will add it to my collection (contracted in prose) is a complete decision on the first native row;Gather all the giyaman in town is the separate complete command on the second. The sentence boundary supports the full-width two-row layout.')],
        no_new_contextual_review_credit=True,no_record_specific_exception_or_font_guard_width_change=True,full_goal_complete=False))
    save(ROOT/'prepared_linear_relocation_and_stored_checks.json',dict(tools=rows,source_stored_bytes=484,source_logical_end=482,source_alignment_tailzeros=2,
        source_commands=14,speeches=11,progressive=10,FE=1,relative_sites=0,predicates=0,A000=1,C200=1,source_end=478,expected_stored_alignment_cases=44,
        target_lengths_to_be_measured=True,exact_inverse_includes_original_tailzeros=True,no_ROM_registry_ledger_or_review_credit_change=True,full_goal_complete=False))
