"""Check Reika's revised second-drink reply in the native Tavern renderer."""

from scripts import observe_seoul_tavern_accept_20261125 as play
from scripts import stage_market_trade_dialogue_20261115 as native
from scripts import verify_seoul_tavern_accept_20261125 as review
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write


OUT = review.OUT.with_name("seoul_reika_reply_preflight_20261125.json")
KEY = 991
ENGLISH = "Are you rich? I'm jealous! Hopefully I'll meet someone nice and be happy soon, too."
EXPECTED = ["Are you rich? I'm jealous!", "Hopefully I'll meet someone nice", "and be happy soon, too."]


def main():
    release = read(play.current.RELEASE)
    ordinary = read(review.OUT)
    assert ordinary["candidate_sha256"] == digest(play.current.ROM) == release["candidate_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    row, = [row for row in ordinary["records"] if row["message_ID"] == KEY]
    assert row["decision"] == "revision_needed" and len(row["observations"]) == 1
    startup = read(release["own_registered_startup"])
    ctx = native.RegisteredRuntime(play.current.RELEASE, release["own_registered_startup"],
                                   captain=startup["actual_captain_getter"])
    arm, archive = ctx.arm, ctx.common
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(archive).hexdigest() == release["target_COMMON_sha256"]
    records = native.owned_entries(archive, arm, sha256(arm[native.DIRECTORY_OFFSET:native.TABLE_OFFSET]).hexdigest())
    clean = NdsImage.open(CLEAN)
    source = native.common_message_entries(clean.read_file(play.current.COMMON), clean.read_file(play.current.ARM))[KEY]
    assert review.review.source_ref(source) == row["source_reference"]
    old = records[KEY]
    assert review.review.source_ref(old) == row["installed_reference"]
    proposed = b" " + ENGLISH.encode("ascii")
    assert old.text.startswith(b" ") and b"%" not in source.text + old.text + proposed
    assert b"\n" not in proposed and proposed.isascii()
    deployed, rebound, slots = native.owned_deployment(archive, arm, records, {KEY: proposed})
    assert len(deployed) == len(archive)
    assert [a.message_id for a, b in zip(records, rebound, strict=True) if a.text != b.text] == [KEY]
    target = native.with_components(ctx, arm, deployed)
    font, _, _ = native.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    crops, pages = [], []
    for version, runtime, body in (("Current", ctx, old.text), ("Proposed", target, proposed)):
        cpu, getter, io = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
        stored = getter(0x5528C, KEY)
        assert bytes(cpu.mem_read(stored, len(body) + 1)) == body + b"\0" and io.reads
        formatted, lines = native.native_layout(cpu, body, KEY, ())
        assert " ".join(lines) == body.decode("ascii").strip()
        expected = row["observations"][0]["lines"] if version == "Current" else EXPECTED
        assert lines == expected, (version, lines)
        glyphs, _ = native.render_portrait(font, arm, kanji, formatted)
        pages.append(dict(version=version, page_count=1, lines=lines, formatted_hex=formatted.hex(),
                          complete_glyph_mask_sha256=sha256(glyphs).hexdigest()))
        crops.append((version, glyphs))
    preview = play.ROOT / "native_preflight"
    preview.mkdir(exist_ok=True)
    result, = native.portrait_sheets(preview, crops)
    write(OUT, dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
                    parent_candidate_sha256=release["candidate_sha256"],
                    baseline_gameplay=reference(review.OUT), proposed_COMMON_sha256=sha256(deployed).hexdigest(),
                    allocation=slots[KEY], exact_allocation_inverse=True, pages=pages, visual_review=result,
                    record=row | dict(english=ENGLISH, proposed_reference=review.review.source_ref(rebound[KEY]),
                        decision="revision_proposed",
                        localization_note="Keep Reika's direct envy and her wish to meet someone nice and be happy soon. "
                                          "The first line completes her reaction and the next line keeps the hoped-for meeting together.",
                        review=dict.fromkeys(GATES, True) | {"formatting": False}),
                    new_editorial_credit=0, paired_gameplay_pending=True, registered=False))
    print("Verified both native pages, the complete glyphs, and the unchanged COMMON allocation.")


if __name__ == "__main__":
    main()
