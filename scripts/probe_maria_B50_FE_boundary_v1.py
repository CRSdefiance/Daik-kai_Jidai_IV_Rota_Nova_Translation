"""Compare FE-specific break encodings with unchanged text and all original native assertions."""
import inspect,textwrap
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw,ImageFont
from dk4tool.dialogue.codec import parse_markup,tokens_to_bytes
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts import square_shopkeeper_font_oracles_v7020 as ascii_font
from scripts import Rafael_B45_FE_source_painter_v7894 as native_FE
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.source_locked_derivation_v5118 import checked_text

ROOT=Path('work/Maria_B50_FE_resolution_20261109_v1')
OLD=Path('work/Maria_B37_B50_clean_20261109')

def main():
    assert not ROOT.exists()
    release_path=Path('work/maria270_release_v1/registered_release_verification.json');release=load(release_path)
    ctx=RegisteredRuntime(release_path,release['own_registered_startup'],captain=3)
    assert digest('translations/release_stack.json')==release['registry_sha256']
    doc_path=OLD/'formatting_v1/formatting_input.json';doc=load(doc_path)
    original=ctx.image.read_file('/data/SC3.DK4')
    from dk4tool.formats.ilnk import IlnkContainer
    now=IlnkContainer.parse(original).blocks
    old=IlnkContainer.parse(ctx.image.__class__.open(doc['current_ROM']).read_file('/data/SC3.DK4')).blocks
    assert now[50]==old[50]
    ascii_factory=FunctionType(ascii_font.make_painter.__code__,{**ascii_font.make_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm)},argdefs=ascii_font.make_painter.__defaults__)
    observations=[]
    adapter=checked_text(inspect.getsource(native_FE.make_source_painter),{
        "        visible=[e for e in events if e['code']!=32]":
            "        OBSERVATIONS.append(dict(events=events,complete_input_hex=text.hex()))\n        visible=[e for e in events if e['code']!=32]",
    })
    namespace={**native_FE.make_source_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm),'ASCII_painter':ascii_factory,'OBSERVATIONS':observations}
    exec(compile(adapter,__file__+'::read-only-event-copy-all-original-native-assertions-preserved','exec'),namespace)
    painter,calibration=namespace['make_source_painter'](ctx.image)
    ROOT.mkdir();cases=[];images=[]
    rows=[r for r in doc['records'] if r['id'] in ['DK4_MES_B50_R0036','DK4_MES_B50_R0043']]
    assert len(rows)==2 and all(r['source_selector']==254 for r in rows)
    for row in rows:
        text=row['english'];assert '{MACRO:' not in text
        for width in [37,38]:
            lines=textwrap.wrap(text,width=width,break_long_words=False,break_on_hyphens=False)
            assert ' '.join(lines)==text and len(lines)<=4
            for mode,guard,phase in [('bareLF',False,False),('leading_guard',True,False),('progressive_phase_guard',True,True)]:
                markup='{SPEAKER:FE}'+'{LB}'.join(lines)
                encoded=tokens_to_bytes(parse_markup(markup),guard_linebreaks=guard,pair_phase_safe_breaks=phase)
                assert encoded[0]==254 and ' '.join(encoded[1:].decode('ascii').split())==text
                key=row['id']+'_'+str(width)+'_'+mode
                before=len(observations)
                case=dict(id=row['id'],width_budget=width,mode=mode,encoded_hex=encoded.hex(),
                    logical_English=text,automatic_lines=lines,line_lengths=list(map(len,lines)))
                try:
                    rendered=painter(encoded[1:])
                    case['all_original_native_glyph_bounds_input_andbitmap_assertions_pass']=True
                    case['row_comparison']=check_FE_rows(encoded[1:],rendered)
                except AssertionError as exc:
                    case.update(rejected=True,error=str(exc),no_formatting_approval=True)
                else:
                    raw=ROOT/(key+'.bin');raw.write_bytes(rendered['physical'])
                    case.update(rejected=False,native_plane=str(raw),native_plane_sha256=digest(raw),
                        unchanged228x48_bitmap_6x12_metrics_and16physical_pitch=True,
                        observed_ASCII_codes=rendered['events'])
                    pic=Image.frombytes('L',(228,64),bytes(0 if v else 255 for v in rendered['physical'])).convert('RGB')
                    images.append((key,pic,case))
                assert len(observations)==before+1
                events=observations[-1]['events']
                case['diagnostic_actual_rows']={str(y):bytes(e['code'] for e in events if e['y']==y).decode('ascii') for y in sorted({e['y'] for e in events})}
                cases.append(case)
    sheets=[];font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
    for start in range(0,len(images),8):
        selected=images[start:start+8];sheet=Image.new('RGB',(960,((len(selected)+1)//2)*170),'#ddd');draw=ImageDraw.Draw(sheet)
        for i,(key,pic,case) in enumerate(selected):
            x,y=i%2*480,i//2*170
            draw.text((x+4,y+3),key.replace('DK4_MES_',''),font=font,fill='black')
            sheet.paste(pic.resize((456,128),Image.Resampling.NEAREST),(x+4,y+30))
        png=ROOT/f'FE_break_matrix_{len(sheets)+1}.png';sheet.save(png)
        sheets.append(dict(path=str(png),sha256=digest(png),pages=len(selected)))
    save(ROOT/'boundary_matrix.json',dict(runtime=ctx.receipt(),cases=cases,calibration=calibration,
        source_owned_diagnostic_adapter=adapter,all_original_painter_assertions_retained=True,
        no_prose_font_viewport_orengine_change=True,passing_cases_still_require_gameplay=True,
        review_sheets=sheets,direct_visual_review_pending=True,new_credit=0,actual_gameplay=False,
        evidence={str(p):digest(p) for p in [release_path,doc_path,Path(__file__),Path(native_FE.__file__)]}))
    for case in cases:print(case['id'],case['width_budget'],case['mode'],'REJECT' if case['rejected'] else 'PASS',case['diagnostic_actual_rows'])
    print('Sheets',len(sheets),'pending direct review;diagnostic only,no release credit.')
if __name__=='__main__':main()
