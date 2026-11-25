"""Bind the independently inventoried parrot source to registered V6160."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B205_source_tools_v6172')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/map_lil_B204_source_v6062.py','scripts/map_lil_B205_source_v6172.py',{
        'B204':'B205','source_v6062':'source_v6172','verification_v6061':'verification_v6166','clean_context_v6059':'clean_context_v6171','all20_clean_castle_figurehead_claim_missing_shachihoko_and_letter_glosses':'all17_clean_parrot_mimicry_catch_and_echoed_victory_glosses',
        '==6349':'==6370','blocks[204]':'blocks[205]','block=204':'block=205','len(old)==26 and len(spoken)==20':'len(old)==25 and len(spoken)==17','[2,11,124,130,145,254]':'[2,15,254]','[2,11,124,130,145]':'[2,15]',
        '[0x4301,0x4381,0x4835,0x4735,0xA000,0]':'[0x4841,0x630C,0x632D,0xA000,0x4721,0xA000,0xA000,0]','work/analysis/lil_B203_runs_v6052/newgame_terminal.json':'work/analysis/lil_B204_runs_v6162/newgame_terminal.json','physical_speeches=20':'physical_speeches=17','FE_panels=4':'FE_panels=7','all20_clean_current_complete_context':'all17_clean_current_complete_context','total_editorial_objects=20,speech_objects=20,ordinary_source_speeches=16,system_FE_panels=4':'total_editorial_objects=17,speech_objects=17,ordinary_source_speeches=10,system_FE_panels=7','source_native_commands=26':'source_native_commands=25','source_A000=1':'source_A000=3','all20_clean_first_glosses':'all17_clean_first_glosses',
        'B204 bound:20 objects/26 commands/four FE letters,no macros;five source actors and actual V6050 opening snapshot.No old-English prose comparison or credit.':'B205 bound:17 objects/25 commands,seven FE sound/echo objects,no macros;two source actors and actual V6160 opening snapshot.No old-English prose comparison or credit.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_source_binding.json',dict(tool=tool,source_gloss_precedes_current_raw_byte_binding=True,all_native_addresses_and_original_inventory_logic_preserved=True,no_B204_letter_actor_count_or_effect_contract_inherited=True,full_goal_complete=False));print('B20517-object/25-command source/current binding prepared against own registered V6160 opening.')
