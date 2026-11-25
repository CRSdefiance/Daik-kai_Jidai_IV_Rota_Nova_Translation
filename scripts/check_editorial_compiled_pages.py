"""Check new text on an exact registered runtime and render legible offline QA sheets."""
import argparse
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import independent_pixels, load, save
from scripts.registered_editorial_runtime import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as FE_expand
from scripts.research_lil_B209_native_pages_v6461 import pages as inherited_pages
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts import square_shopkeeper_font_oracles_v7020 as old_font
from scripts import Rafael_B45_FE_source_painter_v7894 as source_FE

SOURCE = Path('work/analysis/Hodram_B61_B70_source_display_v8881/224_complete_source_dispatches_alignments_pages_andmacro_binding.json')
MACROS = Path('work/analysis/Hodram_B61_B70_logical_v8891/logical_paragraphs.json')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ('manuscript','plan','release','startup','out'):
        parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args()
    assert not args.out.exists()
    doc,plans,source,macros=map(load,[args.manuscript,args.plan,SOURCE,MACROS])
    assert plans['manuscript_sha256']==sha(args.manuscript.read_bytes())
    assert not plans['failures'] and len(doc['records'])==len(plans['records'])
    assert not any(i['severity'] in ['warning','error'] for row in plans['records'] for i in row['base_QA']['issues'])
    ctx=RegisteredRuntime(args.release,args.startup)
    assert doc['current_ROM_sha256']==sha(ctx.rompath.read_bytes())
    font=ctx.image.read_file('/GRP/KANJI.FNT')
    adapter=checked_text(source['source_owned_target_page_adapter'],
        {'12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b':sha(ctx.arm)})
    env={**inherited_pages.__globals__,'expected_pixels':independent_pixels,'codes':codes}
    exec(compile(adapter,__file__+'::current-registered-progressive','exec'),env)
    pages=env['pages']
    progressive_env=dict(progressive_expand.__globals__)
    exec(compile(macros['source_owned_progressive_adapter'],__file__+'::original-macro-ABI','exec'),progressive_env)
    fe_env=dict(FE_expand.__globals__)
    exec(compile(macros['source_owned_FE_adapter'],__file__+'::original-null-actor-ABI','exec'),fe_env)
    # Reuse source-proven native FE descriptors. Only the exact runtime identity
    # changes; every executed instruction is checked by the source painter.
    ascii_factory=FunctionType(old_font.make_painter.__code__,
        {**old_font.make_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm)},
        argdefs=old_font.make_painter.__defaults__)
    fe_factory=FunctionType(source_FE.make_source_painter.__code__,
        {**source_FE.make_source_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm),'ASCII_painter':ascii_factory},
        argdefs=source_FE.make_source_painter.__defaults__)
    painter,calibration=fe_factory(ctx.image)
    args.out.mkdir(parents=True)
    by_id={row['id']:row for row in plans['records']}
    rows,sheets,all_pictures=[],[],[]
    page_count=alignments=0
    for block in doc['blocks']:
        pictures=[]
        for row in (r for r in doc['records'] if r['block']==block):
            planned=by_id[row['id']]
            raw=bytes.fromhex(planned['encoded_hex']);prefix,body=raw[0],raw[1:]
            assert prefix==row['source_selector'] and body and b'\0' not in body and b'%' not in body
            assert not body.startswith((b' ',b'\n')) and not body.endswith((b' ',b'\n'))
            expected=body.replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet')
            logical=row['english'].replace('{MACRO:FI}','Hodram').replace('{MACRO:FA}','Bergstrom').replace('{MACRO:FO}','Bergstrom Fleet')
            assert ' '.join(expected.decode('cp932').split())==logical
            is_FE=prefix==254
            aligned=ctx.execute(fe_env['expand'] if is_FE else progressive_env['expand'],body,*(() if is_FE else (prefix,)))
            assert len(aligned['cases'])==4 and all(c['output_hex']==expected.hex() for c in aligned['cases'])
            alignments+=len(aligned['cases'])
            if is_FE:
                assert planned['expected_native_pages']==1
                rendered=painter(expected)
                plane=rendered.pop('physical');logical_plane=rendered.pop('logical')
                filename=args.out/(row['id']+'_FE.bin');filename.write_bytes(plane)
                logical_file=filename.with_name(row['id']+'_FE_logical.bin');logical_file.write_bytes(logical_plane)
                rendered.update(native_plane=str(filename),native_plane_sha256=sha(plane),
                    native_logical_plane=str(logical_file),native_logical_plane_sha256=sha(logical_plane))
                picture=Image.new('RGB',(228,64))
                picture.putdata([(0,8,0) if v else (239,232,201) for v in plane])
                png=filename.with_suffix('.png');picture.save(png)
                rendered.update(preview=str(png),preview_sha256=sha(png.read_bytes()))
                pictures.append((row['id']+' FE',picture));page_count+=1
            else:
                rendered=pages(ctx.arm,font,expected)
                assert rendered['complete_consumed_bytes']==len(expected)
                assert len(rendered['pages'])==planned['expected_native_pages']
                for page in rendered['pages']:
                    plane=bytes.fromhex(page.pop('native_plane_hex'))
                    filename=args.out/(row['id']+f'_p{page["page"]}.bin');filename.write_bytes(plane)
                    segment=expected[page['start']:page['end']]
                    guarded=page['page']>1 and segment.startswith(b' ') and not segment.startswith(b'  ')
                    assert page['first_visible_origin']==([6,0] if guarded else [0,0])
                    if guarded:
                        assert page['events'][0]==dict(kind='ascii',code=32,style=1,x=0,y=0)
                    picture=Image.new('RGB',(216,64))
                    colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
                    picture.putdata([colors[v] for v in plane])
                    png=filename.with_suffix('.png');picture.save(png)
                    page.update(native_plane=str(filename),native_plane_sha256=sha(plane),
                        preview=str(png),preview_sha256=sha(png.read_bytes()),
                        native_guard_at_zero_not_missing_first_glyph=guarded)
                    pictures.append((row['id']+f' p{page["page"]}',picture));page_count+=1
            rows.append(dict(id=row['id'],block=block,source_reference=row['source_reference'],
                current_reference=row['current_reference'],compiled_hex=raw.hex(),expanded_native_hex=expected.hex(),
                kind=row['kind'],logical_English=row['english'],native_alignment=aligned,
                complete_native_English_display=rendered))
        for start in range(0,len(pictures),12):
            part=pictures[start:start+12]
            sheet=Image.new('RGB',(912,((len(part)+1)//2)*160),'#263238');draw=ImageDraw.Draw(sheet)
            for index,(label,picture) in enumerate(part):
                x,y=index%2*456,index//2*160
                draw.text((x+3,y+3),label+' offline QA',fill='white')
                sheet.paste(picture.resize((picture.width*2,128),Image.Resampling.NEAREST),(x,y+24))
            filename=args.out/f'B{block}_part{start//12+1}.png';sheet.save(filename)
            sheets.append(dict(block=block,path=str(filename),sha256=sha(filename.read_bytes()),pages=len(part)))
        save(args.out/f'B{block}_checked.json',dict(records=[r for r in rows if r['block']==block],actual_gameplay=False,new_credit=0))
        print('Offline native block',block,'records',sum(r['block']==block for r in rows),'pages',len(pictures),flush=True)
    assert len(rows)==len(doc['records']) and alignments==4*len(rows)
    save(args.out/'compiled_native_pages.json',dict(manuscript=str(args.manuscript),
        manuscript_sha256=sha(args.manuscript.read_bytes()),plan=str(args.plan),plan_sha256=sha(args.plan.read_bytes()),
        runtime=ctx.receipt(),font_sha256=sha(font),records=rows,review_sheets=sheets,
        pages=page_count,fresh_compiled_alignments=alignments,source_owned_target_page_adapter=adapter,
        FE_factory_calibration=calibration,fullwidth_Latin_not_introduced=True,
        all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass=True,
        complete_consumption_andpagination_exact=True,direct_visual_review_pending=True,
        formatting_gates_still_false=True,actual_gameplay=False,new_credit=0,
        stored_script_andactual_headers_transitions_andregistered_release_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [args.manuscript,args.plan,SOURCE,MACROS,
            Path(source_FE.__file__),Path(old_font.__file__),Path(__file__)]}))
    print('PASS',len(rows),'records',page_count,'pages',alignments,'alignments; direct review pending.',flush=True)

if __name__=='__main__':
    main()
