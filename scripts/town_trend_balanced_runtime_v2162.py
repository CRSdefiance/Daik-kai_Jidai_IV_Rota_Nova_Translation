"""Compact selector research for only654/655; source-owned extents do not grow."""
from pathlib import Path
import struct
from keystone import Ks,KS_ARCH_ARM,KS_MODE_ARM,KS_MODE_THUMB
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts.primary_town_runtime_v2077 import decode as old_decode
from scripts.verify_village_wrap_v608 import read,save
BASE=0x02000000;ENTRY=0x02132020;TABLE=0x02147B9C;GATE=0x02147E54
ROOT=Path('work/analysis/town_trend_runtime_v2162');SOURCE='29da98540c4366e83cca21102d4440bd8ccda3dac27f0a67cd10fa8c0d319ca5'
EXITS=(0x02169F78,0x0216A010,0x0216A05C,0x0216A0B0)
THRESHOLD=217;POINTER_BIAS=528

def encode(rows):
 result=bytearray()
 for parent,offset,high,values in rows:
  shift=(4 if parent==0x02053C14 else 5)if high else 0
  keys=sorted((v>>shift)-(POINTER_BIAS if high else 0)for v in values);assert 0<=keys[0]<=keys[-1]<65536
  payload=bytearray();last=0;i=0
  while i<len(keys):
   low,j=keys[i],i
   while j+1<len(keys)and keys[j+1]==keys[j]+1:j+=1
   gap=low-last
   while gap>=THRESHOLD:payload.append(THRESHOLD);gap-=THRESHOLD
   payload.append(gap);last=low;length=keys[j]-low
   while length:
    take=min(255-THRESHOLD,length);payload.append(THRESHOLD+take);last+=take;length-=take
   i=j+1
  if len(payload)%2==0:payload.append(THRESHOLD)
  assert 1<=len(payload)<=63 and len(result)%2==0
  kind={0x270:0,0x274:1,0x27C:3}[offset]|(4 if high else 0)
  descriptor=((len(payload)-1)//2<<3)|kind
  result.extend(struct.pack('<HB',parent&65535,descriptor));result.extend(payload)
 return bytes(result)

def decode(data):
 rows=[];pos=0
 for _ in range(8):
  assert pos%2==0;low,descriptor=struct.unpack_from('<HB',data,pos);pos+=3
  parent=0x02050000|low;kind=descriptor&7;offset={0:0x270,1:0x274,3:0x27C}[kind&3];high=0x0211 if kind&4 else 0
  shift=(4 if parent==0x02053C14 else 5)if high else 0
  size=(descriptor>>3)*2+1;end=pos+size;current=0;values=[]
  while pos<end:
   token=data[pos];pos+=1
   if token<=THRESHOLD:
    current+=token
    if token!=THRESHOLD:values.append((current+(POINTER_BIAS if high else 0))<<shift)
   else:
    length=token-THRESHOLD;values.extend((n+(POINTER_BIAS if high else 0))<<shift for n in range(current+1,current+length+1));current+=length
  assert values==sorted(set(values));rows.append((parent,offset,high,tuple(values)))
 return rows,pos

if __name__=='__main__':
 assert not ROOT.exists();rom=NdsImage.open('out/all_routes_combined_v2143_candidate.nds');arm=rom.read_file('/__arm9__.bin');assert sha(arm)==SOURCE
 before=MainCodeFile(arm,BASE);old_table=arm[TABLE-BASE:TABLE-BASE+212];rows,end=old_decode(old_table,numeric_bias=0);assert end==212
 logical=[(p,o,h,tuple(sorted(set(k)|({654,655}if p==0x02054014 else set()))))for p,o,h,k in rows]
 table=encode(logical);assert len(table)==212 and decode(table)==(logical,212)
 for p,o,h,values in logical:
  if h:
   shift=4 if p==0x02053C14 else 5;assert not {(v>>shift)-POINTER_BIAS for v in values}&{842,905,906,1028,1029}
 saved=read('work/analysis/town_services_runtime_v2080/runtime_plan.json');assembly=saved['gate_assembly'];kt=Ks(KS_ARCH_ARM,KS_MODE_THUMB);ka=Ks(KS_ARCH_ARM,KS_MODE_ARM)
 current_gate=bytes(kt.asm(assembly,GATE)[0]);assert len(current_gate)==168 and current_gate+b'\xc0\x46'*2==arm[GATE-BASE:GATE-BASE+172]
 def replace(old,new,count=1):
  global assembly
  assert assembly.count(old)==count,old;assembly=assembly.replace(old,new)
 replace('ldr r3,[sp,#0x27c]','ldr r3,[sp,#0x280]')
 replace('ldrb r7,[r4,#3]\nadds r4,#4\nadds r4,r4,r7','ldrb r7,[r4,#2]\nlsrs r7,r7,#3\nlsls r7,r7,#1\nadds r4,#4\nadds r4,r4,r7')
 replace('matched:\nldrb r3,[r4,#2]','matched:\nldrb r3,[r4,#2]\nlsrs r2,r3,#3')
 replace('lsrs r6,r3,#7\nnegs r6,r6','lsls r6,r3,#29\nasrs r6,r6,#31')
 replace('lsls r3,r3,#25\nlsrs r3,r3,#23\nadd r5,sp,#0x180','lsls r3,r3,#30\nlsrs r3,r3,#28\nadd r5,sp,#0x28c')
 replace('lsls r6,r6,#16\neors r3,r6\nlsrs r7,r3,#16\nbne fallback','lsrs r7,r3,#16\ncmp r6,r7\nbne fallback')
 replace('cmp r6,#0\nbeq ready\nldrb r7,[r4,#2]','cmp r6,#0\nbeq ready\nlsls r3,r3,#16\nldrb r7,[r4,#2]')
 replace('adds r7,#4','adds r7,#20')
 replace('movs r7,#218\nlsls r7,r7,#2\nadds r7,#1\nsubs r3,r3,r7','subs r3,r3,r6\nadds r3,#1')
 replace('ready:\nmov r6,r3\nldrb r5,[r4,#3]\nadds r4,#4','ready:\nmov r6,r3\nlsls r5,r2,#1\nadds r5,#1\nadds r4,#3')
 replace('cmp r7,#191','cmp r7,#217',2);replace('subs r7,#191','subs r7,#217')
 gate=bytes(kt.asm(assembly,GATE)[0]);assert len(gate)==172,len(gate)
 arm_code=lambda text,at:bytes(ka.asm(text,at)[0])
 assert arm[ENTRY-BASE:ENTRY-BASE+4]==arm_code('push {r3-r7,lr}',ENTRY)
 blobs={TABLE:table,GATE:gate,ENTRY:arm_code('push {r2-r7,lr}',ENTRY)}
 for address in EXITS:
  assert arm[address-BASE:address-BASE+4]==arm_code('pop {r3-r7,lr}',address)
  blobs[address]=arm_code('pop {r2-r7,lr}',address)
 code=MainCodeFile(arm,BASE);patches=[]
 for address,value in blobs.items():
  at=address-BASE;old=bytes(code.sections[0].data[at:at+len(value)]);assert len(old)==len(value);code.sections[0].data[at:at+len(value)]=value;patches.append(dict(address=address,section=0,source_hex=old.hex(),target_hex=value.hex()))
 target=bytes(code.save());after=MainCodeFile(target,BASE);shape=lambda c:[(s.ramAddress,len(s.data),s.bssSize)for s in c.sections];assert shape(before)==shape(after)and cache_plan(arm)==cache_plan(target)and len(after.sections[3].data)-48==123040
 assert all(bytes(a.data)==bytes(b.data)for a,b in zip(before.sections[1:],after.sections[1:],strict=True));restored=MainCodeFile(target,BASE)
 for p in patches:
  at=p['address']-BASE;restored.sections[0].data[at:at+len(bytes.fromhex(p['source_hex']))]=bytes.fromhex(p['source_hex'])
 assert bytes(restored.save())==arm
 ROOT.mkdir(parents=True);path=ROOT/'ARM9_RUNTIME_RESEARCH_ONLY.bin';path.write_bytes(target)
 save(ROOT/'runtime_plan.json',dict(source_ARM9_sha256=sha(arm),target_ARM9_sha256=sha(target),research_ARM9=str(path),patches=patches,old_logical_rows=rows,logical_rows=logical,only_new_memberships=dict(parent=0x02054014,IDs=[654,655]),new_header_bytes=3,payloads_odd_length_keep_all_parent_headers_halfword_aligned=True,table_bytes_before_after=[212,212],gate_bytes_before_after=[172,172],delta_skip_threshold=THRESHOLD,maximum_run=255-THRESHOLD,pointer_encoding_bias=POINTER_BIAS,additional_saved_R2_stack_word_restored_at_allfour_existing_exits=True,parent_SP_field_corrected_for28byte_entry_frame=True,gate_assembly=assembly,all_unowned_bytes_inverse_restore_exact=True,all_sections_BSS_ITCM_cache_arena_and123040_staged_bytes_unchanged=True,no_ROM_profile_registry_or_manuscript_mutation=True,native_predicates_guard_ABI_census_fonts_cache_and_actual_release_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(table=len(table),gate=len(gate),ARM9=sha(target),patches=len(patches),native_approval_pending=True))
