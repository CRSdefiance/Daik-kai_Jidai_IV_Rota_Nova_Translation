"""Primary84 literal routing within current code/data extents; research only.

Relocates the12 status offsets into unused space in the replaced96-byte modal
wrapper,freeing its24 static bytes for the full selector table. No pool grows.
"""
from pathlib import Path
import struct
from keystone import Ks,KS_ARCH_ARM,KS_MODE_ARM,KS_MODE_THUMB
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts import search_reports_runtime_v1659 as previous
from scripts.verify_village_wrap_v608 import read,save
BASE=0x02000000
SOURCE='500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e'
ROOT=Path('work/analysis/town_services_runtime_v2077')
MODAL,PACKED,PARENT=0x01FF9CE4,0x01FF9D18,0x01FF9D40
OLD_PACKED,STATUS_LITERAL=0x02147C58,0x02147A20
CONTRACTS,GATE=previous.CONTRACTS,previous.GATE


def rows():
 source=read('work/analysis/town_services_callers_v2068/nine_source_table_caller_parent_contracts.json');adds={p:set()for p,o,h,k in previous.contract_rows()}
 for t in source['tables']:adds[t['original_parent']].add(t['table']&65535)
 for p in(0x02054014,0x02053FCC):adds[p].update(range(64))
 return[(p,o,h,tuple(sorted(set(keys)|adds[p])))for p,o,h,keys in previous.contract_rows()]


def encode(logical,*,numeric_bias):
 result=bytearray()
 for parent,offset,high,values in logical:
  shift=(4 if parent==0x02053C14 else 5)if high else 0
  assert all(v&((1<<shift)-1)==0 for v in values)
  keys=sorted((v>>shift)-(873 if high else numeric_bias)for v in values);assert 0<=keys[0]<=keys[-1]<65536
  payload=bytearray();last=0;i=0
  while i<len(keys):
   low,j=keys[i],i
   while j+1<len(keys)and keys[j+1]==keys[j]+1:j+=1
   gap=low-last
   while gap>=191:payload.append(191);gap-=191
   payload.append(gap);last=low;length=keys[j]-low
   while length:
    take=min(64,length);payload.append(191+take);last+=take;length-=take
   i=j+1
  if len(payload)&1:payload.append(191)
  field=(offset+24-0x180)//4;assert 0<=field<128 and len(payload)<256
  result.extend(struct.pack('<HBB',parent&65535,field|(128 if high else 0),len(payload)));result.extend(payload)
 return bytes(result)


def decode(data,*,numeric_bias):
 pos=0;logical=[]
 for _ in range(8):
  assert pos&1==0;parent,field,size=struct.unpack_from('<HBB',data,pos);pos+=4;parent|=0x02050000
  high=0x0211 if field&128 else 0;offset=(field&127)*4+0x180-24;shift=(4 if parent==0x02053C14 else 5)if high else 0
  bias=873 if high else numeric_bias;end=pos+size;current=0;values=[]
  while pos<end:
   code=data[pos];pos+=1
   if code<=191:
    current+=code
    if code!=191:values.append((current+bias)<<shift)
   else:
    length=code-191;values.extend((n+bias)<<shift for n in range(current+1,current+length+1));current+=length
  assert values==sorted(set(values));logical.append((parent,offset,high,tuple(values)))
 return logical,pos


