"""Audit original Hamburg79/Speyer51, native choices and exact access footprints."""
import json
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_lil_speyer_access_v1923 import apply_fixture,REQUEST
from scripts.native_lil_Amsterdam_location_v1833c import REQUEST as AMSTERDAM
from scripts.native_lil_Bruges_location_v1754 import REQUEST as BRUGES
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/lil_Speyer_original_audit_v1935')
RUN = Path('work/analysis/lil_Speyer_access_run_v1924')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_Speyer_access_run_v1924_RESEARCH_ONLY')
TOWN = Path('work/analysis/lil_Hamburg_arrival_navigation_v1933/closed_original_scene_context.json')
SPEYER = Path('work/analysis/lil_Speyer_original_navigation_v1934/closed_original_scene_context.json')
BASE = 0x02000000

if __name__ == '__main__':
    assert not ROOT.exists()
    plan,terminal,report,trace,journal,town,speyer = map(read,(RUN/'run_plan.json',RUN/'terminal.json',
        CAP/'capture_report.json',CAP/'observer/commands.json',CAP/'navigation_command_journal.json',TOWN,SPEYER))
    rom = Path(plan['research_ROM'])
    digest = sha(rom.read_bytes())
    image = NdsImage.open(rom)
    arm = image.read_file('/__arm9__.bin')
    assert digest==plan['research_ROM_sha256']==report['ROM_sha256']==town['candidate_sha256']==speyer['candidate_sha256']
    assert terminal['terminal'] and terminal['frame']==report['frames']==93780
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and 'battery_save_preloaded'not in report
    assert trace['all_host_slots_restored_and_core_file_exact'] and not trace['errors'] and not trace['mismatches']
    assert all(r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']for r in trace['rows'])
    commands = [json.loads(s)for s in (RUN/'navigation.jsonl').read_text().splitlines()if s.strip()]
    assert commands == [r['command']for r in journal['commands_received']]
    assert commands[-1]=={'stop':True} and journal['last_command_frame']==93780
    schedule = list(read(plan['inputs']))
    assert sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
    for item in journal['commands_received']:
        assert item['validation_passed']
        command = item['command']
        if command.get('buttons')or command.get('touch'):
            event = dict(start=item['frame']+1,duration=command['duration'],buttons=command.get('buttons',[]))
            if command.get('touch'):event['touch']=command['touch']
            schedule.append(event)
    assert schedule==report['scripted_input_schedule']
    photos = {r['frame']:r for r in report['frames_captured']}
    for row in photos.values():assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
    snapshots = {}
    for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']+[report['read_only_RAM_snapshot']]:
        raw = Path(row['path']).read_bytes()
        assert len(raw)==row['bytes']==0x400000 and sha(raw)==row['sha256'] and row['read_only_export']
        if 'frame'in row:snapshots[row['frame']]=row
    synthetic = {k:v for k,v in report.items()if k.startswith('synthetic_')and v}
    assert set(synthetic)=={'synthetic_battle_recovery_proximity_fixtures'}
    fixtures = synthetic['synthetic_battle_recovery_proximity_fixtures']
    assert len(fixtures)==3
    replays = []
    for item,frame,request,count in zip(fixtures,(30290,42580,48810),(BRUGES,AMSTERDAM,REQUEST),(16,16,20),strict=True):
        assert item['frame']==frame and len(item['owned_bytes'])==count
        raw = Path(snapshots[frame]['path']).read_bytes()
        after,proof = apply_fixture(arm,raw,request)
        assert {k:v for k,v in item.items()if k!='frame'}==json.loads(json.dumps(proof))
        assert sha(raw)==item['before_RAM_sha256'] and sha(after)==item['after_RAM_sha256']
        replays.append(dict(frame=frame,owned_bytes=count,before_RAM_sha256=sha(raw),after_RAM_sha256=sha(after),
            all_other4MiB_exact=True,synthetic_funds=60000 if count==20 else None))
    all_blocks = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    scene_results = []
    for number,nav,source_path,expected_count in ((74,town,Path('work/analysis/lil_Hamburg_arrival_navigation_v1933/full_source_context_uncredited.json'),79),
        (128,speyer,Path('work/analysis/lil_Speyer_original_navigation_v1934/full_source_context_uncredited.json'),51)):
        packet = read(source_path)
        by_offset = {r['offset']:r for r in packet['all_current_native_commands']}
        records = {r['id']:r for r in packet['records']}
        rows = [r for r in trace['rows']if r['source'].get('route')==2 and r['source'].get('block')==number]
        assert len(rows)%2==0
        pairs = []
        previous = 0
        for index,(before,after)in enumerate(zip(rows[::2],rows[1::2],strict=True)):
            src = before['source']
            spec = by_offset[src['instruction_offset']]
            assert before['kind']=='before_command' and after['kind']=='after_command' and src==after['source']
            assert trace['rows'][after['entry_row']]==before and src['first_word']==spec['word']
            assert src['whole_resident_payload_exact_ROM'] and src['actual_sha256']==sha(all_blocks[number])
            if spec['word']in (0x100,0x200,0x300):
                span = struct.unpack_from('<H',bytes.fromhex(spec['whole_command_hex']),2)[0]
                taken = spec['word']==0x100 or(spec['word']==0x200 and previous==0)or(spec['word']==0x300 and previous==1)
                assert after['decoded_length']==4+(span if taken else 0)
            else:assert after['decoded_length']==spec['native_extent']
            if after['result_words'][0]==2:previous=after['result_words'][1]
            if index+1<len(rows)//2:assert rows[2*index+2]['source']['instruction_offset']==src['instruction_offset']+after['decoded_length']
            pairs.append(dict(offset=src['instruction_offset'],word=spec['word'],frames=[before['frame'],after['frame']],
                native_decoded_length=after['decoded_length'],native_result_words=after['result_words']))
        assert pairs[0]['offset']==8 and pairs[-1]['word']==0 and pairs[-1]['native_result_words'][0]==0
        observations = nav['old_text_observations']
        assert len(observations)==len({r['id']for r in observations})==expected_count
        for group in observations+nav['original_art_pauses']+nav['choices']:
            active = next((a,b)for a,b in zip(rows[::2],rows[1::2],strict=True)if a['source']==group['source'])
            assert len(group['holds'])==2
            for hold in group['holds']:
                assert active[0]['frame']<hold['frame']<active[1]['frame']
                assert hold['capture_sha256']==photos[hold['frame']]['PNG_sha256']
                assert hold['RAM_sha256']==snapshots[hold['frame']]['sha256']
        observed = {r['id']for r in observations}
        missing = sorted(set(records)-observed)
        if number==74:
            assert not missing and len(nav['original_art_pauses'])==2 and not nav['choices']
            assert any(r['source']['first_word']==0xa000 for r in nav['original_art_pauses'])
        else:
            assert missing==['DK4_MES_B128_R0090','DK4_MES_B128_R0226','DK4_MES_B128_R0229']
            assert len(nav['choices'])==1 and not nav['original_art_pauses']
            choice = next(r for r in pairs if r['word']==0x2100)
            assert choice['offset']==2314 and choice['native_result_words'][:2]==[2,0]
            assert 'DK4_MES_B128_R0254'in observed and 'DK4_MES_B128_R0226'not in observed
        scene_results.append(dict(block=number,source_context=str(source_path),source_context_sha256=sha(source_path.read_bytes()),
            original_command_pairs=pairs,speech_observations=observations,original_interstitials=nav['original_art_pauses'],
            choices=nav['choices'],unvisited_speech_IDs=missing,actual_original_speeches=expected_count))
    ev = image.read_file('/data/EV2.DK4')
    states = []
    for frame,expected in ((76170,{74:1,128:0,25:0}),(76620,{74:1,128:0,25:0}),(93780,{74:1,128:1,25:0})):
        raw = Path(snapshots[frame]['path']).read_bytes()
        cpu,get = get_machine(arm,raw)
        owner = BASE+raw.find(ev[:96])-0x34
        values = {n:get(0x23840,owner+4,n)for n in expected}
        assert values==expected
        assert get(0x34674,get(0xCB1A8)+4+2*132)==5
        company = get(0xCB160)+4+76
        assert get(0x3CCC8,company)==60000
        context = list(struct.unpack('<3I',cpu.mem_read(owner+0x2454,12)))
        if frame>=76620:assert context==[7,5,3]
        assert bytes(cpu.mem_read(BASE,0x400000))==raw
        states.append(dict(frame=frame,original_event_completion_flags=values,original_town_ID=5,
            current_original_event_context=context,current_synthetic_company_funds=60000,all4MiB_unchanged_by_queries=True))
    ROOT.mkdir(parents=True)
    save(ROOT/'original_Hamburg79_Speyer51_and_three_access_fixture_audit.json',dict(candidate=str(rom),candidate_sha256=digest,
        terminal_frame=93780,scenes=scene_results,original_native_town_and_event_transitions=states,
        actual51_B128_speeches_one_selected_choice_two_visible_labels=True,
        three_B128_conditional_speeches_and_all_three_B25_aftermath_speeches_not_individually_activated=True,
        actual79_B74_speeches_and_Gerhard_join_panel_captured_but_not_editorially_reviewed=True,
        ordinary_default_choice_selects_stored_option0_explanation_branch=True,
        no_alternate_choice1_gameplay_claim=True,normal_docking_Port_action_and_original_events_not_overridden=True,
        all_inputs_capture_hashes4MiB_snapshots_and_three_access_footprints_verified=True,
        all_readonly_observer_boundaries_and_host_restoration_pass=True,exact_fixture_replays=replays,
        synthetic_access_only_no_earned_travel_or_funds_claim=True,
        original_text_run_not_revised_glyph_pagination_or_editorial_completion_approval=True,
        evidence={str(p):sha(p.read_bytes())for p in(RUN/'run_plan.json',RUN/'terminal.json',RUN/'navigation.jsonl',
            CAP/'capture_report.json',CAP/'observer/commands.json',TOWN,SPEYER)},
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(original_Hamburg_speeches=79,original_Speyer_speeches=51,
        command_pairs={r['block']:len(r['original_command_pairs'])for r in scene_results},
        three_access_fixtures_exact=True,original_Port_subtype3_actual=True,selected_choice0=True,
        no_revised_orcompletion_credit=True))
