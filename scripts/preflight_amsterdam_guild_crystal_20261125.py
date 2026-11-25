"""Prepare the Guildmaster's crystal pitch in the original dialogue allocation."""

from pathlib import Path

from scripts import stage_square_country_briefings_20261115 as town
from scripts import verify_amsterdam_london_gift_20261125 as review
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write


KEY = 3661
ROOT = Path(".codex-release-work/amsterdam_guild_crystal_20261125").resolve()
OUT = review.OUT.with_name("amsterdam_guild_crystal_preflight_20261125.json")
LINES = ("This one's a crimson crystal.", "Apparently a star pattern appears", "when you look through it.")
PROSE = " ".join(LINES)


def main():
    active = review.play.current
    release, live = map(read, (active.RELEASE, review.OUT))
    assert live["ordinary_gameplay"] and live["candidate_sha256"] == release["candidate_sha256"] == digest(active.ROM)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    row, = [r for r in live["records"] if r["message_ID"] == KEY]
    assert row["review"]["formatting"] is False
    boot = read(release["own_registered_startup"])
    ctx = town.RegisteredRuntime(active.RELEASE, release["own_registered_startup"], captain=boot["actual_captain_getter"])
    clean = NdsImage.open(CLEAN)
    jp = town.common_message_entries(clean.read_file(active.COMMON), clean.read_file(active.ARM))[KEY]
    digest_directory = sha256(ctx.arm[town.DIRECTORY_OFFSET:town.TABLE_OFFSET]).hexdigest()
    entries = town.owned_entries(ctx.common, ctx.arm, digest_directory)
    old = entries[KEY]

    def exact(entry):
        return review.panels.text_reference(entry) | {"exact_hex": entry.text.hex()}

    assert exact(jp) == row["source_reference"] and exact(old) == row["installed_reference"]
    assert all(b"%" not in x.text for x in (jp, old))
    assert not old.text.startswith(b" ")
    raw = PROSE.encode("ascii")
    assert len(raw) <= len(old.text)
    replaced, updated, slots = town.owned_deployment(ctx.common, ctx.arm, entries, {KEY: raw.ljust(len(old.text), b" ")})
    assert {r.message_id for r, s in zip(entries, updated, strict=True) if r != s} == {KEY}
    assert len(replaced) == len(ctx.common) and slots[KEY]["new_null_fields"] == 0
    target = town.with_components(ctx, ctx.arm, replaced)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    raster, _, _ = town.font_tools(ctx.image)
    data, previews = [], []
    installed_lines = tuple(row["observations"][0]["lines"])
    for title, runtime, entry, expected in (("Installed", ctx, old, installed_lines), ("Proposed", target, updated[KEY], LINES)):
        cpu, get, io = runtime.machine(ctx.arm, runtime.common, runtime.raw, runtime.plan)
        pointer = get(0x5528C, KEY)
        assert io.reads and bytes(cpu.mem_read(pointer, len(entry.text) + 1)) == entry.text + b"\0"
        body, lines = town.native_layout(cpu, entry.text, KEY, ())
        assert tuple(lines) == expected and " ".join(lines) == " ".join(entry.text.decode("ascii").split())
        plane, glyphs = town.render_portrait(raster, ctx.arm, kanji, body)
        assert [g["code"] for g in glyphs] == town.glyph_codes(body)
        assert (glyphs[0]["code"], glyphs[-1]["code"]) == (ord(expected[0][0]), ord("."))
        assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
        data.append(dict(version=title, lines=lines, page_count=1, formatted_hex=body.hex(), plane_sha256=sha256(plane).hexdigest()))
        previews.append((f"{KEY} {title}", plane))
    ROOT.mkdir(exist_ok=True)
    pictures = town.portrait_sheets(ROOT, previews)
    proposed = row | dict(english=PROSE, decision="revision proposed", proposed_reference=exact(updated[KEY]),
        localization_note="The Guildmaster identifies the crystal conversationally, keeps the star pattern as hearsay and preserves looking through the crystal. The conditional phrase stays together.",
        review=dict.fromkeys(GATES, True) | {"formatting": False})
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], source_review=reference(review.OUT),
        records=[proposed], original_allocation=slots[KEY], native_layouts=data, native_previews=pictures,
        proposed_COMMON_sha256=sha256(replaced).hexdigest(), ordinary_replay_pending=True, new_editorial_credit=0))
    print("Checked both native crystal-pitch pages within the original allocation.")


if __name__ == "__main__":
    main()
