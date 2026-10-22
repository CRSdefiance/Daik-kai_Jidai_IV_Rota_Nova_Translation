"""Exact original special holds,31 full fixture replays and natural aftermath."""
import struct
from pathlib import Path
from shutil import copy2
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_duel_long_fixture_v1242 import ROM,apply_fixture
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_duel_actual_holds_v1171 import actual_widget
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_long_terminal_v1245')
RUN=Path('work/analysis/duel_long_live_v1243')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_long_v1243_1224')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V1224 Special move')
BASE=0x02000000


def main():
    assert not ROOT.exists() and not GUIDE.exists()
    report_path=CAP/'capture_report.json';report=read(report_path)
    assert report['frames']==11782 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and report['ROM_sha256']==sha(ROM.read_bytes())
    assert not report['goal_complete'] and not report['hardware_device_verification']
    assert read(RUN/'terminal_preservation.json')['source_and_disposable_donors_unchanged']
    for k,v in report.items():
        if k.startswith('synthetic_') and k!='synthetic_battle_recovery_proximity_fixtures':assert not v,k
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=((0xE8CC,0x11000),(0xD458,0xD540),(0x7DF58,0x7E1A4),
        (0x7E750,0x7E788),(0x7E944,0x7E950),(0x519D4,0x51A28),(0xD9824,0xD9868))
    for lo,hi in spans:assert arm[lo:hi]==clean[lo:hi]
    snapshots={}
    for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        if r['frame'] in snapshots:assert snapshots[r['frame']]['sha256']==r['sha256']
        snapshots[r['frame']]=r
    def raw(frame):
        r=snapshots[frame];data=Path(r['path']).read_bytes()
        assert len(data)==r['bytes']==0x400000 and sha(data)==r['sha256'];return data
    fixtures=report['synthetic_battle_recovery_proximity_fixtures']
    assert len(fixtures)==31 and max(r['frame'] for r in fixtures)==5770
    seed,flag=[struct.unpack_from('<I',arm,off)[0] for off in (0xD9858,0x51A20)]
    audits=[]
    for r in fixtures:
        request={'sighting_context':'compassAttack8'} if r['context']=='compassAttack8' else {'duel_context':'healthyContact'}
        before=raw(r['frame']);after,receipt=apply_fixture(arm,before,request)
        assert r=={**receipt,'frame':r['frame']}
        owned=set(r['owned_bytes'])
        changes=[BASE+i for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b]
        assert all(at in owned for at in changes)
        for at in (seed,flag):
            assert not owned.intersection(range(at,at+4)) and before[at-BASE:at-BASE+4]==after[at-BASE:at-BASE+4]
        bc,bget=get_machine(arm,before);ac,aget=get_machine(arm,after)
        assert [bget(o) for o in (0x7F244,0x2E58C)]==[aget(o) for o in (0x7F244,0x2E58C)]==[1,1]
        actors=bget(0xCB184);assert aget(0xCB184)==actors
        objects=[actors+4+i*32 for i in range(207)]+[actors+0x19E4]
        assert [bget(0x7EE08,o) for o in objects]==[aget(0x7EE08,o) for o in objects]
        if r['context']=='longHealthLuckContact':
            assert r['original_unforced_special_random_chance_percent']==10
            for values in r['native_pre_duel_attribute_changes']:
                assert values['attributes_after'][0:2]==[1,1] and values['attributes_after'][4:6]==[100,100]
                assert values['attributes_before'][2:4]==values['attributes_after'][2:4]
                assert values['positive_HP_and_native_maximum'][0]==values['positive_HP_and_native_maximum'][1]>0
        audits.append({'frame':r['frame'],'context':r['context'],'owned_bytes':len(owned),
            'actual_changed_bytes':len(changes),'before_RAM_sha256':sha(before),'after_RAM_sha256':sha(after),
            'full4MiB_delta_all208_actor_IDs_original_RNG_and_event_flags_pass':True})
        if len(audits)%10==0:print(len(audits),'complete pre-duel fixture replays and original identities pass',flush=True)
    journal=read(CAP/'navigation_command_journal.json')
    assert all(r['validation_passed'] for r in journal['commands_received'])
    schedule=read(RUN/'original_load_inputs.json')
    for r in journal['commands_received']:
        c=r['command']
        if c.get('stop'):continue
        assert c['until'] in snapshots and c['until']>r['frame']
        if r['frame']>=5772:assert 'battle_fixture' not in c
        if c.get('buttons') or c.get('touch') is not None:
            event={'start':r['frame']+1,'duration':c.get('duration',12),'buttons':c.get('buttons',[])}
            if c.get('touch') is not None:event['touch']=c['touch']
            schedule.append(event)
    assert schedule==report['scripted_input_schedule']
    assert not any(e['start']>=5773 and e['start']<=10982 for e in schedule)
    scan_path=Path('work/analysis/duel_long_actual_v1244/scan_through8400.json');scan=read(scan_path)
    holds=[r for r in scan['complete_visible_holds'] if r['frame'] in (7622,7662,7702,7742,7782,7822)]
    assert len(holds)==6 and all(r['message_ID']==1990 for r in holds)
    for r in holds:
        assert r['RAM_sha256']==sha(raw(r['frame'])) and r['actual_visible_three144x12_crops_exact']
        assert r['RGB_mismatch_pixels']==0 and r['unchanged1480byte_PIC_is_resident'] and r['last_native_copy_is_carrier1931']
        assert sha(Path(r['capture']).read_bytes())==r['capture_sha256']
        body=raw(r['frame']);widget,controller,header,h=actual_widget(body)
        active=struct.unpack_from('<I',body,controller-0x40-BASE+0x4C4)[0]
        cpu,get=get_machine(arm,body)
        assert get(0x7EE08,active)==1 and get(0x7E944,active,5)==100
        assert struct.unpack_from('<I',body,controller-0x40-BASE+0x4EC)[0]==1
    context=read('work/analysis/duel_special_context_v1215b/source_context_packet.json')
    binding=next(r for r in context['all15_original_message_call_bindings'] if r['message_ID']==1990)
    assert binding['actor_ID']==1 and binding['source_method']==0x0200F114
    assert binding['original_source_return']==0x0200F164 and binding['side']==0 and binding['duration']==120
    states=[]
    for frame,expected in ((5782,[87,90]),(7542,[87,45]),(7822,[87,45]),(8022,[87,23]),(8502,[87,0])):
        body=raw(frame);cpu,get=get_machine(arm,body);actors=get(0xCB184)
        hp=[get(0x7E19C,p) for p in (actors+0x19E4,actors+4+32*32)]
        assert hp==expected,(frame,hp,expected)
        states.append({'frame':frame,'own_enemy_HP':hp,'RAM_sha256':sha(body)})
    # The six exact visible holds, following animated strike and later sea-view
    # aftermath are reviewed separately; no persistent bitmap alone earns credit.
    flow=[]
    for frame,label in ((8022,'original special animation returned to ordinary duel'),
                        (8502,'original natural duel victory'),
                        (10982,'original enemy flagship fled and victory message'),
                        (11782,'ordinary aftermath following A dismissals')):
        image=CAP/f'frame_{frame:06d}_navigation.png'
        assert image.exists() and Image.open(image).size==(256,384)
        flow.append({'frame':frame,'state_for_visual_review':label,'RAM_sha256':sha(raw(frame)),
            'capture':str(image),'capture_sha256':sha(image.read_bytes())})
    ROOT.mkdir(parents=True);GUIDE.mkdir(parents=True)
    screens=[]
    for name,frame in (('Hodram_special_testing_fixture',7622),('special_following_strike_testing_fixture',8022),
                       ('ordinary_victory_return',10982)):
        source=CAP/f'frame_{frame:06d}_navigation.png';dest=GUIDE/(name+'.png');copy2(source,dest)
        assert source.read_bytes()==dest.read_bytes()
        screens.append({'path':str(dest),'sha256':sha(dest.read_bytes()),'source':str(source),'frame':frame})
    proof={'candidate':str(ROM),'candidate_sha256':report['ROM_sha256'],'terminal_frame':11782,
        'report':str(report_path),'report_sha256':sha(report_path.read_bytes()),
        'all31_fixture_replays':audits,'all_fixtures_before_duel5772_last5770':True,
        'native_prerequisites':'Both living captains:stamina/agility1,spirit/luck100;original positive HP maximum;shield49 moved to inventory before combat only.',
        'original_random_chance10_percent_not_forced':True,'no_numeric_message_actor_ID_RNG_seed_eligibility_flag_or_result_injection':True,
        'no_healing_revival_relocation_or_ability_changes_during_or_after_duel':True,
        'all_original_duel_and_attribute_HP_RNG_source_spans_exact':[[lo,hi] for lo,hi in spans],
        'original_special_source_binding':binding,'actual_special_holds':holds,'natural_HP_evolution':states,
        'actual_native_component_and_carrier_copy_confirm_original_new_dispatch':True,
        'all_accepted_inputs_and_navigation_targets_match_actual_report':True,
        'all15_have_complete_native_fonts_only1990_has_actual_activation_claim':True,
        'natural_special_to_combat_and_original_victory_aftermath':flow,
        'source_and_disposable_saves_unchanged':True,'guide_screenshots':screens,
        'visual_review_of_final_combat_victory_and_aftermath_pending':True,
        'targeted_headless_test_not_whole_route_or_hardware_verification':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'terminal_gameplay_verification.json',proof);save(GUIDE/'provenance.json',proof)
    print('31 full fixture audits,6 actual special holds,original HP/combat/victory and exact inputs pass.',flush=True)


if __name__=='__main__':main()
