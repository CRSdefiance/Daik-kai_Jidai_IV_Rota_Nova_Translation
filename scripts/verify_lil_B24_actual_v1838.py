"""Audit natural B24 entry,17 commands,26 full text holds and normal return."""
import json
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_lil_Amsterdam_location_v1833c import apply_fixture,REQUEST
from scripts.native_lil_Bruges_location_v1754 import REQUEST as BRUGES
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B24_actual_v1838')
RUN=Path('work/analysis/lil_B24_research_run_v1834')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_B24_research_run_v1834_RESEARCH_ONLY')
NAV=Path('work/analysis/lil_B24_navigation_v1837/closed_B24_unit_and_next_context.json')
BASE=0x02000000

if __name__=='__main__':
    assert not ROOT.exists()
    plan,terminal,report,trace,journal,nav=map(read,(RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',
        CAP/'observer/commands.json',CAP/'navigation_command_journal.json',NAV))
    rom=Path(plan['research_ROM']);image=NdsImage.open(rom);arm=image.read_file('/__arm9__.bin');digest=sha(rom.read_bytes())
    assert digest==plan['research_ROM_sha256']==terminal['research_ROM_sha256']==report['ROM_sha256']==nav['research_ROM_sha256']
    assert terminal['terminal']and terminal['frame']==report['frames']==nav['terminal_frame_requested']
    assert report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']
    assert 'battery_save_preloaded'not in report
    synthetic={k:v for k,v in report.items()if k.startswith('synthetic_')and v}
    assert set(synthetic)=={'synthetic_battle_recovery_proximity_fixtures'}
    fixtures=synthetic['synthetic_battle_recovery_proximity_fixtures'];assert len(fixtures)==2
    assert not trace['errors']and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
    assert all(r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']for r in trace['rows'])
    commands=[json.loads(s)for s in(RUN/'navigation.jsonl').read_text().splitlines()if s.strip()]
    assert commands==[r['command']for r in journal['commands_received']]
    assert commands[-1]=={'stop':True}and journal['last_command_frame']==report['frames']
    schedule=list(read(plan['inputs']));assert sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
    for r in journal['commands_received']:
        assert r['validation_passed'];c=r['command']
        if c.get('buttons')or c.get('touch'):
            event={'start':r['frame']+1,'duration':c['duration'],'buttons':c.get('buttons',[])}
            if c.get('touch'):event['touch']=c['touch']
            schedule.append(event)
    assert schedule==report['scripted_input_schedule']
    photos={}
    for r in report['frames_captured']:
        assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']and Image.open(r['path']).size==(256,384)
        photos[r['frame']]=r
    snapshots={}
    for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']+[report['read_only_RAM_snapshot']]:
        raw=Path(r['path']).read_bytes()
        assert len(raw)==r['bytes']==0x400000 and sha(raw)==r['sha256']and r['read_only_export']
        if 'frame'in r:snapshots[r['frame']]=r
    for fixture,frame,request in zip(fixtures,(30290,42580),(BRUGES,REQUEST),strict=True):
        assert fixture['frame']==frame and len(fixture['owned_bytes'])==16
        before=Path(snapshots[frame]['path']).read_bytes();after,recomputed=apply_fixture(arm,before,request)
        assert fixture['before_RAM_sha256']==sha(before)and fixture['after_RAM_sha256']==sha(after)
        assert {k:v for k,v in fixture.items()if k!='frame'}==json.loads(json.dumps(recomputed))
        assert all(r['address']in fixture['owned_bytes']for r in fixture['changes'])
    mapping=read('work/analysis/lil_B24_relocation_v1828/parity_and17_native_command_research.json')
    rows=[r for r in trace['rows']if r['source'].get('route')==2 and r['source'].get('block')==24]
    assert len(rows)==34
    pairs=[]
    for n,(a,b,spec)in enumerate(zip(rows[::2],rows[1::2],mapping['all17_commands'],strict=True)):
        src=a['source']
        assert a['kind']=='before_command'and b['kind']=='after_command'and src==b['source']
        assert trace['rows'][b['entry_row']]==a
        assert src['instruction_offset']==spec['new_offset']and src['first_word']==spec['word']
        assert src['whole_resident_payload_exact_ROM']and src['actual_sha256']==mapping['target_block_sha256']
        assert sha(Path(src['actual_payload_file']).read_bytes())==src['actual_sha256']
        assert b['decoded_length']==spec['new_extent']
        if n+1<17:assert rows[2*n+2]['source']['instruction_offset']==src['instruction_offset']+b['decoded_length']
        pairs.append({'source_offset':spec['old_offset'],'actual_offset':spec['new_offset'],
                      'word':spec['word'],'frames':[a['frame'],b['frame']],
                      'decoded_length':b['decoded_length'],'result_words':b['result_words']})
    assert pairs[0]['actual_offset']==8 and pairs[-1]['word']==0 and pairs[-1]['result_words'][0]==0
    assert pairs[-1]['actual_offset']+pairs[-1]['decoded_length']==mapping['new_logical_end']
    assert len(nav['holds'])==13
    fonts={r['id']:r for r in read('work/analysis/lil_B24_fonts_v1826/all13_native_macros_and_complete_font_planes.json')['cases']}
    texts={r['id']:r for r in mapping['texts']};wrapped=struct.unpack_from('<I',arm,0x54450)[0]
    checks=[];pictures=[]
    for group in nav['holds']:
        spec=texts[group['id']];ref=fonts[group['id']]
        preview=Image.open(ref['preview']).convert('RGB');assert preview.size==(216,64)
        wanted={(16+x,296+y)for y in range(64)for x in range(216)if preview.getpixel((x,y))==(0,8,0)}
        a,b=next((a,b)for a,b in zip(rows[::2],rows[1::2],strict=True)if a['source']['instruction_offset']==spec['new_offset']-5)
        holds=[]
        for hold in group['holds']:
            frame=hold['frame'];assert a['frame']<frame<b['frame']
            photo=photos[frame];raw=Path(snapshots[frame]['path']).read_bytes();im=Image.open(photo['path']).convert('RGB')
            actual={(x,y)for y in range(296,360)for x in range(16,232)if im.getpixel((x,y))==(0,8,0)}
            assert wanted==actual,(group['id'],frame,len(wanted-actual),len(actual-wanted))
            assert cstring(raw,wrapped)==bytes.fromhex(spec['encoded_hex'])[1:].replace(b'FI',b'Lil')
            at=a['source']['payload_address']-BASE
            assert sha(raw[at:at+a['source']['payload_bytes']])==mapping['target_block_sha256']
            assert hold['capture_sha256']==photo['PNG_sha256']and hold['RAM_sha256']==sha(raw)
            holds.append({'frame':frame,'capture':photo['path'],'capture_sha256':photo['PNG_sha256'],
                          'RAM_sha256':sha(raw),'whole_native_independent_actual_ink_equal':True})
        assert len(holds)==2
        checks.append({'id':group['id'],'speaker_hex':spec['encoded_hex'][:2],'two_complete_actual_holds':holds,
                       'complete_first_last_letters_bounds_left_row_origins_and_no_extra_pages':True})
        pictures.append(Image.open(holds[1]['capture']).convert('RGB'))
    assert set(texts)=={r['id']for r in checks}
    # Original event completion is queried on exported copies, never set in game.
    ev=image.read_file('/data/EV2.DK4');states=[]
    for frame,expected in ((42580,0),(report['frames'],1)):
        raw=Path(snapshots[frame]['path']).read_bytes();owner=BASE+raw.find(ev[:96])-0x34
        cpu,get=get_machine(arm,raw);complete=get(0x23840,owner+4,24)
        assert complete==expected and bytes(cpu.mem_read(BASE,0x400000))==raw
        states.append({'frame':frame,'original_event24_complete':complete,'query_keeps_all4MiB_exact':True})
    ROOT.mkdir(parents=True);sheets=[]
    for start in range(0,13,7):
        sheet=Image.new('RGB',(1052,870),(28,36,40));draw=ImageDraw.Draw(sheet)
        for j,pic in enumerate(pictures[start:start+7]):
            x=10+(j%4)*260;y=30+(j//4)*420
            draw.text((x,y-20),checks[start+j]['id'],fill=(240,240,240));sheet.paste(pic,(x,y))
        path=ROOT/f'all13_actual_review_{start//7+1}.png';sheet.save(path);sheets.append(str(path))
    save(ROOT/'complete_B24_scene_and_two_coordinate_fixture_audit.json',{
        'candidate':str(rom),'candidate_sha256':digest,'terminal_frame':report['frames'],
        'all17_original_command_pairs':pairs,'speeches':checks,'review_sheets':sheets,
        'source_event24_original_completion_before_after':states,
        'all13_speeches26_actual_complete_native_independent_holds':True,
        'original_docking_event_activation_and_normal_return_not_injected':True,
        'only_two_each16_byte_location_fixtures_no_town_event_RNG_outcome_ownership':True,
        'all_inputs_fixture_replay_PNG_hashes_and4MiB_snapshots_verified':True,
        'all_readonly_callbacks_zero_errors_mismatches_host_restored':True,
        'unreturned_at_end_outside_completed_B24':trace['unreturned_at_capture_end'],
        'docking_prompt_capture':photos[42760],'terminal_capture':photos[report['frames']],
        'visual_review_pending':True,'reference_map_and_registered_release_pending':True,
        'evidence':{str(p):sha(p.read_bytes())for p in (RUN/'run_plan.json',RUN/'terminal.json',RUN/'navigation.jsonl',
            CAP/'capture_report.json',CAP/'observer/commands.json',NAV)},
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'B24_commands':17,'individual_speeches':13,'complete_actual_holds':26,'fixture_bytes_each':16},flush=True)
