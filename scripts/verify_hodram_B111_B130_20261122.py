"""Check every stored speech, style owner, menu, modal and speaker in B111–130."""

from inspect import getsource
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.reviewed_actor_style_object_v1 import unpack
from scripts import check_editorial_compiled_pages as expansion
from scripts import stage_hodram_B111_B130_20261122 as stage
from scripts import verify_hodram_B91_B110_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
CONTEXT_SHORT_NAMES = {}
check_progressive = FunctionType(previous.check_progressive.__code__,
    previous.check_progressive.__globals__ | {"stage": stage})


def qualified_panels(ctx, draft, staged):
    modal = stage.modal
    adapter = base.load(expansion.MACROS)["source_owned_FE_adapter"]
    env = dict(expansion.FE_expand.__globals__)
    exec(compile(adapter, __file__ + "::original-FE-expansion", "exec"), env)
    paint = modal.prior.town.current_fe_painter(ctx)
    planned = draft["planned_FE"]
    panels, pictures = {}, []
    for row in draft["records"]:
        if row["source_selector"] != 254:
            continue
        ident = row["id"]
        reference = planned.get(ident)
        stored = reference["expected_hex"] if reference else row["current_hex"]
        body = bytes.fromhex(stored)[1:]
        assert not stage.TOKEN.findall(body.decode("ascii"))
        results = ctx.execute(env["expand"], body)["cases"]
        assert len(results) == 4 and {v["output_hex"] for v in results} == {body.hex()}
        rows, plane = modal.paint(paint, body)
        assert len(rows) <= 4 and all(y == i*12 for i,(y,_,_) in enumerate(rows)), (ident, rows)
        assert " ".join(text for _, _, text in rows) == row["english"]
        assert all(origin + len(text)*6 <= 222 for _,origin,text in rows)
        sha = native.digest(plane)
        if reference:
            assert row["change_class"] in ("wording", "wrap-only")
            assert reference["rows"] == [list(t) for t in rows] and reference["plane_sha256"] == sha
        panels[ident] = dict(expected_stored_hex=stored, expanded_hex=body.hex(), rows=rows,
                             plane_sha256=sha, macro_alignment_cases=results)
        pictures.append((ident, plane))
    assert len(panels) == 35
    sheets = FunctionType(modal.make_sheets.__code__, modal.make_sheets.__globals__ | {"OUT": ROOT})(pictures)
    return panels, sheets


def parts(source, old, raw, members):
    assert source[:2] == old[:2] == raw[:2] == b"\x00\x41"
    assert source[18:20] == old[18:20] == raw[18:20]
    assert {row["source_selector"] for row in members} == {source[19]}
    tables, bodies = zip(*(unpack(cmd) for cmd in (source, old, raw)), strict=True)
    assert all(len(table) == 8 for table in tables)
    assert all(len(value) == len(members) for value in bodies)
    for row in members:
        i = row["native_slots"][0]
        at = [table[i] for table in tables]
        assert all([slot for slot,value in enumerate(table) if value == pos] == row["native_slots"]
                   for table,pos in zip(tables,at,strict=True))
        yield row, 20 + at[2], *(value[pos] for value,pos in zip(bodies,at,strict=True))


styles = SimpleNamespace(parts=parts)
verification = checked_text(previous.verification, {
    'len(entries) == 211 and fe_count == 7 and not style_objects':
        'len(entries) == 323 and fe_count == 35 and len(style_objects) == 8',
    '[91] and choices[0]["count"] == 2':
        '[114, 114, 114, 118, 119] and all(m["count"] == 3 for m in choices)',
    '    sheet = prior.precedent.prior.sheet': '''    assert sum(len(obj["slot_owner_sets"]) for obj in style_objects) == 48
    assert all(sum(map(len, obj["slot_owner_sets"])) == 8 for obj in style_objects)
    sheet = prior.precedent.prior.sheet''',
    '"hodram_B91_B110_progressive"': '"hodram_B111_B130_progressive"',
    'before[1:].decode("ascii")': 'before[1:].decode("cp932")',
})
start, end = previous.names.index("    notes = {"), previous.names.index("    assert set(notes)")
names = checked_text(previous.names, {
    '    exec(compile(source, __file__ + "::contextual-native-nameplates", "exec"), scope)': (
        '    source = source.replace("actor = root+0x19E4 if ident==0 else root+4+32*ident", "actor = root+4+32*ident")\n'
        '    exec(compile(source, __file__ + "::contextual-native-nameplates", "exec"), scope)'
    ),
    previous.names[start:end]: '''    notes = {
        0: "Rafael Castor is the fixed speaker in the knife exchange. FI in his reply resolves separately to Hodram's given name.",
        1: "Hodram Bergstrom is the ordinary nameplate. The monk addresses his office and Diogo uses the controlled surname.",
        3: "Maria Li is the fixed speaker whose argument turns the Sao Jorge encounter toward recruitment. Her company-name macro identifies her affiliation.",
        5: "Claudio Manaus is Rafael's crewmate who proposes the knife and payment bargain. Rafael uses Claudio in his reply.",
        6: "Julio Erneco calls Cristina his granddaughter. The short header and the spoken family relationship are distinct.",
        10: "Xien Yan answers the bandit's grievance about the town guard. He does not speak Maria's subsequent offer.",
        14: "Emilio Ferog retains the registered ASCII F. His triumphant interjection fits the springing of the village trap.",
        16: "Gerhard Adernkatz objects to threats against the village and works through the riddles with Hodram. Crew dialogue uses his given name as established.",
        18: "Charles Rochefort interrupts the raid and later reminds the captain about sail handling. Both remain in his own name.",
        19: "Carlo Sinat interprets the jade offerings, including their significance in two regions.",
        23: "Manuel Almeida asks for the ship's heading and appears in the village trap exchange. Preserve his name separately from the tutorial panels.",
        43: "Diogo Escante is his short header. Hodram uses Diogo de Escante in the confrontation, with the separate catalogue name component retained.",
        137: "Senior Monk reflects the clean honorific title and the character's formal account of the Yuan invasion.",
        139: "Priest fits the officiant who greets pilgrims with a cross and leads the prayer.",
        151: "Sailor is the established generic label for the injured crewmate. The FE injury notice names no specific actor.",
        160: "Villager is the role who recognizes fellow believers and offers the inherited lamp. The source gives no personal name.",
        163: "Boy is the source role and the child speaks to his actual grandfather. His friendly farewell to Hodram implies no additional family tie.",
        170: "Mysterious Old Man preserves the source role and his initially unknown identity. His relationship to the boy is named in the body dialogue.",
        177: "Sect Leader identifies the man directing the sect and the planned raid. No rank or personal name is established.",
        178: "Follower identifies the group answering the Sect Leader. Preserve the registered ordinary-font F.",
        179: "Villager is the role who speaks about ownership of the knife and suggests returning. This is a separate source actor from the villager with the lamp.",
        180: "Bandit preserves the source role during the confrontation and the beginning of the alliance. The scene supplies no personal name.",
        191: "Donna is the registered name of the woman recommending Santiago Cathedral. Keep the given name as it appears in the source name field.",
        198: "Benazir is the approved name of the woman who repays the gift with a lead about India.",
    }
''',
})
scope = previous.scope | globals()
for source in (verification, names):
    exec(compile(source, __file__ + "::puzzles-and-sails", "exec"), scope)


if __name__ == "__main__":
    if not PROOF.exists():
        scope["verify"]()
    if not NAMES.exists():
        scope["verify_names"]()

