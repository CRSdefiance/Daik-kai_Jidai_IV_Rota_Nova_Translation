"""Preserve the source shield-rumor control/end without claiming anitem acquisition."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B228_control_tools_v7337')
if __name__=='__main__':
    assert not ROOT.exists()
    r=derive('scripts/prove_lil_B226_controls_v7243.py','scripts/prove_lil_B228_controls_v7337.py',{'B226':'B228','controls_v7243':'controls_v7337','source_v7240/twenty_clean_current_Attila_armor_exchange_source_references':'source_v7334/thirteen_clean_current_armadillo_shield_rumor_source_references','blocks[226]':'blocks[228]','len(block)==1196':'len(block)==760',"struct.unpack_from('<H',block,4)[0]==1194":"struct.unpack_from('<H',block,4)[0]==758",'block[1190:]':'block[754:]','len(commands)==22':'len(commands)==15',"[(1182,'00a0ffff45000110',8),(1190,'00000000',4)]":"[(746,'00a0ffff32000110',8),(754,'00000000',4)]",'original_offset=1182':'original_offset=746','block,1190,previous':'block,754,previous','source_stored1196_logical1194_tail2_complete_end1190_preserved':'source_stored760_logical758_tail2_complete_end754_preserved','no_confirmed_armor_discovery_ownership_location_or_gameplay_result_inferred':'no_confirmed_shield_discovery_ownership_location_or_gameplay_result_inferred','Original1196-byte':'Original760-byte'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_source_controls.json',r)
