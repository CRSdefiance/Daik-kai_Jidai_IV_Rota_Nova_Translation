"""Compare the clean and registered textures that could own stored scene labels."""

from argparse import ArgumentParser
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.fls import FlsArchive
from scripts import register_tavern_nearby_town_wrap_20261123 as current


base, native = current.base, current.native
ROOT = Path(".codex-release-work/shared_movie_labels_20261123")
MOVIES = tuple(f"/FLS/M{index}.fls" for index in (*range(22, 28), *range(29, 33)))


def render_row(texture):
    raw = texture.render()
    background = Image.new("RGBA", raw.size, "#37474f")
    background.alpha_composite(raw)
    image = background.convert("RGB")
    image.thumbnail((256, 192), Image.Resampling.NEAREST)
    return image


def make_sheet(path, panels):
    width, height = 268, 220
    sheet = Image.new("RGB", (3 * width, ((len(panels) + 2) // 3) * height), "#263238")
    draw = ImageDraw.Draw(sheet)
    for number, (label, panel) in enumerate(panels):
        x, y = number % 3 * width, number // 3 * height
        draw.text((x + 6, y + 4), label, fill="white")
        sheet.paste(panel, (x + 6, y + 22))
    sheet.save(path)
    return dict(path=str(path), sha256=base.digest(path))


def inventory():
    release = base.load(current.RELEASE)
    candidate = base.digest(current.ROM)
    assert candidate == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    source, target = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    ROOT.mkdir(parents=True, exist_ok=True)
    receipts = {}
    for path in MOVIES:
        original, installed = (rom.read_file(path) for rom in (source, target))
        left, right = map(FlsArchive, (original, installed))
        assert left.count == right.count
        rows, panels = [], []
        stem = Path(path).stem
        for index in range(left.count):
            before, after = (archive.texture(index) for archive in (left, right))
            assert (before.width, before.height) == (after.width, after.height)
            same = before == after
            rows.append(dict(index=index, width=before.width, height=before.height, clean_and_installed_equal=same,
                clean_pixels_sha256=native.digest(before.render().tobytes()),
                installed_pixels_sha256=native.digest(after.render().tobytes())))
            panels.append((f"{stem} / {index} / {'both' if same else 'Japanese'}", render_row(before)))
            if not same:
                panels.append((f"{stem} / {index} / English candidate", render_row(after)))
        sheet = make_sheet(ROOT / f"{stem}_textures.png", panels)
        receipts[path] = dict(clean_archive_sha256=native.digest(original), installed_archive_sha256=native.digest(installed),
            sheet=sheet, textures=rows)
    base.save(ROOT / "texture_inventory.json", dict(candidate_sha256=candidate,
        clean_sha256=release["clean_input_sha256"], movie_archives=receipts, offline_texture_extraction=True))
    print(f"Rendered {sum(len(x['textures']) for x in receipts.values())} clean and current movie texture pairs.")


if __name__ == "__main__":
    ArgumentParser(description=__doc__).parse_args()
    inventory()
