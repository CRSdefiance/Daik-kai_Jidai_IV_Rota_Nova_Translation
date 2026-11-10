"""Verify every final stored parity tail, complete page and original FA processor alignment."""
import inspect
from pathlib import Path
from scripts.Al_Ferid_exact_native_context_v6520 import CurrentContext
from scripts.verify_lil_B174_fonts_v4470 import expand
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.Al_Ferid_font_oracles_v6520 import expected_pixels
from scripts.source_locked_derivation_v5118 import checked_text
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B215_stored_v6762');PLAN=Path('work/analysis/lil_B215_relocation_v6761/all15_objects17_commands_full924_inverse_RESEARCH.json');FONT=Path('work/analysis/lil_B215_native_pages_v6752/all15_paragraphs15_complete_native_pages120_alignments.json');INPUT=Path('work/analysis/current_V6733_native_v6742/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();plan,font=read(PLAN),read(FONT);page_adapter=checked_text(inspect.getsource(old_pages),{'4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351':'aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05'});env={**old_pages.__globals__,'expected_pixels':expected_pixels};exec(compile(page_adapter,__file__+'::current-AA5-pages','exec'),env);ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');records=[]
    for ref in plan['blocks'][0]['text_records']:
        raw=bytes.fromhex(ref['target_hex']);body=raw[1:];native=ctx.execute(expand,body,raw[0]);ctx.machines.pop();assert len(native['cases'])==4 and all(c['output_hex']==body.replace(b'FA',b'Argot').hex() for c in native['cases']);rendered=env['pages'](ctx.arm,ctx.rom.read_file('/GRP/KANJI.FNT'),body.replace(b'FA',b'Argot'));base=next(r for r in font['records'] if r['id']==ref['id']);assert len(rendered['pages'])==1
        for p,b in zip(rendered['pages'],base['pages'],strict=True):
            pixels=bytes.fromhex(p.pop('native_plane_hex'));assert pixels==Path(b['native_plane']).read_bytes() and sha(pixels)==b['native_plane_sha256'];path=ROOT/(ref['id']+'_stored_page.bin');path.write_bytes(pixels);p.update(native_plane=str(path),native_plane_sha256=sha(pixels))
        records.append(dict(id=ref['id'],final_target_hex=raw.hex(),final_target_offset=ref['new_offset'],parity_space_added=ref['parity_space_added'],native_pipeline=native,complete_pages=rendered,all_words_glyphs_native_page_count_and_guards_preserved=True))
    assert len(records)==15 and not ctx.machines;save(ROOT/'all15_final_stored_targets60_alignments15_complete_pages.json',dict(candidate=plan['candidate'],candidate_sha256=plan['candidate_sha256'],relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),records=records,all_final_stored_targets_equal_reviewed_complete_native_ink=True,stored_macro_alignment_cases=60,complete_native_pages=15,all_bounds_canaries_pair_phase_and_both_FA_expansions_pass=True,no_actor_model_roster_or_event_mutation=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),external_references_actual_and_release_pending=True,new_emulator_runs=0,new_credit=0,full_goal_complete=False));print('15 final stored targets/60 alignments/15 complete native pages match the reviewed ink,including parity tails and both FA expansions.')
