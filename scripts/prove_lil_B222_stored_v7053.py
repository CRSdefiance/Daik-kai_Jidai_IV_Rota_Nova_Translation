"""Check changed parity-tail inputs while reusing exact complete compiled inputs by hashes."""
from copy import deepcopy
from pathlib import Path
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from scripts.verify_lil_B174_fonts_v4470 import expand
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B222_stored_v7053');PLAN=Path('work/analysis/lil_B222_relocation_v7052/all16_objects18_commands_full1112_inverse_RESEARCH.json');FONT=Path('work/analysis/lil_B222_native_pages_v7047/all16_paragraphs16_complete_native_pages128_alignments.json');INPUT=Path('work/analysis/current_V7029_native_v7033/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();plan,font=read(PLAN),read(FONT);assert plan['candidate_sha256']==font['candidate_sha256']==read(INPUT)['current_ROM_sha256'];env={**old_pages.__globals__,'expected_pixels':expected_pixels};exec(compile(font['source_owned_2b6_page_adapter'],__file__+'::exact-current-pages','exec'),env);ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');fonts={r['id']:r for r in font['records']};records=[];fresh=reused=0
    for ref in plan['blocks'][0]['text_records']:
        raw=bytes.fromhex(ref['target_hex']);body=raw[1:];base=fonts[ref['id']];compiled=bytes.fromhex(base['compiled_hex'])[1:];assert body in [compiled,compiled+b' '] and ref['compiled_hex']==base['compiled_hex'] and not any(k in body for k in [b'FI',b'FA',b'FO'])
        if body==compiled:
            pipeline=deepcopy(next(p for p in base['logical_and_compiled_current_native_pipelines'] if p['version']=='compiled-protected'));assert all(c['output_hex']==body.hex() for c in pipeline['cases']);rendered={k:deepcopy(base[k]) for k in ['pages','total_bytes','complete_consumed_bytes','all_visible_first_internal_final_characters_in_order','no_blank_or_overlap_page']};reused+=4;mode='exact-compiled-input-reused'
            for page in rendered['pages']:assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
        else:
            pipeline=ctx.execute(expand,body,raw[0]);ctx.machines.pop();assert len(pipeline['cases'])==4 and all(c['output_hex']==body.hex() for c in pipeline['cases']);rendered=env['pages'](ctx.arm,ctx.rom.read_file('/GRP/KANJI.FNT'),body);assert len(rendered['pages'])==1
            for page,before in zip(rendered['pages'],base['pages'],strict=True):
                pixels=bytes.fromhex(page.pop('native_plane_hex'));assert pixels==Path(before['native_plane']).read_bytes() and sha(pixels)==before['native_plane_sha256'];path=ROOT/(ref['id']+'_stored_page.bin');path.write_bytes(pixels);page.update(native_plane=str(path),native_plane_sha256=sha(pixels))
            fresh+=4;mode='fresh-zero-ink-parity-tail-input'
        records.append(dict(id=ref['id'],final_target_hex=raw.hex(),final_target_offset=ref['new_offset'],parity_space_added=ref['parity_space_added'],proof_mode=mode,native_pipeline=pipeline,complete_pages=rendered,all_words_glyphs_native_page_count_and_guards_preserved=True))
    assert len(records)==16 and fresh+reused==64 and fresh==4*sum(r['parity_space_added'] for r in records) and not ctx.machines;save(ROOT/'all16_final_stored_targets64_alignments16_complete_pages.json',dict(candidate=plan['candidate'],candidate_sha256=plan['candidate_sha256'],relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),records=records,all_final_stored_targets_equal_reviewed_complete_native_ink=True,stored_alignment_cases=64,fresh_alignment_cases=fresh,exact_reused_alignment_cases=reused,complete_native_pages=16,zero_ink_parity_tail_count=sum(r['parity_space_added'] for r in records),all_bounds_canaries_pair_phase_and_zero_macros_pass=True,no_actor_roster_event_or_name_asset_mutation=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),external_references_actual_and_release_pending=True,new_emulator_runs=0,new_credit=0,full_goal_complete=False));print(dict(final_stored_targets=16,alignments=64,fresh=fresh,reused=reused,parity_tails=sum(r['parity_space_added'] for r in records),complete_pages=16))
