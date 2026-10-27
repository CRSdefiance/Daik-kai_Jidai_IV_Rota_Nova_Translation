"""Verify the completed staffing/firing pilot; it did not reach the contact shot roll."""
import struct
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_ranged_staffing_v1050b import apply_fixture
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/reinforcement_sniping_v1055')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/reinforcement_sniping_v1051_1034_regional')
ROM=Path('out/all_routes_combined_v1034_candidate.nds')
BASE=0x02000000


def main():
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    report=read(CAP/'capture_report.json');rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin')
    assert report['frames']==8600 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['ROM_sha256']==sha(ROM.read_bytes())
    assert read('work/analysis/reinforcement_sniping_v1051/terminal_preservation.json')['source_and_disposable_donors_unchanged']
    raw={}
    for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        body=Path(r['path']).read_bytes();assert len(body)==r['bytes']==0x400000 and sha(body)==r['sha256']
        if r['frame'] in raw:assert raw[r['frame']]==body
        raw[r['frame']]=body
    fixtures=report['synthetic_battle_recovery_proximity_fixtures'];replays=[]
    seed,flag=[struct.unpack_from('<I',arm,n)[0] for n in (0xD9858,0x51A20)]
    for i,r in enumerate(fixtures):
        after,p=apply_fixture(arm,raw[r['frame']],{'reinforcement_context':r['context']})
        assert r=={**p,'frame':r['frame']}
        for at in (seed,flag):assert raw[r['frame']][at-BASE:at-BASE+4]==after[at-BASE:at-BASE+4]
        replays.append({'frame':r['frame'],'context':r['context'],'owned_byte_count':len(r['owned_bytes']),
            'actual_changed_bytes':len(r['changes']),'entire4MiB_delta_and_receipt_replayed':True,
            'RNG_seed_and_initialization_flag_unchanged':True})
        if (i+1)%10==0:print(i+1,'exact original ranged-pilot fixture replays',flush=True)
    assert len(fixtures)==51
    font=read('work/analysis/reinforcement_sniping_v1031/native_font_proof.json')
    case=next(c for c in font['cases'] if c['message_ID']==1918 and c['argument_case']['hex']==b'Manuel'.hex())
    plane=Image.open(case['preview']).convert('L');holds=[]
    for frame in (6010,6110):
        image=Image.open(CAP/f'frame_{frame:06d}_navigation.png').convert('RGB')
        wrapped=struct.unpack_from('<I',arm,0x54450)[0]
        assert cstring(raw[frame],wrapped).hex()==case['formatted_hex']
        expected={(16+x,296+y) for y in range(64) for x in range(228) if plane.getpixel((x,y))==0}
        actual={(x,y) for y in range(294,366) for x in range(16,244) if image.getpixel((x,y))==(0,8,0)}
        assert expected==actual
        cpu,get=get_machine(arm,raw[frame]);root=get(0xCB1A8);actor=get(0x82478,root+0x2090,1)
        assert actor==16 and get(0x53F4C,get(0xCB184)+4+actor*32,0x021173C0)==1918
        holds.append({'frame':frame,'message_ID':1918,'actor_ID':16,'lines':case['lines'],
            'complete_three_line_native_font_and_blank_paper_matches_actual_RGB':True})
    states=[]
    for frame in (6130,7680,8550,8600):
        cpu,get=get_machine(arm,raw[frame]);root=get(0xCB1A8);own=get(0x36C70,root+4+132+12)
        enemy=get(0x36C70,root+4+8*132+12);model=get(0xAB158,own)
        states.append({'frame':frame,'own_and_enemy_Hull_Crew':[[get(0x5543C,m),get(0x55444,m)] for m in (own,enemy)],
            'native_Lookout_Aim':get(0x8235C,root+0x2090,7,6,0),
            'original_provision_halfwords_3E_40':list(struct.unpack('<2H',cpu.mem_read(model+0x3E,4)))})
    assert states[0]['own_and_enemy_Hull_Crew']==[[60,124],[60,163]]
    assert states[-1]['own_and_enemy_Hull_Crew'][1]==[52,153]
    assert states[-1]['original_provision_halfwords_3E_40']==[0,0]
    save(ROOT/'ranged_pilot_verification.json',{'candidate_sha256':report['ROM_sha256'],
        'terminal_report':str(CAP/'capture_report.json'),'terminal_report_sha256':sha((CAP/'capture_report.json').read_bytes()),
        'complete_fixture_replays':replays,'actual_three_line_covering_fire_holds':holds,'original_combat_states':states,
        'original_damage_observed_enemy_stats_never_restored_in_this_pilot':True,
        'source_context_correction':'Successful shot is checked in original contact/boarding handler737C8 at73B18,not from open-water firing alone. This pilot proves staffing,firing and actual support text only;it receives no shot-event credit.',
        'inherited_receipt_wording_qualification':'Some parent blanket noncoordinate-record flags predate explicit Luck/assignment/staffing fields. Exact declared owned fields and complete4MiB deltas are authoritative. Contact successor1057b qualifies those inherited flags;no game-byte difference was hidden.',
        'no_successful_shot_or_completion_credit':True,'original_and_disposable_donors_unchanged':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('51 exact fixture/RNG-preservation replays and two full three-line actual holds pass;no shot credit.',flush=True)


if __name__=='__main__':main()
