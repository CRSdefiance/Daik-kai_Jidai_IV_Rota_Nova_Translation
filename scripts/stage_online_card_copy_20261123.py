"""Prepare two source-bound Online card wording revisions in their original PXL slots."""

from pathlib import Path
from re import split

from PIL import Image, ImageDraw, ImageFont

from dk4tool.graphics.pxl import PxlImage
from scripts import reconcile_promotional_display_paths_20261123 as review
from scripts.build_integrated_release import apply_pxl_label_batches


base, native, parent = review.base, review.native, review.current
ROOT = Path(".codex-release-work/online_card_copy_v2_20261123")
ROM, PROOF = ROOT / "online_card_copy_research.nds", ROOT / "stored_proof.json"
SHEET = ROOT / "proposed_cards.png"
LABELS = {
    61: ("DK4_EXTRAS_OWN_SHIP", ("number of sails", "to make one your own!"), None,
         "Ships come in a range of types and sizes. Customize materials, weapons, the number of sails, and emblems."),
    62: ("DK4_EXTRAS_VAST_WORLD", ("the Leaning Tower of Pisa",),
         "Explore 3D ruins and cities. See the pyramids. Visit the Leaning Tower of Pisa. There's a whole world to discover!",
         "The pyramids and the Leaning Tower of Pisa are examples of ruins and cities rendered in 3D. Adventure stretches out before you."),
}


def wrap_card(prose, phrases, size):
    font = ImageFont.load_default(size=size)
    sentences = split(r"(?<=[.!?]) ", prose)
    if 2 <= len(sentences) <= 5 and all(85 <= font.getlength(s) <= 220 for s in sentences):
        return sentences
    marked = prose
    for phrase in phrases:
        marked = marked.replace(phrase, phrase.replace(" ", "_"))
    lines, line = [], ""
    words = marked.split()
    for word in words:
        token = word.replace("_", " ")
        joined = f"{line} {token}".lstrip()
        if line and font.getlength(joined) > 220:
            lines.append(line)
            line = ""
        line = f"{line} {token}".lstrip()
    if line:
        lines.append(line)
    assert 2 <= len(lines) <= 5 and all(lines)
    assert " ".join(lines) == prose and all(any(phrase in line for line in lines) for phrase in phrases)
    assert all(font.getlength(line) <= 220 for line in lines)
    return lines


def render_record(path, source, current, spec):
    assert native.digest(source) == spec["clean_sha256"] and native.digest(current) == spec["installed_sha256"]
    old = Path(spec["manuscript"])
    assert base.digest(old) == spec["manuscript_sha256"]
    restored, ids = apply_pxl_label_batches([old], source)
    assert restored == current, path
    original = base.load(old)
    default, = original["records"]
    n = int(path.removesuffix(".pxl").rsplit("Online", 1)[-1])
    _, phrases, alternate, meaning = LABELS[n]
    prose = alternate or spec["working_English_revision"]
    lines = wrap_card(prose, phrases, default["maximum_size"])
    updated = default | dict(text="\n".join(lines))
    manifest = ROOT / f"online{n}_text_graphics_v2.json"
    base.save(manifest, original | dict(records=[updated]))
    target, placed = apply_pxl_label_batches([manifest], source)
    assert ids == placed and len(target) == len(source) == len(current)
    old_art, new_art = map(PxlImage.from_bytes, (current, target))
    assert target[:new_art.pixels_offset] == current[:old_art.pixels_offset]
    assert old_art.palette == new_art.palette and set(new_art.indices) == {0, 1, 15}
    mask = Image.new("L", (256, 192))
    mask.putdata([255 if index else 0 for index in new_art.indices])
    bounds = mask.getbbox()
    assert bounds and 14 <= bounds[0] < bounds[2] <= 242 and 38 <= bounds[1] < bounds[3] <= 160
    assert new_art.indices != old_art.indices
    return target, dict(id=placed[0], file_path=path, speaker="Online guide card",
        context=spec["caption_review"]["context"], english=prose, current_English=spec["current_card_English"],
        source_meaning=meaning,
        clean_reference=dict(file_sha256=spec["clean_sha256"], raster_dimensions=[256, 192]),
        current_reference=dict(file_sha256=spec["installed_sha256"], raster_dimensions=[256, 192]),
        installed_reference=dict(file_sha256=native.digest(target), raster_dimensions=[256, 192]),
        localization_note=spec["individual_source_finding"], preserved_phrases=list(phrases), rendered_lines=lines,
        all_ink_and_outline_bounds=bounds, unchanged_header_palette_and_allocation=True,
        manuscript=str(manifest), manuscript_sha256=base.digest(manifest),
        decision="revision", review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False))


def main():
    release, proof = map(base.load, (parent.RELEASE, review.OUT))
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert release["candidate_sha256"] == proof["candidate_sha256"] == base.digest(parent.ROM)
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    assert not ROM.exists() and not PROOF.exists()
    clean, parent_rom, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM, parent.ROM))
    assert native.digest(parent_rom.read_file(parent.ARM)) == release["target_ARM9_sha256"]
    assert native.digest(parent_rom.read_file(parent.COMMON)) == release["target_COMMON_sha256"]
    ROOT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new("RGB", (512, 214), "#1f2830")
    draw = ImageDraw.Draw(sheet)
    rows = []
    for n, (key, _, _, _) in LABELS.items():
        spec = proof["online_cards"][key]
        path = spec["card_path"]
        asset, row = render_record(path, clean.read_file(path), parent_rom.read_file(path), spec)
        target.replace_file(path, asset)
        rows.append(row)
        x = (n - 61) * 256
        draw.text((x + 4, 2), f"Online {n} / proposed copy", fill="white")
        sheet.paste(PxlImage.from_bytes(asset).render(), (x, 20))
    target.save(ROM)
    staged = base.NdsImage.open(ROM)
    for row in rows:
        path = row["file_path"]
        assert native.digest(staged.read_file(path)) == row["installed_reference"]["file_sha256"]
        staged.replace_file(path, parent_rom.read_file(path))
    assert bytes(staged.rom.save()) == parent.ROM.read_bytes()
    sheet.save(SHEET)
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), clean_sha256=release["clean_input_sha256"],
        predecessor_sha256=release["candidate_sha256"], exact_parent_inverse=True, records=rows,
        changed_files=[r["file_path"] for r in rows], candidate_for_verification_only=True,
        preview=dict(path=str(SHEET), sha256=base.digest(SHEET)),
        evidence={str(p): base.digest(p) for p in (parent.RELEASE, review.OUT, Path(__file__))}))
    print("Both Online card revisions fit their original PXL allocations and the exact parent inverse passes.")


if __name__ == "__main__":
    main()
