"""Execute the original Help parser/font with current instruction guards on all25 planned pages."""
import inspect
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts import verify_help_parser_v281 as original
from scripts.source_locked_derivation_v5118 import checked_text

ROOT=Path('work/analysis/Shared_HELP_early23_formatting_20261104')
OUT=ROOT/'native_pages_v2'
PLAN=ROOT/'automatic_plans_v1.json'
RELEASE=Path('work/analysis/Rafael_B51_B60_release_verified_20261104/registered_release_verification.json')

ADAPTER=checked_text(inspect.getsource(original.verify),{
    '            assert 0 <= x <= WIDTH - 6 and 0 <= y <= HEIGHT - 11':
        '            assert 0 <= x <= WIDTH - 6 and 0 <= y <= HEIGHT - 12',
    '                if 0 <= x + xx < WIDTH and 0 <= y + yy < HEIGHT:\n                    expected[(y + yy) * WIDTH + x + xx] = event["style"] if glyph.getpixel((xx, yy)) else 0':
        '                if 0 <= x + xx < WIDTH and 0 <= y + yy + 1 < HEIGHT:\n                    expected[(y + yy + 1) * WIDTH + x + xx] = event["style"] if glyph.getpixel((xx, yy)) else 0',
    '    cpu.mem_write(POOL, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))':
        """    sections=MainCodeFile(arm,BASE).sections
    payload=bytes(sections[3].data[:-48]);cpu.mem_write(POOL,payload)
    spans=[(s.ramAddress,bytes(s.data)) for s in sections]+[(POOL,payload)]
    words={}
    def exact_instruction(u,pc,size,unused):
        owners=[(base,data) for base,data in spans if base<=pc and pc+size<=base+len(data)]
        assert len(owners)==1,hex(pc)
        base,data=owners[0];expected=data[pc-base:pc-base+size]
        assert bytes(u.mem_read(pc,size))==expected,hex(pc)
        if pc in words:assert words[pc]==expected.hex()
        words[pc]=expected.hex()
    cpu.hook_add(UC_HOOK_CODE,exact_instruction)""",
    '            "input_header_pixel_guards_pass": True}, picture':
        '            "input_header_pixel_guards_pass": True,"all_executed_current_instruction_bytes_exact":True,"executed_source_words":[dict(PC=pc,hex=value) for pc,value in sorted(words.items())]}, picture',
})

if __name__=='__main__':
    assert not OUT.exists();plan=load(PLAN)
    assert len(plan['pages'])==25 and plan['target_topic_count']==212 and plan['planning_cells']==41
    assert sha(Path(plan['manuscript']).read_bytes())==plan['manuscript_sha256']
    raw=Path(plan['research_resource']).read_bytes();assert sha(raw)==plan['target_HELP_sha256']
    blocks=IlnkContainer.parse(raw).blocks
    ctx=RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'),captain=0)
    assert ctx.receipt()['candidate_sha256']==plan['current_ROM_sha256']
    env={**original.verify.__globals__,'__file__':__file__}
    exec(compile(ADAPTER,__file__+'::original-Help-parser-with-exact-current-code-words','exec'),env)
    OUT.mkdir();proofs=[];pictures=[]
    for page in plan['pages']:
        assert blocks[page['topic_id']]==bytes.fromhex(page['encoded_hex'])
        receipt,picture=env['verify'](ctx.arm,page)
        png=OUT/('topic_'+str(page['topic_id'])+'_native.png');picture.save(png)
        receipt.update(source_article_id=page['source_article_id'],page_number=page['page_number'],page_count=page['page_count'],
            encoded_hex=page['encoded_hex'],preview=str(png),preview_sha256=sha(png.read_bytes()))
        proofs.append(receipt);pictures.append((page,picture,png))
        save(OUT/('topic_'+str(page['topic_id'])+'_complete.json'),receipt)
        print('Native Help topic',page['topic_id'],'article',page['source_article_id'],'page',page['page_number'],'checked andsaved',flush=True)
    sheets=[];font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
    for first in range(0,len(pictures),4):
        group=pictures[first:first+4];sheet=Image.new('RGB',(1512,800),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(page,picture,png) in enumerate(group):
            x,y=(i%2)*756,(i//2)*400
            draw.text((x+6,y+5),f"Help{page['source_article_id']} topic{page['topic_id']} p{page['page_number']}/{page['page_count']}",font=font,fill='white')
            sheet.paste(picture.resize((756,360),Image.Resampling.NEAREST),(x,y+30))
        path=OUT/('readable_sheet_'+str(len(sheets)+1)+'.png');sheet.save(path)
        sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),pages=len(group)))
    assert len(proofs)==25 and len(sheets)==7
    save(OUT/'native_help_pages.json',dict(runtime=ctx.receipt(),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),
        research_resource=plan['research_resource'],research_resource_sha256=sha(raw),records=proofs,review_sheets=sheets,
        native_pages=25,complete_articles=23,current_ARM9_sha256=sha(ctx.arm),
        all_complete_glyph_codes_font_pixels_link_requests_row_coordinates_input_header_andpixel_guards_pass=True,
        all_executed_current_instruction_bytes_exact=True,source_owned_parser_adapter=ADAPTER,
        complete_ASCII_ink_offset_y=1,descriptor_geometry_and_6x12_logical_metrics_unchanged=True,
        oracle_revision_reason='Historical v281 expected ink at y+0. The accepted current native ASCII painter places the complete eleven ink rows at y+1, as already validated in square_shopkeeper_font_oracles_v7020 and current story proofs. Initial page0 rejected the old pixel model; all native addresses, code, dimensions, row positions and full-plane equality checks remain unchanged. This updates only the independent expected-pixel model.',
        source_owned_native_addresses_andconstants_unchanged=True,
        original_link_UI_child_creation_observed_but_deliberately_not_executed=True,
        constructed_parser_surface_not_a_gameplay_snapshot=True,
        native_archive_loading_complete_widgets_actual_navigation_gameplay_andregistered_integration_pending=True,
        all_fifth_gates_still_pending=True,direct_visual_review_pending=True,actual_gameplay=False,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [PLAN,RELEASE,Path(original.__file__),Path(__file__)]}))
    print('25 native Help pages/23 articles pass;seven readable sheets needdirect view. Widget/navigation/gameplay/release checks pending.')
