"""All54 current native pages at unchanged logical bounds and physical oracle."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
matrix=read('work/analysis/palace_inn_layouts_v2255/all54_current_native_layouts.json');count=len(matrix['representative_full_font_indices']);source=Path('scripts/verify_tavern_fonts_v2189.py').read_text()
for old,new in(('tavern_fonts_v2189','palace_inn_fonts_v2256'),('tavern_layouts_v2188/all63_current_native_layouts.json','palace_inn_layouts_v2255/all54_current_native_layouts.json'),("matrix['case_count']==67454","matrix['case_count']==1492"),('len(fonts)==310',f'len(fonts)=={count}'),('set(range(820,883))','set(range(1146,1200))'),('all63','all54'),('all67454','all1492'),('all310',f'all{count}')):
    assert old in source;source=source.replace(old,new)
env={'__name__':'__main__','__file__':__file__};exec(compile(source,__file__,'exec'),env)
save(env['ROOT']/'font_scope.json',dict(matrix_kind='1492 original progressive Palace/Inn/Strategist cases',shared_postformat_font_core_geometry=[228,48],metrics=[6,12],source_fixture_current_observed655_not_actual_Inn_or_Palace_callback=True,physical228x64_pitch16_oracle_not_logical_capacity=True,actual_current_Inn_font_continuations_separate='work/analysis/inn_actual_continuations_v2257/actual_snapshot_native_font_continuations.json',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
