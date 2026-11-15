"""Format the 23 source-qualified cinematic FE panels without editing their logical prose."""
import math
from functools import cache
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.codec import parse_markup,tokens_to_bytes
from dk4tool.dialogue.qa import WEAK_LINE_ENDINGS
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime import RegisteredRuntime
from scripts import square_shopkeeper_font_oracles_v7020 as old_font
from scripts import Rafael_B45_FE_source_painter_v7894 as source_FE
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as FE_expand
from scripts.source_locked_derivation_v5118 import checked_text

ROOT=Path('work/analysis/Hodram_B156_cinematic_English_v2_20261102')
INPUT=Path('work/analysis/Hodram_B151_B170_formatting_20261102/deferred_cinematic_records.json')
GEOMETRY=Path('work/analysis/Hodram_B156_cinematic_geometry_20261102/observed_cinematic_geometry.json')
RELEASE=Path('work/analysis/Hodram_B131_B150_release_verified_20261102/registered_release_verification.json')
STARTUP=RELEASE.with_name('own_registered_startup_verification.json')
MACROS=Path('work/analysis/Hodram_B61_B70_logical_v8891/logical_paragraphs.json')

def expanded(text):return text.replace('{MACRO:FI}','Hodram').replace('{MACRO:FA}','Bergstrom').replace('{MACRO:FO}','Bergstrom Fleet')

def wrap(text,width):
    words=text.split();assert ' '.join(words)==text
    @cache
    def solve(start):
        if start==len(words):return (0,0,0),[]
        best=None
        for stop in range(start+1,len(words)+1):
            line=' '.join(words[start:stop]);length=len(expanded(line));final=stop==len(words)
            if length>width:continue
            cost,tail=solve(stop);last=words[stop-1].strip('.,!?;:\"').lower()
            weak=int(not final and last in WEAK_LINE_ENDINGS);tiny=int(final and start>0 and length<=8)
            candidate=((cost[0]+weak+tiny,cost[1]+1,cost[2]+(0 if final else (width-length)**2)),[line,*tail])
            if best is None or candidate[0]<best[0]:best=candidate
        assert best is not None
        return best
    return solve(0)[1]

