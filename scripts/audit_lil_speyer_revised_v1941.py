"""Audit revised Speyer glyphs/menu, original path semantics and disclosed access."""
import json
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_lil_speyer_access_v1923 import apply_fixture,REQUEST
from scripts.native_lil_Amsterdam_location_v1833c import REQUEST as AMSTERDAM
from scripts.native_lil_Bruges_location_v1754 import REQUEST as BRUGES
from scripts.calibrate_lil_speyer_choice_v1939 import planes,verify as verify_menu
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Speyer_revised_audit_v1941')
RUN=Path('work/analysis/lil_Speyer_revised_run_v1938')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_Speyer_revised_run_v1938_RESEARCH_ONLY')
NAV=Path('work/analysis/lil_Speyer_revised_navigation_v1940/closed_revised_B128_unit_and_normal_Hamburg_return.json')
ORIGINAL=Path('work/analysis/lil_Speyer_original_audit_v1935b/original_Hamburg79_Speyer51_and_three_access_fixture_audit.json')
REF=Path('work/analysis/lil_Speyer_reference_census_v1931/all137_commands48_relative_sites_and_shipped_entry_census.json')
BASE=0x02000000

if __name__=='__main__':
    assert not ROOT.exists()
    plan,terminal,report,trace,journal,nav,original,reference=map(read,(RUN/'run_plan.json',RUN/'terminal.json',
        CAP/'capture_report.json',CAP/'observer/commands.json',CAP/'navigation_command_journal.json',NAV,ORIGINAL,REF))
    frame=nav['terminal_frame_requested']
    rom=Path(plan['research_ROM'])
    digest=sha(rom.read_bytes())
    image=NdsImage.open(rom)
    arm=image.read_file('/__arm9__.bin')
    assert digest==plan['research_ROM_sha256']==report['ROM_sha256']==nav['research_ROM_sha256']==reference['research_ROM_sha256']
    assert terminal['terminal']and terminal['frame']==report['frames']==frame
    assert report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']and'battery_save_preloaded'not in report
    assert not trace['errors']and not trace['mismatches']and trace['all_host_slots_restored_and_core_file_exact']
    assert all(r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']for r in trace['rows'])
    commands=[json.loads(s)for s in(RUN/'navigation.jsonl').read_text().splitlines()if s.strip()]
    assert commands==[r['command']for r in journal['commands_received']]
    assert commands[-1]=={'stop':True}and journal['last_command_frame']==frame
    schedule=list(read(plan['inputs']))
    assert sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
    for item in journal['commands_received']:
        assert item['validation_passed']
        command=item['command']
        if command.get('buttons')or command.get('touch'):
            event=dict(start=item['frame']+1,duration=command['duration'],buttons=command.get('buttons',[]))
            if command.get('touch'):event['touch']=command['touch']
            schedule.append(event)
    assert schedule==report['scripted_input_schedule']
    photos={r['frame']:r for r in report['frames_captured']}
    for row in photos.values():assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
    snapshots={}
    for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']+[report['read_only_RAM_snapshot']]:
        data=Path(row['path']).read_bytes()
        assert len(data)==row['bytes']==0x400000 and sha(data)==row['sha256']and row['read_only_export']
        if'frame'in row:snapshots[row['frame']]=row
    synthetic={k:v for k,v in report.items()if k.startswith('synthetic_')and v}
    assert set(synthetic)=={'synthetic_battle_recovery_proximity_fixtures'}
    fixtures=synthetic['synthetic_battle_recovery_proximity_fixtures']
    assert len(fixtures)==3
    replays=[]
    for item,at,request,count in zip(fixtures,(30290,42580,48810),(BRUGES,AMSTERDAM,REQUEST),(16,16,20),strict=True):
        assert item['frame']==at and len(item['owned_bytes'])==count
        raw=Path(snapshots[at]['path']).read_bytes()
        after,proof=apply_fixture(arm,raw,request)
        assert {k:v for k,v in item.items()if k!='frame'}==json.loads(json.dumps(proof))
        assert sha(raw)==item['before_RAM_sha256']and sha(after)==item['after_RAM_sha256']
        replays.append(dict(frame=at,owned_bytes=count,before_RAM_sha256=sha(raw),after_RAM_sha256=sha(after),all_other4MiB_exact=True))
    mapping=next(r for r in read('work/analysis/lil_Speyer_relocation_v1928/nested_source_relocation_research.json')['blocks']if r['block']==128)
    mapped=next(r for r in reference['blocks']if r['block']==128)['mapped_commands']
    texts={r['id']:r for r in mapping['text_records']}
    doc=read('translations/lil_speyer_encounter_editorial_manuscript_v2.json')
    fonts={r['id']:r for r in read(doc['native_font_proof'])['cases']}
    target=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[128]
    assert sha(target)==mapping['research_block_sha256']and len(mapped)==122
    by_offset={r['new_offset']:r for r in mapped}
    rows=[r for r in trace['rows']if r['source'].get('route')==2 and r['source'].get('block')==128]
    assert len(rows)%2==0
    pairs=[]
    previous=0
    for index,(before,after)in enumerate(zip(rows[::2],rows[1::2],strict=True)):
        src=before['source']
        spec=by_offset[src['instruction_offset']]
        assert before['kind']=='before_command'and after['kind']=='after_command'and src==after['source']
        assert trace['rows'][after['entry_row']]==before and src['first_word']==spec['word']
        assert src['whole_resident_payload_exact_ROM']and src['actual_sha256']==mapping['research_block_sha256']
        if spec['word']in(0x100,0x200,0x300):
            span=struct.unpack_from('<H',target,spec['new_offset']+2)[0]
            take=spec['word']==0x100 or(spec['word']==0x200 and previous==0)or(spec['word']==0x300 and previous==1)
            assert after['decoded_length']==4+(span if take else 0)
        else:assert after['decoded_length']==spec['new_native_extent']
        if after['result_words'][0]==2:previous=after['result_words'][1]
        if index+1<len(rows)//2:assert rows[2*index+2]['source']['instruction_offset']==src['instruction_offset']+after['decoded_length']
        pairs.append(dict(offset=src['instruction_offset'],word=spec['word'],frames=[before['frame'],after['frame']],
            native_decoded_length=after['decoded_length'],native_result_words=after['result_words']))
    prior_scene=next(r for r in original['scenes']if r['block']==128)
    assert len(pairs)==len(prior_scene['original_command_pairs'])==107
    for new,old in zip(pairs,prior_scene['original_command_pairs'],strict=True):
        assert by_offset[new['offset']]['old_offset']==old['offset']and new['word']==old['word']
        assert new['native_result_words']==old['native_result_words']
        new.update(original_observed_frames=old['frames'],observed_frame_delta=[a-b for a,b in zip(new['frames'],old['frames'],strict=True)])
    observed=[]
    wrapped=struct.unpack_from('<I',arm,0x54450)[0]
    for group in nav['holds']:
        active=next((a,b)for a,b in zip(rows[::2],rows[1::2],strict=True)if a['source']==group['holds'][0]['source'])
        assert len(group['holds'])==2
        preview=Image.open(fonts[group['id']]['preview']).convert('RGB')
        assert preview.size==(216,64)
        wanted={(16+x,296+y)for y in range(64)for x in range(216)if preview.getpixel((x,y))==(0,8,0)}
        for hold in group['holds']:
            at=hold['frame']
            assert active[0]['frame']<at<active[1]['frame']
            assert hold['capture_sha256']==photos[at]['PNG_sha256']and hold['RAM_sha256']==snapshots[at]['sha256']
            raw=Path(snapshots[at]['path']).read_bytes()
            im=Image.open(photos[at]['path']).convert('RGB')
            actual={(x,y)for y in range(296,360)for x in range(16,232)if im.getpixel((x,y))==(0,8,0)}
            assert actual==wanted and hold['complete_native_independent_actual_ink_equal']
            body=bytes.fromhex(texts[group['id']]['target_hex'])[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
            assert cstring(raw,wrapped)==body
            src=hold['source']
            assert sha(raw[src['payload_address']-BASE:src['payload_address']-BASE+src['payload_bytes']])==mapping['research_block_sha256']
        observed.append(group['id'])
    assert len(observed)==len(set(observed))==51
    assert observed==[r['id']for r in prior_scene['speech_observations']]
    missing=sorted(set(texts)-set(observed))
    assert missing==prior_scene['unvisited_speech_IDs']and len(missing)==3
    ui=read('work/analysis/lil_Speyer_choice_v1927/original_choice_decoder_VM_geometry_and_native_pixels.json')
    menu=next(r for r in ui['current_and_reviewed_VM_and_font_cases']if r['version']=='reviewed-research')
    menu_planes=planes(arm,menu)
    assert len(nav['choices'])==1
    choice=nav['choices'][0]
    active=next((a,b)for a,b in zip(rows[::2],rows[1::2],strict=True)if a['source']==choice['source'])
    assert active[1]['result_words'][:2]==[2,0]
    for hold in choice['holds']:
        at=hold['frame']
        assert active[0]['frame']<at<active[1]['frame']
        assert hold['capture_sha256']==photos[at]['PNG_sha256']and hold['RAM_sha256']==snapshots[at]['sha256']
        proof=verify_menu(Image.open(hold['capture']).convert('RGB'),menu,menu_planes)
        assert proof==hold['menu_proof']
    # B74 is unchanged and was replayed only to reach this sample. Verify its
    # original command semantics without claiming another editorial review.
    unowned=[r for r in trace['rows']if r['source'].get('route')==2 and r['source'].get('block')==74]
    prior_town=next(r for r in original['scenes']if r['block']==74)
    assert len(unowned)==2*len(prior_town['original_command_pairs'])==232
    for before,after,old in zip(unowned[::2],unowned[1::2],prior_town['original_command_pairs'],strict=True):
        assert before['source']==after['source']and before['source']['instruction_offset']==old['offset']
        assert before['source']['first_word']==old['word']and after['result_words']==old['native_result_words']
        assert after['decoded_length']==old['native_decoded_length']
    ev=image.read_file('/data/EV2.DK4')
    states=[]
    for at,complete in((76170,0),(76620,0),(frame,1)):
        raw=Path(snapshots[at]['path']).read_bytes()
        cpu,get=get_machine(arm,raw)
        owner=BASE+raw.find(ev[:96])-0x34
        flags={n:get(0x23840,owner+4,n)for n in(25,74,128)}
        assert flags=={25:0,74:1,128:complete}
        assert get(0x34674,get(0xCB1A8)+4+2*132)==5
        assert get(0x3CCC8,get(0xCB160)+4+76)==60000
        if at>=76620:assert list(struct.unpack('<3I',cpu.mem_read(owner+0x2454,12)))==[7,5,3]
        assert bytes(cpu.mem_read(BASE,0x400000))==raw
        states.append(dict(frame=at,original_event_completion_flags=flags,original_town_ID=5,current_synthetic_company_funds=60000))
    ROOT.mkdir(parents=True)
    selected=['DK4_MES_B128_R0006','DK4_MES_B128_R0010','DK4_MES_B128_R0014','DK4_MES_B128_R0073',
        'DK4_MES_B128_R0080','DK4_MES_B128_R0106','DK4_MES_B128_R0118','DK4_MES_B128_R0135',
        'DK4_MES_B128_R0183','DK4_MES_B128_R0268','DK4_MES_B128_R0303','DK4_MES_B128_R0317']
    by_id={r['id']:r for r in nav['holds']}
    sheets=[]
    for start in range(0,len(selected),4):
        sheet=Image.new('RGB',(512,800),'#263238')
        draw=ImageDraw.Draw(sheet)
        for index,ident in enumerate(selected[start:start+4]):
            x,y=index%2*256,index//2*400
            draw.text((x+3,y+3),ident,fill='white')
            sheet.paste(Image.open(by_id[ident]['holds'][1]['capture']).convert('RGB'),(x,y+16))
        path=ROOT/f'representative_revised_contacts_{start//4+1:02d}.png'
        sheet.save(path)
        sheets.append(str(path))
    save(ROOT/'revised_Speyer51_choice_and_three_access_fixture_audit.json',dict(candidate=str(rom),candidate_sha256=digest,
        terminal_frame=frame,original_command_pairs=pairs,revised_speech_observations=nav['holds'],revised_choice=choice,
        representative_contact_sheets=sheets,representative_visual_record_IDs=selected,
        original_native_town_and_event_transitions=states,unvisited_B128_speech_IDs=missing,
        all_three_B25_aftermath_speeches_not_individually_activated=True,
        all_inputs_capture_hashes4MiB_snapshots_and_three_access_footprints_verified=True,
        all_readonly_observer_boundaries_and_host_restoration_pass=True,exact_fixture_replays=replays,
        normal_docking_Port_action_B128_entry_and_Hamburg_return_not_overridden=True,
        all51_activated_revised_speeches102_holds_complete_native_independent_actual_glyphs=True,
        both_revised_choice_labels_two_actual_holds_complete_native_ink_and_bounds=True,
        native_menu_geometry_and_fixed_margins_calibrated_before_revised_pixels=True,
        same107_original_B128_commands_results_and_event_transitions=True,
        same116_unowned_B74_command_results=True,six_conditional_speeches_not_individually_activated=True,
        choice0_explanatory_branch_actual_choice1_only_source_native_VM=True,
        synthetic_travel_and_funds_not_earned_gameplay_claim=True,
        command_frame_deltas_recorded_not_required_equal_after_prose_resize=True,
        not_a_registered_release_or_full_conditional_path_coverage=True,
        evidence={str(p):sha(p.read_bytes())for p in(RUN/'run_plan.json',RUN/'terminal.json',RUN/'navigation.jsonl',
            CAP/'capture_report.json',CAP/'observer/commands.json',NAV,ORIGINAL,REF)},
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(revised_actual_speeches=51,complete_actual_native_speech_holds=102,choice_holds=2,
        original_command_pairs=107,unowned_B74_commands=116,conditional_speeches_unvisited=6,
        terminal_frame=frame,three_access_footprints_exact=True))
