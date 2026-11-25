"""Guarded block-zero repack of primary town84; all other native copies exact."""
from pathlib import Path
import struct
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.common_single_cache_v861 import entries
from dk4tool.script.common_message_table import common_message_entries,DIRECTORY_OFFSET,TABLE_OFFSET
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_services_payload_v2092b')
DOC=Path('translations/primary_town_services_contextual_editorial_manuscript_v4.json')
BASE=0x02000000
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 doc=read(DOC);runtime_path=Path('work/analysis/town_services_runtime_v2080/runtime_plan.json');runtime=read(runtime_path)
 image=NdsImage.open(doc['current_ROM']);old_arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4');assert sha(old_arm)==doc['required_runtime_ARM9_sha256']==runtime['source_ARM9_sha256']and sha(common)==doc['source_file_sha256']
 clean=NdsImage.open('work/clean.nds');assert sha(Path('work/clean.nds').read_bytes())==doc['source_ROM_sha256']and sha(clean.read_file('/COMMON/MESFILE.DK4'))==doc['editorial_clean_source_file_sha256']
 japanese=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'));directory=read('translations/reinforcement_faction_prose_release_v1.json')['directory_sha256'];before=entries(common,old_arm,directory);source=IlnkContainer.parse(common)
 assert doc['translation_policy']=='natural-dialogue-v2'and doc['target_locale']=='en-US'
 authored={};locks=[]
 for row in doc['records']:
  n=row['message_id'];old=before[n];jp=japanese[n];text=row['english'];assert text.endswith('{PAD}')and text.count('{PAD}')==1;text=text.removesuffix('{PAD}')
  assert text and text==' '.join(text.split())and text.isascii()and not any(c in text for c in'{}\r\n')
  assert all(row['review'][g]for g in('source','context','localization','naturalness'))and row['source_meaning']and row['localization_note']and row['context']
  assert old.text.hex()==row['current_hex']and jp.text.hex()==row['source_hex']
  assert (old.block,old.block_offset,old.copy_end)==tuple(row['current_reference'][k]for k in('block','offset','copy_end'))
  assert (jp.block,jp.block_offset,jp.copy_end)==tuple(row['source_reference'][k]for k in('block','offset','copy_end'))
  assert text.count('%s')==len(row['source_format_arguments'])and '%'not in text.replace('%s','')
  authored[n]=text.encode('ascii');locks.append(dict(message_ID=n,clean_reference=row['source_reference'],current_reference=row['current_reference'],source_hex=row['source_hex'],current_hex=row['current_hex'],target_hex=authored[n].hex(),editorial_decision=row['editorial_decision']))
 assert set(authored)==set(range(85))-{64}and{before[n].block for n in authored}=={0}
 target=Path(runtime['research_ARM9']).read_bytes();assert sha(target)==runtime['target_ARM9_sha256'];code=MainCodeFile(target,BASE);original_shape=[(s.ramAddress,len(s.data),s.bssSize)for s in code.sections]
 changed=[n for n in authored if authored[n]!=before[n].text];body=bytearray();patches=[]
 def put(offset,value):
  old=bytes(code.sections[0].data[offset:offset+len(value)]);assert old==old_arm[offset:offset+len(value)]
  code.sections[0].data[offset:offset+len(value)]=value;patches.append(dict(address=BASE+offset,section=0,source_hex=old.hex(),target_hex=value.hex()))
 numbers=[r.message_id for r in before if r.block==0];assert numbers==list(range(numbers[0],numbers[-1]+1))and numbers[0]==0
 for n in numbers:
  row=before[n];payload=source.blocks[0][row.block_offset:row.copy_end];assert payload==row.text or payload.startswith(row.text+b'\0')
  if n in changed:
   assert not set(payload[len(row.text)+1:])-{0,32};payload=authored[n]+b'\0'
  put(TABLE_OFFSET+n*2,struct.pack('<H',len(body)));body.extend(payload)
 assert 0<len(body)<=8192
 put(DIRECTORY_OFFSET,struct.pack('<HH',numbers[0],len(body)));rebuilt=list(source.blocks);rebuilt[0]=bytes(body);new_common=IlnkContainer(rebuilt).to_bytes();new_arm=bytes(code.save());new_directory=sha(new_arm[DIRECTORY_OFFSET:TABLE_OFFSET]);after=entries(new_common,new_arm,new_directory)
 assert len(before)==len(after)==3668
 receipts=[]
 for n,(old,new)in enumerate(zip(before,after,strict=True)):
  assert new.text==authored.get(n,old.text)
  old_copy=source.blocks[old.block][old.block_offset:old.copy_end];new_copy=rebuilt[new.block][new.block_offset:new.copy_end]
  if n not in changed:assert old_copy==new_copy,n
  receipts.append(dict(message_ID=n,old_block=old.block,old_offset=old.block_offset,old_copy_end=old.copy_end,new_block=new.block,new_offset=new.block_offset,new_copy_end=new.copy_end,old_text_sha256=sha(old.text),new_text_sha256=sha(new.text),old_copy_sha256=sha(old_copy),new_copy_sha256=sha(new_copy),selected=n in authored,text_changed=n in changed,copy_preserved=old_copy==new_copy))
 assert all(rebuilt[n]==source.blocks[n]for n in range(1,41))
 fresh=MainCodeFile(new_arm,BASE);assert [(s.ramAddress,len(s.data),s.bssSize)for s in fresh.sections]==original_shape and cache_plan(old_arm)==cache_plan(new_arm)
 all_patches=runtime['patches']+patches;restored=[bytearray(s.data)for s in fresh.sections]
 for p in all_patches:
  off=p['address']-fresh.sections[p['section']].ramAddress;old=bytes.fromhex(p['source_hex']);restored[p['section']][off:off+len(old)]=old
 original=MainCodeFile(old_arm,BASE);assert all(bytes(x)==bytes(y.data)for x,y in zip(restored,original.sections,strict=True))
 assert all(bytes(fresh.sections[i].data)==bytes(original.sections[i].data)for i in(2,3,4))and len(fresh.sections[3].data)-48==123040
 ap=ROOT/'ARM9_PAYLOAD_RESEARCH_ONLY.bin';cp=ROOT/'COMMON_RESEARCH_ONLY.DK4';ap.write_bytes(new_arm);cp.write_bytes(new_common)
 save(ROOT/'native_payload_plan.json',dict(source_ARM9_sha256=sha(old_arm),source_COMMON_sha256=sha(common),target_ARM9_sha256=sha(new_arm),target_COMMON_sha256=sha(new_common),target_ARM9=str(ap),target_COMMON=str(cp),directory_sha256=new_directory,source_directory_sha256=directory,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),runtime_plan=str(runtime_path),runtime_plan_sha256=sha(runtime_path.read_bytes()),runtime_patches=runtime['patches'],metadata_patches=patches,patches=all_patches,source_locks=locks,all3668_copy_receipts=receipts,selected_IDs=sorted(authored),actual_text_changed_IDs=changed,old_new_block0_bytes=[len(source.blocks[0]),len(body)],source_end_fenced_no_NUL_IDs=[r.message_id for r in before if r.block==0 and source.blocks[0][r.block_offset:r.copy_end]==r.text],all40_other_blocks_exact=True,all_unselected_complete_native_copies_exact=True,opaque1484_block_and_carrier1931_copies_exact=all(receipts[n]['copy_preserved']and rebuilt[before[n].block]==source.blocks[before[n].block]for n in(1484,1931)),all_inverse_section_restore_exact=True,sections_BSS_cache_arena_and123040_staged_payload_extents_unchanged=True,producer_sha256=sha(Path(__file__).read_bytes()),registered_ROM_revised_actual_and_release_completion_pending=True,full_goal_complete=False))
 print(dict(selected=84,changed=len(changed),block0_bytes=[len(source.blocks[0]),len(body)],all_unselected_copies_exact=True,target_ARM9=sha(new_arm),target_COMMON=sha(new_common)))
