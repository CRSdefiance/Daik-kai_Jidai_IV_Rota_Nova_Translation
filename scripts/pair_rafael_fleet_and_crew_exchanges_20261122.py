"""Bind the following full Rafael fleet and crew conversations for review."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import cleanup_rafael_charlotte_and_maria_20261122 as checkpoint
from scripts import pair_rafael_charlotte_and_maria_20261122 as prior
from scripts import register_rafael_charlotte_and_maria_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base = prior.base
BLOCKS = {74: 8, 81: 51, 83: 85, 87: 42, 90: 10, 97: 28}
EARLIER = tuple(Path("translations") / f"rafael_{part}_contextual_final_review_v1.json"
                for part in ("B61_B80", "B81_B84", "B85_B100"))
OUTPUT = Path("translations/editorial_checkpoints/rafael_fleet_and_crew_exchanges_20261122/paired_source.json")
scope = vars(prior) | globals()
scope["scene_packet"] = FunctionType(prior.scene_packet.__code__, scope)
source = checked_text(getsource(prior.main), {
    'older = base.load(EARLIER)["records"]':
        'older = [record for path in EARLIER for record in base.load(path)["records"]]',
    'sum(len(group["open_wrap_leads"]) for group in groups) == 8':
        'sum(len(group["open_wrap_leads"]) for group in groups) == 12',
    'earlier_review=str(EARLIER), earlier_review_sha256=base.digest(EARLIER)':
        'earlier_reviews={str(path):base.digest(path) for path in EARLIER}',
    'Bound 134 texts and eight wrap leads in four complete Rafael exchanges.':
        'Bound 224 texts and twelve wrap leads in six full Rafael exchanges.',
})
exec(compile(source, __file__ + "::source-packet", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
