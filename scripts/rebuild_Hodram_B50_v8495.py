"""Bind complete B50 source/current/final command maps andboth block/whole image inverses;research archive only."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B50_rebuild_v1 import rebuild
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B50_relocation_v8495')
DOC=Path('translations/hodram_B50_editorial_manuscript_v2.json')
CURRENT=Path('work/analysis/Hodram_B50_current_v8488/current_effective.json')
SOURCE=Path('work/analysis/Hodram_B50_source_controls_v8486/source_controls.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,current,controls=map(read,[DOC,CURRENT,SOURCE]);image=NdsImage.open(doc['current_ROM']);clean=NdsImage.open('work/clean.nds');arm=image.read_file('/__arm9__.bin');archive=image.read_file('/data/SC1.DK4');before_ROM=bytes(image.rom.save())
    assert sha(before_ROM)==doc['current_ROM_sha256']==current['current_ROM_sha256'] and sha(archive)==doc['current_archive_sha256']==current['current_archive_sha256']
    packet=current['groups'][0];old=IlnkContainer.parse(archive).blocks[50];japanese=IlnkContainer.parse(clean.read_file('/data/SC1.DK4')).blocks[50]
    assert old.hex()==packet['current_block_hex'] and japanese.hex()==packet['clean_block_hex'] and controls['candidate_sha256']==doc['current_ROM_sha256']
    result=rebuild(archive,arm,doc['records']);assert len(result['groups'])==1 and result['unchanged_archive_blocks']==324;group=result['groups'][0];target=group['target_block'];inventory,_,_=scoped_inventory()
    sourcecommands,sourcespeeches=inventory(arm,japanese);assert sourcecommands==packet['all_source_commands']==controls['groups'][0]['all_original_source_commands'] and len(sourcespeeches)==3
    assert group['all_current_commands']==packet['all_current_commands'] and len(group['all_target_commands'])==12 and not group['relative_fixups']
    for source,previous,final,mapping in zip(sourcecommands,group['all_current_commands'],group['all_target_commands'],group['command_map'],strict=True):
        assert source['word']==previous['word']==final['word']==mapping['word']
        if source['word']==0x4000:assert source['whole_command_hex'][:12]==previous['whole_command_hex'][:12]==final['whole_command_hex'][:12]
        else:assert source['whole_command_hex']==previous['whole_command_hex']==final['whole_command_hex']
    refs={r['id']:r for r in group['text_records']};restored=bytearray(target[:group['target_logical_end']]);restored[:8]=japanese[:8]
    records=[]
    for row in sorted(doc['records'],key=lambda r:refs[r['id']]['new_offset'],reverse=True):
        ref=refs[row['id']];at=ref['new_offset'];restored[at:at+ref['new_length']]=bytes.fromhex(row['source_hex'])
    source_end=8+struct.unpack_from('<H',japanese,4)[0];assert bytes(restored)+japanese[source_end:]==japanese
    for row in doc['records']:
        ref=refs[row['id']];at=ref['new_offset'];value=bytes.fromhex(ref['target_hex']);assert target[at:at+len(value)+1]==value+b'\0' and target[at-5:at+1].hex()==row['source_complete_preamble_hex']
        records.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],final_reference=dict(file_path='/data/SC1.DK4',block=50,offset=at,bytes=len(value),header_offset=at-5,record_index=ref['new_record_index'],target_block_sha256=sha(target)),source_hex=row['source_hex'],current_hex=row['current_hex'],compiled_hex=row['compiled_hex'],stored_hex=ref['target_hex'],parity_space_added=ref['parity_space_added']))
    planned=deepcopy(image);planned.replace_file('/data/SC1.DK4',result['target_archive']);inverse=deepcopy(planned);inverse.replace_file('/data/SC1.DK4',archive)
    assert bytes(inverse.rom.save())==before_ROM and [p for _,p,v in image.iter_files() if planned.read_file(p)!=v]==['/data/SC1.DK4'] and all(planned.read_file(p)==v for p,v in image.iter_components())
    ROOT.mkdir(parents=True);bp=ROOT/'SC1_B50_RESEARCH_ONLY.bin';bp.write_bytes(target);ap=ROOT/'SC1_B50_RESEARCH_ONLY.DK4';ap.write_bytes(result['target_archive'])
    serial={k:v for k,v in group.items() if k!='target_block'};serial.update(file_path='/data/SC1.DK4',target_block=str(bp),clean_block_sha256=sha(japanese),complete_clean_source_block_inverse_exact=True)
    save(ROOT/'reconstruction.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),file_path='/data/SC1.DK4',source_archive_sha256=sha(archive),target_archive=str(ap),target_archive_sha256=sha(result['target_archive']),groups=[serial],records=records,all12_commands3_fullpreambles_6_opaque_effects_item148_show_hide_full_end_andtails_preserved=True,source_relative_sites=0,source_query_sites=0,source_typed_choice_sites=0,other324_blocks_andall_other_files_components_exact=True,complete_clean_current_block_archive_andwhole_inmemory_ROM_inverses_exact=True,research_whole_ROM_sha256=sha(bytes(planned.rom.save())),whole_ROM_not_written_orregistered=True,stored_parity_native_ink_controls_actual_policy_atomic_andregistered_gates_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [DOC,CURRENT,SOURCE,Path('dk4tool/patch/hodram_B50_rebuild_v1.py'),Path(__file__)]}))
    print('B50whole block/archive reconstructed:',group['target_bytes'],'storedbytes',group['target_tail_bytes'],'tail;12commands/3preambles/324unownedblocks/fullclean-current-archive-ROMinverses pass.Parities:',[r['id'] for r in records if r['parity_space_added']],';no ROM orcredit.')
