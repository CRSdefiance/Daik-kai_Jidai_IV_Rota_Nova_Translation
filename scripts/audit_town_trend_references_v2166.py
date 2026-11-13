"""Incoming references and ARMv5 ISA for unchanged-size compact selector allocations."""
from pathlib import Path
import inspect
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB,CS_MODE_ARM
from scripts import audit_item_runtime_storage_v785 as prior
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/town_trend_references_v2166')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);plan=read('work/analysis/town_trend_runtime_v2162/runtime_plan.json');before=NdsImage.open('out/all_routes_combined_v2143_candidate.nds');after=NdsImage.open('out/all_routes_combined_v2143_candidate.nds');arm=before.read_file('/__arm9__.bin');target=Path(plan['research_ARM9']).read_bytes();assert sha(arm)==plan['source_ARM9_sha256']and sha(target)==plan['target_ARM9_sha256'];after.rom.arm9=target
 spans=[[0x02132020,0x02132030],[0x02147B9C,0x02147C70],[0x02147E54,0x02147F00],[0x02169F78,0x02169F84],[0x0216A010,0x0216A018],[0x0216A05C,0x0216A064],[0x0216A0B0,0x0216A0C0]]
 source=inspect.getsource(prior.census);old="rb'(?=(...\\x02))'";assert source.count(old)==1;source=source.replace(old,"rb'(?=(...[\\x01\\x02]))'");env=dict(prior.__dict__);exec(compile(source,__file__,'exec'),env);census=env['census'];a,b=[census(r,spans,spans)for r in(before,after)];external=lambda rows:sorted(r for r in rows if not r[-1]);assert external(a)==external(b)
 interfaces=[]
 for r in external(a):
  assert r[3]==0x02132020,r
  interfaces.append(r)
 assert interfaces
 gate=target[0x147E54:0x147F00];thumb=Cs(CS_ARCH_ARM,CS_MODE_THUMB);instructions=list(thumb.disasm(gate[:-8],0x02147E54));assert sum(i.size for i in instructions)==164 and all(i.size==2 or i.mnemonic in('bl','blx')for i in instructions)
 assert gate[-8:]==arm[0x147E54+160:0x147E54+168]
 bridges=[];isa=Cs(CS_ARCH_ARM,CS_MODE_ARM)
 for p in plan['patches']:
  if p['address']in(0x02132020,0x02169F78,0x0216A010,0x0216A05C,0x0216A0B0):
   ins=next(isa.disasm(bytes.fromhex(p['target_hex']),p['address']));assert ins.mnemonic in('push','pop')and ins.op_str=='{r2, r3, r4, r5, r6, r7, lr}';bridges.append(dict(address=ins.address,bytes=ins.bytes.hex(),mnemonic=ins.mnemonic,operands=ins.op_str))
 units=prior.units(before)+[('ARM7',before.rom.arm7RamAddress,bytes(before.rom.arm7))]
 save(ROOT/'all_unit_references_and_ARMv5_instruction_audit.json',dict(source_ARM9_sha256=sha(arm),target_ARM9_sha256=sha(target),watched_existing_allocations=spans,units=[dict(name=n,base=base,length=len(raw),sha256=sha(raw))for n,base,raw in units],before=a,after=b,all_external_incoming_references_exact=interfaces,no_external_interior_entry_or_data_alias_to_reencoded_table_gate_or_changed_stack_bridges=True,only_public_ENTRY_start_is_called_externally=True,all_byte_offsets_high01_02_ARM_branch_ADR_ThumbBL_BLX_scanned=True,Thumb_code_bytes=164,Thumb_data_bytes=8,Thumb_instructions=[dict(address=i.address,bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str)for i in instructions],ARM_stack_bridge_instructions=bridges,Thumb1_and_ARMv5_BL_BLX_only=True,effective_census_sha256=sha(source.encode()),historical_census_sha256=sha(Path(prior.__file__).read_bytes()),runtime_plan_sha256=sha(Path('work/analysis/town_trend_runtime_v2162/runtime_plan.json').read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),no_ROM_or_registry_mutation=True,full_goal_complete=False));print(dict(units=len(units),external_references=len(interfaces),Thumb_code_bytes=164,table_bytes=212))
