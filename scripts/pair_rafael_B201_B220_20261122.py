"""Bind the next Rafael town and random encounters to clean and installed records."""

from inspect import getsource
from pathlib import Path

from scripts import pair_rafael_B177_B180_20261121 as pairing
from scripts import register_rafael_B181_B187_20261121 as parent
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ROOT = Path("work/analysis/rafael_B201_B220_followup_20261122")
PAIRED = ROOT / "paired_source_registered_candidate.json"
EARLIER = Path("translations/rafael_B201_B220_integrated_final_review_v1.json")
source = checked_text(getsource(pairing.main), {
    'range(177, 181)': 'range(201, 221)',
    'len(ready) == 183': 'len(ready) == 403',
    'for r in ready) == 8': 'for r in ready) == 21',
    '183 exact source and current records bound across Rafael B177–180, including eight choice labels.':
        '403 exact source and current records bound across Rafael B201–220, including 21 choice labels.',
})
scope = vars(pairing) | globals()
exec(compile(source, __file__ + "::exact-source-current-binding", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
