"""Extend the exact transaction verifier to the declared role and letter run."""

import inspect
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import verify_item_transactions_v789 as original
from scripts.native_call_abi_v764 import call
from scripts.native_item_roles_v789 import set_condition
from scripts.native_item_rng_v789 import set_condition as synchronized_input
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = original.ROOT
SELECTED = {6000:1071,6800:1073,7200:1079,7600:1083,8000:1071,9600:1085,
    10400:1086,10800:1091,11200:1095,12800:1071,14800:1097,15200:1120,16000:1100,
    16800:1115,17600:1100,18400:1115,18800:1123}
PHASES=[]


def screen_control(frame,diff,image):
    if diff.getbbox() is None: return
    assert frame in (8800,13600,19600),(frame,'unexpected unselected frame',diff.getbbox())
    folder='item_roles_v789_phase_control' if frame==8800 else f'item_roles_v789_phase_control_{frame}'
    path=original.CAP/folder/'capture_report.json'
    report=read(path)
    old=read(original.CAP/'item_roles_v789_baseline/capture_report.json')
    assert report['ROM_sha256']==old['ROM_sha256'] and report['scripted_input_schedule']==old['scripted_input_schedule']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    frames={r['frame']:r for r in report['frames_captured']}
    old_frames={r['frame']:r for r in old['frames_captured']}
    for f in (3200,4800,6000,6800,7200,10400,14800,16800,20000):
        assert Image.open(frames[f]['path']).convert('RGB').tobytes()==Image.open(old_frames[f]['path']).convert('RGB').tobytes()
    matches=[]
    for f,row in frames.items():
        if not frame-100<=f<=frame: continue
        assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
        if Image.open(row['path']).convert('RGB').tobytes()==image.tobytes(): matches.append(f)
    assert matches,(frame,'no complete original highlight phase matches')
    PHASES.append({'frame':frame,'complete_original_whole_frame_matches':matches,
        'control_report':str(path),'control_report_sha256':sha(path.read_bytes()),'no_rectangular_pixel_exclusion':True})


