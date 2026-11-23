"""Check the stored style table, tutoring panels, role captions and all changed pages."""

from types import FunctionType

from scripts import check_editorial_compiled_pages as expansion
from scripts import stage_hodram_B131_B150_20261122 as stage
from scripts import verify_hodram_B111_B130_20261122 as previous
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
        assert len(alignments) == 4 and {result["output_hex"] for result in alignments} == {expanded.hex()}
        rows, plane = modal.paint(painter, expanded)
        assert len(rows) <= 4 and all(y == i*12 for i,(y,_,_) in enumerate(rows)), (ident,rows)
        assert " ".join(text for _,_,text in rows) == row["english"].replace("FI","Hodram")
        assert all(x + len(text)*6 <= 222 for _,x,text in rows)
        sha = native.digest(plane)
        if preflight:
            assert preflight["rows"] == [list(t) for t in rows] and preflight["plane_sha256"] == sha
        variants = []
        pictures.append((ident, plane))
        if tokens:
            for name in ("I","ABCDEFGHIJKLMNO","ABCDEFGHIJKLMNOP"):
                sample = body.replace(b"FI",name.encode("ascii"))
                test, raster = modal.paint(painter,sample)
                assert len(test) == len(rows)
                assert [line for _,_,line in test] == [line.replace("Hodram",name) for _,_,line in rows]
                stress = dict(name=name, width_cells=len(name),rows=test,
                              expanded_hex=sample.hex(),plane_sha256=native.digest(raster))
                if preflight:
                    planned, = [v for v in preflight["width_cases"] if v["name"] == name]
                    assert stress["plane_sha256"] == planned["plane_sha256"]
                variants.append(stress)
                if len(name) == 16:
                    pictures.append((f"{ident} (16-cell name)", raster))
        panels[ident] = dict(expected_stored_hex=stored, expanded_hex=expanded.hex(), rows=rows,
                             plane_sha256=sha, macro_alignment_cases=alignments,width_stress=variants or None)
    assert len(panels) == 23 and len(pictures) == 27
    sheets = FunctionType(modal.make_sheets.__code__,modal.make_sheets.__globals__ | {"OUT":ROOT})(pictures)
    return panels,sheets


verification = checked_text(previous.verification, {
    "len(entries) == 323 and fe_count == 35 and len(style_objects) == 8":
        "len(entries) == 350 and fe_count == 23 and len(style_objects) == 1",
    '[114, 114, 114, 118, 119] and all(m["count"] == 3 for m in choices)':
        '[132, 134, 135, 136, 140] and all(m["count"] == 2 for m in choices)',
    'sum(len(obj["slot_owner_sets"]) for obj in style_objects) == 48':
        'sum(len(obj["slot_owner_sets"]) for obj in style_objects) == 8',
    '"hodram_B111_B130_progressive"': '"hodram_B131_B150_progressive"',
})
const_start, const_end = previous.names.index("    notes = {"), previous.names.index("    assert set(notes)")
names = checked_text(previous.names, {
    previous.names[const_start:const_end]: '''    notes = {
        0: "Rafael Castor has a distinct fixed selector for his silence and smile. He is separate from the FI address Sera gives to Hodram.",
        1: "Hodram Bergstrom is the captain's nameplate. Sera learns his given name through the source-preserved FI substitutions.",
        4: "Janus Pasar recognizes the workshop and suggests using its methods to improve ship armor.",
        9: "Camille Overijssel is the approved nameplate. Charles remembers him as the person with Lil. Hodram uses the given name when accepting his apology.",
        13: "Cesare Tony is the alternative workshop speaker whose deliberate syllable-by-syllable praise differs from the other crew voices.",
        16: "Gerhard Adernkatz remains the counterpart in the Guiding Staff debate and the officer giving the recruiting lesson. His discussion of the ship and maps stays formal.",
        18: "Charles Rochefort challenges the use of the Guiding Staff and teaches trade controls. The technical language in his different discoveries suits his own voice.",
        23: "Manuel Almeida handles supplies and has his own version of the advice about Sera. His easy tone is distinct from Gerhard's.",
        24: "Sera Shahrbaraz is the short nameplate. Her full name appears in dialogue only when she introduces herself. The earlier caption is embedded in the FE body.",
        26: "Julian Lopes makes a joke out of his own tavern advice and has his own more casual interpretation of the bamboo plan.",
        38: "Zamorin Nagarpur is the existing full nameplate. Hodram calls him Nagarpur in speech and the chapter supplies no new personal name.",
        43: "Diogo Escante is the short nameplate. Diogo de Escante is the approved full name in the introductions and retains the separate catalogue component.",
        58: "Jorge Albacete speaks the angry rebuke before Diogo dismisses him. The existing full nameplate identifies the separate speaker.",
        92: "Barkeep is the shared familiar role for the tavern worker who overhears the discussion, asks about Sera and tells the story about the jar.",
        113: "Port Worker fits the occupation of the man warning about the southern Mediterranean. The warning supplies no name or rank.",
        147: "Guildmaster identifies Diogo's introducer at the guild. The role stays distinct from the governor he introduces.",
        151: "Sailor is the established generic label for the workshop voice. The role-7 lookout remains separate and uses its original voice table.",
    }
''',
})
scope = previous.scope | globals()
for source in (verification,names):
    exec(compile(source,__file__+"::Hodram-crew-lessons-and-discoveries","exec"),scope)


if __name__ == "__main__":
    if not PROOF.exists():
        scope["verify"]()
    if not NAMES.exists():
        scope["verify_names"]()

