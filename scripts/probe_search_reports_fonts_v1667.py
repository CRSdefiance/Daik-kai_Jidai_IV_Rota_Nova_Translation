"""Successor:revised2218,all real quantity width pairs,and disclosed numeric stress."""
from pathlib import Path
from itertools import product

if __name__ == '__main__':
    source = Path('scripts/probe_search_reports_fonts_v1663.py').read_text(encoding='utf-8')
    for a,b in [('work/analysis/search_reports_fonts_v1663','work/analysis/search_reports_fonts_v1667'),
                ('work/analysis/search_reports_payload_v1661','work/analysis/search_reports_payload_v1666'),
                ('translations/search_reports_editorial_manuscript_v1.json','translations/search_reports_editorial_manuscript_v2.json'),
                ('from scripts.search_reports_native_consumers_v1662 import','from scripts.search_reports_native_consumers_v1662b import')]:
        assert source.count(a)==1;source=source.replace(a,b)
    old="            actual = [e for e in events if e['y'] == row_index*16]"
    new="""            origin = 0 if n == 312 else 6
            margin = [e for e in events if e['y'] == row_index*16 and e['x'] < origin]
            assert all(e['code'] == 32 and e['x'] == 0 for e in margin)
            guards.extend(margin)
            actual = [e for e in events if e['y'] == row_index*16 and e['x'] >= origin]"""
    assert source.count(old)==1;source=source.replace(old,new)
    old="        assert native.get('input_hex', native.get('loaded_template_hex')) == value.hex()"
    assert source.count(old)==1;source=source.replace(old,"        assert native['loaded_template_hex'] == value.hex()")
    old="        formatted = bytes.fromhex(native['formatted_hex'])"
    assert source.count(old)==1;source=source.replace(old,"        if n != 312: assert native['input_hex'] == expected.hex()\n"+old)
    old="    cases, findings, choices, previews = [], [], [], []"
    new=old+"\n    stress_findings=[]\n    bounds=read(doc['source_quantity_bounds'])\n    assert bounds['conservative_water_max']==4650 and bounds['conservative_food_max']==3875\n    PAIRS=list(dict.fromkeys(PAIRS+list(product([5,10,100,1000],repeat=2))+[(4650,3875),(4650,5),(5,3875)]))"
    assert source.count(old)==1;source=source.replace(old,new)
    old="        cases.append(case)"
    new="""        if n>=2229 and not (0<=native['source_amounts'][0]<=4650 and 0<=native['source_amounts'][1]<=3875):
            case['outside_original_quantity_bounds_CPU_stress_only']=True
            case['stress_layout_findings']=list(issues)
            if issues:stress_findings.append({'message_ID':n,'source_voice':voice,'amounts':native['source_amounts'],'lines':lines,'findings':list(issues)})
            issues=[];case['findings']=[]
        else:case['source_reachable_quantity_width_layout_gate_applies']=True
        cases.append(case)"""
    assert source.count(old)==1;source=source.replace(old,new)
    source=source.replace('len(cases) == 142','len(cases) == 8+8*len(PAIRS)+len(AMOUNTS)')
    start=source.index("    sheet = Image.new('RGB'")
    end=source.index("    save(ROOT/'native_font_research.json'",start)
    source=source[:start]+"""    sheets=[]
    for first in range(0,len(previews),16):
        group=previews[first:first+16]
        sheet=Image.new('RGB',(936,152*((len(group)+1)//2)),'#263238');draw=ImageDraw.Draw(sheet)
        for j,case in enumerate(group):
            x,y=j%2*468,j//2*152
            draw.text((x+5,y+3),f'ID{case["message_ID"]} voice{case["source_voice"]} {case["native_pipeline"]["source_amounts"]}',fill='white')
            with Image.open(case['preview']) as preview:sheet.paste(preview.resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
        path=ROOT/f'Search_reports_native_review_{first//16+1}.png';sheet.save(path)
        sheets.append({'path':str(path),'sha256':sha(path.read_bytes()),'panels':len(group)})
"""+source[end:]
    source=source.replace("'sheets_for_visual_review':[{'path':str(path),'sha256':sha(path.read_bytes())}]", "'sheets_for_visual_review':sheets,'source_quantity_bounds':doc['source_quantity_bounds'],'outside_source_bounds_stress_findings':stress_findings,'all_original_one_to_four_digit_quantity_width_pairs_tested':True")
    source=source.replace("142 native/independent", "{len(cases)} native/independent")
    exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__,'product':product})
