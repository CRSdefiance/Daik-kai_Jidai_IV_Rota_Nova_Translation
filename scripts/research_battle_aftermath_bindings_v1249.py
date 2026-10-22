"""Complete source speaker bindings for city defense and ship surrender.

These execute original post-eligibility prefixes only. No city attack, RNG
success, ship surrender or gameplay outcome is fabricated in an emulator.
"""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_PC,UC_ARM_REG_LR,UC_ARM_REG_SP
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine,rtti
from scripts.probe_button_prompt_native import STACK,STOP
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_aftermath_bindings_v1249')
BASE=0x02000000


def prefix(arm,raw,start,end,registers):
    cpu,get=get_machine(arm,raw);seen=[]
    def observe(u,pc,size,unused):
        if pc==end:u.emu_stop();return
        seen.append({'entry':pc,'original_return':u.reg_read(UC_ARM_REG_LR),
            'arguments':[u.reg_read(r) for r in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3)]})
        u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    for pc in (BASE+0x53F0C,end):cpu.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
    cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP)
    for reg,value in registers.items():cpu.reg_write(reg,value)
    cpu.emu_start(BASE+start,STOP,count=100000)
    assert cpu.reg_read(UC_ARM_REG_PC)==end and len(seen)==1
    return seen[0]


def main():
    assert not ROOT.exists()
    previous_path=Path('work/analysis/battle_aftermath_context_v1248d/source_context_and_consumer_frames.json')
    previous=read(previous_path);snapshot=Path(previous['snapshot']);raw=snapshot.read_bytes()
    assert sha(raw)==previous['snapshot_sha256']
    path=Path(previous['current_ROM']);rom=NdsImage.open(path);arm=rom.read_file('/__arm9__.bin')
    assert sha(arm)==previous['current_ARM9_sha256']
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in ((0x6ED34,0x6EE44),(0x72AC0,0x72B54),(0x3697C,0x369AC),
                  (0xAB158,0xAB170),(0xA4B70,0xA4BB4),(0x7B60,0x7B74),(0x82428,0x8251C)):
        assert arm[lo:hi]==clean[lo:hi]
    cpu,get=get_machine(arm,raw);fleets=get(0xCB1A8);actors=get(0xCB184)
    bindings=[]
    for index in (1,8):
        fleet=fleets+4+index*132;mobile=get(0x36C70,fleet+12)
        assert mobile
        vt=struct.unpack('<I',cpu.mem_read(fleet,4))[0]
        assert rtti(raw,vt)=='6CFleet'
        mv=struct.unpack('<I',cpu.mem_read(mobile,4))[0]
        assert rtti(raw,mv)=='11CMobileShip'
        captain=get(0x3697C,fleet)
        city=prefix(arm,raw,0x6EE20,BASE+0x6EE30,{UC_ARM_REG_R4:fleet})
        assert city['arguments'][:2]==[captain,0x021178C0] and city['original_return']==BASE+0x6EE30
        flagship=prefix(arm,raw,0x72B44,BASE+0x72B54,{UC_ARM_REG_R7:fleet})
        assert flagship['arguments'][:2]==[captain,0x02117840] and flagship['original_return']==BASE+0x72B54
        model=get(0xAB158,mobile);model_speaker=get(0xA4B70,model)
        assert BASE<=model_speaker<BASE+len(raw)
        nonflagship=prefix(arm,raw,0x72B00,BASE+0x72B14,{UC_ARM_REG_R6:mobile})
        assert nonflagship['arguments'][:2]==[model_speaker,0x02117840]
        bindings.append({'source_fleet_index':index,'source_fleet':fleet,'source_mobile_ship':mobile,
            'fleet_RTTI':'6CFleet','mobile_RTTI':'11CMobileShip',
            'original_fleet_captain_actor_ID':get(0x7EE08,captain),
            'original_ship_model_value':model,'original_model_speaker_actor_ID':get(0x7EE08,model_speaker),
            'city_defense_post_eligibility_prefix':city,
            'flagship_captain_surrender_prefix':flagship,
            'nonflagship_model_spokesperson_surrender_prefix':nonflagship,
            'no_actor_IDs_or_live_conditions_changed':True,
            'CPU_prefix_does_not_establish_actual_city_attack_or_ship_surrender':True})
    roster=fleets+0x2090;definitions=get(0x82E04,roster)
    source_type=get(0x7B60,1)
    assert source_type==6 and get(0x132C0,definitions,15)==source_type
    assert get(0x82428,roster,1)==0 and get(0x82478,roster,1)==18
    ROOT.mkdir(parents=True)
    out=ROOT/'source_context_complete.json'
    save(out,{'source_context':str(previous_path),'source_context_sha256':sha(previous_path.read_bytes()),
        'current_ROM':str(path),'current_ROM_sha256':sha(path.read_bytes()),'current_ARM9_sha256':sha(arm),
        'snapshot':str(snapshot),'snapshot_sha256':sha(raw),
        'native_message_IDs':previous['native_message_IDs'],'source_records':75,
        'city_and_ship_original_bindings':bindings,
        'original_selector1_type6_and_fallback':{'selector_parameter':1,'original_7B60_type':source_type,
            'matching_duty_slot':15,'available_query_82428':0,'fallback_query_82478':18,
            'baseline_fallback_and_CPU_assigned_branch_both_proven':True},
        'original_town_name_argument_and_numeric2192_reply_proven':True,
        'all75_source_consumers_speakers_substitutions_and_linked_contexts_mapped':True,
        'source_prefixes_have_explicit_audio_UI_and_post_eligibility_boundaries':True,
        'no_prose_or_formatting_approval_ROM_or_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==1260 and ledger['records_with_source_and_prose_pass']==1298
    ledger['next_battle_aftermath_context_v1248'].update(complete_source_binding=str(out),
        complete_source_binding_sha256=sha(out.read_bytes()),prose_and_formatting_pending=True)
    save('translations/editorial_review_current_v1.json',ledger)
    print('All75 source contexts mapped,including town-name2192 exchange,city defender and both ship-surrender speakers;prose review next.',flush=True)


if __name__=='__main__':main()
