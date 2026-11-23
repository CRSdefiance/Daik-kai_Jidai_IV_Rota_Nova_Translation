"""Verify the remaining Rafael pages, nameplates, and focused emulator replay."""

from argparse import ArgumentParser
from types import FunctionType, SimpleNamespace

from scripts import preflight_rafael_B161_B169_FE_20261121 as modal
from scripts import stage_rafael_remaining_wraps_20261123 as stage
from scripts import verify_rafael_mediterranean_followups_20261123 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
LIVE = ROOT / "verified_gameplay.json"
GLYPHS = stage.ROOT / "glyph_and_sheet_verification.json"
ROLES = stage.ROOT / "speaker_roles.json"
MODAL_SAMPLE = "DK4_MES_B318_R0198"
NOTES = {
    0: "Rafael Castor remains the captain in the header and the given-name field remains live in the stat notice.",
    5: "Keep Claudio Manaus in the nameplate and Clau in the familiar speech between crewmates.",
    6: "Keep Julio Erneco when he teases Claudio and takes Yifa's resolve seriously.",
    8: "Keep Arcadius Eudoxios for the book and ruins exchanges. His cautious suggestions need no added title.",
    14: "Keep Emilio Ferog for the crewman who wants an axe so he can get stronger.",
    16: "Keep Gerhard Adernkatz. His admiration of Noritsune and Charles Martel comes through in his speech.",
    17: "Use Al Shin in the header for the crew member who reads the book. Keep the separately approved catalogue field.",
    25: "Keep Yifa Sol. The source names her and describes the connection to Sanghyeon through their training.",
    26: "Keep Julian Lopes for the same speaker in the crown hunt and the exchanges with Lucia and Safia.",
    75: "Keep Hans Letzel where the established crew actor comments during this route.",
    81: "Keep Sanghyeon Kan. His seniority in their shared training is expressed in dialogue.",
    82: "Keep Shopkeeper for the unnamed speaker who turns Vivian away.",
    92: "Keep Barkeep for the unnamed tavern worker who passes on the Avalon story.",
    147: "Keep Guildmaster for the established unnamed official in the relevant exchange.",
    151: "Keep Sailor for this established crew role. Retain the separately approved catalogue wording.",
    162: "Keep Boy for the child acting out the local hero's story.",
    169: "Keep Alluring Woman in the public header. Vivian gives her own name during the exchange.",
    170: "Keep Mysterious Old Man for the unnamed expert who identifies cordyceps and offers the book.",
    179: "Keep Villager for the unnamed intermediary. His local knowledge is supplied by his dialogue.",
    182: "Keep Explorer for the unnamed person released from the king's curse.",
    197: "Keep Safia for the woman who answers Julian's Medusa comparison.",
    199: "Keep Lucia for the woman who sees Julian's empress comparison differently from him.",
    201: "Keep Mihwa for the woman who encourages Julian and Rafael's party to find the crown.",
    202: "Keep Reika for the woman who heard two inquiries about the crown.",
}


def sample():
    return {0: tuple((r["block"], int(r["id"].rsplit("R", 1)[1]))
                     for r in base.load(stage.REVIEW)["records"]
                     if r["decision"] == "revision" or r["id"] == MODAL_SAMPLE)}


def report(run):
    return scope["report_path"](int(run))


scope = prior.scope | globals()
scope["scope"] = scope
for name in ("receipt", "report_path", "run_file", "play"):
    scope[name] = FunctionType(prior.scope[name].__code__, scope)
fixture = checked_text(prior.fixture, {
    "Rafael_Mediterranean_Followups_FOCUSED_ONLY.nds": "Rafael_Remaining_Wraps_FOCUSED_ONLY.nds",
})
verify = checked_text(prior.verify, {
    "rafael_mediterranean_excerpt_": "rafael_remaining_wraps_excerpt_",
    "including the move from Claudio’s portrait to Eirene’s speakerless reply":
        "including the speakerless voice in the book and curse exchange",
})
for code in (fixture, verify):
    exec(compile(code, __file__ + "::focused-dialogue", "exec"), scope)


