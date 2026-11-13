"""Prove one whole-object B52 commit in both direct and canonical-source/current-memory lifecycles."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import hodram_B52_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B52_release_paths_v8693 import PARENT,ROM,CONFIG
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/Hodram_B52_atomic_positive_v8690b')
if __name__=='__main__':
    assert not ROOT.exists();parent=NdsImage.open(PARENT);baseline=NdsImage.open(owned.CANONICAL);results=[];ROOT.mkdir(parents=True)
    for mode in ['direct-current','canonical-source-full-current-memory']:
        image=NdsImage(PARENT if mode=='direct-current' else owned.CANONICAL,deepcopy(parent.rom))
        original=image.rom;before=bytes(original.save());files=list(original.files);components={p:v for p,v in image.iter_components()};calls=[];commit=owned.commit_image
        def trapped(target,planned):
            assert target is image and target.rom is original and bytes(original.save())==before and original.files==files and {p:v for p,v in target.iter_components()}==components
            assert planned is not original and bytes(planned.save())==ROM.read_bytes();calls.append('one-final-whole-NDS-commit');commit(target,planned)
        owned.commit_image=trapped
        try:report=owned.apply_release(image,baseline,config=CONFIG)
        finally:owned.commit_image=commit
        assert calls==['one-final-whole-NDS-commit'] and image.rom is not original and bytes(original.save())==before and bytes(image.rom.save())==ROM.read_bytes()
        assert len(report['changed_records'])==len({r['id'] for r in report['changed_records']})==5 and len(report['files'])==1
        row=dict(mode=mode,report=report,candidate_before_sha256=sha(before),planned_output_sha256=sha(ROM.read_bytes()),image_source_path=str(image.source),one_complete_NDS_commit=True,original_object_identity_files_components_andserialized_bytes_exact_until_commit=True,original_object_still_exact_after_commit=True)
        save(ROOT/(mode+'.json'),row);results.append(row);print('PASS B52 atomic positive',mode,flush=True)
    save(ROOT/'atomic_positive.json',dict(cases=results,positive_lifecycles=2,one_complete_NDS_commit_percase=True,whole_output_equals_tested_reference=True,all_native_semantic_production_guards_enabled=True,no_ROM_written_registered_promoted_orcompletion_credit=True,semantic_precommit_challenges_andregistered_release_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path(owned.__file__),CONFIG]}))
    print('B52 atomic positive:both input lifecycles/all gates pass;onewholeNDScommit/5IDs each,exacttestedreference;original objects unchanged untilcommit.No disk ROM/credit.')
