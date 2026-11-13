"""Reject two visually worse constraints and freshly check only one new layout."""
import sys
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha
from scripts.plan_rafael_B85_B100_v1 import main as plan_main

DOC = Path('translations/rafael_B85_B100_contextual_editorial_manuscript_v2.json')
PREFS = Path('translations/rafael_B85_B100_visual_preferences_v3.json')
OUT = Path('translations/rafael_B85_B100_visual_preferences_v4.json')
ROOT = Path('work/analysis/Rafael261_sparse_row_refinement_v4_20261105')

if __name__ == '__main__':
    assert not OUT.exists() and not ROOT.exists()
    prefs = load(PREFS)
    prefs['records']['DK4_MES_B86_R0272']['line_phrases'] = ['Just thinking about it']
    del prefs['records']['DK4_MES_B90_R0023']
    prefs.update(previous_preferences=str(PREFS), previous_preferences_sha256=sha(PREFS.read_bytes()),
        visual_retention=dict(id='DK4_MES_B90_R0023', reason="Retain the original balanced three lines. Keeping a fleet of my own together strands I'd like on a sparse middle line. The original complete paragraph is legible, preserves every word and has no missing glyph or awkward page turn."),
        fresh_layout_reason='The shorter thinking about it constraint produced a sparse Just opening. Keep Just with its following phrase; retain native geometry and all prose.')
    save(OUT, prefs)
    ROOT.mkdir()
    oldargv = sys.argv
    try:
        sys.argv = ['paragraph_planner', '--manuscript', str(DOC), '--preferences', str(OUT), '--out', str(ROOT/'full_plan')]
        plan_main()
    finally:
        sys.argv = oldargv
    doc, plan = map(load, [DOC, ROOT/'full_plan/automatic_plans.json'])
    old = load('work/analysis/Rafael_B85_B100_formatting_v3_20261105/automatic_plans.json')
    a, b = [{r['id']: r for r in d['records']} for d in [old, plan]]
    assert {i for i in a if a[i]['encoded_hex'] != b[i]['encoded_hex']} == {'DK4_MES_B86_R0272', 'DK4_MES_B90_R0023'}
    ident = 'DK4_MES_B86_R0272'
    subset = deepcopy(doc)
    subset.update(records=[r for r in doc['records'] if r['id'] == ident], blocks=[86],
        physical_speech_objects=1, ordinary_speech_objects=1, FE_speech_objects=0,
        typed_choice_objects=0, typed_choice_commands=0, subset_of=str(DOC), subset_of_sha256=sha(DOC.read_bytes()))
    manuscript = ROOT/'fresh_manuscript.json'
    save(manuscript, subset)
    subplan = deepcopy(plan)
    subplan.update(records=[b[ident]], manuscript=str(manuscript), manuscript_sha256=sha(manuscript.read_bytes()),
        subset_of=str(ROOT/'full_plan/automatic_plans.json'), subset_of_sha256=sha((ROOT/'full_plan/automatic_plans.json').read_bytes()))
    save(ROOT/'fresh_plan.json', subplan)
    print('All255 plans pass. One fresh layout;one exact original retention;other253 final layouts unchanged.')
