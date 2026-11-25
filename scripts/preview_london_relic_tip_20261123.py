"""Preview the source-based London relic hint on the current native consumer."""

from hashlib import sha256
from pathlib import Path

from scripts import verify_london_tavern_20261123 as london
from scripts.probe_tavern_conversations_v764 import format_case
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_tavern_nearby_town_wrap_20261123 import town


SAMPLES = (
    ("observed shield", london.ITEM_ARGS),
    ("two long qualifiers", ("Blue Oak Shield", "very far", "south", "very far", "west")),
    ("long name, short distances", ("Aristarchus Telescope", "a little", "north", "a little", "east")),
    ("long name, long distances", ("Aristarchus Telescope", "very far", "south", "very far", "west")),
)
OUT = london.OUT.with_name("london_relic_tip_native_preview_20261123.json")
KEY = 843


def main():
    receipt = london.observed.current.RELEASE
    release, observed = map(london.read, (receipt, london.OUT))
    assert release["candidate_sha256"] == observed["candidate_sha256"]
    ctx = RegisteredRuntime(receipt, release["own_registered_startup"], captain=3)
    u, _, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    installed = london.common_rows(ctx.common, ctx.arm)[KEY]
    evidence, = (row for row in observed["records"] if row["message_ID"] == KEY)
    assert installed.text.hex() == evidence["installed_hex"] and installed.text.startswith(b" ")
    revision = b" " + evidence["proposal"].encode("ascii")
    assert len(revision) <= len(installed.text) and revision.count(b"%s") == installed.text.count(b"%s") == 5
    padded = revision.ljust(len(installed.text), b" ")
    raster, _, _ = town.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    cases, figures = [], []
    for label, args in SAMPLES:
        results = {}
        for status, template in (("installed", installed.text), ("draft", padded)):
            result = format_case(u, dict(message_id=KEY, english=template[1:].decode("ascii")),
                                 [s.encode("ascii") for s in args])
            encoded = bytes.fromhex(result["formatted_hex"])
            pixels, glyphs = town.render_portrait(raster, ctx.arm, kanji, encoded)
            assert [row["code"] for row in glyphs] == town.glyph_codes(encoded)
            assert len(pixels) == 228 * 64
            result["native_plane_sha256"] = sha256(bytes(pixels)).hexdigest()
            result["qualifier_cut"] = any(
                line.endswith((" far", " little")) and following.startswith(("north", "south", "east", "west"))
                for line, following in zip(result["lines"], result["lines"][1:])
            )
            results[status] = result
            figures.append((f"{label} / {status}", pixels))
        cases.append(dict(label=label, arguments=args, **results))
    before, after = cases[0]["installed"], cases[0]["draft"]
    assert before["lines"] == list(evidence["lines"]) and before["qualifier_cut"]
    assert after["lines"] == ["Blue Oak Shield? I know the one.", "Try far south and far west of here."]
    assert not any(case["draft"]["findings"] for case in cases)
    preview, = town.portrait_sheets(london.observed.ROOT, figures)
    saved = OUT.with_suffix(".png")
    Path(preview["path"]).replace(saved)
    london.write(OUT, dict(registered_build=ctx.receipt(), live_evidence=london.reference(london.OUT),
        installed_hex=installed.text.hex(), exact_fixed_length_draft_hex=padded.hex(),
        sample_results=cases, contact_sheet=london.reference(saved),
        storage_changed=False, remaining_work=["Review the complete direction and item-name domain.",
            "Resolve the remaining qualifier wrap in the long-distance sample before registration."]))
    print("The proposed shield tip fits in two native rows. A longer qualifier pair still splits.")


if __name__ == "__main__":
    main()
