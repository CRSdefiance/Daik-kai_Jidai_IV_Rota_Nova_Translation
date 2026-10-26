"""Four source-locked Square prose revisions after the frozen V2097 stack."""
from pathlib import Path
import struct
from ndspy.code import MainCodeFile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries,DIRECTORY_OFFSET,TABLE_OFFSET
from scripts.verify_village_wrap_v608 import read
CONFIG='translations/square_contextual_editorial_release_v1.json';PATH='/COMMON/MESFILE.DK4';BASE=0x02000000;IDS=set(range(656,745));CHANGED={698,701,718,740}

def apply_release(candidate,baseline,path=CONFIG):
 conf=read(path);assert conf['format']=='dk4-square-contextual-editorial-v1'
 for name,digest in conf['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
 common,arm=candidate.read_file(PATH),candidate.read_file('/__arm9__.bin');assert sha(common)==conf['source_COMMON_sha256']and sha(arm)==conf['source_ARM9_sha256'];assert sha(baseline.read_file(PATH))==conf['canonical_COMMON_sha256']
 doc=read(conf['manuscript']);validate_natural_dialogue_batch(doc);assert doc['translation_policy']=='natural-dialogue-v2'and not doc['formatting_review_pending'];assert sha(Path('work/clean.nds').read_bytes())==doc['source_ROM_sha256']
 clean=NdsImage.open('work/clean.nds');jp=common_message_entries(clean.read_file(PATH),clean.read_file('/__arm9__.bin'));plan=read(conf['payload_plan']);before=owned_entries(common,arm,plan['source_directory_sha256']);source=IlnkContainer.parse(common);authored={};selected=set()
 for row in doc['records']:
  n=row['message_id'];assert n in IDS and n not in selected;selected.add(n)
  assert row['source_hex']==jp[n].text.hex()and row['current_hex']==before[n].text.hex()
  for current,entry in [('source',jp[n]),('current',before[n])]:assert tuple(row[current+'_reference'][k]for k in('block','offset','copy_end'))==(entry.block,entry.block_offset,entry.copy_end)
  text=row['english'];assert text.endswith('{PAD}')and text.count('{PAD}')==1;text=text.removesuffix('{PAD}');assert text and text.isascii()and text==' '.join(text.split())and len(text)<236 and not any(c in text for c in'{}\r\n')
  assert text.count('%s')==jp[n].text.count(b'%s')and'%'not in text.replace('%s','')
  if n in CHANGED:assert row['editorial_decision']=='revise';authored[n]=b' '+text.encode('ascii')
  else:assert row['editorial_decision']=='retain-wording'and row['fresh_retained_wording_justification']and' '.join(before[n].text.decode('cp932').split())==text
 assert selected==IDS and set(authored)==CHANGED
 code=MainCodeFile(arm,BASE)
 for p in plan['metadata_patches']:
  at=p['address']-BASE;old,new=bytes.fromhex(p['source_hex']),bytes.fromhex(p['target_hex']);assert p['section']==0 and len(old)==len(new)and bytes(code.sections[0].data[at:at+len(old)])==old
  assert any(DIRECTORY_OFFSET+b*4<=at<DIRECTORY_OFFSET+b*4+4 for b in(8,9))or any(TABLE_OFFSET+r.message_id*2==at for r in before if r.block in(8,9))
  code.sections[0].data[at:at+len(new)]=new
 target_arm=bytes(code.save());assert sha(target_arm)==plan['target_ARM9_sha256']==conf['target_ARM9_sha256']
 blocks=list(source.blocks)
 for b in(8,9):
  rows=[r for r in before if r.block==b];body=bytearray(blocks[b][:rows[0].block_offset])
  for r in rows:
   payload=blocks[b][r.block_offset:r.copy_end]
   if r.message_id in authored:assert not set(payload[len(r.text)+1:])-{0,32};payload=authored[r.message_id]+b'\0'
   assert struct.unpack_from('<H',target_arm,TABLE_OFFSET+r.message_id*2)[0]==len(body);body.extend(payload)
  assert 0<len(body)<=4096;blocks[b]=bytes(body)
 target_common=IlnkContainer(blocks).to_bytes();assert sha(target_common)==plan['target_COMMON_sha256']==conf['target_COMMON_sha256'];after=owned_entries(target_common,target_arm,plan['directory_sha256']);assert len(before)==len(after)==3668
 for old,new in zip(before,after,strict=True):
  assert new.text==authored.get(old.message_id,old.text)
  if old.message_id not in CHANGED:assert source.blocks[old.block][old.block_offset:old.copy_end]==blocks[new.block][new.block_offset:new.copy_end]
 assert all(blocks[b]==source.blocks[b]for b in range(41)if b not in(8,9))
 reverted=MainCodeFile(target_arm,BASE)
 for p in plan['metadata_patches']:
  at=p['address']-BASE;reverted.sections[0].data[at:at+len(bytes.fromhex(p['source_hex']))]=bytes.fromhex(p['source_hex'])
 assert bytes(reverted.save())==arm and plan['all_executable_font_other_runtime_and123040_staged_bytes_exact']
 proofs={k:read(v)for k,v in conf['verification'].items()}
 assert proofs['copies']['ARM9_sha256']==sha(target_arm)and proofs['copies']['COMMON_sha256']==sha(target_common)and proofs['copies']['complete_native_copies']==7336 and len(proofs['copies']['sequenced_cache_cases'])==180
 assert proofs['formatting']['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes())and len(proofs['formatting']['bindings'])==134 and proofs['formatting']['research_48_to64_geometry_not_used']
 assert proofs['control']['case_count']==307 and proofs['control']['page_count']==307 and not proofs['control']['multi_page_cases']and proofs['control']['ARM9_sha256']==sha(arm)
 assert proofs['arguments']['total']==11580 and proofs['arguments']['all_names_and_printf_argument_order_preserved']and proofs['arguments']['all_ASCII_glyphs_present']
 assert len(proofs['ordinary']['actual_holds'])==4 and len(proofs['promoter']['actual_holds'])==4 and proofs['promoter']['geometry_word_02118ACC_unchanged_48']
 candidate.replace_file(PATH,target_common);candidate.replace_file('/__arm9__.bin',target_arm)
 return dict(manuscript=conf['manuscript'],source_ARM9_sha256=sha(arm),source_COMMON_sha256=sha(common),target_ARM9_sha256=sha(target_arm),target_COMMON_sha256=sha(target_common),selected_IDs=sorted(IDS),actual_text_changed_IDs=sorted(CHANGED),changed_records=[dict(id=f'COMMON_MESSAGE_{n}')for n in sorted(IDS)],native_layout_profile=doc['consumer_layout_profile'],all3664_unselected_complete_copies_and39_other_blocks_exact=True,only_four_paragraphs_and_COMMON_metadata_changed=True,geometry_font_runtime_staged_payload_exact=True,natural_dialogue_v2_per_record_gates_enforced=True,revised_actual_gameplay_and_release_verification_not_claimed_here=True,full_goal_complete=False)

