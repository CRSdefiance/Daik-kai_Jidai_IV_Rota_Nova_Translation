"""Parameterize the unchanged4001-frame own-identity Rafael startup capture."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/capture_shared_tutorial_name_data_startup.py').read_text(encoding='utf-8'), {
    "ROOT = Path('work/analysis/Shared_tutorial_name_data_identity_coldboot_20261104')\nPREP = Path('work/analysis/Shared_tutorial_name_data_release_v4_20261104/registered_preparation.json')\nPARENT = Path('work/analysis/Rafael_B36_B41_release_verified_20261104/own_registered_startup_verification.json')":
        """import argparse
parser = argparse.ArgumentParser(description=__doc__)
for key in ['out','preparation','parent-startup']:
    parser.add_argument('--'+key,type=Path,required=True)
args = parser.parse_args()
ROOT, PREP, PARENT = args.out, args.preparation, args.parent_startup""",
    "prep['reference_ROM']": "prep['final_ROM']",
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-inputs-capture-andread-only-RAM-contract-CLI-paths', 'exec'), globals())
