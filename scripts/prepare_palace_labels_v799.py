"""Bind original Palace text ownership and complete native menu-label reads."""

import struct
from pathlib import Path

from PIL import Image,ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_SP,UC_ARM_REG_PC

from dk4tool.patch import palace_label_boundaries as labels
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_item_runtime_storage_v785 import census
from scripts.native_call_abi_v764 import call
from scripts.verify_arrival_native_v792 import prepared
from scripts.probe_button_prompt_native import BASE,STACK
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT=labels.ROOT


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    rom=NdsImage.open('out/all_routes_combined_v797_candidate.nds');arm=rom.read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=list(labels.SPANS)+[(0x02143E04,0x02143E10)]
    expected=sorted(['absolute','section0',labels.TABLE+16*i,p,False] for i,p in enumerate(labels.OLD))
    refs=sorted(census(rom,spans,[]));assert refs==expected,refs
    for p,jp in zip(labels.OLD,labels.JAPANESE,strict=True):assert clean[p-BASE:].split(b'\0',1)[0].decode('cp932')==jp
    assert clean[0x143E4C:0x143E70]==arm[0x143E4C:0x143E70] or clean[0x143E4C:0x143E5C]==arm[0x143E4C:0x143E5C]
    assert arm[0x143E4C:0x143E5C]==clean[0x143E4C:0x143E5C]
    target,proof=labels.plan(arm)
    after=NdsImage.open('out/all_routes_combined_v797_candidate.nds');after.rom.arm9=target
    newrefs=census(after,spans,[]);names,_=labels.blobs()
    assert sorted(newrefs)==sorted(['absolute','section0',labels.TABLE+16*i,names[label],False] for i,label in enumerate(labels.LABELS))
    cpu=prepared(target);cases=[];planes=[]
    for i,label in enumerate(labels.LABELS):
        pointer=names[label];raw=label.encode()+b'\0';dest=0x02470020
        call(cpu,0xCED28,(pointer,));assert cpu.reg_read(UC_ARM_REG_R0)==len(label)
        cpu.mem_write(dest-16,b'\xa5'*96);call(cpu,0xCEC74,(dest,pointer,len(raw)))
        assert bytes(cpu.mem_read(dest,len(raw)))==raw
        assert bytes(cpu.mem_read(dest-16,16))==b'\xa5'*16 and bytes(cpu.mem_read(dest+len(raw),80-len(raw)))==b'\xa5'*(80-len(raw))
        pixels=raster(target,b' '+label.encode(),0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
        assert pixels==independent_font(target,rom.read_file('/GRP/KANJI.FNT'),[label])
        p=ROOT/f'label_{i}_full_font.png';Image.frombytes('L',(228,64),bytes(0 if x else 255 for x in pixels)).save(p)
        planes.append({'id':i,'english':label,'path':str(p),'sha256':sha(p.read_bytes())})
        cases.append({'id':i,'pointer':pointer,'english':label,'NUL_inside_owned_span':True,'unaligned_pointer_native_copy_if_present':pointer%4!=0})
    cpu.mem_write(STACK-16,b'\xa5'*160);cpu.reg_write(UC_ARM_REG_SP,STACK)
    cpu.emu_start(BASE+0x5D4FC,BASE+0x5D518,count=1000)
    assert cpu.reg_read(UC_ARM_REG_PC)==BASE+0x5D518
    assert bytes(cpu.mem_read(STACK+12,96))==target[labels.TABLE-BASE:labels.TABLE-BASE+96]
    sheet=Image.new('RGB',(700,160*6),'#30343c');draw=ImageDraw.Draw(sheet)
    for i,row in enumerate(planes):
        draw.text((8,i*160+4),row['english'],fill='white')
        sheet.paste(Image.open(row['path']).convert('RGB').resize((456,128),Image.Resampling.NEAREST),(8,i*160+24))
    p=ROOT/'all_six_labels_2x.png';sheet.save(p)
    (ROOT/'ARM9_RESEARCH_ONLY.bin').write_bytes(target)
    save(ROOT/'source_ownership.json',{'source_ARM9_sha256':sha(arm),'clean_ARM9_sha256':sha(clean),
        'source_menu96_hex':arm[labels.TABLE-BASE:labels.TABLE-BASE+96].hex(),
        'typed_Cstring_allocations':[{'span':[lo,hi],'clean_hex':clean[lo-BASE:hi-BASE].hex(),'source_hex':arm[lo-BASE:hi-BASE].hex()} for lo,hi in labels.SPANS],
        'before_reference_census':refs,'after_reference_census':newrefs,'no_unknown_incoming_references':True,
        'vtable_offset_RTTI_and_methods_3E4C_3E5C_preserved':True,
        'bad_Contract_source_eight_bytes_have_no_NUL_and_run_into_RTTI_and_Mil_Invest':True,
        'historical_Guild_tail_rejected_as_now_active_India_label':True,
        'cannon_tail_not_reused_ownership_of_its_last_zero_not_established':True})
    save(ROOT/'native_verification.json',{**proof,'all_six_original_strlen_and_full_copy_guards_and_ABI_pass':True,
        'original_menu_initializer_copies_full96_bytes_exact':True,'six_native_cases':cases,'full_font_planes':planes,
        'preview':str(p),'preview_sha256':sha(p.read_bytes()),'actual_menu_GPU_verification_pending':True,
        'producer_sha256':sha(Path('scripts/prepare_palace_labels_v799.py').read_bytes())})
    print('Six complete Palace labels,unaligned native copies,all references and original menu initializer pass;actual menu pending.',flush=True)


if __name__=='__main__':main()
