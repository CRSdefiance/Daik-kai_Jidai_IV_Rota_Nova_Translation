"""Original destination eligibility on copied RAM;classify one RNG-consuming query."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_destination_contexts_v1847')
INV=Path('work/analysis/lil_after_Amsterdam_inventory_v1846/all336_states_and_original_town_eligibility.json')
BASE=0x02000000;SCRATCH=0x02640000

if __name__=='__main__':
    assert not ROOT.exists()
    inv=read(INV);image=NdsImage.open(inv['candidate']);arm=image.read_file('/__arm9__.bin')
    raw=Path(inv['snapshot']).read_bytes();assert sha(raw)==inv['snapshot_sha256']
    ev=image.read_file('/data/EV2.DK4');assert ev==NdsImage.open('work/clean.nds').read_file('/data/EV2.DK4')
    owner=BASE+raw.find(ev[:96])-0x34;cases=[]
    for event,town,category,subtype,expected in [(26,0,5,None,1),(27,7,5,None,1),(28,13,5,None,0),(29,13,5,None,0),(128,5,7,3,0)]:
        cpu,get=get_machine(arm,raw);fleet=get(0xCB1A8)+4+2*132
        obj=get(0xCB178)+4+town*108;vt=struct.unpack('<I',cpu.mem_read(obj,4))[0]
        function=struct.unpack('<I',cpu.mem_read(vt+8,4))[0];pointer=get(function-BASE,obj)
        name=bytes(cpu.mem_read(pointer,80)).split(b'\0')[0].decode('cp932')
        assert get(0xB5600,obj)==town
        cpu.mem_write(fleet+0x3C,bytes([town]));cpu.mem_write(owner+0x2454,struct.pack('<2I',category,town))
        if subtype is not None:cpu.mem_write(owner+0x245C,struct.pack('<I',subtype))
        get(0xCC9A8,SCRATCH+0x80,get(0xCB1B4));before=bytes(cpu.mem_read(BASE,0x400000))
        result=get(0x220D8,owner,inv['all336_original_events'][event]['actual_native_event_pointer'],SCRATCH+0x80,0)
        assert result==expected and bytes(cpu.mem_read(BASE,0x400000))==before
        changes=[{'address':BASE+i,'before':a,'after':b}for i,(a,b)in enumerate(zip(raw,before,strict=True))if a!=b]
        allowed={fleet+0x3C,*range(owner+0x2454,owner+0x245C)}
        if subtype is not None:allowed.update(range(owner+0x245C,owner+0x2460))
        assert all(r['address']in allowed for r in changes)
        cases.append({'event_ID':event,'SC2_block':inv['all336_original_events'][event].get('SC2_action_block'),
            'original_category':category,'offline_town':town,'native_town_name':name,'offline_subtype':subtype,
            'full_original_predicate_result':result,'predicate_all4MiB_unchanged':True,'offline_input_changes':changes,
            'no_live_arrival_or_story_activation_claim':True})
    # Full original event80 predicate consumes a native random draw. Diagnose only
    # within a fresh disposable Unicorn copy;never reseed or advance the live game.
    cpu,get=get_machine(arm,raw);get(0xCC9A8,SCRATCH+0x80,get(0xCB1B4));before=bytes(cpu.mem_read(BASE,0x400000));writes=[]
    def write(c,access,address,size,value,user):
        if BASE<=address<BASE+0x400000:writes.append({'PC':c.reg_read(UC_ARM_REG_PC),'address':address,'bytes':size,'value':value})
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    result=get(0x220D8,owner,inv['all336_original_events'][80]['actual_native_event_pointer'],SCRATCH+0x80,0)
    after=bytes(cpu.mem_read(BASE,0x400000));assert result==0
    assert len(writes)==1 and writes[0]['PC']==BASE+0xD984C and writes[0]['address']==0x02168EB8
    seed_before=struct.unpack_from('<I',before,0x168EB8)[0];seed_after=struct.unpack_from('<I',after,0x168EB8)[0]
    multiplier,increment=struct.unpack_from('<2I',arm,0xD985C)
    assert seed_after==(seed_before*multiplier+increment)&0xFFFFFFFF
    changed=[BASE+i for i,(a,b)in enumerate(zip(before,after,strict=True))if a!=b]
    assert set(changed)<=set(range(0x02168EB8,0x02168EBC))
    assert arm[0xD9834:0xD9868]==NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')[0xD9834:0xD9868]
    ROOT.mkdir(parents=True)
    save(ROOT/'source_destinations_and_original_random_query_classification.json',{
        'candidate':inv['candidate'],'candidate_sha256':inv['candidate_sha256'],'snapshot':inv['snapshot'],
        'snapshot_sha256':inv['snapshot_sha256'],'original_source_destination_cases':cases,
        'London26_and_Stockholm27_predicates_accept_offline_destination_inputs':True,
        'Amsterdam_current67_category5_checks_no_accepted_new_scene':True,
        'event80_query_classification':{'original_predicate_result_in_exact_copy':result,'WRAM_writes':writes,
            'original_LCG_seed_before':seed_before,'original_LCG_seed_after':seed_after,
            'multiplier':multiplier,'increment':increment,'only_original_random_state_word_changed':True,
            'not_a_pure_query_or_general_eligibility_claim':True},
        'no_live_RNG_seed_message_event_town_actor_or_location_mutation':True,
        'B25_requires_original_event128_uncompleted_so_not_assumed_next_scene':True,
        'selected_next_review':'SC2 B27 Stockholm encounter;independent original event27/category5/town7. London B26 remains an unreviewed eligible source lead.',
        'actual_normal_docking_source_control_and_scene_returns_still_pending':True,
        'evidence':{str(INV):sha(INV.read_bytes())},'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'eligible_offline_destinations':['London B26','Stockholm B27'],'event80_original_RNG_draw_classified':True,
        'selected_next_source':'Stockholm B27','actual_activation_pending':True},flush=True)
