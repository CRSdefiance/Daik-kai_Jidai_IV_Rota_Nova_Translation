"""Preserve the existing one-object commit trap for the independently validated Hodram stage."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_atomic_positive_tools_v8297')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/validate_Gerhard_atomic_positive_v8256.py','scripts/validate_Hodram_atomic_positive_v8297.py',{
        'gerhard_surname_editorial_v2':'hodram_three_blocks_editorial_v1',
        'scripts.Gerhard_surname_release_paths_v8238':'scripts.Hodram_three_blocks_release_paths_v8290',
        'Gerhard_atomic_positive_v8256':'Hodram_atomic_positive_v8297',
        "len(report['changed_records'])==6 and len(report['files'])==2":"len(report['changed_records'])==28 and len(report['files'])==1",
        "report['zero_duplicate_editorial_credit']":"report['editorial_completion_credit_pending_registered_release']",
        '6manifest IDs/zero duplicatecredit':'28manifest IDs/registered completioncredit pending',
    })
    ROOT.mkdir(parents=True);save(ROOT/'whole_NDS_commit_trap_successor.json',dict(derivation=result,
        original_identity_files_ARM9_andentire_serialized_ROM_must_stay_exact_until_one_finalcommit=True,
        no_ROM_written_orregistered_newcredit0=True,full_goal_complete=False))
