"""Verify Reika's reflow and the unchanged Seoul screens on the staged ROM."""

from types import FunctionType, SimpleNamespace

from PIL import ImageChops
from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_seoul_reika_20261125 as play
from scripts import verify_seoul_tavern_accept_20261125 as baseline
from scripts.stage_azores_wording_20261123 import common_rows
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, sha256, write


OUT = baseline.OUT.with_name("seoul_reika_reply_paired_20261125.json")
HOLD = 15560


def main():
    stored, draft, prior = map(read, (play.STAGED, play.draft.OUT, baseline.OUT))
    assert stored["candidate_sha256"] == digest(play.ROM) and stored["exact_parent_inverse"]
    assert stored["proposal"] == reference(play.draft.OUT)
    assert prior["candidate_sha256"] == draft["parent_candidate_sha256"]
    scope = vars(baseline.PANELS) | dict(observed=SimpleNamespace(ROOT=play.ROOT))
    after, calls, evidence = FunctionType(baseline.PANELS.capture.__code__, scope)(play.CAPTURE.name, stored)
    old_refs = prior["evidence"]
    assert all(reference(ref["path"]) == ref for ref in old_refs.values())
    previous, revised = (read(refs["capture"]["path"]) for refs in (old_refs, evidence))
    assert old_refs["donor"] == evidence["donor"]
    assert previous["scripted_input_schedule"] == revised["scripted_input_schedule"]
    old_nav, new_nav = (read(refs["journal"]["path"]) for refs in (old_refs, evidence))
    assert old_nav["commands_received"] == new_nav["commands_received"]
    assert calls == read(old_refs["trace"]["path"])["source_requests"]
    before = baseline.PANELS.shots(previous, "_navigation.png")
    assert before.keys() == after.keys() and HOLD in after
    matching = sorted(n for n in after if n != HOLD)
    assert all(before[n]["framebuffer_sha256"] == after[n]["framebuffer_sha256"] for n in matching)
    original, modified = (baseline.previous.captured(frames[HOLD]) for frames in (before, after))
    delta = ImageChops.difference(original, modified)
    bounds = delta.getbbox()
    assert bounds is not None
    delta.paste((0, 0, 0), (16, 296, 245, 360))
    assert delta.getbbox() is None

    rom = NdsImage.open(play.ROM)
    arm, archive = (rom.read_file(path) for path in (play.play.current.ARM, play.play.current.COMMON))
    assert sha256(arm).hexdigest() == stored["target_ARM9_sha256"]
    assert sha256(archive).hexdigest() == draft["proposed_COMMON_sha256"] == stored["target_COMMON_sha256"]
    installed = common_rows(archive, arm)[play.draft.KEY]
    assert baseline.review.source_ref(installed) == draft["record"]["proposed_reference"]
    font = GameAsciiFont.from_arm9(arm)
    lines = play.draft.EXPECTED
    body = baseline.PANELS.exact_body(font, lines, modified)
    speaker = baseline.PANELS.nameplate(font, "Reika", modified)
    shot = baseline.sheet({0: original, 1: modified}, ((0, "Lisbon parent"), (1, "Staged Reika reply")), "paired")
    write(OUT, dict(candidate=reference(play.ROM), source_review=reference(play.draft.OUT), ordinary_gameplay=True,
        parent_hold=before[HOLD], revised_hold=after[HOLD], difference_box=bounds, matching_navigation_frames=matching,
        exact_body=body, exact_nameplate=speaker, lines=lines, evidence=evidence, sheet=shot,
        registered=False, new_editorial_credit=0))
    print(f"Verified the revised Reika reply, complete nameplate, and {len(matching)} matching companion screens.")


if __name__ == "__main__":
    main()
