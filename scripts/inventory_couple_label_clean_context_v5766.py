"""Bind the screenshot tea request to all four clean route copies and complete exchanges."""
from dataclasses import asdict
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/couple_label_clean_context_v5766')
if __name__=='__main__':
    assert not ROOT.exists();clean=Path('work/clean.nds');im=NdsImage.open(clean);arm=im.read_file('/__arm9__.bin')
    inventory,walker,invsource=scoped_inventory();versions=[]
    for route,number in [(0,196),(1,188),(2,184),(3,157)]:
        path=f'/data/SC{route}.DK4';data=im.read_file(path);block=IlnkContainer.parse(data).blocks[number]
        commands,speeches=inventory(arm,block);records=[]
        for speech in speeches:
            at=speech['offset']+5;end=block.index(0,at+1);raw=block[at:end]
            records.append(dict(source_record_index=block[:at].count(b'\0'),source_selector=raw[0],source_hex=raw.hex(),
                complete_preamble_hex=block[at-5:at+1].hex(),Japanese=raw[1:].decode('cp932'),
                source_reference=dict(file_path=path,block=number,header_offset=at-5,offset=at,bytes=len(raw))))
        tea=[r for r in records if 'うちのお茶' in r['Japanese']]
        assert len(tea)==1 and tea[0]['source_selector']==165
        versions.append(dict(route=route,file_path=path,source_file_sha256=sha(data),block=number,
            source_block_sha256=sha(block),source_block_hex=block.hex(),all_native_commands=commands,records=records,tea_record=tea[0]))
    fields=[]
    for ident,expected in [(164,'カップル男'),(165,'カップル女')]:
        at=0x122000+(ident-164)*32;parts=[]
        for delta in [0,4,8]:
            field=at+delta;pointer=struct.unpack_from('<I',arm,field)[0]
            if pointer:
                start=pointer-0x02000000;raw=arm[start:arm.index(0,start)+1]
                parts.append(dict(pointer_field=field,pointer=pointer,storage_offset=start,terminated_hex=raw.hex(),Japanese=raw[:-1].decode('cp932')))
            else:parts.append(dict(pointer_field=field,null=True))
        assert parts[0]['Japanese']==expected
        fields.append(dict(actor_ID=ident,source_file='/__arm9__.bin',source_fields=parts))
    ROOT.mkdir(parents=True)
    save(ROOT/'four_complete_clean_route_exchanges_and_exact_couple_name_fields.json',dict(
        source_ROM=str(clean),source_ROM_sha256=sha(clean.read_bytes()),clean_ARM9_sha256=sha(arm),
        source_name_fields=fields,versions=versions,clean_inventory_walker=walker,clean_inventory_function=invsource,
        screenshot_tea_request_found_in_SC0B196_SC1B188_SC2B184_SC3B157_not_COMMON=True,
        source_0xA5_is_executable_speaker_selector_not_a_halfwidth_text_dot=True,
        couple_role_supported_by_clean_fields_but_marriage_or_age_not_inferred=True,
        complete_exchange_gloss_all_other_actor164_165_uses_current_name_consumers_and_localization_decisions_pending=True,
        no_old_English_dialogue_used_as_translation_source=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    for v in versions:
        print(v['file_path'],'B'+str(v['block']),'commands',len(v['all_native_commands']),'speeches',len(v['records']))
    for r in versions[2]['records']:print(r['source_record_index'],format(r['source_selector'],'02X'),r['Japanese'].replace('\n',' / '))
