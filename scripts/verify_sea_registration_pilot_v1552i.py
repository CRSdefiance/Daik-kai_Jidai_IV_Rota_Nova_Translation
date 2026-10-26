"""Audit original registered creature pilot and record the unrelated old modal defect."""
import json,struct
from pathlib import Path
from dataclasses import asdict
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.declaration_responses_editorial import current_entries
from scripts.native_sea_registration_fixture_v1552g import apply_fixture
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROM = Path('out/all_routes_combined_v1542_candidate.nds')
def audit(run,cap,terminal_frame):
    report_path = cap/'capture_report.json'
    report,plan,terminal = [read(p) for p in [report_path,run/'run_plan.json',run/'terminal_preservation.json']]
    assert report['frames']==terminal_frame and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['hardware_device_verification'] and not report['goal_complete']
    digest = sha(ROM.read_bytes())
    assert report['ROM_sha256']==plan['candidate_sha256']==digest=='b8b256650bb426e99012be06fd060114da0fbf32f763b5c3434204dda8f50437'
    assert sha(Path(plan['source_donor']).read_bytes())==sha(Path(plan['disposable_donor']).read_bytes())==terminal['source_donor_sha256']
    assert terminal['source_and_disposable_donors_unchanged']
    assert sha((run/'navigation.jsonl').read_bytes())==terminal['navigation_sha256']
    assert sha(Path('scripts/headless_desmume_v193.py').read_bytes())==plan['harness_sha256']
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = [(0x2D1CC,0x2D268),(0x363E8,0x3648C),(0x557C8,0x55828),(0x56290,0x5636C),
        (0x56104,0x56224),(0x519D4,0x51A18),(0x348D4,0x34914),(0x36BE8,0x36C00)]
    assert all(arm[a:b]==clean[a:b] for a,b in spans)
    snapshots = {}
    for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        body = Path(row['path']).read_bytes()
        assert len(body)==row['bytes']==0x400000 and sha(body)==row['sha256']
        if row['frame'] in snapshots:
            assert snapshots[row['frame']]['sha256']==row['sha256']
        snapshots[row['frame']] = row
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
    raw = Path(snapshots[4800]['path']).read_bytes()
    after,fixture = apply_fixture(arm,raw,{'sea_inspection_context':'register_original_Monster_Fish'})
    assert report['synthetic_battle_recovery_proximity_fixtures']==[{**fixture,'frame':4800}]
    assert len(fixture['owned_bytes'])==46
    assert {0x02000000+i for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b}<=set(fixture['owned_bytes'])
    assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k!='synthetic_battle_recovery_proximity_fixtures')
    commands = [json.loads(line) for line in (run/'navigation.jsonl').read_text(encoding='utf-8').splitlines()]
    journal = read(cap/'navigation_command_journal.json')['commands_received']
    assert commands==[r['command'] for r in journal]
    assert journal[-1]['frame']==terminal_frame and journal[-1]['command']=={'stop':True}
    schedule = read(run/'original_departure_inputs.json')
    for item in journal:
        assert item['validation_passed']
        command = item['command']
        if command.get('stop'):
            continue
        assert set(command)<={'until','buttons','touch','duration','battle_fixture'}
        assert command['until'] in snapshots and command['until']>item['frame']
        if item['frame']>4800:
            assert 'battle_fixture' not in command
        if command.get('buttons') or command.get('touch') is not None:
            event = {'start':item['frame']+1,'duration':command.get('duration',12),'buttons':command.get('buttons',[])}
            if command.get('touch') is not None:
                event['touch'] = command['touch']
            schedule.append(event)
    assert schedule==report['scripted_input_schedule']
    receipt = {'candidate':str(ROM),'candidate_sha256':digest,'terminal_frame':terminal_frame,
        'terminal_report':str(report_path),'terminal_report_sha256':sha(report_path.read_bytes()),
        'run_plan':str(run/'run_plan.json'),'navigation_sha256':terminal['navigation_sha256'],
        'complete_primary_RAM_and_PNG_hash_audits':True,'snapshot_count':len(snapshots),'capture_count':len(report['frames_captured']),
        'entire4MiB_sole_prebattle46_owned_byte_fixture_and_all_input_schedule_audited':True,
        'sole_fixture':fixture,'source_and_disposable_donor_unchanged':True,
        'source_donor_sha256':terminal['source_donor_sha256'],'original_clean_code_spans':spans,
        'no_further_battle_or_duel_fixture_health_equipment_position_ability_actor_ID_RNG_or_result_edit':True,
        'artificial_registration_and_location_not_natural_spawn':True,
        'no_ROM_build_or_change':True,'targeted_headless_not_complete_route_or_hardware':True,
        'shared_auditor_sha256':sha(Path(__file__).read_bytes())}
    return receipt,snapshots,arm

