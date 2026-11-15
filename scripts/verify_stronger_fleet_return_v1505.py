"""Terminal40-byte fixture/input audit of original declaration,defeat and retreat."""
import struct
from pathlib import Path
from types import FunctionType
from scripts import verify_stronger_fleet_survey_v1476 as previous
from scripts.native_stronger_fleet_current_v1501 import apply_fixture,ROM
from scripts.verify_stronger_fleet_survey_v1476 import observe
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.battle_reaction_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/stronger_fleet_return_verified_v1505')
RUN=Path('work/analysis/stronger_fleet_anchor_v1502')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/stronger_fleet_anchor_v1502_1492')

def bound_read(path):
    if str(path).replace('\\','/')=='work/analysis/ship_loss_surrender_release_v1455/registered_release_verification.json':
        return read('work/analysis/battle_reaction_release_v1491/registered_release_verification.json')
    return read(path)

if __name__=='__main__':
    assert not ROOT.exists()
    fn=FunctionType(previous.audit.__code__,{**previous.__dict__,'read':bound_read,'ROM':ROM,'apply_fixture':apply_fixture},argdefs=previous.audit.__defaults__)
    proof,snapshots,arm=fn(RUN,CAP,9200,[])
    assert sha(Path('scripts/run_stronger_fleet_anchor_v1502.py').read_bytes())==read(RUN/'run_plan.json')['runner_sha256']
    rom=__import__('dk4tool.rom.nds',fromlist=['NdsImage']).NdsImage.open(ROM)
    entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
    observations=[observe(arm,snapshots[n]) for n in [5200,5360,5760,5860,6300,6500,6700,6900,8200,8400,8600,8800,9000,9200]]
    by_frame={r['frame']:r for r in observations}
    assert by_frame[6300]['mode']==[0,1,4] and by_frame[6700]['mode']==[0,1,4]
    assert by_frame[6700]['fleets'][0]['ships'][4]['Hull_Crew']==[21,8]
    assert by_frame[9200]['mode']==[0,0,0]
    assert [s['Hull_Crew'] for s in by_frame[9200]['fleets'][0]['ships']]==[[25,19],[25,11],[24,6],[21,8]]
    owner,wrapped=[struct.unpack_from('<I',arm,o)[0] for o in [0x552A0,0x54450]]
    reports=[]
    for frame,expected in [(8200,[1973]),(8250,[1973]),(8400,[2017]),(8450,[2017]),(8600,[2139]),(8650,[2139]),(8800,[2684,2687]),(8850,[2684,2687])]:
        raw=Path(snapshots[frame]['path']).read_bytes()
        body=raw[owner-0x02000000+0x2030:owner-0x02000000+0x2230].split(b'\0')[0]
        numbers=[e.message_id for e in entries if e.text==body];assert numbers==expected
        formatted=raw[wrapped-0x02000000:wrapped-0x02000000+512].split(b'\0')[0]
        reports.append({'frame':frame,'current_template_candidate_IDs':numbers,'template_hex':body.hex(),
            'formatted_hex':formatted.hex(),'formatted_lines':[s.decode('cp932') for s in formatted.split(b'\n')],
            'RAM_sha256':snapshots[frame]['sha256'],'PNG':str(CAP/f'frame_{frame:06}_navigation.png'),
            '2684_vs2687_not_disambiguated_from_identical_English_alone':len(numbers)>1})
    raw=Path(snapshots[4800]['path']).read_bytes();cpu,get=get_machine(arm,raw);root=get(0xCB1A8)
    duty,actors,captain=root+0x2090,get(0xCB184),get(0x7F244)
    rooms=[]
    for role in range(21):
        count=get(0x829C8,duty,role,0x02460000)
        if not count:continue
        ids=list(struct.unpack('<'+str(count)+'I',cpu.mem_read(0x02460000,count*4)))
        members=[]
        for identity in ids:
            actor=actors+0x19E4 if identity==captain else actors+4+32*identity
            assert get(0x7EE08,actor)==identity
            members.append({'existing_actor_ID':identity,'actor_object':actor,'voice':get(0x7E988,actor)})
        rooms.append({'original_room':role,'members':members})
    ROOT.mkdir(parents=True)
    proof.update(actual_native_observations=observations,actual_current_report_holds=reports,
        original_damage_handler_eligible_rooms=rooms,original_incident_flag2=get(0x82C4C,duty,2),
        original_battle_context4_and_normal_unknown_faction_declaration_confirmed=True,
        original_AI_duel_after_natural_escort_damage_not_forced=True,
        original_Y_Auto_duel_loss_and_normal_evacuate_flagship_defeat_transfer_and_return_to_sailing=True,
        four_surviving_ships_after_lost_Vestaros=True,
        actual_first_six_injury_reaction_fonts_and_new_ship_loss_surrender_families_not_claimed=True,
        retreat7_source_context_review_lead=[2683,2684,2685,2686,2687,2688,2689],
        no_new_original32_reaction_or16_sinking_or24_loss_surrender_completion_credit=True,
        producer_sha256=sha(Path(__file__).read_bytes()),completed_entries_added=0,full_goal_complete=False)
    save(ROOT/'actual_declaration_defeat_and_transfer_return.json',proof)
    print('9200-frame terminal declaration/duel/defeat/transfer return audited;all40-byte fixture,inputs,RAM,PNGs,saves pass. New retreat7 lead;no completion credit.')
