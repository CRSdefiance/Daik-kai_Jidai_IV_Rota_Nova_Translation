"""Check the eight wrapped descriptions in both original item delegates."""

from inspect import getsource
from struct import iter_unpack

from PIL import Image, ImageDraw

from scripts import current_item_detail_machine_v20261111 as machine
from scripts import stage_item_gallery_wraps_20261121 as stage
from scripts.prove_shachihoko_detail_fonts_v6101d import oracle
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_item_interface_research import glyph_codes


base = stage.base
PROOF = stage.ROOT / "native_item_wraps.json"
SHEET = stage.ROOT / "compact_item_wraps.png"


def make_execute(directory, arm):
    source = checked_text(machine.SOURCE, {
        "assert len(extra_sections)==2 and len(extra_sections[0].data)==4096":
            "assert len(extra_sections)==len(CURRENT_EXTRA_ITCM_SECTIONS) and len(extra_sections[0].data)==4096",
    })
    loader = checked_text(getsource(machine.make_execute), {
        "assert len(sections) == 6": "assert len(sections) == 7",
        "for s in sections[-2:]": "for s in sections[4:]",
    })
    env = vars(machine) | {"SOURCE": source}
    exec(compile(loader, __file__ + "::exact-current-item-loader", "exec"), env)
    return env["make_execute"](directory, arm)


def main():
    assert not PROOF.exists() and not SHEET.exists()
    proof = base.load(stage.PROOF)
    assert proof["candidate_sha256"] == base.digest(stage.ROM)
    image = base.NdsImage.open(stage.ROM)
    arm, common, font = (image.read_file(path) for path in (stage.ARM, stage.COMMON, "/GRP/KANJI.FNT"))
    workflow = stage.audit.stage.workflow
    directory = stage.audit.stage.native.digest(arm[workflow.DIRECTORY_OFFSET:workflow.TABLE_OFFSET])
    draw = make_execute(directory, arm)
    pixels, _ = oracle()
    cases, previews = [], []
    for row in proof["records"]:
        ident, reference = row["item_ID"], row["staged_reference"]
        for screen, config in (("main", (0, 4)), ("standalone", (0, 1))):
            for mode in (4, 16):
                native = draw(arm, "fixture", item_page=screen, item_case=config, surface_size=(240, 96),
                    kanji_font=font, mode=mode, item_resource_index=ident, item_common=common)
                offset = 36 if screen == "main" else 24
                descriptions = [d for d in native["item_draws"] if offset <= d["y"] <= offset + 24]
                assert [d["text"] for d in descriptions] == reference["lines"]
                assert descriptions[0]["pointer"] == reference["pointer"]
                assert native["item_actual_common_ids"] == [row["message_ID"]]
                glyphs = native["glyph_events"]
                assert [g["code"] for g in glyphs] == [
                    code for d in native["item_draws"] for code in glyph_codes(d["text"], d["tracking"])
                ]
                assert all(0 <= g["x"] <= 234 and 0 <= g["y"] <= 84 for g in glyphs)
                assert native["pixels"] == pixels(arm, font, glyphs, mode, background=0)
                cases.append(dict(item_ID=ident, page=screen, bitmap_mode=mode, descriptions=descriptions,
                                  exact_ink_and_bounds=True, complete_glyphs=len(glyphs)))
                if screen == "standalone" and mode == 16:
                    preview = Image.new("RGB", (256, 192))
                    preview.putdata([(242, 231, 205) if n == 0 else (22, 20, 17)
                                     for (n,) in iter_unpack("<H", native["pixels"])])
                    previews.append((ident, preview.crop((0, 0, 240, 74))))
    assert len(cases) == 32 and len(previews) == 8
    sheet = Image.new("RGB", (960, 672), "#283442")
    labels = ImageDraw.Draw(sheet)
    for i, (ident, preview) in enumerate(previews):
        x, y = 480 * (i % 2), 168 * (i // 2)
        labels.text((x + 4, y + 2), f"Item {ident:03d}", fill="white")
        sheet.paste(preview.resize((480, 148), Image.Resampling.NEAREST), (x, y + 16))
    sheet.save(SHEET)
    base.save(PROOF, dict(candidate_sha256=proof["candidate_sha256"], cases=cases,
                          sheets={str(SHEET): base.digest(SHEET)}, execution="isolated original item renderer"))
    print("Verified 32 native renders across both item views and bitmap modes.")


if __name__ == "__main__":
    main()
