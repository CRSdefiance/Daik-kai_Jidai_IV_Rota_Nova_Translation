"""Verify both full current close-range text holds before any normal dismissal."""
import struct
from pathlib import Path
from types import FunctionType
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.search_reports_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.sighting_layout_v1069 import compiled
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/close_sighting_live_v1790')
NAV=Path('work/analysis/two_stage_navigation_v1788/selected_original_event_hold_ready.json')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/two_stage_sighting_v1787_1775_twoStageReady8')
ROM=Path('out/all_routes_combined_v1775_candidate.nds')
BASE=0x02000000

if __name__=='__main__':
    assert not ROOT.exists();nav=read(NAV)
    assert nav['native_loading_before_close_observed'] and nav['selection_frame']==5113 and nav['paused_frame']==5443
    assert sha(ROM.read_bytes())==nav['candidate_sha256']
    image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    entries=current_entries(common,arm);doc=read('translations/sighting_editorial_manuscript_v9.json')
    manuscript={r['message_id']:r for r in doc['records']}
    assert all(entries[n].text==compiled(manuscript[n])for n in range(614,629))
    font=read(doc['native_font_proof']);case=next(r for r in font['cases']if r['message_ID']==614
        and r['bearing']['hex']==b'vicinity'.hex()and r['faction_hex']==b'Centurione Co.'.hex())
    class CurrentFont:
        @staticmethod
        def open(path):
            assert str(path)=='out/all_routes_combined_v255_candidate.nds'
            return image
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    checks=[];pictures=[]
    for hold in nav['holds']:
        frame=hold['frame'];raw=(CAP/f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
        assert len(raw)==0x400000 and sha(raw)==hold['RAM_sha256']
        cpu,get=get_machine(arm,raw);root=get(0xCB1A8);actors=get(0xCB184)
        actor=get(0x82478,root+0x2090,1);assert actor==18 and get(0x7F244)==get(0x2E58C)==1
        assert get(0x53F4C,actors+4+actor*32,0x02118560)==614
        owner,wrapped=[struct.unpack_from('<I',arm,k)[0]for k in (0x552A0,0x54450)]
        assert cstring(raw,owner+0x2030)==entries[614].text==compiled(manuscript[614])
        value=cstring(raw,wrapped);assert value.hex()==case['formatted_hex']
        provider=get(0x6567C,0,0);assert cstring(raw,provider)==b'vicinity'
        company=get(0xCB160)+4+8*76;vtable=struct.unpack('<I',cpu.mem_read(company,4))[0]
        name=get(struct.unpack('<I',cpu.mem_read(vtable+8,4))[0]-BASE,company)
        assert cstring(raw,name)==b'Centurione Co.'
        pixels=raster(arm,value,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
        assert pixels==independent_font(arm,image.read_file('/GRP/KANJI.FNT'),case['lines'])
        assert sha(bytes(pixels))==case['complete_native_font_plane_sha256']
        photo=Path(hold['capture']);assert sha(photo.read_bytes())==hold['capture_sha256']
        picture=Image.open(photo).convert('RGB')
        expected={(16+x,296+y)for y in range(64)for x in range(228)if pixels[y*228+x]}
        actual={(x,y)for y in range(294,366)for x in range(16,244)if picture.getpixel((x,y))==(0,8,0)}
        assert expected==actual,(frame,len(expected-actual),len(actual-expected))
        block=IlnkContainer.parse(common).blocks[entries[614].block];assert raw.count(block)==1
        assert bytes(cpu.mem_read(BASE,0x400000))==raw
        checks.append({'frame':frame,'message_ID':614,'source_role1_fallback_actor_ID':actor,
            'lines':case['lines'],'actual_bearing_argument':'vicinity','actual_faction_argument':'Centurione Co.',
            'whole228x64_native_independent_actual_ink_and_blank_plane_equal':True,
            'complete_leading_trailing_letters_left_origins_bounds_and_page_verified':True,
            'unique_complete_resident_native_block_exact':True,'capture':str(photo),'capture_sha256':sha(photo.read_bytes()),'RAM_sha256':sha(raw)})
        pictures.append(picture)
    assert len(checks)==2
    for crop in ((16,294,244,360),(0,194,100,291)):
        assert pictures[0].crop(crop).tobytes()==pictures[1].crop(crop).tobytes()
    ROOT.mkdir(parents=True)
    save(ROOT/'two_complete_close_range_holds_before_dismissal.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'holds':checks,'all15_current_templates_match_reviewed_manuscript_v9':True,
        'original_native_role_voice_bearing_faction_and_full_current_font_verified':True,
        'actual_full_screenshot_visually_viewed':True,'two_stage_native_loading_before_close_observed':True,
        'normal_dismissal_terminal_fixture_and_input_audit_still_pending':True,
        'emulator_left_paused_at5443_not_terminal':True,'navigation':str(NAV),'navigation_sha256':sha(NAV.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Actual close-range614:two complete native/independent/RGB holds pass;native Charles role1,full faction,vicinity,first/last letters andbounds verified. Normal dismissal andterminal audit pending.',flush=True)
