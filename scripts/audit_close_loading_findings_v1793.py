"""Preserve the negative pilot and prove the original wider-band admission rule."""
import json
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_close_follow_v1781 import INITIAL,apply_fixture,position
from scripts.native_call_abi_v764 import call
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/close_loading_findings_v1793')
RUN=Path('work/analysis/close_follow_v1782_openWaterReady8')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/close_follow_v1782_1775_openWaterReady8')
BASE=0x02000000

if __name__=='__main__':
    assert not ROOT.exists()
    report,plan,journal=map(read,(CAP/'capture_report.json',RUN/'run_plan.json',CAP/'navigation_command_journal.json'))
    assert report['frames']==5250 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    rom=Path(plan['candidate']);arm=NdsImage.open(rom).read_file('/__arm9__.bin')
    assert sha(rom.read_bytes())==plan['candidate_sha256']==report['ROM_sha256']
    assert read(RUN/'terminal_preservation.json')['source_and_disposable_donors_unchanged']
    for key in ('source_donor','disposable_donor'):assert sha(Path(plan[key]).read_bytes())==plan['source_donor_sha256']
    commands=[json.loads(s)for s in (RUN/'navigation.jsonl').read_text(encoding='utf-8').splitlines()if s.strip()]
    assert commands==[r['command']for r in journal['commands_received']] and commands[-1]=={'stop':True}
    rejected=[r for r in journal['commands_received']if not r['validation_passed']]
    assert len(rejected)==1 and rejected[0]['frame']==5100 and rejected[0]['rejected_before_any_input_or_fixture']=='Invalid duration'
    schedule=list(read(plan['inputs']))
    for row in journal['commands_received']:
        c=row['command']
        if row['validation_passed']and(c.get('buttons')or c.get('touch')):
            e={'start':row['frame']+1,'duration':c['duration'],'buttons':c.get('buttons',[])}
            if c.get('touch'):e['touch']=c['touch']
            schedule.append(e)
    assert schedule==report['scripted_input_schedule']
    snapshots={}
    for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']+[report['read_only_RAM_snapshot']]:
        data=Path(row['path']).read_bytes();assert len(data)==row['bytes']==0x400000 and sha(data)==row['sha256']
        snapshots[row.get('frame',5250)]=row
    fixtures=report['synthetic_battle_recovery_proximity_fixtures'];assert len(fixtures)==150
    assert [r['frame']for r in fixtures]==list(range(5100,5250))
    checks=[]
    for r in fixtures:
        raw=Path(snapshots[r['frame']]['path']).read_bytes();cpu,get=get_machine(arm,raw);fleets=get(0xCB1A8)
        own,enemy=fleets+4+132,fleets+4+8*132;mobile=get(0x36C70,own+12);target,_=position(cpu,enemy)
        fields={own+0x34:struct.pack('<2i',*target),mobile+16:struct.pack('<2i',*[v*128 for v in target])}
        if r['frame']==5100:
            _,first=apply_fixture(arm,raw,INITIAL);assert r=={**first,'frame':5100}
            fields.update({int(k):bytes.fromhex(v)for k,v in first['declared_fields'].items()if int(k)not in fields})
        assert fields=={int(k):bytes.fromhex(v)for k,v in r['declared_fields'].items()}
        rebuilt=bytearray(raw)
        for at,value in fields.items():rebuilt[at-BASE:at-BASE+len(value)]=value
        assert sha(raw)==r['before_RAM_sha256'] and sha(bytes(rebuilt))==r['after_RAM_sha256']
        owned={at+i for at,value in fields.items()for i in range(len(value))}
        assert sorted(owned)==r['owned_bytes'] and len(owned)==(17 if r['frame']==5100 else 16)
        assert not cpu.mem_read(enemy+0x50,1)[0]&4 and 8 not in bytes(cpu.mem_read(fleets+0x2080,16))[::4]
        assert get(0x78C60,1)==115
        checks.append({'frame':r['frame'],'source_position_owned_fields_and_entire4MiB_reconstruction_exact':True,
            'enemy_unseen_and_not_loaded':True,'actual_native_known_town_scan':115})
    final=Path(snapshots[5250]['path']).read_bytes();cpu,get=get_machine(arm,final);fleets=get(0xCB1A8)
    assert not cpu.mem_read(fleets+4+8*132+0x50,1)[0]&4 and 8 not in bytes(cpu.mem_read(fleets+0x2080,16))[::4]
    raw=Path(snapshots[5100]['path']).read_bytes();close,_=apply_fixture(arm,raw,INITIAL)
    cpu,get=get_machine(arm,close);fleets=get(0xCB1A8);own,enemy=fleets+4+132,fleets+4+8*132;mobile=get(0x36C70,own+12)
    target,_=position(cpu,enemy);admissions=[]
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in ((0x77EDC,0x77FF8),(0x513D0,0x5146C),(0x7BF80,0x7BFA0),(0x7C184,0x7C1A0)):
        assert arm[lo:hi]==clean[lo:hi]
    assert struct.unpack_from('<I',arm,0x7BF8C)[0]==0xE3A08000
    assert struct.unpack_from('<I',arm,0x7C190)[0]==0xE1A01008
    for dx in (0,3,159,160,200,319,320):
        state=bytearray(close);point=[target[0]+dx,target[1]]
        struct.pack_into('<2i',state,own-BASE+0x34,*point);struct.pack_into('<2i',state,mobile-BASE+16,*[v*128 for v in point]);state=bytes(state)
        for mode in (0,1):
            u,g=get_machine(arm,state);requests=[]
            def bridge(machine,pc,size,data):
                requests.append([machine.reg_read(reg)for reg in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3)])
                machine.reg_write(UC_ARM_REG_R0,1);machine.reg_write(UC_ARM_REG_PC,machine.reg_read(UC_ARM_REG_LR))
            hook=u.hook_add(UC_HOOK_CODE,bridge,begin=0x0202CE90,end=0x0202CE90)
            try:call(u,0x77EDC,(0,mode),instruction_limit=1000000)
            finally:u.hook_del(hook)
            assert bytes(u.mem_read(BASE,0x400000))==state
            selected=8 in [r[1]for r in requests]
            assert selected==((160<=dx<320)if mode==0 else dx<160)
            admissions.append({'relative_x':dx,'original_loading_mode':mode,'original_admission_requests':requests,
                'fleet8_requested':selected,'all4MiB_exact_with_only_admission_effect_bridged':True})
    ROOT.mkdir(parents=True)
    save(ROOT/'negative_pilot_and_original_admission_rule.json',{'candidate':str(rom),'candidate_sha256':report['ROM_sha256'],
        'terminal_frame':5250,'all150_source_location_footprints_and_entire4MiB_reconstructions':checks,
        'source_and_disposable_saves_input_schedules_and_RAM_hashes_exact':True,
        'one_invalid_duration_rejected_before_any_fixture_or_input_same_emulator_continued':rejected[0],
        'original14_loading_predicate_cases':admissions,
        'source_normal_update_sets_R8_zero_and_passes_it_to_loading_at0207C194':True,
        'finding':'The normal mode0 loader admits the wider160..319 distance band. Direct close placement ofan unloaded fleet bypasses that admission;initial mode1 covers the inner band. Load normally atmedium range before close approach.',
        'source_admission_requests_only_bridged_not_an_offline_loading_or_gameplay_claim':True,
        'negative_pilot_no_sighting_UI_or_editorial_completion_credit':True,
        'proofs':{str(p):sha(p.read_bytes())for p in [CAP/'capture_report.json',CAP/'navigation_command_journal.json',RUN/'terminal_preservation.json']},
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Negative5250 audited:150 exact location footprints and14 original loading cases. Source mode0 wider-band admission explains missed close spawn;no target credit.',flush=True)
