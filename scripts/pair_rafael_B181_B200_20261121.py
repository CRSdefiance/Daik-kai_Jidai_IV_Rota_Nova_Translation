"""Bind the next recruitment, town, and random scenes to the registered build."""

from inspect import getsource
from pathlib import Path

from scripts import pair_rafael_B170_B176_20261121 as pairing
from scripts import register_rafael_B177_B180_20261121 as parent
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path("work/analysis/rafael_B181_B200_followup_20261121")
PAIRED = ROOT / "paired_source_registered_candidate.json"
EARLIER = Path("translations/rafael_B181_B200_integrated_final_review_v1.json")
source = checked_text(getsource(pairing.main), {
    'range(170, 177)': 'range(181, 201)',
    '== 190': '== 384',
    '190 clean Japanese and installed English records bound across Rafael B170–176.':
        '384 clean Japanese and installed English records bound across Rafael B181–200.',
})
scope = vars(pairing) | globals()
exec(compile(source, __file__ + "::exact-source-current-binding", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
