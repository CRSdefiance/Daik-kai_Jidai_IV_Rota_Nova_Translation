"""Verify the stored exchanges, four menus, role captions and native pages."""

from inspect import getsource
from pathlib import Path
from types import FunctionType
from unicodedata import normalize

from scripts import stage_hodram_B161_B170_20261122 as stage
from scripts import verify_hodram_B151_B160_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
CONTEXT_SHORT_NAMES = {}
check_progressive = FunctionType(previous.check_progressive.__code__,
    previous.check_progressive.__globals__ | {"stage": stage})
expansion = previous.previous.expansion
panels = checked_text(getsource(previous.qualified_panels), {
    "library = previous.expansion": "library = expansion",
    "len(panels) == 25": "len(panels) == len(pictures) == 7",
})


def verify_opaque(ctx, font, expand, entry, row):
    command, = entry["stored_pages"]
    assert row["decision"] == "retention" and command["current"] == command["stored"]
    source = bytes.fromhex(row["source_hex"])
    body = bytes.fromhex(entry["body_hex"])
    assert body.hex() == row["current_hex"] and source[0] == body[0] == 13
    assert normalize("NFKC", source[1:].decode("cp932").strip()) == normalize("NFKC", body[1:].decode("cp932").strip())
    stored_path = Path("work/analysis/Hodram_B151_B170_stored_20261102/stored_native_verification.json")
    stored = base.load(stored_path)
    native_path = stored["native"]
    assert base.digest(native_path) == stored["native_sha256"]
    historic = base.load(native_path)
    assert native.digest(font) == historic["font_sha256"]
    former, = (record for record in stored["records"] if record["id"] == row["id"])
    assert former["stored_hex"] == body.hex() and former["all_stored_planes_equal_directly_viewed_compiled_planes"]
    cases = ctx.execute(expand, body[1:], body[0])["cases"]
    assert len(cases) == 4 and {case["output_hex"] for case in cases} == {former["expanded_hex"]}
    earlier, = former["directly_viewed_planes"]
    plane = Path(earlier["path"]).read_bytes()
    assert len(plane) == 216 * 64 and native.digest(plane) == earlier["sha256"]
    entry["retained_mixed_glyphs"] = dict(text=body[1:].decode("cp932").strip(),
        plane=earlier["path"], plane_sha256=earlier["sha256"], original_expansion=cases,
        stored_reference=str(stored_path), stored_reference_sha256=base.digest(stored_path),
        historical_font_sha256=historic["font_sha256"], actual_bitmap_match_required=True)
    return plane


verification = checked_text(previous.verification, {
    "len(entries) == 331 and fe_count == 25 and not style_objects":
        "len(entries) == 311 and fe_count == 7 and not style_objects",
    '    assert not choices': '    assert [(m["block"], m["count"]) for m in choices] == [(b,2) for b in (167,169,170,170)]',
    '"hodram_B151_B160_progressive"': '"hodram_B161_B170_progressive"',
    '            entries.append(entry)\n            if selector == 254:': '''            entries.append(entry)
            if ident == stage.OPAQUE:
                plane = verify_opaque(ctx, font, expand, entry, row)
                pictures.append((f"{ident} intentional source symbols", plane))
            if selector == 254:''',
    '    assert not style_objects\n    assert all(sum(map(len, obj["slot_owner_sets"])) == 8 for obj in style_objects)':
        '    assert not style_objects',
})
start, end = previous.names.index("    notes = {"), previous.names.index("    assert set(notes)")
names = checked_text(previous.names, {
    previous.names[start:end]: '''    notes = {
        0: "Rafael Castor introduces himself by name and identifies the Castor Company. His fixed actor selector is distinct from the player-controlled Hodram.",
        1: "Hodram Bergstrom observes the tavern exchanges and recruits each seafarer in his own name. His introductions keep the original FI and FA.",
        5: "Claudio Manaus gets the full spoken Claudio address when Rafael asks him to wait. His teasing of Rafael still reads as familiar.",
        6: "Julio Erneco gives that approved name on both recruitment paths. Preserve the same surname in the header and spoken introductions.",
        7: "Cristina Erneco is the established caption in the dance scene. Hodram mentions Mivor's attraction without creating a relationship title.",
        8: "Arcadius Eudoxios is the established caption for the crewmate requesting proof of the ship's ownership. Keep his more formal voice separate from Claudio's.",
        11: "Jam Ludwyan is the short caption. Jam spells his given name on the ship and later gives the full Jam Jack Ludwyan in speech.",
        13: "Cesare Tony remains the nameplate across the ship lesson and the recovery of the Elysion. The embedded Cesare caption is his own shout from offscreen.",
        16: "Gerhard Adernkatz introduces himself with the original FO company substitution. He also speaks in his own name when objecting to Julio coming aboard.",
        18: "Charles Rochefort keeps his approved name and his distinct scientific phrasing about the missing ship.",
        20: "Fernando Dias introduces himself after the favorable coin flip. The spoken name and same full caption preserve the registered ordinary F.",
        22: "Samwell Khan is the registered short caption. He introduces himself as Samwell, while the catalogue keeps its separate middle field.",
        116: "Port Worker identifies the source dock worker who saw the ship leave and reports whether it has returned. None of the reports gives a personal name.",
        151: "Sailor is the shared role for the crewmate who reports the missing ship and the later sighting. Neither report adds a rank.",
        164: "Man is the anonymous male half of the couple. Their disagreement and decision to part are in dialogue rather than the shared caption.",
        165: "Woman identifies the other half of the couple. Fernando's prediction and her own words establish the context without a claim that they are married.",
    }
''',
})
scope = previous.scope | globals()
for source in (panels, verification, names):
    exec(compile(source, __file__ + "::stored-recruitment-pages", "exec"), scope)


if __name__ == "__main__":
    if not PROOF.exists():
        scope["verify"]()
    if not NAMES.exists():
        scope["verify_names"]()

