"""Evidence for actual courier lifecycle, with observed defects kept unapproved."""

import struct
from pathlib import Path

from PIL import Image, ImageChops
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.item_diplomacy_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_letter_delivery_v791 import set_condition
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/letter_delivery_v791')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def load(folder):
    path=CAP/folder/'capture_report.json';rep=read(path)
    assert rep['frames']==20000 and rep['cold_boot'] and not rep['savestate_loaded'] and not rep['callback_errors']
    assert not rep['hardware_device_verification'] and not rep['goal_complete']
    assert sha(Path(rep['ROM']).read_bytes())==rep['ROM_sha256']
    donor=rep['battery_save_preloaded']
    assert donor['source']!=donor['destination'] and donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes())==donor['source_sha256']=='d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
    frames={r['frame']:r for r in rep['frames_captured']}
    for r in frames.values():assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']
    ram={}
    for r in rep['read_only_capture_RAM_snapshots']+rep['read_only_pause_RAM_snapshots']:
        raw=Path(r['path']).read_bytes()
        assert r['read_only_export'] and len(raw)==r['bytes']==0x400000 and sha(raw)==r['sha256']
        if r['frame'] in ram:assert raw==ram[r['frame']]
        ram[r['frame']]=raw
    arm=NdsImage.open(rep['ROM']).read_file('/__arm9__.bin')
    expected={3200:'Istanbul-letter-eligibility',8800:'controlled-letter-random-input',
        9200:'controlled-letter-random-input',10800:'controlled-letter-random-input',
        11200:'controlled-letter-random-input',12400:'two-registered-letter-deadlines',
        13600:'controlled-letter-random-input',14400:'controlled-letter-random-input',
        16800:'controlled-letter-random-input'}
    assert len(rep['synthetic_condition_fixtures'])==len(expected)
    for r in rep['synthetic_condition_fixtures']:
        _,proof=set_condition(arm,ram[r['frame']],{'mode':expected[r['frame']]})
        assert r=={**proof,'frame':r['frame']}
    adapter=rep['delivery_adapter']
    assert adapter['single_fixture_import_replacement'] and adapter['no_text_menu_daily_or_delivery_logic_replacement']
    for key,name in (('original_harness_sha256','headless_desmume_v193.py'),('adapter_sha256','run_letter_delivery_v791.py'),
                     ('fixture_sha256','native_letter_delivery_v791.py'),('qualification_fixture_sha256','native_letter_eligibility_v790.py')):
        assert adapter[key]==sha((Path('scripts')/name).read_bytes())
    journal=read(path.parent/'navigation_command_journal.json')
    assert all(r['validation_passed'] for r in journal['commands_received'])
    assert journal['commands_received'][-1]['command']=={'stop':True}
    return path,rep,arm,frames,ram


def observed(arm,raw):
    cpu=machine(arm);cpu.mem_write(0x02000000,raw)
    def get(fn,args=()):
        call(cpu,fn,args);return cpu.reg_read(UC_ARM_REG_R0)
    pool,clock,companies=get(0xCB130),get(0xCB1B4),get(0xCB160)
    return {'cash':state(arm,raw)['cash'],'tick':struct.unpack('<I',cpu.mem_read(clock+8,4))[0],
        'relation':get(0x3CB30,(companies+4,2)),'friendliness':get(0x3C7F8,(companies+4,2)),
        'letters':[bytes(cpu.mem_read(pool+4+i*16,16)).hex() for i in (4,5)]}


