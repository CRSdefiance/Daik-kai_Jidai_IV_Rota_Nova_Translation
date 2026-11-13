"""Dependency-backed B24 source inventory andactual original town predicates."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_lessons_v1717 import inventory
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B24_source_v1822')
ROM=Path('out/all_routes_combined_v1807_candidate.nds')
PRIOR=Path('work/analysis/lil_followup_inventory_v1821b/source_event_state_and_dependency_inventory.json')

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    proof=read(PRIOR);assert len(proof['uncompleted_dependency_ready_events_directly_requiring23_or120'])==1
    spec=proof['all336_original_events'][24];assert spec['SC2_action_block']==24 and spec['category']==5 and spec['must_be_completed']==[120]
    current=NdsImage.open(ROM);clean=NdsImage.open('work/clean.nds');arm=current.read_file('/__arm9__.bin')
    source=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[24]
    target=IlnkContainer.parse(current.read_file('/data/SC2.DK4')).blocks[24]
    a,speeches=inventory(clean.read_file('/__arm9__.bin'),source);b,now_speeches=inventory(arm,target)
    shape=lambda rows:[(r['offset'],r['word'],r['native_extent'],r['ancestor_0100_offsets'])for r in rows]
    assert shape(a)==shape(b)
    records=[]
    for old,new in zip(speeches,now_speeches,strict=True):
        at=old['offset']+5;before=source[at:source.index(b'\0',at)];now=target[at:target.index(b'\0',at)]
        assert before[0]==now[0]and before[0]in(2,9)
        index=source[:at].count(b'\0');current_index=target[:at].count(b'\0')
        records.append({'id':f'DK4_MES_B24_R{index:04d}','file_path':'/data/SC2.DK4','block':24,'record_index':index,
            'source_reference':{'offset':at,'bytes':len(before),'header_offset':at-5},
            'current_reference':{'offset':at,'bytes':len(now),'header_offset':at-5,'record_index':current_index},
            'source_hex':before.hex(),'source_presentation_prefix_hex':before[:1].hex(),
            'source_complete_preamble_hex':source[at-5:at+1].hex(),'source_Japanese':before[1:].decode('cp932'),
            'current_text_hex':now.hex(),'current_complete_preamble_hex':target[at-5:at+1].hex(),
            'current_stored_English':now[1:].decode('cp932'),'speaker':'Lil Argot'if before[0]==2 else'Camille',
            'ancestor_0100_offsets':old['ancestor_0100_offsets'],
            'native_command_extent':old['native_extent'],'not_yet_a_source_prose_or_formatting_review':True})
    raw=Path(proof['historical_verified_snapshot']).read_bytes();assert sha(raw)==proof['snapshot_sha256']
    ev=current.read_file('/data/EV2.DK4');header=raw.find(ev[:96]);assert header>=0
    body=ev[96:];offset=struct.unpack_from('<I',ev,0x54)[0];cpu,get=get_machine(arm,raw);conditions=[]
    for number,comparison in((16,0),(14,1)):
        pointer=0x02000000+header+96+offset+number*4;word=struct.unpack_from('<I',body,offset+number*4)[0]
        cpu.mem_write(0x02640000,struct.pack('<2I',0x021343F8,pointer));value=get(0x256A0,0x02640000)
        accepted=get(0x2A690,value,comparison)
        conditions.append({'condition_ID':number,'source_word':word,'actual_native_value':value,
            'comparison_category':comparison,'native_comparison_pass':accepted})
    assert[hex(r['source_word'])for r in conditions]==['0x91020003','0x3000fe09']
    assert[(r['actual_native_value'],r['native_comparison_pass'])for r in conditions]==[(1,0),(1,1)]
    assert bytes(cpu.mem_read(0x02000000,0x400000))==raw
    save(ROOT/'B24_clean_current_native_source_and_town_predicates.json',{'format':'dk4-editorial-source-context-packet-v1',
        'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'file_path':'/data/SC2.DK4','block':24,'clean_block_sha256':sha(source),'current_block_sha256':sha(target),
        'clean_block_bytes':len(source),'current_block_bytes':len(target),'all_clean_native_commands':a,'all_current_native_commands':b,
        'all_command_offsets_extents_and_ancestors_match':True,'all_speech_headers_match_independent_raw_scan':True,
        'records':records,'source_event24':spec,'known_original_completed_dependency120':True,
        'native_conditions_at_verified_Bruges_snapshot':conditions,
        'condition16':'Same original type9/subtype1 fleet-town equality predicate as condition15,but compares town3 Bruges instead of town2 Amsterdam. Comparison0 requires false.',
        'condition14':'Original actor9 presence predicate remains true;Camille is present. Comparison1 requires true.',
        'blocked_at_current_Bruges_town_by_original_condition16':True,
        'source_event24_has_additional_context_prefix_00FFFFFF_not_fully_mapped':True,
        'full_original_trigger_eligibility_and_actual_B24_activation_still_unverified':True,
        'historical_snapshot_not_a_new_current_gameplay_visit':True,'input_entire4MiB_unchanged':True,
        'native_inventory_maps_structure_not_scene_execution_or_branch_reachability':True,
        'no_ROM_prose_ledger_credit_or_gameplay_mutation':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'B24_commands':len(a),'B24_speeches':len(records),'native_current_town_condition_blocks_Bruges':True,
        'next_original_scene_activation_not_yet_claimed':True},flush=True)
    for row in records:print(row['id'],row['speaker'],row['source_Japanese'].replace('\n',' / '),'==>',row['current_stored_English'].strip(),flush=True)
