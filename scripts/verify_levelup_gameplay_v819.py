"""Actual Temple repair holds and separate forced six-stat display evidence."""

import struct
from pathlib import Path

from PIL import Image,ImageChops

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.levelup_format_runtime_v819 import ROOT
from scripts.verify_ceremony_families_gameplay_v815 import state,models,persistent_objects,tasks,calendar
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
DONOR='a71d476e3ed49c9c918ebd70367896256117e212edd96ce5f931b3df1dd68410'


def capture(name):
    folder=CAP/name;d=read(folder/'capture_report.json')
    assert d['cold_boot'] and not d['savestate_loaded'] and not d['callback_errors']
    assert d['core_DLL_sha256']=='42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert not d['goal_complete'] and not d['hardware_device_verification']
    assert sha(Path(d['ROM']).read_bytes())==d['ROM_sha256']
    donor=d['battery_save_preloaded'];assert donor['source']!=donor['destination']
    assert donor['source_sha256']==DONOR==sha(Path(donor['source']).read_bytes())
    assert donor['copied_byte_exact_before_cold_boot']
    frames={r['frame']:r for r in d['frames_captured']}
    for r in frames.values():assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']
    snapshots={r['frame']:r for r in d.get('read_only_capture_RAM_snapshots',[])}
    snapshots.update({r['frame']:r for r in d.get('read_only_pause_RAM_snapshots',[])})
    ram={f:Path(r['path']).read_bytes() for f,r in snapshots.items()}
    assert all(len(ram[f])==0x400000 and sha(ram[f])==r['sha256'] for f,r in snapshots.items())
    return d,frames,ram


def text(raw,at):return raw[at-0x02000000:at-0x02000000+512].split(b'\0')[0]


