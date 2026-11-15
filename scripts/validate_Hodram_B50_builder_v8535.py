"""Validate exact old/compatible/additive builder forms and meaningful changed-builder rejections."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v6 import BUILDER,STAGE_V5,STAGE_B49_V2,STAGE_V6,STAGE_B49_V3,STAGE_B50,validate_builder_bytes
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B50_builder_validation_v8535')
if __name__=='__main__':
    assert not ROOT.exists();inspection=read('work/analysis/Hodram_B50_builder_inspection_v8531/builder_inspection.json')
    current=BUILDER.read_bytes();assert sha(current)==inspection['builder_sha256'];digest=inspection['original_builder_sha256']
    original=Path('work/analysis/Hodram_B50_builder_inspection_v8531/original_guarded_builder_inverse.py').read_bytes()
    compatible=current.replace(STAGE_V5.encode(),STAGE_V6.encode(),1).replace(STAGE_B49_V2.encode(),STAGE_B49_V3.encode(),1)
    planned=compatible.replace(STAGE_B49_V3.encode(),(STAGE_B49_V3+STAGE_B50).encode(),1)
    positives=[]
    for label,value in [('whole-original',original),('current-v8475',current),('compatible-without-B50',compatible),('additive-B50',planned)]:
        proof=validate_builder_bytes(value,digest);positives.append(dict(case=label,sha256=sha(value),proof=proof))
    base=compatible;add=STAGE_B50.encode();prior=STAGE_B49_V3.encode();pre=STAGE_V6.encode()
    cases=[
        ('unowned-comment',planned+b'\n# unapproved mutation\n',digest),
        ('new-predecessor-alone',current.replace(STAGE_V5.encode(),pre),digest),
        ('new-B49-alone',current.replace(STAGE_B49_V2.encode(),prior),digest),
        ('B50-with-old-predecessors',current.replace(STAGE_B49_V2.encode(),STAGE_B49_V2.encode()+add),digest),
        ('duplicate-predecessor',planned.replace(pre,pre+pre),digest),
        ('duplicate-B49',planned.replace(prior,prior+prior),digest),
        ('duplicate-B50',planned.replace(add,add+add),digest),
        ('mixed-outcomes-version',planned+STAGE_V5.encode(),digest),
        ('mixed-B49-version',planned+STAGE_B49_V2.encode(),digest),
        ('B50-before-B49',base.replace(prior,add+prior),digest),
        ('B50-before-outcomes',base.replace(pre,add+pre),digest),
        ('B50-after-percent-safety',base+add,digest),
        ('unapproved-B50-module',planned.replace(b'hodram_B50_editorial_v1',b'hodram_B50_editorial_v999'),digest),
        ('B50-wrong-input',planned.replace(b'apply_hodram_B50_editorial(candidate, baseline',b'apply_hodram_B50_editorial(baseline, candidate'),digest),
        ('missing-percent-boundary',planned.replace(b'    # Lexically valid "% o"',b'    # Altered safety boundary'),digest),
        ('wrong-whole-original-hash',planned,'0'*64),
    ]
    rejected=[]
    for label,value,wanted in cases:
        assert value!=planned or wanted!=digest
        try:validate_builder_bytes(value,wanted)
        except ValueError as error:rejected.append(dict(case=label,actual_changed_input=True,sha256=sha(value),requested_original_digest=wanted,rejected=True,error=str(error)))
        else:raise AssertionError('Changed builder accepted:'+label)
    ROOT.mkdir(parents=True);(ROOT/'current_builder.bin').write_bytes(current);(ROOT/'compatible_builder.bin').write_bytes(compatible);(ROOT/'planned_builder.bin').write_bytes(planned)
    assert BUILDER.read_bytes()==current
    save(ROOT/'exact_builder_inverse_cases.json',dict(positives=positives,negative_cases=rejected,negative_count=len(rejected),full_original_source_inverse_sha256=digest,current_builder_sha256=sha(current),planned_builder_sha256=sha(planned),all_owned_stages_once_original_order_before_final_percent_safety=True,all_unowned_original_builder_bytes_invert_exactly=True,no_live_builder_registry_ROM_orcredit_change=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Builder support:4 exact old/compatible/additive forms and16actual changed-builder rejections pass;whole original inverse exact.No live builder edit.')
