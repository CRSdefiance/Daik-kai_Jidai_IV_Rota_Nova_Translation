"""Faithful prose refinements for two concrete weak-wrap findings."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Shrines_Temples_refinement_v3177')
OLD = Path('translations/lil_shrines_temples_editorial_manuscript_v1.json')
NEW = Path('translations/lil_shrines_temples_editorial_manuscript_v2.json')
FAILURE = Path('work/analysis/lil_Shrines_Temples_layout_v3176/all220_paragraph_layout_and_QA.json')
UPDATES = {
    'DK4_MES_B107_R0059': (
        "{SPEAKER:09}...Adorn it like a pure new star? Maybe it's asking us to bring some sort of ornament.",
        "The concrete first-row ending like is resolved by stating the source's quoted adornment clue and tentative bring-an-ornament inference naturally. The extra shine wording was an English explanation, not a separate source fact; no puzzle answer is supplied."),
    'DK4_MES_B108_R0030': (
        "{SPEAKER:A0}Our village has passed this lamp down since ancient times. They say anyone seeking the Proof will need it. I entrust it to you.",
        "The concrete first-row ending in is resolved with an active community subject. The village, ancient transmission, hearsay, necessity for Proof seekers and entrusting the lamp are all preserved; no family inheritance is invented.")}

if __name__ == '__main__':
    assert not ROOT.exists() and not NEW.exists()
    doc, failure = deepcopy(read(OLD)), read(FAILURE)
    assert {r['id'] for r in failure['failures']} == set(UPDATES)
    for row in doc['records']:
        if row['id'] not in UPDATES:
            continue
        english, note = UPDATES[row['id']]
        row['prior_prose_before_wrap_refinement'] = row['english']
        row['english'] = english
        row['localization_note'] += ' ' + note
        assert row['editorial_decision'] == 'revise'
    doc.update(previous_manuscript=str(OLD), previous_manuscript_sha256=sha(OLD.read_bytes()),
        prose_refinement_failure=str(FAILURE), prose_refinement_failure_sha256=sha(FAILURE.read_bytes()),
        no_source_control_gloss_or_review_gate_change=True)
    ROOT.mkdir(parents=True)
    save(NEW, doc)
    save(ROOT / 'faithful_refinement_receipt.json', dict(
        previous=str(OLD), previous_sha256=sha(OLD.read_bytes()),
        manuscript=str(NEW), manuscript_sha256=sha(NEW.read_bytes()),
        failure=str(FAILURE), failure_sha256=sha(FAILURE.read_bytes()), changed_IDs=sorted(UPDATES),
        no_meaning_or_native_control_waiver=True, native_font_and_menu_gates_pending=True,
        source_prose_or_completion_credit_added=0, new_emulator_runs=0,
        producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print('Two faithful prose refinements; all source facts retained; no weak-wrap waiver.')
