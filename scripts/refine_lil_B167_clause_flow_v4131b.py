"""Preserve failed layout;refine three complete clauses without removing any source fact."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/lil_B167_clause_flow_v4131b')
INPUT = Path('translations/lil_B167_editorial_manuscript_v1.json')
OUTPUT = Path('translations/lil_B167_editorial_manuscript_v2.json')
CHANGES = {
    75:("Square sails can't turn lengthwise. They're good with a following wind, but can't reach the best angle in a headwind.",
        'Use direct conversational clauses for the same orientation limit and wind tradeoff. Lengthwise means fore-and-aft here; good with a following wind preserves the source favorable performance, and headwind preserves adverse wind. Keep the explicit best-angle limitation; add no mechanic or reduced requirement.'),
    78:("Triangular sails, or lateens to old hands, run fore-and-aft. Unlike square sails, they can't turn across the ship.",
        'Old hands is a natural seafaring idiom for the source people-in-the-know aside, not a literal age, rank or relationship. Keep triangular shape, lateen terminology, fore-and-aft orientation and crosswise limit; make the aside easier to follow aloud.'),
    81:("They can take the right angle in a headwind, but they're slower with a following wind. Still with me?",
        'Retain the exact angle advantage in adverse wind, lower speed with following wind and rhetorical understanding check. Headwind is natural English for the source adverse-wind condition; no source fact or menu is removed or added.'),
}
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    doc=deepcopy(read(INPUT))
    before=read(INPUT)
    for row in doc['records']:
        if row['source_record_index'] in CHANGES:
            value,note=CHANGES[row['source_record_index']]
            row['prior_reviewed_English_before_clause_refinement']=row['english']
            row['english']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+value
            row['localization_note']+=' '+note
        assert all(row['review'][k] for k in ['source','context','localization','naturalness']) and not row['review']['formatting']
    assert [(r['id'],r['editorial_decision'],r['source_hex'],r['current_hex'],r['source_meaning']) for r in doc['records']]==[
        (r['id'],r['editorial_decision'],r['source_hex'],r['current_hex'],r['source_meaning']) for r in before['records']]
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()))
    save(OUTPUT,doc)
    tools=[]
    tools.append(derive('dk4tool/dialogue/lil_B167_layout_v1.py','dk4tool/dialogue/lil_B167_layout_v2.py',{
        'def _word(value):':"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('old','hands'),('run','fore-and-aft'),(\"they're\",'slower'),('right','angle'),('best','angle')})\n\ndef _word(value):"}))
    tools.append(derive('scripts/plan_lil_B167_layout_v4131.py','scripts/plan_lil_B167_layout_v4131b.py',{
        'lil_B167_layout_v1':'lil_B167_layout_v2','lil_B167_layout_v4131':'lil_B167_layout_v4131b',
        'lil_B167_editorial_manuscript_v1':'lil_B167_editorial_manuscript_v2','lil_B167_editorial_manuscript_v2':'lil_B167_editorial_manuscript_v3'}))
    tools.append(derive('scripts/verify_lil_B167_fonts_v4132.py','scripts/verify_lil_B167_fonts_v4132b.py',{
        'lil_B167_layout_v1':'lil_B167_layout_v2','lil_B167_fonts_v4132':'lil_B167_fonts_v4132b',
        'lil_B167_editorial_manuscript_v2':'lil_B167_editorial_manuscript_v3'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'three_clause_refinements_and_source_facts_preserved.json',dict(previous_manuscript=str(INPUT),
        previous_manuscript_sha256=sha(INPUT.read_bytes()),manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),
        changed_source_record_indices=sorted(CHANGES),all_source_facts_controls_meanings_and_decisions_unchanged=True,
        previous_failed_layout='work/analysis/lil_B167_layout_v4131/all27_paragraph_layout_QA.json',
        previous_failed_layout_sha256=sha(Path('work/analysis/lil_B167_layout_v4131/all27_paragraph_layout_QA.json').read_bytes()),
        tools=tools,no_authored_break_padding_guard_change_or_wording_waiver=True,no_ROM_registry_ledger_credit_change=True))
    print('Three complete B167 clauses refined;all meanings,source facts and decisions preserved;failed plan retained.')
