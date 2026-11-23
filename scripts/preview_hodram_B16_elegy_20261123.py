"""Preview the two source-bound Hodram B16 stanza revisions on the native renderer."""

from types import SimpleNamespace

from PIL import Image, ImageDraw

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import review_current_story_wraps_20261122 as workflow
from scripts import verify_monster_fish_outcome_20261123 as outcome
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, sha256, write


OUT = outcome.OUT.with_name("hodram_B16_elegy_proposed_20261123.json")
SHEET = OUT.with_suffix(".png")
FIRST = '"The sea is like a mother. The waves lap in a familiar rhythm, calling to mind the heartbeat of a mother far away.'
REVISIONS = {
    "DK4_MES_B16_R0032": dict(
        english=FIRST,
        protected_phrases=["The waves lap in a familiar rhythm,", "calling to mind", "a mother far away."],
        note="The recurring waves have a familiar rhythm that seems to awaken the memory of a distant mother's heartbeat. Restore the act of remembering and keep the description of the waves together.",
    ),
    "DK4_MES_B16_R0039": dict(
        protected_phrases=["Both hold us", "as long as we live."],
        note="Keep the lifetime bond and closing quotation. Let the repeated refrain finish on its own row as it does in the preceding two stanzas, then keep Both with its verb.",
    ),
}


def main():
    observed, release, previous = map(read, (outcome.OUT, outcome.replay.RELEASE, outcome.STORY_REVIEW))
    assert observed["candidate_sha256"] == release["candidate_sha256"] == digest(release["candidate"])
    rom = NdsImage.open(release["candidate"])
    arm = rom.read_file(outcome.ARM)
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    ctx = SimpleNamespace(arm=arm)
    font = rom.read_file("/GRP/KANJI.FNT")
    paint = workflow.display.clipped_renderer(ctx)
    rows = {r["id"]: r for r in previous["records"] if r["block"] == 16}
    story = {r["id"]: r for r in observed["story"]}
    assert len(story) == len(rows) == 14
    results, images = [], []
    for key, proposal in REVISIONS.items():
        current, row = story[key], rows[key]
        old = bytes.fromhex(current["installed"]["exact_stored_hex"])
        original = bytes.fromhex(current["source"]["exact_stored_hex"])
        assert original[0] == old[0] and old[0] == 0x17
        assert " ".join(old[1:].decode("ascii").split()) == row["english"]
        revised = row | {k: v for k, v in proposal.items() if k != "note"}
        body, plan = workflow.layout.plan_progressive(revised, old[0], old[1:], original[1:])
        assert b"%" not in body and " ".join(body.decode("ascii").split()) == revised["english"]
        assert plan["expected_native_pages"] == 1 and 1 <= len(plan["lines"]) <= 4
        assert plan["lines"][0].lstrip('"') == "The sea is like a mother."
        page, = workflow.display.display.raster(ctx, font, paint, body, plan["lines"], 1)
        assert page["native_independent_plane_equal"]
        plane = bytes.fromhex(page["native_plane_hex"])
        assert len(plane) % 216 == 0
        images.append(Image.frombytes("L", (216, len(plane) // 216), plane).point(lambda v: 25 if v else 246))
        change = "wrap_only" if revised["english"] == row["english"] else "prose_and_wrap"
        results.append(dict(id=key, speaker=row["speaker"], context=row["context"], source_meaning=row["source_meaning"],
                            localization_note=proposal["note"], previous_English=row["english"], english=revised["english"],
                            protected_phrases=revised["protected_phrases"], change_class=change, decision="revision",
                            exact_source=current["source"], exact_current=current["installed"],
                            source_Japanese=current["Japanese"], candidate_body_hex=(old[:1] + body).hex(),
                            stored_control=old[:1].hex(), native_layout=plan,
                            native_page_sha256=sha256(plane).hexdigest(), before_lines=current["lines"],
                            preview_passed=True,
                            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=True)))
    assert "The waves lap in a familiar rhythm," in results[0]["native_layout"]["lines"]
    assert results[1]["native_layout"]["lines"][1].startswith("Both hold us")
    packet = dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
                  encoder="dialogue-relocatable-v1", records=results, review_gates=list(results[0]["review"]))
    validate_natural_dialogue_batch(packet)
    sheet = Image.new("RGB", (464, sum(image.height * 2 + 43 for image in images)), (29, 32, 35))
    draw = ImageDraw.Draw(sheet)
    y = 0
    for item, image in zip(results, images, strict=True):
        draw.text((15, y + 7), f"{item['id'].replace('DK4_MES_', '')} / Native proposal", fill=(255, 255, 255))
        sheet.paste(image.resize((432, image.height * 2), Image.Resampling.NEAREST).convert("RGB"), (16, y + 26))
        y += image.height * 2 + 43
    sheet.save(SHEET)
    write(OUT, packet | dict(registered_release=reference(outcome.replay.RELEASE), gameplay=reference(outcome.OUT),
                             prior_story_review=reference(outcome.STORY_REVIEW), preview=reference(SHEET),
                             retained_stanza_two=story["DK4_MES_B16_R0035"]["installed"],
                             retained_stanza_two_reason="The short attribution is a natural pause before the reported likeness of the two words. The existing refrain and final clause stay intact.",
                             stayed_within_native_216_pixel_width=True, offline_preview=True,
                             formatting_gate_scope="offline proposed pages",
                             storage_round_trip_gameplay_and_release_pending=True, new_editorial_credit=0))
    print("Native previews passed for two elegy revisions. The registered ROM remains the observed parent.")


if __name__ == "__main__":
    main()
