"""Append the reviewed351 transaction to verified516 without inheriting its resume ticket."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/prepare_plain_SC0_registered_successor_v1.py').read_text(encoding='utf-8'), {
    "format='dk4-reviewed-rafael-plain-scene-release-v1'": "format='dk4-reviewed-rafael-mixed-scene-release-v1'",
    "    profile = deepcopy(oldprofile)": "    profile = deepcopy(oldprofile)\n    profile.pop('canonical_checkpoint_resume',None)",
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-eight-stage-preparation-one-qualified351-transaction', 'exec'), globals())
