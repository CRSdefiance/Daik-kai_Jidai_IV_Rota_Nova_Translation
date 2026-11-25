"""Compare current post-macro routes for all84 proposed paragraphs.

Original route APIs execute on cloned RAM. Constructed frames are explicit CPU
inputs,not additional live message requests or production dispatch approval.
"""
from pathlib import Path
import struct
from unicorn import UC_HOOK_CODE
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import BASE,STACK
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_services_current_routes_v2069')
SOURCE=Path('work/analysis/town_services_literals_v2055/all84_original_printf_shared_expander_and_literal_guards.json')
CALLERS=Path('work/analysis/town_services_callers_v2068/nine_source_table_caller_parent_contracts.json')
BALANCED=Path('work/analysis/town_services_native_formatter_v2067/all84_explicit_native_formatter_and_228x48_planes.json')
INPUT,OUTPUT=0x02660000,0x02662000
PCS=(0x01FFCF3C,0x02132020,0x02147E54,0x02169F78,0x0216A010,0x0214797C,0x01FFCF40,0x01FFCE1C,0x01FFCD98,0x01FFCA00,0x01FFC828,0x02053914)
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 prior,callers,balanced=map(read,(SOURCE,CALLERS,BALANCED));assert not prior['failures']and not balanced['errors']
 arm=NdsImage.open(prior['current_ROM']).read_file('/__arm9__.bin');assert sha(arm)==prior['ARM9_sha256']
 raw=Path(prior['source_snapshot']['path']).read_bytes();cpu,get=get_machine(arm,raw)
 table_for={n:(row['table'],row['original_parent'],row['original_selector_stack_offset'])for row in callers['tables']for n in row['source_members']if n>=0}
 assert len(table_for)==61
 desired={(c['message_ID'],tuple(c['supplied_arguments'])):c for c in balanced['native_font_planes']}
 rows=[];errors=[];visited=[]
 def observe(u,pc,size,data):visited.append(pc)
 for pc in PCS:cpu.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
 for old in prior['cases']:
  if old['alignment']!=0:continue
  n=old['message_ID'];text=bytes.fromhex(old['formatted_hex'])
  if n in table_for:
   table,parent,field=table_for[n];routes=[('source-bound-table',0x01FFCF3C,parent,table,field)]
  elif n in(83,84):routes=[('distinct-literal-modal-frame',0x01FFC828,0x020546E8,n,0xD0)]
  else:routes=[('numeric-direct-frame',0x01FFCF3C,0x02054014,n,0x274),('numeric-yes-no-frame',0x01FFCF3C,0x02053FCC,n,0x274)]
  for label,entry,parent,selector,field in routes:
   try:
    for at in(0xC4,0xD0,0x264,0x270,0x274,0x27C):cpu.mem_write(STACK+at,bytes(4))
    cpu.mem_write(STACK+(0xC4 if n in(83,84)else 0x264),struct.pack('<I',parent));cpu.mem_write(STACK+field,struct.pack('<I',selector))
    cpu.mem_write(INPUT-16,b'\xa5'*1056);cpu.mem_write(INPUT,text+b'\0');before=bytes(cpu.mem_read(INPUT-16,1056))
    cpu.mem_write(OUTPUT-16,b'\xa5'*1056);visited.clear();call(cpu,entry-BASE,(OUTPUT,INPUT,0),instruction_limit=3000000)
    value=bytes(cpu.mem_read(OUTPUT,1024)).split(b'\0')[0]
    assert b' '.join(value.split())==text and bytes(cpu.mem_read(INPUT-16,1056))==before
    assert bytes(cpu.mem_read(OUTPUT-16,16))==b'\xa5'*16 and bytes(cpu.mem_read(OUTPUT+len(value)+1,1023-len(value)))==b'\xa5'*(1023-len(value))
    assert bytes(cpu.mem_read(BASE,len(raw)))==raw
    lines=[line.strip().decode('cp932')for line in value.split(b'\n')]
    rows.append(dict(message_ID=n,supplied_arguments=old['supplied_arguments'],route=label,entry=entry,parent=parent,selector=selector,original_selector_stack_offset=field,
     current_output_hex=value.hex(),current_lines=lines,visited_route_PCs=list(visited),same_as_explicit_balanced_native_output=value.hex()==desired[n,tuple(old['supplied_arguments'])]['formatted_hex'],
     some_stored_row_exceeds_measured38cell_paper=any(len(line.encode('cp932'))>38 for line in lines),all4MiB_ABI_input_output_guards_exact=True,
     source_table_path_bound=label=='source-bound-table',numeric_both_parent_controls_not_individual_source_call_claim=label.startswith('numeric')))
   except Exception as exc:errors.append(dict(message_ID=n,route=label,supplied_arguments=old['supplied_arguments'],error=str(exc),type=type(exc).__name__))
 save(ROOT/'all84_current_macro_route_outputs.json',dict(ARM9_sha256=sha(arm),source_proof=str(SOURCE),source_proof_sha256=sha(SOURCE.read_bytes()),caller_proof=str(CALLERS),caller_proof_sha256=sha(CALLERS.read_bytes()),balanced_proof=str(BALANCED),balanced_proof_sha256=sha(BALANCED.read_bytes()),cases=rows,errors=errors,
  actual_current_route_APIs_no_formatter_macro_or_getter_stubs=True,source_bound_table_paths_and_dual_numeric_parent_controls=True,
  CPU_constructed_frames_not_live_event_requests=True,full_native_planes_and_style_not_approved_by_this_probe=True,
  no_ROM_runtime_registry_mutation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(cases=len(rows),errors=len(errors),same_balanced=sum(r['same_as_explicit_balanced_native_output']for r in rows),IDs_with_stored_rows_over38=sorted({r['message_ID']for r in rows if r['some_stored_row_exceeds_measured38cell_paper']})))
 for e in errors[:4]:print(e)
 assert not errors and {r['message_ID']for r in rows}==set(range(85))-{64}
