"""Check changed Help pages and reuse only exact old page/runtime/font/visual proofs."""
import argparse
from copy import deepcopy
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.check_early_HELP23_native_pages import ADAPTER,original

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ['plan','prior-native','prior-visual','release','out']:parser.add_argument('--'+key,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    plan,prior,visual=map(load,[args.plan,args.prior_native,args.prior_visual])
    assert prior['all_complete_glyph_codes_font_pixels_link_requests_row_coordinates_input_header_andpixel_guards_pass']and prior['all_executed_current_instruction_bytes_exact']
    assert visual['native_proof_sha256']==sha(args.prior_native.read_bytes())
    viewed={r['topic_id']:r for r in visual['pages']};old={r['topic_id']:r for r in prior['records']}
    assert set(viewed)==set(old)
    ctx=RegisteredRuntime(args.release,args.release.with_name('own_registered_startup_verification.json'),captain=0)
    assert prior['runtime']==ctx.receipt()and prior['current_ARM9_sha256']==sha(ctx.arm)
    parent=NdsImage.open(plan['current_ROM']);verified=NdsImage.open(load(args.release)['candidate'])
    assert sha(Path(plan['current_ROM']).read_bytes())==plan['current_ROM_sha256']
    assert all(parent.read_file(p)==verified.read_file(p)for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT'])
    resource=Path(plan['research_resource']).read_bytes();assert sha(resource)==plan['target_HELP_sha256'];blocks=IlnkContainer.parse(resource).blocks
    env={**original.verify.__globals__,'__file__':__file__};exec(compile(ADAPTER,__file__+'::unchanged-complete-native-Help-parser','exec'),env)
    args.out.mkdir();records=[];fresh=[];reused=[]
    for page in plan['pages']:
        t=page['topic_id'];assert blocks[t]==bytes.fromhex(page['encoded_hex'])
        if t in old and old[t]['encoded_hex']==page['encoded_hex']:
            receipt=deepcopy(old[t]);assert sha(Path(receipt['preview']).read_bytes())==receipt['preview_sha256']==viewed[t]['preview_sha256']
            assert viewed[t]['all_complete_words_first_final_glyphs_links_andboundaries_directly_viewed']
            receipt['exact_native_andvisual_reuse']=dict(native=str(args.prior_native),native_sha256=sha(args.prior_native.read_bytes()),
                visual=str(args.prior_visual),visual_sha256=sha(args.prior_visual.read_bytes()),same_encoded_page_current_runtime_font_controls_andpixels=True)
            reused.append(t)
        else:
            receipt,picture=env['verify'](ctx.arm,page);p=args.out/f'topic_{t}_native.png';picture.save(p)
            receipt.update(preview=str(p),preview_sha256=sha(p.read_bytes()));fresh.append((page,picture))
        receipt.update(topic_id=t,source_article_id=page['source_article_id'],page_number=page['page_number'],page_count=page['page_count'],encoded_hex=page['encoded_hex'])
        records.append(receipt);save(args.out/f'topic_{t}_complete.json',receipt)
        print('Help',t,'exact proof reuse'if t in reused else'fresh native check',flush=True)
    if 'fresh_page_IDs'in plan:assert [p['topic_id']for p,picture in fresh]==plan['fresh_page_IDs']
    sheets=[];font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
    for first in range(0,len(fresh),4):
        group=fresh[first:first+4];sheet=Image.new('RGB',(1512,800),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(page,picture)in enumerate(group):
            x,y=i%2*756,i//2*400;draw.text((x+6,y+5),f"Help{page['topic_id']} p{page['page_number']}/{page['page_count']}",font=font,fill='white')
            sheet.paste(picture.resize((756,360),Image.Resampling.NEAREST),(x,y+30))
        p=args.out/f'fresh_readable_sheet_{len(sheets)+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes()),pages=len(group)))
    save(args.out/'native_help_pages.json',dict(runtime=ctx.receipt(),plan=str(args.plan),plan_sha256=sha(args.plan.read_bytes()),records=records,
        review_sheets=sheets,native_pages=len(records),complete_articles=len({r['source_article_id']for r in records}),
        fresh_pages=len(fresh),fresh_page_IDs=[p['topic_id']for p,picture in fresh],exact_reused_pages=len(reused),exact_reused_page_IDs=reused,
        current_ARM9_sha256=sha(ctx.arm),all_complete_glyph_codes_font_pixels_link_requests_row_coordinates_input_header_andpixel_guards_pass=True,
        all_executed_current_instruction_bytes_exact=True,complete_ASCII_ink_offset_y=1,source_owned_parser_adapter=ADAPTER,
        all_reused_pages_have_exact_individual_prior_native_andvisual_proofs=True,
        planned_parent_ARM9_COMMON_font_exact_to_verified_runtime=True,constructed_parser_surface_not_a_gameplay_snapshot=True,
        original_link_UI_child_creation_observed_but_deliberately_not_executed=True,actual_gameplay=False,new_credit=0,
        fresh_direct_visual_review_pending=True,actual_changed_pages_andregistered_integration_pending=True,
        evidence={str(p):sha(p.read_bytes())for p in [args.plan,args.prior_native,args.prior_visual,args.release,Path(original.__file__),Path(__file__)]}))
    print(dict(native_pages=len(records),fresh=len(fresh),exact_reused=len(reused),fresh_sheets=len(sheets),fresh_visual_review_pending=True))
