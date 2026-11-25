"""Derive current-font stored proof, including fresh padded FI input and measured default Lil."""
from scripts.source_locked_derivation_v5118 import derive

if __name__ == '__main__':
    print(derive('scripts/prove_lil_B193_stored_v5462.py', 'scripts/prove_lil_B194_stored_v5507.py', {
        'B193': 'B194', 'stored_v5462': 'stored_v5507', 'relocation_v5461': 'relocation_v5506b',
        'voices_v5448': 'voices_v5490',
        'all15': 'all11', 'targets60': 'targets44',
        '==15': '==11', '==60': '==44', '=60': '=44', '=15': '=11', '=14': '=10',
        'in [166,167,168,254]': 'in [6,117,156,254]',
        "expanded=stored[1:]\n                assert not any(m in expanded for m in [b'FI',b'FA',b'FO'])":
        "assert not any(m in stored[1:] for m in [b'FA',b'FO'])\n                expanded=stored[1:].replace(b'FI',b'Lil')",
        'actual_selected_B193_linear_A000_C200_and_end_reachability_unexecuted':
        'actual_selected_B194_conditional_FI_resource42_two_C200_and_end_reachability_unexecuted',
        'Verify all15': 'Verify all11',
    }))