def glyphs(arm,kanji,picture,encoded,lines):
    plane=raster(arm,encoded,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=1000000)
    assert plane==independent_font(arm,kanji,lines)
    expected={(16+i%228,296+i//228) for i,p in enumerate(plane) if p==1}
    actual={(x,y) for y in range(294,366) for x in range(16,244) if picture.getpixel((x,y))==(0,8,0)}
    assert expected==actual,(len(expected-actual),len(actual-expected),lines)


def ordinary():
    old,of,oram=capture('ceremony_v809_temple_preparations')
    new,nf,nram=capture('levelup_v819_temple_research')
    assert new['frames']==10200
    assert new['scripted_input_schedule']==[r for r in old['scripted_input_schedule'] if r['start']<10000]
    oldrom=NdsImage.open(old['ROM']);rom=NdsImage.open(new['ROM'])
    before=oldrom.read_file('/__arm9__.bin');arm=rom.read_file('/__arm9__.bin')
    wrapped=struct.unpack_from('<I',arm,0x54450)[0]
    holds=[];controls=[];states=[]
    for f in (3200,3400,*range(3800,10201,400)):
        a=Image.open(of[f]['path']).convert('RGB');b=Image.open(nf[f]['path']).convert('RGB')
        diff=ImageChops.difference(a,b)
        if f in (6600,7400):
            raw=text(nram[f],wrapped);lines=[r.strip().decode('cp932') for r in raw.split(b'\n')]
            assert len(lines)==(3 if f==6600 else 2)
            assert raw.startswith(b' ') and all(r.startswith(b'  ') for r in raw.split(b'\n')[1:])
            assert not raw.endswith(b'\n')
            glyphs(arm,rom.read_file('/GRP/KANJI.FNT'),b,raw,lines)
            diff.paste((0,0,0),(16,294,244,366));assert diff.getbbox() is None
            holds.append(dict(frame=f,lines=lines,wrapped_hex=raw.hex(),capture=nf[f],
                complete_native_independent_font_and_actual_dark_pixel_plane_exact=True,
                every_leading_trailing_letter_number_margin_and_blank_row_verified=True,
                every_pixel_outside_text_body_equal_previous_V809=True))
        else:
            assert diff.getbbox() is None,(f,diff.getbbox())
            controls.append(dict(frame=f,whole_two_screen_frame_equal_V809=True))
        for fn in (state,models,persistent_objects,tasks,calendar):assert fn(before,oram[f])==fn(arm,nram[f]),(f,fn.__name__)
        assert oram[f][0x168EB8:0x168EBC]==nram[f][0x168EB8:0x168EBC]
        states.append(dict(frame=f,calendar=calendar(arm,nram[f]),
            original_actor_town_goods_items_models_tasks_funds_calendar_and_PRNG_equal_V809=True))
    geometry,gf,gram=capture('levelup_v819_modal_geometry')
    assert Path(gf[6600]['path']).read_bytes()==Path(nf[6600]['path']).read_bytes() and gram[6600]==nram[6600]
    save(ROOT/'temple_gameplay_verification.json',dict(research_ROM=new['ROM'],sha256=new['ROM_sha256'],
        complete_stat_holds=holds,whole_screen_controls=controls,state_pairs=states,
        read_only_native_export_frame6600_leaves_entire4MiB_and_two_screen_capture_exact=True,
        original_donor_unchanged=True,normal_scene_and_original_return_no_extra_pages=True,
        synthetic_growth_not_used_in_this_run=True,saved_setup_isolated_access_not_earned=True,
        registered_integration_not_yet_created=True,full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('Actual Temple repair:2 complete font holds,17 whole-screen controls and19 state/PRNG pairs pass.',flush=True)


def six_stat_fixture():
    fixture=read(ROOT/'six_stat_display_fixture_provenance.json')
    report,frames,ram=capture('levelup_v819_six_stat_display_fixture')
    assert report['ROM_sha256']==fixture['ROM_sha256'] and report['frames']==10200
    rom=NdsImage.open(report['ROM']);arm=rom.read_file('/__arm9__.bin')
    production=(ROOT/'ARM9_RESEARCH_ONLY.bin').read_bytes()
    restored=bytearray(arm)
    for row in fixture['fixture_only_patches']:
        at=row['address']-0x02000000;before=bytes.fromhex(row['before_hex']);after=bytes.fromhex(row['after_hex'])
        assert arm[at:at+4]==after and production[at:at+4]==before
        restored[at:at+4]=before
    assert bytes(restored)==production
    wrapped=struct.unpack_from('<I',arm,0x54450)[0]
    names=['Stamina','Agility','Charm','Wits','Spirit','Luck']
    lines=[f'{name} increased by ３!' for name in names]
    full=b' '+b'\n  '.join(r.encode('cp932') for r in lines)
    holds=[]
    for first,second,next_header in ((6600,7000,7400),(7800,8200,8600)):
        for f,selected,prefix in ((first,lines[:4],b' '),(second,lines[4:],b'  ')):
            assert text(ram[f],wrapped)==full
            pic=Image.open(frames[f]['path']).convert('RGB')
            encoded=prefix+b'\n  '.join(r.encode('cp932') for r in selected)
            glyphs(arm,rom.read_file('/GRP/KANJI.FNT'),pic,encoded,selected)
            holds.append(dict(frame=f,page=1 if f==first else 2,lines=selected,
                actual_complete_font_and_blank_plane_matches=True,capture=frames[f],
                aligned_complete_first_and_final_letters_numbers_and_bounds=True))
        assert text(ram[first],wrapped)==text(ram[second],wrapped)
    # Charles' real next header immediately follows Hodram's second page;
    # the ordinary town menu immediately follows Charles' second page.
    assert b'Charles' in text(ram[7400],wrapped)
    normal,ordinary_frames,_=capture('levelup_v819_temple_research')
    assert ImageChops.difference(Image.open(frames[8600]['path']).convert('RGB'),
        Image.open(ordinary_frames[7800]['path']).convert('RGB')).getbbox() is None
    save(ROOT/'six_stat_actual_pagination.json',dict(research_fixture_ROM=report['ROM'],sha256=report['ROM_sha256'],
        fixture_provenance=str(ROOT/'six_stat_display_fixture_provenance.json'),
        fixture_only8_instruction_bytes_recover_exact_production_repair_ARM9=True,
        complete_actual_page_holds=holds,maximum_six_stat_rows_paginate_four_then_two=True,
        actual_A_input_advances_to_original_next_actor_and_then_town_without_blank_page=True,
        original_pager_name_number_and_font_pipeline_used=True,
        no_earned_six_stat_growth_or_unmodified_world_outcome_claim=True,
        production_repair_must_exclude_both_fixture_instructions=True,
        targeted_automated_emulator_evidence_not_hardware_or_full_route_verification=True,
        full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Six-stat display fixture:4 actual complete page holds; four-plus-two pagination, next actor and town return pass.',flush=True)


def main():
    ordinary()
    six_stat_fixture()


if __name__=='__main__':main()
