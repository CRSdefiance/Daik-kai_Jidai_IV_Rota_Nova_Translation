"""Verify the native progressive scenes, menu captions, and seven FE notices."""

from types import FunctionType

from scripts import stage_hodram_B91_B110_20261122 as stage
from scripts import verify_hodram_B81_B89_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
CONTEXT_SHORT_NAMES = {}
DYNAMIC_ROLE = {
    "DK4_MES_B110_R0015": ("Runtime-selected crew voice", "Hodram Bergstrom"),
    "DK4_MES_B110_R0069": ("Runtime-selected crew voice", "Hodram Bergstrom"),
}
check_progressive = FunctionType(previous.check_progressive.__code__,
    previous.check_progressive.__globals__ | {"stage": stage})
verification = checked_text(previous.verification, {
    'len(entries) == 306 and fe_count == 5': 'len(entries) == 211 and fe_count == 7',
    '[m["block"] for m in choices] == [87]': '[m["block"] for m in choices] == [91]',
    '"hodram_B81_B89_progressive"': '"hodram_B91_B110_progressive"',
})
start, end = previous.names.index("    notes = {"), previous.names.index("    assert set(notes)")
names = checked_text(previous.names, {
    previous.names[start:end]: '''    notes = {
        1: "Hodram Bergstrom is the ordinary nameplate. The distinct CF role-zero selector remains dynamic in the priest scene.",
        4: "Janus Pasar keeps the approved name while he discusses the telescope and doubts its attribution.",
        6: "Julio Erneco worries about Cristina as her grandfather. Hodram's respectful address does not extend that relationship to himself.",
        12: "Yukihisa Shiraki speaks in his formal register when explaining the clan and when asking to see Muramasa.",
        14: "Emilio Ferog retains the regular-font F in his nameplate. His enthusiasm carries the tomato, banana and Hestia's Pot exchanges.",
        15: "Angelo Puccini is the crewmate who brings the nukenin rumor. Mamma mia remains his own exclamation.",
        16: "Gerhard Adernkatz remembers the sword he lost and follows up on what the priest says about the Proof.",
        18: "Charles Rochefort explains the amber with his usual scientific curiosity. The port worker's confusion stays his own reaction.",
        20: "Fernando Dias retains the registered ordinary F. His spoken objections and his stat notices refer to the same person.",
        22: "Samwell Khan is the short header for the crewmate who brings the two animal-themed rumors. The full catalogue component is separately inherited.",
        108: "Trader is the source shop role. Giving the seedling does not establish a different occupation.",
        114: "Port Worker identifies the man who mentions the island off the cape.",
        139: "Priest is the source role. His explanation and blessing name no separate person or rank.",
        152: "Sailor is the familiar voice who asks whether the captain believes in miracles.",
        188: "Margrete is the established nameplate for the speaker who points the crew toward the priest.",
    }
''',
})


def qualified_panels(ctx, draft, staged):
    modal = scope["modal"]
    from scripts import check_editorial_compiled_pages as library

    adapter = base.load(library.MACROS)["source_owned_FE_adapter"]
    env = dict(library.FE_expand.__globals__)
    exec(compile(adapter, __file__ + "::original-Hodram-FE-expansion", "exec"), env)
    paint = modal.prior.town.current_fe_painter(ctx)
    panels, pictures = {}, []
    defaults = scope["DEFAULT_NAMES"]
    for row in draft["records"]:
        if row["source_selector"] != 254:
            continue
        assert row["decision"] == "retention"
        body = bytes.fromhex(row["current_hex"])[1:]
        macros = stage.TOKEN.findall(body.decode("ascii"))
        assert all(macro == "FI" for macro in macros) and len(macros) <= 1
        cases = ctx.execute(env["expand"], body)["cases"]
        expected = stage.TOKEN.sub(lambda m: defaults[m[0]], body.decode("ascii")).encode("ascii")
        assert len(cases) == 4 and {c["output_hex"] for c in cases} == {expected.hex()}
        expanded = expected
        rows, plane = modal.paint(paint, expanded)
        assert " ".join(text for _, _, text in rows) == stage.TOKEN.sub(lambda m: defaults[m[0]], row["english"])
        entry = dict(expected_stored_hex=row["current_hex"], expanded_hex=expanded.hex(),
            plane_sha256=native.digest(plane), rows=rows, macro_alignment_cases=cases)
        pictures.append((row["id"], plane))
        if macros:
            maximum = body.replace(b"FI", b"ABCDEFGHIJKLMNOP")
            wide_rows, wide_plane = modal.paint(paint, maximum)
            assert len(wide_rows) == len(rows) == 1 and wide_rows[0][2] == maximum.decode("ascii").strip()
            entry["width_stress"] = dict(maximum_name_cells=16, expanded_hex=maximum.hex(),
                                         rows=wide_rows, plane_sha256=native.digest(wide_plane))
            pictures.append((row["id"] + " 16-cell name (offline)", wide_plane))
        panels[row["id"]] = entry
    assert len(panels) == 7 and len(pictures) == 9
    sheets = FunctionType(modal.make_sheets.__code__, modal.make_sheets.__globals__ | {"OUT": ROOT})(pictures)
    return panels, sheets


scope = previous.scope | globals()
for source in (verification, names):
    exec(compile(source, __file__ + "::native-pages", "exec"), scope)


if __name__ == "__main__":
    if not PROOF.exists():
        scope["verify"]()
    if not NAMES.exists():
        scope["verify_names"]()
