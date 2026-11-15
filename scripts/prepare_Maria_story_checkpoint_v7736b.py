"""Preserve the never-applied22-info staged checkpoint; freeze correct23-info successor."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/maria_story_checkpoint_tools_v7736b');assert not root.exists()
    provenance=derive('scripts/checkpoint_Maria_story_v7736.py','scripts/checkpoint_Maria_story_v7736b.py',{
        'v7736':'v7736b','V7736':'V7736b','v7737':'v7737b',
        '22 individually justified row-count infos':'23 individually justified row-count infos',
        "assert plans['fresh_logical_alignment_cases']==12 and plans['exact_own_current_logical_alignment_cases_reused']==256":
        "assert plans['fresh_logical_alignment_cases']==12 and plans['exact_own_current_logical_alignment_cases_reused']==256\n    assert sum('row_count_reason' in r for r in plans['records'])==23",
        'No new emulator runs orgameplay coverage wereadded.':
        'The never-applied staged7736 checkpoint andits audit remainpreserved:its summary said22 row-count infos instead ofthe actual23. This source-locked successor corrects that factual count andadds anexact gate;no prior artifact isedited orcredit changed. No new emulator runs orgameplay coverage wereadded.',
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=provenance,preserved_staged_checkpoint='work/analysis/maria_story_checkpoint_v7736/staged_checkpoint.json',
        prior_checkpoint_never_applied=True,actual_row_count_infos=23,no_ROM_orcredit_change=True,full_goal_complete=False))
    print('Preserved staged7736,never applied.Corrected successor7736b binds23 exact row-count infos.')
