"""Bind nine clean-exact table literals to original COMMON entry calls."""
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from capstone.arm import ARM_OP_MEM,ARM_REG_PC,ARM_OP_IMM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_services_callers_v2068')
VOICES=Path('work/analysis/town_services_voice_tables_v2063/nine_clean_exact_voice_tables_and_all_native_catalog_selections.json')
CONTRACTS={0x02053CB0:(0x02053D24,0x27C),0x02053D44:(0x02053DB8,0x27C),0x02053F0C:(0x02053F40,0x274)}
EXPECTED={0x02117460:0x02053CB0,0x021174A0:0x02053D44,0x021189C0:0x02053F0C,0x02118A00:0x02053CB0,0x02118A20:0x02053D44,0x02118A40:0x02053D44,0x02118A60:0x02053D44,0x02118A80:0x02053D44,0x02118AA0:0x02053CB0}
if __name__=='__main__':
 assert not ROOT.exists();voices=read(VOICES);arm=NdsImage.open('out/all_routes_combined_v2047_candidate.nds').read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
 cs=Cs(CS_ARCH_ARM,CS_MODE_ARM);cs.detail=True;rows=[];scopes={}
 for table in voices['tables']:
  target=table['table'];references=[]
  for literal in table['clean_ARM9_pointer_literal_references']:
   for at in range(max(0,literal-4104),literal,4):
    i=next(cs.disasm(clean[at:at+4],0x02000000+at),None)
    if not i or not i.mnemonic.startswith('ldr')or len(i.operands)<2:continue
    operand=i.operands[1]
    if operand.type!=ARM_OP_MEM or operand.mem.base!=ARM_REG_PC or at+8+operand.mem.disp!=literal:continue
    calls=[x for x in cs.disasm(clean[at:at+160],0x02000000+at)if x.mnemonic in('bl','blx')and x.operands[0].type==ARM_OP_IMM and x.operands[0].imm in CONTRACTS]
    assert calls and calls[0].operands[0].imm==EXPECTED[target]
    first=calls[0];start=max(0,at-24);end=max(first.address-0x02000000+4,at+4)
    assert arm[start:end]==clean[start:end]and arm[literal:literal+4]==clean[literal:literal+4]
    parent,field=CONTRACTS[EXPECTED[target]]
    references.append(dict(pointer_literal=0x02000000+literal,load_PC=i.address,load_operands=i.op_str,first_native_entry_call_PC=first.address,native_entry=EXPECTED[target],original_parent=parent,original_selector_stack_offset=field,
     caller_start=0x02000000+start,caller_end=0x02000000+end,caller_hex=arm[start:end].hex(),caller_sha256=sha(arm[start:end]),clean_current_exact=True,
     original_caller_disassembly=[dict(address=x.address,mnemonic=x.mnemonic,operands=x.op_str)for x in cs.disasm(arm[start:end],0x02000000+start)]))
   assert any(r['pointer_literal']==0x02000000+literal for r in references)
  assert references
  parent,field=CONTRACTS[EXPECTED[target]];scopes.setdefault(parent,dict(stack_offset=field,tables=[]))['tables'].append(target)
  rows.append(dict(table=target,family=table['family'],source_members=table['source_members'],source_callers=references,original_parent=parent,original_selector_stack_offset=field))
 entries=[]
 for start,end in((0x53CB0,0x53D44),(0x53D44,0x53DC0),(0x53F0C,0x53F4C)):
  assert arm[start:end]==clean[start:end]
  entries.append(dict(start=0x02000000+start,end=0x02000000+end,hex=arm[start:end].hex(),sha256=sha(arm[start:end]),disassembly=[dict(address=i.address,mnemonic=i.mnemonic,operands=i.op_str)for i in cs.disasm(arm[start:end],0x02000000+start)]))
 ROOT.mkdir(parents=True)
 save(ROOT/'nine_source_table_caller_parent_contracts.json',dict(ARM9_sha256=sha(arm),clean_ARM9_sha256=sha(clean),voice_proof=str(VOICES),voice_proof_sha256=sha(VOICES.read_bytes()),tables=rows,exact_parent_scopes=scopes,clean_exact_native_entries=entries,
  original_table_entry_and_selector_stack_fields_bound=True,source_context_static_code_plus_prior_native_catalog_queries_not_event_activation=True,
  twenty_three_direct_IDs=voices['remaining23_direct_IDs'],numeric_direct_and_yes_no_production_scope_still_requires_exact_source_binding=True,
  no_ROM_registry_runtime_mutation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(tables=len(rows),source_load_call_pairs=sum(len(r['source_callers'])for r in rows),parent_scopes={hex(k):[hex(t)for t in v['tables']]for k,v in scopes.items()}))
