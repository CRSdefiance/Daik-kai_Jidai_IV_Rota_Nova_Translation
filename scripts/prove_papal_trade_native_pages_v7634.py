"""Fresh compiled ABI checks for both routes; render distinct pages once with exact reuse."""
import inspect
from copy import deepcopy
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.draft_papal_trade_prose_v7631 import MANUSCRIPTS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_native_pages_v7634')
PLAN=Path('work/analysis/papal_trade_layout_v7632b/two_routes36_automatic_full_width_plans_all_base_QA_preserved.json')
PRIOR=Path('work/analysis/lil_B234_native_pages_v7587/all18_paragraphs18_complete_native_pages144_alignments.json')
LOGICAL=Path('work/analysis/papal_trade_logical_inputs_v7633/all36_new_logical_bodies144_fresh_native_literal_IF_alignment_cases.json')
if __name__=='__main__':
    assert not ROOT.exists();plan,prior,logical=map(read,[PLAN,PRIOR,LOGICAL])
    doc=read(MANUSCRIPTS[0]);now=NdsImage.open(doc['current_ROM']);old=NdsImage.open(prior['candidate'])
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256'] and sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']
    for path in ['/__arm9__.bin','/GRP/KANJI.FNT','/COMMON/MESFILE.DK4']:assert now.read_file(path)==old.read_file(path)
    arm,font=now.read_file('/__arm9__.bin'),now.read_file('/GRP/KANJI.FNT')
    page_adapter=prior['source_owned_2b6_page_adapter'];page_env={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes}
    exec(compile(page_adapter,__file__+'::exact-original-pages','exec'),page_env)
    adapter=checked_text(inspect.getsource(expand),{'assert identity==prefix and captain==2':'assert identity==prefix and EXPECTED_CAPTAIN in [0,1] and captain==EXPECTED_CAPTAIN'})
    cache={};fresh=0;reuse=0;pictures=[];groups=[];ROOT.mkdir(parents=True)
    for pg,lg in zip(plan['groups'],logical['groups'],strict=True):
        route=pg['route'];mp=MANUSCRIPTS[route];d=read(mp);assert pg['manuscript_sha256']==lg['manuscript_sha256']==sha(mp.read_bytes())
        ctx=RouteCurrentContext(d['current_strict_native_input'],'unused-no-historical-ROM',ROOT/f'route{route}_current_context')
        env={**expand.__globals__,'EXPECTED_CAPTAIN':route};exec(compile(adapter,__file__+'::route-compiled-body','exec'),env)
        rows=[]
        for r,p,l in zip(d['records'],pg['records'],lg['records'],strict=True):
            assert r['id']==p['id']==l['id'];body=bytes.fromhex(p['encoded_hex'])[1:];prefix=r['source_selector']
            assert prefix in [19,104] and body and not body.endswith(b'\n') and not any(v in body for v in [b'FI',b'FA',b'FO',b'\0'])
            native=ctx.execute(env['expand'],body,prefix);ctx.machines.pop()
            assert len(native['cases'])==4 and all(c['output_hex']==body.hex() for c in native['cases'])
            key=body.hex()
            if key not in cache:
                previous=next((v for v in prior['records'] if bytes.fromhex(v['compiled_hex'])[1:]==body),None)
                if previous:
                    rendered={k:deepcopy(v) for k,v in previous.items() if k not in ['id','source_kind','source_selector','compiled_hex','formatted_markup','logical_and_compiled_current_native_pipelines']}
                    for page in rendered['pages']:
                        assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
                        assert sha(Path(page['preview']).read_bytes())==page['preview_sha256']
                    mode='exact-prior-compiled-body-whole-ARM9-FNT-reuse';reuse+=1
                else:
                    rendered=page_env['pages'](arm,font,body);mode='fresh-original-native-page-render';fresh+=1
                    assert len(rendered['pages'])==p['expected_native_pages']==1
                    for page in rendered['pages']:
                        pixels=bytes.fromhex(page.pop('native_plane_hex'));plane=ROOT/(r['id']+f'_page{page["page"]}.bin');plane.write_bytes(pixels)
                        leading=len(body[page['start']:page['end']])-len(body[page['start']:page['end']].lstrip(b' '))
                        assert leading==0 and page['first_visible_origin']==[0,0]
                        picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
                        picture.putdata([colors[v] for v in pixels]);preview=plane.with_suffix('.png');picture.save(preview)
                        page.update(native_plane=str(plane),native_plane_sha256=sha(pixels),preview=str(preview),preview_sha256=sha(preview.read_bytes()),compiler_owned_page_continuation_guard_bytes=leading,exact_first_visible_origin_verified_without_font_orbounds_change=True)
                assert len(rendered['pages'])==1
                cache[key]=dict(rendered=rendered,mode=mode,first_reference=dict(file_path=d['file_path'],id=r['id']),prior_reference=dict(path=str(PRIOR),id=previous['id']) if previous else None)
                for page in rendered['pages']:pictures.append((r['source_record_index'],Image.open(page['preview']).convert('RGB')))
            cached=cache[key]
            rows.append(dict(id=r['id'],file_path=d['file_path'],source_record_index=r['source_record_index'],source_selector=prefix,compiled_hex=p['encoded_hex'],formatted_markup=p['formatted_markup'],logical_native_alignment_exact_reference=l,compiled_native_alignment=native,page_proof_mode=cached['mode'],native_page_proof_first_reference=cached['first_reference'],prior_exact_native_page_reference=cached['prior_reference'],**deepcopy(cached['rendered'])))
        assert len(rows)==18 and not ctx.machines
        groups.append(dict(route=route,route_identity=d['route_identity'],records=rows,fresh_compiled_alignment_cases=72,logical_alignment_cases_exact_proof_reuse=72,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes())))
    assert len(cache)==18 and len(pictures)==18 and fresh+reuse==18;sheets=[]
    for start in range(0,18,6):
        sheet=Image.new('RGB',(1296,320),'#263238');draw=ImageDraw.Draw(sheet)
        for n,(index,picture) in enumerate(pictures[start:start+6]):
            x,y=n%3*432,n//3*160;draw.text((x+3,y+3),f'SC0 B246 / SC1 B237 R{index} exact shared native page',fill='white');sheet.paste(picture.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
        path=ROOT/f'all18_distinct_native_pages_sheet{start//6+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'two_routes36_complete_pages144_fresh_compiled_alignments_exact_logical_andfont_reuse.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],layout_plan=str(PLAN),layout_plan_sha256=sha(PLAN.read_bytes()),logical_proof=str(LOGICAL),logical_proof_sha256=sha(LOGICAL.read_bytes()),prior_native_page_proof=str(PRIOR),prior_native_page_proof_sha256=sha(PRIOR.read_bytes()),groups=groups,distinct_native_pages=18,fresh_native_page_renders=fresh,distinct_prior_exact_reused_native_page_renders=reuse,second_route_exact_shared_page_reuse=18,fresh_compiled_alignment_cases=144,exact_reused_logical_alignment_cases=144,all36_single_original_four_row_pages=True,all_first_internal_final_glyphs_bounds_canaries_consumption_andpair_phase_verified=True,source_owned_route_compiled_adapter=adapter,source_owned_2b6_page_adapter=page_adapter,review_sheets=sheets,visual_review_pending=True,generic_preview_shade_not_actual_R5_CP932_palette_claim=True,offline_native_CPU_checks_not_optional_scene_gameplay=True,all36_formatting_gates_remain_false=True,stored_actual_controls_policy_reference_andrelease_pending=True,evidence={str(p):sha(p.read_bytes()) for p in [PLAN,LOGICAL,PRIOR,*MANUSCRIPTS.values(),Path(__file__)]},new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print(f'36 complete single native pages;144 fresh compiled alignments /144 exact logical reuse;{fresh} fresh distinct page renders /{reuse} prior exact page reuse /18 second-route reuse. Visual, stored, actual andrelease pending.')
