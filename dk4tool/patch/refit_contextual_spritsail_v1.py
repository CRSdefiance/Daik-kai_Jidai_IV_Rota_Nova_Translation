"""Source-locked Refit review: two bounded help paragraphs and one label."""
from pathlib import Path
from dk4tool.dialogue.refit_help import compile_paragraph
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries as previous_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries,DIRECTORY_OFFSET,TABLE_OFFSET
from scripts.verify_village_wrap_v608 import read
CONFIG='translations/refit_contextual_spritsail_release_v1.json'
PATH='/COMMON/MESFILE.DK4'

def current_entries(common,arm):
 conf=read(CONFIG);assert sha(common)==conf['target_COMMON_sha256']and sha(arm)==conf['target_ARM9_sha256']
 return owned_entries(common,arm,conf['directory_sha256'])

def apply_release(candidate,baseline,path=CONFIG):
 conf=read(path);assert conf['format']=='dk4-refit-contextual-spritsail-v1'
 for name,digest in conf['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
 arm,common=candidate.read_file('/__arm9__.bin'),candidate.read_file(PATH)
 assert sha(arm)==conf['source_ARM9_sha256']and sha(common)==conf['source_COMMON_sha256']
 assert sha(baseline.read_file(PATH))==conf['canonical_COMMON_sha256']
 doc=read(conf['manuscript']);validate_natural_dialogue_batch(doc);assert not doc['formatting_review_pending']and doc['revised_IDs']==[1268,1280]and doc['retained_count']==41
 clean=NdsImage.open('work/clean.nds');assert sha(Path('work/clean.nds').read_bytes())==doc['source_ROM_sha256']
 jp=common_message_entries(clean.read_file(PATH),clean.read_file('/__arm9__.bin'));canonical=common_message_entries(baseline.read_file(PATH),baseline.read_file('/__arm9__.bin'),clean=False);before=previous_entries(common,arm)
 assert [r['message_id']for r in doc['records']]==list(range(1247,1290))
 authored={}
 for row in doc['records']:
  n=row['message_id'];help_record=n not in range(1256,1268)
  assert row['source_hex']==jp[n].text.hex()and row['canonical_source_hex']==canonical[n].text.hex()and row['current_hex']==before[n].text.hex()
  for prefix,e in(('source',jp[n]),('current',before[n])):assert tuple(row[prefix+'_reference'][k]for k in('block','offset','copy_end'))==(e.block,e.block_offset,e.copy_end)
  english=row['english'];assert english and english.isascii()and english==' '.join(english.split())and not any(c in english for c in'{}\r\n')
  payload=compile_paragraph(english)[0][:-1]if help_record else b' '+english.encode('ascii')
  if n in(1268,1280):assert row['editorial_decision']=='revise'and b'spritsail'in payload and b'split sail'not in payload;authored[n]=payload
  else:assert payload==before[n].text and row['editorial_decision']=='retain-wording'and row['fresh_retained_wording_justification']
 source=IlnkContainer.parse(common);blocks=list(source.blocks);plan=read(conf['payload_plan']);assert len(plan['COMMON_patches'])==2
 for p in plan['COMMON_patches']:
  n=p['message_ID'];e=before[n];lo,hi=e.block_offset,e.copy_end
  assert n in authored and(p['block'],p['offset'],p['copy_end'])==(e.block,lo,hi)
  old=blocks[e.block][lo:hi];assert old.hex()==p['source_hex']and old==e.text+b'\0'
  value=authored[n]+b'\0';assert len(value)<=hi-lo;value+=bytes(hi-lo-len(value));assert value.hex()==p['target_hex']
  assert not any(r.message_id!=n and r.block==e.block and max(lo,r.block_offset)<min(hi,r.copy_end)for r in before)
  blocks[e.block]=blocks[e.block][:lo]+value+blocks[e.block][hi:]
 target_common=IlnkContainer(blocks).to_bytes();label=plan['ARM9_patch'];lo,hi=label['offset'],label['end'];assert(lo,hi)==(0x133234,0x133240)
 assert arm[lo:hi]==bytes.fromhex(label['source_hex'])==b'Split Sail\0\0'and bytes.fromhex(label['target_hex'])==b'Spritsail\0\0\0'
 assert clean.read_file('/__arm9__.bin')[0x13322C:0x133240].split(b'\0')[0].decode('cp932')=='スプリットセイル'
 target_arm=arm[:lo]+bytes.fromhex(label['target_hex'])+arm[hi:];assert sha(target_arm)==conf['target_ARM9_sha256']and sha(target_common)==conf['target_COMMON_sha256']
 assert sha(arm[DIRECTORY_OFFSET:TABLE_OFFSET])==conf['directory_sha256']and target_arm[DIRECTORY_OFFSET:TABLE_OFFSET]==arm[DIRECTORY_OFFSET:TABLE_OFFSET]
 after=owned_entries(target_common,target_arm,conf['directory_sha256']);assert len(before)==len(after)==3668
 for a,b in zip(before,after,strict=True):
  assert(a.block,a.block_offset,a.copy_end)==(b.block,b.block_offset,b.copy_end)and b.text==authored.get(a.message_id,a.text)
  if a.message_id not in authored:assert source.blocks[a.block][a.block_offset:a.copy_end]==blocks[b.block][b.block_offset:b.copy_end]
 assert all(a==b for i,(a,b)in enumerate(zip(source.blocks,blocks,strict=True))if i!=16)and all(len(a)==len(b)for a,b in zip(source.blocks,blocks,strict=True))
 proof=read(conf['offline_approval']);assert proof['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes())and proof['research_ARM9_sha256']==sha(target_arm)and proof['research_COMMON_sha256']==sha(target_common)
 assert proof['all43_individual_source_context_localization_naturalness_and_formatting_gates']and len(proof['all86_cold_warm_native_copies'])==86 and len(proof['all10_help_spoken_and_current_actual_sheets_viewed'])==10
 fonts=read(conf['help_fonts']);assert len(fonts['records'])==31 and all(r['complete_independent_font_plane_equal']and r['text_and_pixel_guards_and_ABI_preserved']for r in fonts['records'])
 docrows={r['message_id']:r for r in doc['records']}
 assert all(r['English']==docrows[r['message_id']]['english']for r in fonts['records'])
 candidate.replace_file(PATH,target_common);candidate.replace_file('/__arm9__.bin',target_arm)
 return dict(manuscript=conf['manuscript'],source_ARM9_sha256=sha(arm),source_COMMON_sha256=sha(common),target_ARM9_sha256=sha(target_arm),target_COMMON_sha256=sha(target_common),selected_IDs=list(range(1247,1290)),actual_text_changed_IDs=[1268,1280],changed_records=[dict(id=f'COMMON_MESSAGE_{n}')for n in(1268,1280)],auxiliary_ARM9_label='Spritsail',only_two_complete_owned_COMMON16_copies_and12_owned_label_bytes_changed=True,all3666_other_complete_copies_and_metadata_exact=True,no_code_font_geometry_section_or_staged_pool_change=True,all43_per_record_v2_gates=True,revised_actual_component_widget_and_help_gameplay_pending=True,full_goal_complete=False)
