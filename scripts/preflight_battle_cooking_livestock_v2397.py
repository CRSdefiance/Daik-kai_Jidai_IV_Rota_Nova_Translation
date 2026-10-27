"""Next25 registered source/compiler preflight;no editorial credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/preflight_livestock_prayer_v2325.py')
if __name__=='__main__':
 source=OLD.read_text();changes={'scripts.livestock_prayer_layout_v854':'scripts.battle_cooking_livestock_layout_v908','livestock_prayer_preflight_v2325':'battle_cooking_livestock_preflight_v2397','livestock_prayer_context_source_v2324/all24':'battle_cooking_livestock_context_source_v2396/all25','livestock_prayer_editorial':'battle_cooking_livestock_editorial','range(1423,1447)':'range(1620,1645)','==1447':'==1644','registered_livestock854_compiler_used':'registered_battle_cooking908_compiler_used','next24_preflight':'next25_preflight','all24_complete_clean_current_compiled_payloads_match':'all25_complete_clean_current_compiled_payloads_match','next_records=24':'next_records=25'}
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/battle_cooking_livestock_preflight_v2397/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),registered_release_config_is_v2_from_manifest=True,no_new_editorial_credit=True,full_goal_complete=False))
