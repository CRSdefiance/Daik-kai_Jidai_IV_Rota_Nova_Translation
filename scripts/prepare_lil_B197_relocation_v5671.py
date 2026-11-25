"""Prepare exact B197 three-option relocation and final stored speech proofs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B197_relocation_tools_v5671')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B196_relocation_v5615.py','scripts/research_lil_B197_relocation_v5671.py',{
        'B196':'B197','relocation_v5615':'relocation_v5671','combined_v5580':'combined_v5637',
        '0x2100':'0x2200',"b'\\0\\x21'":"b'\\0\\x22'",
        "[r['option_index'] for r in rows]==[0,1]":"[r['option_index'] for r in rows]==[0,1,2]",
        'text_base=6,count=2':'text_base=8,count=3',"p=at+6+struct.unpack_from":"p=at+8+struct.unpack_from",
        'number==196 and len(end_maps)==7':'number==197 and len(end_maps)==1',
        "        assert all(a['target_offset']+4<b['target_offset'] for a,b in zip(end_maps,end_maps[1:])) # six purchases and final refusal have distinct ends":
        "        assert end_maps[0]['source_offset']==874 # single original common-tail end",
        "text_records']) for r in results)==24":"text_records']) for r in results)==21",
        "choice_commands']) for r in results)==6":"choice_commands']) for r in results)==1",
        "relative_skip_fixups']) for r in results)==52":"relative_skip_fixups']) for r in results)==6",
        "target_native_skip_cases']) for r in results)==260":"target_native_skip_cases']) for r in results)==30",
        "command_map']) for r in results)==119":"command_map']) for r in results)==39",
        'in [196]':'in [197]',
        'six_original2100_objects_twelve_source_ordered_buy_refusal_labels':'one_original2200_object_three_source_ordered_proposal_refusal_delegation_labels',
        'all24speech_six_menus_and52_relative_operands':'all21speech_one_menu_and6_relative_operands',
        'all260_relocated_native_skip_cases':'all30_relocated_native_skip_cases',
        'seven_separated_declared_purchase_refusal_end_words_exact':'single_original_common_tail_end_word_exact',
        '119commands/24speech/six2100/52spans/260targetskipcases,seven separated ends,all1816 source bytes inverse and335otherblocks exact.':
        '39commands/21speech/one2200/6spans/30targetskipcases,one common end,all880 predecessor bytes inverse and335otherblocks exact.'})]
    rows.append(derive('scripts/prove_lil_B196_stored_v5616.py','scripts/prove_lil_B197_stored_v5672.py',{
        'B196':'B197','all24':'all21','stored_v5616':'stored_v5672','relocation_v5615':'relocation_v5671',
        'voices_v5591':'voices_v5648','[2,6,19,20,25,173,254]':'[21,169,254]',
        'len(cases)==24':'len(cases)==21','fresh+reused==96':'fresh+reused==84','targets96_macro':'targets84_macro',
        'current_final_stored_macro_alignment_cases=96':'current_final_stored_macro_alignment_cases=84',
        'actual_selected_B196_price_branches_and_source_controls_unexecuted':'actual_selected_B197_English_choice_paths_and_source_controls_unexecuted',
        'stored_targets=24,progressive=23,FE=1,macro_cases=96':'stored_targets=21,progressive=20,FE=1,macro_cases=84'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_three_option_relocation_and_stored_checks.json',dict(tools=rows,
        source_commands=39,source_speeches=21,source2200_menus=1,labels=3,relative_sites=6,target_skip_cases=30,ends=1,
        original_source47xx_effect_resource_6003_and_all_other_leaves_unchanged=True,
        logical_inverse_plus_original_two_tailzeros_recovers_every_predecessor_byte=True,
        no_B196_R74_rule_or_source_FI_inherited=True,new_ROMs=0,new_editorial_credit=0,full_goal_complete=False))
