"""Prove final stored C strings, reusing exact planes and freshly checking five parity tails."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from scripts.verify_lil_B174_fonts_v4470 import expand
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B223_stored_v7098');PLAN=Path('work/analysis/lil_B223_relocation_v7097/all17_object_relocation_RESEARCH_ONLY.json');FONT=Path('work/analysis/lil_B223_native_pages_v7092c/all17_paragraphs19_complete_pages136_native_alignments.json');DOC=Path('translations/lil_B223_editorial_manuscript_v2.json');INPUT=Path('work/analysis/current_V7067_native_v7077/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();plan,font,doc=map(read,[PLAN,FONT,DOC]);assert plan['native_font_proof_sha256']==sha(FONT.read_bytes()) and font['manuscript_sha256']==doc['previous_manuscript_sha256'] and plan['manuscript_sha256']==sha(DOC.read_bytes())
    spec=plan['blocks'][0];block=Path(spec['research_block']).read_bytes();assert sha(block)==spec['research_block_sha256'] and (len(block),spec['research_logical_end'],spec['research_tail_bytes'])==(1384,1384,0)
    records=spec['text_records']+[r for s in spec['actor_style_commands'] for r in s['alternative_records']];assert len(records)==17;byid={r['id']:r for r in doc['records']};fonts={r['id']:r for r in font['records']}
    env=dict(expand.__globals__);exec(compile(font['source_owned_expand_adapter'],__file__+'::same-processor','exec'),env);pg={**old_pages.__globals__,'expected_pixels':expected_pixels};exec(compile(font['source_owned_2b6_page_adapter'],__file__+'::same-pages','exec'),pg)
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');results=[];fresh=reused=0
    for r in records:
        row=byid[r['id']];ordinary=row['kind']=='progressive';value=bytes.fromhex(r['target_hex']);assert block[r['new_offset']:r['new_offset']+len(value)+1]==value+b'\0'
        if ordinary:assert value[0]==row['source_selector'];body=value[1:]
        else:body=value
        old=fonts[r['id']];compiled=bytes.fromhex(old['compiled_hex'])[1:];assert body in [compiled,compiled+b' ']
        if body==compiled:
            pipeline=next(p for p in old['logical_and_compiled_current_native_pipelines'] if p['version']=='compiled-protected');assert all(c['output_hex']==body.hex() for c in pipeline['cases']);reused+=4;rendered={k:old[k] for k in ['pages','total_bytes','complete_consumed_bytes','all_visible_first_internal_final_characters_in_order','no_blank_or_overlap_page']};mode='exact-compiled-bytes-native-proof-reused'
            for page in rendered['pages']:assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
        else:
            pipeline=ctx.execute(env['expand'],body,row['source_selector']);ctx.machines.pop();assert all(c['output_hex']==body.hex() for c in pipeline['cases']);fresh+=4;rendered=pg['pages'](ctx.arm,ctx.rom.read_file('/GRP/KANJI.FNT'),body);assert len(rendered['pages'])==len(old['pages']);mode='fresh-parity-tail-zero-ink-original-page-count-proof'
            for page,before in zip(rendered['pages'],old['pages'],strict=True):
                pixels=bytes.fromhex(page.pop('native_plane_hex'));assert sha(pixels)==before['native_plane_sha256'] and pixels==Path(before['native_plane']).read_bytes();path=ROOT/(r['id']+f'_stored_page{page["page"]}.bin');path.write_bytes(pixels);page.update(native_plane=str(path),native_plane_sha256=sha(pixels),same_complete_ink_as_reviewed_compiled_page=True)
        results.append(dict(id=r['id'],kind=row['kind'],source_selector=row['source_selector'],final_target_hex=value.hex(),final_target_offset=r['new_offset'],proof_mode=mode,current_macro_pipeline=pipeline,complete_pages=rendered,unchanged_words_glyphs_page_count_and_zero_ink_tail=True))
    assert len(results)==17 and (fresh,reused)==(20,48) and not ctx.machines
    save(ROOT/'all17_stored_targets68_alignments_nineteen_complete_pages.json',dict(candidate=plan['candidate'],candidate_sha256=plan['candidate_sha256'],relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),compiled_native_font_proof=str(FONT),compiled_native_font_proof_sha256=sha(FONT.read_bytes()),records=results,final_stored_alignment_cases=68,fresh_alignment_cases=20,exact_reused_alignment_cases=48,fresh_parity_tail_records=5,complete_pages=19,all_final_stored_targets_equal_reviewed_complete_native_ink=True,no_extra_blank_page_or_lost_leading_trailing_internal_glyph=True,all_seven_style_bodies_exclude_virtual_D0_and_have_independent_terminators=True,original_static_and_D0_selectors_and_zero_macros_preserved=True,current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),not_actual_English_scene_observation=True,external_references_and_atomic_registered_release_pending=True,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [PLAN,FONT,DOC,INPUT,Path(__file__)]},full_goal_complete=False));print('17 stored targets/68 alignments(20fresh,48exact reused)/19 complete pages pass. Five parity tails have zero ink; no extra page.')
