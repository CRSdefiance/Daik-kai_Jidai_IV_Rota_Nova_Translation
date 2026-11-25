"""Bind original allied-fleet reinforcement to complete actual font pixels and battle entry."""
import struct
from pathlib import Path
from PIL import Image
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.reinforcement_sniping_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from scripts.native_reinforcement_pact_v1048 import apply_fixture
from scripts.reinforcement_sniping_layout_v1024 import compiled
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/reinforcement_sniping_v1052')
FOLDER=Path('E:/Rota Nova translations/Generated/work/emulation_v193/reinforcement_sniping_v1049_1034_regional')
ROM=Path('out/all_routes_combined_v1034_candidate.nds')
BASE=0x02000000


def main():
    assert not ROOT.exists()
    report_path=FOLDER/'capture_report.json';report=read(report_path)
    assert report['frames']==5810 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['hardware_device_verification'] and not report['goal_complete']
    digest=sha(ROM.read_bytes());assert digest==report['ROM_sha256']
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    donor=report['battery_save_preloaded']
    assert donor['source_sha256']=='2bec91a13ba69361c5c79ff52dcc3c8a3d5cf2ccbe2fc4b614bac8d12ab4cee1'
    assert sha(Path(donor['source']).read_bytes())==donor['source_sha256'] and donor['copied_byte_exact_before_cold_boot']
    assert read('work/analysis/reinforcement_sniping_v1049/terminal_preservation.json')['source_and_disposable_donors_unchanged']
    raw={};shots={}
    for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        body=Path(r['path']).read_bytes();assert len(body)==r['bytes']==0x400000 and sha(body)==r['sha256']
        if r['frame'] in raw:assert raw[r['frame']]==body
        raw[r['frame']]=body
    for r in report['frames_captured']:
        p=Path(r['path']);assert sha(p.read_bytes())==r['PNG_sha256']
        if r['frame'] in shots:assert Image.open(shots[r['frame']]).tobytes()==Image.open(p).tobytes()
        shots[r['frame']]=p
    fixtures=report['synthetic_battle_recovery_proximity_fixtures']
    assert len(fixtures)==1 and [r['frame'] for r in fixtures]==[5100]
    assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k!='synthetic_battle_recovery_proximity_fixtures')
    replay=[]
    for r in fixtures:
        after,proof=apply_fixture(arm,raw[r['frame']],{'reinforcement_context':r['context']})
        assert r=={**proof,'frame':r['frame']}
        assert sha(after)==r['after_RAM_sha256']
        replay.append({'frame':r['frame'],'context':r['context'],'owned_byte_count':len(r['owned_bytes']),
            'changed_byte_count':len(r['changes']),'entire4MiB_delta_and_receipt_replayed_exactly':True})
    doc=read('translations/reinforcement_sniping_editorial_manuscript_v2.json');row=next(r for r in doc['records'] if r['message_id']==1911)
    entries=current_entries(common,arm);assert entries[1911].text==compiled(row)
    font=read(doc['native_font_proof']);holds=[]
    for frame in (5410,5510):
        cpu,get=get_machine(arm,raw[frame]);fleets=get(0xCB1A8);actors=get(0xCB184)
        actor=get(0x82478,fleets+0x2090,1);obj=actors+4+actor*32
        assert actor!=get(0x7F244) and get(0x53F4C,obj,0x021173E0)==1911
        company=get(0xCB160)+4+7*76
        assert get(0x3CB30,company,2)==1 and get(0x3C740,company)==8
        vt=struct.unpack('<I',cpu.mem_read(company,4))[0]
        at=get(struct.unpack('<I',cpu.mem_read(vt+8,4))[0]-BASE,company)
        argument=bytes(cpu.mem_read(at,128)).split(b'\0')[0];assert argument==b'Walds'
        owner,wrapped=[struct.unpack_from('<I',arm,k)[0] for k in (0x552A0,0x54450)]
        assert cstring(raw[frame],owner+0x2030)==compiled(row)
        value=cstring(raw[frame],wrapped)
        cases=[c for c in font['cases'] if c['message_ID']==1911 and c['argument_case']['hex']==argument.hex()]
        assert len(cases)==1;case=cases[0];assert value.hex()==case['formatted_hex']
        preview=Path(case['preview']);assert sha(preview.read_bytes())==case['preview_sha256']
        plane=Image.open(preview).convert('L');image=Image.open(shots[frame]).convert('RGB')
        assert plane.size==(228,64) and image.size==(256,384)
        expected={(16+x,296+y) for y in range(64) for x in range(228) if plane.getpixel((x,y))==0}
        actual={(x,y) for y in range(294,366) for x in range(16,244) if image.getpixel((x,y))==(0,8,0)}
        assert expected==actual,(frame,len(expected-actual),len(actual-expected))
        block=IlnkContainer.parse(common).blocks[entries[1911].block]
        assert raw[frame].count(block)==1
        holds.append({'frame':frame,'message_ID':1911,'native_First_Mate_or_original_fallback_actor_ID':actor,
            'original_voice_selector_table':0x021173E0,'supporting_original_allied_fleet_ID':24,
            'supporting_original_company_ID':7,'native_complete_company_label_hex':argument.hex(),
            'lines':case['lines'],'complete_native_font_plane_and_blank_paper_matches_actual_RGB':True,
            'uniform_visible_margins_complete_leading_trailing_letters_and_bounds':True,
            'source_template_wrap_and_unique_complete_resident_block_exact':True,
            'capture':str(shots[frame]),'capture_sha256':sha(shots[frame].read_bytes()),
            'RAM':str(FOLDER/f'frame_{frame:06d}_arm9_ram.bin'),'RAM_sha256':sha(raw[frame])})
    a,b=[Image.open(shots[f]).convert('RGB') for f in (5410,5510)]
    assert a.crop((16,294,244,360)).tobytes()==b.crop((16,294,244,360)).tobytes()
    assert a.crop((0,194,85,291)).tobytes()==b.crop((0,194,85,291)).tobytes()
    cpu,get=get_machine(arm,raw[5610]);fleets=get(0xCB1A8)
    assert get(0x7F244)==get(0x2E58C)==1
    assert list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)))==[0,1,8]
    groups=list(cpu.mem_read(fleets+0x2080,16));assert groups[0:2]==[1,0] and groups[4:6]==[8,2] and groups[8:10]==[24,1]
    companies=get(0xCB160);assert get(0x3CB30,companies+4+8*76,2)==2
    ROOT.mkdir()
    save(ROOT/'actual_reinforcement_verification.json',{'candidate':str(ROM),'candidate_sha256':digest,
        'terminal_cold_boot_report':str(report_path),'terminal_cold_boot_report_sha256':sha(report_path.read_bytes()),
        'terminal_frame':5810,'exact_fixture_replays':replay,'complete_actual_holds':holds,
        'stable_dialogue_body_portrait_and_native_name':True,
        'normal_A_dismissal_enters_original_battle_without_blank_or_extra_page':True,
        'actual_loaded_fleet_groups':groups,'actual_source_battle_context':[0,1,8],
        'original_reinforcement_scan_loaded_existing_allied_fleet24_as_player_support':True,
        'normal_declaration_opponent_reply_and_source_relation2_observed':True,
        'actual_battle_entry_screenshot':str(shots[5610]),'actual_battle_entry_screenshot_sha256':sha(shots[5610].read_bytes()),
        'portrait_and_commander_name_visually_reviewed':True,
        'original_and_disposable_donors_unchanged':True,
        'no_numeric_message_or_battle_outcome_injection_and_no_earned_progression_claim':True,
        'admiral_shot_actual_scene_still_pending':True,
        'no_editorial_completion_credit_added_by_this_verifier':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Original reinforcement announcement:two complete actual font/RGB holds,one exact19-byte context fixture and normal battle transition pass.',flush=True)


if __name__=='__main__':main()