if __name__=='__main__':
    assert not ROOT.exists();doc=load(INPUT);g=load(GEOMETRY)
    visual=load(GEOMETRY.with_name('source_cinematic_visual_review.json'))
    assert visual['geometry_sha256']==sha(GEOMETRY.read_bytes()) and visual['source_FE_panels_viewed']==23
    assert g['all23_source_FE_typed_geometry_228x48_288stride_6x12_current_vtables_exact']
    observed={r['id']:r for r in g['matched_source_records'] if r['source_selector']==254}
    ctx=RegisteredRuntime(RELEASE,STARTUP);clean=NdsImage.open('work/clean.nds');blocks=IlnkContainer.parse(clean.read_file('/data/SC1.DK4')).blocks
    assert sha(Path('work/clean.nds').read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    macro_env=dict(FE_expand.__globals__);exec(compile(load(MACROS)['source_owned_FE_adapter'],__file__+'::unchanged-macro-ABI','exec'),macro_env)
    ascii_factory=FunctionType(old_font.make_painter.__code__,{**old_font.make_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm)},argdefs=old_font.make_painter.__defaults__)
    factory=FunctionType(source_FE.make_source_painter.__code__,{**source_FE.make_source_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm),'ASCII_painter':ascii_factory},argdefs=source_FE.make_source_painter.__defaults__)
    paint,calibration=factory(ctx.image);ROOT.mkdir(parents=True);rows=[];pictures=[]
    for row in doc['records']:
        ident=row['id'];assert ident in observed and row['source_selector']==254 and row['block']==156
        original=bytes.fromhex(row['source_hex']);ref=row['source_reference'];assert blocks[156][ref['offset']:ref['offset']+len(original)]==original
        assert observed[ident]['source_reference']==ref and observed[ident]['actual_geometry_228x48_stride288_font6x12']
        source=row['source_Japanese'];text=row['english'];heading=source.lstrip('\n').startswith('＜')
        first_nonblank=source.lstrip('\n').split('\n')[0];right=first_nonblank.startswith('\u3000')
        # Leave room for the generated LF guard, pair-phase repair and a native
        # edge cell. Right-side blocks also require at least one indent cell.
        width=34 if right else 35
        if heading:
            title,body=text.split(': ',1);assert (title=='Sera' and source.lstrip('\n').startswith('＜セラ＞')) or (title=='{MACRO:FI}' and source.lstrip('\n').startswith('＜FI＞'))
            content=[title+':',*wrap(body,width)]
        else:content=wrap(text,width)
        blank_source=len(source)-len(source.lstrip('\n'));blanks=min(blank_source,4-len(content));assert blanks>=0
        indent=max(1,34-max(len(expanded(s)) for s in content)) if right else 0
        lines=['']*blanks+[(' '*indent+s) for s in content]
        assert 1<=len(lines)<=4 and ' '.join(s.strip() for s in lines if s.strip())==text
        markup='{SPEAKER:FE}'+'{LB}'.join(lines)
        raw=tokens_to_bytes(parse_markup(markup),guard_linebreaks=True,pair_phase_safe_breaks=True,macro_ascii_lengths=dict(FI=6,FA=9,FO=15))
        assert raw[0]==254 and b'\0' not in raw and b'%' not in raw and not raw.endswith((b' ',b'\n'))
        expected=raw[1:].replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet')
        assert ' '.join(expected.decode('ascii').split())==expanded(text)
        assert all(raw[1:].count(m.encode())==row['source_macros'][m] for m in ['FI','FA','FO'])
        aligned=ctx.execute(macro_env['expand'],raw[1:]);assert len(aligned['cases'])==4 and all(c['output_hex']==expected.hex() for c in aligned['cases'])
        rendered=paint(expected);membership=check_FE_rows(expected,rendered)
        plane=rendered.pop('physical');logical=rendered.pop('logical');assert rendered['complete_consumed_bytes']==len(expected)
        for suffix,data in [('physical',plane),('logical',logical)]:
            path=ROOT/f'{ident}_{suffix}.bin';path.write_bytes(data);rendered[suffix+'_plane']=str(path);rendered[suffix+'_sha256']=sha(data)
        picture=Image.new('RGB',(228,64));picture.putdata([(0,8,0) if n else (239,232,201) for n in plane]);png=ROOT/f'{ident}.png';picture.save(png)
        reason=('Keep the source embedded speaker heading on its own row. ' if heading else '')
        reason+=('Keep the source right-side turn as a right-side text block using measured ASCII spacing. ' if right else 'Keep the source left-side turn. ')
        reason+=f'Keep {blanks} source leading blank row(s). '
        if blanks<blank_source:reason+=f'The English uses {len(content)} content rows, so remove {blank_source-blanks} blank row(s) to retain every word on the native four-row panel.'
        rows.append(dict(id=ident,source_reference=ref,current_reference=row['current_reference'],source_hex=row['source_hex'],current_hex=row['current_hex'],
            logical_English=text,compiled_hex=raw.hex(),expanded_native_hex=expected.hex(),formatted_markup=markup,lines=lines,layout_reason=reason,
            source_heading=heading,source_leading_blank_rows=blank_source,kept_blank_rows=blanks,source_right_side=right,automatic_indent_cells=indent,
            source_observed_paint=observed[ident]['actual_paint_frame'],native_macro_alignments=aligned,native=rendered,native_row_membership=membership,
            preview=str(png),preview_sha256=sha(png.read_bytes()),expected_native_pages=1,visual_approval_pending=True,
            all_prose_punctuation_speaker_controls_macros_andcomplete_glyphs_preserved=True,stored_allocation_andactual_English_gameplay_pending=True))
        save(ROOT/f'{ident}_checked.json',rows[-1]);pictures.append((ident,picture))
    assert len(rows)==23 and set(observed)=={r['id'] for r in rows};sheets=[]
    for at in range(0,len(pictures),12):
        subset=pictures[at:at+12];sheet=Image.new('RGB',(912,math.ceil(len(subset)/2)*160),'#263238');draw=ImageDraw.Draw(sheet)
        for j,(ident,picture) in enumerate(subset):
            x=j%2*456;y=j//2*160;draw.text((x+3,y+3),ident+' cinematic offline QA',fill='white');sheet.paste(picture.resize((456,128),Image.Resampling.NEAREST),(x,y+24))
        path=ROOT/f'cinematic_English_{at//12+1:02d}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),pages=len(subset)))
    save(ROOT/'compiled_cinematic_pages.json',dict(records=rows,pages=23,runtime=ctx.receipt(),review_sheets=sheets,FE_calibration=calibration,
        source_geometry=str(GEOMETRY),source_geometry_sha256=sha(GEOMETRY.read_bytes()),source_visual_review=visual,
        complete_native_macro_alignments=92,all_native_glyphs_row_membership_bounds_canaries_andsingle_page_consumption_pass=True,
        all23_individual_layout_reasons_documented=True,logical_prose_unmodified=True,five_gate_formatting_still_false=True,visual_review_pending=True,
        actual_English_gameplay=False,natural_endgame=False,stored_integration_pending=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [INPUT,GEOMETRY,GEOMETRY.with_name('source_cinematic_visual_review.json'),MACROS,Path(__file__),Path(source_FE.__file__)]}))
    print('23 cinematic English pages/92 macro alignments pass native checks; individual source staging retained. Two new sheets require direct visual review; stored/gameplay/release gates pending.')
