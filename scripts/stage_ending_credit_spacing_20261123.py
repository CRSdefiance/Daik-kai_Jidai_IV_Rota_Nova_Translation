"""Prepare source-bound spacing corrections in the four existing ending credit textures."""

from collections import Counter
from pathlib import Path

from dk4tool.graphics.fls import FlsArchive
from scripts import register_tavern_drink_reply_20261123 as parent


base, native = parent.base, parent.native
ROOT = Path(".codex-release-work/ending_credit_spacing_20261123")
ROM, PROOF = ROOT / "ending_credit_spacing_research.nds", ROOT / "stored_proof.json"
ORIGINAL = "SpecialThanks : BRIDGE Inc."
ENGLISH = "Special Thanks: BRIDGE Inc."
ROUTES = (("Rafael", 29, 6), ("Hodram", 30, 10), ("Lil", 31, 8), ("Maria", 32, 6))
EARLIER = Path("work/analysis/ending_transitions_v642/preflight.json")
ORIGINAL_INK = "3546eda32f7363b7786544e8ee7c2306f8c7101f8ea50268b408d2b5565b219a"
THANKS = (89, 123)
SPACE = 6


def layout(texture):
    source = bytes(texture.indices)
    assert (texture.width, texture.height) == (256, 16)
    assert Counter(source) == {0: 2829, 15: 306, 255: 961}
    assert texture.palette[0][:3] == texture.palette[255][:3] == (0, 0, 0)
    assert texture.palette[15][:3] == (255, 255, 255)
    left, right = THANKS
    revised = bytearray(source)
    for row in range(texture.height):
        start = row * texture.width
        word = source[start + left:start + right]
        blank = source[start + right:start + right + SPACE]
        assert set(blank) == {0 if row else 255}
        revised[start + left:start + right + SPACE] = blank + word
    assert Counter(revised) == Counter(source)
    assert all(not v or v == 255 for y in range(texture.height)
        for v in revised[y * texture.width + left:y * texture.width + left + SPACE])
    return revised


def replace_credit(data, index):
    fls = FlsArchive(data)
    texture = fls.texture(index)
    assert native.digest(bytes(texture.indices)) == ORIGINAL_INK
    assert (fls.records[index][0] >> 16, fls.records[index][1] & 0xFFFF) == (256, 16)
    texture.indices[:] = layout(texture)
    revised = fls.to_bytes()
    start, size = fls.records[index][4:]
    start += fls.data_offset
    assert len(revised) == len(data)
    assert revised[:start] == data[:start] and revised[start + size:] == data[start + size:]
    reread = FlsArchive(revised)
    assert reread.records == fls.records and reread.texture(index) == texture
    return revised, dict(slot_offset=start, slot_bytes=size,
        source_texture_sha256=ORIGINAL_INK, installed_texture_sha256=native.digest(bytes(texture.indices)),
        palette_storage_unchanged=True, visible_dimensions=[256, 16], original_white_glyph_pixels=306)


def stage():
    assert not ROM.exists() and not PROOF.exists()
    release, earlier = map(base.load, (parent.RELEASE, EARLIER))
    assert base.digest(parent.ROM) == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    clean, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM))
    arm, clean_arm = target.read_file(parent.ARM), clean.read_file(parent.ARM)
    assert native.digest(arm) == release["target_ARM9_sha256"]
    ranges = []
    for spec in earlier["original_code_ranges"][:9]:
        lo, hi = spec["offset"]
        assert arm[lo:hi] == clean_arm[lo:hi] and native.digest(arm[lo:hi]) == spec["sha256"]
        ranges.append(spec)
    rows, originals, updates = [], {}, {}
    for captain, movie, index in ROUTES:
        path = f"/FLS/M{movie}.fls"
        original = clean.read_file(path)
        assert original == target.read_file(path)
        source_hash = native.digest(original)
        assert source_hash == earlier["original_ending_movies"][path]
        result, layout_proof = replace_credit(original, index)
        originals[path], updates[path] = original, result
        rows.append(dict(id=f"M{movie}_ENDING_CREDIT_{index}", file_path=path, captain=captain,
            texture_index=index, context="Company acknowledgement after the Fin card in the original ending.",
            source_meaning="The original English credit gives special thanks to BRIDGE Inc.",
            speaker="Ending credit", source_English=ORIGINAL, current_English=ORIGINAL, english=ENGLISH,
            decision="revision", localization_note="Separate the two words and attach the colon to the label.",
            source_reference=dict(archive_sha256=source_hash, texture_index=index),
            current_reference=dict(archive_sha256=source_hash, texture_index=index),
            installed_reference=dict(archive_sha256=native.digest(result), texture_index=index),
            layout=layout_proof,
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
        target.replace_file(path, result)
    ROOT.mkdir(parents=True, exist_ok=True)
    target.save(ROM)
    staged = base.NdsImage.open(ROM)
    for path, data in updates.items():
        assert staged.read_file(path) == data
        staged.replace_file(path, originals[path])
    assert bytes(staged.rom.save()) == parent.ROM.read_bytes()
    base.save(PROOF, dict(clean_sha256=release["clean_input_sha256"], candidate_sha256=base.digest(ROM),
        predecessor_sha256=release["candidate_sha256"], records=rows, native_code_dependencies=ranges,
        exact_parent_inverse=True, changed_files=list(updates), offline=True,
        evidence={str(path): base.digest(path) for path in (EARLIER, parent.RELEASE, Path(__file__))}))
    print("Prepared the four credit textures in their original slots and verified the complete predecessor inverse.")


if __name__ == "__main__":
    stage()
