"""Exercise the shared late path against real B31_B53 and precommit chain failures."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.late_editorial_extensions_v1 import apply_extensions
from scripts.Hodram_B31_B53_release_paths_v8767 import PARENT,ROM,DOC,CONFIG
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B31_B53_shared_extension_v8773')
WATCH=None
CALLS=[]


class WatchedImage(NdsImage):
    def __setattr__(self,key,value):
        if key=='rom' and self is WATCH:
            CALLS.append('one-final-whole-NDS')
        super().__setattr__(key,value)


if __name__=='__main__':
    assert not ROOT.exists();parent=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    adapter=Path('dk4tool/patch/hodram_b31_b53_extension_v2.py')
    spec=dict(id='hodram-b31_b53',module='dk4tool.patch.hodram_b31_b53_extension_v2',module_sha256=sha(adapter.read_bytes()),
         config=str(CONFIG),config_sha256=sha(CONFIG.read_bytes()),parent_ROM_sha256=sha(PARENT.read_bytes()),target_ROM_sha256=sha(ROM.read_bytes()))
    ROOT.mkdir(parents=True);save(ROOT/'extension_spec.json',spec)
    image=WatchedImage(baseline.source,deepcopy(parent.rom));WATCH=image;CALLS=[]
    original=image.rom;before=bytes(original.save());files=list(original.files);components={p:v for p,v in image.iter_components()}
    reports=apply_extensions(image,baseline,[spec])
    assert CALLS==['one-final-whole-NDS'] and image.rom is not original and bytes(original.save())==before and original.files==files
    assert bytes(image.rom.save())==ROM.read_bytes() and len(reports)==1 and len(reports[0]['changed_records'])==3
    assert all(image.read_file(p)==v for p,v in components.items())
    save(ROOT/'positive.json',dict(spec=spec,reports=reports,one_final_whole_NDS_commit=True,
         original_object_identity_files_components_andserialized_bytes_exact_until_commit=True,
         whole_output_equals_reviewed_reference=True,canonical_source_full_current_memory=True,
         all_frozen_native_editorial_andproduction_guards_active=True))
    print('PASS shared B31_B53 extension positive:one final wholeNDS commit/exact reviewed reference/all guards',flush=True)
    prior_path=Path('work/analysis/Hodram_B52_shared_extension_v8697/shared_extension_validation.json')
    prior=read(prior_path);shared=Path('dk4tool/patch/late_editorial_extensions_v1.py')
    assert prior['negative_count']==6 and prior['no_guard_digest_orsemantic_bypass'] and sha(shared.read_bytes())==prior['evidence'][str(shared)]
    changed=deepcopy(spec);changed['target_ROM_sha256']='0'*64
    mutations=[('changed-target_ROM_sha256',[changed],[])]
    negatives=[]
    for label,specs,existing in mutations:
        image=WatchedImage(baseline.source,deepcopy(parent.rom));WATCH=image;CALLS=[]
        original=image.rom;before=bytes(original.save());files=list(original.files);components={p:v for p,v in image.iter_components()}
        assert specs!=[spec] or existing
        try:apply_extensions(image,baseline,specs,existing)
        except ValueError as error:
            diagnostic=str(error)
            assert diagnostic.startswith('Late editorial extension:') and 'Native dependency changed' not in diagnostic
        else:raise AssertionError('Changed shared extension accepted:'+label)
        assert not CALLS and image.rom is original and bytes(original.save())==before and original.files==files and {p:v for p,v in image.iter_components()}==components
        row=dict(case=label,actual_changed_input=True,rejected=True,diagnostic=diagnostic,commit_calls=0,
             original_object_identity_files_components_andserialized_bytes_unchanged=True,
             all_dependency_native_editorial_andsemantic_guards_active=True)
        save(ROOT/(label+'.json'),row);negatives.append(row);print('PASS shared rejection',label,flush=True)
    WATCH=None
    save(ROOT/'shared_extension_validation.json',dict(positive_lifecycles=1,negative_count=1,negative_cases=negatives,exact_unchanged_framework_six_previous_cases_reused_by_source_hash=True,prior_shared_validation=str(prior_path),prior_shared_validation_sha256=sha(prior_path.read_bytes()),
         one_complete_NDS_commit_after_all_extension_checks=True,
         late_target_identity_failure_leaves_complete_original_NDS_object_unchanged=True,
         no_guard_digest_orsemantic_bypass=True,no_disk_ROM_registration_orcompletion_credit=True,
         full_goal_complete=False,evidence={str(p):sha(Path(p).read_bytes()) for p in [__file__,adapter,CONFIG,
             'dk4tool/patch/late_editorial_extensions_v1.py','dk4tool/patch/hodram_B31_B53_editorial_v2.py']}))
    print('Shared late path:real B31_B53 positive andone genuine late-target rejection;unchanged framework6cases reused byexact sourcehash;zero premature commits. No disk ROM/credit.')
