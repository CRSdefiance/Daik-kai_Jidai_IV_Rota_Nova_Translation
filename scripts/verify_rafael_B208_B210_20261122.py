"""Verify stored speech, every original menu slot, and the nameplates."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import stage_rafael_B208_B210_20261122 as stage
from scripts import verify_rafael_B177_B180_20261121 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
display, modal = previous.display, previous.modal
CHARM = stage.CHARM


def qualified_panels(ctx, draft, staged):
    expand = modal.expansions(ctx)
    plans = {ident: plan for group in staged["groups"] for ident, plan in group["plans"].items()}
    painter = modal.prior.town.current_fe_painter(ctx)
    panels, pictures = {}, []
    for row in draft["records"]:
        if row["source_selector"] != 254:
            continue
        ident = row["id"]
        if ident == CHARM:
            assert row["decision"] == "revision"
            stored = plans[ident]["expected_stored_hex"]
        else:
            assert row["decision"] == "retention"
            stored = row["current_hex"]
        body = bytes.fromhex(stored)[1:]
        expanded, cases = expand(body)
        assert len(cases) == 4 and expanded == body.replace(b"FI", b"Rafael")
        rows, plane = modal.paint(painter, expanded)
        assert " ".join(text for _, _, text in rows) == row["english"].replace("FI", "Rafael")
        panels[ident] = dict(expected_stored_hex=stored, expanded_hex=expanded.hex(),
                             plane_sha256=native.digest(plane), rows=rows, macro_alignment_cases=cases)
        pictures.append((ident, plane))
        if ident == CHARM:
            assert body.rstrip() == b"FI's Charm rose by 1!"
            max_expanded = body.replace(b"FI", modal.WIDE_NAME)
            stress, shown = modal.paint(painter, max_expanded)
            assert stress == [(y, x, text.replace("Rafael", modal.WIDE_NAME.decode("ascii"))) for y, x, text in rows]
            panels[ident]["width_stress"] = dict(expanded_hex=max_expanded.hex(), rows=stress,
                                               plane_sha256=native.digest(shown))
            pictures.append((ident + " 16-cell name", shown))
    assert len(panels) == 8
    sheets = FunctionType(modal.make_sheets.__code__, modal.make_sheets.__globals__ | {"OUT": ROOT})(pictures)
    return panels, sheets


verification = checked_text(previous.verification, {
    '    qualified = qualified_panels(ctx, draft)': '    qualified, panel_sheets = qualified_panels(ctx, draft, staged)',
    'len(entries) == 183 and fe_count == 1': 'len(entries) == 77 and fe_count == 8',
    '[177, 178, 179, 180] and all(m["count"] == 2 for m in choices)':
        '[208] * 6 + [209] and [m["count"] for m in choices] == [2] * 6 + [3]',
    '"rafael_B177_B180_progressive"': '"rafael_B208_B210_progressive"',
    '''                                    "row_proof": panel["rows"], "proven_by_exact_preflight_binding": True}]''':
        '''                                    "row_proof": panel["rows"], "macro_alignment_cases": panel["macro_alignment_cases"],
                                    "width_stress": panel.get("width_stress"), "proven_by_exact_preflight_binding": True}]''',
    'sheets=fresh + caption_sheets': 'sheets=fresh + caption_sheets + panel_sheets',
})
names = checked_text(previous.names, {
    '("B177_B180",)': '("B201_B220",)',
    '    notes[5] = "Keep Claudio Manaus in the header. Clau is a familiar spoken address, and the coin-game joke gives no new title or relationship."':
        '    notes = {ident: note for ident, note in notes.items() if ident in selectors}',
})
scope = previous.scope | globals()
for script in (verification, names):
    exec(compile(script, __file__ + "::stored-native-display", "exec"), scope)


if __name__ == "__main__":
    scope["verify"]()
    scope["verify_names"]()
