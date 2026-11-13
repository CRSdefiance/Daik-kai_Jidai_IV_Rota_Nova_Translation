"""Original progressive-name style11,read directly from the unmodified current caller."""
import inspect
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_name_catalog_glyphs_v278 import raster as inherited_raster
from scripts.source_locked_derivation_v5118 import checked_text
ARM9='4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351'
def style_source_proof(arm):
    assert sha(arm)==ARM9;clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');start,end=0x54270,0x542A0;code=arm[start:end];assert code==clean[start:end]
    instructions=[dict(address=i.address,mnemonic=i.mnemonic,operands=i.op_str) for i in Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(code,0x02000000+start)]
    by={r['address']:r for r in instructions}
    assert (by[0x02054270]['mnemonic'],by[0x02054270]['operands'])==('add','r0, sp, #0x1f8')
    assert (by[0x0205427C]['mnemonic'],by[0x0205427C]['operands'])==('bl','#0x20d5160')
    assert (by[0x02054280]['mnemonic'],by[0x02054280]['operands'])==('mov','r1, #0xb')
    assert (by[0x02054288]['mnemonic'],by[0x02054288]['operands'])==('str','r1, [sp, #0x228]')
    assert (by[0x0205428C]['mnemonic'],by[0x0205428C]['operands'])==('bl','#0x207ed88')
    assert (by[0x02054294]['mnemonic'],by[0x02054294]['operands'])==('add','r0, sp, #0x1f8')
    assert (by[0x02054298]['mnemonic'],by[0x02054298]['operands'])==('bl','#0x20d5404')
    assert 0x228-0x1F8==48
    return dict(original_current_and_clean_name_caller_hex=code.hex(),instructions=instructions,source_name_getter=0x0207ED88,source_name_painter=0x020D5404,source_name_context_style_field_offset=48,source_name_style=11,style11_CP932_shadow_zero_not_style1_white_shadow=True,no_code_font_name_palette_or_native_guard_change=True)
source=inspect.getsource(inherited_raster)
source=checked_text(source,{'call(cpu, 0xD5160, (ctx, view, 1))':'call(cpu, 0xD5160, (ctx, view, 1))\n    cpu.mem_write(ctx + 48, struct.pack("<I", 11))'})
namespace=dict(inherited_raster.__globals__);exec(compile(source,__file__+'::original-style11-name-plane','exec'),namespace)
_raster=namespace['raster']
def native_name_raster(arm,text,**kwargs):
    style_source_proof(arm)
    result=_raster(arm,text,**kwargs);assert all(e['style']==11 for e in result[1]);return result
NATIVE_NAME_RASTER_SOURCE=source
