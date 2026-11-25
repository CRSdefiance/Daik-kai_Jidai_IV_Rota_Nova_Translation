"""Successor regression proof including source PC-relative literal ownership."""
import inspect
import struct
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import escape_direct_runtime_v1183b as runtime
from scripts import verify_escape_direct_runtime_v1184 as prior
from scripts.inventory_shipyard_storage_v760 import units
from scripts.audit_item_runtime_storage_v785 import census
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/escape_direct_runtime_v1184b')


def literal_accesses(rom,spans):
    rows=[]
    for name,base,raw in units(rom)+[('ARM7',rom.rom.arm7RamAddress,bytes(rom.rom.arm7))]:
        for off in range(0,len(raw)-3,4):
            word=struct.unpack_from('<I',raw,off)[0];at=base+off
            # Original ARM immediate PC-relative loads/stores, either sign.
            if word&0x0F2F0000==0x050F0000:
                target=at+8+((word&4095) if word&0x800000 else -(word&4095))
                if any(lo<=target<hi for lo,hi in spans): rows.append(['ARM_PC_relative',name,at,target])
        for off in range(0,len(raw)-1,2):
            word=struct.unpack_from('<H',raw,off)[0];at=base+off
            if word&0xF800==0x4800:
                target=((at+4)&~3)+(word&255)*4
                if any(lo<=target<hi for lo,hi in spans): rows.append(['Thumb_PC_relative',name,at,target])
    return rows


def main():
    assert not ROOT.exists()
    rom=NdsImage.open(prior.ROM);old=rom.read_file('/__arm9__.bin')
    owned=read('work/analysis/recruitment_owned_v772/owned_runtime_plan.json')['private_spans']
    assert any(lo<=runtime.SUFFIX_SLOT and runtime.SUFFIX_SLOT+4<=hi for lo,hi in owned)
    assert census(rom,[(runtime.SUFFIX_SLOT,runtime.SUFFIX_SLOT+8)],[])==[]
    assert literal_accesses(rom,[(runtime.SUFFIX_SLOT,runtime.SUFFIX_SLOT+8)])==[]
    old_tail_access=literal_accesses(rom,[(runtime.GATE+164,runtime.GATE+172)])
    assert old_tail_access==[['Thumb_PC_relative','section0',runtime.STATUS_LOAD,runtime.GATE+164]]
    target,plan=runtime.apply(old)
    after=NdsImage.open(prior.ROM);after.rom.arm9=target
    spans=plan['private_spans']
    refs=[census(r,spans,owned+spans) for r in (rom,after)]
    external=lambda rows:sorted(r for r in rows if not r[-1])
    assert external(refs[0])==external(refs[1])
    accesses=[literal_accesses(r,spans) for r in (rom,after)]
    outside=lambda rows: sorted(r for r in rows if not any(lo<=r[2]<hi for lo,hi in owned+spans))
    assert outside(accesses[0])==outside(accesses[1])
    ROOT.mkdir(parents=True)
    arm_path=ROOT/'ARM9_RUNTIME_RESEARCH_ONLY.bin';arm_path.write_bytes(target)
    save(ROOT/'runtime_plan.json',{**plan,'research_ARM9':str(arm_path),
        'source_ROM_sha256':sha(prior.ROM.read_bytes()),'source_owned_spans':owned,
        'source_status_tail_no_incoming_literal_or_branch_references':True,
        'old_gate_tail_PC_relative_access':old_tail_access,
        'source_target_absolute_branch_and_literal_reference_census':refs,
        'source_target_PC_relative_access_census':accesses,
        'external_incoming_references_exact':True,
        'runtime_module_sha256':sha(Path(runtime.__file__).read_bytes())})
    bound=FunctionType(prior.scope.__code__,{**prior.scope.__globals__,'ROOT':ROOT,'runtime':runtime})
    bound(target)
    for fn in (prior.historical.modal_equivalence,prior.historical.status):
        bound=FunctionType(fn.__code__,{**fn.__globals__,'ROOT':ROOT},argdefs=fn.__defaults__)
        bound(old,target) if fn is prior.historical.modal_equivalence else bound(target)
    paths=[ROOT/p for p in ('runtime_plan.json','scope_proof.json','scope_binding.json','modal_equivalence.json','status_contracts.json')]
    save(ROOT/'native_runtime_verification.json',{'source_ROM':str(prior.ROM),'source_ROM_sha256':sha(prior.ROM.read_bytes()),
        'source_ARM9_sha256':sha(old),'target_ARM9_sha256':sha(target),
        'proofs':{str(p):sha(p.read_bytes()) for p in paths},
        'all122324_exact_dispatch_ABI_cases':True,
        'all3668_modal_outputs_and238_wrong_parent5_edge_cases_exact':True,
        'all140_status_whole8MiB_guards_exact':True,
        'source_PC_relative_ownership_checked_before_reuse':True,
        'no_ROM_written_or_editorial_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Corrected direct escape and all existing modal/status contracts pass.',flush=True)


if __name__=='__main__':main()
