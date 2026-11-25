"""Audit original creature inspection runs and every actual response pixel."""
import inspect,struct
from pathlib import Path
from types import FunctionType
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.sea_responses_editorial import current_entries
from scripts import verify_sea_registration_pilot_v1552j as template
from scripts import native_sea_inspection_fixture_v1566 as current_fixture
from scripts import native_sea_inspection_control_fixture_v1567b as old_fixture
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/sea_inspection_verified_v1568b')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
BASE=0x02000000
TABLE=0x021186E0

def audit(label,module,terminal):
    source=inspect.getsource(template.audit).replace('==46','==48').replace('46_owned','48_owned')
    source=source.replace('register_original_Monster_Fish', 'register_original_Monster_Fish_and_assign_lookout')
    digest=sha(module.ROM.read_bytes())
    source=source.replace('b8b256650bb426e99012be06fd060114da0fbf32f763b5c3434204dda8f50437',digest)
    env={**template.__dict__,'__file__':__file__,'ROM':module.ROM,'apply_fixture':module.apply_fixture}
    exec(compile(source,__file__,'exec'),env)
    run=Path('work/analysis')/label
    cap=CAP/(label+('_1563' if module is current_fixture else '_1542'))
    return env['audit'](run,cap,terminal)

if __name__=='__main__':
    assert not ROOT.exists()
    new,newshots,arm=audit('sea_inspection_final_v1567d',current_fixture,6300)
    initial,initialshots,initialarm=audit('sea_inspection_actual_v1567',current_fixture,6100)
    old,oldshots,oldarm=audit('sea_inspection_control_v1567c',old_fixture,6100)
    newreport,initialreport,oldreport=[read(p['terminal_report']) for p in [new,initial,old]]
    # The whole earlier run is a byte-identical actual framebuffer replay prefix.
    newframes={r['frame']:r for r in newreport['frames_captured']}
    for row in initialreport['frames_captured']:
        with Image.open(row['path']) as a,Image.open(newframes[row['frame']]['path']) as b:
            assert a.convert('RGB').tobytes()==b.convert('RGB').tobytes()
    assert newreport['scripted_input_schedule'][:len(oldreport['scripted_input_schedule'])]==oldreport['scripted_input_schedule']
    rom=NdsImage.open(new['candidate']);oldrom=NdsImage.open(old['candidate'])
    common=rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm)
    assert rom.read_file('/GRP/KANJI.FNT')==oldrom.read_file('/GRP/KANJI.FNT')
    fonts=read('work/analysis/sea_responses_fonts_v1558/native_font_research.json')
    case=next(r for r in fonts['cases'] if r['message_ID']==2209)
    assert fonts['ARM9_sha256']==sha(arm) and fonts['COMMON_sha256']==sha(common)
    class CurrentFont:
        @staticmethod
        def open(path):
            assert path=='out/all_routes_combined_v255_candidate.nds'
            return rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    owner,wrapped=[struct.unpack_from('<I',arm,p)[0]-BASE for p in [0x552A0,0x54450]]
    oldwrapped=struct.unpack_from('<I',oldarm,0x54450)[0]-BASE
    holds,controls=[],[]
    for row in oldreport['frames_captured']:
        frame=row['frame'];target=newframes[frame]
        with Image.open(row['path']) as oi,Image.open(target['path']) as ni:
            picture,oldpicture=ni.convert('RGB'),oi.convert('RGB')
            diff={(i%256,i//256) for i,(a,b) in enumerate(zip(picture.get_flattened_data(),oldpicture.get_flattened_data(),strict=True)) if a!=b}
            if not diff:
                controls.append({'frame':frame,'whole256x384_RGB_exact_to_V1542':True});continue
            raw=Path(newshots[frame]['path']).read_bytes();cpu,get=get_machine(arm,raw)
            duty=get(0xCB1A8)+0x2090
            assert get(0x8205C,duty,1)==32 and get(0x82BC4,duty,3)==18 and get(0x82BC4,duty,9)==208
            identity=get(0x82478,duty,7);actor=get(0xCB184)+4+32*identity
            assert identity==18 and get(0x7E988,actor)==0 and get(0x53F4C,actor,TABLE)==2209
            value=raw[owner+0x2030:owner+0x2230].split(b'\0')[0]
            formatted=raw[wrapped:wrapped+512].split(b'\0')[0]
            assert value==entries[2209].text and formatted.hex()==case['native_pipeline']['formatted_hex']
            native=consumer(arm,common,raw,{'patches':[]},0x53D44,7,TABLE)
            assert native['input_hex']==value.hex() and native['formatted_hex']==formatted.hex()
            assert native['parent']==0x02053DB8 and native['selector_offset']==0x27C
            pixels=raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
            assert pixels==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),case['lines'])
            with Image.open(case['preview']) as preview:
                reference=preview.convert('L')
                assert all(bool(p)==(reference.getpixel((i%228,i//228))==0) for i,p in enumerate(pixels))
            expected={(16+i%228,296+i//228) for i,p in enumerate(pixels) if p}
            actual={(x,y) for y in range(294,366) for x in range(16,244) if picture.getpixel((x,y))==(0,8,0)}
            assert actual==expected,(frame,len(expected-actual),len(actual-expected))
            oldraw=Path(oldshots[frame]['path']).read_bytes()
            oldformatted=oldraw[oldwrapped:oldwrapped+512].split(b'\0')[0]
            oldpixels=raster(arm,oldformatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
            oldexpected={(16+i%228,296+i//228) for i,p in enumerate(oldpixels) if p}
            oldactual={(x,y) for y in range(294,366) for x in range(16,244) if oldpicture.getpixel((x,y))==(0,8,0)}
            assert oldactual==oldexpected
            assert diff==expected^oldexpected,(frame,len(diff),len(expected^oldexpected))
            holds.append({'frame':frame,'message_ID':2209,'actual_actor_ID':18,'original_role':7,'source_voice':0,
                'native_pipeline':native,'complete_native_independent_reference_and_actual_RGB_letters_match':True,
                'whole_RGB_changes_equal_exact_old_new_native_letter_XOR':True,'changed_pixels':len(diff),
                'complete_leading_trailing_letters_uniform6px_margins_bounds_and_blank_paper_pass':True,
                'capture':target['path'],'capture_sha256':target['PNG_sha256']})
    assert [r['frame'] for r in holds]==[5800,5830,5900,5930]
    # This is an observed unrelated legacy message,not completion of the following box.
    for frame in [6040,6100]:
        raw=Path(newshots[frame]['path']).read_bytes()
        assert raw[owner+0x2030:owner+0x2230].split(b'\0')[0]==entries[306].text
    raw=Path(newshots[6300]['path']).read_bytes();cpu,get=get_machine(arm,raw)
    assert struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12))==(0,0,0)
    controller=raw.find(struct.pack('<I',0x02147148),0x170000)
    assert controller>=0 and struct.unpack_from('<I',raw,controller+0x74)[0]==0
    save_data={'candidate':new['candidate'],'candidate_sha256':new['candidate_sha256'],
        'audits':[new,initial,old],'holds':holds,'whole_other_RGB_controls':controls,
        'entire48_owned_byte_fixture_and_all4MiB_inputs_RAM_PNG_and_unchanged_donors_audited':True,
        'original_target_inspection_role7_Charles18_voice0_ID2209_observed':True,
        'normal_response_dismissal_following_ID306_and_final_A_close_return_to_Inspect6300':True,
        'legacy306_and307_wrong_text_findings_remain_open':True,
        'only2209_individually_activated_other7_have_native_family_coverage':True,
        'source_prose_reviews_added':0,'completed_entries_added':0,
        'targeted_headless_not_full_playthrough_or_hardware':True,'visual_actual_review_pending':True,
        'V1568_label_erratum':'6300 returns to Info Mode over the sailing scene;global mode000 alone does not prove the Sea View interface. Source bytes and captures are unchanged.',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    ROOT.mkdir(parents=True);save(ROOT/'original_inspection_complete_pixels_and_transition.json',save_data)
    print('Actual2209 full native/independent/reference/RGB holds',len(holds),'other whole controls',len(controls),'normal final return to Inspect6300;legacy306/307 remain open,no completion credit.')
