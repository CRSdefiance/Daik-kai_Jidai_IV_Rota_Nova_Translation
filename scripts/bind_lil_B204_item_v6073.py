"""Bind the clean cultural-object name and current item116 field without title invention."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,POOL,cstring
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B204_item_fields_v6073')
SOURCE=Path('work/analysis/lil_B204_source_v6062/all20_clean_current_complete_context.json')
CONTROL=Path('work/analysis/lil_B204_controls_v6069/six_exact_leaves_picture47xx_two43xx_one_A000_structural_pairs_and_guarded_end.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,control=map(read,[SOURCE,CONTROL]);clean,current=[NdsImage.open(p).read_file('/__arm9__.bin') for p in ['work/clean.nds',packet['current_ROM']]]
    payload=bytes(MainCodeFile(current,BASE).sections[3].data[:-48]);assert len(payload)==123040 and current.count(payload)==1
    field=0x11E210+116*24;sp,cp=[struct.unpack_from('<I',a,field)[0] for a in [clean,current]];src=cstring(clean,sp-BASE)
    if POOL<=cp<POOL+len(payload):off=cp-POOL;value=cstring(payload,off);at=current.index(payload)+off;storage='verified-staged-payload'
    else:at=cp-BASE;value=cstring(current,at);storage='original-static-ARM9'
    descriptor=control['source_one_picture_pair'][0]['cases'][0]['original_picture_boundary_calls'][0]
    assert descriptor['descriptor']==[0,116,1,5] and descriptor['layout']==[3,1,1]
    assert src[:-1].decode('cp932')=='シャチホコ' and all('シャチホコ' in next(r for r in packet['records'] if r['source_record_index']==i)['source_Japanese'] for i in [52,55])
    ROOT.mkdir(parents=True);save(ROOT/'clean_item116_current_name_and_original_picture_descriptor.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        item_ID=116,pointer_field=field,source_pointer=sp,source_storage_offset=sp-BASE,source_terminated_hex=src.hex(),Japanese=src[:-1].decode('cp932'),current_pointer=cp,current_storage_offset=at,current_storage=storage,current_terminated_hex=value.hex(),current_English=value[:-1].decode('cp932'),source_complete_static_item_row_hex=clean[field:field+24].hex(),
        original_picture_descriptor=descriptor,cultural_term_spoken_source_indices=[52,55],Jam_figurehead_claim_does_not_establish_correct_castle_ornament_use=True,actual_widget_cultural_term_localization_and_full_effects_not_yet_reviewed=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTROL,Path(__file__)]},new_review_credit=0,full_goal_complete=False))
    print(src[:-1].decode('cp932'),value[:-1].decode('cp932'))
