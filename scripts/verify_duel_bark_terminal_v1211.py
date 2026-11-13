"""Terminal source-bound reaction, input, fixture and normal-flow verification."""
from pathlib import Path
from shutil import copy2
from types import FunctionType
import struct
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.duel_bark_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_duel_bark_fixture_v1207 import apply_fixture
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_bark_terminal_v1211')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_bark_v1207_1206')
RUN=Path('work/analysis/duel_bark_live_v1207')
ROM=Path('out/all_routes_combined_v1206_candidate.nds')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V1206 Combat reactions')
BASE=0x02000000


def main():
    assert not ROOT.exists() and not GUIDE.exists()
    report_path=CAP/'capture_report.json';report=read(report_path)
    assert report['frames']==8203 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['goal_complete'] and not report['hardware_device_verification']
    assert report['ROM_sha256']==sha(ROM.read_bytes())
    assert read(RUN/'terminal_preservation.json')['source_and_disposable_donors_unchanged']
    for key,value in report.items():
        if key.startswith('synthetic_') and key!='synthetic_battle_recovery_proximity_fixtures':assert not value,key
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=((0x737C8,0x74010),(0xE8CC,0x11000),(0xD458,0xD540),(0x7E154,0x7E1A4),
        (0x7E988,0x7E9B0),(0xCF534,0xCF5B8),(0x519D4,0x51A28),(0xD9824,0xD9868))
    for lo,hi in spans:assert arm[lo:hi]==clean[lo:hi],(hex(lo),hex(hi))
    snapshots={}
    for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        if row['frame'] in snapshots:assert snapshots[row['frame']]['sha256']==row['sha256']
        snapshots[row['frame']]=row
    def raw(frame):
        row=snapshots[frame];body=Path(row['path']).read_bytes()
        assert len(body)==row['bytes']==0x400000 and sha(body)==row['sha256']
        return body
    fixtures=report['synthetic_battle_recovery_proximity_fixtures']
    assert len(fixtures)==31 and max(r['frame'] for r in fixtures)==5770
    seed,flag=[struct.unpack_from('<I',arm,off)[0] for off in (0xD9858,0x51A20)]
    audits=[]
    for r in fixtures:
        request={'sighting_context':'compassAttack8'} if r['context']=='compassAttack8' else {'duel_context':'healthyContact'}
        before=raw(r['frame']);after,receipt=apply_fixture(arm,before,request)
        assert r=={**receipt,'frame':r['frame']}
        assert sha(before)==r['before_RAM_sha256'] and sha(after)==r['after_RAM_sha256']
        owned=set(r['owned_bytes'])
        for at in (seed,flag):assert not owned.intersection(range(at,at+4)) and before[at-BASE:at-BASE+4]==after[at-BASE:at-BASE+4]
        bcpu,bget=get_machine(arm,before);acpu,aget=get_machine(arm,after)
        assert [bget(o) for o in (0x7F244,0x2E58C)]==[aget(o) for o in (0x7F244,0x2E58C)]==[1,1]
        actors=bget(0xCB184);assert aget(0xCB184)==actors
        assert before[actors-BASE:actors-BASE+0x19E4]==after[actors-BASE:actors-BASE+0x19E4]
        if r['context']=='healthyContact':
            assert all(v>0 for v in r['positive_captain_HP_before'])
            assert all(v>0 for values in r['live_Hull_Crew_before'] for v in values)
        audits.append({'frame':r['frame'],'context':r['context'],'before_RAM_sha256':sha(before),'after_RAM_sha256':sha(after),
            'owned_bytes':len(owned),'actual_changed_bytes':len(r['changes']),'complete4MiB_delta_RNG_and_identity_guards_pass':True})
        if len(audits)%10==0:print(len(audits),'complete pre-duel fixture audits pass',flush=True)
    journal_path=CAP/'navigation_command_journal.json';journal=read(journal_path)
    rejected=[r for r in journal['commands_received'] if not r['validation_passed']]
    assert [(r['frame'],r['command']['until'],r['rejected_before_any_input_or_fixture']) for r in rejected]==[
        (6032,6033,'Invalid duration'),(6892,6893,'Invalid duration')]
    accepted=[r for r in journal['commands_received'] if r['validation_passed']]
    schedule=read(RUN/'original_load_inputs.json')
    for r in accepted:
        command=r['command']
        if command.get('stop'):continue
        assert command['until'] in snapshots
        assert command.get('duration',12)<=command['until']-r['frame']
        if command.get('buttons') or command.get('touch') is not None:
            event={'start':r['frame']+1,'duration':command.get('duration',12),'buttons':command.get('buttons',[])}
            if command.get('touch') is not None:event['touch']=command['touch']
            schedule.append(event)
        if r['frame']>=5772:assert 'battle_fixture' not in command
    assert schedule==report['scripted_input_schedule']
    assert not any(e['start'] in (6033,6893) for e in schedule)
    scan_path=Path('work/analysis/duel_bark_actual_v1210/scan_through6913.json');scan=read(scan_path)
    assert scan['candidate_sha256']==report['ROM_sha256']
    holds=[]
    for n,frames in ((1958,(6093,6113)),(1966,(5953,5973))):
        for frame in frames:
            row=next(r for r in scan['complete_visible_holds'] if r['message_ID']==n and r['frame']==frame)
            assert row['RAM_sha256']==sha(raw(frame)) and row['actual_visible_three144x12_crops_exact']
            assert sha(Path(row['capture']).read_bytes())==row['capture_sha256']
            holds.append(row)
    entries=current_entries(common,arm)
    escape=next(r for r in read('work/analysis/escape_direct_fonts_v1185/native_direct_escape_fonts.json')['cases'] if r['message_ID']==1973)
    class CurrentFont:
        @staticmethod
        def open(path):return rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    escape_holds=[]
    owner,wrapped=[struct.unpack_from('<I',arm,o)[0] for o in (0x552A0,0x54450)]
    for frame in (7313,7323):
        body=raw(frame);cpu,get=get_machine(arm,body);actors=get(0xCB184);root=get(0xCB1A8)
        actor=get(0x82478,root+0x2090,1);assert actor==18 and get(0x53F4C,actors+4+actor*32,0x02117620)==1973
        assert body[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0]==entries[1973].text
        value=body[wrapped-BASE:wrapped-BASE+256].split(b'\0')[0];assert value.hex()==escape['formatted_hex']
        pixels=raster(arm,value,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
        assert pixels==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),escape['lines'])
        image_path=CAP/f'frame_{frame:06d}_navigation.png';im=Image.open(image_path).convert('RGB')
        expected={(16+x,296+y) for y in range(64) for x in range(228) if pixels[y*228+x]}
        actual={(x,y) for y in range(294,366) for x in range(16,244) if im.getpixel((x,y))==(0,8,0)}
        assert expected==actual
        escape_holds.append({'frame':frame,'message_ID':1973,'lines':escape['lines'],'RAM_sha256':sha(body),
            'capture':str(image_path),'capture_sha256':sha(image_path.read_bytes()),'complete228x64_font_and_actual_RGB_exact':True})
    states=[]
    for frame,expected in ((5782,[144,117]),(6913,[26,50]),(7313,[0,6])):
        body=raw(frame);cpu,get=get_machine(arm,body);actors=get(0xCB184)
        hp=[get(0x7E19C,p) for p in (actors+0x19E4,actors+4+32*32)];assert hp==expected
        states.append({'frame':frame,'own_enemy_captain_HP':hp,'RAM_sha256':sha(body)})
    flow=[]
    for frame,label in ((7443,'original abandon-ship consequence'),(7563,'original flagship loss'),(7783,'original Game Over'),(8203,'ordinary title menu')):
        body=raw(frame);image=CAP/f'frame_{frame:06d}_navigation.png'
        flow.append({'frame':frame,'visually_reviewed_state':label,'RAM_sha256':sha(body),'capture':str(image),'capture_sha256':sha(image.read_bytes())})
    ROOT.mkdir(parents=True);GUIDE.mkdir(parents=True);screens=[]
    for label,frame in (('negative_reaction',5953),('positive_reaction',6093),('preserved_escape_notice',7323),('normal_title_return',8203)):
        source=CAP/f'frame_{frame:06d}_navigation.png';dest=GUIDE/(label+'.png');copy2(source,dest)
        assert dest.read_bytes()==source.read_bytes();screens.append({'path':str(dest),'sha256':sha(dest.read_bytes()),'source':str(source),'frame':frame})
    result={'candidate':str(ROM),'candidate_sha256':report['ROM_sha256'],'terminal_frame':8203,
        'terminal_report':str(report_path),'terminal_report_sha256':sha(report_path.read_bytes()),'all31_fixture_replays':audits,
        'all_original_combat_input_outcome_and_RNG_source_spans_exact':[[lo,hi] for lo,hi in spans],
        'last_fixture_frame5770_before_duel5772':True,'actual_new_reaction_holds':holds,'actual_preserved_escape_holds':escape_holds,
        'original_A_bit5_mapping_read_only_proof':'work/analysis/duel_bark_inputs_v1209/physical_A_timing_plan.json',
        'all_accepted_navigation_targets_reached_and_exact_controller_schedule_matches':True,
        'input_event_starts_are_pause_frame_plus1_not_command_pause_frame':True,
        'two_rejected_duration2_in_one_frame_gap_commands_applied_no_input_or_fixture':rejected,
        'actual_timing_controller_events':[e for e in schedule if 5903<=e['start']<=6913],
        'natural_HP_evolution':states,'normal_A_defeat_GameOver_title_flow':flow,'source_and_disposable_saves_unchanged':True,
        'all16_have_native_fonts_only1958_and1966_have_actual_activation_claims':True,
        'targeted_headless_test_not_complete_route_or_hardware_proof':True,'guide_screenshots':screens,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'terminal_gameplay_verification.json',result);save(GUIDE/'provenance.json',result)
    print('31 fixture replays,4 new reaction+2 preserved escape holds,exact accepted inputs and normal title return pass.',flush=True)


if __name__=='__main__':main()
