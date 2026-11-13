"""Verify connected original item-cache transfers, not raw SLACK display."""
import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
)

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine

ROM = Path('out/all_routes_combined_v546_candidate.nds')
CAPTURE = Path('E:/Rota Nova translations/Generated/work/emulation_v193/legacy_descriptor_v547')
ROOT = Path('work/analysis/scratch_consumers_v548')
BASE, BUFFER, OWNER = 0x02000000, 0x02233040, 0x022857AC
OPEN, READ, SEEK, CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    digest = sha(ROM.read_bytes())
    assert digest == '499e0ad767b1badf899ab6873ad787f171651035c7d6316012af2b8afc8c77d3'
    arm, original = rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    ranges = [(0x47608,0x478D0),(0x47DE8,0x47F88),(0xD0170,0xD026C),(0xE2974,0xE29AC)]
    assert all(arm[a:b] == original[a:b] for a,b in ranges)
    snapshot = (CAPTURE/'frame_002400_arm9_ram.bin').read_bytes()
    assert len(snapshot) == 0x400000
    report = json.loads((CAPTURE/'capture_report.json').read_text(encoding='utf-8'))
    assert report['ROM_sha256'] == digest and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report.get('battery_save_preloaded')
    data = rom.read_file('/_pxl/item.pxl')
    assert data == clean.read_file('/_pxl/item.pxl')
    image = PxlImage.from_bytes(data)
    assert (image.width,image.height,image.pixels_offset) == (32,6976,532)
    u = machine(arm)
    u.mem_write(BASE,snapshot)
    headers = OWNER+0x82CC
    descriptions = []
    for slot in range(16):
        header = headers+20*slot
        words = struct.unpack('<5I',u.mem_read(header,20))
        assert words[:3] == (8,16,32)
        destination = (header+words[4])&0xFFFFFFFF
        assert destination == OWNER+0x2CC+slot*2048
        descriptions.append({'slot':slot,'header':header,'words':list(words),'pixel_pointer':destination})
    handles, events, buffer_reads = {}, [], []

    def bridge(uc,address,size,_):
        if address == 0x020E5650:
            raise ValueError('Native loader assertion')
        if address not in (OPEN,READ,SEEK,CLOSE):
            return
        obj = uc.reg_read(UC_ARM_REG_R0)
        if address == OPEN:
            name = bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_R1),128)).split(b'\0')[0].decode('ascii')
            path = '/'+name.replace('\\','/').lstrip('/')
            assert path == '/_pxl/item.pxl' and obj not in handles
            handles[obj] = 0
            uc.mem_write(obj+0x20,struct.pack('<2I',0,len(data)))
            events.append({'operation':'open','path':path})
            result = 1
        elif address == SEEK:
            offset = uc.reg_read(UC_ARM_REG_R1)
            assert uc.reg_read(UC_ARM_REG_R2) == 0 and 0 <= offset <= len(data)
            handles[obj] = offset
            events.append({'operation':'seek','offset':offset})
            result = 1
        elif address == READ:
            target, count = uc.reg_read(UC_ARM_REG_R1),uc.reg_read(UC_ARM_REG_R2)
            start = handles[obj]
            assert start+count <= len(data)
            uc.mem_write(target,data[start:start+count])
            handles[obj] += count
            events.append({'operation':'read','offset':start,'bytes':count,'destination':target})
            result = count
        else:
            del handles[obj]
            events.append({'operation':'close'})
            result = 1
        uc.reg_write(UC_ARM_REG_R0,result)
        uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))

    def observe(uc,access,address,size,value,_):
        if BUFFER <= address < BUFFER+1024:
            buffer_reads.append((uc.reg_read(UC_ARM_REG_PC),address,size))

    h1 = u.hook_add(UC_HOOK_CODE,bridge)
    h2 = u.hook_add(UC_HOOK_MEM_READ,observe)
    cases = []
    try:
        for index in range(218):
            for slot in range(16):
                # Clear native tag state to force an original reader/cache miss.
                call(u,0x47DE8,(OWNER+0x38,))
                destination = descriptions[slot]['pixel_pointer']
                u.mem_write(destination-16,b'\xA5'*1056)
                u.mem_write(BUFFER-16,b'\x5A'*1056)
                tags_before = bytes(u.mem_read(headers,320))
                bank_before = bytes(u.mem_read(OWNER+0x2CC,0x8000))
                start, read_start = len(events),len(buffer_reads)
                executed = call(u,0x47704,(OWNER,index,slot),instruction_limit=150000)
                expected = bytes(image.indices[index*1024:(index+1)*1024])
                assert bytes(u.mem_read(destination,1024)) == expected
                assert bytes(u.mem_read(BUFFER,1024)) == expected
                assert bytes(u.mem_read(destination-16,16)) == b'\xA5'*16
                assert bytes(u.mem_read(destination+1024,16)) == b'\xA5'*16
                assert bytes(u.mem_read(BUFFER-16,16)) == b'\x5A'*16
                assert bytes(u.mem_read(BUFFER+1024,16)) == b'\x5A'*16
                assert bytes(u.mem_read(headers,320)) == tags_before and not handles
                bank_after = bytes(u.mem_read(OWNER+0x2CC,0x8000))
                at = slot*2048
                assert bank_after[:at] == bank_before[:at]
                assert bank_after[at+1024:] == bank_before[at+1024:]
                tags_pointer = struct.unpack('<I',u.mem_read(OWNER+0x40,4))[0]
                tags = list(struct.unpack('<16I',u.mem_read(tags_pointer,64)))
                assert tags == [index if n == slot else 0xFFFFFFFF for n in range(16)]
                current = events[start:]
                assert [x['operation'] for x in current] == ['open','seek','read','close']
                assert current[1]['offset'] == 532+index*1024
                assert current[2] == {'operation':'read','offset':532+index*1024,'bytes':1024,'destination':BUFFER}
                observed = buffer_reads[read_start:]
                assert sum(x[2] for x in observed) == 1024
                assert {x[0] for x in observed} == {0x020E2988}
                assert {0x02047704,0x02047864,0x020E2974} <= executed
                previous = len(events),len(buffer_reads)
                call(u,0x47704,(OWNER,index,slot))
                assert previous == (len(events),len(buffer_reads))
                assert bytes(u.mem_read(destination,1024)) == expected
                cases.append({'index':index,'slot':slot,'source_offset':532+index*1024,
                              'destination':destination,'pixel_sha256':sha(expected),
                              'connected_reader_transfer_full_return_ABI_and_canaries':True,
                              'repeat_cache_hit_skips_file_and_buffer_read':True,
                              'entire_other_cache_pixel_bank_and_all_headers_unchanged':True,
                              'only_selected_native_slot_tag_matches_item':True})
    finally:
        u.hook_del(h1)
        u.hook_del(h2)
    main = MainCodeFile(arm,rom.rom.arm9RamAddress)
    literals = []
    for section in main.sections:
        literals += [section.ramAddress+i for i in range(0,len(section.data)-3,4)
                     if struct.unpack_from('<I',section.data,i)[0] == BUFFER]
    overlays = loadOverlayTable(rom.rom.arm9OverlayTable,lambda oid,fid:rom.rom.files[fid])
    overlay_refs = []
    for oid,overlay in overlays.items():
        overlay_refs += [{'overlay':oid,'address':overlay.ramAddress+i}
                         for i in range(0,len(overlay.data)-3,4)
                         if struct.unpack_from('<I',overlay.data,i)[0] == BUFFER]
    proof = {'candidate':str(ROM),'candidate_sha256':digest,'ROM_changed':False,
             'original_code_ranges_exact':ranges,'current_native_snapshot':str(CAPTURE/'frame_002400_arm9_ram.bin'),
             'snapshot_sha256':sha(snapshot),'actual_captured_item_cache_owner':OWNER,
             'captured_16_native_headers':descriptions,'source_file_sha256':sha(data),
             'all3488_reader_to_cache_misses':cases,'all3488_repeat_hits_verified':True,
             'original_copy_direction':'r0 is source; r1 is destination at020E2974',
             'all_main_aligned_BUFFER_literal_locations':literals,'ARM9_overlay_aligned_literals':overlay_refs,
             'scope':'Original full transfer routine and native captured headers, with supplied item/slot inputs and SDK filesystem bridge; no GPU or natural acquisition credit.',
             'no_SLACK_colour_binding_or_global_unused_claim':True,'all22_requirements_and18_incomplete_entries_retained':True,
             'full_goal_complete':False}
    (ROOT/'transfer_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('3488 original connected item-cache transfers and repeat hits pass; scratch buffer consumers distinguished; V546 unchanged.')


if __name__ == '__main__':
    main()
