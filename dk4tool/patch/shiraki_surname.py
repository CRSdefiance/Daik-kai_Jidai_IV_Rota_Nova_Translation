"""Restore the complete source surname in its original fixed eight-byte slot."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

OFFSET=0x15BFD8
SOURCE=bytes.fromhex('83568389834c0000')
OLD=b'Shira\0\0\0'
NEW=b'Shiraki\0'


def transform(arm):
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert clean[OFFSET:OFFSET+8]==SOURCE
    assert SOURCE.split(b'\0')[0].decode('cp932')=='シラキ'
    assert arm[OFFSET:OFFSET+8]==OLD
    result=arm[:OFFSET]+NEW+arm[OFFSET+8:]
    assert len(result)==len(arm)
    assert [i for i,(a,b)in enumerate(zip(arm,result))if a!=b]==[OFFSET+5,OFFSET+6]
    return result,{'changed_records':['NPC_SURNAME_SHIRAKI'],
                   'original_Japanese':'シラキ','old_incomplete_English':'Shira',
                   'complete_English':'Shiraki','original_slot':[OFFSET,8],
                   'changed_bytes':[OFFSET+5,OFFSET+6],
                   'fixed_slot_extent_pointer_layout_and_all_other_bytes_preserved':True,
                   'first_NUL_moves_from_slot_byte5_to7_within_the_same_slot':True,
                   'terminal_in_slot_NUL_preserved':True,
                   'code_allocation_or_pool_growth':0,'status':'experimental',
                   'native_and_actual_name_caption_checks_required':True}


def apply_release(arm,path):
    config=json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format']=='dk4-shiraki-surname-v1'
    assert sha(arm)==config['source_arm9_sha256']
    result,report=transform(arm)
    assert sha(result)==config['target_arm9_sha256']
    return result,report
