"""Five reviewed surname paragraphs through the original Lil macro consumer."""
import inspect
from pathlib import Path
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.Lil_current_route_context_v8198 import RouteCurrentContext
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Gerhard_logical_v8204')
MANUSCRIPT=Path('translations/gerhard_surname_consistency_manuscript_v1.json')
NAMES=Path('work/analysis/Gerhard_before_names_v8200/four_identities8_getters3_source_voices16_synthetic_Lil_alignments.json')

if __name__=='__main__':
    assert not ROOT.exists();doc,names=map(read,[MANUSCRIPT,NAMES])
    inp=Path(names['current_native_input']);assert sha(inp.read_bytes())==names['current_native_input_sha256']
    assert names['measured_default_macro_lengths']==dict(FI=3,FA=5,FO=9)
    assert doc['native_names_sha256']==sha(NAMES.read_bytes()) and len(doc['records'])==5
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(inp,'unused-no-historical-ROM',ROOT/'current_context');rows=[]
    totals=dict(FI=0,FA=0,FO=0)
    for row in doc['records']:
        assert all(row['review'][k] for k in ['source','context','localization','naturalness']) and not row['review']['formatting']
        assert row['already_editorially_completed'] and row['previous_credit_classification']=='revised-and-integrated'
        body=row['english'].replace('{MACRO:FI}','FI').replace('{MACRO:FA}','FA').replace('{MACRO:FO}','FO').encode('ascii')
        prefix=row['source_selector'];assert prefix in [1,9,16] and row['kind']=='progressive'
        assert not any(v in body for v in [b'\n',b'\r',b'\0',b'%'])
        for token in totals:totals[token]+=body.count(token.encode())
        result=ctx.execute(expand,body,prefix);ctx.machines.pop()
        expected=body.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
        assert len(result['cases'])==4 and all(c['output_hex']==expected.hex() for c in result['cases'])
        rows.append(dict(id=row['id'],file_path=row['file_path'],block=row['block'],source_selector=prefix,kind=row['kind'],
            logical_body_hex=body.hex(),expected_expanded_hex=expected.hex(),native_alignment=result,
            all_literal_first_internal_final_bytes_preserved_before_font_render=True))
    assert totals==dict(FI=1,FA=0,FO=0) and len(rows)==5 and not ctx.machines
    save(ROOT/'5_logical_paragraphs20_original_native_alignments.json',dict(
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),names_proof=str(NAMES),names_proof_sha256=sha(NAMES.read_bytes()),
        records=rows,fresh_native_alignment_cases=20,total_bound_alignment_cases=20,progressive_alignment_cases=20,FE_null_actor_alignment_cases=0,
        source_owned_progressive_adapter=inspect.getsource(expand),original_captain=2,measured_default_macro_lengths=dict(FI=3,FA=5,FO=9),source_macro_totals=totals,
        all_native_ABI_input_output_canaries_scratch_ownership_andunowned4MiB_exact=True,
        logical_byte_checks_not_wrapped_fonts_bounds_pagination_stored_oractual_scene=True,
        no_custom_player_name_ornew_source_macro_coverage_claim=True,ordinary_captain2_context_no_state_fixture=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        no_new_source_prose_completed_revised_orretained_credit=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [MANUSCRIPT,NAMES,Path(__file__)]},full_goal_complete=False))
    print('5 logical paragraphs /20 original Lil alignments pass;FI1/FA0/FO0;no coverage credit.')
