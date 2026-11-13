"""Two bounded help copies and one owned component label; no playable ROM."""
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.dialogue.refit_help import compile_paragraph
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET,TABLE_OFFSET
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/refit_spritsail_payload_v2278')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);rom=NdsImage.open('out/all_routes_combined_v2171_candidate.nds');arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');before=current_entries(common,arm);container=IlnkContainer.parse(common);blocks=list(container.blocks);rows=read('translations/refit_contextual_editorial_manuscript_v1.json')['records'];patches=[]
 for row in rows:
  n=row['message_id'];entry=before[n];assert row['current_hex']==entry.text.hex()
  if n not in(1268,1280):continue
  compiled,lines=compile_paragraph(row['english']);span=blocks[entry.block][entry.block_offset:entry.copy_end];assert span==entry.text+b'\0'and len(compiled)<=len(span)
  target=compiled+bytes(len(span)-len(compiled));lo,hi=entry.block_offset,entry.copy_end
  assert not any(e.message_id!=n and e.block==entry.block and max(lo,e.block_offset)<min(hi,e.copy_end)for e in before)
  blocks[entry.block]=blocks[entry.block][:lo]+target+blocks[entry.block][hi:]
  patches.append(dict(message_ID=n,block=entry.block,offset=lo,copy_end=hi,source_hex=span.hex(),target_hex=target.hex(),lines=lines,complete_source_copy_owned_and_no_alias=True))
 target_common=IlnkContainer(blocks).to_bytes();target_arm=bytearray(arm);lo,hi=0x133234,0x133240;assert arm[lo:hi]==b'Split Sail\0\0';target_arm[lo:hi]=b'Spritsail\0\0\0';target_arm=bytes(target_arm);directory=sha(arm[DIRECTORY_OFFSET:TABLE_OFFSET]);after=owned_entries(target_common,target_arm,directory)
 for x,y in zip(before,after,strict=True):
  assert (x.block,x.block_offset,x.copy_end)==(y.block,y.block_offset,y.copy_end)
  authored=next((r for r in rows if r['message_id']==x.message_id and x.message_id in(1268,1280)),None)
  assert y.text==(compile_paragraph(authored['english'])[0][:-1]if authored else x.text)
  if not authored:assert container.blocks[x.block][x.block_offset:x.copy_end]==blocks[y.block][y.block_offset:y.copy_end]
 changedblocks=sorted({r['block']for r in patches});assert all(a==b for i,(a,b)in enumerate(zip(container.blocks,blocks,strict=True))if i not in changedblocks)
 reverted=bytearray(target_arm);reverted[lo:hi]=arm[lo:hi];assert bytes(reverted)==arm and cache_plan(arm)==cache_plan(target_arm)
 old,new=[MainCodeFile(a,0x02000000)for a in(arm,target_arm)];assert [(s.ramAddress,len(s.data),s.bssSize)for s in old.sections]==[(s.ramAddress,len(s.data),s.bssSize)for s in new.sections];assert all(bytes(a.data)==bytes(b.data)for a,b in zip(old.sections[1:],new.sections[1:],strict=True))and len(new.sections[3].data)-48==123040
 assert arm[0x114E4C:0x114E50]==bytes.fromhex('34321302')and target_arm[0x114E4C:0x114E50]==arm[0x114E4C:0x114E50]
 ap=ROOT/'ARM9_RESEARCH_ONLY.bin';cp=ROOT/'COMMON_RESEARCH_ONLY.DK4';ap.write_bytes(target_arm);cp.write_bytes(target_common)
 save(ROOT/'payload_plan.json',dict(source_ARM9_sha256=sha(arm),source_COMMON_sha256=sha(common),target_ARM9=str(ap),target_COMMON=str(cp),target_ARM9_sha256=sha(target_arm),target_COMMON_sha256=sha(target_common),directory_sha256=directory,COMMON_patches=patches,ARM9_patch=dict(offset=lo,end=hi,source_hex=arm[lo:hi].hex(),target_hex=target_arm[lo:hi].hex(),sole_exact_label_pointer_reference=0x114E4C),all3666_other_complete_copies_and_metadata_exact=True,all_unselected_blocks_and_all_block_lengths_exact=True,all_runtime_code_fonts_sections_BSS_cache_and123040_staged_bytes_exact=True,manuscript='translations/refit_contextual_editorial_manuscript_v1.json',manuscript_sha256=sha(Path('translations/refit_contextual_editorial_manuscript_v1.json').read_bytes()),research_only_not_a_ROM=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(COMMON_IDs=[1268,1280],ARM9_owned_bytes=12,changed_blocks=changedblocks,metadata_runtime_code_and3666copies_exact=True))
