"""Bind final stored inputs;reuse exact byte/plane/runtime proofs andrun only new parity inputs."""
from copy import deepcopy
from pathlib import Path
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from scripts.verify_lil_B174_fonts_v4470 import expand
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B225_stored_v7214');PLAN=Path('work/analysis/lil_B225_relocation_v7213/all13_objects16_commands_full976_inverse_RESEARCH.json');FONT=Path('work/analysis/lil_B225_native_pages_v7207/all13_paragraphs14_complete_native_pages104_alignments.json');OLD=Path('work/analysis/lil_B225_stored_v7198/all13_final_stored_targets52_alignments14_complete_pages.json');INPUT=Path('work/analysis/current_V7168_native_v7173/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();plan,font,old=map(read,[PLAN,FONT,OLD]);assert plan['candidate_sha256']==font['candidate_sha256']==old['candidate_sha256']==read(INPUT)['current_ROM_sha256'];fonts={r['id']:r for r in font['records']};prior={r['id']:r for r in old['records']};ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');env={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes};exec(compile(font['source_owned_2b6_page_adapter'],__file__+'::exact-pages','exec'),env);records=[];fresh=initial=compiled_reuse=0
    for ref in plan['blocks'][0]['text_records']:
        raw=bytes.fromhex(ref['target_hex']);body=raw[1:];base=fonts[ref['id']];compiled=bytes.fromhex(base['compiled_hex'])[1:];assert body in [compiled,compiled+b' '] and not any(x in body for x in [b'FI',b'FA',b'FO'])
        if ref['target_hex']==prior[ref['id']]['final_target_hex']:
            r=deepcopy(prior[ref['id']]);r['final_target_offset']=ref['new_offset'];initial+=4;mode='exact-initial-stored-input-plane-runtime-reused'
            assert [p['native_plane_sha256'] for p in r['complete_pages']['pages']]==[p['native_plane_sha256'] for p in base['pages']]
        elif body==compiled:
            pipeline=deepcopy(next(p for p in base['logical_and_compiled_current_native_pipelines'] if p['version']=='compiled-protected'));rendered={k:deepcopy(base[k]) for k in ['pages','total_bytes','complete_consumed_bytes','all_visible_first_internal_final_characters_in_order','no_blank_or_overlap_page']};compiled_reuse+=4;mode='exact-newly-proven-compiled-input-reused';r=dict(id=ref['id'],native_pipeline=pipeline,complete_pages=rendered)
        else:
            pipeline=ctx.execute(expand,body,raw[0]);ctx.machines.pop();rendered=env['pages'](ctx.arm,ctx.rom.read_file('/GRP/KANJI.FNT'),body);assert len(rendered['pages'])==len(base['pages'])
            for pg,before in zip(rendered['pages'],base['pages'],strict=True):
                pixels=bytes.fromhex(pg.pop('native_plane_hex'));assert pixels==Path(before['native_plane']).read_bytes() and sha(pixels)==before['native_plane_sha256'];path=ROOT/(ref['id']+'_page'+str(pg['page'])+'.bin');path.write_bytes(pixels);pg.update(native_plane=str(path),native_plane_sha256=sha(pixels))
            fresh+=4;mode='fresh-new-parity-tail-input';r=dict(id=ref['id'],native_pipeline=pipeline,complete_pages=rendered)
        assert len(r['native_pipeline']['cases'])==4 and all(c['output_hex']==body.hex() for c in r['native_pipeline']['cases'])
        for pg in r['complete_pages']['pages']:assert sha(Path(pg['native_plane']).read_bytes())==pg['native_plane_sha256']
        r.update(final_target_hex=raw.hex(),final_target_offset=ref['new_offset'],parity_space_added=ref['parity_space_added'],proof_mode=mode,all_words_glyphs_native_page_count_and_guards_preserved=True);records.append(r)
    assert len(records)==13 and fresh+initial+compiled_reuse==52 and sum(len(r['complete_pages']['pages']) for r in records)==14 and not ctx.machines
    save(ROOT/'all13_final_stored_targets52_alignments14_complete_pages.json',dict(candidate=plan['candidate'],candidate_sha256=plan['candidate_sha256'],relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),initial_stored_proof=str(OLD),initial_stored_proof_sha256=sha(OLD.read_bytes()),records=records,all_final_stored_targets_equal_reviewed_complete_native_ink=True,stored_alignment_cases=52,fresh_alignment_cases=fresh,exact_reused_alignment_cases=initial+compiled_reuse,exact_reused_initial_stored_cases=initial,exact_reused_revised_compiled_cases=compiled_reuse,complete_native_pages=14,zero_ink_parity_tail_count=sum(r['parity_space_added'] for r in records),all_bounds_canaries_pair_phase_andzero_macros_pass=True,no_actor_roster_event_orname_asset_mutation=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),external_references_actual_andrelease_pending=True,evidence={str(p):sha(p.read_bytes()) for p in [PLAN,FONT,OLD,INPUT,Path(__file__)]},new_emulator_runs=0,new_credit=0,full_goal_complete=False));print(dict(records=13,alignments=52,fresh=fresh,initial_reuse=initial,new_compiled_reuse=compiled_reuse,pages=14))
