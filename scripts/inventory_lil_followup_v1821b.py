"""Original EV2 state/dependency inventory after the verified Bruges lesson."""
import struct
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_followup_inventory_v1821b')
ROM=Path('out/all_routes_combined_v1807_candidate.nds')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_crew_final_text_v1764_RESEARCH_ONLY')
SNAP=CAP/'frame_041420_arm9_ram.bin'
BASE=0x02000000
SCRATCH=0x02640000

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    current=NdsImage.open(ROM);clean=NdsImage.open('work/clean.nds')
    historical_path=Path('work/analysis/lil_lessons_research_v1761/lil_lessons_V1711_derived_RESEARCH_ONLY.nds')
    historical=NdsImage.open(historical_path);arm=current.read_file('/__arm9__.bin');ev=current.read_file('/data/EV2.DK4')
    assert arm==historical.read_file('/__arm9__.bin')
    assert current.read_file('/data/SC2.DK4')==historical.read_file('/data/SC2.DK4')
    assert ev==clean.read_file('/data/EV2.DK4')==historical.read_file('/data/EV2.DK4')
    report=read(CAP/'capture_report.json');assert report['frames']==41420 and report['cold_boot']and not report['savestate_loaded']
    raw=SNAP.read_bytes();snapshot=next(r for r in report['read_only_pause_RAM_snapshots']if r['frame']==41420)
    assert sha(raw)==snapshot['sha256']and len(raw)==0x400000 and report['ROM_sha256']==sha(historical_path.read_bytes())
    clean_arm=clean.read_file('/__arm9__.bin')
    ranges=[(0x2235C,0x22430),(0x23840,0x23A28)]
    assert all(arm[a:b]==clean_arm[a:b]for a,b in ranges)
    body=ev[96:];counts=struct.unpack_from('<9H',ev,10);starts=struct.unpack_from('<9I',ev,40)
    events=[]
    for category,count in enumerate(counts):
        offset=starts[category]
        for local in range(count):
            word0,word1=struct.unpack_from('<2I',body,offset);length=(word1&255)*4;assert length>=8
            record=body[offset:offset+length];assert len(record)==length
            must=[];must_not=[];following=8
            if word1&(1<<24):
                packed=struct.unpack_from('<H',record,8)[0];yes,no=packed>>8,packed&255
                needed=struct.unpack_from(f'<{yes+no}H',record,10)if yes+no else()
                must=list(needed[:yes]);must_not=list(needed[yes:]);following+=((yes+no)*2+5)&~3
                assert following<=length and all(v<336 or v==0xFFFF for v in(*must,*must_not))
            events.append({'event_ID':len(events),'category':category,'category_local_index':local,'body_offset':offset,
                'source_hex':record.hex(),'source_word0':word0,'source_word1':word1,'source_record_bytes':length,
                'action_index':(word0>>16)&0x3FFF,'must_be_completed':must,'must_not_be_completed':must_not,
                'payload_after_dependency_prefix_hex':record[following:].hex(),
                'additional_native_conditions_not_yet_evaluated':True})
            offset+=length
        assert offset==struct.unpack_from('<I',ev,44+category*4)[0]
    assert len(events)==336
    header=raw.find(ev[:96]);assert header>=0 and raw.find(ev[:96],header+1)<0
    owner=BASE+header-0x34;cpu,get=get_machine(arm,raw);status={0xFFFF:False};assert get(0x23840,owner+4,0xFFFF)==0;action_begin=struct.unpack_from('<I',ev,0x4C)[0]
    for row in events:
        n=row['event_ID'];get(0x23888,SCRATCH,owner+4,n)
        pointer=struct.unpack('<I',cpu.mem_read(SCRATCH,4))[0];assert pointer==BASE+header+96+row['body_offset']
        loaded=bytes(cpu.mem_read(pointer,row['source_record_bytes']));source=bytes.fromhex(row['source_hex'])
        assert loaded[4:]==source[4:]and(struct.unpack_from('<I',loaded)[0]^row['source_word0'])&~0xC0008000==0
        completed=get(0x23840,owner+4,n);assert completed in(0,1);status[n]=bool(completed)
        action=struct.unpack_from('<H',body,action_begin+row['action_index']*2)[0]
        row.update(actual_native_event_pointer=pointer,original_completion_flag=completed,native_action_word=action)
        if action&0xF000==0x2000:row['SC2_action_block']=action&0xFFF
    assert status[22]and status[23]and status[120]
    assert get(0x7F244)==get(0x2E58C)==2
    fleet=get(0xCB1A8)+4+2*132;assert get(0x34674,fleet)==3
    candidates=[];direct=[];blocks=IlnkContainer.parse(current.read_file('/data/SC2.DK4')).blocks
    clean_blocks=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks
    for row in events:
        passes=all(status[n]for n in row['must_be_completed'])and not any(status[n]for n in row['must_not_be_completed'])
        row['original_dependency_gate_passes']=passes
        if not row['original_completion_flag']and passes:
            candidate=dict(row)
            if'SC2_action_block'in row:
                n=row['SC2_action_block'];assert n<len(blocks)
                candidate.update(clean_script_block_sha256=sha(clean_blocks[n]),current_script_block_sha256=sha(blocks[n]),
                    clean_script_block_bytes=len(clean_blocks[n]),current_script_block_bytes=len(blocks[n]))
            candidates.append(candidate)
            if set(row['must_be_completed'])&{23,120}:direct.append(candidate)
    assert bytes(cpu.mem_read(BASE,0x400000))==raw
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    instructions=[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str}
        for a,b in ranges for i in md.disasm(arm[a:b],BASE+a)]
    save(ROOT/'source_event_state_and_dependency_inventory.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'historical_verified_snapshot':str(SNAP),'snapshot_sha256':sha(raw),'historical_snapshot_not_a_new_current_gameplay_visit':True,
        'current_and_snapshot_runtime_SC2_and_EV2_byte_exact':True,'EV2_sha256':sha(ev),'all336_original_events':events,
        'dependency_ready_uncompleted_events_only_not_full_eligibility':candidates,
        'uncompleted_dependency_ready_events_directly_requiring23_or120':direct,
        'current_original_town':3,'captain_ID':2,'original_completed_events22_23_120':True,
        'original_native_dependency_counts_completed_first_then_not_completed_source_bound':True,
        'all336_native_event_getters_match_independent_source_walk_and_state_bits':True,
        'all336_native_completion_getters_all4MiB_unchanged':True,'source_sentinel65535_returns_false_and_is_not_a_real_event_ID':True,'original_dependency_instructions':instructions,
        'no_RNG_event_flag_town_actor_location_script_or_message_override':True,
        'no_next_scene_or_prose_completion_claim_before_remaining_original_conditions_are_mapped':True,
        'next':'Map remaining conditions andnative category/context for the direct dependency-ready candidates before choosing an actual scene. Do not infer sequential block order.',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'original_events':336,'completed':sum(status.values()),'dependency_ready_uncompleted':len(candidates),
        'direct_followups_to23_or120':[{'event':r['event_ID'],'category':r['category'],'SC2_block':r.get('SC2_action_block'),
            'must':r['must_be_completed'],'must_not':r['must_not_be_completed']}for r in direct],
        'not_full_eligibility_or_next_scene_claim':True},flush=True)
