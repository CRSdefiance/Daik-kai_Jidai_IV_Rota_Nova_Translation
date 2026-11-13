"""Validate only exact original/legacy/current owned stages and reject unowned builder changes."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v2 import BUILDER,STAGE,LEGACY_STAGE,validate_builder_bytes
from dk4tool.dialogue.hodram_outcomes_profile_v3 import contract
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_builder_fixture_successor_validation_v8373')
if __name__=='__main__':
    assert not ROOT.exists();frozen=contract();live=BUILDER.read_bytes();digest=frozen['dependencies'][str(BUILDER)];oldstage=LEGACY_STAGE.encode();stage=STAGE.encode();anchor=b'    # Lexically valid "% o"'
    assert live.count(oldstage)==1 and stage not in live;original=live.replace(oldstage,b'',1);assert sha(original)==digest and original.count(anchor)==1
    planned=original.replace(anchor,stage+anchor,1);positives=[validate_builder_bytes(v,digest) for v in [original,live,planned]]
    assert positives[1]['owned_stage_version']=='preserved-v2' and positives[2]['owned_stage_version']=='current-v3' and planned.replace(stage,b'',1)==original
    variants={
        'changed-original-code':bytes([original[0]^1])+original[1:],
        'changed-original-with-current-stage':bytes([planned[0]^1])+planned[1:],
        'duplicate-current-stage':original.replace(anchor,stage+stage+anchor,1),
        'both-known-stages':original.replace(anchor,oldstage+stage+anchor,1),
        'changed-current-import':planned.replace(b'hodram_outcomes_editorial_v3',b'hodram_outcomes_editorial_v1'),
        'changed-current-key':planned.replace(b"profile_config.get('hodram_outcomes_editorial')",b"profile_config.get('unreviewed_outcomes')"),
        'changed-legacy-import':live.replace(b'hodram_outcomes_editorial_v2',b'hodram_outcomes_editorial_v1'),
        'unowned-whitespace':planned+b'\n',
        'wrong-current-insertion-boundary':original.replace(anchor,stage+b'\n'+anchor,1),
        'current-stage-before-previous-stack':stage+original,
        'legacy-stage-before-previous-stack':oldstage+original,
    };negatives=[]
    for label,raw in variants.items():
        assert raw not in [original,live,planned]
        try:validate_builder_bytes(raw,digest)
        except ValueError as error:negatives.append(dict(case=label,rejected=True,error=str(error),changed_input_sha256=sha(raw)))
        else:raise AssertionError('Unsafe builder accepted:'+label)
    assert len(negatives)==11 and BUILDER.read_bytes()==live
    ROOT.mkdir(parents=True);save(ROOT/'three_exact_builder_forms_eleven_changed_builder_rejections_full_source_inverse.json',dict(positives=positives,negatives=negatives,original_frozen_builder_sha256=digest,legacy_current_builder_sha256=sha(live),planned_builder_sha256=sha(planned),legacy_stage_sha256=sha(oldstage),current_owned_stage_sha256=sha(stage),all417_frozen_dependency_entries_preserved=True,all_nonbuilder_dependencies_exact=True,full_original_builder_inverse_exact=True,no_builder_registry_ROM_orcredit_changed=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Builder successor:3exact forms pass/11changed builders reject;onlyone knownstage allowed/full frozen sourceinverse exact.No files changed.')
