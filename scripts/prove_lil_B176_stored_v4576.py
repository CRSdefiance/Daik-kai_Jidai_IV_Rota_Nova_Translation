"""Verify all10 final parity-preserving stored targets through their native consumers."""
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_lil_B174_fonts_v4470 import expand as expand_progressive
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as expand_FE
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster,expected_pixels
from scripts.lil_kuhn_china_FE_painter_v2909 import make_painter
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B176_stored_v4576')
DOC=Path('translations/lil_B176_editorial_manuscript_v3.json')
PLAN=Path('work/analysis/lil_B176_relocation_v4575/nested_source_relocation_research.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,plan=map(read,[DOC,PLAN]);fontpath=Path(doc['native_font_proof']);font=read(fontpath)
    assert sha(fontpath.read_bytes())==doc['native_font_proof_sha256'] and plan['manuscript_sha256']==sha(DOC.read_bytes())
    fonts={r['id']:r for r in font['cases']};source=read(doc['source_context']);image=NdsImage.open(doc['current_ROM'])
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B176_fonts_v4570/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context')
    class FontROM:
        @staticmethod
        def open(path):
            assert str(path)=='work/clean.nds'
            return ctx.rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__)
    raster.__kwdefaults__=original_raster.__kwdefaults__
    cases=[];fresh=0;reused=0;paint=None;calibration=None
    expected_fresh=4*sum(r['parity_space_added'] for b in plan['blocks'] for r in b['text_records'])
    for b in plan['blocks']:
        target=Path(b['research_block']).read_bytes();assert sha(target)==b['research_block_sha256']
        for r in b['text_records']:
            c=fonts[r['id']];compiled=bytes.fromhex(c['encoded_hex']);stored=bytes.fromhex(r['target_hex']);pad=r['parity_space_added']
            assert stored==compiled+(b' ' if pad else b'') and len(stored)%2==r['old_length']%2
            assert target[r['new_offset']:r['new_offset']+len(stored)]==stored and target[r['new_offset']+len(stored)]==0
            fe=stored[0]==254;assert stored[0] in [174,175,254]
            if not pad:
                pipeline=next(p for p in c['current_native_macro_pipelines'] if p['kind']=='compiled-protected')
                events=c['complete_glyph_events'];plane_sha=c['whole_native_plane_sha256'];reused+=4
                method='Exact stored/compiled bytes reuse four original native alignment cases and the complete reviewed native plane.'
            else:
                pipeline=ctx.execute(expand_FE,stored[1:]) if fe else ctx.execute(expand_progressive,stored[1:],stored[0])
                ctx.machines.pop();fresh+=4
                expanded=stored[1:]
                assert not any(m in expanded for m in [b'FI',b'FA',b'FO'])
                assert len(pipeline['cases'])==4 and all(p['output_hex']==expanded.hex() for p in pipeline['cases'])
                if fe:
                    if paint is None:paint,calibration=make_painter(image)
                    result=paint(expanded);events=result['events']
                    assert result['complete_return_input_object_canaries_and_native_independent_plane_equal']
                    assert sha(result['logical'])==c['whole_native_plane_sha256']
                    assert sha(result['physical'])==c['whole_physical228x64_plane_sha256']
                    plane_sha=sha(result['logical'])
                    assert all(p['null_source_actor'] for p in pipeline['cases'])
                else:
                    pixels,events,metrics=raster(ctx.arm,expanded)
                    assert pixels==expected_pixels(ctx.arm,metrics,events);plane_sha=sha(pixels)
                    assert plane_sha==c['whole_native_plane_sha256']
                assert [e['code'] for e in events if e['code']!=32]==[e['code'] for e in c['complete_glyph_events'] if e['code']!=32]
                assert all(0<=e['x']<=(222 if fe else 210) and 0<=e['y']<=(36 if fe else 48) for e in events if e['code']!=32)
                method='Fresh four-alignment original processor cases and complete native logical/physical planes for the formatter-owned parity tail.'
            cases.append(dict(id=r['id'],block=b['block'],consumer='FE-paper' if fe else 'progressive',parity_space_added=pad,
                stored_target_hex=stored.hex(),stored_offset=r['new_offset'],current_final_target_macro_alignment_cases=pipeline,
                complete_final_target_native_plane_equals_reviewed_plane=True,native_plane_sha256=plane_sha,complete_native_glyph_events=events,
                tail_padding_consumed_without_blank_page_or_lost_glyph=True,proof_method=method))
    assert len(cases)==10 and fresh==expected_fresh and fresh+reused==40 and not ctx.machines
    assert sum(c['consumer']=='FE-paper' for c in cases)==1
    save(ROOT/'all10_final_stored_targets40_macro_cases_and_complete_planes.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),native_font_proof=str(fontpath),native_font_proof_sha256=sha(fontpath.read_bytes()),
        final_target_parity_cases=cases,current_final_stored_macro_alignment_cases=40,new_parity_macro_alignment_cases=fresh,
        exact_byte_identical_reused_macro_alignment_cases=reused,new_parity_tail_planes=fresh//4,exact_reused_compiled_planes=reused//4,
        all10_final_targets_complete_native_planes_equal_reviewed_planes=True,source_complete_preambles_and_old_parity_preserved=True,
        actual_selected_B176_scene_A000_C200_bodies_and_single_end_reachability_unexecuted=True,
        FE_calibration=calibration,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        no_playable_ROM_registry_ledger_orcompletion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(stored_targets=10,progressive=9,FE=1,macro_cases=40,fresh_parity_cases=fresh,reused_exact_cases=reused,new_parity_planes=fresh//4,credit=0))
