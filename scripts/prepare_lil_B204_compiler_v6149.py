"""Retain the atomic source assembler and supply B204's exact verified contracts."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.seal_lil_B204_references_v6148 import FLAGS
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B204_compiler_tools_v6149')
if __name__=='__main__':
    assert not ROOT.exists();old=Path('dk4tool/patch/lil_B203_editorial_v1.py').read_text('utf-8');fa=old.index('FLAGS=');fb=old.index('\ndef load',fa);start=old.index('    native,stored,controls,sample,ends,names=');end=old.index('    fonts={c',start)
    helper="    from dk4tool.patch.lil_B204_editorial_guards_v1 import validate\n    native,stored,controls,sample,ends,names,fields,terms,voices,state,approval,actual,rows,ids,spec,old_blocks,block,original=validate(doc,mapping,seal,conf,source,arm,japanese)\n"
    exact=next(x for x in old.splitlines() if x.startswith('    exact=['))
    changes={old[fa:fb]:'FLAGS='+repr(FLAGS)+'\n',old[start:end]:helper,'B203':'B204','lil_B203_layout_v2':'lil_B204_layout_v4','lil_B203_profile':'lil_B204_profile_v2','SELECTORS={2,76,170,254}':'SELECTORS={2,11,124,130,145,254}',
      '==203':'==204','block=203':'block=204','[203]':'[204]',"Counter({b'FI':1})":"Counter()",'one original FI and no FA/FO':'no original FI/FA/FO',
      "end==814 and len(block)==816 and block[end:]==bytes(2)":"end==1312 and len(block)==1312 and block[end:]==bytes(0)",'mapped(end)==768':'mapped(end)==1344','len(target)==768 and len(logical)==768':'len(target)==1344 and len(logical)==1344',
      "len(commands)==31 and sum(c['word']==0x4000 for c in commands)==22":"len(commands)==26 and sum(c['word']==0x4000 for c in commands)==20",'[(810,764)]':'[(1308,1340)]',
      exact:"    exact=[(256,'0143'),(258,'8143'),(342,'354874a8'),(694,'3547'),(696,'00a0ffff01007430'),(1308,'00000000')]",'9 exact leaves required':'6 exact leaves required','[0x4820,0x4735,0x6003,0x632E,0xA000,0xA000,0xA000,0xA000,0]':'[0x4301,0x4381,0x4835,0x4735,0xA000,0]',
      'source_commands=31':'source_commands=26','all21_progressive_one_FE_FI_resource632E_6003_picture47xx_four_A000_and_single_end_preserved':'all16_progressive_four_FE_letters_two43xx_picture47xx_one_A000_and_single_end_preserved',
      'actual_two_complete_B22_fixtures22_panels86_holds23_timings18_prompt_differences_equal_sampled_PRNG_not_natural_activation':'actual_three_source_scopes20_panels77_holds_timing_RNG_and16_prompt_differences_not_natural_activation','native_code_and123040_staged_payload_unchanged':'native_code_and123264_staged_payload_unchanged',
    }
    tool=derive('dk4tool/patch/lil_B203_editorial_v1.py','dk4tool/patch/lil_B204_editorial_v1.py',changes);ROOT.mkdir(parents=True);save(ROOT/'source_locked_compiler_derivation.json',dict(tool=tool,all_native_integer_constants_atomic_assembly_and_single_final_mutation_preserved=True,B204_readonly_guards='dk4tool/patch/lil_B204_editorial_guards_v1.py',full_goal_complete=False));print('B204 atomic compiler prepared:source assembly/inverse preserved;exact20-object/four-letter/measured-gameplay guards supplied.')
