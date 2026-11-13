"""Prepare fresh layout/native proofs without overwriting the initial failed run."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B174_layout_successor_tools_v4468')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/plan_lil_B174_layout_v4465.py','scripts/plan_lil_B174_layout_v4469.py',{
        'lil_B174_layout_v4465':'lil_B174_layout_v4469',
        'lil_B174_editorial_manuscript_v1':'lil_B174_editorial_manuscript_v2',
        'lil_B174_editorial_manuscript_v2':'lil_B174_editorial_manuscript_v3',
    }),derive('scripts/verify_lil_B174_fonts_v4466.py','scripts/verify_lil_B174_fonts_v4470.py',{
        'lil_B174_fonts_v4466':'lil_B174_fonts_v4470',
        'lil_B174_editorial_manuscript_v2':'lil_B174_editorial_manuscript_v3',
    })]
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tools=tools,
        initial_failed_producer_and_QA_preserved=True,all_geometry_guards_and_protected_phrases_unchanged=True,
        no_credit=True,full_goal_complete=False))
    print('Prepared fresh33-paragraph layout and264 alignment-case successor, preserving initial failure.')
