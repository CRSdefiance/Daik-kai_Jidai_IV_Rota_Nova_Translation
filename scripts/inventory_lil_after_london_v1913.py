"""Original336 event/state inventory after actual London return86310."""
from copy import deepcopy
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_after_London_inventory_v1913')
ROM=Path('out/all_routes_combined_v1909_candidate.nds')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_London_revised_run_v1903_RESEARCH_ONLY')
SNAP=CAP/'frame_086310_arm9_ram.bin'
PRIOR=Path('work/analysis/lil_followup_inventory_v1821b/source_event_state_and_dependency_inventory.json')
BASE=0x02000000;SCRATCH=0x02640000

if __name__=='__main__':
    assert not ROOT.exists()
    im=NdsImage.open(ROM);clean=NdsImage.open('work/clean.nds');arm=im.read_file('/__arm9__.bin');ev=im.read_file('/data/EV2.DK4')
    report=read(CAP/'capture_report.json');assert report['frames']==86310 and report['cold_boot']and not report['savestate_loaded']
    assert sha(ROM.read_bytes())==report['ROM_sha256']
    raw=SNAP.read_bytes();assert len(raw)==0x400000
    assert any(r.get('frame')==86310 and r['sha256']==sha(raw)for r in report['read_only_pause_RAM_snapshots'])
    original=read(PRIOR);assert sha(ev)==original['EV2_sha256']and ev==clean.read_file('/data/EV2.DK4')
    for a,b in [(0x220D8,0x22ECC),(0x23840,0x23A28),(0x256A0,0x256D0),(0x2A690,0x2A6C0)]:
        assert arm[a:b]==clean.read_file('/__arm9__.bin')[a:b]
    header=raw.find(ev[:96]);assert header>=0 and raw.find(ev[:96],header+1)<0
    owner=BASE+header-0x34;cpu,get=get_machine(arm,raw)
    assert list(struct.unpack('<2I',cpu.mem_read(owner+0x2454,8)))==[5,0]
    assert get(0x2E58C)==get(0x7F244)==2
    fleet=get(0xCB1A8)+4+2*132;assert get(0x34674,fleet)==0
    events=deepcopy(original['all336_original_events']);status={65535:False}
    for row in events:
        n=row['event_ID'];get(0x23888,SCRATCH,owner+4,n)
        pointer=struct.unpack('<I',cpu.mem_read(SCRATCH,4))[0]
        assert pointer==BASE+header+96+row['body_offset']
        value=bytes(cpu.mem_read(pointer,row['source_record_bytes']));expected=bytes.fromhex(row['source_hex'])
        assert value[4:]==expected[4:]and(struct.unpack_from('<I',value)[0]^row['source_word0'])&~0xC0008000==0
        complete=get(0x23840,owner+4,n);assert complete in(0,1);status[n]=bool(complete)
        row.update(actual_native_event_pointer=pointer,original_completion_flag=complete)
        row.pop('additional_native_conditions_not_yet_evaluated',None)
    assert status[22]and status[23]and status[24]and status[120]
    assert bytes(cpu.mem_read(BASE,0x400000))==raw
    blocks=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks
    jp=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks
    ready=[];town_cases=[];errors=[]
    for row in events:
        passes=all(status[n]for n in row['must_be_completed'])and not any(status[n]for n in row['must_not_be_completed'])
        row['original_dependency_gate_passes']=passes
        if row['original_completion_flag']or not passes:continue
        candidate=dict(row)
        if 'SC2_action_block'in row:
            b=row['SC2_action_block'];candidate.update(clean_script_block_sha256=sha(jp[b]),
                current_script_block_sha256=sha(blocks[b]),clean_script_block_bytes=len(jp[b]),current_script_block_bytes=len(blocks[b]))
        ready.append(candidate)
        if row['category']!=5:continue
        # Original owner category/context remain5/London0;no hypothetical edits.
        cpu,get=get_machine(arm,raw);get(0xCC9A8,SCRATCH+0x80,get(0xCB1B4))
        try:
            result=get(0x220D8,owner,row['actual_native_event_pointer'],SCRATCH+0x80,0)
            assert result in(0,1)
            assert bytes(cpu.mem_read(BASE,0x400000))==raw
        except Exception as error:
            errors.append({'event_ID':row['event_ID'],'error':str(error),'not_eligibility_or_unused_claim':True});continue
        town_cases.append({'event_ID':row['event_ID'],'SC2_block':row.get('SC2_action_block'),
            'full_original_predicate_result':result,'all4MiB_unchanged':True})
    ROOT.mkdir(parents=True)
    save(ROOT/'all336_states_and_original_London_town_eligibility.json',{
        'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'ARM9_sha256':sha(arm),'EV2_sha256':sha(ev),
        'snapshot':str(SNAP),'snapshot_sha256':sha(raw),'source_trace_capture_report':str(CAP/'capture_report.json'),
        'current_registered_ROM_whole_file_exact_to_actual_snapshot_ROM':True,'original_category_context':[5,0],
        'all336_original_event_getters_and_completion_flags_source_bound':True,
        'all336_original_events':events,'original_completed_event_IDs':[n for n in range(336)if status[n]],
        'dependency_ready_uncompleted_events_not_full_eligibility':ready,
        'current_category5_full_native_predicate_cases':town_cases,'native_query_errors':errors,
        'full_predicate_acceptance_does_not_prove_original_outer_scheduler_or_actual_activation':True,
        'no_RAM_event_town_RNG_location_or_ROM_mutation':True,
        'source_inventory_inherited_from_original_complete336_source_walk':str(PRIOR),'prior_inventory_sha256':sha(PRIOR.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'completed':[n for n in range(336)if status[n]],'dependency_ready':len(ready),
        'current_town_full_predicate_cases':len(town_cases),'accepted':[r for r in town_cases if r['full_original_predicate_result']],
        'unmapped_query_errors':len(errors)},flush=True)