def formatting():
    glyphs = prior.prior.prototype.prior.display.verification.glyphs
    FunctionType(glyphs.verify.__code__, vars(glyphs) | dict(stage=stage, OUTPUT=GLYPHS))()
    proof, draft, registered = map(base.load, (stage.PROOF, stage.REVIEW, stage.parent.RELEASE))
    candidate = base.digest(stage.ROM)
    assert candidate == proof["candidate_sha256"] and proof["draft_sha256"] == base.digest(stage.REVIEW)
    assert proof["predecessor_sha256"] == registered["candidate_sha256"]
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, registered["own_registered_startup"], captain=3)
    image = base.NdsImage.open(stage.ROM)
    assert all(ctx.image.read_file(p) == image.read_file(p) for p in stage.established.display.ASSETS)
    bank = native.IlnkContainer.parse(image.read_file(stage.ARCHIVE)).blocks
    paint = modal.prior.town.current_fe_painter(ctx)
    owners = {r["id"]: r for r in draft["records"] if r["source_selector"] == 254}
    records, pictures = [], []
    for group in proof["groups"]:
        block = group["block"]
        assert native.digest(bank[block]) == group["after"]
        for command in group["commands"]:
            raw = bytes.fromhex(command["stored"])
            if command["word"] != 0x4000 or raw[5] != 254:
                continue
            ident, = command["record_ids"]
            owner = owners.pop(ident)
            at = command["stored_offset"]
            assert owner["decision"] == "retention"
            assert raw[:6] == bytes.fromhex("0040ffff00fe")
            assert raw == bytes.fromhex(owner["current_reference"]["exact_command_hex"])
            assert bank[block][at:at+len(raw)] == raw == bytes.fromhex(command["current"])
            body = raw[6:raw.index(0, 6)]
            assert set(modal.TOKEN.findall(body)) <= {b"FI"}
            expanded = modal.layout.expand(body)
            rows, plane = modal.paint(paint, expanded)
            assert all(not any(plane[y*228+216:(y+1)*228]) for y in range(64))
            assert " ".join(" ".join(text for _, _, text in rows).split()) == owner["english"].replace("FI", "Rafael")
            if b"FI" in body:
                stress = body.replace(b"FI", modal.WIDE_NAME)
                wide_rows, wide_plane = modal.paint(paint, stress)
                assert wide_rows == [(y, x, text.replace("Rafael", modal.WIDE_NAME.decode("ascii"))) for y, x, text in rows]
                assert all(not any(wide_plane[y*228+216:(y+1)*228]) for y in range(64))
                pictures.append((ident + " / maximum name width", wide_plane))
            pictures.append((ident + " / retained", plane))
            records.append(dict(route=0, block=block, id=ident, second_page=False, stored_offset=at,
                exact_command_hex=raw.hex(), visual_rows=rows, expanded_hex=expanded.hex(),
                physical_plane_hex=plane.hex(), physical_plane_sha256=native.digest(plane)))
    assert len(records) == 4 and not owners
    directory = stage.ROOT / "retained_FE"
    directory.mkdir(exist_ok=True)
    make_sheets = FunctionType(modal.make_sheets.__code__, modal.make_sheets.__globals__ | {"OUT": directory})
    sheets = make_sheets(pictures)
    base.save(stage.FE_PROOF, dict(candidate_sha256=candidate, records=records, sheets=sheets,
        original_modal_consumer=True, complete_stored_page_count=len(records),
        retained_macro_bytes_exact=True, runtime_assets_match_predecessor=True))
    print("Verified four byte-identical speakerless panels and both widths of the Charm notice.")


def names():
    labels = prior.prior.prototype.prior.names
    context = labels.scope | dict(PROOF=ROLES, NOTES=NOTES, parent=stage.parent,
        stage=SimpleNamespace(OUTPUT=stage.REVIEW, PROOF=stage.PROOF, ROM=stage.ROM),
        display=SimpleNamespace(PROOF=stage.NATIVE), live_receipt=LIVE)
    exec(compile(labels.source, __file__ + "::speaker-and-catalogue-names", "exec"), context)
    context["main"]()


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("formatting", "replay", "verify", "names"))
    action = cli.parse_args().action
    if action in ("replay", "verify"):
        scope["SAMPLE"] = sample()
        if action == "replay":
            scope["fixture"](0)
            scope["play"](0)
        else:
            scope["verify"]()
    else:
        globals()[action]()
