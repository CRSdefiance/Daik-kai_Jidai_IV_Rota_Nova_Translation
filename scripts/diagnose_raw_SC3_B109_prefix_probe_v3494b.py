"""Locate the first missing context in the isolated numeric-control probe."""
from pathlib import Path
from types import FunctionType
from unicorn import UC_HOOK_MEM_INVALID
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_LR
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import prove_raw_SC3_B109_prefix_controls_v3494 as prior
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/raw_SC3_B109_prefix_probe_diagnostic_v3494b');assert not root.exists();root.mkdir(parents=True);records=[];faults=[]
    def machine(arm):
        cpu=prior.machine(arm)
        def invalid(u,access,address,size,value,unused):faults.append(dict(PC=u.reg_read(UC_ARM_REG_PC),LR=u.reg_read(UC_ARM_REG_LR),address=address,size=size,access=access));return False
        cpu.hook_add(UC_HOOK_MEM_INVALID,invalid);return cpu
    probe=FunctionType(prior.probe.__code__,{**prior.probe.__globals__,'machine':machine},argdefs=prior.probe.__defaults__)
    for label,path in [('clean','work/clean.nds'),('current','out/all_routes_combined_v3487_candidate.nds')]:
        im=NdsImage.open(path);arm=im.read_file('/__arm9__.bin');block=IlnkContainer.parse(im.read_file('/data/SC3.DK4')).blocks[109]
        for offset in ([8,14] if label=='clean' else [8,14,16]):
            faults.clear()
            try:result=probe(arm,block,offset);records.append(dict(version=label,offset=offset,result=result))
            except Exception as error:records.append(dict(version=label,offset=offset,error=repr(error),faults=list(faults)))
    save(root/'isolated_native_control_context_diagnostic.json',dict(cases=records,previous=str(Path(prior.__file__)),previous_sha256=sha(Path(prior.__file__).read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),no_ROM_ledger_registry_orcredit_change=True,full_goal_complete=False));print([(r['version'],r['offset'],r.get('error'),r.get('faults')) for r in records])
