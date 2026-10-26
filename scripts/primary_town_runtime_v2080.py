"""Successor: preserve fixed status string base after offset-table relocation."""
from pathlib import Path
from ndspy.code import MainCodeFile
from keystone import Ks,KS_ARCH_ARM,KS_MODE_THUMB
from scripts.primary_town_runtime_v2077 import apply as previous,ROOT as PRIOR,BASE
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/town_services_runtime_v2080')
TAIL=0x02147D28
if __name__=='__main__':
 assert not ROOT.exists()
 arm=NdsImage.open('out/all_routes_combined_v2047_candidate.nds').read_file('/__arm9__.bin');target,plan=previous(arm)
 assert target==Path(read(PRIOR/'runtime_plan.json')['research_ARM9']).read_bytes()
 code=MainCodeFile(target,BASE);at=TAIL-BASE;old=bytes(code.sections[0].data[at:at+8]);assert old.hex()=='3846000c01380004'
 asm='movs r0,#133; lsls r0,r0,#2; subs r0,#1; lsls r0,r0,#16'
 fixed=bytes(Ks(KS_ARCH_ARM,KS_MODE_THUMB).asm(asm,TAIL)[0]);assert fixed.hex()=='8520800001380004'
 code.sections[0].data[at:at+8]=fixed;result=bytes(code.save())
 a,b=MainCodeFile(arm,BASE),MainCodeFile(result,BASE)
 assert [(s.ramAddress,len(s.data),s.bssSize)for s in a.sections]==[(s.ramAddress,len(s.data),s.bssSize)for s in b.sections]
 plan['patches'].append(dict(address=TAIL,section=0,source_hex=old.hex(),target_hex=fixed.hex()));plan['private_spans'].append([TAIL,TAIL+8])
 restored=[bytearray(s.data)for s in b.sections]
 for p in plan['patches']:
  off=p['address']-b.sections[p['section']].ramAddress;restored[p['section']][off:off+len(bytes.fromhex(p['source_hex']))]=bytes.fromhex(p['source_hex'])
 assert all(bytes(x)==bytes(y.data)for x,y in zip(restored,a.sections,strict=True))
 ROOT.mkdir(parents=True);path=ROOT/'ARM9_RUNTIME_RESEARCH_ONLY.bin';path.write_bytes(result)
 save(ROOT/'runtime_plan.json',dict(**{**plan,'target_ARM9_sha256':sha(result)},research_ARM9=str(path),supersedes_v2077_research_only=True,status_tail_fixed_DATA_BASE=0x02130000,status_tail_assembly=asm,old_status_tail_implicitly_derived_base_from_packed_pointer=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(target_sha256=sha(result),fixed_status_base=hex(0x02130000),no_extent_growth=True))
