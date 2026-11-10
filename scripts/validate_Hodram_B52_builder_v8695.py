"""Validate exact historical/compatible/shared-hook builders and changed-source failures."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v7 import STAGE_V7,STAGE_B49_V4,STAGE_B50_V2,STAGE_B51
from dk4tool.patch.hodram_outcomes_builder_guard_v8 import STAGE_V8,STAGE_B49_V5,STAGE_B50_V3,STAGE_B51_V2,BUILDER_STAGE,BUILDER,validate_builder_bytes
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B52_builder_validation_v8695')
SUPPORT=Path('work/analysis/Hodram_B52_builder_support_v8694b')

if __name__=='__main__':
    assert not ROOT.exists();support=read(SUPPORT/'source_equivalence.json');digest=support['original_frozen_builder_digest']
    current=(SUPPORT/'builder.before.py').read_bytes();planned=(SUPPORT/'builder.planned.py').read_bytes()
    assert BUILDER.read_bytes()==current
    old=[s.encode() for s in [STAGE_V7,STAGE_B49_V4,STAGE_B50_V2,STAGE_B51]]
    new=[s.encode() for s in [STAGE_V8,STAGE_B49_V5,STAGE_B50_V3,STAGE_B51_V2]]
    hook=BUILDER_STAGE.encode();compatible=planned.replace(hook,b'',1)
    original=Path('work/analysis/Hodram_B51_builder_inspection_v8594/original_guarded_builder_inverse.py').read_bytes()
    positives=[]
    for label,raw in [('whole-original',original),('current-V8609',current),('historical-before-B51',current.replace(old[3],b'',1)),('compatible-prefix',compatible),('shared-late-hook',planned)]:
        proof=validate_builder_bytes(raw,digest);positives.append(dict(case=label,sha256=sha(raw),proof=proof))
    cases=[('unowned-comment',planned+b'\n# unapproved change\n',digest),
           ('hook-with-old-prefix',current.replace(b'    # Lexically valid "% o"',hook+b'    # Lexically valid "% o"',1),digest),
           ('duplicate-hook',planned.replace(hook,hook+hook,1),digest),
           ('hook-before-B51',compatible.replace(new[3],hook+new[3],1),digest),
           ('hook-after-final-guards',compatible+hook,digest),
           ('wrong-hook-input',planned.replace(b'apply_extensions(candidate, baseline',b'apply_extensions(baseline, candidate'),digest),
           ('wrong-hook-profile',planned.replace(b"get('late_editorial_extensions', [])",b"get('unowned_extensions', [])"),digest),
           ('wrong-hook-module',planned.replace(b'late_editorial_extensions_v1 import',b'late_editorial_extensions_v999 import'),digest),
           ('missing-final-boundary',planned.replace(b'    # Lexically valid "% o"',b'    # changed final boundary'),digest),
           ('wrong-original-digest',planned,'0'*64)]
    for index,(prior,stage) in enumerate(zip(old,new,strict=True)):
        cases.extend([(f'only-new-stage-{index}',current.replace(prior,stage,1),digest),
                      (f'missing-stage-{index}',planned.replace(stage,b'',1),digest),
                      (f'duplicate-stage-{index}',planned.replace(stage,stage+stage,1),digest),
                      (f'mixed-old-stage-{index}',planned+prior,digest)])
    for index in range(3):
        swapped=compatible.replace(new[index],b'__FIRST_STAGE__',1).replace(new[index+1],new[index],1).replace(b'__FIRST_STAGE__',new[index+1],1)
        cases.append((f'reordered-prefix-{index}',swapped.replace(new[3],new[3]+hook,1),digest))
    negatives=[]
    for label,raw,wanted in cases:
        assert raw!=planned or wanted!=digest
        try:validate_builder_bytes(raw,wanted)
        except ValueError as error:negatives.append(dict(case=label,actual_changed_input=True,sha256=sha(raw),requested_original_digest=wanted,rejected=True,error=str(error)))
        else:raise AssertionError('Changed builder accepted:'+label)
    assert len(positives)==5 and len(negatives)==29 and BUILDER.read_bytes()==current
    ROOT.mkdir(parents=True)
    save(ROOT/'exact_builder_inverse_cases.json',dict(positives=positives,negative_cases=negatives,negative_count=29,
         original_frozen_builder_digest=digest,current_builder_sha256=sha(current),planned_builder_sha256=sha(planned),
         complete_original_source_inverse_including_all_unowned_newline_bytes_exact=True,
         shared_hook_only_after_complete_B51_before_existing_final_guards=True,
         no_live_builder_registry_ROM_orcredit_change=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Shared builder hook:5 exact historical/compatible forms and29 changed-source rejections;whole original builder inverse preserved. Live builder/registry/ROM unchanged.')
