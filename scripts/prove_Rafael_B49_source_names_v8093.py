"""All61 clean Japanese pages;two fresh header names andfive exact header-plane reuses."""
import inspect
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events
from scripts import lil_B207_name_style_v6354d as name_source
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_source_name_planes_v8093')
CURRENT=Path('work/analysis/Rafael_B49_current_v8086/all61_complete_source_current_refs_before_new_English_manuscript.json')
EFFECTIVE=Path('work/analysis/Rafael_B49_effective_v8087/all61_effective_English_templates122_original_dispatches_no_FE.json')
NAMES=Path('work/analysis/Rafael_B49_names_v8078/seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json')
NATIVE=Path('work/analysis/Rafael_B49_pages_refined_v8092/61_final_native_pages20_fresh224_reused_alignments.json')
LOGICAL=Path('work/analysis/Rafael_B49_logical_v8089/61_logical_paragraphs244_original_native_alignments_no_FE.json')
OLD=Path('work/analysis/Rafael_B48_source_name_planes_v8037/91_complete_source_pages9_names36_literal_alignments4_FE.json')
START=Path('work/analysis/Rafael_B48_context_binding_v8069/own_Rafael_startup_andstrict_captain0_context.json')
if __name__=='__main__':
    assert not ROOT.exists();current,effective,names,native,logical,old,start=map(read,[CURRENT,EFFECTIVE,NAMES,NATIVE,LOGICAL,OLD,START])
    image=NdsImage.open(current['current_ROM']);arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
    assert sha(arm)==old['ARM9_sha256']==current['current_ARM9_sha256'] and sha(font)==old['font_sha256']
    assert start['candidate_sha256']==current['current_ROM_sha256'] and start['all_whole_RGB_actor_andcaptain_controls_equal']
    assert start['all_strict2b6_COMMON_directory_and123264_payload_guards_pass']
    pe={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes};exec(compile(native['source_owned_progressive_page_adapter'],__file__+'::source-pages','exec'),pe)
    ne=dict(expand.__globals__);exec(compile(logical['source_owned_progressive_adapter'],__file__+'::own-literal-name','exec'),ne)
    style_adapter=checked_text(inspect.getsource(name_source.style_source_proof),{'assert sha(arm)==ARM9;':'assert sha(arm)==CURRENT_ARM9;'})
    assert style_adapter==old['source_owned_name_style_adapter']
    se={**name_source.__dict__,'CURRENT_ARM9':sha(arm)};exec(compile(style_adapter,__file__+'::style11','exec'),se)
    exec(compile(inspect.getsource(name_source.native_name_raster),__file__+'::native-raster','exec'),se)
    assert se['style_source_proof'](arm)==old['original_current_name_style_source_proof']
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(names['current_native_input'],'unused-no-historical-ROM',ROOT/'current_context');nameplanes=[];sourcepages=[];fresh=[];reused=[]
    for getter in names['native_fourteen_progressive_andfull_getters']['rows']:
        if getter['consumer']!='progressive-nameplate':continue
        text=getter['text'];raw=text.encode('ascii');actor=getter['actor_ID']
        prior=next((r for r in old['name_planes'] if r['actor_ID']==actor),None)
        if prior is not None:
            assert prior['text']==text and prior['input_hex']==raw.hex() and sha(Path(prior['native_plane']).read_bytes())==prior['native_plane_sha256']
            pixels,events,usedfont=se['native_name_raster'](arm,raw)
            assert pixels==Path(prior['native_plane']).read_bytes()==expected_pixels(arm,usedfont,events) and events==prior['events']
            plane=deepcopy(prior);plane.update(reused_exact_native_name_plane_andliteral_alignment=True,prior_name_proof=str(OLD),prior_name_proof_sha256=sha(OLD.read_bytes()),
                original_current_code_font_literal_text_andwhole_actor_startup_controls_equal=True)
            nameplanes.append(plane);reused.append(actor);continue
        assert actor in [2,9]
        result=ctx.execute(ne['expand'],raw,actor);ctx.machines.pop();assert len(result['cases'])==4 and all(c['output_hex']==raw.hex() for c in result['cases'])
        pixels,events,usedfont=se['native_name_raster'](arm,raw);assert pixels==expected_pixels(arm,usedfont,events)
        visible,flushes=original_name_events(events,raw);assert visible==codes(raw)
        plane=ROOT/f'actor{actor}_complete_name.bin';plane.write_bytes(pixels)
        nameplanes.append(dict(actor_ID=actor,text=text,input_hex=raw.hex(),native_alignment=result,native_plane=str(plane),native_plane_sha256=sha(pixels),events=events,
            original_zero_ink_flushes=flushes,original_pair_flush_width=(len(raw)+1)//2*12,original_source_style=11,reused_exact_native_name_plane_andliteral_alignment=False));fresh.append(actor)
    for row in current['records']:
        assert row['source_selector']!=254
        case=next(c for c in effective['source_current_dispatches'] if c['id']==row['id'] and c['version']=='clean-Japanese')
        body=bytes.fromhex(next(b for b in case['boundaries'] if b['kind']=='unexecuted-progressive-body')['text_hex']);source=bytes.fromhex(row['source_hex'])[1:]
        assert body==source.replace(b'FI',b'Rafael').replace(b'FA',b'Castor').replace(b'FO',b'Castor Co.')
        rendered=pe['pages'](arm,font,body)
        for page in rendered['pages']:
            pixels=bytes.fromhex(page.pop('native_plane_hex'));plane=ROOT/(row['id']+f'_source_page{page["page"]}.bin');plane.write_bytes(pixels);page.update(native_plane=str(plane),native_plane_sha256=sha(pixels))
        sourcepages.append(dict(id=row['id'],file_path=row['file_path'],block=49,source_selector=row['source_selector'],source_reference=row['source_reference'],kind='progressive',source_body_hex=source.hex(),original_current_expanded_source_hex=body.hex(),**rendered))
    assert len(nameplanes)==7 and fresh==[2,9] and reused==[0,4,5,6,8] and len(sourcepages)==61 and not ctx.machines
    assert sum(len(r['pages']) for r in sourcepages)==61
    save(ROOT/'61_complete_source_pages7_names8_fresh20_reused_literal_alignments.json',dict(
        candidate=current['current_ROM'],candidate_sha256=current['current_ROM_sha256'],ARM9_sha256=sha(arm),font_sha256=sha(font),name_planes=nameplanes,source_records=sourcepages,source_complete_native_pages=61,
        current_name_literal_alignment_cases=28,fresh_name_literal_alignment_cases=8,exact_reused_name_literal_alignment_cases=20,fresh_header_actors=fresh,reused_header_actors=reused,
        original_current_name_style_source_proof=old['original_current_name_style_source_proof'],source_owned_name_style_adapter=style_adapter,source_owned_header_raster=inspect.getsource(name_source.native_name_raster),
        source_owned_macro_adapter=logical['source_owned_progressive_adapter'],source_owned_page_adapter=native['source_owned_progressive_page_adapter'],
        all61_original_Japanese_paragraphs_twoFI_andcomplete_name_glyphs_preserved=True,
        all_native_complete_codes_glyph_planes_bounds_input_canaries_andconsumption_exact=True,
        source_only_nineteenth_cell_not_observed_in_offline_line_width_scan_no_new_global_geometry_claim=True,
        no_FE_source_orFE_palette_coverage_claim=True,offline_source_andname_planes_not_actual_orfull207_name_approval=True,
        actual_source_English_body_header_C281_transition_andreturn_audit_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,EFFECTIVE,NAMES,NATIVE,LOGICAL,OLD,START,Path(name_source.__file__),Path(__file__)]}))
    print('61source Japanese pages/seven style11names pass. Lil/Camille:8fresh literal alignments;five exact headers/20cases reused. Actual headers/catalogue/custom names still pending.')
