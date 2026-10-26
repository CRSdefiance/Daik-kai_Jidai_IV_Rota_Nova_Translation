"""Audit revised Stockholm actual glyphs, original path and three coordinate-only fixtures."""
import json
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from PIL import Image
from scripts.verify_port_gameplay_v762 import cstring
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_lil_Stockholm_location_v1850 import apply_fixture,REQUEST
from scripts.native_lil_Amsterdam_location_v1833c import REQUEST as AMSTERDAM
from scripts.native_lil_Bruges_location_v1754 import REQUEST as BRUGES
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Stockholm_revised_audit_v1867c')
RUN=Path('work/analysis/lil_Stockholm_revised_run_v1864')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_Stockholm_revised_run_v1864_RESEARCH_ONLY')
NAV=Path('work/analysis/lil_Stockholm_revised_navigation_v1865/closed_revised_B27_unit_and_next_context.json')
BASE=0x02000000

if __name__=='__main__':
    assert not ROOT.exists()
    plan,terminal,report,trace,journal,nav=map(read,(RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',
        CAP/'observer/commands.json',CAP/'navigation_command_journal.json',NAV))
    rom=Path(plan['research_ROM']);digest=sha(rom.read_bytes());im=NdsImage.open(rom);arm=im.read_file('/__arm9__.bin')
    assert digest==plan['research_ROM_sha256']==report['ROM_sha256']==nav['research_ROM_sha256']
    assert terminal['terminal']and terminal['frame']==report['frames']==62850
    assert report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']and'battery_save_preloaded'not in report
    synthetic={k:v for k,v in report.items()if k.startswith('synthetic_')and v}
    assert set(synthetic)=={'synthetic_battle_recovery_proximity_fixtures'}
    fixtures=synthetic['synthetic_battle_recovery_proximity_fixtures'];assert len(fixtures)==3
    assert not trace['errors']and not trace['mismatches']and trace['all_host_slots_restored_and_core_file_exact']
    assert all(r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']for r in trace['rows'])
    commands=[json.loads(s)for s in(RUN/'navigation.jsonl').read_text().splitlines()if s.strip()]
    assert commands==[r['command']for r in journal['commands_received']]
    assert commands[-1]=={'stop':True}and journal['last_command_frame']==62850
    schedule=list(read(plan['inputs']));assert sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
    for item in journal['commands_received']:
        assert item['validation_passed'];c=item['command']
        if c.get('buttons')or c.get('touch'):
            event={'start':item['frame']+1,'duration':c['duration'],'buttons':c.get('buttons',[])}
            if c.get('touch'):event['touch']=c['touch']
            schedule.append(event)
    assert schedule==report['scripted_input_schedule']
    photos={r['frame']:r for r in report['frames_captured']}
    for r in photos.values():assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']
    snapshots={}
    for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']+[report['read_only_RAM_snapshot']]:
        raw=Path(r['path']).read_bytes();assert len(raw)==r['bytes']==0x400000 and sha(raw)==r['sha256']and r['read_only_export']
        if 'frame'in r:snapshots[r['frame']]=r
    replays=[]
    for item,frame,request in zip(fixtures,(30290,42580,48810),(BRUGES,AMSTERDAM,REQUEST),strict=True):
        assert item['frame']==frame and len(item['owned_bytes'])==16
        raw=Path(snapshots[frame]['path']).read_bytes();after,proof=apply_fixture(arm,raw,request)
        assert {k:v for k,v in item.items()if k!='frame'}==json.loads(json.dumps(proof))
        assert sha(raw)==item['before_RAM_sha256']and sha(after)==item['after_RAM_sha256']
        replays.append({'frame':frame,'owned_bytes':16,'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(after),
                        'all_other4MiB_exact':True})
    packet=read('work/analysis/lil_Stockholm_source_v1848b/all51_clean_current_native_source_context.json')
    reference=read('work/analysis/lil_Stockholm_reference_census_v1866/all102_commands24_relative_sites_and_shipped_entry_census.json')
    mapping=read('work/analysis/lil_Stockholm_relocation_v1861/nested_source_relocation_research.json')['blocks'][0]
    assert reference['research_ROM_sha256']==digest
    target=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[27]
    assert sha(target)==mapping['research_block_sha256']
    old_by={r['offset']:r for r in packet['all_current_native_commands']}
    mapped=reference['mapped_commands'];assert len(mapped)==102
    by_offset={r['new_offset']:{**old_by[r['old_offset']],'offset':r['new_offset'],
        'native_extent':r['new_native_extent'],'whole_command_hex':target[r['new_offset']:r['new_offset']+r['new_native_extent']].hex()}
        for r in mapped}
    fonts={r['id']:r for r in read('work/analysis/lil_Stockholm_fonts_v1858/all51_native_macros_and_complete_font_planes.json')['cases']}
    texts={r['id']:r for r in mapping['text_records']}
    wrapped=struct.unpack_from('<I',arm,0x54450)[0]
    rows=[r for r in trace['rows']if r['source'].get('route')==2 and r['source'].get('block')==27]
    assert len(rows)%2==0;pairs=[];previous=0
    for n,(a,b)in enumerate(zip(rows[::2],rows[1::2],strict=True)):
        src=a['source'];spec=by_offset[src['instruction_offset']]
        assert a['kind']=='before_command'and b['kind']=='after_command'and src==b['source']
        assert trace['rows'][b['entry_row']]==a and src['first_word']==spec['word']
        assert src['whole_resident_payload_exact_ROM']and src['actual_sha256']==mapping['research_block_sha256']
        if spec['word']in(0x100,0x200,0x300):
            raw_command=bytes.fromhex(spec['whole_command_hex']);span=struct.unpack_from('<H',raw_command,2)[0]
            take=spec['word']==0x100 or(spec['word']==0x200 and previous==0)or(spec['word']==0x300 and previous==1)
            assert b['decoded_length']==4+(span if take else 0)
        else:assert b['decoded_length']==spec['native_extent']
        if b['result_words'][0]==2:previous=b['result_words'][1]
        if n+1<len(rows)//2:assert rows[2*n+2]['source']['instruction_offset']==src['instruction_offset']+b['decoded_length']
        pairs.append({'offset':src['instruction_offset'],'word':spec['word'],'frames':[a['frame'],b['frame']],
            'native_decoded_length':b['decoded_length'],'native_result_words':b['result_words']})
    assert pairs[0]['offset']==8 and pairs[-1]['word']==0 and pairs[-1]['native_result_words'][0]==0
    observed=[]
    for group in nav['holds']:
        active=next((a,b)for a,b in zip(rows[::2],rows[1::2],strict=True)if a['source']==group['holds'][0]['source'])
        assert len(group['holds'])==2
        for h in group['holds']:
            assert active[0]['frame']<h['frame']<active[1]['frame']
            assert h['capture_sha256']==photos[h['frame']]['PNG_sha256']and h['RAM_sha256']==snapshots[h['frame']]['sha256']
            raw=Path(snapshots[h['frame']]['path']).read_bytes()
            photo=Image.open(photos[h['frame']]['path']).convert('RGB')
            expected=Image.open(fonts[group['id']]['preview']).convert('RGB')
            wanted={(16+x,296+y)for y in range(64)for x in range(216)if expected.getpixel((x,y))==(0,8,0)}
            actual={(x,y)for y in range(296,360)for x in range(16,232)if photo.getpixel((x,y))==(0,8,0)}
            assert actual==wanted and h['complete_native_independent_actual_ink_equal']
            assert cstring(raw,wrapped)==bytes.fromhex(texts[group['id']]['target_hex'])[1:].replace(b'FI',b'Lil')
            src=h['source'];at=src['payload_address']-BASE
            assert sha(raw[at:at+src['payload_bytes']])==mapping['research_block_sha256']
        observed.append(group['id'])
    assert len(observed)==len(set(observed))==36 and sorted({r['prefix_hex']for r in nav['holds']})==['01','02','09','14']
    missing=sorted(set(r['id']for r in packet['records'])-set(observed));assert len(missing)==15
    assert len(nav['original2000_art_pauses'])==1
    art=nav['original2000_art_pauses'][0];assert art['source']['first_word']==0x2000 and len(art['holds'])==2
    ev=im.read_file('/data/EV2.DK4');states=[]
    for frame,known,complete in ((48810,0,0),(50040,2,0),(62850,2,1)):
        raw=Path(snapshots[frame]['path']).read_bytes();cpu,get=get_machine(arm,raw)
        owner=BASE+raw.find(ev[:96])-0x34;town=get(0xCB178)+4+7*108
        assert get(0xB50D8,town)==known and get(0x23840,owner+4,27)==complete
        assert bytes(cpu.mem_read(BASE,0x400000))==raw
        states.append({'frame':frame,'original_known_Stockholm_flag':known,'original_event27_complete':complete})
    conditions=[]
    raw=Path(snapshots[48810]['path']).read_bytes();cpu,get=get_machine(arm,raw)
    for prefix,value in((20,1),(16,0)):
        word=0x3000FE00|prefix;cpu.mem_write(0x02641000,struct.pack('<I',word));cpu.mem_write(0x02641040,struct.pack('<2I',0x021343F8,0x02641000))
        result=get(0x256A0,0x02641040);assert result==value and bytes(cpu.mem_read(BASE,0x400000))==raw
        conditions.append({'source_condition_word':word,'native_value':result,'input4MiB_unchanged':True})
    original=read('work/analysis/lil_Stockholm_context_audit_v1855/original_Stockholm36_branch_and_three_fixture_audit.json')
    inverse={r['new_offset']:r['old_offset']for r in mapped}
    assert len(pairs)==len(original['original_command_pairs'])==75
    for new,old in zip(pairs,original['original_command_pairs'],strict=True):
        assert inverse[new['offset']]==old['offset']and new['word']==old['word']
        assert new['native_result_words']==old['native_result_words']
        new['original_observed_frames']=old['frames']
        new['observed_frame_delta']=[a-b for a,b in zip(new['frames'],old['frames'],strict=True)]
    assert observed==[r['id']for r in original['original_speech_observations']]
    assert states==original['original_native_town_and_event_transitions']
    ROOT.mkdir(parents=True)
    sheets=[]
    for page in range(6):
        sheet=Image.new('RGB',(512,1188),(35,40,45))
        from PIL import ImageDraw
        draw=ImageDraw.Draw(sheet)
        for n,group in enumerate(nav['holds'][page*6:(page+1)*6]):
            x=n%2*256;y=n//2*396
            draw.text((x+4,y+1),group['id'],fill='white')
            shot=Image.open(group['holds'][0]['capture']).convert('RGB');assert shot.size==(256,384)
            sheet.paste(shot,(x,y+12))
        path=ROOT/f'actual_revised_contacts_{page+1:02}.png';sheet.save(path);sheets.append(str(path))
    save(ROOT/'revised_Stockholm36_branch_and_three_fixture_audit.json',{'candidate':str(rom),'candidate_sha256':digest,
        'terminal_frame':62850,'original_command_pairs':pairs,'revised_speech_observations':nav['holds'],'contact_sheets':sheets,
        'original_art2000_interstitial':art,'original_native_town_and_event_transitions':states,
        'inline_original_actor_presence_conditions':conditions,'unvisited_original_speech_IDs':missing,
        'original_Gerhard_branch_absent_not_a_formatter_failure':True,'nine0x10_speaker_objects_unvisited_here':True,
        'all_inputs_capture_hashes4MiB_snapshots_and_three_coordinate_footprints_verified':True,
        'all_readonly_observer_boundaries_and_host_restoration_pass':True,'exact_fixture_replays':replays,
        'normal_discovery_docking_B27_entry_and_terminal_return_not_injected':True,
        'all36_activated_revised_speeches72_holds_complete_native_independent_actual_glyphs':True,
        'same75_original_commands_results_and_event_transitions':True,
        '15_conditional_records_not_individually_activated':True,
        'not_a_registered_release_or_full_conditional_branch_coverage':True,
        'command_frame_deltas_recorded_not_required_equal_after_prose_resize':True,
        'evidence':{str(p):sha(p.read_bytes())for p in(RUN/'run_plan.json',RUN/'terminal.json',RUN/'navigation.jsonl',
            CAP/'capture_report.json',CAP/'observer/commands.json',NAV)},
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'actual_revised_speeches':36,'original_command_pairs':len(pairs),'unvisited_conditional':15,
        'Gerhard_original_presence_predicate':0,'three_coordinate_fixtures_replayed':True},flush=True)
