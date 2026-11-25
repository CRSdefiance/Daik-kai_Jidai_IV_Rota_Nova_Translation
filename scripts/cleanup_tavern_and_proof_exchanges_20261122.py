"""Refresh the current wrap queue and clear redundant tavern checkpoint artifacts."""

from inspect import getsource

from scripts import cleanup_rafael_diplomacy_and_friends_20261122 as precedent
from scripts import refresh_story_wrap_queue_20261122 as prior_queue
from scripts import register_tavern_and_proof_exchanges_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.draft.ROOT / "current_wrap_queue.json"
refresh_source = checked_text(getsource(prior_queue.main), {
    '(current.parent.REVIEW, current.REVIEW)': '(current.parent.parent.REVIEW, current.parent.REVIEW, current.REVIEW)',
})
queue_scope = vars(prior_queue) | {"current": release, "OUTPUT": QUEUE}
exec(compile(refresh_source, __file__ + "::current-wrap-queue", "exec"), queue_scope)

cleanup_source = checked_text(precedent.source, {
    'fixture = base.load(release.live.ROOT / "fixture.json")': 'fixture = base.load(release.live.ROM.with_name("fixture.json"))',
    'fixture["fixture_ROM"]': 'fixture["fixture"]',
    'fixture["fixture_ROM_sha256"]': 'fixture["fixture_sha256"]',
    'release_stack_with_rafael_diplomacy_and_friends.json': 'release_stack_with_tavern_and_proof_exchanges.json',
})
handoff_source = checked_text(precedent.handoff_source, {
    'queue.OUTPUT': 'QUEUE',
    'The Pereira negotiations, Eirene conversation and Charlotte village scenes account for 268 retrospective decisions. Thirteen lines have new wording, 15 have wrap fixes and 240 have justified retentions. All 28 changed panels passed native visual checks, and five changed panels and five retained panels played with intact speaker labels in a focused Rafael replay. The other 23 changed panels have offline display evidence.':
        'The review covers 203 spoken turns and eight choice labels. Fourteen lines have revised wording, 18 have improved wraps and 171 have justified retentions. Seven changed and eight retained panels played with intact speaker labels in a focused Hodram replay. Mikhail’s joke went from two pages to one and advanced directly to Hodram’s reply. The other 25 changed turns, including Maria’s lines, have offline display evidence.',
})
scope = precedent.scope | globals()
scope["workflow"] = release.parent.scope["workflow"]
for program in (cleanup_source, handoff_source):
    exec(compile(program, __file__ + "::cleanup", "exec"), scope)


if __name__ == "__main__":
    if not QUEUE.exists():
        queue_scope["main"]()
    scope["handoff"](scope["cleanup"]())
