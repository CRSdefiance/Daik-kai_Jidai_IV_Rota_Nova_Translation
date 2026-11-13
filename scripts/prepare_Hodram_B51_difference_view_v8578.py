"""Render all measured later B51 RGB differences for direct review."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B51_difference_tools_v8578')
    assert not root.exists()
    result = derive('scripts/prepare_Hodram_B50_difference_view_v8510.py', 'scripts/render_Hodram_B51_differences_v8578.py', {
        'B50 captures': 'B51 captures',
        'Hodram_B50_difference_view_v8510': 'Hodram_B51_difference_view_v8578',
        'Hodram_B50_comparison_v8509': 'Hodram_B51_comparison_v8577',
        '[5110,5650,5830,7270]': '[4870,5650,5830]',
        'all_four_later_RGB_differences.png': 'all_three_later_RGB_differences.png',
    })
    root.mkdir(parents=True)
    save(root / 'derivation.json', dict(derivation=result, all_later_nonidentical_pairs_included=True, no_retiming_capture_replay_ROM_write_orcredit=True))
