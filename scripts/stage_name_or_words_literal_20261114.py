"""Use the registered literal formatter for the original COMMON 296 modal."""

from pathlib import Path
from struct import unpack_from

from keystone import KS_ARCH_ARM,KS_MODE_ARM,Ks
from ndspy.code import MainCodeFile

from scripts import stage_name_or_words_confirmation_20261114 as text_stage
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.verify_release_baseline import files

base,parent=text_stage.base,text_stage.parent
ROOT=Path("work/name_or_words_confirmation_20261114_v3")
ROM=ROOT/text_stage.ROM.name
STORED=ROOT/"staged.json"
ARM,COMMON,CLEAN,GATES,ID,DRAFT=(text_stage.ARM,text_stage.COMMON,text_stage.CLEAN,text_stage.GATES,text_stage.ID,text_stage.DRAFT)
BASE=0x02000000
START=0x01FFDBC0
END=0x01FFDC2C
FALLBACK=0x01FFDB54
PARAGRAPH=0x01FFD04C
LITERAL=0x01FFD0EC
OLD_PARENT=0x020546E8
YES_NO_PARENT=0x0205469C
EXISTING_IDS=(334,342,343,344,345)
OLD="9fb3518e967bb1d13ea496a90d354c3031c394491ad15ed15a4bb76f4fdccba0"


def select(arm):
    digest=parent.parent.parent.source.current.assets.edit.digest
    code=MainCodeFile(arm,BASE)
    assert bytes(code.save())==arm and len(code.sections)==6
    tail=code.sections[-1]
    assert tail.ramAddress==0x01FFD000 and len(tail.data)==0x2FFC and not tail.bssSize
    lo,hi=START-tail.ramAddress,END-tail.ramAddress
    old=bytes(tail.data[lo:hi])
    assert digest(old)==OLD
    assert unpack_from("<6I",old,0x54)==(OLD_PARENT,*EXISTING_IDS)
    assembler=Ks(KS_ARCH_ARM,KS_MODE_ARM)
    source=f"""
        ldr r3,[sp,#0xc4]
        ldr ip,={OLD_PARENT:#x}
        cmp r3,ip
        beq known_notices
        ldr ip,={YES_NO_PARENT:#x}
        cmp r3,ip
        bne {FALLBACK:#x}
        ldr r3,[sp,#0xd0]
        cmp r3,#296
        beq {LITERAL:#x}
        b {FALLBACK:#x}
    known_notices:
        ldr r3,[sp,#0xd0]
        ldr ip,=334
        cmp r3,ip
        beq {PARAGRAPH:#x}
        sub ip,r3,#340
        sub ip,ip,#2
        cmp ip,#3
        bls {PARAGRAPH:#x}
        b {FALLBACK:#x}
        .ltorg
    """
    payload=bytes(assembler.asm(source,START)[0])
    assert len(payload)<len(old) and len(payload)%4==0
    target=payload.ljust(len(old),b"\0")
    tail.data[lo:hi]=target
    revised=bytes(code.save())
    assert len(revised)==len(arm)
    rest=MainCodeFile(revised,BASE)
    rest.sections[-1].data[lo:hi]=old
    assert bytes(rest.save())==arm
    return revised,dict(start=START,end=END,original_hex=old.hex(),target_hex=target.hex(),code_bytes=len(payload),
        prior_message_scope=list(EXISTING_IDS),new_message_scope=[YES_NO_PARENT,296],
        unchanged_ITCM_extents=True,unchanged_native_literal=LITERAL,unchanged_prior_paragraph=PARAGRAPH,preserved_fallback=FALLBACK)


def main():
    assert not ROOT.exists()
    provenance=base.load(text_stage.STORED)
    parent_rom=base.load(parent.RELEASE)
    assert base.digest(text_stage.ROM)==provenance["candidate_sha256"]
    assert base.digest(parent.ROM)==parent_rom["candidate_sha256"]==provenance["previous_sha256"]
    image=base.NdsImage.open(text_stage.ROM)
    previous=base.NdsImage.open(parent.ROM)
    before,active=files(previous),files(image)
    assert {p for p in before if before[p]!=active[p]}=={COMMON}
    revised,selector=select(active[ARM])
    verify_runtime(revised,parent_rom)
    image.replace_file(ARM,revised)
    final=files(image)
    assert {p for p in before if before[p]!=final[p]}=={ARM,COMMON}
    ROOT.mkdir()
    image.save(ROM)
    image.replace_file(ARM,before[ARM])
    image.replace_file(COMMON,before[COMMON])
    assert bytes(image.rom.save())==parent.ROM.read_bytes()
    digest=parent.parent.parent.source.current.assets.edit.digest
    base.save(STORED,provenance|dict(candidate_sha256=base.digest(ROM),target_ARM9_sha256=digest(revised),
        literal_dispatch=selector,glyph_only_research_sha256=provenance["candidate_sha256"]))
    print("Reused the existing selector space and literal formatter. ARM9, COMMON and whole-ROM inverses pass.")


if __name__=="__main__":
    main()
