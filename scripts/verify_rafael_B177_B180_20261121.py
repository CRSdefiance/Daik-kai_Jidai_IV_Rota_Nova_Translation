"""Verify the stored revised pages, all original choice slots, and speaker names."""

from inspect import getsource
from types import FunctionType

from scripts import preflight_rafael_B161_B169_FE_20261121 as modal
from scripts import stage_rafael_B177_B180_20261121 as stage
from scripts import verify_rafael_B161_B169_20261121 as previous
from scripts import verify_rafael_gerhard_tutorial_20261121 as menus
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
display = previous.display
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
CHOICE_WORDS = (0x2100, 0x2200)


def qualified_panels(ctx, draft):
    ident = "DK4_MES_B177_R0114"
    row, = [r for r in draft["records"] if r["source_selector"] == 254]
    assert row["id"] == ident and row["decision"] == "retention"
    body = bytes.fromhex(row["current_hex"])[1:]
    expand = modal.expansions(ctx)
    expanded, cases = expand(body)
    assert len(cases) == 4 and expanded == body
    painter = modal.prior.town.current_fe_painter(ctx)
    rows, plane = modal.paint(painter, expanded)
    assert " ".join(text for _, _, text in rows) == row["english"]
    return {ident: dict(expected_stored_hex=row["current_hex"], expanded_hex=expanded.hex(),
                       plane_sha256=native.digest(plane), rows=rows, macro_alignment_cases=cases)}


verification = checked_text(getsource(previous.verify), {
    '    assert not ROOT.exists()': '    assert not PROOF.exists()\n    ROOT.mkdir(exist_ok=True)',
    '    qualified = stage.qualified_panels()': '    qualified = qualified_panels(ctx, draft)',
    '    entries, pictures, pagination = [], [], []':
        '''    entries, pictures, pagination, choices = [], [], [], []
    menu_adapters = menus.menu.adapters(ctx.arm)
    verify_menu = FunctionType(menus.verify_menu.__code__, menus.verify_menu.__globals__ | {"ROOT": ROOT})''',
    '            ident, = cmd["record_ids"]':
        '''            if cmd["word"] in CHOICE_WORDS:
                members = [rows.pop(ident) for ident in cmd["record_ids"]]
                assert raw == old and all(r["decision"] == "retention" for r in members)
                originals = {cmd["source_offset"]: {"offset": cmd["source_offset"], "whole_command_hex": cmd["source"]}}
                observed = verify_menu(ctx.arm, originals, cmd, members, menu_adapters)
                choices.append(observed | {"block": n})
                entries.extend(dict(id=r["id"], block=n, stored_pages=[cmd]) for r in members)
                continue
            ident, = cmd["record_ids"]''',
    'len(entries) == 368 and fe_count == 30': 'len(entries) == 183 and fe_count == 1',
    '    ROOT.mkdir()':
        '    assert [m["block"] for m in choices] == [177, 178, 179, 180] and all(m["count"] == 2 for m in choices)',
    '"rafael_B161_B169_progressive"': '"rafael_B177_B180_progressive"',
    '    panels = base.load(stage.FE_PROOF)["sheets"]': '    caption_sheets = [m["sheet"] for m in choices]',
    'menus=[], style_objects=[], sheets=fresh + panels': 'menus=choices, style_objects=[], sheets=fresh + caption_sheets',
})
names = checked_text(getsource(previous.verify_names), {
    '("B161_B165", "B166_B167", "B168_B169")': '("B177_B180",)',
    '    notes[132] = "Officiant matches the registered generic ceremonial role. This speaker formally confers the item, and the exchange gives no specific rank."':
        '    notes[5] = "Keep Claudio Manaus in the header. Clau is a familiar spoken address, and the coin-game joke gives no new title or relationship."',
})
scope = vars(previous) | globals()
for script in (verification, names):
    exec(compile(script, __file__ + "::stored-native-display", "exec"), scope)


if __name__ == "__main__":
    scope["verify"]()
    scope["verify_names"]()
