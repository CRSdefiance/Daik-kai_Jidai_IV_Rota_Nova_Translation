"""Faithful denial successor for an observed tightly fitted menu glyph loss."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_Shrines_Temples_choice_refinement_v3187')
OLD=Path('translations/lil_shrines_temples_choice_manuscript_v1.json')
NEW=Path('translations/lil_shrines_temples_choice_manuscript_v2.json')
DIAG=Path('work/analysis/lil_Shrines_Temples_menu_diagnostic_v3186/mismatch/first_complete_plane_mismatch.json')
PROOFOLD=Path('scripts/prove_lil_shrines_choices_v3185b.py')
PROOFNEW=Path('scripts/prove_lil_shrines_choices_v3188.py')

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,NEW,PROOFNEW])
    doc=deepcopy(read(OLD));diagnostic=read(DIAG)
    row=next(r for r in doc['records'] if r['id']=='DK4_CHOICE_B105_C186_O2')
    assert row['english']==diagnostic['text']=="There's no such animal."
    assert diagnostic['width']==138 and diagnostic['stride']==140
    actual={tuple(p) for p in diagnostic['native_points']}
    expected={tuple(p) for p in diagnostic['expected_points']}
    missing=sorted(expected-actual)
    assert missing and all(x<6 for x,y,v in missing) and not actual-expected
    row['prior_prose_before_native_menu_refinement']=row['english']
    row['english']="That animal doesn't exist."
    assert len(row['english'])==26 and row['editorial_decision']=='revise'
    note=("The equally faithful denial That animal doesn't exist preserves the third answer's claim that no such animal exists. The previous wording was natural but the complete138px native menu plane lost part of its leading T. This26cell wording must pass a new156px native canvas proof. No authored padding, clipping allowance, renderer patch or changed answer index is used.")
    row['localization_note']+=' '+note
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),
        native_menu_refinement_diagnostic=str(DIAG),native_menu_refinement_diagnostic_sha256=sha(DIAG.read_bytes()))
    text=PROOFOLD.read_text(encoding='utf-8')
    for a,b in [('lil_Shrines_Temples_choices_v3185b','lil_Shrines_Temples_choices_v3188'),
                ('lil_shrines_temples_choice_manuscript_v1.json','lil_shrines_temples_choice_manuscript_v2.json'),
                ('source_derived_Shrines_Temples_choice_painter_v3185b','source_derived_Shrines_Temples_choice_painter_v3188'),
                ('source_derived_three_choice_VM_v3185b','source_derived_three_choice_VM_v3188'),
                ('native_count=2','native_count=3')]:
        assert a in text
        text=text.replace(a,b)
    PROOFNEW.write_text(text,encoding='utf-8')
    ROOT.mkdir(parents=True);save(NEW,doc)
    save(ROOT/'source_faithful_denial_successor.json',dict(
        manuscript=str(NEW),manuscript_sha256=sha(NEW.read_bytes()),
        previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),
        id=row['id'],source_Japanese=row['source_Japanese'],source_reference=row['source_reference'],source_hex=row['source_hex'],
        source_meaning=row['source_meaning'],previous_English=diagnostic['text'],english=row['english'],reason=note,
        missing_leading_T_ink_coordinates=missing,diagnostic=str(DIAG),diagnostic_sha256=sha(DIAG.read_bytes()),
        next_native_proof_producer=str(PROOFNEW),next_native_proof_producer_sha256=sha(PROOFNEW.read_bytes()),
        prior_executed_proof=str(PROOFOLD),prior_executed_proof_sha256=sha(PROOFOLD.read_bytes()),
        no_runtime_change_or_older_record_technical_reaudit=True,
        source_prose_or_completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Faithful26cell denial successor;leading-T loss preserved;new complete menu proof required.')
