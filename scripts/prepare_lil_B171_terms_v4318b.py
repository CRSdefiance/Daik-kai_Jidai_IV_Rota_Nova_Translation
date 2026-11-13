"""Use the story row's explicit block rather than a COMMON-style source subfield."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B171_terms_tools_v4318b')

if __name__ == '__main__':
    assert not ROOT.exists()
    tool = derive('scripts/reconcile_lil_B171_terms_v4318.py', 'scripts/reconcile_lil_B171_terms_v4318b.py', {
        'lil_B171_terms_v4318': 'lil_B171_terms_v4318b',
        "assert sr['block'] == ref['block'] == 170": "assert row['block'] == ref['block'] == 170 and row['file_path']=='/data/SC2.DK4'",
    })
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tool=tool,
        correction='Story source_reference stores offset/bytes/header;its parent row stores the source block. The first reader assumed a COMMON-style nested block field and stopped before output creation. The successor binds the explicit row block,path and integrated block;no byte or editorial requirement changes.',
        failed_predecessor_preserved=True, no_ROM_registry_ledger_orcredit_change=True, full_goal_complete=False))
