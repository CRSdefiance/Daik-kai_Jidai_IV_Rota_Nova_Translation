"""Verify the current ordinary Ceuta voyage, including its changed random outcome."""

from collections import Counter
from pathlib import Path
from types import FunctionType, SimpleNamespace

from PIL import Image
from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import observe_ceuta_foam_20261124 as run
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, render
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.stage_tavern_nearby_town_wrap_20261123 import town


OUT = panels.OUT.with_name("ceuta_storm_and_hunger_20261124.json")
ARM, COMMON = run.current.ARM, run.current.COMMON
PACKAGES = Path("releases")
REVIEWS = {97: "20261111_sailing_alerts", 383: "20261119_sea_hazard_dialogue",
    601: "20261122_ceuta_supply_alerts", 609: "20261122_ceuta_supply_alerts"}
HOLDS = (
    (9035, 9076, 601, "Charles Rochefort", ("water",), ("No water left!",)),
    (9197, 9276, 601, "Charles Rochefort", ("food",), ("No food left!",)),
    (10263, 10280, 383, "Manuel Almeida", (), ("Admiral, a storm!",)),
    (10842, 11180, 601, "Charles Rochefort", ("water",), ("No water left!",)),
    (11639, 12180, 609, "Sailor", (), ("Ugh... My head's spinning...", "I'm so hungry... I can't go on...")),
)
FLOAT = ((10147, 10280, "Charles"), (10512, 10580, "Manuel"), (11535, 11580, "Gerhard"))


def review_for(key, jp, en):
    package = PACKAGES / f"all_routes_editorial_{REVIEWS[key]}_candidate"
    path = package / "verification/registered_review.json"
    assert digest(path) == read(package / "checksums.json")[path.relative_to(package).as_posix()]
    row, = [r for r in read(path)["records"] if r["id"] == f"COMMON_MESSAGE_{key}"]
    assert row["source_hex"] == jp.text.hex() and row["review"] == dict.fromkeys(GATES, True)
    assert row["english"].removesuffix("{PAD}").split() == en.text.decode("ascii").split()
    return dict(id=row["id"], previous_review=reference(path), clean_Japanese=jp.text.decode("cp932"),
        source_reference=panels.text_reference(jp) | dict(exact_hex=jp.text.hex()),
        installed_reference=panels.text_reference(en) | dict(exact_hex=en.text.hex()), english=row["english"],
        source_meaning=row["source_meaning"], localization_note=row["localization_note"], review=row["review"],
        decision="retention", holds=[])


def floating_match(raster, arm, kanji, screen, phrase):
    data = phrase.encode("ascii")
    ink, glyphs = render(raster, arm, kanji, data)
    assert [glyph["code"] for glyph in glyphs] == list(data.replace(b" ", b""))
    plane = Image.frombytes("L", (228, 48), bytes(p == 1 for p in ink))
    bbox = plane.getbbox()
    pixels = plane.crop(bbox).tobytes()
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    view = screen.crop((64, 237, 224, 289))
    foreground = Image.frombytes("L", view.size, bytes(pixel == (0, 8, 0) for pixel in view.get_flattened_data()))
    matches = [(x, y) for y in range(foreground.height - h + 1) for x in range(foreground.width - w + 1)
               if foreground.crop((x, y, x + w, y + h)).tobytes() == pixels]
    assert len(matches) == 1, phrase
    (x, y), = matches
    return dict(complete_foreground_sha256=sha256(pixels).hexdigest(), bounds=(x+64, y+237, x+64+w, y+237+h))


def portrait_match(pixels, screen):
    predicted = Image.frombytes("L", (228, 64), bytes(bool(p) for p in pixels))
    actual = Image.frombytes("L", (228, 64), bytes(color == (0, 8, 0)
        for color in screen.crop((16, 296, 244, 360)).get_flattened_data()))
    bound, observed = predicted.getbbox(), actual.getbbox()
    assert bound is not None and observed is not None
    assert predicted.crop(bound).size == actual.crop(observed).size
    assert predicted.crop(bound).tobytes() == actual.crop(observed).tobytes()
    return dict(preview_ink_bounds=bound, observed_ink_bounds=observed,
        original_origin_delta=(observed[0] - bound[0], observed[1] - bound[1]))


