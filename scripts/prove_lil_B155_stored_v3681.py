"""Bind all50 stored targets;fresh checks only for appended parity spaces."""
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_lil_B155_fonts_v3670 import expand
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B155_stored_v3681')
DOC=Path('translations/lil_B155_editorial_manuscript_v8.json')
PLAN=Path('work/analysis/lil_B155_relocation_v3680/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan=map(read,[DOC,PLAN]);fp=Path(doc['native_font_proof']);font=read(fp);assert sha(fp.read_bytes())==doc['native_font_proof_sha256'] and plan['manuscript_sha256']==sha(DOC.read_bytes());fonts={r['id']:r for r in font['cases']};source=read(doc['source_context']);ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B155_B160_source_v3656/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context')
    class FontROM:
        @staticmethod
        def open(path):assert str(path)=='work/clean.nds';return ctx.rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__);raster.__kwdefaults__=original_raster.__kwdefaults__;cases=[];fresh=reused=0;expected_fresh=4*sum(r['parity_space_added'] for b in plan['blocks'] for r in b['text_records'])
    for b in plan['blocks']:
        target=Path(b['research_block']).read_bytes();assert sha(target)==b['research_block_sha256']
        for r in b['text_records']:
            c=fonts[r['id']];compiled=bytes.fromhex(c['encoded_hex']);stored=bytes.fromhex(r['target_hex']);pad=r['parity_space_added'];assert stored==compiled+(b' ' if pad else b'') and len(stored)%2==r['old_length']%2 and stored[0] in [2,6,9,15,20] and target[r['new_offset']:r['new_offset']+len(stored)]==stored and target[r['new_offset']+len(stored)]==0
            if not pad:pipeline=next(p for p in c['current_native_macro_pipelines'] if p['kind']=='compiled-protected');events=c['complete_glyph_events'];plane_sha=c['whole_native_plane_sha256'];reused+=4;method='Exact stored compiled bytes reuse the four prior macro cases andwhole viewed native plane.'
            else:
                pipeline=ctx.execute(expand,stored[1:],stored[0]);ctx.machines.pop();expanded=stored[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.');assert len(pipeline['cases'])==4 and all(p['output_hex']==expanded.hex() for p in pipeline['cases']);fresh+=4;pixels,events,metrics=raster(ctx.arm,expanded);assert pixels==expected_pixels(ctx.arm,metrics,events);plane_sha=sha(pixels);assert plane_sha==c['whole_native_plane_sha256'] and [e['code'] for e in events if e['code']!=32]==[e['code'] for e in c['complete_glyph_events'] if e['code']!=32] and all(0<=e['x']<=210 and 0<=e['y']<=48 for e in events if e['code']!=32);method='Fresh four original macro alignments andwhole native font plane withone appended parity space.'
            cases.append(dict(id=r['id'],block=155,consumer='progressive',parity_space_added=pad,stored_target_hex=stored.hex(),stored_offset=r['new_offset'],current_final_target_macro_alignment_cases=pipeline,complete_final_target_native_plane_equals_reviewed_plane=True,native_plane_sha256=plane_sha,complete_native_glyph_events=events,tail_padding_consumed_without_blank_page_or_lost_glyph=True,proof_method=method))
    assert len(cases)==50 and fresh==expected_fresh and fresh+reused==200 and not ctx.machines;save(ROOT/'all50_final_stored_targets200_macro_cases_and_complete_planes.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),native_font_proof=str(fp),native_font_proof_sha256=sha(fp.read_bytes()),final_target_parity_cases=cases,current_final_stored_macro_alignment_cases=200,new_parity_macro_alignment_cases=fresh,exact_byte_identical_reused_macro_alignment_cases=reused,new_parity_tail_planes=fresh//4,exact_reused_compiled_planes=reused//4,all50_final_targets_complete_native_planes_equal_reviewed_planes=True,source_complete_preambles_and_old_parity_preserved=True,all_resource_bodies_and_actual_selected_scenes_unexecuted=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),no_playable_ROM_registry_ledger_orcompletion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(stored_targets=50,macro_cases=200,fresh_parity_cases=fresh,reused_exact_cases=reused,new_parity_planes=fresh//4,credit=0))
