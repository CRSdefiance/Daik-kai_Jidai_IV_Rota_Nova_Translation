"""Fresh captain3 name literal ABI cases, with exact established native font-plane reuse."""
import inspect
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_name_inputs_v7685')
CURRENT=Path('work/analysis/maria_B207_consumers_v7682/all18_effective_Maria_bodies36_dispatches_four_getters_two_voices.json')
PRIOR=Path('work/analysis/lil_B234_name_planes_v7579/two_actors_four_getters_five_literal_planes20_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();current,prior=map(read,[CURRENT,PRIOR]);old,now=[NdsImage.open(p) for p in [prior['candidate'],current['candidate']]]
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256'] and sha(Path(current['candidate']).read_bytes())==current['candidate_sha256']
    for path in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:assert old.read_file(path)==now.read_file(path)
    assert len(prior['name_planes'])==5 and current['source_name_fields']==prior['source_fields']
    adapter=checked_text(inspect.getsource(expand),{'assert identity==prefix and captain==2':'assert identity==prefix and captain==EXPECTED_CAPTAIN==3'})
    env={**expand.__globals__,'EXPECTED_CAPTAIN':3};exec(compile(adapter,__file__+'::actual-Maria-name-literals','exec'),env)
    inp=Path(current['current_strict_native_input']);assert sha(inp.read_bytes())==current['current_strict_native_input_sha256']
    ROOT.mkdir(parents=True);ctx=MariaUnlockedCurrentContext(inp,'unused-no-historical-ROM',ROOT/'current_context');planes=[]
    for previous in prior['name_planes']:
        text=previous['text'];actor=previous['actor_for_literal_pipeline'];raw=text.encode('ascii');assert actor in [19,104]
        native=ctx.execute(env['expand'],raw,actor);ctx.machines.pop();assert len(native['cases'])==4 and all(c['output_hex']==raw.hex() for c in native['cases'])
        assert sha(Path(previous['native_plane']).read_bytes())==previous['native_plane_sha256'] and sha(Path(previous['preview']).read_bytes())==previous['preview_sha256']
        plane=deepcopy(previous);plane['historical_captain2_alignment_proof']=plane.pop('native_alignment')
        plane.update(native_alignment=native,proof_mode='fresh-actual-Maria3-literal-ABI-with-exact-native-font-plane-reuse',fresh_name_font_renderer_executions=0,actual_optional_headers_andcatalogue_UI_unvisited=True);planes.append(plane)
    assert not ctx.machines and sum(len(p['native_alignment']['cases']) for p in planes)==20
    save(ROOT/'Maria20_fresh_literal_alignments_five_exact_reused_font_planes.json',dict(candidate=current['candidate'],candidate_sha256=current['candidate_sha256'],consumer_proof=str(CURRENT),consumer_proof_sha256=sha(CURRENT.read_bytes()),previous_complete_native_font_proof=str(PRIOR),previous_complete_native_font_proof_sha256=sha(PRIOR.read_bytes()),name_planes=planes,source_owned_name_literal_adapter=adapter,actual_captain_ID=3,fresh_native_literal_alignment_cases=20,distinct_exact_reused_native_font_planes=5,fresh_name_font_renderer_executions=0,all_first_internal_final_glyphs_zero_ink_flushes_andbounds_reused_by_exact_inputs=True,regional_European_excluded_from_getters_not_surname_or_nationality_approval=True,no_global_macro_I_font_geometry_orold_captain2_guard_change=True,actual_optional_headers_andcatalogue_UI_unvisited=True,name_localization_andfull207_review_not_approved_by_font_proof=True,existing_system_only_unlock_fixture=True,earned_unlock_verified=False,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,PRIOR,Path(expand.__code__.co_filename),Path(__file__)]},full_goal_complete=False))
    print('Maria3:20 fresh name-literal ABI cases;five exact native font planes reused. No optional header orcatalogue UI claim.')
