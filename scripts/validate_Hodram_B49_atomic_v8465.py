"""Prove one whole-object atomic B49 commit after all independent gates in current-memory lifecycle."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import hodram_B49_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B49_release_paths_v8450 import PARENT,ROM
from scripts.verify_village_wrap_v608 import save
CONFIG='translations/hodram_B49_editorial_release_v3.json'
ROOT=Path('work/analysis/Hodram_B49_atomic_positive_v8465')
if __name__=='__main__':
    assert not ROOT.exists();parent=NdsImage.open(PARENT);image=NdsImage(owned.CANONICAL,deepcopy(parent.rom));baseline=NdsImage.open(owned.CANONICAL)
    original=image.rom;before=bytes(original.save());files=list(original.files);components={p:v for p,v in image.iter_components()};calls=[];commit=owned.commit_image
    def trapped(target,planned):
        assert target is image and target.rom is original and bytes(target.rom.save())==before and target.rom.files==files and {p:v for p,v in target.iter_components()}==components
        assert planned is not original and bytes(planned.save())==ROM.read_bytes();calls.append('one-final-whole-NDS-commit');commit(target,planned)
    owned.commit_image=trapped
    try:report=owned.apply_release(image,baseline,config=CONFIG)
    finally:owned.commit_image=commit
    assert calls==['one-final-whole-NDS-commit'] and image.rom is not original and bytes(original.save())==before and bytes(image.rom.save())==ROM.read_bytes()
    assert len(report['changed_records'])==16 and len({r['id'] for r in report['changed_records']})==16 and len(report['files'])==1
    ROOT.mkdir(parents=True);save(ROOT/'atomic_positive.json',dict(report=report,candidate_before_sha256=sha(before),planned_output_sha256=sha(ROM.read_bytes()),image_source_path=str(image.source),canonical_source_path_withcomplete_V8377_memory=True,one_complete_NDS_commit=True,original_object_identity_files_components_andserialized_bytes_exact_until_commit=True,original_object_still_exact_after_commit=True,no_ROM_written_registered_promoted_orcompletion_credit=True,semantic_precommit_challenges_andregistered_release_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path(owned.__file__),Path(CONFIG)]}))
    print('B49 atomic positive:allgates pass,onecompleteNDScommit/16manifestIDs,byte-exact testedreference;original object/files/components exact untilcommit.No disk ROM orcredit.')
