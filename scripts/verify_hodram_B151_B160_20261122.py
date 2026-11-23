"""Verify the revised pages, staged farewell positions and speaker labels."""

from types import FunctionType

from scripts import stage_hodram_B151_B160_20261122 as stage
from scripts import verify_hodram_B131_B150_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
CONTEXT_SHORT_NAMES = {}
check_progressive = FunctionType(previous.check_progressive.__code__,
    previous.check_progressive.__globals__ | {"stage": stage})


def qualified_panels(ctx, draft, staged):
    modal = stage.modal
    library = previous.expansion
    adapter = base.load(library.MACROS)["source_owned_FE_adapter"]
    env = dict(library.FE_expand.__globals__)
    exec(compile(adapter, __file__ + "::FE-expansion", "exec"), env)
    painter = modal.prior.town.current_fe_painter(ctx)
    panels, pictures = {}, []
    for row in draft["records"]:
        if row["source_selector"] != 254:
            continue
        ident = row["id"]
        preflight = draft["planned_FE"].get(ident)
        stored = preflight["expected_hex"] if preflight else row["current_hex"]
        body = bytes.fromhex(stored)[1:]
        tokens = stage.TOKEN.findall(body.decode("ascii"))
        assert all(token == "FI" for token in tokens)
        expanded = body.replace(b"FI", b"Hodram")
        alignments = ctx.execute(env["expand"], body)["cases"]
        assert len(alignments) == 4 and {value["output_hex"] for value in alignments} == {expanded.hex()}

        def render(sample, name):
            rows, plane = modal.paint(painter, sample)
            expected = stage.TOKEN.sub(lambda match: name, row["english"])
            assert " ".join(text for _, _, text in rows) == expected, (ident, name, rows, expected)
            assert len(rows) <= 5 and all(
                0 <= y <= 48 and y % 12 == 0 and 0 <= x and x + len(text) * 6 <= 222
                for y, x, text in rows
            ), (ident, name, rows)
            return rows, plane

        rows, plane = render(expanded, "Hodram")
        sha = native.digest(plane)
        if preflight:
            assert preflight["rows"] == [list(value) for value in rows] and preflight["plane_sha256"] == sha
            if "before" in preflight:
                assert [value[:2] for value in preflight["before"]] == [[y, x] for y, x, _ in rows]
        pictures.append((ident, plane))
        variants = []
        if tokens:
            for name in ("I", "ABCDEFGHIJKLMNO", "ABCDEFGHIJKLMNOP"):
                sample = body.replace(b"FI", name.encode("ascii"))
                test, raster = render(sample, name)
                variants.append(dict(name=name, rows=test, expanded_hex=sample.hex(),
                                     plane_sha256=native.digest(raster)))
                if len(name) == 16:
                    pictures.append((f"{ident} (16-cell name)", raster))
        panels[ident] = dict(expected_stored_hex=stored, expanded_hex=expanded.hex(), rows=rows,
                             plane_sha256=sha, macro_alignment_cases=alignments, width_stress=variants or None)
    assert len(panels) == 25
    sheets = FunctionType(modal.make_sheets.__code__, modal.make_sheets.__globals__ | {"OUT": ROOT})(pictures)
    return panels, sheets


verification = checked_text(previous.verification, {
    "len(entries) == 350 and fe_count == 23 and len(style_objects) == 1":
        "len(entries) == 331 and fe_count == 25 and not style_objects",
    'assert [m["block"] for m in choices] == [132, 134, 135, 136, 140] and all(m["count"] == 2 for m in choices)':
        "assert not choices",
    'assert sum(len(obj["slot_owner_sets"]) for obj in style_objects) == 8': "assert not style_objects",
    '"hodram_B131_B150_progressive"': '"hodram_B151_B160_progressive"',
})
start, end = previous.names.index("    notes = {"), previous.names.index("    assert set(notes)")
names = checked_text(previous.names, {
    previous.names[start:end]: '''    notes = {
        1: "Hodram Bergstrom is the accepted short caption. The commands that address him by FI or FA use the native player substitution.",
        6: "Julio Erneco is the crewmate who independently confirms Angelo's advice about market share.",
        15: "Angelo Puccini gives the same full name after the duel. His boasts and trade advice belong to the same speaker.",
        16: "Gerhard Adernkatz serves as Hodram's officer and continues with him when he retires. His own name stays separate from the offices discussed.",
        17: "Al Shin is the registered caption. He gives only Al in the first introduction, which suits the new acquaintance.",
        18: "Charles Rochefort notices Al and offers an opinion about teamwork. He has his own alternate delivery in the lamp scene.",
        19: "Carlo Sinat gives the same full name when accepting the offer. Purser is the position Hodram offers him in speech.",
        20: "Fernando Dias makes the joke about being observant. The registered F stays in the ordinary English font.",
        21: "Ian Dukov appears on the nameplate and in Ian's own introduction. The harassing forms of address belong to the patrons' speech.",
        23: "Manuel Almeida greets Hodram when he returns from the palace. The congratulations stay in Manuel's voice.",
        24: "Sera Shahrbaraz is the regular caption before the farewell. Sera and her addresses to Hodram in the speakerless staged exchanges are embedded in the panels.",
        25: "Yifa Sol gives her own explanation for trying the lamp. Her name stays distinct from Charles on the alternative branch.",
        78: "Sirwood Eme addresses the party in Abkhaz. Preserve his caption separately from the staged farewell.",
        92: "Barkeep expresses the source tavern role in familiar English. Ian's respectful response needs no implication of kinship.",
        96: "Patron is the anonymous customer. The later attack adds no personal name or rank to the standing caption.",
        105: "Trader reflects Adil's shared source role. Carlo and Adil's wife identify him by name aloud.",
        113: "Port Worker is the source dock role that relays the Alexandria summons.",
        115: "Port Worker is the separate regional role that brings the rumor of a new Black Sea town.",
        120: "Guard is the palace role. His announcement there does not give him a personal name.",
        121: "Guard identifies the distinct regional actor who checks the company name at the Alexandria audience.",
        125: "King expresses the monarch's role in the palace audience. Hodram uses the proper form of address in speech.",
        132: "Officiant is the source ceremonial role. The man withholds his own name in the dialogue.",
        142: "Innkeeper is the actor's shared Japanese role. Her relationship to Adil is clear in speech and does not need to be added to the standing caption.",
        148: "Guildmaster is the source guild role. The man can be Al's employer without adding a military rank.",
        152: "Sailor is the existing caption for the shared source subordinate. In the ambush his conduct establishes that he is one of the attackers.",
        164: "Man is the established caption for the anonymous male half of the couple. The couple designation stays out of the conversational nameplate.",
        165: "Woman is the established caption for the anonymous female half of the couple. Her lines identify who she is talking about.",
    }
''',
})
scope = previous.scope | globals()
for source in (verification, names):
    exec(compile(source, __file__ + "::farewell-and-recruitment", "exec"), scope)


if __name__ == "__main__":
    if not PROOF.exists():
        scope["verify"]()
    if not NAMES.exists():
        scope["verify_names"]()

