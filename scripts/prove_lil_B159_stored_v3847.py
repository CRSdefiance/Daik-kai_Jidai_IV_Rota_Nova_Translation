"""Bind all41 final stored targets;execute only new parity-tail inputs and reuse exact progressive/FE bytes."""
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_lil_B156_fonts_v3707 import expand as expand_progressive
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as expand_FE
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B159_stored_v3847')
DOC=Path('translations/lil_B159_editorial_manuscript_v4.json')
PLAN=Path('work/analysis/lil_B159_relocation_v3846/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan=map(read,[DOC,PLAN]);fontpath=Path(doc['native_font_proof']);font=read(fontpath);assert sha(fontpath.read_bytes())==doc['native_font_proof_sha256'] and plan['manuscript_sha256']==sha(DOC.read_bytes());fonts={r['id']:r for r in font['cases']};source=read(doc['source_context']);image=NdsImage.open(doc['current_ROM']);ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B159_B160_source_v3825/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context');paint,calibration=None,None
    class FontROM:
        @staticmethod
        def open(path):assert str(path)=='work/clean.nds';return ctx.rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__);raster.__kwdefaults__=original_raster.__kwdefaults__;cases=[];fresh=0;reused=0;expected_fresh=4*sum(r['parity_space_added'] for b in plan['blocks'] for r in b['text_records'])
    for b in plan['blocks']:
        target=Path(b['research_block']).read_bytes();assert sha(target)==b['research_block_sha256']
        for r in b['text_records']:
            c=fonts[r['id']];compiled=bytes.fromhex(c['encoded_hex']);stored=bytes.fromhex(r['target_hex']);pad=r['parity_space_added'];assert stored==compiled+(b' ' if pad else b'') and len(stored)%2==r['old_length']%2 and target[r['new_offset']:r['new_offset']+len(stored)]==stored and target[r['new_offset']+len(stored)]==0;fe=stored[0]==254;assert stored[0] in [2,9,14,20,22]
            if not pad:
                pipeline=next(p for p in c['current_native_macro_pipelines'] if p['kind']=='compiled-protected');events=c['complete_glyph_events'];plane_sha=c['whole_native_plane_sha256'];reused+=4;method='Exact compiled stored bytes reuse the four previously verified original macro cases and native plane.'
            else:
                pipeline=ctx.execute(expand_FE,stored[1:]) if fe else ctx.execute(expand_progressive,stored[1:],stored[0]);ctx.machines.pop();expanded=stored[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.');assert len(pipeline['cases'])==4 and all(p['output_hex']==expanded.hex() for p in pipeline['cases']);fresh+=4
                if fe:
                    targetpaint=paint(expanded);assert targetpaint['complete_return_input_object_canaries_and_native_independent_plane_equal'];pixels=targetpaint['physical'];events=targetpaint['events'];assert sha(targetpaint['logical'])==c['complete_logical228x48_plane_sha256']
                else:pixels,events,metrics=raster(ctx.arm,expanded);assert pixels==expected_pixels(ctx.arm,metrics,events)
                plane_sha=sha(pixels);assert plane_sha==c['whole_native_plane_sha256'];assert [e['code'] for e in events if e['code']!=32]==[e['code'] for e in c['complete_glyph_events'] if e['code']!=32];assert all(0<=e['x']<=(222 if fe else 210) and 0<=e['y']<=(36 if fe else 48) for e in events if e['code']!=32);method='Fresh original four-alignment macro calls and whole native font plane for appended parity space.'
            cases.append(dict(id=r['id'],block=b['block'],consumer='FE-paper' if fe else 'progressive',parity_space_added=pad,stored_target_hex=stored.hex(),stored_offset=r['new_offset'],current_final_target_macro_alignment_cases=pipeline,complete_final_target_native_plane_equals_reviewed_plane=True,native_plane_sha256=plane_sha,complete_native_glyph_events=events,tail_padding_consumed_without_blank_page_or_lost_glyph=True,proof_method=method))
    assert len(cases)==41 and fresh==expected_fresh and fresh+reused==164 and not ctx.machines
    save(ROOT/'all41_final_stored_targets164_macro_cases_and_complete_planes.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),native_font_proof=str(fontpath),native_font_proof_sha256=sha(fontpath.read_bytes()),final_target_parity_cases=cases,current_final_stored_macro_alignment_cases=164,new_parity_macro_alignment_cases=fresh,exact_byte_identical_reused_macro_alignment_cases=reused,new_parity_tail_planes=fresh//4,exact_reused_compiled_planes=reused//4,all41_final_targets_complete_native_planes_equal_reviewed_planes=True,source_complete_preambles_and_old_parity_preserved=True,all_resource_bodies_and_actual_selected_scenes_unexecuted=True,FE_calibration=calibration,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),no_playable_ROM_registry_ledger_orcompletion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(stored_targets=41,progressive=41,FE=0,macro_cases=164,fresh_parity_cases=fresh,reused_exact_cases=reused,new_parity_planes=fresh//4,credit=0))
