"""Prove exact source inverse for planned additive registration without changing the builder orregistry."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v3 import (
    BUILDER,STAGE_V3,STAGE_V4,LEGACY_STAGE,STAGE_B49,ANCHOR,validate_builder_bytes,
)
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_builder_v8431')

if __name__=='__main__':
    assert not ROOT.exists();raw=BUILDER.read_bytes();contract=read('translations/hodram_outcomes_native_contract_v1.json');digest=contract['dependencies'][str(BUILDER)]
    assert raw.count(STAGE_V3.encode())==1 and raw.count(ANCHOR)==1 and STAGE_B49.encode() not in raw
    frozen=raw.replace(STAGE_V3.encode(),b'',1);assert sha(frozen)==digest
    legacy=raw.replace(STAGE_V3.encode(),LEGACY_STAGE.encode(),1);compatible=raw.replace(STAGE_V3.encode(),STAGE_V4.encode(),1)
    planned=compatible.replace(ANCHOR,STAGE_B49.encode()+ANCHOR,1)
    positives=[]
    for name,value in [('frozen-original',frozen),('preserved-v2',legacy),('current-v3',raw),('compatible-v4-only',compatible),('compatible-v4-plus-B49',planned)]:
        proof=validate_builder_bytes(value,digest);positives.append(dict(name=name,sha256=sha(value),proof=proof))
    bad=[
        ('duplicate-outcomes',planned.replace(STAGE_V4.encode(),STAGE_V4.encode()*2,1)),
        ('duplicate-B49',planned.replace(STAGE_B49.encode(),STAGE_B49.encode()*2,1)),
        ('B49-without-outcomes',planned.replace(STAGE_V4.encode(),b'',1)),
        ('old-stage-with-B49',planned.replace(STAGE_V4.encode(),STAGE_V3.encode(),1)),
        ('B49-before-outcomes',compatible.replace(STAGE_V4.encode(),STAGE_B49.encode()+STAGE_V4.encode(),1)),
        ('B49-after-safety-marker',compatible.replace(ANCHOR,ANCHOR+b'\n'+STAGE_B49.encode(),1)),
        ('gap-before-B49',planned.replace(STAGE_B49.encode(),b'\n'+STAGE_B49.encode(),1)),
        ('gap-before-safety',planned.replace(ANCHOR,b'\n'+ANCHOR,1)),
        ('changed-B49-module',planned.replace(b'hodram_B49_editorial_v1 import',b'hodram_B49_editorial_v2 import',1)),
        ('changed-B49-key',planned.replace(b"profile_config.get('hodram_B49_editorial')",b"profile_config.get('unreviewed_B49')",1)),
        ('changed-B49-report-target',planned.replace(b'apply_hodram_B49_editorial(candidate, baseline',b'apply_hodram_B49_editorial(baseline, candidate',1)),
        ('changed-outcomes-module',planned.replace(b'hodram_outcomes_editorial_v4 import',b'hodram_outcomes_editorial_v5 import',1)),
        ('unowned-leading-byte',bytes([planned[0]^1])+planned[1:]),
        ('unowned-trailing-byte',planned+b'\n'),
        ('frozen-unowned-trailing-byte',frozen+b'\n'),
        ('partial-B49-stage',planned.replace(STAGE_B49.encode(),STAGE_B49.encode()[:-1],1)),
    ]
    negatives=[]
    for name,value in bad:
        assert value!=planned and value!=raw and value!=frozen and sha(value) not in {p['sha256'] for p in positives}
        try:validate_builder_bytes(value,digest)
        except ValueError as error:negatives.append(dict(name=name,sha256=sha(value),actual_changed_builder=True,rejected=True,diagnostic=str(error)))
        else:raise AssertionError('Changed builder accepted:'+name)
    assert len(positives)==5 and len(negatives)==16 and BUILDER.read_bytes()==raw
    ROOT.mkdir(parents=True);(ROOT/'current_builder.bin').write_bytes(raw);(ROOT/'frozen_original.bin').write_bytes(frozen);(ROOT/'planned_builder.bin').write_bytes(planned)
    (ROOT/'compatible_outcomes_stage.bin').write_bytes(STAGE_V4.encode());(ROOT/'B49_stage.bin').write_bytes(STAGE_B49.encode())
    save(ROOT/'exact_builder_inverse_cases.json',dict(positives=positives,negative_cases=negatives,positive_count=5,negative_count=16,all_original417_contract_dependencies_retained_unchanged=True,only_two_exact_owned_stage_texts_normalized=True,full_original_source_inverse_sha256=digest,builder_before_sha256=sha(raw),planned_builder_sha256=sha(planned),builder_andregistry_not_modified=True,compatible_outcomes_production_imports_config_alias_full_V8377_equivalence_andB49_atomic_stage_still_required=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('dk4tool/patch/hodram_outcomes_builder_guard_v3.py'),Path('translations/hodram_outcomes_native_contract_v1.json')]}))
    print('Planned builder:5 exact-stage/full-source-inverse positives,16 actualchanged-builder rejections;currentbuilder/registry unchanged.Predecessor production compatibility andB49atomic stage remainpending.')
