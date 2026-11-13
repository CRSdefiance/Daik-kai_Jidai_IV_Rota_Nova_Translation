"""Reuse exact B52 source/stored speech and scoped-name planes for actual capture auditing."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_model_tools_v8650');assert not root.exists()
    result=derive('scripts/model_Hodram_B51_actual_v8575.py','scripts/model_Hodram_B52_actual_v8650.py',{
        'Hodram_B51_models_v8575':'Hodram_B52_models_v8650','Hodram_B51_source_display_v8556':'Hodram_B52_source_display_v8626','Hodram_B51_stored_v8566':'Hodram_B52_stored_v8643','Hodram_B51_pages_v8563':'Hodram_B52_pages_v8635','Hodram_B51_fixtures_v8573':'Hodram_B52_fixtures_v8648',
        "'block': 51":"'block': 52",'len(rows) == 5':'len(rows) == 3',"row['source_selector'] in [1, 16, 18, 113]":"row['source_selector'] in [113]",
        'scoped_clean_current_four_names_andreused_native_consumers':'scoped_clean_current_one_name_andreused_native_consumers',"{row['actor_ID'] for row in names} == {1, 16, 18, 113}":"{row['actor_ID'] for row in names} == {113}",
        'source_original5_andreviewed_stored5_planes_reused_by_exact_hash':'source_original3_andreviewed_stored3_planes_reused_by_exact_hash','four_current_nameplanes_reused_by_exact_code_font_wholeactor_binding':'one_current_nameplane_reused_by_exact_code_font_wholeactor_binding',
        'Bind already verified B51 source/stored pages and four names':'Bind already verified B52 source/stored pages and one scoped name',
        'B51 actual models: five Japanese/five stored body planes and four nameplanes':'B52 actual models: three Japanese/three stored body planes and one nameplane',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,all_native_planes_andwhole_current_code_font_actor_andfixture_hash_bindings_preserved=True,no_completed_native_probe_replay_andno_actual_coverage_credit=True,new_credit=0,full_goal_complete=False))
