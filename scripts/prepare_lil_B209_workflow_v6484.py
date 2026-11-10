"""Add explicit registered-workflow metadata without altering any sealed editorial record."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B209_workflow_v6484')
INPUT=Path('translations/lil_B209_editorial_manuscript_v3.json')
OUTPUT=Path('translations/lil_B209_editorial_manuscript_v4.json')
OLD=Path('work/analysis/lil_B209_reference_approval_v6481/approval_receipt.json')
SEAL=ROOT/'approval_receipt.json'
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();old=read(INPUT);doc=deepcopy(old);approval=read(OLD)
    assert approval['manuscript_sha256']==sha(INPUT.read_bytes()) and approval['all20_five_gates_and_exact_reference_obligations_approved']
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],formatting_review_pending=False,reference_approval=str(SEAL),registered_workflow_metadata_added_without_prose_or_reference_change=True)
    validate_natural_dialogue_batch(doc);assert doc['records']==old['records'] and doc['native_approved_manuscript']==old['native_approved_manuscript'] and doc['reference_map_sha256']==old['reference_map_sha256']
    ROOT.mkdir(parents=True);save(OUTPUT,doc);updated=deepcopy(approval);updated.update(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),previous_reference_approval=str(OLD),previous_reference_approval_sha256=sha(OLD.read_bytes()),explicit_encoder_and_five_review_gates_validated_by_shared_validator=True,all20_editorial_records_and_reference_map_unchanged=True,producer_sha256=sha(Path(__file__).read_bytes()));save(SEAL,updated)
    save(ROOT/'metadata_receipt.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),approval=str(SEAL),approval_sha256=sha(SEAL.read_bytes()),original_sealed20_records_exact=True,source_prose_or_completion_credit_added=0,full_goal_complete=False));print('Explicit relocatable encoder/five-gate metadata passes shared v2 validator;all20 sealed records and native/reference approvals unchanged.')
