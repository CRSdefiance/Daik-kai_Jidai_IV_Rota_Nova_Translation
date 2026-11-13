"""Source-locked primary numeric and monthly routing,existing allocations only.

Research ARM9 only. Native preservation,applicable fonts and release remain gates.
"""
from pathlib import Path
import struct
from keystone import Ks,KS_ARCH_ARM,KS_MODE_ARM
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts import search_reports_runtime_v1659 as previous
from scripts import battle_aftermath_runtime_v1253 as codec
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/town_services_runtime_v2070')
ROM=Path('out/all_routes_combined_v2047_candidate.nds')
BASE=0x02000000
SOURCE='500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e'
DIRECT=0x01FFC664
TAIL=0x02157084
YESNO=0x02151714

def contract_rows():
 rows=[]
 for parent,off,high,keys in previous.contract_rows():
  if parent==0x02053F40:
   assert(off,high)==(0x274,0x0211)and 0x89C0 not in keys
   keys=tuple(sorted((*keys,0x89C0)))
  rows.append((parent,off,high,keys))
 return rows

def apply(arm):
 assert sha(arm)==SOURCE
 code=MainCodeFile(arm,BASE);assert len(code.sections)==5
 before=[bytes(s.data)for s in code.sections];assert before[4][0x664:0x680]==bytes(Ks(KS_ARCH_ARM,KS_MODE_ARM).asm('sub ip,r3,#688;cmp ip,#53;bls 0x01ffcf78;add ip,ip,#13;cmp ip,#6;bls 0x01ffcf78;b 0x02157084',DIRECT)[0])
 ks=Ks(KS_ARCH_ARM,KS_MODE_ARM)
 original_tail=bytes(ks.asm('cmp ip,#86;beq 0x01ffcf78;b 0x01ffcbd8',TAIL)[0]);assert arm[TAIL-BASE:TAIL-BASE+12]==original_tail
 original_yes=bytes(ks.asm('sub ip,ip,#736;cmp ip,#6;beq 0x01ffcf78;b 0x01ffcd98',YESNO)[0])+bytes(4);assert arm[YESNO-BASE:YESNO-BASE+20]==original_yes
 clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');assert clean[YESNO-BASE:YESNO-BASE+20]=='隊列　　　　　　　　'.encode('cp932')
 # Logical TEQ with an unrotated8-bit immediate preserves C. After CMP,
 # BLS therefore recognizes either the earlier range or the exact old key.
 direct_asm='sub ip,r3,#688;cmp ip,#53;cmphi r3,#63;bls 0x01ffcf78;add ip,ip,#13;cmp ip,#6;b 0x02157084'
 tail_asm='teqhi ip,#86;bls 0x01ffcf78;b 0x01ffcbd8'
 yes_asm='cmp ip,#63;subhi ip,ip,#736;teqhi ip,#6;bls 0x01ffcf78;b 0x01ffcd98'
 blobs={DIRECT:bytes(ks.asm(direct_asm,DIRECT)[0]),TAIL:bytes(ks.asm(tail_asm,TAIL)[0]),YESNO:bytes(ks.asm(yes_asm,YESNO)[0])}
 assert [len(blobs[a])for a in(DIRECT,TAIL,YESNO)]==[28,12,20]
 assert arm[previous.CONTRACTS-BASE:previous.CONTRACTS-BASE+188]==previous.table()
 logical=contract_rows();table=previous.bind(codec.encode)(logical);decoded,end=previous.bind(codec.decode)(table)
 assert decoded==logical and end==len(table)==188
 blobs[previous.CONTRACTS]=table
 patches=[]
 for address,value in blobs.items():
  index=4 if address<BASE else 0;section=code.sections[index];at=address-section.ramAddress;assert 0<=at<at+len(value)<=len(section.data)
  old=bytes(section.data[at:at+len(value)]);section.data[at:at+len(value)]=value
  patches.append(dict(address=address,section=index,source_hex=old.hex(),target_hex=value.hex()))
 target=bytes(code.save());after=MainCodeFile(target,BASE)
 shape=lambda c:[(s.ramAddress,len(s.data),s.bssSize)for s in c.sections]
 assert shape(code)==shape(after)==shape(MainCodeFile(arm,BASE))and cache_plan(arm)==cache_plan(target)
 assert len(after.sections[3].data)-48==123040 and bytes(after.sections[3].data)==before[3]
 assert all(bytes(after.sections[i].data)==before[i]for i in(1,2))
 restored=[bytearray(s.data)for s in after.sections]
 for p in patches:
  at=p['address']-after.sections[p['section']].ramAddress;restored[p['section']][at:at+len(bytes.fromhex(p['source_hex']))]=bytes.fromhex(p['source_hex'])
 assert all(bytes(a)==b for a,b in zip(restored,before,strict=True))
 assert target[previous.GATE-BASE:previous.GATE-BASE+172]==arm[previous.GATE-BASE:previous.GATE-BASE+172]
 return target,dict(source_ARM9_sha256=sha(arm),target_ARM9_sha256=sha(target),patches=patches,private_spans=[[a,a+len(b)]for a,b in blobs.items()],
  primary_numeric_scope=list(range(64)),numeric_scope_excludes_separate_ritual64=True,monthly_table=0x021189C0,
  original_direct_ranges688_to741_and675_to681_plus761_retained=True,original_yes_no742_retained=True,
  all_old_selector_memberships_and_gate_code_preserved=True,source_ownership=['dk4tool/patch/market_contract_editorial.py:existing28byte ITCM stub and12byte dispatcher in44byte provider allocation','dk4tool/patch/specialty_question_editorial.py:complete20byte retired Fleet slot','scripts/search_reports_runtime_v1659.py:existing188byte contract bank'],
  direct_assembly=direct_asm,tail_assembly=tail_asm,yes_no_assembly=yes_asm,contract_rows=logical,
  all_sections_BSS_cache_ITCM_arena_and123040_staged_bytes_no_growth=True,all_changed_bytes_inverse_restorable=True,
  native_routing_preservation_applicable_font_approval_repack_gameplay_and_release_pending=True)
if __name__=='__main__':
 assert not ROOT.exists();arm=NdsImage.open(ROM).read_file('/__arm9__.bin');target,plan=apply(arm);ROOT.mkdir(parents=True)
 p=ROOT/'ARM9_RUNTIME_RESEARCH_ONLY.bin';p.write_bytes(target)
 save(ROOT/'runtime_plan.json',dict(**plan,research_ARM9=str(p),producer_sha256=sha(Path(__file__).read_bytes()),no_ROM_registry_profile_mutation=True,full_goal_complete=False))
 print(dict(research_ARM9=str(p),changed_spans=4,contract_bytes=188,numeric_IDs0_to63=True,ritual64_excluded=True,no_growth=True,target_sha256=sha(target)))
