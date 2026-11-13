"""Source-reviewed Market investment/error replies with generated guarded lines."""

import struct
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.shop_business_editorial import compile_paragraph
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import (
    DIRECTORY_OFFSET,
    TABLE_OFFSET,
    common_message_entries,
)
from scripts.verify_village_wrap_v608 import read

IDS = (747,748,749,753,762,763,764,765,766)
DIRECTORY = 'f57f08bd6869b3927d8e6be154f6d9eb90147f7b28e97c4afc3bebc32aa40e25'


def transform(common, arm, manuscript):
    assert manuscript['translation_policy'] == 'natural-dialogue-v2'
    validate_natural_dialogue_batch(manuscript)
    assert tuple(r['message_id'] for r in manuscript['records']) == IDS
    path = '/COMMON/MESFILE.DK4'
    clean = NdsImage.open('work/clean.nds')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    assert sha(clean.read_file(path)) == manuscript['source_clean_COMMON_sha256']
    assert sha(canonical.read_file(path)) == manuscript['source_canonical_COMMON_sha256']
    source = common_message_entries(clean.read_file(path),clean.read_file('/__arm9__.bin'))
    accepted = common_message_entries(canonical.read_file(path),canonical.read_file('/__arm9__.bin'),clean=False)
    before = common_message_entries(common,arm,clean=False)
    blocks = IlnkContainer.parse(common).blocks
    authored = {}
    for row in manuscript['records']:
        number = row['message_id']
        assert source[number].text == bytes.fromhex(row['source_hex'])
        assert accepted[number].text == bytes.fromhex(row['canonical_source_hex'])
        assert before[number].text == bytes.fromhex(row['current_text_hex'])
        assert b'%' not in source[number].text
        authored[number] = compile_paragraph(row['english'])[0]
    # Same complete-selection/NUL relocation contract as Refit help V707/V708.
    # Unselected text bytes, including752 and every already reviewed message,
    # remain exact. Only bytes preceding native starts are discarded.
    selected = [e for e in before if 7 <= e.block <= 10]
    assert [e.message_id for e in selected] == list(range(545,855))
    groups,body,group = [],bytearray(),[]
    for entry in selected:
        text = authored.get(entry.message_id,entry.text)+b'\0'
        if len(body)+len(text)>4096:
            groups.append((group,bytes(body)))
            body,group = bytearray(),[]
        group.append((entry.message_id,len(body),text))
        body.extend(text)
    groups.append((group,bytes(body)))
    assert len(groups)==4
    rebuilt = list(blocks)
    target_arm = bytearray(arm)
    fields,mappings = [],[]
    for block,(group,raw) in zip(range(7,11),groups,strict=True):
        assert len(raw)<=4096
        rebuilt[block]=raw
        field=DIRECTORY_OFFSET+block*4
        struct.pack_into('<HH',target_arm,field,group[0][0],len(raw))
        fields.append((field,4))
        for number,offset,text in group:
            field=TABLE_OFFSET+number*2
            struct.pack_into('<H',target_arm,field,offset)
            fields.append((field,2))
            mappings.append({'message_id':number,'block':block,'offset':offset,'text_hex':text[:-1].hex()})
    target_arm=bytes(target_arm)
    target_common=IlnkContainer(rebuilt).to_bytes()
    assert sha(target_arm[DIRECTORY_OFFSET:TABLE_OFFSET])==DIRECTORY
    after = common_message_entries(target_common,target_arm,clean=False)
    for a,b in zip(before,after,strict=True):
        assert a.message_id == b.message_id
        assert b.text == authored.get(a.message_id,a.text)
    assert all(a==b for i,(a,b) in enumerate(zip(blocks,rebuilt,strict=True)) if i not in (7,8,9,10))
    restored = bytearray(target_arm)
    for at,size in fields:restored[at:at+size]=arm[at:at+size]
    assert bytes(restored)==arm and len(target_arm)==len(arm)
    assert cache_plan(target_arm)==cache_plan(arm)
    return target_common,target_arm,{'changed_records':[f'COMMON_MESSAGE_{i}' for i in IDS],
        'owned_ARM9_metadata_fields':fields,'native_directory_sha256':DIRECTORY,
        'repacked_native_IDs':mappings,
        'block_groups':[{'block':b,'first_id':g[0][0],'last_id':g[-1][0],'bytes':len(raw)} for b,(g,raw) in zip(range(7,11),groups,strict=True)],
        'all_other3659_message_text_bytes_and37_blocks_exact':True,
        'original3668_IDs41_blocks4096_byte_cache_limits_preserved':True,
        'no_executable_font_pool_startup_or_allocator_change':True,'experimental':True,'full_goal_complete':False}


def apply_release(common,arm,config_path):
    config=read(config_path)
    assert config['format'] == 'dk4-market-replies-editorial-v1'
    assert sha(common) == config['source_common_sha256'] and sha(arm) == config['source_arm9_sha256']
    manuscript=Path(config['manuscript'])
    assert sha(manuscript.read_bytes()) == config['manuscript_sha256']
    for path,digest in config['dependencies'].items():
        assert sha(Path(path).read_bytes()) == digest
    common,arm,proof=transform(common,arm,read(manuscript))
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    return common,arm,proof
