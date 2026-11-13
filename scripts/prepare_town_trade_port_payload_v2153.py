"""Guarded single-block research repack; two trend paragraph revisions only."""
from pathlib import Path
import struct
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.square_contextual_reference_v1 import current_entries
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import DIRECTORY_OFFSET,TABLE_OFFSET,common_message_entries
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_trade_port_payload_v2153')
DOC=Path('translations/town_trade_port_contextual_editorial_manuscript_v1.json')
BASE=0x02000000
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 doc=read(DOC);rom=NdsImage.open(doc['current_ROM']);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
 assert sha(arm)==doc['current_ARM9_sha256']and sha(common)==doc['current_COMMON_sha256']and sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
 before=current_entries(common,arm);blocks=IlnkContainer.parse(common).blocks;clean=NdsImage.open('work/clean.nds');jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'));authored={}
 for r in doc['records']:
  n=r['message_id'];assert r['source_hex']==jp[n].text.hex()and r['current_hex']==before[n].text.hex()
  if n not in doc['revised_IDs']:continue
  text=r['english'].removesuffix('{PAD}');assert text== ' '.join(text.split())and text.isascii()and not any(c in text for c in '{}\r\n') and text.count('%s')==1 and '%'not in text.replace('%s','')and len(text)<236
  assert before[n].text.startswith(b' ')and not before[n].text.startswith(b'  ')
  authored[n]=b' '+text.encode('ascii')
 assert set(authored)=={654,655};affected={before[n].block for n in authored};assert affected=={7}
 code=MainCodeFile(arm,BASE);rebuilt=list(blocks);patches=[]
 def put(off,value):
  old=bytes(code.sections[0].data[off:off+len(value)]);assert old==arm[off:off+len(value)]
  code.sections[0].data[off:off+len(value)]=value;patches.append(dict(address=BASE+off,section=0,source_hex=old.hex(),target_hex=value.hex()))
 sizes=[]
 for b in sorted(affected):
  rows=[r for r in before if r.block==b];assert [r.message_id for r in rows]==list(range(rows[0].message_id,rows[-1].message_id+1))and [r.block_offset for r in rows]==sorted({r.block_offset for r in rows})
  body=bytearray(blocks[b][:rows[0].block_offset])
  for r in rows:
   payload=blocks[b][r.block_offset:r.copy_end];assert payload==r.text or payload.startswith(r.text+b'\0')
   if r.message_id in authored:
    assert not set(payload[len(r.text)+1:])-{0,32};payload=authored[r.message_id]+b'\0'
   put(TABLE_OFFSET+r.message_id*2,struct.pack('<H',len(body)));body.extend(payload)
  assert 0<len(body)<=8192;put(DIRECTORY_OFFSET+4*b,struct.pack('<HH',rows[0].message_id,len(body)));rebuilt[b]=bytes(body);sizes.append(dict(block=b,before=len(blocks[b]),after=len(body)))
 target_common=IlnkContainer(rebuilt).to_bytes();target_arm=bytes(code.save());directory=sha(target_arm[DIRECTORY_OFFSET:TABLE_OFFSET]);after=owned_entries(target_common,target_arm,directory);copies=[]
 for old,new in zip(before,after,strict=True):
  n=old.message_id;assert new.text==authored.get(n,old.text);a=blocks[old.block][old.block_offset:old.copy_end];b=rebuilt[new.block][new.block_offset:new.copy_end]
  if n not in authored:assert a==b,n
  copies.append(dict(message_ID=n,old_block=old.block,old_offset=old.block_offset,old_copy_end=old.copy_end,new_block=new.block,new_offset=new.block_offset,new_copy_end=new.copy_end,old_copy_sha256=sha(a),new_copy_sha256=sha(b),old_text_sha256=sha(old.text),new_text_sha256=sha(new.text),copy_preserved=a==b,text_changed=n in authored))
 assert all(a==b for i,(a,b)in enumerate(zip(blocks,rebuilt,strict=True))if i not in affected)
 fresh=MainCodeFile(target_arm,BASE);oldcode=MainCodeFile(arm,BASE);assert [(s.ramAddress,len(s.data),s.bssSize)for s in fresh.sections]==[(s.ramAddress,len(s.data),s.bssSize)for s in oldcode.sections]
 restored=[bytearray(s.data)for s in fresh.sections]
 for p in patches:
  off=p['address']-BASE;restored[0][off:off+len(bytes.fromhex(p['source_hex']))]=bytes.fromhex(p['source_hex'])
 assert all(bytes(a)==bytes(b.data)for a,b in zip(restored,oldcode.sections,strict=True))and cache_plan(arm)==cache_plan(target_arm)and len(fresh.sections[3].data)-48==123040
 ap=ROOT/'ARM9_RESEARCH_ONLY.bin';cp=ROOT/'COMMON_RESEARCH_ONLY.DK4';ap.write_bytes(target_arm);cp.write_bytes(target_common)
 save(ROOT/'native_payload_plan.json',dict(source_ARM9_sha256=sha(arm),source_COMMON_sha256=sha(common),target_ARM9_sha256=sha(target_arm),target_COMMON_sha256=sha(target_common),target_ARM9=str(ap),target_COMMON=str(cp),source_directory_sha256=sha(arm[DIRECTORY_OFFSET:TABLE_OFFSET]),directory_sha256=directory,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),selected_IDs=[r['message_id']for r in doc['records']],actual_text_changed_IDs=sorted(authored),metadata_patches=patches,all3668_copy_receipts=copies,block_sizes=sizes,all3666_unselected_complete_copies_exact=True,all40_other_blocks_exact=True,opaque1484_prefix_and_carrier1931_blocks_and_copies_exact=True,all_inverse_section_restore_exact=True,all_executable_font_other_runtime_and123040_staged_bytes_exact=True,sections_BSS_cache_arena_extents_unchanged=True,producer_sha256=sha(Path(__file__).read_bytes()),not_a_playable_ROM=True,full_goal_complete=False))
 print(dict(revised=sorted(authored),block_sizes=sizes,ARM9=sha(target_arm),COMMON=sha(target_common),unselected_exact=3666))
