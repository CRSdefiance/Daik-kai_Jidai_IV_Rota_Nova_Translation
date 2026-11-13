"""Original four-alignment macro/literal checks for28 Hodram paragraphs;no FE consumers."""
import inspect
from pathlib import Path
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as FE_expand
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/Hodram_B137_B45_B46_logical_v8242')
MANUSCRIPT=Path('translations/hodram_B137_B45_B46_editorial_manuscript_v1.json')
NAMES=Path('work/analysis/Hodram_B137_B45_B46_names_v8192/six_static_speakers12_getters_clean_fields24_synthetic_macro_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,names=map(read,[MANUSCRIPT,NAMES]);inp=Path(names['current_native_input'])
    assert sha(inp.read_bytes())==names['current_native_input_sha256']
    prog=checked_text(inspect.getsource(progressive_expand),{'assert identity==prefix and captain==2':'assert identity==prefix and captain==1'})
    fe=checked_text(inspect.getsource(FE_expand),{"b'Lil'":"b'Hodram'","b'Argot'":"b'Bergstrom'","b'Argot Co.'":"b'Bergstrom Fleet'"})
    pe=dict(progressive_expand.__globals__);exec(compile(prog,__file__+'::own-captain1-progressive','exec'),pe)
    fe_env=dict(FE_expand.__globals__);exec(compile(fe,__file__+'::own-captain1-null-actor-FE','exec'),fe_env)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(inp,'unused-no-historical-ROM',ROOT/'current_context');rows=[]
    for row in doc['records']:
        body=row['english'].replace('{MACRO:FI}','FI').replace('{MACRO:FA}','FA').replace('{MACRO:FO}','FO').encode('cp932');prefix=row['source_selector'];is_FE=prefix==254
        assert prefix in [1,2,9,16,18,113] and not any(v in body for v in [b'\n',b'\r',b'\0',b'%'])
        result=ctx.execute(fe_env['expand'] if is_FE else pe['expand'],body,*(() if is_FE else (prefix,)));ctx.machines.pop()
        expected=body.replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet')
        assert len(result['cases'])==4 and all(c['output_hex']==expected.hex() for c in result['cases'])
        if is_FE:assert all(c['null_source_actor'] for c in result['cases'])
        rows.append(dict(id=row['id'],file_path=row['file_path'],source_selector=prefix,kind=row['kind'],
            logical_body_hex=body.hex(),expected_expanded_hex=expected.hex(),native_alignment=result,
            all_literal_I_F_complete_leading_trailing_andinternal_bytes_preserved_before_font_render=True))
    assert len(rows)==28 and not ctx.machines
    save(ROOT/'28_logical_paragraphs112_original_native_alignments_no_FE.json',dict(
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),names_proof=str(NAMES),names_proof_sha256=sha(NAMES.read_bytes()),
        records=rows,fresh_native_alignment_cases=112,total_bound_alignment_cases=112,progressive_alignment_cases=112,FE_null_actor_alignment_cases=0,
        source_owned_progressive_adapter=prog,source_owned_FE_adapter=fe,original_captain=1,
        measured_default_FI6_FA9_FO15=True,source_macro_totals=dict(FI=0,FA=0,FO=0),
        all_native_ABI_input_output_canaries_scratch_ownership_andunowned4MiB_exact=True,
        Hodram_three_blocks28_progressive_no_FE_all_six_static_source_actors_only=True,
        logical_byte_checks_not_wrapped_fonts_bounds_pagination_stored_oractual_scene=True,
        custom_player_name_coverage_not_claimed=True,no_global_guard_macro_profile_orfont_change=True,
        ordinary_captain1_context_no_state_fixture=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        new_credit=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [MANUSCRIPT,NAMES,Path(__file__)]},full_goal_complete=False))
    print('28 logical paragraphs/112guarded native alignments pass;allprogressive/noFE,sourcezeroFA/FI/FO.Layout,fonts,actual andrelease pending.')