def main():
    release = read(run.current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(run.current.ROM) == release["candidate_sha256"]
    capture = FunctionType(panels.capture.__code__, vars(panels) | {"observed": SimpleNamespace(ROOT=run.ROOT.parent)})
    _, calls, evidence = capture(run.ROOT.name, release)
    timeline = read(evidence["capture"]["path"])
    assert timeline["frames"] == 12580
    captures = {row["frame"]: row for row in timeline["frames_captured"]}
    trace = {}
    for a, b in zip(calls[::2], calls[1::2], strict=True):
        assert a["PC"] == 0x0205528C and b == a | {"PC": 0x020534F4}
        trace[a["frame"], a["message_ID"]] = a
    counts = Counter(row["message_ID"] for row in calls[::2])
    assert counts == {85: 1, 86: 1, 97: 9, 601: 3, 383: 1, 609: 1}
    assert not counts.keys() & {284, 318, 750, 751, 752}
    ctx = RegisteredRuntime(run.current.RELEASE, release["own_registered_startup"], captain=3)
    cpu, _, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    clean = NdsImage.open(CLEAN)
    source = panels.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    en = common_rows(ctx.common, ctx.arm)
    records = {key: review_for(key, source[key], en[key]) for key in REVIEWS}
    native_raster, _, _ = town.font_tools(ctx.image)
    floating_raster = font_tools(ctx.image)[0]
    font = GameAsciiFont.from_arm9(ctx.arm)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    photos = []
    for request, frame, key, speaker, values, expected in HOLDS:
        a = trace[request, key]
        assert source[key].text.count(b"%s") == en[key].text.count(b"%s") == len(values)
        raw, lines = town.native_layout(cpu, en[key].text, key, values, parent=a["caller_LR"] + 0x1C)
        assert tuple(lines) == expected
        pixels, glyphs = town.render_portrait(native_raster, ctx.arm, kanji, raw)
        assert [g["code"] for g in glyphs] == town.glyph_codes(raw)
        screen = panels.picture(captures[frame])
        placement = portrait_match(pixels, screen)
        body_ink_pixels = panels.exact_body(font, lines, screen)
        nameplate = panels.nameplate(font, speaker, screen)
        records[key]["holds"].append(dict(request=a, capture=captures[frame], arguments=values, speaker=speaker,
            nameplate=nameplate, lines=lines, complete_native_preview_sha256=sha256(bytes(pixels)).hexdigest(),
            whole_body_glyph_ink_pixels=body_ink_pixels, placement=placement))
        photos.append((f"{frame} / {speaker}", screen))
    for request, frame, name in FLOAT:
        a = trace[request, 97]
        assert a["caller_LR"] == 0x0207E3E3 and source[97].text.count(b"%s") == 1
        line = (en[97].text % name.encode("ascii")).decode("ascii").strip()
        match = floating_match(floating_raster, ctx.arm, kanji, panels.picture(captures[frame]), line)
        records[97]["holds"].append(dict(request=a, capture=captures[frame], name=name, line=line, native=match))
    for frame in (10580, 12580):
        panels.find_mask(font, "Sea View", panels.picture(captures[frame]), (96, 0, 161, 15))
    sheets = FunctionType(panels.sheets_for.__code__, vars(panels) | {"OUT": OUT})
    report = dict(candidate_sha256=release["candidate_sha256"], ordinary_existing_Ceuta_save=True, evidence=evidence,
        original_sea_foam_reference=reference(run.PROOF), changed_natural_outcome=True, observed_foam=False,
        trace_counts=dict(counts), source_records=list(records.values()), rendered_portrait_holds=len(HOLDS),
        floating_notice_holds=len(FLOAT), sea_returns=[captures[n] for n in (10580, 12580)],
        sheets=sheets("ceuta_storm_and_hunger", photos, (0, 272, 256, 380)),
        new_editorial_credit=0, ROM_changed=False, conditional_sample_only=True)
    write(OUT, report)
    print(f"Verified {len(HOLDS)} portrait panels, {len(FLOAT)} floating notices and both returns to sailing.")


if __name__ == "__main__":
    main()
