"""Verify the native letter variants, retained controls, and revised dialogue pages."""

from types import FunctionType

from scripts import stage_rafael_B221_B240_20261122 as stage
from scripts import verify_rafael_B211_B220_20261122 as previous
from scripts import verify_rafael_ruins_and_proof_20261121 as styles
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
display, modal = previous.display, previous.modal


def qualified_panels(ctx, draft, staged):
    expand = modal.expansions(ctx)
    painter = modal.prior.town.current_fe_painter(ctx)
    panels, pictures = {}, []
    for row in draft["records"]:
        if row["source_selector"] != 254:
            continue
        assert row["decision"] == "retention"
        body = bytes.fromhex(row["current_hex"])[1:]
        expanded, cases = expand(body)
        assert len(cases) == 4 and expanded == body
        rows, plane = modal.paint(painter, body)
        assert " ".join(text for _, _, text in rows) == row["english"]
        panels[row["id"]] = dict(expected_stored_hex=row["current_hex"], expanded_hex=body.hex(),
            plane_sha256=native.digest(plane), rows=rows, macro_alignment_cases=cases)
        pictures.append((row["id"], plane))
    assert len(panels) == 3
    sheets = FunctionType(modal.make_sheets.__code__, modal.make_sheets.__globals__ | {"OUT": ROOT})(pictures)
    return panels, sheets


verification = checked_text(previous.verification, {
    '    menu_adapters = menus.menu.adapters(ctx.arm)':
        '    style_objects = []\n    menu_adapters = menus.menu.adapters(ctx.arm)',
    '            ident, = cmd["record_ids"]': '''            if cmd["word"] == 0x4100:
                members = [rows.pop(ident) for ident in cmd["record_ids"]]
                assert all(row["kind"] == "actor-style" for row in members)
                style_objects.append(dict(block=n, source_offset=cmd["source_offset"], stored_offset=at,
                    slot_owner_sets=[row["native_slots"] for row in members]))
                for row, offset, jp, former, body in styles.parts(source, old, raw, members):
                    ident = row["id"]
                    assert jp.hex() == row["source_hex"] and former.hex() == row["current_hex"]
                    plan = group["plans"][ident]
                    entry = dict(id=ident, block=n, stored_pages=[cmd], body_offset=at + offset,
                                 body_hex=body.hex(), style_slots=row["native_slots"])
                    entries.append(entry)
                    assert (former != body) == (row["decision"] == "revision")
                    if row["decision"] == "retention":
                        continue
                    assert not stage.TOKEN.findall(row["english"])
                    assert " ".join(body.decode("ascii").split()) == row["english"]
                    encoded = bytes.fromhex(plan["encoded_hex"])
                    assert (bytes([row["source_selector"]]) + body) in (encoded, encoded + b" ")
                    assert plan["expected_native_pages"] == 1
                    page, = display.display.raster(ctx, font, paint, body, plan["lines"], 1)
                    assert page["native_independent_plane_equal"] and page["all_bitmap_header_input_canaries_exact"]
                    plane = bytes.fromhex(page["native_plane_hex"])
                    entry.update(layouts=[dict(scope="registered default", expanded_hex=body.hex(),
                        lines=plan["lines"], page_sha256=[native.digest(plane)])])
                    pictures.append((f"{ident} slots {row['native_slots']}", plane))
                    revised_pages += 1
                continue
            ident, = cmd["record_ids"]''',
    'len(entries) == 224 and fe_count == 19': 'len(entries) == 270 and fe_count == 3 and len(style_objects) == 4',
    '[213, 218, 218] and [m["count"] for m in choices] == [2, 2, 2]':
        '[224, 224, 233] and [m["count"] for m in choices] == [2, 3, 2]',
    '"rafael_B211_B220_progressive"': '"rafael_B221_B240_progressive"',
    'menus=choices, style_objects=[],': 'menus=choices, style_objects=style_objects,',
})
names = checked_text(previous.previous.names, {
    '("B201_B220",)': '("B221_B240",)',
})
scope = previous.scope | globals()
for script in (verification, names):
    exec(compile(script, __file__ + "::stored-native-display", "exec"), scope)


if __name__ == "__main__":
    scope["verify"]()
    scope["verify_names"]()
