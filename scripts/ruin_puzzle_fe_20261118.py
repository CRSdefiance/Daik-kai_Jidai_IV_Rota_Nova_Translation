"""Fit the two ruin inscriptions with the original four-row FE painter."""

from itertools import combinations
from types import FunctionType

from dk4tool.dialogue.codec import parse_markup, tokens_to_bytes
from dk4tool.patch.grand_race_menu_release import sha
from scripts import Rafael_B45_FE_source_painter_v7894 as fe
from scripts import square_shopkeeper_font_oracles_v7020 as font
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows

QUESTION = "A vessel is filled to the brim with water. Ice floats on top. When it melts, what happens to the water level?"
DIRECTIONS = "Press the front stone for a rise, left for a fall, or right for no change."
INSCRIPTIONS = {
    "question": (QUESTION, ("filled to the brim", "Ice floats on top.", "When it melts,", "water level?")),
    "directions": (DIRECTIONS, ("Press the front stone for a rise,", "left for a fall,", "or right for no change.")),
}


def native_painter(ctx):
    identity = {"CURRENT_ARM9": sha(ctx.arm)}
    ascii_factory = FunctionType(font.make_painter.__code__, vars(font) | identity)
    factory = FunctionType(fe.make_source_painter.__code__, vars(fe) | identity | {"ASCII_painter": ascii_factory})
    return factory(ctx.image)[0]


def candidate_rows(paragraph, phrases):
    words = paragraph.split()
    opportunities = range(1, len(words))
    candidates = []
    for count in range(1, 5):
        for cuts in combinations(opportunities, count - 1):
            lines = [" ".join(words[a:b]) for a, b in zip((0, *cuts), (*cuts, len(words)), strict=True)]
            if any(len(line) > 36 for line in lines):
                continue
            if not all(any(phrase in line for line in lines) for phrase in phrases):
                continue
            markup = "{SPEAKER:FE}" + "{LB}".join(lines)
            raw = tokens_to_bytes(parse_markup(markup), guard_linebreaks=True, pair_phase_safe_breaks=True)
            weak_endings = {"a", "an", "the", "to", "with", "of", "it"}
            # Keep phrase boundaries first, then prefer the fullest rows.
            weak = sum(line.split()[-1] in weak_endings for line in lines[:-1])
            sparse = sum(len(line) < 13 and not line.endswith((".", "?", "!")) for line in lines[:-1])
            density = sum((36 - len(line)) ** 2 for line in lines[:-1])
            candidates.append(((weak, sparse, count, density), lines, raw))
    return sorted(candidates)


def visible_events(rendered):
    return [event for event in rendered["events"] if event["code"] != 32]


def revise(row, role, painter, expand):
    paragraph, phrases = INSCRIPTIONS[role]
    current = bytes.fromhex(row["current_hex"])
    assert current[0] == 254 and paragraph.isascii()
    assert not any(token in current[1:] for token in (b"FI", b"FA", b"FO", b"FU", b"%"))
    for _, lines, compiled in candidate_rows(paragraph, phrases):
        if len(compiled) > len(current):
            continue
        target = compiled.ljust(len(current), b" ")
        try:
            normal, stored = painter(compiled[1:]), painter(target[1:])
            membership = check_FE_rows(compiled[1:], normal)
        except AssertionError:
            continue
        if normal["physical"] != stored["physical"] or visible_events(normal) != visible_events(stored):
            continue
        assert compiled[0] == target[0] == 254 and " ".join(compiled[1:].decode().split()) == paragraph
        pixels = stored.pop("physical")
        stored.pop("logical")
        assert len(pixels) == 228 * 64 and all(not any(pixels[y*228+216:(y+1)*228]) for y in range(64))
        assert stored["complete_consumed_bytes"] == len(target) - 1
        processor = expand(target[1:])
        assert len(processor["cases"]) == 4 and all(c["output_hex"] == target[1:].hex() for c in processor["cases"])
        cropped = b"".join(pixels[y * 228:y * 228 + 216] for y in range(64))
        reason = {
            "question": "Keep the brim-full vessel and the ice floating on the water. Ask about the level after it melts.",
            "directions": "Keep front for a rise, left for a fall, and right for no change. Keep those three conditions on separate lines.",
        }[role]
        row.update(english="{SYSTEM}" + paragraph, decision="revision", target_hex=target.hex(),
                   localization_note=reason, automatic_layout=dict(lines=lines, expected_native_pages=1,
                       encoded_hex=compiled.hex(), planning_cells=36),
                   after_native=dict(processor=processor, fe=stored, fe_row_membership=membership,
                       fe_plane_sha256=sha(pixels), fe_plane_hex=pixels.hex(), pages=[dict(page=1,
                       native_plane_hex=cropped.hex(), plane_sha256=sha(cropped), preview_crop_zero_ink_right_edge=True)]))
        return
    raise AssertionError((row["route"], row["id"], "No complete original FE layout passed"))
