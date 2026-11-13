"""Prepare tests for exactly the nine original B203 nonspeech commands."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    original="""(8,'2d63'),(94,'0143'),(96,'00460b80'),(100,'8143'),(618,'304865a8'),(718,'3547'),
        (864,'0360'),(866,'2e63'),(906,'00a0ffff01021360'),(914,'00a0ffff01006530'),(922,'4046081d'),(926,'00000000')"""
    target="""(334,'204812a8'),(738,'3547'),(740,'0360'),(742,'2e63'),
        (778,'00a0fffffaff0191'),(786,'00a0ffff01020260'),(794,'00a0ffff01001230'),(802,'00a0ffff1d000100'),(810,'00000000')"""
    proof=derive('scripts/prove_lil_B200_controls_v5833.py','scripts/prove_lil_B203_controls_v6017.py',{
        'B200':'B203','controls_v5833':'controls_v6017','source_v5826':'source_v6010','voices_v5827':'voices_v6011',
        'all19_clean_current_complete_context':'all22_clean_current_complete_context','.blocks[200]':'.blocks[203]',
        "sum(c['word']==0x4000 for c in commands)==19":"sum(c['word']==0x4000 for c in commands)==22",
        original:target,
        '[0x632D,0x632E]':'[0x632E]',
        '[0x4821,0x4822,0x4823,0x4700,0x4830,0x4735]':'[0x4821,0x4822,0x4823,0x4700,0x4820,0x4735]',
        '[0x632D,0x632E,0x6003]':'[0x632E,0x6003]',
        '[0x4830,0x4735]':'[0x4820,0x4735]','word==0x4830':'word==0x4820',
        'at==926 and len(blocks[0])==len(blocks[1])==932':'at==810 and len(blocks[0])==len(blocks[1])==816',
        'logical==930':'logical==814','[0x4301,0x4600,0x4381,0xA000,0x4640]':'[0xA000]',
        'len(resources)==20':'len(resources)==10','len(structural)==6':'len(structural)==4',
        "call['descriptor']==[0,101,1,5] and call['layout']==[3,0,0]":"call['descriptor']==[0,18,1,5] and call['layout']==[2,0,0]",
        'twelve_exact_leaves_two_resources6003_picture47xx_six_structural_pairs_and_end':'nine_exact_leaves_resource632E_6003_picture47xx_four_A000_pairs_and_end',
        'all12_source_current_nonspeech_leaves':'all9_source_current_nonspeech_leaves',
        'two_resource_words20_boundary_cases':'one_resource632E_ten_boundary_cases',
        'source_six_structural_pairs':'source_four_A000_structural_pairs',
        'picture_descriptor101_layout3_0_0':'picture_descriptor18_layout2_0_0',
        'source4301_4600_4381_and_final4640_preserved_without_forced_transition_or_location':'no_source4301_4600_4381_4640_transition_commands_invented',
        'two_A000_operands_preserved_without_invented_reward_or_stat_body_semantics':'four_A000_operands_preserved_without_invented_payment_reward_or_stat_body_semantics',
        'actual_scene_transition_resource_effect_picture_stat_bodies_and_all19_speeches_still_unobserved':'actual_resource_effect_picture_payment_stat_bodies_and_all22_objects_still_unobserved',
        'no_predicate_choice_relative_FI_or2000_pause_inherited':'one_source_FE_FI_notice_no_FA_FO_predicate_choice_relative_or2000_pause_invented',
        'B20012 leaves exact:20 resource/10 6003 boundary cases,one picture/one47xx pair,six structural pairs,ten guarded ends. Actual semantics pending.':'B2039 leaves exact:10 resource/10 6003 boundary cases,one picture/one47xx pair,four A000 pairs,ten guarded ends. Descriptor18/layout2,0,0;actual semantics pending.',
    })
    root=Path('work/analysis/lil_B203_control_tools_v6017');root.mkdir(parents=True);save(root/'derivation.json',proof)
