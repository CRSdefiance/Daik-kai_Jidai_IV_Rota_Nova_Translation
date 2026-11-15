"""Assert one whole-NDS commit and every predecessor byte unchanged before that commit."""
from pathlib import Path
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import hodram_outcomes_editorial_v4 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_outcomes_release_paths_v8347 import PARENT,ROM
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_outcome_atomic_positive_v8445')
if __name__=='__main__':
    assert not ROOT.exists();parent=NdsImage.open(PARENT);image=NdsImage(owned.CANONICAL,deepcopy(parent.rom));baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    original=image.rom;before=bytes(original.save());files=list(original.files);arm=image.read_file('/__arm9__.bin');calls=[]
    commit=owned.commit_image
    def trapped(target,planned):
        assert target is image and target.rom is original and bytes(target.rom.save())==before and target.rom.files==files and target.read_file('/__arm9__.bin')==arm
        assert planned is not original and bytes(planned.save())==ROM.read_bytes()
        calls.append('one-final-complete-NDS-object-commit');commit(target,planned)
    owned.commit_image=trapped
    try:report=owned.apply_release(image,baseline,config=owned.PRESERVED_CONFIG)
    finally:owned.commit_image=commit
    assert calls==['one-final-complete-NDS-object-commit'] and image.rom is not original and bytes(original.save())==before
    assert bytes(image.rom.save())==ROM.read_bytes() and sha(before)==sha(PARENT.read_bytes())
    assert len(report['changed_records'])==6 and len(report['files'])==1 and report['editorial_completion_credit_pending_registered_release']
    ROOT.mkdir(parents=True);save(ROOT/'one_whole_NDS_commit_exact_reference_andunchanged_precommit_input.json',dict(report=report,
        candidate_before_sha256=sha(before),image_source_path=str(image.source),canonical_source_path_with_exact_current_parent_memory=True,exact_preserved_registered_v3config_alias_used=True,compatible_v4_configuration=owned.CONFIG,planned_output_sha256=sha(ROM.read_bytes()),single_complete_NDS_commit=True,
        original_object_identity_andall_files_components_bytes_unchanged_until_commit=True,original_object_still_exact_after_commit=True,
        no_ROM_written_registered_promoted_ornew_credit=True,independent_semantic_corruption_suite_andregistered_release_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path(owned.__file__),Path(owned.CONFIG)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('PASS:one completeNDS commit only afterallgates;originalROM object exact;target byte-equal approvedreference;6manifest IDs/registered completioncredit pending.')
