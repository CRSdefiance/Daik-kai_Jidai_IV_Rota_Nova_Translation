"""Prepare complete conditional relocation and stored-target native checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B190_relocation_tools_v5328')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B186_relocation_v5157.py','scripts/research_lil_B190_relocation_v5328.py',{
        'B186':'B190','relocation_v5157':'relocation_v5328','editorial_manuscript_v5':'editorial_manuscript_v3','combined_v5122':'combined_v5304',
        'Relocate all12':'Relocate all17','one700':'one500','len(source)==652 and old_end==650':'len(source)==608 and old_end==606',
        "len(spec['all_current_native_commands'])==24":"len(spec['all_current_native_commands'])==29",
        "sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==12":"sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==17",
        'number==186':'number==190','==[646]':'==[602]',"sum(len(r['text_records']) for r in results)==12":"sum(len(r['text_records']) for r in results)==17",
        "sum(len(r['command_map']) for r in results)==24":"sum(len(r['command_map']) for r in results)==29",'not in [186]':'not in [190]',
        'all12speech':'all17speech','24structural commands/12speech':'29structural commands/17speech'} )]
    rows.append(derive('scripts/prove_lil_B189_stored_v5288.py','scripts/prove_lil_B190_stored_v5329.py',{
        'B189':'B190','stored_v5288':'stored_v5329','relocation_v5287':'relocation_v5328','voices_v5274b':'voices_v5315','[82,104,113,147,254]':'[119,159,254]',
        'actual_selected_B189_scene_A000_C200_and_end_reachability_unexecuted':'actual_selected_B190_scene_predicate_three_alternatives_C200_and_end_reachability_unexecuted'}))
    ROOT.mkdir(parents=True)
    font=Path('work/analysis/lil_B190_fonts_v5326/all17_progressive_FE_native_planes_and136_alignment_cases.json');f=read(font)
    save(ROOT/'viewed_layout_retention_reasons.json',dict(native_font_proof=str(font),native_font_proof_sha256=sha(font.read_bytes()),all17_panels_on_three_native_sheets_viewed_after_image_return=True,
        retained_layouts=[dict(id='DK4_MES_B190_R0032',reason='Two substantial rows keep the residence owner and the of-this-mansion completion legible. The ordinary soft wrap adds no punctuation or dramatic pause. No orphan or third row;maximum first-row fill is not required.'),
            dict(id='DK4_MES_B190_R0036',reason='Two native rows keep the recognized illness and its no-known-cause modifier complete. The source distinction is preserved without shortening or a third row.'),
            dict(id='DK4_MES_B190_R0056',reason='Two rows keep They say store-bought medicine together before the complete cured-it-in-one-go predicate. All reportedness,retail availability and quick-cure wording remains.'),
            dict(id='DK4_MES_B190_R0059',reason='Two substantial rows retain both retail medicine and the illness of unknown cause as one complete questioning reply. No isolated final word or extra page.'),
            dict(id='DK4_MES_B190_R0071',reason='The apparent-truth reply and reported universal-illness reputation fit two full native rows. Source hearsay stays explicit;no word or skepticism is removed for width.'),
            dict(id='DK4_MES_B190_R0074',reason='Two rows preserve the excited personal hypothetical wish. The final like-that-myself phrase remains substantial rather than becoming an orphan or a third row.')],
        no_new_contextual_review_credit=True,no_record_specific_exception_or_font_guard_width_change=True,full_goal_complete=False))
    save(ROOT/'prepared_conditional_relocation_and_stored_checks.json',dict(tools=rows,source_stored_bytes=608,source_logical_end=606,source_alignment_tailzeros=2,
        source_commands=29,speeches=17,progressive=16,FE=1,relative_sites=6,predicates=1,threshold=500,A000=3,C200=1,source_end=602,
        expected_stored_alignment_cases=68,expected_native_target_skip_cases=30,target_lengths_to_be_measured=True,
        exact_inverse_includes_original_tailzeros=True,no_ROM_registry_ledger_or_review_credit_change=True,full_goal_complete=False))
