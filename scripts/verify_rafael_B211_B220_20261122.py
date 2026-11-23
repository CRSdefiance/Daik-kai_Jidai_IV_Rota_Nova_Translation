"""Verify the newly stored pages, letter signature, menus and speaker nameplates."""

from types import FunctionType

from scripts import stage_rafael_B211_B220_20261122 as stage
from scripts import verify_rafael_B208_B210_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
display, modal = previous.display, previous.modal
LETTER_END = "DK4_MES_B216_R0074"


def qualified_panels(ctx, draft, staged):
    expand = modal.expansions(ctx)
    painter = modal.prior.town.current_fe_painter(ctx)
    plans = {ident: plan for group in staged["groups"] for ident, plan in group["plans"].items()}
    panels, pictures = {}, []
    for row in draft["records"]:
        if row["source_selector"] != 254:
            continue
        ident = row["id"]
        stored = plans[ident]["expected_stored_hex"] if row["decision"] == "revision" else row["current_hex"]
        assert (ident in stage.NOTICES) == (row["decision"] == "revision")
        body = bytes.fromhex(stored)[1:]
        expanded, cases = expand(body)
        assert len(cases) == 4 and expanded == body.replace(b"FI", b"Rafael")
        rows, plane = modal.paint(painter, expanded)
        expected = row["english"].replace("FI", "Rafael")
        assert " ".join(text for _, _, text in rows) == expected
        if ident == LETTER_END:
            assert rows == [(0, 0, 'Take care now.'), (12, 36, 'Jam Jack Ludwyan')]
        panel = dict(expected_stored_hex=stored, expanded_hex=expanded.hex(), plane_sha256=native.digest(plane),
                     rows=rows, macro_alignment_cases=cases)
        panels[ident] = panel
        pictures.append((ident, plane))
        if ident in stage.NOTICES:
            assert body.count(b"FI") == 1 and len(rows) == 1
            expanded_wide = body.replace(b"FI", modal.WIDE_NAME)
            stress, shown = modal.paint(painter, expanded_wide)
            assert stress == [(0, 0, row["english"].replace("FI", modal.WIDE_NAME.decode("ascii")))]
            panel["width_stress"] = dict(expanded_hex=expanded_wide.hex(), rows=stress, plane_sha256=native.digest(shown))
            pictures.append((ident + " 16-cell name", shown))
    assert len(panels) == 19
    sheets = FunctionType(modal.make_sheets.__code__, modal.make_sheets.__globals__ | {"OUT": ROOT})(pictures)
    return panels, sheets


verification = checked_text(previous.verification, {
    'len(entries) == 77 and fe_count == 8': 'len(entries) == 224 and fe_count == 19',
    '[208] * 6 + [209] and [m["count"] for m in choices] == [2] * 6 + [3]':
        '[213, 218, 218] and [m["count"] for m in choices] == [2, 2, 2]',
    '"rafael_B208_B210_progressive"': '"rafael_B211_B220_progressive"',
})
scope = previous.scope | globals()
for script in (verification, previous.names):
    exec(compile(script, __file__ + "::stored-native-display", "exec"), scope)


if __name__ == "__main__":
    scope["verify"]()
    scope["verify_names"]()
