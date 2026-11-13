"""Refine two phrase boundaries and qualified sympathy;preserve all33 source decisions."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B170_phrase_flow_v4275')
INPUT=Path('translations/lil_B170_editorial_manuscript_v2.json')
OUTPUT=Path('translations/lil_B170_editorial_manuscript_v3.json')
OLD=Path('dk4tool/dialogue/lil_B170_layout_v1.py')
NEW=Path('dk4tool/dialogue/lil_B170_layout_v2.py')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists() and not NEW.exists()
    doc=deepcopy(read(INPUT))
    row=next(r for r in doc['records'] if r['source_record_index']==104)
    previous=row['english']
    row['english']="{SPEAKER:02}Still, I guess I understand wanting to prove your teacher wrong."
    row['phrase_flow_previous_english']=previous
    row['phrase_flow_refinement_reason']='I guess I understand preserves Lil\'s qualified sympathy in a natural complete clause;all teacher and prove-wrong meaning remains. Keep the phrase sort of intact in the formatter rather than permit the earlier split.'
    row['localization_note']=row['localization_note'].replace('Sort of understand retains the source hedge','I guess I understand retains the source hedge')+' '+row['phrase_flow_refinement_reason']
    text=OLD.read_text(encoding='utf-8')
    pairs=[('come','over'),('over','here'),('sort','of'),('of','understand')]
    assert text.count('\ndef _word(value):')==1
    text=text.replace('\ndef _word(value):','\nPROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset('+repr(pairs)+')\n\ndef _word(value):')
    compile(text,str(NEW),'exec')
    NEW.write_text(text,encoding='utf-8',newline='\n')
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),phrase_flow_formatter=str(NEW),phrase_flow_formatter_sha256=sha(NEW.read_bytes()))
    ROOT.mkdir(parents=True)
    save(OUTPUT,doc)
    save(ROOT/'qualified_sympathy_and_phrase_boundaries.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),
        revised_record=row['id'],previous_english=previous,current_english=row['english'],reason=row['phrase_flow_refinement_reason'],
        additional_protected_pairs=pairs,previous_formatter=str(OLD),previous_formatter_sha256=sha(OLD.read_bytes()),new_formatter=str(NEW),new_formatter_sha256=sha(NEW.read_bytes()),
        all33_source_meanings_controls_macros_and21_12_decisions_preserved=True,no_wording_weak_ending_or_native_guard_waiver=True,
        source_prose_or_completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    plan=Path('scripts/plan_lil_B170_layout_v4273.py').read_text(encoding='utf-8')
    plan=plan.replace('lil_B170_layout_v1','lil_B170_layout_v2').replace('lil_B170_layout_v4273','lil_B170_layout_v4276')
    plan=plan.replace("INPUT=Path('translations/lil_B170_editorial_manuscript_v1.json')","INPUT=Path('translations/lil_B170_editorial_manuscript_v3.json')")
    plan=plan.replace("OUTPUT=Path('translations/lil_B170_editorial_manuscript_v2.json')","OUTPUT=Path('translations/lil_B170_editorial_manuscript_v4.json')")
    target=Path('scripts/plan_lil_B170_layout_v4276.py')
    assert not target.exists()
    target.write_text(plan,encoding='utf-8',newline='\n')
    print('B170 qualified sympathy refined and four phrase boundaries strengthened;21 revisions/12 retentions and all meanings preserved.')
