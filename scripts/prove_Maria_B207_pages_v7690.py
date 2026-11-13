"""Fresh Maria compiled text ABI checks and exact original native page/font proofs."""
import inspect
from copy import deepcopy
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_pages_v7690')
PLAN=Path('work/analysis/maria_B207_layout_v7689/Maria18_automatic_full_width_plans_all_base_QA_preserved.json')
LOGICAL=Path('work/analysis/maria_B207_logical_v7688/all18_Maria_logical_bodies72_fresh_literal_IF_alignments.json')
PRIOR=Path('work/analysis/papal_trade_native_pages_v7634/two_routes36_complete_pages144_fresh_compiled_alignments_exact_logical_andfont_reuse.json')
MANUSCRIPT=Path('translations/maria_B207_editorial_manuscript_v1.json')
if __name__=='__main__':
    assert not ROOT.exists();plan,logical,prior,doc=map(read,[PLAN,LOGICAL,PRIOR,MANUSCRIPT])
    assert plan['manuscript_sha256']==logical['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    now,old=[NdsImage.open(p) for p in [doc['current_ROM'],prior['candidate']]]
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256'] and sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']
    for path in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:assert now.read_file(path)==old.read_file(path)
    arm,font=now.read_file('/__arm9__.bin'),now.read_file('/GRP/KANJI.FNT')
    page_adapter=prior['source_owned_2b6_page_adapter'];pe={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes};exec(compile(page_adapter,__file__+'::exact-original-page-renderer','exec'),pe)
    adapter=checked_text(inspect.getsource(expand),{'assert identity==prefix and captain==2':'assert identity==prefix and captain==EXPECTED_CAPTAIN==3'})
    env={**expand.__globals__,'EXPECTED_CAPTAIN':3};exec(compile(adapter,__file__+'::Maria-compiled-body','exec'),env)
    ROOT.mkdir(parents=True);ctx=MariaUnlockedCurrentContext(doc['current_strict_native_input'],'unused-no-historical-ROM',ROOT/'current_context')
    rows=[];pictures=[];fresh=0;reused=0
    for r,p,l in zip(doc['records'],plan['records'],logical['records'],strict=True):
        assert r['id']==p['id']==l['id'];encoded=bytes.fromhex(p['encoded_hex']);body=encoded[1:];prefix=r['source_selector']
        assert encoded[0]==prefix and prefix in [19,104] and body and not body.endswith(b'\n') and not any(v in body for v in [b'FI',b'FA',b'FO',b'\0'])
        native=ctx.execute(env['expand'],body,prefix);ctx.machines.pop();assert len(native['cases'])==4 and all(c['output_hex']==body.hex() for c in native['cases'])
        previous=next((v for v in prior['groups'][0]['records'] if bytes.fromhex(v['compiled_hex'])[1:]==body),None)
        if previous:
            rendered={k:deepcopy(previous[k]) for k in ['pages']};reused+=1;mode='exact-prior-compiled-body-whole-ARM9-COMMON-FNT-native-font-reuse'
            for page in rendered['pages']:
                assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256'] and sha(Path(page['preview']).read_bytes())==page['preview_sha256']
        else:
            rendered=pe['pages'](arm,font,body);fresh+=1;mode='fresh-original-native-page-render'
            for page in rendered['pages']:
                pixels=bytes.fromhex(page.pop('native_plane_hex'));plane=ROOT/(r['id']+f'_page{page["page"]}.bin');plane.write_bytes(pixels)
                leading=len(body[page['start']:page['end']])-len(body[page['start']:page['end']].lstrip(b' '))
                assert leading==0 and page['first_visible_origin']==[0,0]
                picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
                picture.putdata([colors[v] for v in pixels]);preview=plane.with_suffix('.png');picture.save(preview)
                page.update(native_plane=str(plane),native_plane_sha256=sha(pixels),preview=str(preview),preview_sha256=sha(preview.read_bytes()),compiler_owned_page_continuation_guard_bytes=leading,exact_first_visible_origin_verified_without_font_orbounds_change=True)
        assert len(rendered['pages'])==p['expected_native_pages']==1
        rows.append(dict(id=r['id'],file_path=doc['file_path'],source_record_index=r['source_record_index'],source_selector=prefix,compiled_hex=p['encoded_hex'],formatted_markup=p['formatted_markup'],logical_native_alignment_exact_reference=l,compiled_native_alignment=native,page_proof_mode=mode,prior_exact_native_page_reference=dict(path=str(PRIOR),file_path=previous['file_path'],id=previous['id']) if previous else None,**rendered))
        pictures.append((r['source_record_index'],Image.open(rendered['pages'][0]['preview']).convert('RGB')))
    assert not ctx.machines and len(rows)==18 and fresh+reused==18
    sheets=[]
    for start in range(0,18,6):
        sheet=Image.new('RGB',(1296,320),'#263238');draw=ImageDraw.Draw(sheet)
        for n,(index,picture) in enumerate(pictures[start:start+6]):
            x,y=n%3*432,n//3*160;draw.text((x+3,y+3),'Maria SC3B207 R'+str(index)+' native offline page',fill='white');sheet.paste(picture.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
        path=ROOT/f'Maria_native_pages_sheet{start//6+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'Maria18_complete_native_pages72_fresh_compiled_alignments.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),layout_plan=str(PLAN),layout_plan_sha256=sha(PLAN.read_bytes()),logical_proof=str(LOGICAL),logical_proof_sha256=sha(LOGICAL.read_bytes()),prior_native_page_proof=str(PRIOR),prior_native_page_proof_sha256=sha(PRIOR.read_bytes()),records=rows,distinct_native_pages=18,fresh_native_page_renders=fresh,exact_reused_native_page_renders=reused,fresh_compiled_alignment_cases=72,exact_reused_logical_alignment_cases=72,all18_single_original_four_row_pages=True,all_first_internal_final_glyphs_bounds_canaries_consumption_andpair_phase_verified=True,source_owned_Maria_compiled_adapter=adapter,source_owned_2b6_page_adapter=page_adapter,review_sheets=sheets,visual_review_pending=True,generic_preview_shade_not_actual_CP932_palette_claim=True,offline_native_CPU_checks_not_optional_scene_gameplay=True,all18_formatting_gates_remain_false=True,stored_actual_controls_policy_reference_andrelease_pending=True,existing_system_only_unlock_fixture=True,earned_unlock_verified=False,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),evidence={str(p):sha(p.read_bytes()) for p in [PLAN,LOGICAL,PRIOR,MANUSCRIPT,Path(__file__)]},new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print(dict(complete_single_native_pages=18,fresh_compiled_alignments=72,exact_logical_alignment_reuse=72,fresh_native_page_renders=fresh,exact_native_page_reuse=reused,visual_stored_actual_release_pending=True))
