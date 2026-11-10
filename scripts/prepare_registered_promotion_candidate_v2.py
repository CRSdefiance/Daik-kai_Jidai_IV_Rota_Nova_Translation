"""Keep registered reconstruction guards and describe the current pending batch accurately."""
from pathlib import Path

from scripts import prepare_registered_promotion_candidate_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(Path(previous.__file__).read_text(encoding='utf-8'), {
    "The next Lil361 B283–B298 source intake remains unfinished and excluded. Its clean-source packet and exact references are preserved in Git; no new prose or review credit is shipped.":
    "The next Lil361 B283–B298 batch has completed contextual prose, offline display and stored checks. Three initialized emulator runs have complete body/header pixel bindings; direct gameplay visual review, menu/transition approval, fifth gates and registered integration remain pending. Its source-first drafts, revisions, justified retentions and evidence are preserved separately in Git. This unfinished batch is excluded from the ROM and receives no new completion credit.",
})


if __name__ == '__main__':
    env = {**previous.__dict__, '__file__': __file__, '__name__': 'registered_promotion_v2'}
    exec(compile(source, __file__ + '::unchanged-reconstruction-and-release-guards', 'exec'), env)
    env['main']()
