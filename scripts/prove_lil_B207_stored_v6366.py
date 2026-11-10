"""Prove all13 actual stored bodies,including source-parity tails,through current native consumers."""
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v6261b import CurrentContext
from scripts.verify_lil_B174_fonts_v4470 import expand
from scripts.verify_name_catalog_glyphs_v278 import raster as inherited_raster
from scripts.shady_man_font_oracles_v6263 import expected_pixels
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B207_stored_v6366')
DOC=Path('translations/lil_B207_editorial_manuscript_v5.json')
PLAN=Path('work/analysis/lil_B207_relocation_v6365/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan=map(read,[DOC,PLAN]);font=read(doc['native_font_proof']);assert plan['manuscript_sha256']==sha(DOC.read_bytes()) and sha(Path(doc['native_font_proof']).read_bytes())==doc['native_font_proof_sha256'];fonts={r['id']:r for r in font['cases']}
    ROOT.mkdir(parents=True);ctx=CurrentContext(doc['current_strict_native_input'],'unused-no-historical-ROM',ROOT/'current_context')
    class FontROM:
        @staticmethod
        def open(path):assert str(path)=='work/clean.nds';return ctx.rom
    raster=FunctionType(inherited_raster.__code__,{**inherited_raster.__globals__,'NdsImage':FontROM},argdefs=inherited_raster.__defaults__);raster.__kwdefaults__=inherited_raster.__kwdefaults__
    cases=[];fresh=0;reused=0;spec=plan['blocks'][0];target=Path(spec['research_block']).read_bytes();assert sha(target)==spec['research_block_sha256']
    for r in spec['text_records']:
        case=fonts[r['id']];compiled=bytes.fromhex(case['encoded_hex']);stored=bytes.fromhex(r['target_hex']);pad=r['parity_space_added'];assert stored==compiled+(b' ' if pad else b'') and stored[0] in [2,14] and len(stored)%2==r['old_length']%2 and target[r['new_offset']:r['new_offset']+len(stored)+1]==stored+b'\0'
        if not pad:
            pipeline=next(p for p in case['current_native_macro_pipelines'] if p['kind']=='compiled-protected');events=case['complete_glyph_events'];plane_sha=case['whole_native_plane_sha256'];reused+=4;method='Exact stored/compiled bytes reuse four native alignment cases and the complete approved plane.'
        else:
            pipeline=ctx.execute(expand,stored[1:],stored[0]);ctx.machines.pop();fresh+=4;assert all(p['output_hex']==stored[1:].hex() for p in pipeline['cases']);pixels,events,fontdata=raster(ctx.arm,stored[1:]);assert pixels==expected_pixels(ctx.arm,fontdata,events);plane_sha=sha(pixels);assert plane_sha==case['whole_native_plane_sha256'] and [e['code'] for e in events if e['code']!=32]==[e['code'] for e in case['complete_glyph_events'] if e['code']!=32] and all(0<=e['x']<=210 and 0<=e['y']<=48 for e in events if e['code']!=32);method='Fresh four-alignment original processor cases and complete unchanged native plane for the single owned parity space.'
        cases.append(dict(id=r['id'],block=207,consumer='progressive',parity_space_added=pad,stored_target_hex=stored.hex(),stored_offset=r['new_offset'],current_final_target_macro_alignment_cases=pipeline,complete_final_target_native_plane_equals_reviewed_plane=True,native_plane_sha256=plane_sha,complete_native_glyph_events=events,tail_padding_consumed_without_blank_page_or_lost_glyph=True,proof_method=method))
    assert len(cases)==13 and fresh+reused==52 and fresh==4*sum(r['parity_space_added'] for r in spec['text_records']) and not ctx.machines
    save(ROOT/'all13_final_stored_targets52_alignment_cases_and_complete_planes.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),native_font_proof=doc['native_font_proof'],native_font_proof_sha256=doc['native_font_proof_sha256'],final_target_parity_cases=cases,current_final_stored_macro_alignment_cases=52,new_parity_macro_alignment_cases=fresh,exact_byte_identical_reused_macro_alignment_cases=reused,new_parity_tail_planes=fresh//4,exact_reused_compiled_planes=reused//4,all13_final_targets_complete_native_planes_equal_reviewed_planes=True,source_complete_preambles_and_old_parity_preserved=True,no_FE_menu_branch_or_macro_assumption=True,actual_English_scene_and_references_still_pending=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_ROMs=0,new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(stored_planes=13,alignment_cases=52,fresh=fresh,exact_reused=reused,all_planes_unchanged=True))
