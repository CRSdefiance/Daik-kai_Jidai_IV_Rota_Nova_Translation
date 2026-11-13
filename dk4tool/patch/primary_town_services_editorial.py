"""Source-locked primary-town editorial layer after the frozen V2047 stack."""
from pathlib import Path
import struct
from ndspy.code import MainCodeFile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.common_single_cache_v861 import entries
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries,DIRECTORY_OFFSET,TABLE_OFFSET
from scripts.verify_village_wrap_v608 import read
CONFIG='translations/primary_town_services_editorial_release_v1.json'
PATH='/COMMON/MESFILE.DK4'
BASE=0x02000000
IDS=set(range(85))-{64}

def compiled(row):
 text=row['english'];assert text.endswith('{PAD}')and text.count('{PAD}')==1
 text=text.removesuffix('{PAD}');assert text and text.isascii()and text==' '.join(text.split())and len(text)<236 and not any(c in text for c in'{}\r\n')
 if row.get('qa_waivers'):assert row.get('qa_waiver_reason','').strip()
 return text.encode('ascii')

def apply_release(candidate,baseline,path=CONFIG):
 conf=read(path);assert conf['format']=='dk4-primary-town-services-editorial-v1'
 for name,digest in conf['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
 common,arm=candidate.read_file(PATH),candidate.read_file('/__arm9__.bin')
 assert sha(common)==conf['source_COMMON_sha256']and sha(arm)==conf['source_ARM9_sha256']
 assert sha(baseline.read_file(PATH))==conf['canonical_COMMON_sha256']
 doc=read(conf['manuscript']);validate_natural_dialogue_batch(doc);assert doc['translation_policy']=='natural-dialogue-v2'and not doc['formatting_review_pending']
 plan=read(conf['payload_plan']);assert plan['source_COMMON_sha256']==sha(common)and plan['source_ARM9_sha256']==sha(arm)
 assert sha(Path('work/clean.nds').read_bytes())==doc['source_ROM_sha256'];clean=NdsImage.open('work/clean.nds')
 jp=common_message_entries(clean.read_file(PATH),clean.read_file('/__arm9__.bin'))
 before=owned_entries(common,arm,plan['source_directory_sha256']);source=IlnkContainer.parse(common);authored={}
 for row in doc['records']:
  n=row['message_id'];assert n in IDS and n not in authored
  assert row['source_hex']==jp[n].text.hex()and row['current_hex']==before[n].text.hex()
  assert (jp[n].block,jp[n].block_offset,jp[n].copy_end)==tuple(row['source_reference'][k]for k in('block','offset','copy_end'))
  assert (before[n].block,before[n].block_offset,before[n].copy_end)==tuple(row['current_reference'][k]for k in('block','offset','copy_end'))
  text=compiled(row);assert text.count(b'%s')==jp[n].text.count(b'%s')and b'%'not in text.replace(b'%s',b'')and b'%'not in jp[n].text.replace(b'%s',b'')
  authored[n]=text
 assert set(authored)==IDS
 code=MainCodeFile(arm,BASE)
 for p in plan['patches']:
  section=code.sections[p['section']];at=p['address']-section.ramAddress;old,new=bytes.fromhex(p['source_hex']),bytes.fromhex(p['target_hex'])
  assert len(old)==len(new)and bytes(section.data[at:at+len(old)])==old
  section.data[at:at+len(new)]=new
 target_arm=bytes(code.save());assert sha(target_arm)==conf['target_ARM9_sha256']==plan['target_ARM9_sha256']
 blocks=list(source.blocks);body=bytearray();changed=[]
 for old in before:
  if old.block!=0:continue
  payload=source.blocks[0][old.block_offset:old.copy_end];assert payload==old.text or payload.startswith(old.text+b'\0')
  if old.message_id in authored and authored[old.message_id]!=old.text:
   assert not set(payload[len(old.text)+1:])-{0,32};payload=authored[old.message_id]+b'\0';changed.append(old.message_id)
  assert struct.unpack_from('<H',target_arm,TABLE_OFFSET+old.message_id*2)[0]==len(body);body.extend(payload)
 assert 0<len(body)<=8192;blocks[0]=bytes(body);target_common=IlnkContainer(blocks).to_bytes()
 assert sha(target_common)==conf['target_COMMON_sha256']==plan['target_COMMON_sha256']and changed==plan['actual_text_changed_IDs']
 after=owned_entries(target_common,target_arm,plan['directory_sha256']);assert len(before)==len(after)==3668
 for old,new in zip(before,after,strict=True):
  n=old.message_id;assert new.text==authored.get(n,old.text)
  if n not in changed:assert source.blocks[old.block][old.block_offset:old.copy_end]==blocks[new.block][new.block_offset:new.copy_end]
 assert all(blocks[n]==source.blocks[n]for n in range(1,41))
 # The repack changes only COMMON metadata after the already-tested runtime.
 reverted=MainCodeFile(target_arm,BASE)
 for p in plan['metadata_patches']:
  off=p['address']-BASE;value=bytes.fromhex(p['source_hex']);assert DIRECTORY_OFFSET<=off< DIRECTORY_OFFSET+4 or TABLE_OFFSET<=off<TABLE_OFFSET+2*len([r for r in before if r.block==0]);reverted.sections[0].data[off:off+len(value)]=value
 runtime=read(plan['runtime_plan']);assert bytes(reverted.save())==Path(runtime['research_ARM9']).read_bytes()
 proofs={key:read(value)for key,value in conf['verification'].items()}
 assert proofs['fonts']['ARM9_sha256']==runtime['target_ARM9_sha256']and proofs['routes']['ARM9_sha256']==runtime['target_ARM9_sha256']and proofs['names']['ARM9_sha256']==runtime['target_ARM9_sha256']
 assert proofs['status']['total_cases']==280 and proofs['selector']['total_cases']==128834
 assert len(proofs['routes']['cases'])==148 and not proofs['routes']['errors']and all(r['same_as_explicit_balanced_native_output']for r in proofs['routes']['cases'])
 assert proofs['fonts']['native_count']==122 and all(r['fresh_native_independent_pixel_equality']and r['first_last_glyph_bounds_and_single_panel_pass']for r in proofs['fonts']['planes'])
 assert proofs['copies']['ARM9_sha256']==sha(target_arm)and proofs['copies']['COMMON_sha256']==sha(target_common)and proofs['copies']['complete_native_copies']==7336 and len(proofs['copies']['sequenced_cache_cases'])==180
 assert len(proofs['style']['decisions'])==10 and proofs['style']['all_ten_native_previews_viewed']and proofs['names']['count']==36 and proofs['name_pixels']['native_name_plane_count']==33
 assert len(proofs['name_pixels']['unsupported_stress_cases'])==3 and all(v['pixels_not_approved_for_unsupported_stress_character']for v in proofs['name_pixels']['unsupported_stress_cases'])
 assert proofs['modal']['all3666_unselected_outputs_exact']and proofs['references']['no_external_entry_or_alias_to_relocated_status_data']
 candidate.replace_file(PATH,target_common);candidate.replace_file('/__arm9__.bin',target_arm)
 return dict(manuscript=conf['manuscript'],source_ARM9_sha256=sha(arm),source_COMMON_sha256=sha(common),target_ARM9_sha256=sha(target_arm),target_COMMON_sha256=sha(target_common),selected_IDs=sorted(IDS),actual_text_changed_IDs=changed,changed_records=[{'id':f'COMMON_MESSAGE_{n}'}for n in sorted(IDS)],native_layout_profile=doc['consumer_layout_profile'],all_unselected_complete_copies_and40_other_blocks_exact=True,native_pixel_proof_inherited_over_metadata_only_repack=True,natural_dialogue_v2_and_all_per_record_gates_enforced=True,unsupported_symbol_stress_cases_have_no_pixel_approval=True,actual_gameplay_and_release_verification_not_claimed_here=True,full_goal_complete=False)
