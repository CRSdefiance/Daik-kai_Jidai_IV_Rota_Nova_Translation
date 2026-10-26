"""Source-locked shared-town61 review with two revisions and bounded selector codec."""
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
from scripts.town_trend_balanced_runtime_v2162 import decode
CONFIG='translations/town_trade_port_contextual_editorial_release_v1.json';PATH='/COMMON/MESFILE.DK4';BASE=0x02000000
IDS=set(range(765,820))|{267,653,654,655,1245,1246};CHANGED={654,655}

def apply_release(candidate,baseline,path=CONFIG):
 conf=read(path);assert conf['format']=='dk4-town-trade-port-contextual-editorial-v1'
 for name,digest in conf['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
 common,arm=candidate.read_file(PATH),candidate.read_file('/__arm9__.bin');assert sha(common)==conf['source_COMMON_sha256']and sha(arm)==conf['source_ARM9_sha256'];assert sha(baseline.read_file(PATH))==conf['canonical_COMMON_sha256']
 doc=read(conf['manuscript']);validate_natural_dialogue_batch(doc);assert doc['translation_policy']=='natural-dialogue-v2'and not doc['formatting_review_pending'];assert sha(Path('work/clean.nds').read_bytes())==doc['source_ROM_sha256']
 plan=read(conf['payload_plan']);runtime=read(plan['runtime_plan']);assert sha(Path(plan['runtime_plan']).read_bytes())==plan['runtime_plan_sha256'] and plan['runtime_patches']==runtime['patches'];assert runtime['source_ARM9_sha256']==sha(arm)==plan['source_ARM9_sha256'];assert plan['actual_text_changed_IDs']==[654,655]and len(runtime['patches'])==7 and runtime['table_bytes_before_after']==[212,212]and runtime['gate_bytes_before_after']==[172,172]
 clean=NdsImage.open('work/clean.nds');jp=common_message_entries(clean.read_file(PATH),clean.read_file('/__arm9__.bin'));before=owned_entries(common,arm,plan['source_directory_sha256']);source=IlnkContainer.parse(common);authored={};selected=set()
 for row in doc['records']:
  n=row['message_id'];assert n in IDS and n not in selected;selected.add(n);assert row['source_hex']==jp[n].text.hex()and row['current_hex']==before[n].text.hex()
  for label,entry in(('source',jp[n]),('current',before[n])):assert tuple(row[label+'_reference'][k]for k in('block','offset','copy_end'))==(entry.block,entry.block_offset,entry.copy_end)
  text=row['english'];assert text.endswith('{PAD}')and text.count('{PAD}')==1;text=text.removesuffix('{PAD}');assert text and text.isascii()and text==' '.join(text.split())and len(text)<236 and not any(c in text for c in'{}\r\n')and text.count('%s')==jp[n].text.count(b'%s')and'%'not in text.replace('%s','')
  if n in CHANGED:assert row['editorial_decision']=='revise';authored[n]=b' '+text.encode('ascii')
  else:assert row['editorial_decision']=='retain-wording'and row['fresh_retained_wording_justification']and' '.join(before[n].text.decode('cp932').split())==text
 assert selected==IDS and set(authored)==CHANGED
 historical=read('work/analysis/recruitment_owned_v772/owned_runtime_plan.json')['private_spans'];town=read('work/analysis/town_services_runtime_v2080/runtime_plan.json');table=next(p for p in town['patches']if p['address']==0x02147B9C)
 assert len(bytes.fromhex(table['target_hex']))==212 and arm[0x147B9C:0x147C70]==bytes.fromhex(table['target_hex'])
 for p in runtime['patches']:
  a=p['address'];size=len(bytes.fromhex(p['target_hex']));assert (a==0x02147B9C and size==212)or any(lo<=a<a+size<=hi for lo,hi in historical)
 code=MainCodeFile(arm,BASE)
 for p in plan['metadata_patches']+runtime['patches']:
  at=p['address']-BASE;old,new=bytes.fromhex(p['source_hex']),bytes.fromhex(p['target_hex']);assert p['section']==0 and len(old)==len(new)and bytes(code.sections[0].data[at:at+len(old)])==old
  if p in plan['metadata_patches']:assert DIRECTORY_OFFSET+28<=at<DIRECTORY_OFFSET+32 or any(TABLE_OFFSET+r.message_id*2==at for r in before if r.block==7)
  code.sections[0].data[at:at+len(new)]=new
 target_arm=bytes(code.save());assert sha(target_arm)==plan['target_ARM9_sha256']==conf['target_ARM9_sha256'];assert decode(target_arm[0x147B9C:0x147C70])==(list(map(lambda r:(r[0],r[1],r[2],tuple(r[3])),runtime['logical_rows'])),212)
 blocks=list(source.blocks);rows=[r for r in before if r.block==7];body=bytearray(blocks[7][:rows[0].block_offset])
 for r in rows:
  payload=blocks[7][r.block_offset:r.copy_end]
  if r.message_id in authored:assert not set(payload[len(r.text)+1:])-{0,32};payload=authored[r.message_id]+b'\0'
  assert struct.unpack_from('<H',target_arm,TABLE_OFFSET+r.message_id*2)[0]==len(body);body.extend(payload)
 assert len(body)==4472 and len(body)<=8192;blocks[7]=bytes(body);target_common=IlnkContainer(blocks).to_bytes();assert sha(target_common)==plan['target_COMMON_sha256']==conf['target_COMMON_sha256'];after=owned_entries(target_common,target_arm,plan['directory_sha256']);assert len(before)==len(after)==3668
 for old,new in zip(before,after,strict=True):
  assert new.text==authored.get(old.message_id,old.text)
  if old.message_id not in CHANGED:assert source.blocks[old.block][old.block_offset:old.copy_end]==blocks[new.block][new.block_offset:new.copy_end]
 assert all(blocks[b]==source.blocks[b]for b in range(41)if b!=7)
 reverted=MainCodeFile(target_arm,BASE)
 for p in plan['metadata_patches']+runtime['patches']:
  at=p['address']-BASE;value=bytes.fromhex(p['source_hex']);reverted.sections[0].data[at:at+len(value)]=value
 assert bytes(reverted.save())==arm and len(code.sections[3].data)-48==123040 and all(bytes(a.data)==bytes(b.data)for a,b in zip(code.sections[1:],MainCodeFile(arm,BASE).sections[1:],strict=True))
 proofs={k:read(v)for k,v in conf['verification'].items()};fonts=proofs['fonts'];assert fonts['ARM9_sha256']==sha(target_arm)and fonts['COMMON_sha256']==sha(target_common)and len(fonts['all32552_layouts'])==32552 and fonts['full_font_count']==203 and len(fonts['physical_sheets'])==17
 assert all(r['fresh_actual_target_native_layout_equal_expected']and r['native_production_control']['complete']and r['physical_native_independent_full_ink_shadow_equal']for r in fonts['full_font_samples'])
 assert proofs['predicates']['total_cases']==1057968 and proofs['predicates']['allR0_toR11_including_R2_and_SP_LR_preserved']and proofs['predicates']['all_input_stack_fields_unchanged']
 assert proofs['references']['only_public_ENTRY_start_is_called_externally']and proofs['references']['no_external_interior_entry_or_data_alias_to_reencoded_table_gate_or_changed_stack_bridges']and proofs['references']['Thumb1_and_ARMv5_BL_BLX_only']
 assert proofs['copies']['ARM9_sha256']==sha(target_arm)and proofs['copies']['COMMON_sha256']==sha(target_common)and proofs['copies']['complete_native_copies']==7336 and len(proofs['copies']['sequenced_cache_cases'])==180
 approval=proofs['formatting'];assert approval['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes())and approval['all203_native_physical_planes_on17sheets_viewed']and approval['all248revisedproductlayouts_no_style_findings_or_waivers']and proofs['modal']['actual_bounds']==[0,0,228,48]and proofs['modal']['first_glyph_x']==0
 candidate.replace_file(PATH,target_common);candidate.replace_file('/__arm9__.bin',target_arm)
 return dict(manuscript=conf['manuscript'],source_ARM9_sha256=sha(arm),source_COMMON_sha256=sha(common),target_ARM9_sha256=sha(target_arm),target_COMMON_sha256=sha(target_common),selected_IDs=sorted(IDS),actual_text_changed_IDs=sorted(CHANGED),changed_records=[dict(id=f'COMMON_MESSAGE_{n}')for n in sorted(IDS)],native_layout_profile=doc['consumer_layout_profile'],only_two_paragraphs_COMMON7_metadata_and_seven_owned_selector_stack_spans_changed=True,all3666_other_complete_copies_and40_other_blocks_exact=True,all_font_geometry_sections_cache_and123040_staged_bytes_preserved=True,native_selector_cases=1057968,full_font_samples=203,all61_v2_per_record_gates_enforced=True,revised_actual_gameplay_and_release_verification_not_claimed_here=True,full_goal_complete=False)
