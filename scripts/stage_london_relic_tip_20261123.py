"""Stage the reviewed London relic clue in its fixed COMMON message allocation."""

from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.common_message_table import common_message_entries
from scripts import compare_london_relic_wraps_20261123 as matrix
from scripts import register_genoa_alternate_dialogue_20261123 as parent
from scripts import stage_cartridge_title_20261123 as files
from scripts import verify_london_tavern_20261123 as london
from scripts.stage_tavern_nearby_town_wrap_20261123 import town


ROOT = Path(".codex-release-work/london_relic_tip_20261123")
ROM = ROOT / "London_Relic_Tip_STAGED.nds"
STORED = ROOT / "stored_proof.json"
MANUSCRIPT = ROOT / "reviewed_dialogue.json"
KEY = matrix.KEY
ARM, COMMON = london.ARM, london.COMMON


def render(ctx, cpu, template, args, raster, kanji):
    result = matrix.case(cpu, template, args)
    data = bytes.fromhex(result["formatted_hex"])
    pixels, glyphs = town.render_portrait(raster, ctx.arm, kanji, data)
    assert [row["code"] for row in glyphs] == town.glyph_codes(data) and len(pixels) == 228 * 64
    assert "four_row_width_bound" not in result["findings"]
    result["native_plane_sha256"] = sha256(bytes(pixels)).hexdigest()
    return pixels, result


def stage(comparison, index):
    report, discovery, release = map(files.read, (comparison, london.OUT, parent.RELEASE))
    old = release["candidate_sha256"]
    assert old == files.digest(release["candidate"]) == discovery["candidate_sha256"]
    assert old == report["registered_build"]["candidate_sha256"] and report["rendered_layouts_per_template"] == 7848
    assert release["registry_sha256"] == files.digest(files.REGISTRY) and index > 0
    assert release["clean_input_sha256"] == files.digest(files.CLEAN)
    previous, chosen = report["comparisons"][0], report["comparisons"][index]
    assert not matrix.measure(chosen["displayed_london"]["lines"]) and matrix.measure(previous["displayed_london"]["lines"])
    assert chosen["counts"]["split_qualifier_direction"] < previous["counts"]["split_qualifier_direction"]
    assert not ROOT.exists()
    ctx = matrix.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    clean = files.NdsImage.open(files.CLEAN)
    source = common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    before = london.common_rows(ctx.common, ctx.arm)
    original = before[KEY].text
    assert previous["template"] == original.decode("ascii").strip()
    revised = (b" " + chosen["template"].encode("ascii")).ljust(len(original), b" ")
    assert len(revised) == len(original) and revised.count(b"%s") == original.count(b"%s") == 5
    assert b"\n" not in revised and b"\r" not in revised
    common, after, slots = town.owned_deployment(ctx.common, ctx.arm, before, {KEY: revised})
    assert [a.message_id for a, b in zip(before, after, strict=True) if a != b] == [KEY]
    assert after[KEY].text == revised and slots[KEY]["new_null_fields"] == 0

    contents = ctx.image.rom
    ctx.image.replace_file(COMMON, common)
    result = bytes(contents.save())
    ctx.image.replace_file(COMMON, ctx.common)
    assert bytes(contents.save()) == Path(release["candidate"]).read_bytes()
    ROOT.mkdir(parents=True)
    ROM.write_bytes(result)
    stored = files.NdsImage.open(ROM)
    assert stored.read_file(COMMON) == common and stored.read_file(ARM) == ctx.arm
    assert london.common_rows(stored.read_file(COMMON), ctx.arm)[KEY].text == revised
    candidate = files.digest(ROM)
    records = []
    for row in discovery["records"]:
        key = row["message_ID"]
        jp, prior, current = source[key], before[key], after[key]
        assert jp.text.hex() == row["source_hex"] and prior.text.hex() == row["installed_hex"]
        assert current.text.count(b"%s") == prior.text.count(b"%s") == jp.text.count(b"%s")
        meaning = ("The hostess recognizes the relic and suggests looking the stated distance in each of two cardinal directions from here."
                   if key == KEY else row["rationale"])
        note = ("The opening question picks up the relic's name. The search remains tentative, anchored to the current town, and preserves both qualifiers and directions in their original order."
                if key == KEY else row["rationale"])
        records.append(dict(id=f"COMMON_MESSAGE_{key}", file_path=COMMON, message_id=key,
            english=current.text.decode("ascii").strip(), speaker=row["speaker"],
            context="Ordinary London Tavern order and the alternate conversation after another drink.",
            source_meaning=meaning, localization_note=note, review=dict.fromkeys(files.GATES, True),
            decision="revision" if key == KEY else "retention", clean_Japanese=jp.text.decode("cp932"),
            source_reference=town.reference(jp), current_reference=town.reference(prior),
            registered_reference=town.reference(current) | dict(candidate_sha256=candidate, exact_stored_hex=current.text.hex()),
            installed_hex=current.text.hex()))
    manuscript = dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
        encoder="dialogue-relocatable-v1", review_gates=list(files.GATES), records=records)
    validate_natural_dialogue_batch(manuscript)
    files.write(MANUSCRIPT, manuscript)

    cpu, _, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    raster, _, _ = town.font_tools(stored)
    kanji = stored.read_file("/GRP/KANJI.FNT")
    samples = (london.ITEM_ARGS, tuple(chosen["longest"]["arguments"]),
               ("Blue Oak Shield", "very far", "south", "very far", "west"),
               ("Sextant", "a little", "north", "a little", "east"))
    pages, figures = [], []
    for args in samples:
        for version, text in (("before", original), ("revised", revised)):
            image, layout = render(ctx, cpu, text[1:].decode("ascii"), args, raster, kanji)
            if args == london.ITEM_ARGS and version == "revised":
                assert layout["lines"] == chosen["displayed_london"]["lines"]
            pages.append(dict(version=version, arguments=args, display=layout))
            figures.append((f"{args[0]} / {version}", image))
    sheets = town.portrait_sheets(ROOT, figures)
    files.write(STORED, dict(candidate_sha256=candidate, previous_sha256=old, allocations=slots,
        target_ARM9_sha256=files.sha256(ctx.arm).hexdigest(), target_COMMON_sha256=files.sha256(common).hexdigest(),
        whole_parent_inverse=True, original_argument_count=5, comparison=files.reference(comparison),
        manuscript=files.reference(MANUSCRIPT), original_gameplay=files.reference(london.OUT),
        selected_comparison=index, samples=pages, sheets=sheets,
        baseline_wrap_counts=previous["counts"], revised_wrap_counts=chosen["counts"]))
    print(f"Staged {candidate} with only COMMON {KEY} changed.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("comparison", type=Path)
    cli.add_argument("index", type=int)
    args = cli.parse_args()
    stage(args.comparison, args.index)
