"""Check eleven compiler parity tails freshly;reuse thirteen exact viewed bodies andverify relocated two-choice alignment."""
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
ROOT=Path('work/analysis/Rafael_B46_stored_v7939')
RELOCATION=Path('work/analysis/Rafael_B46_relocation_v7938/one_block24_speeches2_choices4_fixups20_cases_exact_full_inverse.json')
NATIVE=Path('work/analysis/Rafael_B46_pages_v7933/24_complete_native_pages96_compiled_alignments12_FE.json')
MANUSCRIPT=Path('translations/rafael_B46_editorial_manuscript_v2.json')
LOGICAL=Path('work/analysis/Rafael_B46_logical_v7931/24_logical_paragraphs96_original_native_alignments12_FE.json')
if __name__=='__main__':
    assert not ROOT.exists();relocation,native,doc,logical=map(read,[RELOCATION,NATIVE,MANUSCRIPT,LOGICAL])
    viewed=read('work/analysis/Rafael_B46_native_review_v7935/24_pages2_choices_full_native_review_individual_wrap_reasons.json')
    assert viewed['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and len(viewed['directly_viewed_sheets'])==5 and all(s['directly_viewed'] for s in viewed['directly_viewed_sheets'])
    assert native['manuscript_sha256']==sha(Path(doc['prior_manuscript']).read_bytes())
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    blockpath=Path(relocation['groups'][0]['target_block']);target=blockpath.read_bytes()
    assert sha(target)==relocation['groups'][0]['target_block_sha256']
    archive=Path(relocation['target_archive']).read_bytes();assert sha(archive)==relocation['target_archive_sha256']
    assert IlnkContainer.parse(archive).blocks[46]==target
    arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
    pe={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes}
    exec(compile(native['source_owned_progressive_page_adapter'],__file__+'::same-current-progressive-page-guards','exec'),pe)
    prog_env=dict(progressive_expand.__globals__);exec(compile(logical['source_owned_progressive_adapter'],__file__+'::same-current-progressive-macros','exec'),prog_env)
    fe_env=dict(FE_expand.__globals__);exec(compile(logical['source_owned_FE_adapter'],__file__+'::same-current-null-actor-FE-macros','exec'),fe_env)
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
        stored=next(r for r in relocation['groups'][0]['text_records'] if r['id']==row['id'])
        raw=bytes.fromhex(stored['target_hex']);compiled=bytes.fromhex(stored['compiled_hex']);at=stored['new_offset']
        assert compiled.hex()==old['compiled_hex'] and raw==compiled+(b' ' if stored['parity_space_added'] else b'')
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
                assert sha(rendered['logical'])==oldpage['native_plane_sha256']
                assert sha(rendered['physical'])==oldpage['physical_plane_sha256']
                assert rendered['complete_return_input_object_canaries_and_native_independent_plane_equal']
                proof=dict(native_alignment=alignment,complete_consumed_bytes=len(expected),
                    full_logical_andphysical_planes_exact_to_viewed=oldpage,
                    native_glyph_events=rendered['events'],original_null_actor_consumer=True)
            else:
                rendered=pe['pages'](arm,font,expected)
                assert len(rendered['pages'])==len(old['pages'])==1 and rendered['complete_consumed_bytes']==len(expected)
                for page,previous in zip(rendered['pages'],old['pages'],strict=True):
                    plane=bytes.fromhex(page.pop('native_plane_hex'))
                    assert sha(plane)==previous['native_plane_sha256']==sha(Path(previous['native_plane']).read_bytes())
                    page.update(viewed_native_plane=previous['native_plane'],viewed_native_plane_sha256=previous['native_plane_sha256'])
                proof=dict(native_alignment=alignment,**rendered)
            fresh.append(row['id'])
        rows.append(dict(id=row['id'],file_path=row['file_path'],block=46,source_selector=row['source_selector'],kind=row['kind'],
            source_reference=row['source_reference'],predecessor_reference=row['current_reference'],
            target_reference=dict(offset=at,bytes=len(raw),header_offset=at-5,record_index=stored['new_record_index']),
            stored_hex=raw.hex(),compiled_hex=compiled.hex(),expanded_stored_hex=expected.hex(),
            compiler_owned_parity_space=stored['parity_space_added'],reused_exact_native_body=raw==compiled,
            complete_native_stored_proof=proof,complete_native_ink_exact_to_directly_viewed_page=True))
        print('STORED_PASS',row['id'],'fresh parity tail' if raw!=compiled else 'exact native reuse',flush=True)
    from scripts.source_locked_derivation_v5118 import checked_text
    from scripts import verify_ship_advice_choice_centering_20261022 as original
    cp=Path('work/analysis/Rafael_B46_choice_planes_v7934/two_labels8_native_style_planes_trimmed_native_width_andthree_returns.json')
    fp=Path('work/analysis/Rafael_B46_menu_flow_v7925/two_choice_native_forwarding_four_relative_sites_accept22_decline7_source_scope.json')
    choice,flow=map(read,[cp,fp]);m=relocation['groups'][0]['choice_commands'][0];start=m['new_offset']
    obj=target[start:start+m['new_length']];assert obj.hex()==m['target_hex']==choice['target_menu_object_hex']
    adapter=checked_text(flow['source_owned_VM_adapter'],{
        'def choice_vm(arm, object_bytes):':'def choice_vm(arm, object_bytes, alignment):',
        "    cpu.mem_write(text - 16, b'\\xA5' * 96)":"    assert alignment in [0,2];text+=alignment\n    cpu.mem_write(text - 16, b'\\xA5' * 96)",
    })
    env=dict(original.__dict__);exec(compile(adapter,__file__+'::aligned-complete-relocated-menu','exec'),env)
    menus=[]
    for alignment in [0,2]:
        result=env['choice_vm'](arm,obj,alignment);assert result==choice['native_target_VM']
        menus.append(dict(object_alignment_mod4=alignment,actual_relocated_menu_alignment=alignment==start%4,native_VM=result,modal_loop_bridged_not_actual_controller_selection=True))
    assert start%4==2 and len(m['label_references'])==2
    for r in m['label_references']:
        at=r['new_offset'];value=bytes.fromhex(r['target_hex'])
        assert target[at:at+len(value)+1]==value+b'\0' and value.decode('ascii')==doc['typed_choice_records'][r['option_index']]['english']
    save(ROOT/'two_stored_menu_labels_exact8_viewed_planes_two_header_alignments.json',dict(
        research_block=str(blockpath),research_block_sha256=sha(target),menu=m,stored_menu_hex=obj.hex(),
        complete_original_VM_provider_geometry_andthree_returns_at_both_even_header_alignments=menus,
        label_font_proof=str(cp),label_font_proof_sha256=sha(cp.read_bytes()),all8_current_target_style_planes_reused_by_exact_label_andwidth=True,
        source_owned_alignment_adapter=adapter,actual_backing_highlights_andcontroller_selection_pending=True,
        new_credit=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [cp,fp,Path(__file__)]},full_goal_complete=False))
    assert len(rows)==24 and len(fresh)==11 and len(reused)==13 and not ctx.machines
    save(ROOT/'all24_stored_bodies44_fresh52_reused_alignments_exact_viewed_planes.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],research_block=str(blockpath),research_block_sha256=sha(target),
        relocation=str(RELOCATION),relocation_sha256=sha(RELOCATION.read_bytes()),native_viewed_proof=str(NATIVE),native_viewed_proof_sha256=sha(NATIVE.read_bytes()),
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),records=rows,
        fresh_parity_tail_records=fresh,exact_native_reused_records=reused,fresh_native_alignment_cases=44,exact_reused_native_alignment_cases=52,
        all24_complete_native_pages_full_first_internal_final_glyphs_bounds_andconsumption_pass=True,
        all24_native_ink_planes_exact_to_already_viewed=True,eleven_parity_tails_create_no_blank_oradditional_page=True,
        all24_complete_six_byte_preambles_andonly_source00_prefix_zeros_preserved=True,
        all12_FE_original_null_actor_zero_macro_logical_andphysical_planes_exact=True,
        FE_current_executed_instruction_addresses=len(FE_executed),FE_current_instruction_andobject_canary_guards_preserved=True,
        historical_FE_geometry_calibration=calibration,
        stored_body_checks_not_actual_scene_transition_wholetrade_mechanics_orrelease=True,
        caller_loader_fullreference_wholecontrol_actual_policy_andregistered_release_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('All24 stored bodies pass:11 parity tails fresh/44 alignments;13 exact bodies reuse52 cases. All viewed planes exact. Menu both-even alignments pass. Actual/caller/loader/release pending.')
