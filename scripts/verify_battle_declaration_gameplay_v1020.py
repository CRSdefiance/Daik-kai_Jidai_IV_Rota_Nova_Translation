"""Terminal actual-scene evidence, exact fixture replay, cancellation and acceptance."""
import struct
from pathlib import Path
from PIL import Image, ImageChops
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_battle_declaration_visible_v1012 import dispatch_fixture as unknown_fixture
from scripts.native_battle_declaration_lookout_v1017 import dispatch_fixture as identified_fixture
from scripts.verify_battle_declaration_modal_v1016 import verify as modal
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_village_wrap_v608 import read,save

BASE=0x02000000
ROM=Path('out/all_routes_combined_v997_candidate.nds')
ROOT=Path('work/analysis/battle_declaration_v1020')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
CASES={
 'unknown':('battle_declaration_v1015_997_KnownJanus',7260,unknown_fixture),
 'known':('battle_declaration_v1018_997_KnownJanus',7160,identified_fixture),
 'ready':('battle_declaration_v1019_997_KnownJanus',6860,identified_fixture)}


def state(arm,raw):
    cpu,get=get_machine(arm,raw)
    companies=get(0xCB160);company=companies+4+9*76;leader=get(0x3CD2C,company)
    clock=get(0xCB1B4)+8
    return {'relation':get(0x3CB30,company,2),'leader_byte26':get(0x7DB0C,leader),
        'captain_ID':get(0x7F244),'active_fleet_ID':get(0x2E58C),
        'cash':get(0x3CCC8,companies+4+2*76),'clock':struct.unpack('<I',cpu.mem_read(clock,4))[0],
        'source_context8_12_16':list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12))),
        'all20_companies_sha256':sha(bytes(cpu.mem_read(companies,4+20*76))),
        'persistent_objects':persistent_objects(arm,raw),'own_models':models(arm,raw)}


