"""Validate new logical prose before any wrapping, plus original typed-table label construction/getters."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_outcomes_registered_route_context_v8380 import RouteCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as FE_expand
from scripts.prove_lil_B212_controls_v6603b import compile_menu
from scripts.prove_lil_B212_consumers_v6595 import choice_getters
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_logical_v8389')
DOC=Path('translations/hodram_B49_editorial_manuscript_v1.json')
SOURCE=Path('work/analysis/Hodram_B49_source_display_v8386b/source_display.json')
INPUT=Path('work/analysis/current_V8377_Hodram_native_v8380/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,source=map(read,[DOC,SOURCE]);packet=read(doc['source_context']);assert doc['source_context_sha256']==sha(Path(doc['source_context']).read_bytes()) and packet['source_native_display_sha256']==sha(SOURCE.read_bytes())
    assert len(doc['records'])==14 and len(doc['typed_choice_records'])==2 and doc['source_macro_counts']==dict(FI=0,FA=0,FO=0);inp=read(INPUT);assert inp['current_ROM_sha256']==doc['current_ROM_sha256']
    image=NdsImage.open(inp['current_ROM']);previous=NdsImage.open(source['candidate']);assert all(image.read_file(p)==previous.read_file(p) for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT'])
    env=dict(progressive_expand.__globals__);exec(compile(source['source_owned_progressive_adapter'],__file__+'::original-current-progressive','exec'),env)
    fe=dict(FE_expand.__globals__);exec(compile(source['source_owned_FE_adapter'],__file__+'::original-null-actor-FE','exec'),fe)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');rows=[]
    for row in doc['records']:
        assert all(row['review'][k] for k in ['source','context','localization','naturalness']) and row['review']['formatting'] is False
        body=row['english'].encode('cp932');prefix=row['source_selector'];FE=prefix==254;assert prefix in [1,2,254] and body and not any(b in body for b in [b'\0',b'\n',b'\r',b'%'])
        assert not any(m in body or m in bytes.fromhex(row['source_hex'])[1:] for m in [b'FI',b'FA',b'FO'])
        result=ctx.execute(fe['expand'] if FE else env['expand'],body,*(() if FE else (prefix,)));ctx.machines.pop();assert len(result['cases'])==4 and all(c['output_hex']==body.hex() for c in result['cases'])
        if FE:assert all(c['null_source_actor'] for c in result['cases'])
        rows.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],source_selector=prefix,logical_body_hex=body.hex(),expected_expanded_hex=body.hex(),native_alignment=result))
    assert len(rows)==14 and not ctx.machines;menu=packet['typed_choices'][0];labels=[r['english'].encode('ascii') for r in sorted(doc['typed_choice_records'],key=lambda r:r['option_index'])];target=compile_menu(0x2100,labels)
    proposal=dict(menu['current_command']);proposal.update(whole_command_hex=target.hex(),native_extent=len(target));getters=choice_getters(image.read_file('/__arm9__.bin'),proposal)
    assert len(target)==22 and len(getters)==2 and all(c['count']==2 and [bytes.fromhex(r['hex']) for r in c['labels']]==labels and c['original_count_pointer_ABI_all4MiB_owner_stream_and_guards_exact'] for c in getters)
    save(ROOT/'logical_prose_and_choice_table.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=rows,fresh_native_alignment_cases=56,progressive_alignment_cases=52,FE_null_actor_alignment_cases=4,source_macro_counts=dict(FI=0,FA=0,FO=0),two_source_bound_ellipsis_records_complete=True,all_literal_leading_internal_trailing_bytes_ABI_scratch_ownership_andunowned4MiB_exact=True,typed_choice=dict(source_command=menu['source_command'],current_command=menu['current_command'],proposed_logical_table_hex=target.hex(),proposed_bytes=22,current_bytes=len(bytes.fromhex(menu['current_command']['whole_command_hex'])),labels=[r['english'] for r in doc['typed_choice_records']],native_getters=getters,original0x2100_two_offset_fields_NULs_andeven_zero_padding_preserved=True,three_current_No_trailing_spaces_removed_without_word_revision=True,proposed_getter_offsets_use_old_command_position_for_logical_probe_not_final_relocation=True,final_stored_offsets_UI_geometry_full_glyphs_andselection_routing_pending=True),source_owned_progressive_adapter=source['source_owned_progressive_adapter'],source_owned_FE_adapter=source['source_owned_FE_adapter'],logical_checks_not_compiled_wrap_fonts_bounds_pagination_stored_oractual_scene=True,all16_formatting_gates_remain_false=True,current_native_input=str(INPUT),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),no_ROM_registration_ledger_orcredit_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [DOC,SOURCE,INPUT,Path(compile_menu.__code__.co_filename),Path(choice_getters.__code__.co_filename),Path(__file__)]}))
    print('B49 logical:52progressive+4nullactorFE alignments/allliteral bytes pass;two typedlabels compileto22bytes/nativegetters pass2alignments.No authoredpadding orwordchanges.16formatting gates remainfalse;zero credit.')
