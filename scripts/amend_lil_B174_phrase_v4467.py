"""Preserve the first draft and revise one complete conditional proposal naturally."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B174_phrase_v4467')
INPUT=Path('translations/lil_B174_editorial_manuscript_v1.json')
OUTPUT=Path('translations/lil_B174_editorial_manuscript_v2.json')
FAILED=Path('work/analysis/lil_B174_layout_v4465/all33_paragraph_layout_QA.json')

if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    doc=deepcopy(read(INPUT));finding=read(FAILED)
    assert len(finding['failures'])==1 and finding['failures'][0]['id']=='DK4_MES_B174_R0128'
    row=next(r for r in doc['records'] if r['source_record_index']==128)
    previous=deepcopy(row)
    assert row['english']=="{SPEAKER:1A}If I find something even more wonderful than the Silla Gold Crown, I'll come right back. Then let's go on a date!"
    row['english']="{SPEAKER:1A}If I find something even better than the Silla Gold Crown, I'll come right back. How about a date then?"
    row['localization_note']=("Restore the explicit if-condition, Julian's first-person acquisition/return and the named Silla Gold Crown comparison. "
        "The old When we find a finer gift, we'll come back converted a contingent proposal into a group promise. "
        "Even better naturally expresses もっとステキな物 as a personal comparison, without imposing a monetary value or identifying another treasure. "
        "How about a date then? preserves the eager invitation and ties it to his conditional prompt return. "
        "This complete-sentence phrasing also lets automatic native wrapping preserve the item title; no facts, source conditions or source commands are removed, "
        "and no authored breaks, padding, metric change or phrase-warning waiver is introduced. The initial wording and failed layout proof remain preserved.")
    row['previous_prose_English']=previous['english']
    row['previous_prose_localization_note']=previous['localization_note']
    row['prose_revision_producer']=str(Path(__file__))
    row['review']=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
    assert {r['id']:r for r in doc['records'] if r['id']!=row['id']}=={
        r['id']:r for r in read(INPUT)['records'] if r['id']!=row['id']}
    assert row['editorial_decision']=='revise' and (doc['revised'],doc['retained'])==(23,10)
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),
        phrase_revision_producer=str(Path(__file__)),phrase_revision_producer_sha256=sha(Path(__file__).read_bytes()),
        original_failed_layout_proof=str(FAILED),original_failed_layout_proof_sha256=sha(FAILED.read_bytes()))
    ROOT.mkdir(parents=True);save(OUTPUT,doc)
    save(ROOT/'complete_conditional_proposal_revision.json',dict(manuscript=str(OUTPUT),
        manuscript_sha256=sha(OUTPUT.read_bytes()),source_ID=row['id'],previous_English=previous['english'],
        revised_English=row['english'],localization_note=row['localization_note'],
        every_other_record_and_source_control_preserved=True,all33_read_as_complete_exchange_again=True,
        no_waiver_or_metric_guard_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Preserved v1 and failed layout; revised only R128 conditional invitation. All33 contextual decisions rechecked, no credit.')
