"""Complete current auxiliary label glyphs; actual menu geometry stays separately bound."""
from pathlib import Path
from PIL import Image,ImageDraw
from scripts.verify_village_wrap_v608 import read,save
from scripts.primary_town_native_font_v2102 import font_tools,glyph_codes
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_production_compact_capacity_v2138 import probe
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/palace_inn_aux_fonts_v2259')
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True);rom=NdsImage.open('out/all_routes_combined_v2171_candidate.nds');arm=rom.read_file('/__arm9__.bin');kanji=rom.read_file('/GRP/KANJI.FNT');doc=read('translations/palace_inn_contextual_editorial_manuscript_v1.json');raster,_,_=font_tools(rom)
    obs=read('E:/Rota Nova translations/Generated/work/emulation_v193/town_trend_actual_v2178_50_V2171/common_observer/requests.json')['rows'][0];native_times={r['current_native_text_hex']for r in read('work/analysis/inn_context_v2251d/native_context.json')['month_prefix_native_cases']};cases=[]
    for i,r in enumerate(doc['auxiliary_labels']):
        value=r['english'].replace('%s','１０');text=b' '+value.encode('cp932')
        if i>=6:assert value.encode('cp932').hex()in native_times
        logical=probe(arm,obs,text);assert logical['complete']and logical['logical_row_origins']==[0];events=[];plane=raster(arm,text,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000,glyph_events=events)
        assert plane==independent_font(arm,kanji,[value])and [e['code']for e in events if e['code']!=32]==glyph_codes(text)
        p=ROOT/f'aux_{i}.png';Image.frombytes('L',(228,64),bytes(0 if v else 255 for v in plane)).save(p);cases.append(dict(id=r['id'],expanded_English=value,full_native_font_control=logical,complete_native_and_independent_glyphs=True,preview=str(p),preview_sha256=sha(p.read_bytes()),generic_shared_font_capacity_not_actual_Palace_menu_geometry=True))
    sheet=Image.new('RGB',(1404,168*3),'#263238');draw=ImageDraw.Draw(sheet)
    for i,r in enumerate(cases):
        x,y=i%3*468,i//3*168;draw.text((x+4,y+3),r['id']+' / '+r['expanded_English'],fill='white');sheet.paste(Image.open(r['preview']).convert('RGB').resize((456,128),Image.Resampling.NEAREST),(x+4,y+25))
    p=ROOT/'nine_current_auxiliary_fonts.png';sheet.save(p);save(ROOT/'auxiliary_font_proof.json',dict(ARM9_sha256=sha(arm),cases=cases,review_sheets=[dict(path=str(p),sha256=sha(p.read_bytes()),scope='offline-current-shared-font-glyphs-not-actual-menu')],nine_complete_native_returns_and_independent_fonts=True,current144_native_time_provider_outputs_bound=True,actual_Palace12_menu_rows_historical_geometry_separate=True,visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(auxiliary_fonts=9,sheets=1))
