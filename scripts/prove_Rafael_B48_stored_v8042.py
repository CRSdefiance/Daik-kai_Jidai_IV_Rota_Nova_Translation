"""Fresh48 compiler parity-tail checks;reuse43 exact bodies across progressive andFE consumers."""
from copy import deepcopy
from pathlib import Path
from types import FunctionType,SimpleNamespace
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as FE_expand
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels,make_painter
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B48_stored_v8042')
RELOCATION=Path('work/analysis/Rafael_B48_relocation_v8041/one_block91_speeches28_relative_fixups140_cases_exact_full_inverse.json')
NATIVE=Path('work/analysis/Rafael_B48_pages_refined_v8038/91_final_native_paragraphs92_pages4_fresh360_reused_alignments.json')
VIEW=Path('work/analysis/Rafael_B48_native_review_v8040/91_paragraphs92_native_pages9_names_two_scoped_warnings37_infos_wrap_review.json')
DOC=Path('translations/rafael_B48_editorial_manuscript_v3.json')
LOGICAL=Path('work/analysis/Rafael_B48_logical_v8032/91_logical_paragraphs364_original_native_alignments4_FE.json')
if __name__=='__main__':
    assert not ROOT.exists()
    relocation,native,view,doc,logical=map(read,[RELOCATION,NATIVE,VIEW,DOC,LOGICAL])
    assert view['manuscript_sha256']==sha(DOC.read_bytes()) and len(view['directly_viewed_sheets'])==17 and all(s['directly_viewed'] for s in view['directly_viewed_sheets'])
    assert native['manuscript_sha256']==sha(Path(doc['prior_manuscript']).read_bytes())
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    group=relocation['groups'][0];blockpath=Path(group['target_block']);target=blockpath.read_bytes()
    assert sha(target)==group['target_block_sha256'] and len(target)==group['target_logical_end']==4948
    archive=Path(relocation['target_archive']).read_bytes()
    assert sha(archive)==relocation['target_archive_sha256'] and IlnkContainer.parse(archive).blocks[48]==target
    arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
    pe={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes}
    exec(compile(native['source_owned_progressive_page_adapter'],__file__+'::original-native-pages','exec'),pe)
    prog_env=dict(progressive_expand.__globals__);exec(compile(logical['source_owned_progressive_adapter'],__file__+'::original-progressive-macros','exec'),prog_env)
    fe_env=dict(FE_expand.__globals__);exec(compile(logical['source_owned_FE_adapter'],__file__+'::original-null-actor-FE','exec'),fe_env)
    paint,calibration=make_painter(image);cold_original=paint.__globals__['cold_machine']
    sections=MainCodeFile(arm,BASE).sections;payload=bytes(sections[3].data[:-48]);assert len(payload)==123264
    executable_sections=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)];FE_executed=set()
    def guarded_cold(current_arm):
        assert current_arm==arm
        cpu=cold_original(current_arm)
        def exact(u,pc,size,unused):
            owners=[s for s in executable_sections if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)]
            assert len(owners)==1,hex(pc)
            section=owners[0];at=pc-section.ramAddress
            assert bytes(u.mem_read(pc,size))==bytes(section.data[at:at+size]),hex(pc)
            FE_executed.add(pc)
        cpu.hook_add(UC_HOOK_CODE,exact);return cpu
    paint=FunctionType(paint.__code__,{**paint.__globals__,'cold_machine':guarded_cold},argdefs=paint.__defaults__,closure=paint.__closure__)
    names=read(logical['names_proof']);ROOT.mkdir(parents=True)
    ctx=RouteCurrentContext(names['current_native_input'],'unused-no-historical-ROM',ROOT/'current_context')
    rows=[];fresh=[];reused=[]
    for row in doc['records']:
        old=next(r for r in native['records'] if r['id']==row['id'])
        stored=next(r for r in group['text_records'] if r['id']==row['id'])
        raw=bytes.fromhex(stored['target_hex']);compiled=bytes.fromhex(stored['compiled_hex']);at=stored['new_offset']
        assert compiled.hex()==old['compiled_hex']==row['compiled_hex'] and raw==compiled+(b' ' if stored['parity_space_added'] else b'')
        assert raw[0]==row['source_selector'] and b'\0' not in raw[1:] and target[at:at+len(raw)+1]==raw+b'\0'
        assert target[at-5:at+1].hex()==row['source_complete_preamble_hex']
        expected=raw[1:].replace(b'FI',b'Rafael').replace(b'FA',b'Castor').replace(b'FO',b'Castor Co.')
        if raw==compiled:
            assert expected.hex()==old['expanded_native_hex']
            proof=deepcopy(old);reused.append(row['id'])
        else:
            is_FE=raw[0]==254;body=raw[1:]
            alignment=ctx.execute(fe_env['expand'] if is_FE else prog_env['expand'],body,*(() if is_FE else (raw[0],)));ctx.machines.pop()
            assert len(alignment['cases'])==4 and all(r['output_hex']==expected.hex() for r in alignment['cases'])
            if is_FE:
                assert all(r['null_source_actor'] for r in alignment['cases'])
                rendered=paint(expected);oldpage=old['pages'][0]
                assert sha(rendered['logical'])==oldpage['native_plane_sha256'] and sha(rendered['physical'])==oldpage['physical_plane_sha256']
                assert rendered['complete_return_input_object_canaries_and_native_independent_plane_equal']
                pages=deepcopy(old['pages']);pages[0].update(end=len(expected),events=rendered['events'])
                proof=dict(native_alignment=alignment,complete_consumed_bytes=len(expected),pages=pages,
                    full_logical_andphysical_planes_exact_to_viewed=oldpage,native_glyph_events=rendered['events'],
                    original_null_actor_consumer=True,logical_geometry=[228,48],physical_geometry=[228,64])
            else:
                rendered=pe['pages'](arm,font,expected)
                assert len(rendered['pages'])==len(old['pages'])==row['native_page_count'] and rendered['complete_consumed_bytes']==len(expected)
                for page,previous in zip(rendered['pages'],old['pages'],strict=True):
                    plane=bytes.fromhex(page.pop('native_plane_hex'))
                    assert sha(plane)==previous['native_plane_sha256']==sha(Path(previous['native_plane']).read_bytes())
                    page.update(viewed_native_plane=previous['native_plane'],viewed_native_plane_sha256=previous['native_plane_sha256'])
                proof=dict(native_alignment=alignment,**rendered)
            fresh.append(row['id'])
        assert len(proof['pages'])==(2 if row['source_record_index']==347 else 1)
        rows.append(dict(id=row['id'],file_path=row['file_path'],block=48,source_selector=row['source_selector'],kind=row['kind'],
            source_reference=row['source_reference'],predecessor_reference=row['current_reference'],
            target_reference=dict(offset=at,bytes=len(raw),header_offset=at-5,record_index=stored['new_record_index']),
            stored_hex=raw.hex(),compiled_hex=compiled.hex(),expanded_stored_hex=expected.hex(),
            compiler_owned_parity_space=stored['parity_space_added'],reused_exact_native_body=raw==compiled,
            complete_native_stored_proof=proof,complete_native_ink_exact_to_directly_viewed_pages=True))
        print('STORED_PASS',row['id'],'fresh parity tail' if raw!=compiled else 'exact native reuse',flush=True)
    assert len(rows)==91 and len(fresh)==48 and len(reused)==43 and not ctx.machines
    assert sum(len(r['complete_native_stored_proof']['pages']) for r in rows)==92
    save(ROOT/'all91_stored_bodies192_fresh172_reused_alignments92_exact_viewed_pages.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],research_block=str(blockpath),research_block_sha256=sha(target),
        relocation=str(RELOCATION),relocation_sha256=sha(RELOCATION.read_bytes()),
        native_viewed_proof=str(NATIVE),native_viewed_proof_sha256=sha(NATIVE.read_bytes()),
        native_review=str(VIEW),native_review_sha256=sha(VIEW.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        records=rows,fresh_parity_tail_records=fresh,exact_native_reused_records=reused,
        fresh_native_alignment_cases=192,exact_reused_native_alignment_cases=172,total_bound_alignment_cases=364,
        all91_complete_native_paragraphs92_pages_full_first_internal_final_glyphs_bounds_consumption_pass=True,
        all91_native_ink_planes_exact_to_already_viewed=True,
        all48_parity_tails_no_blank_oradditional_page_andfour_FE_physical_planes_exact=True,
        R347_both_complete_stored_pages_exact_to_viewed=True,R140_tag_kept_together=True,
        all91_complete_sixbyte_preambles_source00_4B71_andone_FI_preserved=True,
        two_exact_QA_warnings_narrow_exceptions_and37_infos_unchanged=True,
        FE_current_executed_instruction_addresses=len(FE_executed),all_FE_current_sections_and123264_payload_exact=True,
        stored_checks_not_actual_scene_page_transition_orrelease=True,
        final_dispatch_predicates_queries_fullreference_callers_loaders_actual_policy_atomic_andrelease_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(Path(p).read_bytes()) for p in [RELOCATION,NATIVE,VIEW,DOC,LOGICAL,Path(__file__)]},
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('91stored bodies/92pages pass:192fresh parity-tail/172exactreused alignments.All17viewed sheets retain exactink;no extra page.Actual/control/reference/release pending.')
