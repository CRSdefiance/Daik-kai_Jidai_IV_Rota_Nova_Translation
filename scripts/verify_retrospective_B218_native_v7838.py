"""Complete native before/after planes for the one changed automatic wrap."""
import inspect
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.verify_lil_B174_fonts_v4470 import expand
from scripts.research_lil_B209_native_pages_v6461 import pages as original_pages
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_B218_native_v7838')
DOC=Path('translations/lil_B218_retrospective_layout_manuscript_v1.json')
PLAN=Path('work/analysis/retrospective_B218_predicate_plan_v7833/one_changed_automatic_plan12_exact_reuses_all13_unmodified_base_QA.json')
INPUT=Path('work/analysis/current_V7821_Lil_native_v7837/current_native_input.json')
STARTUP=Path('work/analysis/retrospective_Lil_context_binding_v7837/own_Lil_startup_andstrict_current_context.json')
if __name__=='__main__':
    assert not ROOT.exists()
    doc,plan,inp,start=map(read,[DOC,PLAN,INPUT,STARTUP])
    assert plan['manuscript_sha256']==sha(DOC.read_bytes()) and sha(INPUT.read_bytes())==start['strict_current_native_input_sha256']
    assert inp['current_ROM_sha256']==doc['current_ROM_sha256']==start['candidate_sha256']
    row=next(r for r in doc['records'] if r['id']=='DK4_MES_B218_R0027')
    p=next(p for p in plan['records'] if p['id']==row['id'])
    assert p['proposed']['lines']==["(Ian's interested?","That's a surprise.)"]
    image=NdsImage.open(inp['current_ROM']);arm=image.read_file('/__arm9__.bin');font=image.read_file('/GRP/KANJI.FNT')
    adapter=checked_text(inspect.getsource(original_pages),{
        '4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351':
        '2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'})
    ns={**original_pages.__globals__,'expected_pixels':expected_pixels};exec(compile(adapter,__file__+'::unchanged-native-geometry-andcomplete-glyph-guards','exec'),ns)
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    logical=row['english'].split('}',1)[1].encode('ascii')
    values=[('logical',logical),('previous-compiled',bytes.fromhex(p['previous']['encoded_hex'])[1:]),
        ('proposed-compiled',bytes.fromhex(p['proposed']['encoded_hex'])[1:])]
    pipelines=[];planes=[];pictures=[]
    for label,body in values:
        assert not any(m in body for m in [b'FI',b'FA',b'FO'])
        result=ctx.execute(expand,body,2);ctx.machines.pop()
        assert all(c['output_hex']==body.hex() for c in result['cases']) and len(result['cases'])==4
        pipelines.append(dict(version=label,**result))
        if label=='logical':continue
        rendered=ns['pages'](arm,font,body);assert len(rendered['pages'])==1 and rendered['complete_consumed_bytes']==len(body)
        page=rendered['pages'][0];pixels=bytes.fromhex(page.pop('native_plane_hex'));plane=ROOT/(label+'.bin');plane.write_bytes(pixels)
        assert page['first_visible_origin']==[0,0]
        picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
        picture.putdata([colors[v] for v in pixels]);path=plane.with_suffix('.png');picture.save(path)
        page.update(native_plane=str(plane),native_plane_sha256=sha(pixels),preview=str(path),preview_sha256=sha(path.read_bytes()))
        planes.append(dict(version=label,compiled_hex=(p['previous'] if label=='previous-compiled' else p['proposed'])['encoded_hex'],**rendered))
        pictures.append((label,picture))
    assert len(pipelines)==3 and len(planes)==2 and not ctx.machines
    sheet=Image.new('RGB',(864,180),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(label,picture) in enumerate(pictures):
        draw.text((i*432+3,3),label+' / same 216px viewport',fill='white')
        sheet.paste(picture.resize((432,128),Image.Resampling.NEAREST),(i*432,26))
    sp=ROOT/'current_before_after_complete_native_planes.png';sheet.save(sp)
    save(ROOT/'one_changed_wrap12_alignments_two_complete_current_native_planes.json',dict(
        id=row['id'],file_path='/data/SC2.DK4',block=218,candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),
        original_static_selector=2,actual_current_captain=2,zero_source_logical_compiled_macros=True,
        current_original_processor_alignment_cases=12,pipelines=pipelines,native_planes=planes,
        all_first_internal_andfinal_characters_complete_in_order=True,
        independent_current_font_planes_bounds_unique_cells_canaries_andcomplete_consumption=True,
        original216px_fourrows_geometry_andall_native_high_numeric_constants_preserved=True,
        all_other12_compiled_plans_exact_unchanged_not_retested_here=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        source_owned_native_page_adapter=adapter,source_owned_expand_adapter=inspect.getsource(expand),
        review_sheet=dict(path=str(sp),sha256=sha(sp.read_bytes())),visual_review_pending=True,
        stored_target_branch_controls_actual_gameplay_policy_andregistered_release_pending=True,
        offline_native_planes_are_not_actual_B218_gameplay=True,new_credit=0,new_emulator_runs=0,
        evidence={str(q):sha(q.read_bytes()) for q in [DOC,PLAN,INPUT,STARTUP,Path(__file__)]},full_goal_complete=False))
    print('B218 R27:12 current original processor alignments;before/after complete native planes pass.View pending.Storage/actual/policy/release pending.')
