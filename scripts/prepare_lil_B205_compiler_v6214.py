"""Reuse the atomic assembler with B205's exact independent source and actual contracts."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.seal_lil_B205_references_v6213 import FLAGS
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B205_compiler_tools_v6214')
if __name__=='__main__':
    assert not ROOT.exists();old=Path('dk4tool/patch/lil_B204_editorial_v2.py').read_text(encoding='utf-8');a=old.index('FLAGS=');b=old.index('\ndef load',a);exact=next(l for l in old.splitlines() if l.startswith('    exact=['))
    tool=derive('dk4tool/patch/lil_B204_editorial_v2.py','dk4tool/patch/lil_B205_editorial_v1.py',{
        old[a:b]:'FLAGS='+repr(FLAGS)+'\n','B204':'B205','lil_B204_layout_v4':'lil_B205_layout_v2','lil_B204_profile_v2':'lil_B205_profile_v2','lil_B204_editorial_guards_v1':'lil_B205_editorial_guards_v1','SELECTORS={2,11,124,130,145,254}':'SELECTORS={2,15,254}',
        'all20_source_native_reference_and_representative_rules_approved':'all17_source_native_reference_and_representative_rules_approved','all_measured_timing_RNG_state_and_prompt_differences_preserved':'all_measured_timing_RNG_state_and_RGB_scopes_preserved',
        '==204':'==205','block=204':'block=205','[204]':'[205]','end==1312 and len(block)==1312':'end==620 and len(block)==620','mapped(end)==1344':'mapped(end)==578','len(target)==1344 and len(logical)==1344':'len(target)==580 and len(logical)==578',
        "len(commands)==26 and sum(c['word']==0x4000 for c in commands)==20":"len(commands)==25 and sum(c['word']==0x4000 for c in commands)==17",'[(1308,1340)]':'[(616,574)]',
        exact:"    exact=[(32,'414893a8'),(346,'0c63'),(348,'2d63'),(590,'00a0ffff010d0260'),(598,'2147'),(600,'00a0ffff010d0f60'),(608,'00a0ffff01009330'),(616,'00000000')]",'6 exact leaves required':'8 exact leaves required','[0x4301,0x4381,0x4835,0x4735,0xA000,0]':'[0x4841,0x630C,0x632D,0xA000,0x4721,0xA000,0xA000,0]',
        'source_commands=26':'source_commands=25','all16_progressive_four_FE_letters_two43xx_picture47xx_one_A000_and_single_end_preserved':'all10_progressive_seven_FE_echoes_sounds_two63xx_picture47xx_three_A000_and_single_end_preserved',
        'actual_three_source_scopes20_panels77_holds_timing_RNG_and16_prompt_differences_not_natural_activation':'actual_two_complete_same_code_scopes17_panels63_holds_timing_RNG98_later_RGB_matches_not_natural_activation',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_atomic_compiler_derivation.json',dict(tool=tool,readonly_guards='dk4tool/patch/lil_B205_editorial_guards_v1.py',native_addresses_atomic_assembly_inverse_and_single_final_mutation_preserved=True,source620_target580_logical578_two_target_tailbytes=True,source_objects=17,source_commands=25,full_goal_complete=False));print('B205 atomic assembler prepared with exact17-object,eight-leaf,source/actual/name/echo guards and target tail2.')
