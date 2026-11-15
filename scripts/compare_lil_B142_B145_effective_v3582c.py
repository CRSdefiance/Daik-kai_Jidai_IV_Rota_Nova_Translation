"""Use the exact fresh38 context field names;preserve the failed adapter."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    a=Path('scripts/compare_lil_B142_B145_effective_v3582b.py');t=a.read_text(encoding='utf-8')
    for x,y in [('all38_complete_clean_source_objects_read_before_older_English_comparison','all_four_complete_clean_exchanges_read'),('all38_fresh_source_glosses_precede_localized_English','all38_glosses_before_older_English')]:assert x in t;t=t.replace(x,y)
    exec(compile(t,str(Path(__file__))+'::corrected_context_fields','exec'),dict(__name__='__main__',__file__=__file__))
    save(Path('work/analysis/lil_B142_B145_comparison_v3582/context_adapter_correction.json'),dict(failed_predecessor=str(a),failed_predecessor_sha256=sha(a.read_bytes()),actual_context_field_names_bound=True,no_source_or_English_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
