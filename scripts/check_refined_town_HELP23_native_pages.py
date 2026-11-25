"""Fresh native checks forchanged pages;exact-byte/runtime reuse forunchanged reviewed pages."""
from copy import deepcopy
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.check_early_HELP23_native_pages import ADAPTER,original

ROOT=Path('work/analysis/Shared_HELP_T21_T43_formatting_20261104')
PLAN=ROOT/'refined_v2/automatic_plans_v1.json'
PRIOR=ROOT/'native_pages_v1/native_help_pages.json'
OUT=ROOT/'refined_native_v2'
RELEASE=Path('work/analysis/Rafael_B61_B80_release_verified_20261104/registered_release_verification.json')
if __name__=='__main__':
    assert not OUT.exists();plan,prior=map(load,[PLAN,PRIOR]);assert prior['native_pages']==29 and len(plan['pages'])==28
    ctx=RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'),captain=0)
    assert prior['runtime']==ctx.receipt() and prior['current_ARM9_sha256']==sha(ctx.arm)
    parent=NdsImage.open(plan['current_ROM']);verified=NdsImage.open(load(RELEASE)['candidate'])
    assert sha(Path(plan['current_ROM']).read_bytes())==plan['current_ROM_sha256']
    assert all(parent.read_file(p)==verified.read_file(p) for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT'])
    resource=Path(plan['research_resource']).read_bytes();assert sha(resource)==plan['target_HELP_sha256'];blocks=IlnkContainer.parse(resource).blocks
    old={p['topic_id']:p for p in prior['records']};env={**original.verify.__globals__,'__file__':__file__}
    exec(compile(ADAPTER,__file__+'::same-complete-current-code-andpixel-guarded-Help-parser','exec'),env)
    OUT.mkdir();proofs=[];pictures=[];fresh=reused=0
    for page in plan['pages']:
        t=page['topic_id'];assert blocks[t]==bytes.fromhex(page['encoded_hex'])
        if t in old and old[t]['encoded_hex']==page['encoded_hex']:
            receipt=deepcopy(old[t]);png=Path(receipt['preview']);assert sha(png.read_bytes())==receipt['preview_sha256']
            picture=Image.open(png).convert('RGB');reused+=1
            receipt.update(exact_native_reuse=dict(proof=str(PRIOR),sha256=sha(PRIOR.read_bytes()),topic_id=t,
                encoded_bytes_current_ARM9_font_runtime_andparser_exact=True,prior_page_count=receipt['page_count']))
        else:
            receipt,picture=env['verify'](ctx.arm,page);png=OUT/('topic_'+str(t)+'_native.png');picture.save(png);fresh+=1
            receipt.update(preview=str(png),preview_sha256=sha(png.read_bytes()))
        receipt.update(source_article_id=page['source_article_id'],page_number=page['page_number'],page_count=page['page_count'],encoded_hex=page['encoded_hex'])
        proofs.append(receipt);pictures.append((page,picture));save(OUT/('topic_'+str(t)+'_complete.json'),receipt)
        print('Refined Help topic',t,'fresh' if 'exact_native_reuse' not in receipt else 'exact-reused',flush=True)
    sheets=[];font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
    for first in range(0,len(pictures),4):
        sheet=Image.new('RGB',(1512,800),'#263238');draw=ImageDraw.Draw(sheet);group=pictures[first:first+4]
        for i,(page,picture) in enumerate(group):
            x,y=(i%2)*756,(i//2)*400;draw.text((x+6,y+5),f"Help{page['source_article_id']} topic{page['topic_id']} p{page['page_number']}/{page['page_count']}",font=font,fill='white')
            sheet.paste(picture.resize((756,360),Image.Resampling.NEAREST),(x,y+30))
        p=OUT/('readable_sheet_'+str(len(sheets)+1)+'.png');sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes()),pages=len(group)))
    save(OUT/'native_help_pages.json',dict(runtime=ctx.receipt(),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),records=proofs,review_sheets=sheets,
        native_pages=28,complete_articles=23,fresh_pages=fresh,exact_reused_pages=reused,current_ARM9_sha256=sha(ctx.arm),
        all_complete_glyph_codes_font_pixels_link_requests_row_coordinates_input_header_andpixel_guards_pass=True,
        all_executed_current_instruction_bytes_exact=True,complete_ASCII_ink_offset_y=1,source_owned_parser_adapter=ADAPTER,
        planned_parent_ARM9_COMMON_font_exact_to_verified_runtime=True,constructed_parser_surface_not_a_gameplay_snapshot=True,
        original_link_UI_child_creation_observed_but_deliberately_not_executed=True,actual_gameplay=False,new_credit=0,
        all_fifth_gates_still_pending=True,direct_visual_review_pending=True,actual_navigation_archive_loading_andregistered_integration_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [PLAN,PRIOR,RELEASE,Path(original.__file__),Path(__file__)]}))
    print('Refined28 pages:',fresh,'fresh native;',reused,'exact byte/runtime reuse;seven sheets await direct review. No new credit.')
