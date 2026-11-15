"""Bind the original defeat notice to complete native fonts and visible pixels."""
from pathlib import Path
from types import FunctionType
import struct
from PIL import Image
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.escape_direct_entries import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/escape_actual_holds_v1193')
ROM=Path('out/all_routes_combined_v1189_candidate.nds')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/escape_direct_v1190_1189')
BASE=0x02000000


def main():
    assert not ROOT.exists()
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    entries=current_entries(common,arm)
    ref=read('work/analysis/escape_direct_fonts_v1185/native_direct_escape_fonts.json')
    case=next(r for r in ref['cases'] if r['message_ID']==1973)
    assert ref['ARM9_sha256']==sha(arm)
    class CurrentFont:
        @staticmethod
        def open(path):return rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    holds=[]
    for frame in (6912,6922):
        ram_path=CAP/f'frame_{frame:06d}_arm9_ram.bin';image_path=CAP/f'frame_{frame:06d}_navigation.png'
        raw=ram_path.read_bytes();assert len(raw)==0x400000
        cpu,get=get_machine(arm,raw);actors=get(0xCB184);root=get(0xCB1A8)
        actor=get(0x82478,root+0x2090,1);assert actor==18
        assert get(0x7F244)==get(0x2E58C)==1
        assert get(0x53F4C,actors+4+actor*32,0x02117620)==1973
        hp=[get(0x7E19C,a) for a in (actors+0x19E4,actors+4+32*32)]
        assert hp==[0,45]
        owner,wrapped=[struct.unpack_from('<I',arm,off)[0] for off in (0x552A0,0x54450)]
        text=lambda p:raw[p-BASE:p-BASE+256].split(b'\0')[0]
        assert text(owner+0x2030)==entries[1973].text
        value=text(wrapped);assert value.hex()==case['formatted_hex']
        pixels=raster(arm,value,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
        assert pixels==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),case['lines'])
        assert sha(pixels)==case['native_font_sha256']
        image=Image.open(image_path).convert('RGB')
        expected={(16+x,296+y) for y in range(64) for x in range(228) if pixels[y*228+x]}
        actual={(x,y) for y in range(294,366) for x in range(16,244) if image.getpixel((x,y))==(0,8,0)}
        assert expected==actual,(frame,len(expected-actual),len(actual-expected))
        block=IlnkContainer.parse(common).blocks[entries[1973].block];assert raw.count(block)==1
        holds.append({'frame':frame,'message_ID':1973,'first_mate_actor_ID':actor,'native_voice_table':0x02117620,
            'own_enemy_captain_HP':hp,'formatted_hex':value.hex(),'lines':case['lines'],
            'complete228x64_native_font_plane_sha256':sha(pixels),
            'complete_native_font_and_blank_paper_RGB_exact':True,
            'complete_words_first_last_letters_uniform_margins_and_bounds':True,
            'source_bound_x16_y296_geometry_from_existing_portrait_consumer':True,
            'unique_whole_resident_COMMON_block_exact':True,
            'RAM':str(ram_path),'RAM_sha256':sha(raw),'capture':str(image_path),'capture_sha256':sha(image_path.read_bytes())})
    a,b=[Image.open(CAP/f'frame_{f:06d}_navigation.png').convert('RGB') for f in (6912,6922)]
    assert a.crop((16,294,244,366)).tobytes()==b.crop((16,294,244,366)).tobytes()
    ROOT.mkdir(parents=True)
    save(ROOT/'actual_notice_holds.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),'actual_message_ID':1973,'complete_actual_holds':holds,
        'both_portraits_and_two_complete_text_rows_visually_reviewed':True,
        'all13_have_native_matrix_but_only1973_has_actual_activation_claim':True,
        'terminal_fixture_preservation_and_normal_dismissal_still_require_separate_verification':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'no_completion_credit':True,'full_goal_complete':False})
    print('Actual1973:two complete native font/RGB holds pass; Everyone stays intact.',flush=True)


if __name__=='__main__':main()