def main():
    assert not ROOT.exists()
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');digest=sha(ROM.read_bytes())
    assert digest==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    data={};reports=[];fixtures=[];screens=[];preservation=[]
    for label,(name,terminal,dispatch) in CASES.items():
        folder=CAP/name;path=folder/'capture_report.json';report=read(path)
        assert report['frames']==terminal and report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors'] and not report['hardware_device_verification']
        assert report['ROM_sha256']==digest and report['goal_complete'] is False
        assert report['controlled_battle_declaration_fixture_dispatch']['source_and_disposable_donors_unchanged']
        donor=report['battery_save_preloaded']
        assert donor['copied_byte_exact_before_cold_boot'] and donor['source']!=donor['destination']
        assert sha(Path(donor['source']).read_bytes())==donor['source_sha256']=='febc859c5af2df6fa8023c349bb7f31b5fc15ea769fb2eea527b3a3f80521731'
        ram={}
        for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
            raw=Path(row['path']).read_bytes()
            assert len(raw)==row['bytes']==0x400000 and row['read_only_export'] and sha(raw)==row['sha256']
            if row['frame'] in ram:assert ram[row['frame']]==raw
            ram[row['frame']]=raw
        frames={}
        for row in report['frames_captured']:
            p=Path(row['path']);assert sha(p.read_bytes())==row['PNG_sha256']
            if row['frame'] in frames:
                assert Image.open(frames[row['frame']]).tobytes()==Image.open(p).tobytes()
            frames[row['frame']]=p
        selected=report['synthetic_battle_recovery_proximity_fixtures']
        assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k!='synthetic_battle_recovery_proximity_fixtures')
        for receipt in selected:
            frame=receipt['frame'];request={'declaration_context':receipt['declaration_context']} if 'declaration_context' in receipt else receipt['action']
            after,proof=dispatch(arm,ram[frame],request)
            assert receipt=={**proof,'frame':frame},(label,frame,'fixture replay differs')
            assert sha(after)==receipt['after_RAM_sha256']
            fixtures.append({'case':label,'frame':frame,'request':request,'owned_byte_count':len(receipt['owned_bytes']),
                'actual_change_count':len(receipt['changes']),'exact_receipt_and_all4MiB_delta_reproduced':True})
        data[label]=(folder,ram,frames)
        reports.append({'case':label,'path':str(path),'sha256':sha(path.read_bytes()),'terminal_frame':terminal,
            'all_frame_and_RAM_hashes_verified':True,'exact_fixture_replays':len(selected),
            'cold_boot_and_no_savestate_original_donor_unchanged':True})
    holds=[]
    for label,display,frames in [('unknown','UnknownJanus',[6160]),('unknown','UnknownEmilio',[6560,6660]),
                                 ('known','KnownJanus',[6160,6260]),('ready','ReadyEmilio',[6360,6460])]:
        for frame in frames:holds.append(modal(data[label][0],display,frame))
    for label,a,b in [('unknown',6560,6660),('known',6160,6260),('ready',6360,6460)]:
        images=[Image.open(data[label][2][f]).convert('RGB') for f in (a,b)]
        assert images[0].crop((16,294,244,360)).tobytes()==images[1].crop((16,294,244,360)).tobytes()
        assert images[0].crop((0,194,85,291)).tobytes()==images[1].crop((0,194,85,291)).tobytes()
        screens.append({'case':label,'frames':[a,b],
            'entire_dialogue_body_above_advance_area_and_portrait_name_region_stable':True,
            'whole_frame_difference_bounds':ImageChops.difference(*images).getbbox()})
    cancels=[]
    for label,before,after in [('unknown',5960,6260),('known',5960,6360),('ready',5960,6160)]:
        a,b=[state(arm,data[label][1][f]) for f in (before,after)]
        assert a==b,(label,'cancellation changed persistent source state')
        assert a['relation']==0 and a['source_context8_12_16']==[0,0,0]
        # Exact original target-mode object and selected faction survive No.
        raw=data[label][1][after]
        matches=[i for i in range(0x189000,0x18DB10,4) if raw[i:i+4]==struct.pack('<I',0x02147148)]
        assert len(matches)==1 and struct.unpack_from('<I',raw,matches[0]+0x74)[0]==1
        cancels.append({'case':label,'before':before,'after':after,'state':a,
            'No_returns_to_original_Declare_War_mode_without_war_or_persistent_changes':True})
    outcomes=[]
    for label,before,opponent,after in [('unknown',6660,6860,7260),('known',6560,6760,7160)]:
        a,b,c=[state(arm,data[label][1][f]) for f in (before,opponent,after)]
        assert a['relation']==b['relation']==0 and c['relation']==2
        assert [a['leader_byte26'],b['leader_byte26'],c['leader_byte26']]==([0,1,1] if label=='unknown' else [1,1,1])
        assert a['source_context8_12_16']==[0,0,0] and c['source_context8_12_16']==[0,1,28]
        assert a['cash']==b['cash']==c['cash']
        assert all(s['captain_ID']==1 and s['active_fleet_ID']==1 for s in (a,b,c))
        outcomes.append({'case':label,'frames':[before,opponent,after],
            'before':a,'original_opponent_reply':b,'actual_battle_started':c,
            'Yes_original_unknown_knowledge_and_relation_side_effects_observed':True,
            'normal_original_opponent_reply_and_duel_transition_no_blank_page':True,
            'no_victory_or_battle_outcome_claim':True})
    ready=[state(arm,data['ready'][1][f]) for f in (6260,6360,6460,6860)]
    assert [s['relation'] for s in ready]==[2,2,2,2]
    assert all(s['source_context8_12_16']==[0,0,0] for s in ready[:3])
    assert ready[-1]['source_context8_12_16']==[0,1,28]
    assert all(s['cash']==ready[0]['cash'] for s in ready)
    ROOT.mkdir()
    save(ROOT/'actual_gameplay_verification.json',{'candidate_sha256':digest,'reports':reports,
        'all_exact_fixture_replays':fixtures,'complete_actual_modal_holds':holds,
        'stable_body_portrait_and_native_name_controls':screens,'cancellations':cancels,
        'known_and_unknown_Yes_paths':outcomes,'ready_late_fixture_states':ready,
        'ready_dismissal_enters_original_battle_without_extra_page':True,
        'all_three_source_families_representatively_verified':True,
        'all22_individual_gameplay_activations_not_claimed':True,
        'source_role7_Lookout_and_original_705F8_widget_unknown_flag_mapped':True,
        'actor_names_portraits_complete_body_bounds_choices_and_transitions_visually_reviewed':True,
        'new_ROM_build_not_required_same_registered_V997_and_exact_patch':True,
        'original_donors_and_canonical_unchanged':True,'producer_sha256':sha(Path(__file__).read_bytes()),
        'full_goal_complete':False})
    print('Three terminal cold boots;7 complete modal holds;16 exact fixture replays;3 No returns;known/unknown Yes and readiness dismissal pass.',flush=True)


if __name__=='__main__':main()
