"""Post-format native font pages at validated COMMON bounds; physical pitch stays separate."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

matrix=read('work/analysis/guild_courier_layouts_v2241/all79_current_native_layouts.json');count=len(matrix['representative_full_font_indices'])
source=Path('scripts/verify_tavern_fonts_v2189.py').read_text()
for old,new in(('tavern_fonts_v2189','guild_courier_fonts_v2242'),('tavern_layouts_v2188/all63_current_native_layouts.json','guild_courier_layouts_v2241/all79_current_native_layouts.json'),("matrix['case_count']==67454","matrix['case_count']==2823"),('len(fonts)==310',f'len(fonts)=={count}'),('set(range(820,883))','set([346,347,348,*range(1070,1146)])'),('all63','all79'),('all67454','all2823'),('all310',f'all{count}')):
    assert old in source,old
    source=source.replace(old,new)
env={'__name__':'__main__','__file__':__file__};exec(compile(source,__file__,'exec'),env)
save(env['ROOT']/'font_scope.json',dict(matrix_kind='2774 original progressive cases plus49 separately formatted original modal cases',shared_postformat_font_core_geometry=[228,48],metrics=[6,12],source_font_fixture_is_current_observed655_not_a_claimed_courier_callback=True,modal_control_and_printf_proof_separate='work/analysis/courier_context_v2238b/consumer_proof.json',current_modal49_layouts_and12_wrong_parent_controls_separate=True,physical228x64_pitch16_oracle_not_logical_capacity=True,actual_modal_pixel_evidence_must_remain_labeled_historical_until_new_capture=True,no_modal_SDK_widget_or_GPU_menu_simulation_claim=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
