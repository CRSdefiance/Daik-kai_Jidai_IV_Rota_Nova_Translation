"""Register the already tested relocatable encoder metadata;retain the rejected descriptive draft tag."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_encoder_v8426')
OLD=Path('translations/hodram_B49_editorial_manuscript_v3.json')
DOC=Path('translations/hodram_B49_editorial_manuscript_v4.json')
APPROVAL=Path('work/analysis/Hodram_B49_format_v8423/formatting_approval.json')

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();old,approval=map(read,[OLD,APPROVAL])
    assert old['encoder']=='natural-dialogue' and approval['manuscript_sha256']==sha(OLD.read_bytes()) and approval['all16_five_gates_true']
    try:validate_natural_dialogue_batch(old)
    except ValueError as error:assert str(error)=='natural-dialogue-v1 requires a supported dialogue encoder'
    else:raise AssertionError('Preserved draft encoder unexpectedly accepted')
    doc=deepcopy(old);doc['encoder']='dialogue-relocatable-v1'
    assert {k:v for k,v in doc.items() if k!='encoder'}=={k:v for k,v in old.items() if k!='encoder'}
    validate_natural_dialogue_batch(doc);validate_natural_dialogue_batch({**doc,'records':doc['typed_choice_records']})
    ROOT.mkdir(parents=True);save(DOC,doc)
    updated=deepcopy(approval);updated.update(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),predecessor_metadata_manuscript=str(OLD),predecessor_metadata_manuscript_sha256=sha(OLD.read_bytes()),predecessor_approval=str(APPROVAL),predecessor_approval_sha256=sha(APPROVAL.read_bytes()),only_root_encoder_metadata_changed=True,encoder_before='natural-dialogue',encoder_after='dialogue-relocatable-v1',all_source_current_final_record_fields_compiled_bytes_prose_reviews_names_andactual_proofs_unchanged=True,standard_natural_dialogue_v2_batch_andtyped_labels_pass=True,no_policy_guard_global_encoder_native_ROM_orcredit_change=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes()))
    save(ROOT/'metadata_approval.json',updated)
    print('B49 manuscriptv4 registers tested dialogue-relocatable-v1;only one root metadata value changes. Standardv2 speech/choice validation passes;rejectedv3 retained.No ROM/prose/credit change.')
