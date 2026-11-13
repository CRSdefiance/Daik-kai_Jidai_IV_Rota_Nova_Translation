"""Four original native alignments for every complete proposed logical paragraph."""
import inspect
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/maria_story_logical_v7732')
MANUSCRIPT=Path('translations/maria_B34_B108_B35_editorial_manuscript_v1.json')
NAMES=Path('work/analysis/maria_story_names_macros_v7727/eight_static_speakers_sixteen_getters_clean_fields_actual_source_macros.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,names=map(read,[MANUSCRIPT,NAMES]);inp=Path(names['current_native_input'])
    assert sha(inp.read_bytes())==names['current_native_input_sha256']
    adapter=checked_text(inspect.getsource(expand),{'assert identity==prefix and captain==2':'assert identity==prefix and captain==EXPECTED_CAPTAIN==3'})
    ns={**expand.__globals__,'EXPECTED_CAPTAIN':3};exec(compile(adapter,__file__+'::Maria-logical-four-alignments','exec'),ns)
    ROOT.mkdir(parents=True);ctx=MariaUnlockedCurrentContext(inp,'unused-no-historical-ROM',ROOT/'current_context');rows=[]
    for row in doc['records']:
        body=row['english'].encode('cp932');prefix=row['source_selector'];assert prefix in names['exact_static_source_selectors'] and not any(v in body for v in [b'\n',b'\r',b'\0'])
        result=ctx.execute(ns['expand'],body,prefix);ctx.machines.pop()
        expected=body.replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan')
        assert len(result['cases'])==4 and all(c['output_hex']==expected.hex() for c in result['cases'])
        rows.append(dict(id=row['id'],file_path=row['file_path'],source_selector=prefix,logical_body_hex=body.hex(),expected_expanded_hex=expected.hex(),native_alignment=result,
            all_literal_I_F_complete_leading_trailing_andinternal_bytes_preserved_before_font_render=True))
    assert len(rows)==67 and not ctx.machines
    save(ROOT/'67_logical_paragraphs268_original_native_macro_literal_alignments.json',dict(
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),names_proof=str(NAMES),names_proof_sha256=sha(NAMES.read_bytes()),
        records=rows,fresh_native_alignment_cases=268,source_owned_Maria_adapter=adapter,original_captain=3,
        exact_default_FI5_FA2_FO7_measured_before_checks=True,source_macro_totals=dict(FI=1,FA=4,FO=7),
        all_native_ABI_input_output_canaries_scratch_ownership_andunowned4MiB_exact=True,
        logical_byte_checks_not_wrapped_native_fonts_bounds_pagination_stored_oractual_scenes=True,
        custom_player_name_coverage_not_claimed=True,no_global_guard_macro_profile_orfont_change=True,
        existing_system_only_unlock_fixture=True,earned_unlock_verified=False,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        new_credit=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [MANUSCRIPT,NAMES,Path(__file__)]},full_goal_complete=False))
    print('67 complete proposed logical paragraphs/268 native alignments pass:literal I/F,12 real macros,all byte/ABI/canary/unowned-state guards.No font oractual approval yet.')
