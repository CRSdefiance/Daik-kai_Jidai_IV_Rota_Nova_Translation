"""Both original corrected status paths:complete bytes,native glyphs,RGB and transitions."""
import inspect,struct
from pathlib import Path
from types import FunctionType
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.inspection_status_editorial import current_entries
from scripts import verify_sea_registration_pilot_v1552j as template
from scripts import native_inspection_status_lookout_fixture_v1581 as new_lookout
from scripts import native_inspection_status_no_lookout_fixture_v1581b as new_no_lookout
from scripts import native_sea_inspection_fixture_v1566 as old_lookout
from scripts import native_sea_registration_fixture_v1552g as old_no_lookout
from scripts.probe_inspection_status_fonts_v1574 import pipeline,literal_independent
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/inspection_status_actual_verified_v1583')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
BASE=0x02000000

def audit(label,module,terminal,lookout,version):
    source=inspect.getsource(template.audit)
    if lookout:
        source=source.replace('==46','==48').replace('46_owned','48_owned')
        source=source.replace('register_original_Monster_Fish','register_original_Monster_Fish_and_assign_lookout')
    digest=sha(module.ROM.read_bytes())
    source=source.replace('b8b256650bb426e99012be06fd060114da0fbf32f763b5c3434204dda8f50437',digest)
    env={**template.__dict__,'__file__':__file__,'ROM':module.ROM,'apply_fixture':module.apply_fixture}
    exec(compile(source,__file__,'exec'),env)
    run=Path('work/analysis')/label;cap=CAP/(label+'_'+str(version))
    receipt,shots,arm=env['audit'](run,cap,terminal)
    # The inherited auditor's old label is narrowed explicitly;these are test fixtures.
    receipt['fixture_scope']='Original registration and its natural RNG initialization,target cached location,and only for lookout path the two-byte move of existing Charles18 from station9 to3.'
    return receipt,shots,arm

