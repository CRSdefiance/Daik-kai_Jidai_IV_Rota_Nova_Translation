"""Review all four copies of the Alexandria sweet-food trend scene."""

from hashlib import sha256
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import register_maria_final_wraps_20261114 as parent
from scripts import stage_rafael_early_wraps_20261111 as layout
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path("work/alexandria_cook_exchange_20261114_v1")
OUT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/alexandria_cooking_exchange_context_20261114_v1.json")
BLOCKS = (198, 190, 186, 159)
CAPTAINS = ("Rafael", "Hodram", "Lil", "Maria")
SPEAKERS = {0xAE: "Owner", 0xAF: "Cook", 0xFE: "Market notice"}
DESCRIPTION = "In Alexandria the owner tastes a dish, insists on sweetness, dismisses the cook’s doubts, and leaves him to work out the changes. The market notice forecasts a possible trend."
TRIAL = "Of course! I said so, didn't I?"
OPENING = "Hmm... Something's missing. I know! It needs to be sweeter!"
FAREWELL = "Sweet, remember? I'm counting on you! Oh-ho-ho-ho!"
MANUSCRIPT = (
    ("The owner tastes the dish, senses something missing and realizes she wants it sweeter.",
     "Keep the pause while she thinks and the sudden realization. It sets up the cook echoing what she just said.",
     {1: OPENING, 3: OPENING}),
    ("The cook echoes her demand for sweetness in a short question.",
     "Keep the cook's brief echo so the owner can launch into her explanation. Match the wording of her preceding demand.",
     {1: "Sweeter?", 3: "Sweeter?"}),
    ("She says the light flavor won't satisfy customers, then repeats the foreign word for sweet with exaggerated emphasis.",
     "Keep the customer objection and the repeated emphasis on sweet. The repetition is the owner's running joke. Rafael’s current wording works with a fuller wrap.",
     {1: "Yes! Our customers won't settle for a flavor this mild. It has to be sweeet! Sweet!"}),
    ("The cook responds with polite hesitation and doubts whether she's right.",
     "The short skeptical question lets the owner's response carry the joke.",
     {}),
    ("She insists that it must be so because she's the one saying it.",
     "Keep her certainty and comic appeal to her own authority. Hodram's version already sounds like an owner cutting off an argument.",
     {0: TRIAL, 2: TRIAL, 3: TRIAL}),
    ("The cook acknowledges her certainty and asks how to make the dish sweeter.",
     "The cook asks for a practical method, giving her a chance to leave the work to him.",
     {}),
    ("She tells the cook that figuring that out is his job.",
     "Keep her brisk deflection after the practical question. The exchange supplies no method or ingredient.",
     {}),
    ("The cook hesitates and gives the first grudging acknowledgment.",
     "Keep the repeated 'yeah' as weary compliance. His second acknowledgment repeats it after the owner doubles down.",
     {3: "...Yeah, yeah."}),
    ("She insists that sweet food is sure to become fashionable.",
     "Keep her personal certainty. The impersonal notice at the end gives a more tentative forecast.",
     {}),
    ("The cook repeats the grudging acknowledgment.",
     "Retain the echo of his earlier reply, with the pause gone. His impatience sets up the owner's cheerful farewell.",
     {3: "Yeah, yeah."}),
    ("She repeats sweet once more, urges him to do his best, then laughs in delight.",
     "Keep the running catchphrase, breezy encouragement, and laugh. A gleeful send-off fits her tone after she leaves the work to the cook.",
     {1: FAREWELL, 3: FAREWELL}),
    ("The impersonal notice says sweet foods may become popular in Alexandria.",
     "The current forecast keeps Alexandria and the uncertain outcome. Preserve the modal notice and its original stored text.",
     {}),
)
PHRASES = {
    0: ("Something's missing.", "I know!", "It needs to be sweeter!"),
    2: ("won't be satisfied", "with anything this mild.", "won't settle", "for a flavor this mild.", "It has to be sweeet!", "Sweet is what matters."),
    4: ("I said so, didn't I?",),
    10: ("Sweet, remember?", "I'm counting on you!", "Oh-ho-ho-ho!"),
}


base = parent.base
stage = parent.stage
gates = dict(source=True, context=True, localization=True, naturalness=True, formatting=False)


def digest(data):
    return sha256(data).hexdigest()


def planner():
    source = checked_text(getsource(layout.bind_planner), {
        "len(bytes.fromhex(row['current_hex']))-1-len(body)": "row['layout_body_budget']-len(body)",
    })
    env = vars(layout).copy()
    exec(compile(source, __file__ + "::registered-wrap-rules-with-explicit-reallocation-budget", "exec"), env)
    return env["bind_planner"]()


