"""Positive exact-extension/inverse and changed-builder rejection tests without touching the real builder."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v1 import BUILDER,STAGE,validate_builder_bytes
from dk4tool.dialogue.hodram_outcomes_profile_v2 import contract
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_builder_inverse_validation_v8359c')
if __name__=='__main__':
    assert not ROOT.exists();frozen=contract();before=BUILDER.read_bytes();digest=frozen['dependencies'][str(BUILDER)];assert sha(before)==digest
    anchor=b'    # Lexically valid "% o"';stage=STAGE.encode();assert before.count(anchor)==1 and stage not in before;planned=before.replace(anchor,stage+anchor,1)
    positives=[validate_builder_bytes(before,digest),validate_builder_bytes(planned,digest)];assert positives[1]['exact_owned_stage_inverse'] and planned.replace(stage,b'',1)==before
    variants={
        'changed-original-code':bytes([before[0]^1])+before[1:],
        'changed-original-code-with-owned-stage':bytes([planned[0]^1])+planned[1:],
        'duplicate-owned-stage':before.replace(anchor,stage+stage+anchor,1),
        'changed-owned-import':planned.replace(b'hodram_outcomes_editorial_v2',b'hodram_outcomes_editorial_v1'),
        'changed-stage-target':planned.replace(b"profile_config.get('hodram_outcomes_editorial')",b"profile_config.get('unreviewed_outcomes')"),
        'unowned-whitespace-edit':planned+b'\n',
        'wrong-insertion-boundary':before.replace(anchor,stage+b'\n'+anchor,1),
        'stage-before-all-previous-work':stage+before,
    };negatives=[]
    for label,raw in variants.items():
        assert raw not in [before,planned]
        try:validate_builder_bytes(raw,digest)
        except ValueError as error:negatives.append(dict(case=label,rejected=True,error=str(error),changed_input_sha256=sha(raw)))
        else:raise AssertionError('Unsafe builder accepted:'+label)
    assert len(negatives)==8 and BUILDER.read_bytes()==before
    ROOT.mkdir(parents=True);save(ROOT/'exact_owned_builder_stage_full_inverse_two_positives_eight_changed_builder_rejections.json',dict(positives=positives,negatives=negatives,frozen_contract_andall417_dependency_entries_unchanged=True,original_builder_sha256=digest,owned_stage_sha256=sha(stage),planned_builder_sha256=sha(planned),whole_original_builder_inverse_exact=True,all_nonbuilder_dependencies_still_exact=True,no_builder_registry_ROM_orcredit_changed=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Builder guard:original/exact owned extension pass;8changed builders rejected;whole original inverse exact.No files changed.')