def main():
    old,new=[load(s) for s in ('letter_delivery_v791_baseline','letter_delivery_v791_recovered')]
    pa,ra,aa,fa,xa=old;pb,rb,ab,fb,xb=new
    assert ra['scripted_input_schedule']==rb['scripted_input_schedule'] and ra['core_options']==rb['core_options']
    assert set(fa)==set(fb)
    # Replay exports additional read-only startup RAM at its explicit PNG frames.
    assert {f for f in xa if f>=3200}=={f for f in xb if f>=3200}
    ja,jb=[read(p.parent/'navigation_command_journal.json') for p in (pa,pb)]
    assert ja['ROM_sha256']==ra['ROM_sha256'] and jb['ROM_sha256']==rb['ROM_sha256']
    assert {k:v for k,v in ja.items() if k!='ROM_sha256'}=={k:v for k,v in jb.items() if k!='ROM_sha256'}
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in ((0x91598,0x93BAC),(0xCB240,0xCB3C8)):
        assert aa[lo:hi]==ab[lo:hi]==clean[lo:hi]
    states=[];observations={}
    for f in sorted(xb):
        if f<3200:continue
        left,right=observed(aa,xa[f]),observed(ab,xb[f]);observations[f]=right
        assert state(aa,xa[f])==state(ab,xb[f]) and tasks(aa,xa[f])==tasks(ab,xb[f])
        states.append({'frame':f,'cash_and_courier_records_exact':True,
            'models_exact':models(aa,xa[f])==models(ab,xb[f]),
            'actors_towns_items_goods_exact':persistent_objects(aa,xa[f])==persistent_objects(ab,xb[f]),
            'baseline':left,'candidate':right})
    for f,row in observations.items():
        cash=8371-(1000 if f>=9600 else 0)-(1000 if f>=11600 else 0)-(1 if f>=14800 else 0)-(1 if f>=17200 else 0)
        assert row['cash']==cash
        kinds=[bytes.fromhex(s)[4] for s in row['letters']]
        assert kinds==([11,11] if f<9200 or f>=19600 else [2,11] if f<11200 else [2,0] if f<18000 else [11,0])
        assert row['relation']==(1 if 3600<=f<18000 else 0),(f,row['relation'])
    assert observations[12400]['tick']==26877+96
    assert observations[20000]['tick']==26877+192
    assert observations[12400]['friendliness']==50 and observations[18000]['friendliness']==52
    assert observations[20000]['friendliness']==57
    for f in (12800,14800):
        assert all(int.from_bytes(bytes.fromhex(s)[12:16],'little')==26973+48 for s in observations[f]['letters'])
    rom=NdsImage.open(rb['ROM']);entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),ab)
    owner=struct.unpack_from('<I',ab,0x552A0)[0];wrapped=struct.unpack_from('<I',ab,0x54450)[0]
    defects=[]
    for f,n,expected in ((17200,347,b'Castor Co. got a letter.\n  R'),(18000,347,b'Castor Co. got a letter.\n  R'),
                         (19200,348,'elations rose ５.      '.encode('cp932'))):
        assert cstring(xb[f],owner+0x2030)==entries[n].text and cstring(xb[f],wrapped)==expected
        defects.append({'frame':f,'id':n,'capture':fb[f],'template_hex':entries[n].text.hex(),
            'formatted_hex':expected.hex(),'formatting_approved':False})
    equal=[];differences=[]
    for f in sorted(fb):
        diff=ImageChops.difference(Image.open(fa[f]['path']).convert('RGB'),Image.open(fb[f]['path']).convert('RGB'))
        if diff.getbbox() is None:equal.append(f)
        else:differences.append({'frame':f,'bounds':diff.getbbox(),'approved_as_pixel_control':False})
    assert set(r['frame'] for r in differences)=={6000,6400,8000,8800,9200,9600,10000,10400,10800,11200,14800,15200,16000,19200,20000}
    assert all(f in equal for f in (17200,17600,18000,18400,18800,19600))
    save(ROOT/'delivery_verification.json',{'candidate_sha256':rb['ROM_sha256'],
        'source_reports':[str(pa),str(pb)],'report_sha256':[sha(p.read_bytes()) for p in (pa,pb)],
        'registered_two_letters_original_fees_and_day_progression':True,'deadlines_only_accelerated_after_registration':True,
        'both_couriers_completed_and_original_town_return':20000,'two1000_fees_two1_coin_stays':True,
        'pact_terminated_before_goodwill_increase':True,'candidate_goodwill_increase':5,
        'candidate_termination_relation_increase':2,'native_state_comparison':states,
        'strict_whole_screen_controls':equal,'unapproved_pixel_differences':differences,'actual_formatting_defects':defects,
        'random_stream_and_all_daily_objects_not_claimed_identical':True,
        'all_broader_gameplay_or_formatting_approval':False,'CScheme_virtual_name_menu_not_observed':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print(f'Two original couriers complete;{len(states)} exact cash/task pairs;{len(equal)} exact full screens.347/348 formatting defects remain open.',flush=True)


if __name__=='__main__':main()
