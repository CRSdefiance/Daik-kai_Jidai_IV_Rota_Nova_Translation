"""Verify complete packed sea-foam selections and guarded native word rasters."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_SP

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.probe_remaining_common_layout import warm_copy
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_repair_wait_native_v474 import scope
from scripts.verify_tavern_addresses_v413 import wrap

OUT = Path('work/analysis/sea_foam_family_v514')


def queued(arm, text, parent, argument, destination_only=False):
    u = machine(arm)
    u.mem_write(STACK+0x264,struct.pack('<I',parent))
    argument_offset=0x27c if parent==0x02053DB8 else 0x270
    u.mem_write(STACK+argument_offset,struct.pack('<I',argument))
    if destination_only:
        u.reg_write(UC_ARM_REG_SP,STACK)
        def stop(uc,address,size,data):
            if address in (0x01FFCF78,0x01FF9EDC): uc.emu_stop()
        handle=u.hook_add(UC_HOOK_CODE,stop)
        u.emu_start(0x01FFCF3C,0x01FFD000,count=100)
        u.hook_del(handle)
        assert u.reg_read(UC_ARM_REG_SP)==STACK
        return u.reg_read(UC_ARM_REG_PC)
    u.mem_write(0x02387A20,bytes(MainCodeFile(arm,0x02000000).sections[3].data[:-48]))
    source,output=0x0242C020,0x0242D020
    u.mem_write(source-16,b'\xA5'*16+text+b'\0'+b'\xA5'*16)
    u.mem_write(output-16,b'\xA5'*288)
    call(u,0x01FFCF3C-0x02000000,(output,source,0))
    assert bytes(u.mem_read(source,len(text)+1))==text+b'\0'
    assert bytes(u.mem_read(output-16,16))==bytes(u.mem_read(output+256,16))==b'\xA5'*16
    return bytes(u.mem_read(output,256)).split(b'\0',1)[0]


def main():
    parent = NdsImage.open('out/all_routes_combined_v508_candidate.nds')
    old_arm,old_common = parent.read_file('/__arm9__.bin'),parent.read_file('/COMMON/MESFILE.DK4')
    arm,common = (OUT/'target_arm9.bin').read_bytes(),(OUT/'target_common.bin').read_bytes()
    before = common_message_entries(old_common,old_arm,clean=False)
    after = common_message_entries(common,arm,clean=False)
    a,b = IlnkContainer.parse(old_common).blocks,IlnkContainer.parse(common).blocks
    assert len(a) == len(b) == 41
    assert all(len(x)==len(y)and x.count(b'\0')==y.count(b'\0')for x,y in zip(a,b))
    for e,f in zip(before,after):
        if not 457 <= e.message_id <= 480:
            assert e.text.rstrip() == f.text.rstrip(),e.message_id
    dispatch = []
    for parent_return in (0x02054014,0x02054044):
        changed = []
        for number in range(3668):
            x,y = scope(old_arm,parent_return,number),scope(arm,parent_return,number)
            if parent_return == 0x02054014 and 457 <= number <= 480:
                assert x[0] == 0x01FF9EDC and y[0] == 0x01FFCF78
                changed.append(number)
            else:
                assert x[0] == y[0],(parent_return,number,x,y)
        dispatch.append({'parent':parent_return,'all3668_destinations_compared':True,'newly_wrapped_ids':changed})
    tables = {0x02118840:range(457,463),0x02118820:range(463,469),
              0x02118800:range(470,477),0x02116730:range(477,481)}
    for table, numbers in tables.items():
        count=4 if table==0x02116730 else 8
        original_ids=struct.unpack_from('<'+str(count)+'I',arm,table-0x02000000)
        assert set(original_ids)-{0xffffffff}==set(numbers)
    table_scope=[]
    for argument in range(0x02116000,0x02119000,4):
        a=queued(old_arm,b'',0x02053DB8,argument,True)
        b=queued(arm,b'',0x02053DB8,argument,True)
        assert a==0x01FF9EDC
        assert b==(0x01FFCF78 if argument in tables else a)
        table_scope.append(argument)
    for number in range(3668):
        a=queued(old_arm,b'',0x02053C5C,number,True)
        b=queued(arm,b'',0x02053C5C,number,True)
        assert b==(0x01FFCF78 if 457<=number<=480 else a)
    for argument in range(0x02116000,0x02119000,4):
        a=queued(old_arm,b'',0x02053C14,argument,True)
        b=queued(arm,b'',0x02053C14,argument,True)
        assert b==(0x01FFCF78 if argument==0x02116730 else a)
    copies = [warm_copy(arm,common,n,after[n].text,cold_cache=cold)
              for n in [456,*range(457,481),481]for cold in (False,True)]
    page = Image.new('RGB',(684,8*104),'#dddddd')
    drawing = ImageDraw.Draw(page)
    cases = []
    for index,number in enumerate(range(457,481)):
        text = after[number].text.rstrip()
        formatted = wrap(arm,text,0x02054014,number)
        table=next((table for table,ids in tables.items()if number in ids),None)
        real_parent=0x02053C14 if table==0x02116730 else 0x02053DB8 if table else 0x02053C5C
        assert queued(arm,text,real_parent,table if table else number)==formatted
        assert b' '.join(formatted.split()) == b' '.join(text.split())
        events = []
        pixels = raster(arm,formatted,0x01FFCE40-0x02000000,size=(228,80),instruction_limit=1000000,glyph_events=events)
        decoded = text.decode('cp932')
        visible = [e for e in events if e['code']not in(32,10)]
        expected = [int.from_bytes(c.encode('cp932'),'big')for c in decoded if c not in(' ','\n')]
        assert [e['code']for e in visible] == expected,number
        offset = 0
        for word in decoded.split():
            group = visible[offset:offset+len(word)]
            assert len({e['y']for e in group}) == 1,(number,word)
            offset += len(word)
        assert all(0<=e['x']<228 and 0<=e['y']and e['y']+16<=80 for e in visible)
        image = Image.frombytes('L',(228,80),bytes(0 if p else 255 for p in pixels))
        image.save(OUT/f'message_{number}_native.png')
        x,y = (index%3)*228,(index//3)*104
        page.paste(image,(x,y+20))
        drawing.text((x+3,y+3),f'Native COMMON{number}',fill='black')
        cases.append({'message':number,'complete_English':decoded,'native_lines':formatted.decode('cp932').splitlines(),
                      'every_word_on_one_row_and_all_first_internal_final_glyphs_in_order':True,
                      'complete_native_ink_pixels':sum(bool(p)for p in pixels)})
    page.save(OUT/'complete_family_native_review.png')
    # The 20 added bytes were owned padding and remained zero in two genuine
    # parent-ROM cold-boot terminal states before this repair.
    padding = []
    for folder in ('tavern_family_v508_athens','tavern_family_v508_fresh'):
        path = Path('work/emulation_v193')/folder/'native_state/arm9_itcm.bin'
        tcm = path.read_bytes()
        assert tcm[0x4BEC:0x4C00] == bytes(20)
        assert tcm[0x4CD0:0x4D00]==bytes(48)
        assert tcm[0x4D98:0x4E00]==bytes(104)
        padding.append({'snapshot':str(path),'sha256':sha(tcm),'owned20_bytes_zero_in_parent':True})
    proof = {'target_arm9_sha256':sha(arm),'target_common_sha256':sha(common),
             'all3668_message_identities_and_all41_cache_sizes_NUL_counts_preserved':True,
             'all_unselected_visible_text_preserved':True,'dispatch':dispatch,
             'original_queued_voice_tables':{hex(k):list(v)for k,v in tables.items()},
             'queued_table_address_neighbors_checked':len(table_scope),
             'queued_numeric_all3668_dispatches_checked':True,
             'all24_actual_queued_parent_outputs_equal_reviewed_direct_outputs':True,
             'all52_cold_warm_neighbor_copies':copies,'all24_complete_native_rasters':cases,
             'parent_runtime_padding_witnesses':padding,
             'previews_are_native_supplied_text_rasters_not_gameplay':True,
             'registered_release_and_actual_replay_pending':True,'full_goal_complete':False}
    (OUT/'native_proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('All24 full source messages,52 cold/warm copies and7336 dispatch comparisons pass.')


if __name__ == '__main__':
    main()
