"""Actual compass622,its preserved covering-fire successor,and normal battle entry."""
from pathlib import Path
from types import FunctionType
import struct
from PIL import Image
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.sighting_grammar_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from scripts.native_sighting_context_v1109 import apply_fixture
from scripts.sighting_layout_v1069 import compiled
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sighting_incoming_actual_v1109')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/sighting_incoming_v1109_1105_compassAttack8')
ROM=Path('out/all_routes_combined_v1105_candidate.nds')
BASE=0x02000000


def main():
    assert not ROOT.exists()
    report_path=CAP/'capture_report.json';report=read(report_path)
    assert report['frames']==5710 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['ROM_sha256']==sha(ROM.read_bytes())
    assert read('work/analysis/sighting_incoming_v1109_compassAttack8/terminal_preservation.json')['source_and_disposable_donors_unchanged']
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    raw={}
    for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        body=Path(r['path']).read_bytes();assert len(body)==r['bytes']==0x400000 and sha(body)==r['sha256']
        if r['frame'] in raw:assert raw[r['frame']]==body
        raw[r['frame']]=body
    fixtures=report['synthetic_battle_recovery_proximity_fixtures'];assert len(fixtures)==1 and fixtures[0]['frame']==5100
    r=fixtures[0];after,p=apply_fixture(arm,raw[5100],{'sighting_context':'compassAttack8'})
    assert r=={**p,'frame':5100} and sha(after)==r['after_RAM_sha256'] and len(r['owned_bytes'])==19
    doc=read('translations/sighting_editorial_manuscript_v9.json');rows={r['message_id']:r for r in doc['records']}
    font=read(doc['native_font_proof']);old_font=read('work/analysis/reinforcement_sniping_v1031/native_font_proof.json')
    entries=current_entries(common,arm)
    class CurrentFont:
        @staticmethod
        def open(path):
            assert str(path)=='out/all_routes_combined_v255_candidate.nds'
            return rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    holds=[]
    for frame,n in ((5310,622),(5410,622),(5510,1917),(5610,1917)):
        cpu,get=get_machine(arm,raw[frame]);root=get(0xCB1A8);actors=get(0xCB184)
        actor=get(0x82478,root+0x2090,1);assert actor==18 and get(0x7F244)==get(0x2E58C)==1
        table=0x02118540 if n==622 else 0x021173C0
        assert get(0x53F4C,actors+4+actor*32,table)==n
        owner,wrapped=[struct.unpack_from('<I',arm,k)[0] for k in (0x552A0,0x54450)]
        value=cstring(raw[frame],wrapped)
        if n==622:
            assert cstring(raw[frame],owner+0x2030)==compiled(rows[n])==entries[n].text
            company=get(0xCB160)+4+8*76;vt=struct.unpack('<I',cpu.mem_read(company,4))[0]
            name=get(struct.unpack('<I',cpu.mem_read(vt+8,4))[0]-BASE,company)
            argument=bytes(cpu.mem_read(name,128)).split(b'\0')[0];assert argument==b'Centurione Co.'
            cases=[r for r in font['cases'] if r['message_ID']==n and r['bearing']['hex']==b'SE'.hex() and r['faction_hex']==argument.hex()]
            assert len(cases)==1;case=cases[0]
        else:
            assert cstring(raw[frame],owner+0x2030)==entries[n].text
            case=next(r for r in old_font['cases'] if r['message_ID']==n and r['argument_case']['hex']==b'Manuel'.hex())
        assert value.hex()==case['formatted_hex']
        pixels=raster(arm,value,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
        assert pixels==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),case['lines'])
        if n==622:assert sha(bytes(pixels))==case['complete_native_font_plane_sha256']
        image_path=CAP/f'frame_{frame:06d}_navigation.png';image=Image.open(image_path).convert('RGB')
        expected={(16+x,296+y) for y in range(64) for x in range(228) if pixels[y*228+x]}
        actual={(x,y) for y in range(294,366) for x in range(16,244) if image.getpixel((x,y))==(0,8,0)}
        assert expected==actual,(frame,len(expected-actual),len(actual-expected))
        block=IlnkContainer.parse(common).blocks[entries[n].block];assert raw[frame].count(block)==1
        holds.append({'frame':frame,'message_ID':n,'source_role1_fallback_actor_ID':actor,'source_table':table,
            'lines':case['lines'],'whole228x64_native_font_and_blank_paper_equal_actual_RGB':True,
            'complete_leading_trailing_letters_uniform_margins_and_bounds':True,'unique_complete_resident_native_block_exact':True,
            'capture':str(image_path),'capture_sha256':sha(image_path.read_bytes()),'RAM_sha256':sha(raw[frame])})
    for a,b in ((5310,5410),(5510,5610)):
        x,y=[Image.open(CAP/f'frame_{f:06d}_navigation.png').convert('RGB') for f in (a,b)]
        assert x.crop((16,294,244,360)).tobytes()==y.crop((16,294,244,360)).tobytes()
        assert x.crop((0,194,85,291)).tobytes()==y.crop((0,194,85,291)).tobytes()
    cpu,get=get_machine(arm,raw[5710]);root=get(0xCB1A8)
    assert list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)))==[0,1,8]
    groups=list(cpu.mem_read(root+0x2080,16))
    by_id={groups[k]:groups[k+1] for k in range(0,16,4) if groups[k]!=64}
    assert by_id=={1:0,57:1,8:2}
    assert groups[0:2]==[1,0]
    for fleet,company in ((1,2),(57,2),(8,8)):
        assert get(0x35320,root+4+fleet*132)==company
    # Original77DA4 sets the enemy's selected group+1 to2; original
    # support discovery changes Manuel's existing world slot to1.
    # The source indexes by selected group record, not by fleet order.
    control_cpu,control=get_machine(arm,raw[5310])
    control_root=control(0xCB1A8)
    control_groups=list(control_cpu.mem_read(control_root+0x2080,16))
    before_roles={control_groups[k]:control_groups[k+1] for k in range(0,16,4) if control_groups[k]!=64}
    assert before_roles=={1:0,57:5,8:2}
    assert [groups[k] for k in range(0,16,4)]==[control_groups[k] for k in range(0,16,4)]
    ROOT.mkdir(parents=True)
    save(ROOT/'actual_compass_and_covering_fire_verification.json',{'candidate':str(ROM),'candidate_sha256':report['ROM_sha256'],
        'terminal_report':str(report_path),'terminal_report_sha256':sha(report_path.read_bytes()),'terminal_frame':5710,
        'one_exact19_byte_location_and_original_hostility_attack_order_precondition_replay':True,'complete_actual_holds':holds,
        'normal_sighting_A_dismissal_to_original_covering_fire_then_normal_A_to_sea':True,
        'original_pending_battle_setup_and_identity_bound_roles_verified':True,
        'visually_observed_sea_return_not_complete_battle_playthrough':True,
        'prior_verifier_rejected_fixed_slot_order_preserved':'scripts/verify_sighting_compass_v1094.py',
        'original_battle_context':[0,1,8],'original_loaded_fleet_groups':groups,'source_and_disposable_saves_unchanged':True,
        'no_numeric_message_or_result_injection':True,'close_range_incoming_attack_and_Armed_Latina_UI_still_pending':True,
        'no_new_editorial_completion_credit':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Actual622 incoming attack and preserved1917 support:four complete font/RGB holds,one exact19-byte fixture and normal sea return pass. Remaining sighting/label gates stay open.',flush=True)


if __name__=='__main__':main()
