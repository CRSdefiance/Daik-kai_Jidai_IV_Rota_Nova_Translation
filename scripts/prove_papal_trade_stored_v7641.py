"""Verify all36 stored C strings, zero-ink parity tails and exact complete page reuse."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.draft_papal_trade_prose_v7631 import MANUSCRIPTS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_stored_v7641')
MAP=Path('work/analysis/papal_trade_relocation_v7640/two_archives36_speeches40_commands_exact_predecessor_inverse_RESEARCH.json')
FONT=Path('work/analysis/papal_trade_native_pages_v7634/two_routes36_complete_pages144_fresh_compiled_alignments_exact_logical_andfont_reuse.json')
if __name__=='__main__':
    assert not ROOT.exists();mapping,font=map(read,[MAP,FONT]);assert mapping['candidate_sha256']==font['candidate_sha256']
    page_env={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes}
    exec(compile(font['source_owned_2b6_page_adapter'],__file__+'::exact-original-stored-pages','exec'),page_env)
    ROOT.mkdir(parents=True);groups=[];font_cache={};fresh=reused=fresh_font=0
    for mg,fg in zip(mapping['groups'],font['groups'],strict=True):
        route=mg['route'];doc=read(MANUSCRIPTS[route]);ctx=RouteCurrentContext(doc['current_strict_native_input'],'unused-no-historical-ROM',ROOT/f'route{route}_current_context')
        assert ctx.doc['current_ROM_sha256']==mapping['candidate_sha256']
        env={**expand.__globals__,'EXPECTED_CAPTAIN':route}
        exec(compile(font['source_owned_route_compiled_adapter'],__file__+'::actual-route-stored-input','exec'),env)
        archive=Path(mg['target_archive']).read_bytes();assert sha(archive)==mg['target_archive_sha256'];block=IlnkContainer.parse(archive).blocks[mg['block']];assert sha(block)==mg['research_block_sha256'];rows=[];rf=rr=0
        for ref,base in zip(mg['text_records'],fg['records'],strict=True):
            assert ref['id']==base['id'];raw=bytes.fromhex(ref['target_hex']);body=raw[1:];compiled=bytes.fromhex(base['compiled_hex'])[1:]
            assert body in [compiled,compiled+b' '] and ref['compiled_hex']==base['compiled_hex']
            at=ref['new_offset'];assert block[at:at+len(raw)+1]==raw+b'\0' and block[at-5:at+1].hex()==ref['source_preamble_hex']
            if body==compiled:
                pipeline=deepcopy(base['compiled_native_alignment']);assert len(pipeline['cases'])==4 and all(c['output_hex']==body.hex() for c in pipeline['cases'])
                rendered={k:deepcopy(base[k]) for k in ['pages','total_bytes','complete_consumed_bytes','all_visible_first_internal_final_characters_in_order','no_blank_or_overlap_page']}
                mode='exact-compiled-input-androute-context-proof-reuse';rr+=4
            else:
                pipeline=ctx.execute(env['expand'],body,raw[0]);ctx.machines.pop()
                assert len(pipeline['cases'])==4 and all(c['output_hex']==body.hex() for c in pipeline['cases']);rf+=4
                key=body.hex()
                if key not in font_cache:
                    rendered=page_env['pages'](ctx.arm,ctx.rom.read_file('/GRP/KANJI.FNT'),body);assert len(rendered['pages'])==len(base['pages'])==1
                    for page,before in zip(rendered['pages'],base['pages'],strict=True):
                        pixels=bytes.fromhex(page.pop('native_plane_hex'));assert pixels==Path(before['native_plane']).read_bytes() and sha(pixels)==before['native_plane_sha256']
                        p=ROOT/(ref['id']+'_stored_page'+str(page['page'])+'.bin');p.write_bytes(pixels);page.update(native_plane=str(p),native_plane_sha256=sha(pixels),same_complete_ink_as_reviewed_compiled_page=True)
                    font_cache[key]=deepcopy(rendered);fresh_font+=1
                rendered=deepcopy(font_cache[key]);mode='fresh-actual-route-parity-tail-ABI-with-exact-distinct-font-input-cache'
            for page in rendered['pages']:assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
            rows.append(dict(id=ref['id'],file_path=mg['file_path'],final_target_hex=raw.hex(),final_target_offset=at,final_target_bytes=len(raw),parity_space_added=ref['parity_space_added'],proof_mode=mode,native_pipeline=pipeline,complete_pages=rendered,all_words_glyphs_bounds_guards_consumption_andpage_count_preserved=True))
        assert len(rows)==18 and rf+rr==72 and rf==4*sum(r['parity_space_added'] for r in rows) and not ctx.machines
        fresh+=rf;reused+=rr;groups.append(dict(route=route,route_identity=mg['route_identity'],file_path=mg['file_path'],block=mg['block'],records=rows,fresh_alignment_cases=rf,exact_reused_alignment_cases=rr,stored_alignment_cases=72,complete_native_pages=18,zero_ink_parity_tails=sum(r['parity_space_added'] for r in rows),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes())))
    assert fresh==64 and reused==80 and fresh_font==8
    save(ROOT/'all36_stored_targets144_alignments16_zero_ink_tails36_complete_pages.json',dict(candidate=mapping['candidate'],candidate_sha256=mapping['candidate_sha256'],relocation_map=str(MAP),relocation_map_sha256=sha(MAP.read_bytes()),compiled_native_font_proof=str(FONT),compiled_native_font_proof_sha256=sha(FONT.read_bytes()),groups=groups,stored_alignment_cases=144,fresh_alignment_cases=fresh,exact_reused_alignment_cases=reused,zero_ink_parity_tail_count=16,distinct_fresh_stored_font_renders=fresh_font,second_route_identical_stored_font_reuse=8,all36_final_stored_targets_equal_reviewed_complete_ink=True,all36_original_single_four_row_pages=True,all_bounds_canaries_pairphase_zero_macros_andcomplete_consumption_pass=True,source0_storage_tail_andtarget2_storage_tail_distinct_from_four_byte_end=True,no_ROM_registry_ledger_orname_item_asset_mutation=True,loaders_callers_actual_andregistered_release_pending=True,evidence={str(p):sha(p.read_bytes()) for p in [MAP,FONT,*MANUSCRIPTS.values(),Path(__file__)]},new_credit=0,full_goal_complete=False))
    print('36 stored targets /144 alignments:64 fresh and80 exact route-specific reuse.16 zero-ink tails/eight distinct font renders preserve all36 complete single pages;no ROM/ledger change.')
