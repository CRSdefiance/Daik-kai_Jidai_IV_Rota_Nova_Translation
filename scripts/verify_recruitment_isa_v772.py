"""Audit the compiled executed Thumb ranges for ARM946 instruction support."""

from pathlib import Path

from capstone import CS_ARCH_ARM,CS_MODE_THUMB,Cs

from dk4tool.patch.grand_race_menu_release import sha
from scripts import recruitment_owned_runtime_v772 as runtime
from scripts.recruitment_quantity_v772 import assemble as quantity
from scripts.verify_recruitment_owned_v772 import ROOT
from scripts.verify_village_wrap_v608 import save


def main():
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);blobs=runtime.assemble();rows=[]
    parts=[(runtime.GATE,blobs[runtime.GATE][:-32]),(runtime.STATUS,blobs[runtime.STATUS][:-8]),
        (runtime.STATUS_TAIL,blobs[runtime.STATUS_TAIL]),(runtime.COPY,blobs[runtime.COPY])]
    q=quantity();at=next(iter(q));body=q[at][12:];actual=[]
    for inst in cs.disasm(body,at+12):
        actual.append(inst)
        if inst.mnemonic=='pop' and 'pc' in inst.op_str:break
    assert actual[-1].mnemonic=='pop' and 'pc' in actual[-1].op_str
    parts.append((at+12,body[:sum(i.size for i in actual)]))
    for at,blob in parts:
        instructions=list(cs.disasm(blob,at));assert sum(i.size for i in instructions)==len(blob)
        for inst in instructions:
            assert inst.size==2 or inst.size==4 and inst.mnemonic in('bl','blx')
            assert inst.mnemonic not in('it','cbz','cbnz','cps','rev','uxth','uxtb','sxth','sxtb','bkpt')
        rows.append({'address':at,'bytes':len(blob),'instructions':[{'at':i.address,'mnemonic':i.mnemonic,
            'operands':i.op_str,'hex':i.bytes.hex()} for i in instructions]})
    save(ROOT/'Thumb_ISA_audit.json',{'all_compiled_Thumb_code':rows,'only16bit_Thumb1_and_ARMv5_BL_BLX':True,
        'physical_hardware_verification':False,'runtime_source_sha256':sha(Path(runtime.__file__).read_bytes()),
        'quantity_source_sha256':sha(Path('scripts/recruitment_quantity_v772.py').read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print(f'{sum(len(r["instructions"]) for r in rows)} instructions audited;no Thumb2-only operations.',flush=True)


if __name__=='__main__':main()
