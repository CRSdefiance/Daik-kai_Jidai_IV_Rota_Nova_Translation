"""Bind linguistic anchors with fresh current native lookups, not an unrelated whole-ARM9 equality."""
import re
import struct
from pathlib import Path
from unicorn.arm_const import UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_R1,UC_ARM_REG_SP
from dk4tool.patch.confirmed_name_message_catalog import CALLS,MACRO
from dk4tool.patch.main_pool_cache_visibility import BASE
from scripts.source_locked_derivation_v5118 import checked_text

def current_anchor_lookup(ctx,body,expected):
    cpu,_,_=ctx.machine(ctx.arm,ctx.common,ctx.raw,ctx.plan)
    instruction=struct.unpack_from('<I',ctx.arm,CALLS[0])[0];assert instruction>>24==0xEB
    delta=(instruction&0xffffff)<<2
    if delta&0x2000000:delta-=0x4000000
    entry=BASE+CALLS[0]+8+delta;at=0x02468020;value=body[1:]
    cpu.mem_write(at-16,b'\xa5'*(len(value)+33));cpu.mem_write(at,value+b'\0')
    before=bytes(cpu.mem_read(at-16,len(value)+33))
    for reg,x in [(UC_ARM_REG_R1,at),(UC_ARM_REG_LR,BASE+CALLS[0]+4),(UC_ARM_REG_SP,0x027f0000)]:cpu.reg_write(reg,x)
    cpu.emu_start(entry,MACRO,count=1000000);assert cpu.reg_read(UC_ARM_REG_PC)==MACRO
    chosen=cpu.reg_read(UC_ARM_REG_R1);effective=bytes(cpu.mem_read(chosen,1024)).split(b'\0')[0]
    assert len(effective)<1024 and bytes(cpu.mem_read(at-16,len(value)+33))==before
    paragraph=' '.join(effective.decode('cp932').split())
    target=re.sub(r'\{MACRO:(FI|FA|FO|FU)\}',r'\1',expected)
    assert paragraph==target,(paragraph,target)
    assert bytes(cpu.mem_read(ctx.actor_root,0x1a04))==ctx.actor_bytes;ctx.calls.clear()
    return dict(current_effective_hex=effective.hex(),current_comparison_paragraph=paragraph,
        catalogue_selected=chosen!=at,original_current_lookup_andinput_actor_guards_pass=True,
        old_ARM9_not_used_as_new_runtime_orfont_proof=True)

source=checked_text(Path('scripts/bind_maria330_registered_story_terms_v1.py').read_text(encoding='utf-8'),{
    "image=NdsImage.open(prior['target_ROM']);assert image.read_file('/__arm9__.bin')==ctx.arm and image.read_file('/COMMON/MESFILE.DK4')==ctx.common":
        "image=NdsImage.open(prior['target_ROM']);assert image.read_file('/COMMON/MESFILE.DK4')==ctx.common",
    "review=row['review'],exact_current_complete_block_sha256=sha(blocks[block])))":
        "review=row['review'],exact_current_complete_block_sha256=sha(blocks[block]),current_native_lookup=current_anchor_lookup(ctx,body,row['english'])))",
    "exact_unchanged_registered_anchors_reused_not_new_dictionary_research=True":
        "exact_unchanged_registered_anchors_reused_not_new_dictionary_research=True,unrelated_older_ARM9_equality_not_asserted=True,current_anchor_native_lookups=2",
    "[current_path,*paths,Path(__file__)]":"[current_path,*paths,Path(__file__),Path('scripts/bind_maria330_registered_story_terms_v1.py')]",
})
if __name__=='__main__':exec(compile(source,__file__+'::exact-stored-block-anchors-plus-fresh-current-native-consumer-not-old-ARM9','exec'),globals())
