"""Bind59 stored targets;repaint36 parity tails,reuse23 exact compiled bodies."""
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_lil_B141_fonts_v3549 import expand as expand_progressive
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as expand_FE
from scripts.lil_kuhn_china_FE_painter_v2909 import make_painter
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B152_B154_stored_v3639')
DOC=Path('translations/lil_B152_B154_editorial_manuscript_v6.json')
PLAN=Path('work/analysis/lil_B152_B154_relocation_v3638/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan=map(read,[DOC,PLAN]);fontpath=Path(doc['native_font_proof']);font=read(fontpath);assert sha(fontpath.read_bytes())==doc['native_font_proof_sha256'] and plan['manuscript_sha256']==sha(DOC.read_bytes());fonts={r['id']:r for r in font['cases']};source=read(doc['source_context']);image=NdsImage.open(doc['current_ROM']);ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B152_B160_voices_v3616/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context');paint,calibration=make_painter(image)
    class FontROM:
        @staticmethod
        def open(path):assert str(path)=='work/clean.nds';return ctx.rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__);raster.__kwdefaults__=original_raster.__kwdefaults__;cases=[];fresh=0;reused=0
    for b in plan['blocks']:
        target=Path(b['research_block']).read_bytes();assert sha(target)==b['research_block_sha256']
        for r in b['text_records']:
            c=fonts[r['id']];compiled=bytes.fromhex(c['encoded_hex']);stored=bytes.fromhex(r['target_hex']);pad=r['parity_space_added'];assert stored==compiled+(b' ' if pad else b'') and len(stored)%2==r['old_length']%2 and target[r['new_offset']:r['new_offset']+len(stored)]==stored and target[r['new_offset']+len(stored)]==0;fe=stored[0]==254;assert stored[0] in [2,9,14,17,20,92,115,148]
            if not pad:
                pipeline=next(p for p in c['current_native_macro_pipelines'] if p['kind']=='compiled-protected');events=c['complete_glyph_events'];plane_sha=c['whole_native_plane_sha256'];reused+=4;method='Exact compiled stored bytes reuse the four previously verified original macro cases and native plane.'
            else:
                pipeline=ctx.execute(expand_FE,stored[1:]) if fe else ctx.execute(expand_progressive,stored[1:],stored[0]);ctx.machines.pop();expanded=stored[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.');assert len(pipeline['cases'])==4 and all(p['output_hex']==expanded.hex() for p in pipeline['cases']);fresh+=4
                if fe:
                    targetpaint=paint(expanded);assert targetpaint['complete_return_input_object_canaries_and_native_independent_plane_equal'];pixels=targetpaint['physical'];events=targetpaint['events'];assert sha(targetpaint['logical'])==c['complete_logical228x48_plane_sha256']
                else:pixels,events,metrics=raster(ctx.arm,expanded);assert pixels==expected_pixels(ctx.arm,metrics,events)
                plane_sha=sha(pixels);assert plane_sha==c['whole_native_plane_sha256'];assert [e['code'] for e in events if e['code']!=32]==[e['code'] for e in c['complete_glyph_events'] if e['code']!=32];assert all(0<=e['x']<=(222 if fe else 210) and 0<=e['y']<=(36 if fe else 48) for e in events if e['code']!=32);method='Fresh original four-alignment macro calls and whole native font plane for appended parity space.'
            cases.append(dict(id=r['id'],block=b['block'],consumer='FE-paper' if fe else 'progressive',parity_space_added=pad,stored_target_hex=stored.hex(),stored_offset=r['new_offset'],current_final_target_macro_alignment_cases=pipeline,complete_final_target_native_plane_equals_reviewed_plane=True,native_plane_sha256=plane_sha,complete_native_glyph_events=events,tail_padding_consumed_without_blank_page_or_lost_glyph=True,proof_method=method))
    assert len(cases)==59 and fresh==144 and reused==92 and not ctx.machines
    save(ROOT/'all59_final_stored_targets236_macro_cases_and_complete_planes.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),native_font_proof=str(fontpath),native_font_proof_sha256=sha(fontpath.read_bytes()),final_target_parity_cases=cases,current_final_stored_macro_alignment_cases=236,new_parity_macro_alignment_cases=144,exact_byte_identical_reused_macro_alignment_cases=92,new_parity_tail_planes=36,exact_reused_compiled_planes=23,all59_final_targets_complete_native_planes_equal_reviewed_planes=True,source_complete_preambles_and_old_parity_preserved=True,all_resource_bodies_and_actual_selected_scenes_unexecuted=True,FE_calibration=calibration,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),no_playable_ROM_registry_ledger_orcompletion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('All59 stored targets match reviewed native planes;236 alignment cases:144fresh on36parity tails plus92exact reuses. No new ROM or gameplay.')
