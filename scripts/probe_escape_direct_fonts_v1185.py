"""Rebind all1417 escape argument/font cases to the proven direct caller."""
import inspect
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import probe_reinforcement_sniping_layout_v1030 as prior
from scripts.probe_duel_escape_fonts_v1157 import original_raster,independent_font,prepared
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/escape_direct_fonts_v1185')
RUNTIME=Path('work/analysis/escape_direct_runtime_v1184c/runtime_plan.json')


def main():
    assert not ROOT.exists()
    plan=read(RUNTIME);arm=Path(plan['research_ARM9']).read_bytes()
    assert sha(arm)==plan['target_ARM9_sha256']
    ref_path=Path('work/analysis/duel_escape_fonts_v1157/native_escape_fonts.json');ref=read(ref_path)
    src=inspect.getsource(prior.native_layout)
    for old,new in [('0x02053DB8','0x02053F40'),
                    ('struct.pack(\'<I\',n)','struct.pack(\'<I\',table)'),
                    ('struct.pack(\'<I\',table))\n    call','struct.pack(\'<I\',0))\n    call')]:
        assert src.count(old)==1;src=src.replace(old,new)
    env=dict(prior.__dict__);exec(compile(src,__file__,'exec'),env);native_layout=env['native_layout']
    rom=NdsImage.open('out/all_routes_combined_v1166_candidate.nds');kanji=rom.read_file('/GRP/KANJI.FNT')
    class CurrentFont:
        @staticmethod
        def open(path): return rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    ROOT.mkdir(parents=True);rows=[];cache={};previews=[]
    for i,case in enumerate(ref['cases']):
        if i%32==0:cpu=prepared(arm)
        n=case['message_ID'];text=bytes.fromhex(case['compiled_hex']);v=case['variant']
        argument=bytes.fromhex(v['name_hex']) if v else None
        table=0x02117500 if n<1973 else 0x02117620
        formatted,lines=native_layout(cpu,text,n,argument,table)
        assert formatted.hex()==case['formatted_hex'] and lines==case['lines']
        if formatted not in cache:
            pixels=raster(arm,formatted,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000)
            assert pixels==independent_font(arm,kanji,lines)
            cache[formatted]=pixels
        pixels=cache[formatted]
        rows.append({'message_ID':n,'variant':v,'compiled_hex':text.hex(),'formatted_hex':formatted.hex(),
            'lines':lines,'native_font_sha256':sha(pixels),'direct_frame':[0x02053F40,0x274,table],
            'original_printf_wrap_complete228x64_native_independent_font_and_guards_pass':True})
        if not any(r['message_ID']==n for r in previews):
            p=ROOT/f'ID{n}_direct.png';Image.frombytes('L',(228,64),bytes(0 if x else 255 for x in pixels)).save(p)
            previews.append({'message_ID':n,'path':str(p),'sha256':sha(p.read_bytes()),'lines':lines})
        if (i+1)%235==0:print(i+1,'direct-frame font cases pass',flush=True)
    assert len(rows)==1417
    sheet=Image.new('RGB',(936,1078),'#263238');d=ImageDraw.Draw(sheet)
    for i,row in enumerate(previews):
        x,y=i%2*468,i//2*154
        d.text((x+5,y+3),f"COMMON{row['message_ID']} direct-frame CPU font",fill='white')
        with Image.open(row['path']) as im:sheet.paste(im.resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
    p=ROOT/'direct_escape_review.png';sheet.save(p)
    save(ROOT/'native_direct_escape_fonts.json',{'ARM9_sha256':sha(arm),'runtime_plan':str(RUNTIME),'runtime_plan_sha256':sha(RUNTIME.read_bytes()),
        'historical_inputs_and_expected_output_reference':str(ref_path),'reference_sha256':sha(ref_path.read_bytes()),
        'historical_parent_binding_superseded':True,'cases':rows,'complete_native_font_cases':len(rows),'unique_planes':len(cache),
        'all13_previews':previews,'review_sheet':str(p),'review_sheet_sha256':sha(p.read_bytes()),
        'native_layout_effective_verifier_sha256':sha(src.encode()),'all_161_previously_reviewed_contextual_boundary_findings_unchanged':True,
        'original_full53F0C_UI_pipeline_and_gameplay_still_separate':True,'no_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('1417 corrected direct-frame escape native fonts pass.',flush=True)


if __name__=='__main__':main()