def build_rows(ctx, clean, clean_hash):
    inventory, _, _ = stage.prior.scoped_inventory()
    clean_arm = clean.read_file(stage.ARM)
    plan = planner()
    slots = []
    envelopes = []
    baseline = None
    for route, block in enumerate(BLOCKS):
        path = f"/data/SC{route}.DK4"
        old, original = [stage.IlnkContainer.parse(rom.read_file(path)).blocks[block] for rom in (ctx.image, clean)]
        ja_commands, ja_records = stage.prior.raw_speeches(clean_arm, original, inventory)
        en_commands, en_records = stage.prior.raw_speeches(ctx.arm, old, inventory)
        assert [r["word"] for r in ja_commands] == [r["word"] for r in en_commands]
        assert len(ja_records) == len(en_records) == len(MANUSCRIPT) == 12
        clean_bodies = [row["raw_hex"] for row in ja_records]
        if baseline is None:
            baseline = clean_bodies
        assert baseline == clean_bodies
        routes = []
        for turn, (ja, en, (meaning, note, versions)) in enumerate(zip(ja_records, en_records, MANUSCRIPT, strict=True)):
            src, old_text = map(bytes.fromhex, (ja["raw_hex"], en["raw_hex"]))
            assert ja["complete_preamble_hex"] == en["complete_preamble_hex"]
            selector = ja["selector"]
            assert src[0] == old_text[0] == selector
            assert not stage.initial_names.bare_tokens(src[1:]) and not stage.initial_names.bare_tokens(old_text[1:])
            before = " ".join(old_text[1:].decode("ascii").split())
            english = versions.get(route, before)
            assert not stage.initial_names.bare_tokens(english.encode("ascii"))
            is_reflow = route == 0 and turn == 2
            changed = english != before or is_reflow
            row = dict(id=f"SC{route}_B{block}_R{ja['record_index']:04d}", file_path=path, block=block, source_selector=selector,
                kind="system_panel" if selector == 0xFE else "progressive", speaker=SPEAKERS[selector], source_meaning=meaning,
                localization_note=note, context=f"{CAPTAINS[route]} route. {DESCRIPTION}", source_Japanese=src[1:].decode("cp932"),
                source_reference=ja | dict(clean_ROM_sha256=clean_hash, block_sha256=digest(original)),
                current_reference=en | dict(candidate_sha256=ctx.receipt()["candidate_sha256"], block_sha256=digest(old)),
                source_hex=src.hex(), current_hex=old_text.hex(), current_English=before, english=english,
                decision="reflow" if is_reflow else "revision" if changed else "retention", review=gates.copy())
            if changed:
                phrases = set()
                for phrase in PHRASES.get(turn, ()):
                    if phrase in english:
                        words = [stage.prior.layout.norm(word) for word in phrase.split()]
                        phrases.update(zip(words, words[1:]))
                row.update(english=f"{{SPEAKER:{selector:02X}}}{english}", layout_body_budget=144)
                fitted = plan(row | {"protected_pairs": phrases})
                assert " ".join(fitted["lines"]) == english
                encoded = bytes.fromhex(fitted["encoded_hex"])
                assert encoded[:1] == src[:1] and b"\0" not in encoded[1:]
                assert fitted["expected_native_pages"] == 1
                assert all(d["severity"] == "warning" and d["code"] == "line-break-count" for d in fitted["diagnostics"])
                pad = (len(old_text) - len(encoded)) % 4
                target = encoded + b" " * pad
                row.update(automatic_layout=fitted, requested_relocated_hex=target.hex(),
                    storage_size_delta=len(target)-len(old_text), implicit_alignment_spaces=pad)
            routes.append(row)
        slots.extend(routes)
        envelopes.append(dict(file_path=path, block=block,
            source_block_sha256=digest(original), current_block_sha256=digest(old),
            clean_commands=ja_commands, current_commands=en_commands,
            speech_ids=[row["id"] for row in routes]))
    assert len(slots) == 48
    return slots, envelopes


def main():
    assert not ROOT.exists() and not OUT.exists()
    release = base.load(parent.RELEASE)
    ctx = RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    assert base.digest(stage.CLEAN) == release["clean_input_sha256"]
    clean = base.NdsImage.open(stage.CLEAN)
    rows, groups = build_rows(ctx, clean, release["clean_input_sha256"])
    ROOT.mkdir()
    _, painter = stage.prior.precedent.planners(ctx.arm)
    font = ctx.image.read_file("/GRP/KANJI.FNT")
    renders = {}
    pictures = []
    for row in rows:
        if row["decision"] == "retention":
            continue
        code = row["source_selector"]
        ids = []
        for label, field in (("before", "current_hex"), ("after", "requested_relocated_hex")):
            body = bytes.fromhex(row[field])[1:]
            key = (code, body)
            if key not in renders:
                renders[key] = stage.native(ctx, code, body, painter)
            page, = renders[key]["pages"]
            assert page["first_visible_origin"] == [0, 0]
            pictures.append((row["id"] + " " + label, bytes.fromhex(page["native_plane_hex"])))
            ids.append(page["plane_sha256"])
            if label == "after":
                no_pad = bytes.fromhex(row["automatic_layout"]["encoded_hex"])[1:]
                expect, = painter(ctx.arm, font, no_pad)["pages"]
                assert page["plane_sha256"] == digest(bytes.fromhex(expect["native_plane_hex"]))
        row.update(before_and_after_plane_sha256=ids,
            display_layout_and_macro_cases_pass=True, formatted_storage_candidate_verified_offline=True)
        print(row["id"], row["decision"], row["automatic_layout"]["lines"], row["storage_size_delta"], flush=True)
    sheets = FunctionType(layout.contact_sheets.__code__, vars(layout) | {"ROOT": ROOT})(pictures)
    base.save(ROOT / "native_preview.json", dict(runtime=ctx.receipt(), checked_individual_pages=len(pictures),
        original_processor_alignments=4*len(renders), unique_native_paint_cases=len(renders),
        native_cases=list(renders.values()), sheets=sheets, visual_review_pending=True))
    base.save(OUT, dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(gates), candidate_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
        records=rows, complete_exchanges=groups, producer_sha256=base.digest(__file__),
        checked_native_preview_sha256=base.digest(ROOT / "native_preview.json"), format_gate_pending=True,
        registered_release_applied=False, zero_new_credit=True, full_goal_complete=False))


if __name__ == "__main__":
    main()

