"""Repair only a missing derivation key before any fixture was written."""
from scripts.source_locked_derivation_v5118 import derive

if __name__ == '__main__':
    print(derive('scripts/prepare_lil_B194_display_v5514.py', 'scripts/prepare_lil_B194_display_v5514c.py', {
        'Paired B194 fixtures retain38 source commands,three unforced500/700/500 RNG predicates,16relative sites,13 stored speeches and all alternative A000s.':
        'B191 fixtures retain all38 commands+9 original init commands,twelve progressive/one impersonal FE,three mixed predicates,16relative sites,four alternative A000s and no-effect paths,C200 and end.',
    }))
