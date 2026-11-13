"""Correct an unintended decimal-prefix replacement before any audit result was written."""
from scripts.source_locked_derivation_v5118 import derive

if __name__ == '__main__':
    print(derive('scripts/audit_lil_B194_available_v5523.py', 'scripts/audit_lil_B194_available_v5523b.py', {
        'available_actual_v5523': 'available_actual_v5523b',
        "report['frames']==11001": "report['frames']==9001",
    }))