if __name__=='__main__':
    assert not ROOT.exists()
    cases=[('inspection_status_lookout_v1582',new_lookout,6300,True,1578,'sea_inspection_final_v1567d',old_lookout,1563,306,[6040,6100]),
        ('inspection_status_no_lookout_v1582b',new_no_lookout,6850,False,1578,'sea_registration_live_v1552h',old_no_lookout,1542,307,[6600,6630])]
    records=[]
    for label,module,terminal,lookout,version,oldlabel,oldmodule,oldversion,number,expectedholds in cases:
        current,shots,arm=audit(label,module,terminal,lookout,version)
        old,oldshots,oldarm=audit(oldlabel,oldmodule,terminal,lookout,oldversion)
        report,oldreport=read(current['terminal_report']),read(old['terminal_report'])
        assert report['scripted_input_schedule']==oldreport['scripted_input_schedule']
        rom,oldrom=NdsImage.open(current['candidate']),NdsImage.open(old['candidate'])
        assert rom.read_file('/GRP/KANJI.FNT')==oldrom.read_file('/GRP/KANJI.FNT')
        common=rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm)
        font=read('work/analysis/inspection_status_fonts_v1574/native_font_proof.json')
        assert font['ARM9_sha256']==sha(arm) and font['COMMON_sha256']==sha(common)
        case=next(r for r in font['cases'] if r['message_ID']==number)
        class CurrentFont:
            @staticmethod
            def open(path):
                assert path=='out/all_routes_combined_v255_candidate.nds';return rom
        raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
        newframes={r['frame']:r for r in report['frames_captured']}
        owner,wrapped=[struct.unpack_from('<I',arm,p)[0]-BASE for p in [0x552A0,0x54894]]
        oldwrapped=struct.unpack_from('<I',oldarm,0x54894)[0]-BASE
        holds,controls=[],[]
        for row in oldreport['frames_captured']:
            frame=row['frame'];target=newframes[frame]
            with Image.open(row['path']) as oi,Image.open(target['path']) as ni:
                picture,oldpicture=ni.convert('RGB'),oi.convert('RGB')
                diff={(i%256,i//256) for i,(a,b) in enumerate(zip(picture.get_flattened_data(),oldpicture.get_flattened_data(),strict=True)) if a!=b}
                if not diff:controls.append({'frame':frame,'whole256x384_RGB_exact_to_reference':True,'reference_version':oldversion});continue
                raw=Path(shots[frame]['path']).read_bytes()
                value=raw[owner+0x2030:owner+0x2230].split(b'\0')[0]
                formatted=raw[wrapped:wrapped+512].split(b'\0')[0]
                assert value==entries[number].text and formatted.hex()==case['native_pipeline']['formatted_hex']
                native=pipeline(arm,common,raw,{'patches':[]},number)
                assert native['loaded_template_hex']==native['formatted_hex']==value.hex()
                pixels=raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
                assert pixels==literal_independent(arm,rom.read_file('/GRP/KANJI.FNT'),case['english'])
                with Image.open(case['preview']) as im:
                    preview=im.convert('L');assert all(bool(p)==(preview.getpixel((i%228,i//228))==0) for i,p in enumerate(pixels))
                expected={(16+i%228,296+i//228) for i,p in enumerate(pixels) if p}
                actual={(x,y) for y in range(294,366) for x in range(16,244) if picture.getpixel((x,y))==(0,8,0)}
                assert actual==expected,(number,frame,len(expected-actual),len(actual-expected))
                oldraw=Path(oldshots[frame]['path']).read_bytes();oldformatted=oldraw[oldwrapped:oldwrapped+512].split(b'\0')[0]
                oldpixels=raster(arm,oldformatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
                oldexpected={(16+i%228,296+i//228) for i,p in enumerate(oldpixels) if p}
                oldactual={(x,y) for y in range(294,366) for x in range(16,244) if oldpicture.getpixel((x,y))==(0,8,0)}
                assert oldactual==oldexpected and diff==expected^oldexpected
                holds.append({'message_ID':number,'frame':frame,'english':case['english'],'complete_native_independent_reference_and_actual_RGB_match':True,
                    'all_RGB_changes_equal_exact_old_new_letter_XOR':True,'changed_pixels':len(diff),'native_pipeline':native,
                    'capture':target['path'],'capture_sha256':target['PNG_sha256'],'complete_leading_trailing_letters_literal_margin_bounds_and_blank_paper_pass':True})
        assert [r['frame'] for r in holds]==expectedholds
        # The original fear/awe response remains complete and unchanged in the latest combined ROM.
        if lookout:
            assert {5800,5830,5900,5930} <= {r['frame'] for r in controls}
            for frame in [5800,5830,5900,5930]:
                raw=Path(shots[frame]['path']).read_bytes();assert raw[owner+0x2030:owner+0x2230].split(b'\0')[0]==entries[2209].text
        raw=Path(shots[terminal]['path']).read_bytes();cpu,get=get_machine(arm,raw)
        assert struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12))==(0,0,0)
        controller=raw.find(struct.pack('<I',0x02147148),0x170000)
        assert controller>=0 and struct.unpack_from('<I',raw,controller+0x74)[0]==0
        records.append({'message_ID':number,'candidate':current['candidate'],'candidate_sha256':current['candidate_sha256'],
            'audit':current,'reference_audit':old,'holds':holds,'whole_other_RGB_controls':controls,
            'normal_A_dismissal_and_original_Info_Mode_return':True,'terminal_frame':terminal,
            'return_is_Inspect_over_sea_not_Sea_View_UI':True,'existing_2209_complete_scene_retained':lookout})
    ROOT.mkdir(parents=True)
    save(ROOT/'both_original_status_paths_native_RGB_and_transitions.json',{'candidate':records[0]['candidate'],'candidate_sha256':records[0]['candidate_sha256'],
        'paths':records,'both_source_original_statuses_observed_without_message_injection':True,
        'entire4MiB_fixtures_input_primary_RAM_PNG_and_unchanged_donor_audits_pass':True,
        'only_expected306307_letter_pixels_change_in_both_replays':True,'both_normal_Inspect_returns_proven':True,
        'targeted_headless_not_full_route_or_hardware':True,'visual_review_pending':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Both306/307 original paths/full native and actual RGB holds/normal Inspect returns pass;all other full screens exact and2209 preserved.')
