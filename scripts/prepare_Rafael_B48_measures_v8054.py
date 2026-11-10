"""Prepare measured paired-state comparison and the complete two-page focus sheet."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    common={'B47':'B48','R53':'R347','Rafael_B47_actual_v7999':'Rafael_B48_actual_v8053'}
    print(derive('scripts/measure_Rafael_B47_pairs_v8000.py','scripts/measure_Rafael_B48_pairs_v8054.py',{
        **common,'Rafael_B47_actual_comparison_v8000':'Rafael_B48_actual_comparison_v8054',
        '16001':'40001','all11':'all78','11_scene':'78_scene',
    }))
    print(derive('scripts/render_Rafael_B47_actual_focus_v8002.py','scripts/render_Rafael_B48_actual_focus_v8055.py',{
        **common,'Rafael_B47_actual_focus_v8002':'Rafael_B48_actual_focus_v8055',
        "s['source_record_index']==53":"s['source_record_index']==347",
        "following=next(s for s in english['speech_observations'] if s['source_record_index']==70)":"following=english['speech_observations'][english['speech_observations'].index(b)+1]",
        'EN following R70':'EN following R351',
    }))
