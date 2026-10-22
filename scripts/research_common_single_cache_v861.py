"""Prospective cache/packing proof only;does not build or register a ROM."""

import struct
from pathlib import Path

from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from ndspy.code import MainCodeFile,loadOverlayTable

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.common_single_cache_v861 import CACHE_AT,ORIGINAL,SINGLE,patch_cache,entries,repack
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET,TABLE_OFFSET
from scripts.planning_finance_layout_v860 import compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/common_single_cache_v861')
ROM=Path('out/all_routes_combined_v855_candidate.nds')


def main():
    ROOT.mkdir(parents=True,exist_ok=True);assert not (ROOT/'prospective_repack.json').exists()
    rom=NdsImage.open(ROM);common,arm=rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin')
    doc=read('translations/planning_finance_editorial_manuscript_v2.json');assert sha(ROM.read_bytes())==doc['current_ROM_sha256']
    authored={r['message_id']:compiled(r) for r in doc['records']}
    before,blocks,first,last,selected,opaque,groups,attempts=repack(common,arm,authored)
    policy=patch_cache(arm);target=bytearray(policy);rebuilt=list(blocks);fields=[]
    for b,(group,body) in zip(range(first,last+1),groups,strict=True):
        rebuilt[b]=body;at=DIRECTORY_OFFSET+b*4;struct.pack_into('<HH',target,at,group[0][0],len(body));fields.append((at,4))
        for n,offset,payload in group:
            at=TABLE_OFFSET+n*2;struct.pack_into('<H',target,at,offset);fields.append((at,2))
    c,a=IlnkContainer(rebuilt).to_bytes(),bytes(target);directory=sha(a[DIRECTORY_OFFSET:TABLE_OFFSET])
    after=entries(c,a,directory)
    assert all(y.text==authored.get(x.message_id,x.text) for x,y in zip(before,after,strict=True))
    assert all(blocks[b]==rebuilt[b] for b in range(41) if not first<=b<=last)
    for n,payload in opaque.items():
        e=after[n];assert rebuilt[e.block][e.block_offset:e.copy_end]==payload
    restored=bytearray(a)
    for at,size in fields:restored[at:at+size]=arm[at:at+size]
    assert bytes(restored)==policy;restored[CACHE_AT:CACHE_AT+8]=ORIGINAL;assert bytes(restored)==arm
    old,new=MainCodeFile(arm,0x02000000),MainCodeFile(a,0x02000000)
    assert [(s.ramAddress,len(s.data),s.bssSize) for s in old.sections]==[(s.ramAddress,len(s.data),s.bssSize) for s in new.sections]
    assert old.sections[3].data==new.sections[3].data and len(new.sections[3].data)-48==123040
    assert cache_plan(a)==cache_plan(arm)
    cs=Cs(CS_ARCH_ARM,CS_MODE_ARM);references=[];literal=[]
    spans=[('ARM9',0x02000000,arm)]
    for oid,overlay in loadOverlayTable(rom.rom.arm9OverlayTable,lambda oid,fid:rom.rom.files[fid]).items():spans.append((f'overlay{oid}',overlay.ramAddress,bytes(overlay.data)))
    for name,base,data in spans:
        for offset in range(0,len(data)-3,4):
            word=struct.unpack_from('<I',data,offset)[0]
            if (word>>25)&7==5:
                displacement=(word&0xFFFFFF)*4
                if displacement&0x2000000:displacement-=0x4000000
                dest=(base+offset+8+displacement)&0xFFFFFFFF
                if 0x020535E0<=dest<0x02053628 and not 0x020535E0<=base+offset<0x02053628:
                    references.append({'surface':name,'address':base+offset,'target':dest})
            if 0x020535E0<=word<0x02053628 or 0x020535E0<=word-1<0x02053628:literal.append({'surface':name,'at':base+offset,'word':word})
    assert references==[{'surface':'ARM9','address':0x02053514,'target':0x020535E0}],references
    assert not literal,literal
    for name,data in [('code_only_ARM9.bin',policy),('target_ARM9.bin',a),('target_COMMON.bin',c)]: (ROOT/name).write_bytes(data)
    save(ROOT/'prospective_repack.json',{'source_ROM':str(ROM),'source_ROM_sha256':sha(ROM.read_bytes()),
        'source_COMMON_sha256':sha(common),'source_ARM9_sha256':sha(arm),'code_only_ARM9_sha256':sha(policy),
        'target_COMMON_sha256':sha(c),'target_ARM9_sha256':sha(a),'directory_sha256':directory,
        'repacked_block_range':[first,last],'target_block_lengths':[len(rebuilt[b]) for b in range(first,last+1)],
        'old_cache_input_span':[0x30,0x2030],'old_two_slots4096_each':True,'new_single_slot8192_same_span':True,
        'output_span_unchanged':[0x2030,0x2230],'changed_cache_code_span':[CACHE_AT,CACHE_AT+8],
        'old_cache_code_hex':ORIGINAL.hex(),'new_cache_code_hex':SINGLE.hex(),
        'new_instructions':[i.mnemonic+' '+i.op_str for i in cs.disasm(SINGLE,0x02000000+CACHE_AT)],
        'bounded_ARM9_overlay_call_census':references,'literal_references':literal,
        'all3668_complete_strings_match_expected_and_all3644_unselected_exact':True,
        'all_unselected_blocks_and_opaque_payloads_exact':True,'metadata_fields':fields,'attempts':attempts,
        'all_other_ARM9_bytes_restored_exactly_after_owned_metadata_and8_cache_bytes':True,
        'all_sections_BSS_startup_name_cache_arena_and123040_staged_bytes_exact':True,
        'no_prose_shortening_or_unreviewed_padding_changes':True,
        'native_full_copies_boundary_tests_actual_boot_scenes_registration_and_patch_pending':True,
        'source_ROM_and_current_ledger_candidate_unchanged':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Research packing fits full prose in existing block',first,'size',len(rebuilt[first]),'using the same8KiB input allocation. Native/actual gates remain.',flush=True)


if __name__=='__main__':main()
