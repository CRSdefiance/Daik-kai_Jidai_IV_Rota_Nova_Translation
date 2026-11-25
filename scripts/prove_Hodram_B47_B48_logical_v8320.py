"""Guard all six logical English bodies through original progressive/null-actor FE macro wrappers."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_registered_route_context_v8303 import RouteCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as FE_expand
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B47_B48_logical_v8320')
DOC=Path('translations/hodram_B47_B48_editorial_manuscript_v1.json')
SOURCE=Path('work/analysis/Hodram_B47_B48_source_display_v8316b/six_source_dispatches24_macro_alignments_five_progressive_one_FE_pages_Lil_identity_reuse.json')
INPUT=Path('work/analysis/current_V8300_Hodram_native_v8303/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,source=map(read,[DOC,SOURCE]);assert doc['source_display_proof_sha256']==sha(SOURCE.read_bytes()) and len(doc['records'])==6
    env=dict(progressive_expand.__globals__);exec(compile(source['source_owned_progressive_adapter'],__file__+'::unchanged-captain1-progressive','exec'),env)
    fe=dict(FE_expand.__globals__);exec(compile(source['source_owned_FE_adapter'],__file__+'::unchanged-null-actor-FE','exec'),fe)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');rows=[]
    for row in doc['records']:
        assert all(row['review'][k] for k in ['source','context','localization','naturalness']) and not row['review']['formatting']
        body=row['english'].replace('{MACRO:FI}','FI').encode('cp932');prefix=row['source_selector'];is_FE=prefix==254
        assert prefix in [2,254] and body and not any(v in body for v in [b'\0',b'\n',b'\r',b'%'])
        sourcebody=bytes.fromhex(row['source_hex'])[1:];assert body.count(b'FI')==sourcebody.count(b'FI') and not any(m in body for m in [b'FA',b'FO'])
        result=ctx.execute(fe['expand'] if is_FE else env['expand'],body,*(() if is_FE else (prefix,)));ctx.machines.pop()
        expected=body.replace(b'FI',b'Hodram');assert len(result['cases'])==4 and all(c['output_hex']==expected.hex() for c in result['cases'])
        if is_FE:assert all(c['null_source_actor'] for c in result['cases'])
        rows.append(dict(id=row['id'],file_path=row['file_path'],source_reference=row['source_reference'],current_reference=row['current_reference'],source_selector=prefix,kind=row['kind'],logical_body_hex=body.hex(),expected_expanded_hex=expected.hex(),native_alignment=result))
    assert len(rows)==6 and not ctx.machines
    save(ROOT/'six_logical_paragraphs24_guarded_alignments_distinct_FE_one_FI.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=rows,fresh_native_alignment_cases=24,progressive_alignment_cases=20,FE_null_actor_alignment_cases=4,
        source_macro_counts=dict(FI=1,FA=0,FO=0),measured_default_FI6_FA9_FO15=True,all_literal_leading_internal_trailing_bytes_runtime_substitution_ABI_scratch_ownership_andunowned4MiB_exact=True,
        original_FE24310_null_actor_not_fallback208_orstatic254=True,source_owned_progressive_adapter=source['source_owned_progressive_adapter'],source_owned_FE_adapter=source['source_owned_FE_adapter'],
        logical_byte_checks_not_compiled_wrap_fonts_bounds_pagination_stored_oractual_scene=True,all_six_formatting_gates_remain_false=True,
        custom_player_names_native_effects_FE_scene_geometry_transition_policy_andregistered_release_pending=True,current_native_input=str(INPUT),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [DOC,SOURCE,INPUT,Path(__file__)]}))
    print('Six logical English paragraphs:20progressive+4nullactorFE guarded alignments/one real FI;all literal bytes andfull4MiB/ABI/scratch guards pass.Formatting/actual/release pending.')
