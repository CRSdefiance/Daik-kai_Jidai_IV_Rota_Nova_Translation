"""Faithful successor refusal avoids the concrete tightly fitted19-cell loss."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
OLD=Path('translations/lil_recruits_julian_choice_manuscript_v1.json')
DOC=Path('translations/lil_recruits_julian_choice_manuscript_v2.json')
ROOT=Path('work/analysis/lil_Recruits_Julian_choice_refine_v3091')
PRIOR=Path('translations/lil_mediterranean_africa_choices_editorial_draft_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();doc=deepcopy(read(OLD))
    row=next(r for r in doc['records'] if r['option_index']==1);assert row['english']=='You must be joking!'
    row['english']='You must be kidding!';assert len(row['english'])==20
    row['localization_note']+=' The previous idiomatic wording remains a sound contextual translation, but its nineteen-cell unpadded menu exposed eleven missing pixels from the leading Y in the tightly fitted114px native painter. The equally natural twenty-cell refusal keeps the source emphatic disbelief and uses a120px native canvas; it must pass complete new native revalidation. No manual padding or runtime fix is introduced. Preserve the failed3090 and diagnostic3090b producers; an analogous current-batch menu finding was already documented in the linked Mediterranean/Africa successor, without reopening that completed batch.'
    row.pop('fresh_retained_wording_justification');row['editorial_decision']='revise'
    assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
    doc.update(revised=1,retained=1,previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),current_batch_nineteen_cell_painter_risk_resolved_pending_new_native_proof=True)
    ROOT.mkdir(parents=True);save(DOC,doc);save(ROOT/'source_faithful_refusal_successor.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),
        revised_ID=row['id'],source_Japanese=row['source_Japanese'],source_reference=row['source_reference'],source_hex=row['source_hex'],previous_English='You must be joking!',english=row['english'],reason=row['localization_note'],
        diagnostic_missing_ink_coordinates=[[0,6],[0,7],[0,8],[1,9],[3,9],[1,10],[3,10],[2,11],[2,12],[2,13],[2,14]],
        current_padded132px_labels_passed_before_reviewed114px_leading_Y_failure=True,
        failed_and_diagnostic_producers={str(p):sha(p.read_bytes()) for p in [Path('scripts/prove_lil_recruits_julian_choices_v3090.py'),Path('scripts/diagnose_lil_recruits_julian_choices_v3090b.py')]},
        earlier_source_of_analogous_menu_finding=str(PRIOR),earlier_source_sha256=sha(PRIOR.read_bytes()),
        no_runtime_change_or_older_record_technical_reaudit=True,source_prose_or_completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('One faithful twenty-cell refusal successor; failed nineteen-cell native test preserved. Complete new menu proof required.')