def fixture_receipt(report, raw, arm):
    fixtures = report['synthetic_condition_fixtures']
    assert len(fixtures) == 1 and fixtures[0]['frame'] == 3200
    _, proof = set_condition(arm, raw, {'mode':'item-and-letter-roles'})
    assert fixtures[0] == {**proof,'frame':3200}
    assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k != 'synthetic_condition_fixtures')
    adapter = report['item_role_adapter']
    assert adapter['single_import_replacement'] and adapter['no_dialogue_or_menu_logic_replacement']
    assert adapter['original_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
    assert adapter['fixture_producer_sha256'] == sha(Path('scripts/native_item_roles_v789.py').read_bytes())
    assert adapter['adapter_sha256'] == sha(Path('scripts/run_item_roles_v789.py').read_bytes())


def nominal(arm):
    cpu=machine(arm)
    call(cpu,0x93D5C,(0,))
    return bytes(cpu.mem_read(cpu.reg_read(UC_ARM_REG_R0),128)).split(b'\0')[0]


def arguments(n,old,new,oa,arm):
    if n in (1100,1115):
        assert old[-1] == nominal(oa) == '親善'.encode('cp932')
        assert new[-1] == nominal(arm) == b'goodwill letter'
        assert old[:-1] == new[:-1]
        if n == 1115: assert new == (b'Kurushima',b'goodwill letter')
    else: assert old == new


def outcomes(arm,ram,states):
    cash={r['frame']:r['cash'] for r in states}
    assert all(cash[f] == 38816 for f in (3200,6800,7200,7600))
    assert all(cash[f] == 38816-7546 for f in (8000,10400,10800,11200))
    assert all(cash[f] == 38816-7546+6314 for f in (11600,14800,15200,16800,17200,18400,18800))
    assert all(cash[f] == 38816-7546+6314-1000 for f in (19200,19600,20000))
    source = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in ((0x91480,0x914D8),(0x93BAC,0x93C04),(0x5BAB4,0x5BB30)):
        assert arm[lo:hi] == source[lo:hi]
    rows=[]
    for f in (3200,17200,18400,18800,19200,20000):
        cpu=machine(arm);cpu.mem_write(0x02000000,ram[f])
        def get(fn,args=()):
            call(cpu,fn,args);return cpu.reg_read(UC_ARM_REG_R0)
        pool,calendar=get(0xCB130),get(0xCB1B4)
        docs=[bytes(cpu.mem_read(pool+4+i*16,16)) for i in range(4,14)]
        active=[i+4 for i,d in enumerate(docs) if d[4]<10]
        expected=[] if f<18800 else [4]
        assert active == expected
        ticks=struct.unpack('<I',cpu.mem_read(calendar+8,4))[0]
        assert ticks == (2611 if f<19200 else 2659)
        if active:
            doc=docs[0]
            assert struct.unpack_from('<I',doc)[0] == 0x0214C618
            assert list(doc[4:10]) == [0,3,10,17,115,21]
            assert struct.unpack_from('<I',doc,12)[0] == 3187
            company=get(0xCB160)+4+17*76
            vt=struct.unpack('<I',cpu.mem_read(company,4))[0]
            p=get(struct.unpack('<I',cpu.mem_read(vt+8,4))[0]-0x02000000,(company,))
            assert bytes(cpu.mem_read(p,64)).split(b'\0')[0] == b'Kurushima'
        rows.append({'frame':f,'cash':cash[f],'native_calendar_ticks':ticks,'active_courier_indices':active,
            'all_ten_courier_records_hex':[d.hex() for d in docs]})
    assert rows[0]['all_ten_courier_records_hex'] == rows[1]['all_ten_courier_records_hex'] == rows[2]['all_ten_courier_records_hex']
    assert all(r['all_ten_courier_records_hex'][1:] == rows[0]['all_ten_courier_records_hex'][1:] for r in rows)
    save(ROOT/'qualified_outcomes.json',{'native_frames':rows,'purchase_after_Purser':7546,'sale_after_Purser':6314,
        'cancelled_confirmation_no_fee_or_document':True,'accepted_confirmation_one1000_coin_fee_and_one_document':True,
        'original_registration_advances_calendar48_ticks':True,'goodwill_target_company17_Kurushima':True,
        'original_courier_scan_is_start4_end14_exclusive_ten_slots_not14_slots':True,
        'document_due_at3187_still_pending_at_town_return2659':True,'actual_delivery_not_claimed':True})


def verify_states(oa,arm,old_ram,new_ram):
    states=[];ordinary_differences=[]
    for f in sorted(new_ram):
        if f<3200: continue
        a,b=original.state(oa,old_ram[f]),original.state(arm,new_ram[f])
        assert a==b and original.models(oa,old_ram[f])==original.models(arm,new_ram[f])
        old_objects,new_objects=original.persistent_objects(oa,old_ram[f]),original.persistent_objects(arm,new_ram[f])
        assert original.tasks(oa,old_ram[f])==original.tasks(arm,new_ram[f])
        if f<=18800:
            assert old_objects==new_objects
        else:
            ordinary_differences.append({'frame':f,'old_objects':old_objects,'new_objects':new_objects,
                'economic_models_and_document_records_match':True,
                'uncontrolled_daily_persistent_objects_identical':old_objects==new_objects})
        states.append({'frame':f,'cash':b['cash'],
            'full_native_models_objects_and_tasks_exact':old_objects==new_objects})
    controlled=[]
    for version,base_ram in ((783,old_ram),(788,new_ram)):
        path=original.CAP/f'item_roles_v789_seeded_{version}/capture_report.json'
        report=read(path)
        assert report['frames']==20000 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        raw={}
        for row in report.get('read_only_capture_RAM_snapshots',[])+report.get('read_only_pause_RAM_snapshots',[]):
            data=Path(row['path']).read_bytes();assert sha(data)==row['sha256'] and len(data)==0x400000
            raw[row['frame']]=data
        this_arm=oa if version==783 else arm
        fixtures=report['synthetic_condition_fixtures']
        assert len(fixtures)==2
        for f,mode in ((3200,'item-and-letter-roles'),(18800,'synchronize-post-acknowledgment-RNG')):
            proof=synchronized_input(this_arm,raw[f],{'mode':mode})[1]
            assert next(r for r in fixtures if r['frame']==f)=={**proof,'frame':f}
        for f in raw:
            if 3200<=f<=18800: assert raw[f]==base_ram[f],(version,f,'pre-seed RAM changed')
        adapter=report['item_rng_adapter']
        assert adapter['single_import_replacement'] and adapter['no_dialogue_menu_or_daily_logic_replacement']
        for field,name in (('adapter_sha256','scripts/run_item_rng_v789.py'),
                           ('fixture_producer_sha256','scripts/native_item_rng_v789.py'),
                           ('role_fixture_sha256','scripts/native_item_roles_v789.py')):
            assert adapter[field]==sha(Path(name).read_bytes())
        controlled.append((raw,path))
    late=[]
    for f in (19200,19600,20000):
        a,b=controlled[0][0][f],controlled[1][0][f]
        assert original.state(oa,a)==original.state(arm,b)
        assert original.models(oa,a)==original.models(arm,b)
        assert original.persistent_objects(oa,a)==original.persistent_objects(arm,b)
        assert original.tasks(oa,a)==original.tasks(arm,b)
        late.append({'frame':f,'all_native_economics_models_persistent_objects_and_tasks_exact':True})
    save(ROOT/'daily_update_control.json',{'ordinary_postday_comparisons':ordinary_differences,
        'ordinary_random_stream_parity_not_claimed':True,'same_PRNG_input_controlled_frames':late,
        'all_preseed4MiB_RAM_exact_to_corresponding_uncontrolled_run':True,
        'controlled_capture_reports':[str(p) for r,p in controlled],
        'controlled_reports_sha256':[sha(p.read_bytes()) for r,p in controlled],
        'production_ROM_and_daily_logic_unchanged':True,
        'source_of_conversation_random_call_count_difference_not_yet_mapped':True,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    return states


def main():
    load=inspect.getsource(original.load)
    replacements={"report['frames'] == 15600":"report['frames'] == 20000",
        "    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))\n":"",
        "    return path, report, rom, frames, ram":"    fixture_receipt(report,ram[3200],rom.read_file('/__arm9__.bin'))\n    return path, report, rom, frames, ram"}
    for before,after in replacements.items():
        assert load.count(before) == 1,before
        load=load.replace(before,after)
    body=inspect.getsource(original.main)
    a=body.index("    cash = {r['frame']:r['cash'] for r in states}")
    b=body.index("    save(ROOT/'ordinary_transactions_gameplay.json'",a)
    body=body[:a]+'    outcomes(arm,new_ram,states)\n'+body[b:]
    a=body.index('    for f in sorted(new_ram):')
    b=body.index('    outcomes(arm,new_ram,states)',a)
    body=body[:a]+'    states=verify_states(oa,arm,old_ram,new_ram)\n'+body[b:]
    replacements={
        "'item_transactions_v789_baseline'":"'item_roles_v789_baseline'",
        "'item_transactions_v789_live'":"'item_roles_v789_live'",
        "assert old_match and old_match.groups() == args":"assert old_match\n        arguments(n,old_match.groups(),args,oa,arm)",
        "assert diff.getbbox() is None, (f, 'unselected full screen', diff.getbbox())":"screen_control(f,diff,b)",
        "ROOT/'ordinary_transactions_gameplay.json'":"ROOT/'qualified_transactions_gameplay.json'",
        "'purchase_7700_sale_6160_original_outcomes_preserved':True,'both_declines_preserve_cash':True,":"'purchase7546_sale6314_and_one1000_coin_fee_original_outcomes_preserved':True,",
        "'fleet_ships_and_persistent_objects_return_to_original_state':True,":"'one_registered_goodwill_document_pending_delivery':True,",
        "'company_cash_change_is_expected_transaction_result_not_a_preservation_failure':True,":"'qualified_outcomes':str(ROOT/'qualified_outcomes.json'),",
        "'normal_town_return_frame':15600,'no_fixtures_or_savestates':True,":"'normal_town_return_frame':20000,'three_declared_role_bytes_only_no_savestates':True,",
        '7700 purchase,6160 sale,both declines and town return pass.':'7546 purchase,6314 sale,goodwill cancellation/registration and town return pass.'}
    for before,after in replacements.items():
        assert body.count(before) == 1,before
        body=body.replace(before,after)
    env={**original.__dict__,'SELECTED':SELECTED,'fixture_receipt':fixture_receipt,'arguments':arguments,
        'outcomes':outcomes,'screen_control':screen_control,'verify_states':verify_states,'__file__':str(Path(__file__).resolve())}
    program=load+'\n\n'+body
    path=ROOT/'effective_qualified_gameplay_verifier.py'
    path.write_text(program,encoding='utf-8')
    exec(compile(program,str(path),'exec'),env)
    env['main']()
    result=read(ROOT/'qualified_transactions_gameplay.json')
    result.update({'effective_program_sha256':sha(program.encode()),
        'frozen_base_verifier_sha256':sha(Path(original.__file__).read_bytes()),
        'nominal_argument_translation_source_bound_to_real_getters':True,
        'still_pending':['other diplomatic type eligibility','actual shared CScheme SDK/GPU list and all names','delivery lifecycle']})
    result['original_whole_screen_highlight_phase_controls']=PHASES
    result['strict_whole_screen_controls']=[f for f in result['strict_whole_screen_controls'] if f not in {r['frame'] for r in PHASES}]
    result['ordinary_exact_native_state_model_object_task_frames']=[r['frame'] for r in result['paired_native_state_model_object_task_frames'] if r['full_native_models_objects_and_tasks_exact']]
    result['daily_world_update_requires_declared_identical_PRNG_input_control']=str(ROOT/'daily_update_control.json')
    save(ROOT/'qualified_transactions_gameplay.json',result)


if __name__ == '__main__': main()
