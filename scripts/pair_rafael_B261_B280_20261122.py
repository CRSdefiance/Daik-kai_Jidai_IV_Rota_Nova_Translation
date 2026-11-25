"""Bind Rafael's ruins riddle and arrest assignments to the registered candidate."""

from pathlib import Path

from scripts import pair_rafael_B221_B240_20261122 as prior
from scripts import register_rafael_B221_B240_20261122 as parent
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ROOT = Path("work/analysis/rafael_B261_B280_followup_20261122")
PAIRED = ROOT / "paired_source_registered_candidate.json"
EARLIER = Path("translations/rafael_B261_B280_integrated_final_review_v1.json")
source = checked_text(prior.source, {
    'range(221, 241)': 'range(261, 281)',
    'len(ready) == 270': 'len(ready) == 135',
    'for r in ready) == 7': 'for r in ready) == 5',
    'for r in ready) == 29': 'for r in ready) == 16',
    'for g in groups) == 4': 'for g in groups) == 2',
    '270 exact source and current records bound across Rafael B221–240, including seven choice labels and 29 actor-style variants.':
        '135 exact source and current records bound across Rafael B261–280, including five choice labels and 16 actor-style variants.',
})
scope = prior.scope | globals()
exec(compile(source, __file__ + "::exact-source-current-binding", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