if __name__=='__main__':
    root=Path('work/analysis/sea_registration_pilot_verified_v1552i');assert not root.exists()
    run=Path('work/analysis/sea_registration_live_v1552h')
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/sea_registration_live_v1552h_1542')
    proof,snapshots,arm=audit(run,cap,6850)
    rom=NdsImage.open(ROM);clean=NdsImage.open('work/clean.nds');original=clean.read_file('/__arm9__.bin')
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),original)
    en=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
    raw=Path(snapshots[6630]['path']).read_bytes();cpu,get=get_machine(arm,raw);duty=get(0xCB1A8)+0x2090
    assert get(0x8205C,duty,1)==3 and get(0x82BC4,duty,3)==208 and get(0x82BC4,duty,9)==18
    assert get(0x82478,duty,7)==18 and get(0x82B30,duty)==27
    owner=struct.unpack_from('<I',arm,0x552A0)[0]-0x2000000;wrapped=struct.unpack_from('<I',arm,0x54450)[0]-0x2000000
    assert raw[owner+0x2030:owner+0x2230].split(b'\0')[0]==en[307].text
    assert raw[wrapped:wrapped+512].split(b'\0')[0]==en[307].text
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    spans=[(0x705F8,0x706A4),(0x6F5D4,0x6F610),(0x8205C,0x820DC),(0x82B0C,0x82B38)]
    source=[{'span':[0x2000000+a,0x2000000+b],'sha256':sha(original[a:b]),'instructions':[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str} for i in md.disasm(original[a:b],0x2000000+a)]} for a,b in spans]
    records=[{'ID':n,'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),'current_English':en[n].text.decode('cp932'),'current_hex':en[n].text.hex(),'source_reference':{k:v for k,v in asdict(jp[n]).items() if k!='text'},'current_reference':{k:v for k,v in asdict(en[n]).items() if k!='text'}} for n in range(304,309)]
    proof.update(original_creature_registered_but_unidentified_target_selected_by_normal_touch=True,
        actual_no_lookout_modal_ID307=records[3],no_creature_response2209_2216_or_editorial_completion_credit=True,
        original_role7_actor18_is_fallback_and_does_not_prove_lookout_station_occupied=True,
        original_lookout_slot3_empty_and_current_Charles_slot9=True,
        normal_modal_A_dismissal_and_return_to_sea6850=True,full_goal_complete=False)
    root.mkdir(parents=True);save(root/'original_registration_and_no_lookout_verified.json',proof)
    packet=root/'source_unidentified_target_and_old_modal_defects.json'
    save(packet,{'candidate':str(ROM),'candidate_sha256':proof['candidate_sha256'],'actual_audit':str(root/'original_registration_and_no_lookout_verified.json'),
        'records':records,'clean_code':source,'actual_modal307_frame':6630,'source_faithful_meanings':{'306':'You cannot view that information!','307':'No one is assigned as lookout.'},
        'findings':'306/307 current text is an unrelated split trade-good-description draft;307 is actually displayed.308 also starts with an unrelated suffix and needs its separate fatigue consumer/context. No source/prose review or completion credit is added by this lead inventory.',
        'next_original_test':'Move existing Charles18 from slot9 to empty lookout3 with original82BB8;do not change actor objects,force target flags or inject a message.', 'full_goal_complete':False})
    ledger=read('translations/editorial_review_current_v1.json')
    ledger['newly_observed_sea_inspection_modal_defects']={'packet':str(packet),'packet_sha256':sha(packet.read_bytes()),'actual_ID':307,'other_leads':[306,308],'status':'source-context-lead;authoring-native-release-gameplay-pending','source_prose_reviews_added':0,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V1552i-original-registered-creature-and-no-lookout','proof':str(root/'original_registration_and_no_lookout_verified.json'),'source_prose_reviews_added':0,'completed_entries_added':0,'full_goal_complete':False})
    save('translations/editorial_review_current_v1.json',ledger)
    print('Terminal6850 original-registration pilot audited;actual307 wrong-text defect recorded;source confirms empty lookout3,not missing creature or failed renderer. No completion credit.')
