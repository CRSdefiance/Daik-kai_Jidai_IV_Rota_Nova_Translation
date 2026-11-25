"""Inventory one source-bound anonymous speaker label without adopting a replacement."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/collapsed_speaker_lead_v5832')
SOURCE=Path('work/analysis/lil_B200_source_v5826/all19_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B200_names_v5831/four_original_progressive_and_catalogue_name_consumers.json')
GLOSS=Path('work/analysis/lil_B200_clean_context_v5825/all19_clean_collapse_inn_recovery_declined_reward_and_Charm_glosses.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,names,gloss=map(read,[SOURCE,NAMES,GLOSS])
    clean,current=NdsImage.open('work/clean.nds'),NdsImage.open(packet['current_ROM'])
    original,arm=clean.read_file('/__arm9__.bin'),current.read_file('/__arm9__.bin')
    inventory,walker,invsource=scoped_inventory();signature=bytes.fromhex('0040ffff00ac');blocks=[];total=0
    for route in range(4):
        file=f'/data/SC{route}.DK4';data=clean.read_file(file);bank=IlnkContainer.parse(data).blocks;total+=len(bank)
        for number,blob in enumerate(bank):
            if signature not in blob:continue
            commands,speeches=inventory(original,blob);records=[]
            for speech in speeches:
                at=speech['offset']+5;end=blob.index(0,at+1);value=blob[at:end]
                records.append(dict(source_record_index=blob[:at].count(b'\0'),source_selector=value[0],source_hex=value.hex(),
                    complete_preamble_hex=blob[at-5:at+1].hex(),Japanese=value[1:].decode('cp932'),
                    source_reference=dict(file_path=file,block=number,offset=at,bytes=len(value),header_offset=at-5)))
            direct=[r for r in records if r['source_selector']==172]
            if direct:blocks.append(dict(file_path=file,block=number,source_file_sha256=sha(data),source_block_sha256=sha(blob),
                source_block_hex=blob.hex(),all_native_commands=commands,all_speech_records=records,direct_role_speeches=direct))
    assert total==1307
    source_fields=[]
    for ident in [19,172]:
        fields=[]
        for delta in [0,4,8]:
            field=0x120B80+ident*32+delta;pointer=struct.unpack_from('<I',original,field)[0]
            if pointer:
                at=pointer-0x02000000;value=original[at:original.index(0,at)+1]
                fields.append(dict(pointer_field=field,pointer=pointer,storage_offset=at,terminated_hex=value.hex(),Japanese=value[:-1].decode('cp932')))
            else:fields.append(dict(pointer_field=field,null=True))
        source_fields.append(dict(actor_ID=ident,source_file='/__arm9__.bin',source_fields=fields))
    expected={19:'Carlo Sinat',172:'Collapsed Person'}
    assert names['progressive_nameplate_values']==names['full_catalogue_values']=={str(k):v for k,v in expected.items()}
    sections=MainCodeFile(arm,0x02000000).sections;payload=bytes(sections[3].data[:-48]);assert len(payload)==123040 and sections[3].ramAddress==0x023A7200
    ident=172;field=0x120B80+ident*32;pointer=struct.unpack_from('<I',arm,field)[0];value=expected[ident].encode()+b'\0';at=pointer-0x02387A20
    assert payload[at:at+len(value)]==value
    literal_hits=[i for i in range(len(arm)-3) if arm[i:i+4]==struct.pack('<I',pointer)];assert literal_hits==[field]
    aliases=[]
    for actor in range(207):
        for delta in [0,4,8]:
            f=0x120B80+actor*32+delta;p=struct.unpack_from('<I',arm,f)[0]
            if pointer<=p<pointer+len(value):aliases.append(dict(actor_ID=actor,field=f,pointer=p,interior_delta=p-pointer))
    assert aliases==[dict(actor_ID=172,field=field,pointer=pointer,interior_delta=0)]
    # Bind identical source exchanges by both all speech bytes and full command bytes.
    own=next(b for b in blocks if b['file_path']=='/data/SC2.DK4' and b['block']==200)
    assert own['source_block_sha256']==packet['blocks'][0]['clean_block_sha256']
    assert [r['source_hex'] for r in own['all_speech_records']]==[r['source_hex'] for r in gloss['records']]
    groups={}
    for b in blocks:groups.setdefault(b['source_block_sha256'],[]).append(dict(file_path=b['file_path'],block=b['block']))
    ROOT.mkdir(parents=True);save(ROOT/'all_route_literal_uses_exact_name_fields_and_localization_finding.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),clean_ARM9_sha256=sha(original),current_ARM9_sha256=sha(arm),
        source_blocks_scanned=total,selected_native_blocks=blocks,exact_whole_block_identity_groups=groups,source_name_fields=source_fields,
        current_primary_name_owner=dict(actor_ID=172,pointer_field=field,runtime_pointer=pointer,current_English=expected[172],terminated_hex=value.hex(),
            staged_payload_offset=at,staged_payload_bytes=len(value),literal_ARM9_pointer_occurrences=literal_hits,all207_primary_secondary_middle_aliases=aliases),
        current_native_name_consumers=str(NAMES),current_native_name_consumers_sha256=sha(NAMES.read_bytes()),
        finding='Collapsed Person literally describes the triggering condition and sounds like an internal scene label. The same anonymous speaker wakes,asks questions and offers thanks while the nameplate getter still returns Collapsed Person. Review a natural anonymous label across every distinct clean exchange;do not infer gender,age,occupation,travel status,marriage or a diagnosis.',
        proposed_wording_not_selected=True,Stranger_is_a_contextual_candidate_only_requires_all_distinct_exchange_review=True,
        no_global_substitution_no_target_bytes_no_new_name_editorial_completion_credit=True,
        complete_B200_gloss_already_read_before_old_English=True,
        literal_full_preamble_prefilter_then_original_native_inventory_confirms_reported_uses=True,
        literal_census_not_exhaustive_dynamic_selector_or_other_UI_consumer_proof=True,
        actual_B200_nameplate_display_not_yet_observed=True,target_native_display_substitutions_and_registered_release_pending=True,
        clean_inventory_walker=walker,clean_inventory_function=invsource,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAMES,GLOSS,Path(__file__)]},new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,full_goal_complete=False))
    print('172 source fields',source_fields[1]['source_fields'])
    print('literal source uses',[(b['file_path'],b['block'],len(b['direct_role_speeches']),len(b['all_speech_records'])) for b in blocks])
    print('distinct complete source blocks',len(groups),'No replacement selected,ROM changed or name-review credit added.')