def apply(arm):
 assert sha(arm)==SOURCE;code=MainCodeFile(arm,BASE);before=[bytes(s.data)for s in code.sections]
 assert len(code.sections)==5 and len(before[1])==8172 and len(before[3])-48==123040
 legacy=encode(previous.contract_rows(),numeric_bias=780);assert legacy+bytes(188-len(legacy))==previous.table()
 assert arm[CONTRACTS-BASE:CONTRACTS-BASE+188]==previous.table()and arm[GATE-BASE:GATE-BASE+172]==previous.gate()[0]
 assert struct.unpack_from('<I',arm,STATUS_LITERAL-BASE)[0]==OLD_PACKED
 packed=arm[OLD_PACKED-BASE:OLD_PACKED-BASE+24];assert len(packed)==24
 logical=rows();table=encode(logical,numeric_bias=0);decoded,end=decode(table,numeric_bias=0);assert decoded==logical and len(table)==end==212
 assembly=previous.gate()[1]
 old='pointer_bias:\nmovs r7,#93\nsubs r3,r3,r7\nready:\nmovs r7,#195\nlsls r7,r7,#2\nsubs r3,r3,r7'
 new='pointer_bias:\nmovs r7,#218\nlsls r7,r7,#2\nadds r7,#1\nsubs r3,r3,r7\nready:'
 assert assembly.count(old)==1;assembly=assembly.replace(old,new)
 old='movs r4,#31\nlsls r4,r4,#1\nsubs r4,r3,r4';new='movs r4,#211\nlsls r4,r4,#2\nsubs r4,#2\nsubs r4,r3,r4'
 assert assembly.count(old)==1;assembly=assembly.replace(old,new)
 gate=bytes(Ks(KS_ARCH_ARM,KS_MODE_THUMB).asm(assembly,GATE)[0]);assert len(gate)==168;gate+=b'\xc0\x46'*2
 for parent,off,high,values in logical:
  if high:
   shift=4 if parent==0x02053C14 else 5
   assert not {(n>>shift)-873 for n in values}&{842,905,906,1028,1029}
 ks=Ks(KS_ARCH_ARM,KS_MODE_ARM)
 modal_asm=f'''ldr r3,[sp,#0xc4]
ldr ip,[pc,#{PARENT-(MODAL+4+8)}]
cmp r3,ip
bne fallback
ldr r3,[sp,#0xd0]
sub r3,r3,#83
cmp r3,#1
bls 0x02147b98
fallback:
push {{r4,lr}}
bl 0x02053914
mov r0,#0
pop {{r4,pc}}'''
 modal_code=bytes(ks.asm(modal_asm,MODAL)[0]);assert len(modal_code)==48
 original=before[1][MODAL-0x01FF8000:MODAL-0x01FF8000+96]
 assert len(original)==96 and struct.unpack_from('<I',original,92)[0]==0x020546E8
 assert original[:4]==bytes(ks.asm('push {r4-r6,lr}',MODAL)[0])
 modal=bytearray(96);modal[:48]=modal_code;modal[PACKED-MODAL:PACKED-MODAL+24]=packed;struct.pack_into('<I',modal,PARENT-MODAL,0x020546E8)
 # This caller is only the83 receipt loop. Literal post-printf copy makes its
 # old display-only F/I expansion unnecessary;retain raw original name bytes.
 assert next(__import__('capstone').Cs(__import__('capstone').CS_ARCH_ARM,__import__('capstone').CS_MODE_ARM).disasm(arm[0xB2590:0xB2594],BASE+0xB2590)).op_str=='#0x1ff9ba0'
 assert arm[0xB253C:0xB2540].hex()=='5390a0e3'and arm[0xB25A4:0xB25A8].hex()=='0900a0e1'
 blobs={CONTRACTS:table,GATE:gate,STATUS_LITERAL:struct.pack('<I',PACKED),MODAL:bytes(modal),BASE+0xB2590:bytes.fromhex('00a0a0e1')}
 patches=[]
 for address,value in blobs.items():
  index=1 if address<BASE else 0;section=code.sections[index];at=address-section.ramAddress;assert 0<=at<at+len(value)<=len(section.data)
  old=bytes(section.data[at:at+len(value)]);section.data[at:at+len(value)]=value;patches.append(dict(address=address,section=index,source_hex=old.hex(),target_hex=value.hex()))
 result=bytes(code.save());after=MainCodeFile(result,BASE);shape=lambda c:[(s.ramAddress,len(s.data),s.bssSize)for s in c.sections]
 assert shape(code)==shape(after)==shape(MainCodeFile(arm,BASE))and cache_plan(arm)==cache_plan(result)
 assert all(bytes(after.sections[i].data)==before[i]for i in(2,3,4))
 restored=[bytearray(s.data)for s in after.sections]
 for p in patches:
  at=p['address']-after.sections[p['section']].ramAddress;old=bytes.fromhex(p['source_hex']);restored[p['section']][at:at+len(old)]=old
 assert all(bytes(a)==b for a,b in zip(restored,before,strict=True))
 return result,dict(source_ARM9_sha256=sha(arm),target_ARM9_sha256=sha(result),patches=patches,private_spans=[[a,a+len(b)]for a,b in blobs.items()],
  contract_rows=logical,encoded_table_bytes=212,table_bank_bytes_before_after=[212,212],packed_status_offsets_hex=packed.hex(),packed_status_old=OLD_PACKED,packed_status_new=PACKED,
  numeric_encoding_bias=0,pointer_encoding_bias=873,native_gate_bytes=168,owned_gate_bytes=172,
  source_owned_modal_wrapper_bytes=96,modal_literal_IDs=[83,84],modal_parent=0x020546E8,
  original_raw_receipt_force_name_assignment_restored=True,display_name_escape_helper_preserved_but_not_used_by83_literal_consumer=True,
  source_copy_and_native_MACRO_is_retained_for_every_unselected_modal=True,
  gate_assembly=assembly,modal_assembly=modal_asm,all_unowned_bytes_inverse_restore_exact=True,
  all_sections_BSS_ITCM_arena_cache_and123040_staged_bytes_keep_exact_extents=True,
  no_ROM_profile_registry_or_manuscript_mutation=True,native_status_selector_fonts_cache_repack_and_revised_actual_gates_pending=True)

if __name__=='__main__':
 assert not ROOT.exists();arm=NdsImage.open('out/all_routes_combined_v2047_candidate.nds').read_file('/__arm9__.bin');target,plan=apply(arm);ROOT.mkdir(parents=True)
 p=ROOT/'ARM9_RUNTIME_RESEARCH_ONLY.bin';p.write_bytes(target)
 save(ROOT/'runtime_plan.json',dict(**plan,research_ARM9=str(p),producer_sha256=sha(Path(__file__).read_bytes()),supersedes_research_only_v2070=True,full_goal_complete=False))
 print(dict(research_ARM9=str(p),target_sha256=sha(target),table_bytes=212,packed_status_bytes_relocated=24,modal_IDs=[83,84],no_extent_growth=True))
