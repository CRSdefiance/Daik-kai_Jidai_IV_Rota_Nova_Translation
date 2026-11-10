"""Preserve raw paired differences and correct a focus-sheet label to its exact observed ID."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/measure_Rafael_B47_waits_v8001.py','scripts/measure_Rafael_B48_waits_v8056.py',{
        'B47':'B48','R53':'R347','Rafael_B47_waits_v8001':'Rafael_B48_waits_v8056',
        'Rafael_B47_actual_v7999':'Rafael_B48_actual_v8053',
        'Rafael_B47_actual_comparison_v8000/11_scene':'Rafael_B48_actual_comparison_v8054/78_scene',
        'all_routes_combined_v7964':'all_routes_combined_v8013',
        'rafael_B47_editorial_manuscript_v2':'rafael_B48_editorial_manuscript_v3',
        "s['source_record_index']==53":"s['source_record_index']==347",
        'actual_later_models_persistent_objects_actors_calendar_andall_sampled_RGB_differ':'actual_later_persistent_objects_actors_andall_sampled_RGB_differ_models_state_tasks_calendar_equal',
    }))
    print(derive('scripts/render_Rafael_B48_actual_focus_v8055.py','scripts/render_Rafael_B48_actual_focus_v8055b.py',{
        'Rafael_B48_actual_focus_v8055':'Rafael_B48_actual_focus_v8055b','EN following R351':'EN following R350',
    }))
