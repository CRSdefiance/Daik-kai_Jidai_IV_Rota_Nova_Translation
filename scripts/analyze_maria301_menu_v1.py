"""Keep native caption/highlight checks scoped to Maria's exact two-choice command."""
from scripts.analyze_native_choice_fixture_samples_v3 import source as previous, menu_scopes
from scripts.analyze_maria301_display_v1 import verified_existing_unlock
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    " and not report.get('battery_save_preloaded')": ' and verified_existing_unlock(report)',
    "source_rows=load(manuscript_path)['records']":
        "source_rows=[r for r in load(manuscript_path)['records'] if r['kind']=='typed-choice-label']\n        assert len(source_rows)==2 and all(r['block']==29 for r in source_rows)",
    'actual_gameplay=True,disclosed_initialized_fixture=True,':
        'actual_gameplay=True,disclosed_initialized_fixture=True,existing_system_only_unlock_not_earned=True,',
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-native-menu-captions-highlights-explicit-Maria-unlock', 'exec'), globals())
