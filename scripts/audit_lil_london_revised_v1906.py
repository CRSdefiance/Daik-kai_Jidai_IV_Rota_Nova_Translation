"""Audit complete revised glyph holds,path semantics,art pan and access footprints."""
import json
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_lil_london_location_v1883 import apply_fixture,REQUEST
from scripts.native_lil_Amsterdam_location_v1833c import REQUEST as AMSTERDAM
from scripts.native_lil_Bruges_location_v1754 import REQUEST as BRUGES
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_London_revised_audit_v1906')
RUN=Path('work/analysis/lil_London_revised_run_v1903')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_London_revised_run_v1903_RESEARCH_ONLY')
NAV=Path('work/analysis/lil_London_revised_navigation_v1904/closed_revised_B26_unit_and_next_context.json')
ORIGINAL=Path('work/analysis/lil_London_context_audit_v1892/original_London105_branch_and_three_fixture_audit.json')
BASE=0x02000000

if __name__=='__main__':
    assert not ROOT.exists()
    plan,terminal,report,trace,journal,nav=map(read,(RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',
        CAP/'observer/commands.json',CAP/'navigation_command_journal.json',NAV))
    frame=nav['terminal_frame_requested']
    rom=Path(plan['research_ROM'])
    digest=sha(rom.read_bytes())
    image=NdsImage.open(rom)
    arm=image.read_file('/__arm9__.bin')
    assert digest==plan['research_ROM_sha256']==report['ROM_sha256']==nav['research_ROM_sha256']
    assert terminal['terminal'] and terminal['frame']==report['frames']==frame
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert 'battery_save_preloaded' not in report
    synthetic={k:v for k,v in report.items() if k.startswith('synthetic_') and v}
    assert set(synthetic)=={'synthetic_battle_recovery_proximity_fixtures'}
    fixtures=synthetic['synthetic_battle_recovery_proximity_fixtures']
    assert len(fixtures)==3
    assert not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
    assert all(r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'] for r in trace['rows'])
    commands=[json.loads(s) for s in (RUN/'navigation.jsonl').read_text().splitlines() if s.strip()]
    assert commands==[r['command'] for r in journal['commands_received']]
    assert commands[-1]=={'stop':True} and journal['last_command_frame']==frame
    schedule=list(read(plan['inputs']))
    assert sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
    for item in journal['commands_received']:
        assert item['validation_passed']
        c=item['command']
        if c.get('buttons') or c.get('touch'):
            event=dict(start=item['frame']+1,duration=c['duration'],buttons=c.get('buttons',[]))
            if c.get('touch'):event['touch']=c['touch']
            schedule.append(event)
    assert schedule==report['scripted_input_schedule']
    photos={r['frame']:r for r in report['frames_captured']}
    for r in photos.values():assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']
    snapshots={}
    for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']+[report['read_only_RAM_snapshot']]:
        data=Path(r['path']).read_bytes()
        assert len(data)==r['bytes']==0x400000 and sha(data)==r['sha256'] and r['read_only_export']
        if 'frame' in r:snapshots[r['frame']]=r
    replays=[]
    for item,at,request in zip(fixtures,(30290,42580,48810),(BRUGES,AMSTERDAM,REQUEST),strict=True):
        assert item['frame']==at and len(item['owned_bytes'])==16
        raw=Path(snapshots[at]['path']).read_bytes()
        after,proof=apply_fixture(arm,raw,request)
        assert {k:v for k,v in item.items() if k!='frame'}==json.loads(json.dumps(proof))
        assert sha(raw)==item['before_RAM_sha256'] and sha(after)==item['after_RAM_sha256']
        replays.append(dict(frame=at,owned_bytes=16,before_RAM_sha256=sha(raw),after_RAM_sha256=sha(after),all_other4MiB_exact=True))
    packet=read('work/analysis/lil_London_source_v1879b/all111_clean_current_native_source_context.json')
    mapping=read('work/analysis/lil_London_relocation_v1899/nested_source_relocation_research.json')
    reference=read('work/analysis/lil_London_reference_census_v1905/all262_commands92_relative_sites_and_shipped_entry_census.json')
    doc=read('translations/lil_london_editorial_manuscript_v4.json')
    fonts={r['id']:r for r in read(doc['native_font_proof'])['cases']}
    texts={r['id']:r for r in mapping['text_records']}
    target=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[26]
    assert sha(target)==mapping['research_block_sha256'] and reference['research_ROM_sha256']==digest
    old_by={r['offset']:r for r in packet['all_current_native_commands']}
    mapped=reference['mapped_commands']
    assert len(mapped)==262
    by_offset={r['new_offset']:{**old_by[r['old_offset']], 'offset':r['new_offset'],
        'native_extent':r['new_native_extent'],'whole_command_hex':target[r['new_offset']:r['new_offset']+r['new_native_extent']].hex()} for r in mapped}
    rows=[r for r in trace['rows'] if r['source'].get('route')==2 and r['source'].get('block')==26]
    assert len(rows)%2==0
    pairs=[]
    previous=0
    for n,(a,b) in enumerate(zip(rows[::2],rows[1::2],strict=True)):
        src=a['source']
        spec=by_offset[src['instruction_offset']]
        assert a['kind']=='before_command' and b['kind']=='after_command' and src==b['source']
        assert trace['rows'][b['entry_row']]==a and src['first_word']==spec['word']
        assert src['whole_resident_payload_exact_ROM'] and src['actual_sha256']==mapping['research_block_sha256']
        if spec['word'] in (0x100,0x200,0x300):
            span=struct.unpack_from('<H',bytes.fromhex(spec['whole_command_hex']),2)[0]
            take=spec['word']==0x100 or (spec['word']==0x200 and previous==0) or (spec['word']==0x300 and previous==1)
            assert b['decoded_length']==4+(span if take else 0)
        else:assert b['decoded_length']==spec['native_extent']
        if b['result_words'][0]==2:previous=b['result_words'][1]
        if n+1<len(rows)//2:assert rows[2*n+2]['source']['instruction_offset']==src['instruction_offset']+b['decoded_length']
        pairs.append(dict(offset=src['instruction_offset'],word=spec['word'],frames=[a['frame'],b['frame']],
            native_decoded_length=b['decoded_length'],native_result_words=b['result_words']))
    assert pairs[0]['offset']==8 and pairs[-1]['word']==0 and pairs[-1]['native_result_words'][0]==0
    wrapped=struct.unpack_from('<I',arm,0x54450)[0]
    observed=[]
    for group in nav['holds']:
        active=next((a,b) for a,b in zip(rows[::2],rows[1::2],strict=True) if a['source']==group['holds'][0]['source'])
        assert len(group['holds'])==2
        modal=texts[group['id']]['consumer']=='original_FE_modal_5473C_mode1'
        width=228 if modal else 216
        expected=Image.open(fonts[group['id']]['preview']).convert('RGB')
        assert expected.size==(width,64)
        wanted={(16+x,296+y) for y in range(64) for x in range(width) if expected.getpixel((x,y))==(0,8,0)}
        for hold in group['holds']:
            at=hold['frame']
            assert active[0]['frame']<at<active[1]['frame']
            assert hold['capture_sha256']==photos[at]['PNG_sha256'] and hold['RAM_sha256']==snapshots[at]['sha256']
            raw=Path(snapshots[at]['path']).read_bytes()
            photo=Image.open(photos[at]['path']).convert('RGB')
            actual={(x,y) for y in range(296,360) for x in range(16,16+width) if photo.getpixel((x,y))==(0,8,0)}
            assert actual==wanted and hold['complete_native_independent_actual_ink_equal']
            if not modal:
                body=bytes.fromhex(texts[group['id']]['target_hex'])[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
                assert cstring(raw,wrapped)==body
            src=hold['source']
            assert sha(raw[src['payload_address']-BASE:src['payload_address']-BASE+src['payload_bytes']])==mapping['research_block_sha256']
        observed.append(group['id'])
    assert len(observed)==len(set(observed))==105
    missing=sorted(set(texts)-set(observed))
    assert len(missing)==6
    assert len(nav['original2000_art_pauses'])==4 and len(nav['original4905_art_pans'])==1
    for art in nav['original2000_art_pauses']:
        assert art['source']['first_word']==0x2000 and len(art['holds'])==2
    pan=nav['original4905_art_pans'][0]
    assert pan['before']['source']['first_word']==0x4905 and pan['original_timed_pan_completes_without_input']
    ev=image.read_file('/data/EV2.DK4')
    states=[]
    for at,complete in ((48810,0),(49440,0),(frame,1)):
        raw=Path(snapshots[at]['path']).read_bytes()
        cpu,get=get_machine(arm,raw)
        owner=BASE+raw.find(ev[:96])-0x34
        town=get(0xCB178)+4
        assert get(0xB50D8,town)==2 and get(0x23840,owner+4,26)==complete
        assert bytes(cpu.mem_read(BASE,0x400000))==raw
        states.append(dict(frame=at,original_known_London_flag=2,original_event26_complete=complete))
    original=read(ORIGINAL)
    inverse={r['new_offset']:r['old_offset'] for r in mapped}
    assert len(pairs)==len(original['original_command_pairs'])==228
    for new,old in zip(pairs,original['original_command_pairs'],strict=True):
        assert inverse[new['offset']]==old['offset'] and new['word']==old['word']
        assert new['native_result_words']==old['native_result_words']
        new['original_observed_frames']=old['frames']
        new['observed_frame_delta']=[a-b for a,b in zip(new['frames'],old['frames'],strict=True)]
    assert observed==[r['id'] for r in original['original_speech_observations']]
    assert [(s['original_known_London_flag'],s['original_event26_complete']) for s in states]==[(s['original_known_London_flag'],s['original_event26_complete']) for s in original['original_native_town_and_event_transitions']]
    ROOT.mkdir(parents=True)
    # Full pixel checks cover210holds;visual review focuses ondistinct consumers,
    # long paragraphs,substitutions,the clothing joke andnormal return.
    selected=['DK4_MES_B26_R0005','DK4_MES_B26_R0080','DK4_MES_B26_R0087','DK4_MES_B26_R0090',
        'DK4_MES_B26_R0098','DK4_MES_B26_R0137','DK4_MES_B26_R0175','DK4_MES_B26_R0186',
        'DK4_MES_B26_R0320','DK4_MES_B26_R0346','DK4_MES_B26_R0386','DK4_MES_B26_R0450',
        'DK4_MES_B26_R0461','DK4_MES_B26_R0541','DK4_MES_B26_R0566','DK4_MES_B26_R0654']
    by_id={r['id']:r for r in nav['holds']}
    sheets=[]
    for start in range(0,len(selected),4):
        sheet=Image.new('RGB',(512,800),'#263238')
        draw=ImageDraw.Draw(sheet)
        for n,ident in enumerate(selected[start:start+4]):
            x,y=n%2*256,n//2*400
            draw.text((x+3,y+3),ident,fill='white')
            shot=Image.open(by_id[ident]['holds'][1]['capture']).convert('RGB')
            sheet.paste(shot,(x,y+16))
        path=ROOT/f'representative_revised_contacts_{start//4+1:02d}.png'
        sheet.save(path)
        sheets.append(str(path))
    save(ROOT/'revised_London105_branch_and_three_fixture_audit.json',dict(candidate=str(rom),candidate_sha256=digest,
        terminal_frame=frame,original_command_pairs=pairs,revised_speech_observations=nav['holds'],
        representative_contact_sheets=sheets,representative_visual_record_IDs=selected,
        original_art2000_interstitials=nav['original2000_art_pauses'],original4905_art_pan=pan,
        original_native_town_and_event_transitions=states,unvisited_original_speech_IDs=missing,
        all_inputs_capture_hashes4MiB_snapshots_and_three_coordinate_footprints_verified=True,
        all_readonly_observer_boundaries_and_host_restoration_pass=True,exact_fixture_replays=replays,
        normal_docking_B26_entry_and_terminal_return_not_injected=True,
        all105_activated_revised_speeches210_holds_complete_native_independent_actual_glyphs=True,
        same228_original_commands_results_and_event_transitions=True,
        six_conditional_records_not_individually_activated=True,
        command_frame_deltas_recorded_not_required_equal_after_prose_resize=True,
        not_a_registered_release_or_full_conditional_branch_coverage=True,
        evidence={str(p):sha(p.read_bytes()) for p in (RUN/'run_plan.json',RUN/'terminal.json',RUN/'navigation.jsonl',
            CAP/'capture_report.json',CAP/'observer/commands.json',NAV,ORIGINAL)},
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(revised_actual_speeches=105,complete_actual_native_holds=210,original_command_pairs=228,
        conditional_unvisited=6,terminal_frame=frame,three_coordinate_footprints_exact=True))
