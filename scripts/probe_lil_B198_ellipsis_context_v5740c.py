"""Test the original progressive caller's explicit context style11 against retained pauses."""
import inspect,struct
from pathlib import Path
from PIL import Image
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B198_ellipsis_context_v5740c')
FONT=Path('work/analysis/lil_B198_fonts_v5723/all17_progressive_FE_native_planes_and136_alignment_cases.json')
ACTUAL=Path('work/analysis/lil_B198_actual_v5740/fifteen_actual_panels_source_matched_controls_and_complete_native_holds.json')
if __name__=='__main__':
    assert not ROOT.exists()
    font,actual=read(FONT),read(ACTUAL);image=NdsImage.open(font['candidate']);arm=image.read_file('/__arm9__.bin')
    assert arm[0x54270:0x5429C]==bytes.fromhex('7e0f8de20410a0e10120a0e3b70302eb0b10a0e30a00a0e128128de5bdaa00eb0010a0e17e0f8de2590402eb')
    assert struct.unpack_from('<I',arm,0x54280)[0]==0xE3A0100B
    assert struct.unpack_from('<I',arm,0x54288)[0]==0xE58D1228
    adapter=checked_text(inspect.getsource(original_raster),{
        'call(cpu, 0xD5404, (ctx, string))':"cpu.mem_write(ctx + 0x30, struct.pack('<I', 11))\n    call(cpu, 0xD5404, (ctx, string))"})
    class FontROM:
        @staticmethod
        def open(path):
            assert str(path)=='work/clean.nds'
            return image
    env={**original_raster.__globals__,'NdsImage':FontROM}
    exec(compile(adapter,__file__+'::source_caller_context11','exec'),env)
    report=read(actual['versions'][1]['capture_report']);ROOT.mkdir(parents=True);cases=[]
    for ident in ['DK4_MES_B198_R0049','DK4_MES_B198_R0076','DK4_MES_B198_R0038']:
        case=next(r for r in font['cases'] if r['id']==ident)
        interval=next(r['interval'] for r in actual['actual_panels'] if r['id']==ident)
        photo=next(r for r in reversed(report['frames_captured']) if interval['start']+30<r['frame']<interval['returned']-10)
        pixels,events,glyphs=env['raster'](arm,bytes.fromhex(case['expanded_hex']))
        captured=Image.open(photo['path']).convert('RGB')
        ink={(x,y) for y in range(64) for x in range(216) if pixels[y*216+x]==11}
        gray={(x,y) for y in range(64) for x in range(216) if pixels[y*216+x]==115}
        actual_ink={(x,y) for y in range(64) for x in range(216) if captured.getpixel((16+x,296+y))==(0,8,0)}
        actual_gray={(x,y) for y in range(64) for x in range(216) if captured.getpixel((16+x,296+y))==(98,97,98)}
        binary=ROOT/(ident+'_source_caller_style11_plane.bin');binary.write_bytes(pixels)
        cases.append(dict(id=ident,capture=photo,capture_sha256=sha(Path(photo['path']).read_bytes()),
            native_events=events,native_value_counts={str(v):pixels.count(v) for v in sorted(set(pixels))},native_plane=str(binary),native_plane_sha256=sha(pixels),
            exact_actual_ink=ink==actual_ink,exact_actual_gray=gray==actual_gray,
            native_ink_count=len(ink),native_gray_count=len(gray),actual_ink_count=len(actual_ink),actual_gray_count=len(actual_gray)))
    save(ROOT/'original_caller_style11_two_CP932_pauses_and_ASCII_control.json',dict(
        candidate=font['candidate'],candidate_sha256=font['candidate_sha256'],original_caller_span=arm[0x54270:0x5429C].hex(),
        source_context_stack_offset=0x1F8,source_context_style_field=0x30,source_explicit_style=11,
        original_caller_store_0x228_equals_context_0x1F8_plus0x30=True,source_owned_raster_adapter=adapter,cases=cases,
        no_ROM_runtime_prose_or_captured_pixel_change=True,evidence={str(p):sha(p.read_bytes()) for p in [FONT,ACTUAL,Path(__file__)]},
        new_emulator_runs=0,new_editorial_credit=0,full_goal_complete=False))
    print([(r['id'],r['exact_actual_ink'],r['exact_actual_gray'],r['native_ink_count'],r['native_gray_count']) for r in cases])
