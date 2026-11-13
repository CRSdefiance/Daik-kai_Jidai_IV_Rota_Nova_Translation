"""Original154-ship initialization and81 bearings for two bounded source labels."""
from pathlib import Path
from types import FunctionType
import struct
from PIL import Image
from ndspy.code import MainCodeFile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.sighting_labels_v1083b import apply,FIELDS
from scripts.prepare_item_ship_owner import prepare
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sighting_labels_v1083b')
ROM=Path('out/all_routes_combined_v1034_candidate.nds')


def main():
    assert not ROOT.exists()
    rt=read('work/analysis/sighting_runtime_v1076/native_runtime_verification.json')
    old_path=Path('work/analysis/sighting_layout_v1072/ARM9_RUNTIME_RESEARCH_ONLY.bin')
    old=old_path.read_bytes();assert sha(old)==rt['research_ARM9_sha256']
    new,plan=apply(old)
    source=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert source[0x15E0A4:0x15E0B4].split(b'\0')[0].decode('cp932')=='武装ラティーナ'
    table=struct.unpack_from('<I',old,0xCD3CC)[0]
    field=0x0211DB5C;assert (field-table)%44==0
    ship_index=50+(field-table)//44;assert 50<=ship_index<154
    assert struct.unpack_from('<I',old,field-0x02000000)[0]==0x0215E0A4
    initializers=[];tables=[]
    for arm in (old,new):
        cpu=machine(arm)
        receipt=prepare(arm,cpu,118,ship_index)
        root=struct.unpack_from('<I',arm,0xCB150)[0]
        values=bytes(cpu.mem_read(root+4,154*0x8C));tables.append(values)
        assert receipt['native_default_ship_initializers']==154 and receipt['native_fixed_source_names_checked']==104
        initializers.append(receipt)
    assert initializers[0]['name']=='武装Latina' and initializers[1]['name']=='Armed Latina'
    before,after=tables;at=ship_index*0x8C+8
    assert before[:at]==after[:at] and before[at+19:]==after[at+19:]
    assert after[at:at+13]==b'Armed Latina\0'
    root=read('work/analysis/sighting_editorial_v1065/source_context_packet.json')
    raw=Path(root['source_snapshot']).read_bytes();assert sha(raw)==root['source_snapshot_sha256']
    target_raw=bytearray(raw)
    for at,source_value,target_value in FIELDS:
        assert raw[at:at+len(source_value)]==source_value
        target_raw[at:at+len(target_value)]=target_value
    a,get_a=get_machine(old,raw);b,get_b=get_machine(new,bytes(target_raw));bearings=[]
    for x in (-100,-10,-2,-1,0,1,2,10,100):
        for y in (-100,-10,-2,-1,0,1,2,10,100):
            pa=get_a(0x6567C,x&0xFFFFFFFF,y&0xFFFFFFFF);pb=get_b(0x6567C,x&0xFFFFFFFF,y&0xFFFFFFFF)
            aa=bytes(a.mem_read(pa,64)).split(b'\0')[0];bb=bytes(b.mem_read(pb,64)).split(b'\0')[0]
            assert pa==pb and bb==(b'vicinity' if aa=='至近距離'.encode('cp932') else aa)
            bearings.append({'relative_vector':[x,y],'source_hex':aa.hex(),'target_hex':bb.hex(),'native_ABI':True})
    rom=NdsImage.open(ROM)
    class Font:
        @staticmethod
        def open(path):
            assert str(path)=='out/all_routes_combined_v255_candidate.nds'
            return rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':Font},argdefs=original_raster.__defaults__)
    ROOT.mkdir(parents=True);images=[]
    for label in ('Armed Latina','Enemy ship Armed Latina captured!'):
        value=b' '+label.encode('ascii')
        pixels=raster(new,value,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000)
        assert pixels==independent_font(new,rom.read_file('/GRP/KANJI.FNT'),[label])
        path=ROOT/('native_name.png' if label=='Armed Latina' else 'native_capture_notice.png')
        Image.frombytes('L',(228,64),bytes(0 if v else 255 for v in pixels)).save(path)
        images.append({'label':label,'preview':str(path),'preview_sha256':sha(path.read_bytes()),'complete_native_independent_font_plane_match':True})
    c,d=[MainCodeFile(v,0x02000000) for v in (old,new)]
    assert [(s.ramAddress,len(s.data),s.bssSize) for s in c.sections]==[(s.ramAddress,len(s.data),s.bssSize) for s in d.sections]
    assert all(c.sections[i].data==d.sections[i].data for i in (1,2,3,4)) and len(d.sections[3].data)-48==123040
    arm_path=ROOT/'ARM9_RUNTIME_AND_LABELS_RESEARCH_ONLY.bin';arm_path.write_bytes(new)
    save(ROOT/'native_label_proof.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'runtime_proof':'work/analysis/sighting_runtime_v1076/native_runtime_verification.json','runtime_proof_sha256':sha(Path('work/analysis/sighting_runtime_v1076/native_runtime_verification.json').read_bytes()),
        'runtime_only_ARM9':str(old_path),'runtime_only_ARM9_sha256':sha(old),'research_ARM9':str(arm_path),'research_ARM9_sha256':sha(new),
        'label_plan':plan,'source_ship_name':'武装ラティーナ','source_meaning':'Armed version of the established Latina ship class.',
        'default_fixed_ship_index':ship_index,'original_metadata_pointer_field':field,'original_name_field_address':0x0215E0A4,
        'original_default_initializers_source_and_target':initializers,'all153_other_initialized_ship_records_exact':True,
        'all_selected_ship_bytes_except_owned19_byte_name_field_exact':True,'complete_Armed_Latina_and_NUL_survive_original_initializer':True,
        'all81_bearing_getter_ABI_cases':bearings,'native_font_previews':images,
        'all_sections_BSS_cache_and_entire123040_staged_payload_unchanged':True,
        'native_context_source_labels_only_no_actual_acquisition_or_live_RAM_change':True,
        'native_repack_copy_registered_ROM_patch_and_actual_display_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Original154-ship initialization preserves153 other records;complete Armed Latina and81 bearing cases pass. Two native-font previews pending.',flush=True)


if __name__=='__main__':main()
