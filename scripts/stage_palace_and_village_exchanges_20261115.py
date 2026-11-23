"""Reconcile the palace, village, and ruins exchanges with the cumulative release."""

from inspect import getsource
from pathlib import Path
import re
from types import FunctionType

from scripts import register_town_quest_exchanges_20261115 as parent
from scripts import stage_kurushima_encounter_20261115 as names
from scripts import stage_town_trend_exchanges_20261115 as native
from scripts.source_locked_derivation_v5118 import checked_text

base, layout = native.base, native.layout
ROOT = Path("work/palace_and_village_exchanges_20261115_v2")
ROM, STORED = ROOT / "Palace_and_Village_Exchanges_RESEARCH_ONLY.nds", ROOT / "staged.json"
MANUSCRIPT = native.MANUSCRIPT.with_name("palace_and_village_exchanges_20261115_v2.json")
BLOCKS = {
    "society": (115, 115, 106, 88),
    "faith": (117, 117, 108, 89),
    "rescue": (121, 121, 112, 95),
    "bandits": (123, 123, 115, 97),
    "dagger": (126, 126, 118, 100),
}
HISTORY = (
    ("rafael_B101_B120_contextual_final_review_v1", "rafael_B121_B140_contextual_final_review_v2"),
    ("hodram_B111_B130_contextual_final_review_v1",),
    ("lil_shrines_temples_contextual_final_review_v1", "lil_B111_B119_contextual_final_review_v1", "lil382_residual_A_integrated_final_review_v1"),
    ("maria_B73_B95_final_review_v1", "maria_B96_B124_final_review_v1", "maria_B97_contextual_final_review_v1"),
)
CONTEXT = {
    "society": "The party overhears the Ancient Megalithic Civilization Research Society. The leader's claimed revelation becomes a threat against the village. The route-specific interventions and cowardly retreat play out before the party confronts him over what he tries to take.",
    "faith": "The villager recognizes fellow believers and recounts why his community lives quietly. The protagonist asks about the Proof according to their own knowledge. The villager entrusts them with the lamp and asks them to keep the Proof out of Ottoman hands.",
    "rescue": "Each captain leaves the palace with a different reaction. The grandfather begs the crew to save his grandson. Relief turns to gratitude after the rescue. The governor's gift once honored the grandfather's bravery; he now wants the people who saved his grandson to have it.",
    "bandits": "The raid grievance moves from lost livelihood to village destruction and retaliation. The protagonists confront deliberate slave trading, plunder and attacks on uninvolved people. The exchange moves to the political struggle, an invitation to join the crew, and the possibility that a tablet hidden in the ruins is relevant.",
    "dagger": "The speaker recognizes the blade, acknowledges the discoverers' right to it, and thanks them for returning something of lasting importance to the community. Hodram's scene includes a distinct discussion about who deserves the find. The gold notice and return keep their own conditions and voices.",
}
FI = "{MACRO:FI}"
# Targets use clean source IDs and retain route-specific wording where it works.
# A None draft reflows the existing logical paragraph.
EDITS = {
    (0, 121, 6): (None, ("let's head back to town.",), "Keep Rafael's quick impression and invitation to return. Keep his invitation together."),
    (0, 121, 45): (None, ("Please save my grandson!",), "The grandfather's relief turns into an urgent request. Keep the whole plea together."),
    (0, 121, 90): ("You're safe now! Thank goodness!", ("You're safe now!",), "The contraction is natural in the grandfather's relief."),
    (0, 121, 96): ("I'm glad your grandson is safe.", (), "Rafael's immediate response gets a natural subject and keeps his relief for the boy."),
    (0, 121, 113): ("When I was young, I drove off the local bandits. The governor gave me this reward.", ("the local bandits.", "The governor gave me this reward."), "The older man recalls stopping the local bandits. Keep the governor's reward and avoid implying a particular fate for the bandits."),
    (1, 121, 42): (None, ("Please, save my grandson!",), "The grandfather's relief gives way to an urgent plea, which belongs on one line."),
    (1, 121, 107): ("When I was young, I drove off the local bandits. The governor gave me this reward.", ("the local bandits.", "The governor gave me this reward."), "Keep the old man's action, the governor and the reason for the reward together."),
    (2, 112, 43): ("You're just in time! Save my grandson!", ("Save my grandson!",), "The relief and plea are distinct beats. Keep the plea together."),
    (2, 112, 96): ("I have nothing to give you... Oh! Wait here!", ("I have nothing to give you...", "Wait here!"), "The old man speaks of his own lack of a gift. His sudden thought sets up the presentation."),
    (3, 95, 5): ("Do the palace officials realize how fast the world's changing? Never mind. Let's go.", ("the palace officials", "the world's changing?", "Never mind. Let's go."), "Keep Maria's reflective question about the officials' awareness and her decision to leave."),
    (3, 95, 42): (None, ("Save my grandson!",), "The urgent plea remains a whole phrase after the relieved greeting."),
    (3, 95, 95): ("I have nothing to give you... Oh, I know! Wait here a moment!", ("Oh, I know!", "Wait here a moment!"), "Give the realization its beat and keep the request clear."),
    (3, 95, 107): ("When I was young, I drove off the local bandits. The governor gave me this reward.", ("the local bandits.", "The governor gave me this reward."), "Keep the bandits together with the action and the governor's reward in its own sentence."),
    (3, 95, 121): ("If you insist... thank you. We'll accept it.", ("If you insist...", "We'll accept it."), "Maria accepts with gratitude after the older man insists."),
    (0, 117, 33): (None, ("in our village", "since ancient times.", "seeking the Proof", "I entrust it to you."), "Keep the village's inheritance, the seeker and the entrustment as coherent phrases."),
    (1, 117, 31): ("Our village has handed this lamp down for ages. They say anyone who seeks the Proof needs it. We'll entrust it to you.", ("for ages.", "anyone who seeks the Proof", "We'll entrust it to you."), "Wrap the long explanation without breaking its central phrases."),
    (2, 108, 30): ("Our village has passed this lamp down since ancient times. They say anyone seeking the Proof needs it. I entrust it to you.", ("since ancient times.", "seeking the Proof", "I entrust it to you."), "Keep the provenance and final offer together."),
    (3, 89, 15): ("Do you know any village legends about the Proof of Conquest?", ("the Proof of Conquest?",), "Preserve Maria's request for a legend specifically connected to the Proof."),
    (3, 89, 26): ("Do I ever...", (), "The villager already knows something concrete. The reply leads directly into the gift."),
    (3, 89, 30): ("Our village has passed this lamp down since ancient times. They say the lamp is essential to anyone seeking the Proof. We entrust it to you.", ("since ancient times.", "anyone seeking the Proof.", "We entrust it to you."), "Keep the lamp's age, what people say about the Proof, and the entrustment. Avoid isolating a preposition from its phrase."),
    (3, 97, 57): (None, ("all over again.", "More of your people", "will suffer."), "Keep the second sentence's subject together so the warning about his own people stays clear."),
    (3, 97, 72): (None, ("carve up the whole world.", "Proofs of Conquest", "to justify it.", "We're gathering them to stop that."), "Keep the approved title intact and leave the great powers' justification distinct from Maria's reason to collect the Proofs."),
    (3, 97, 114): (None, ("that Proof you're after,", "hidden in the ruins."), "Keep the bandit's uncertainty and the find in the ruins together."),
    (0, 126, 16): (None, ("our tribe", "draw strength from.", "Please accept it."), "The tribe has found something it can draw strength from. The gift request keeps its own beat."),
    (2, 118, 16): (None, ("our tribe", "source of hope at last.", "Please accept this."), "The retained wording captures the emotional support. Keep the request together."),
    (3, 100, 15): ("Thanks to you, we've finally found our people's source of strength. Please take this.", ("source of strength.", "Please take this."), "Use the speaker's gratitude and shared source of strength without turning the implement into a named sacred object."),
    (3, 88, 48): (f"What now, {FI}? We lack the guns for an assault.", ("We lack the guns for an assault.",), "Retain Xien's address and the insufficiency of the available guns. Protect the captain's longer substituted names."),
    (3, 88, 196): (None, ("your country's army", "fireworks and firecrackers?"), "The jibe depends on both fireworks and firecrackers. Keep them together."),
    (3, 88, 204): ("Gunpowder was invented in China. Westerners seem to have found more effective ways to use it in war. But its other uses seem new to you.", ("Gunpowder was invented in China.", "seem to have found", "to use it in war.", "But its other uses seem new to you."), "Preserve Maria's claim, her qualified comparison of wartime use, and her jab about these other uses. Put the jab after the page turn if the original allocation requires one."),
}
# The current wording of these turns differs from the cited older manuscript.
# These notes bind the retention to what the current ROM actually says.
RETENTIONS = {
    (0, 115, 17): "The disbelief and short confirmation tag keep Rafael's urgency and the promise that the group will return.",
    (0, 121, 45): "The cry for help gives the grandfather two short bursts of relief and an urgent grandson-rescue plea.",
    (0, 123, 146): "The speaker challenges the point of revenge and the idea that it can replace what the bandits lost.",
    (0, 126, 10): "The two sentences keep the find and the discoverers' right to retain it.",
    (1, 115, 50): "The immediate instruction to get the villagers to safety keeps its urgent intent.",
    (1, 121, 110): "The grandfather admits he doesn't know the item's origin and qualifies its value as hearsay.",
    (1, 123, 92): "The condemnation is explicitly about indiscriminate attacks and is expressed as the character's accusation.",
    (1, 123, 107): "The stammer and exclamation preserve the bandit's alarm and demand for an alternative.",
    (1, 123, 110): "The two sentences keep the rivalry, the fighting across the seas, and the call to end the rivalry.",
    (2, 106, 195): "The current wording keeps the expectation that something like this might happen and the prior request for village help.",
    (2, 108, 35): "The plea asks them to do what they can to prevent the Proof from reaching the Ottoman Empire.",
    (2, 115, 105): "The bandit's colloquial accusation answers the preceding argument without changing it; the copied scene remains byte-exact.",
    (2, 115, 109): "The rebuke and rhetorical question preserve both the futility of revenge and the idea of irrecoverable happiness.",
    (2, 115, 128): "The political statement retains the powers' intent, their justification, and the speaker's opposition.",
    (3, 88, 44): "The reaction conveys Maria's shock as the leader reveals his intent to attack the village.",
    (3, 97, 114): "The bandit's contraction and 'Dunno' fit his voice while he tells Maria where it was found and admits uncertainty.",
    (3, 100, 9): "The plain explanation makes the right to keep the dagger follow directly from discovering it.",
}
SPEAKER_FORMAT = re.compile(r"\{(?:SPEAKER:[0-9A-Fa-f]{2}|SYSTEM(?::[A-Fa-f0-9]+)?)\}")
MACRO_FORMAT = re.compile(r"\{MACRO:([A-Z]+)\}")


def normalize(text):
    return " ".join(MACRO_FORMAT.sub(r"\1", SPEAKER_FORMAT.sub("", text)).replace("{LB}", " ").split())


def historical(route):
    result = {}
    for name in HISTORY[route]:
        path = Path("translations") / (name + ".json")
        for index, row in enumerate(base.load(path)["records"]):
            result[row["id"]] = (path, index, row)
    return result


def allocated_page_planner():
    # A fixed speech payload longer than four complete rows must retain a
    # visible fifth row so its padding never produces a blank trailing page.
    source = checked_text(getsource(layout.bind_planner), {
        "'return (0,0,0,0,0,0,0),()'": "'return ((0,0,0,0,0,0,0),()) if line >= 5 else None'",
    })
    env = vars(layout).copy()
    exec(compile(source, __file__ + "::retain-allocated-second-page", "exec"), env)
    return env["bind_planner"]()


MULTIPAGE = allocated_page_planner()


def compile_row(row, fixed, phrases):
    if FI in row["english"]:
        names.compile_revision(row, phrases)
        return
    norm = layout.prior.layout.norm
    pairs = [(norm(a), norm(b)) for phrase in phrases for a, b in zip(phrase.split(), phrase.split()[1:])]
    planner = MULTIPAGE if len(fixed) - 1 > 4 * 36 else layout.plan_record
    plan = planner(row | dict(protected_pairs=pairs))
    assert all(any(p.casefold() in line.casefold() for line in plan["lines"]) for p in phrases), plan["lines"]
    payload = bytes.fromhex(plan["encoded_hex"])
    assert payload[0] == fixed[0] and len(payload) <= len(fixed)
    row.update(automatic_layout=plan, target_hex=payload.ljust(len(fixed), b" ").hex(),
               trailing_blank_bytes=len(fixed) - len(payload))
    layout.fit_storage_padding(row)


def review_exchange(group, route, block, ja, old, clean_arm, arm, inv, past, errors):
    jcmd, jtxt = native.raw_speeches(clean_arm, ja, inv)
    ecmd, etxt = native.raw_speeches(arm, old, inv)
    assert [c["word"] for c in jcmd] == [c["word"] for c in ecmd]
    records = []
    for source, current in zip(native.references(jcmd, jtxt), native.references(ecmd, etxt), strict=True):
        selector, number = source["selector"], source["record_index"]
        assert current["selector"] == selector and source["complete_preamble_hex"] == current["complete_preamble_hex"]
        ident = f"DK4_MES_B{block}_R{number:04d}"
        old_path, old_index, earlier = past[ident]
        assert all(earlier["review"].get(g) is True for g in native.GATES), (route, ident)
        before, fixed = [bytes.fromhex(row["raw_hex"]) for row in (source, current)]
        earlier_source = bytes.fromhex(earlier["source_hex"]).rstrip(b"\0")
        assert earlier_source.endswith(before) or before.endswith(earlier_source), (route, ident, earlier_source, before)
        previous = " ".join(fixed[1:].decode("cp932").split())
        old_english = earlier["english"]
        marker = f"{{SPEAKER:{selector:02X}}}" if selector != 254 else "{SYSTEM}"
        edit = EDITS.get((route, block, number))
        text, phrases, note = edit or (None, (), RETENTIONS.get((route, block, number), earlier["localization_note"]))
        row = dict(id=ident, route=route, group=group, block=block, file_path=f"/data/SC{route}.DK4",
            kind="system-FE" if selector == 254 else "progressive", source_selector=selector,
            speaker=earlier.get("speaker", earlier.get("source_actor_name", str(selector))),
            english=marker + (text or previous), previous_English=previous, decision="retention",
            source_reference=source | dict(block_sha256=native.digest(ja)), source_hex=source["raw_hex"],
            current_reference=current | dict(block_sha256=native.digest(old)), current_hex=current["raw_hex"],
            Japanese=before[1:].decode("cp932"), source_meaning=earlier["source_meaning"],
            localization_note=note, context=CONTEXT[group],
            earlier_review=dict(path=old_path.as_posix(), row_index=old_index, id=ident,
                                earlier_English=old_english, same_logical_English=normalize(old_english) == previous,
                                review=earlier["review"]), review=dict.fromkeys(native.GATES, True))
        if edit:
            assert selector != 254
            if FI in row["english"]:
                assert before[1:].count(b"FI") == fixed[1:].count(b"FI") == 1
            else:
                assert not any(token in before[1:] or token in fixed[1:] for token in (b"FI", b"FA", b"FO", b"FU", b"%"))
            try:
                compile_row(row, fixed, phrases)
            except (AssertionError, ValueError) as ex:
                errors.append((route, block, number, len(fixed)-1, row["english"], str(ex)))
            if row.get("target_hex", row["current_hex"]) != row["current_hex"]:
                row["decision"] = "revision"
        records.append(row)
    return records, ecmd


def collect():
    release = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    ctx = native.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    clean = base.NdsImage.open(native.CLEAN)
    clean_arm = clean.read_file(native.ARM)
    inv, _, _ = native.scoped_inventory()
    groups, errors = {}, []
    for route in range(4):
        file = f"/data/SC{route}.DK4"
        ja, en = [native.IlnkContainer.parse(i.read_file(file)).blocks for i in (clean, ctx.image)]
        past = historical(route)
        for group, blocks in BLOCKS.items():
            n = blocks[route]
            groups[route, n] = review_exchange(group, route, n, ja[n], en[n], clean_arm, ctx.arm, inv, past, errors)
    return release, ctx, inv, groups, errors


def validate_native(ctx, records):
    simple = [r for r in records if FI not in r["english"]]
    validator = checked_text(getsource(layout.native_validation), {
        "('before', 'current_hex'), ('after', 'target_hex')": "('after', 'target_hex'),",
    })
    env = vars(layout).copy()
    exec(compile(validator, __file__ + "::revised-progressive-validation", "exec"), env)
    env["native_validation"](ctx, simple)
    pictures = []
    for row in simple:
        pages = row["after_native"]["pages"]
        lines = [line for page in pages for line in native.visible_lines(page)]
        assert lines == row["automatic_layout"]["lines"], (row["id"], lines)
        for page in pages:
            pictures.append((f"SC{row['route']} {row['id'].split('_B')[1]} {page['page']}/{len(pages)}",
                             bytes.fromhex(page["native_plane_hex"])))
    dynamic = [r for r in records if FI in r["english"]]
    if dynamic:
        validator = checked_text(getsource(names.validate_pages), {
            "('before', 'after') if revision else ('retained',)": "('after',) if revision else ('retained',)",
            "assert len(pictures) == 22": "assert len(pictures) == 5",
        })
        scope = vars(names).copy()
        exec(compile(validator, __file__ + "::named-speaker-display-validation", "exec"), scope)
        pictures.extend(scope["validate_pages"](ctx, dynamic))
    return pictures


def main():
    if ROOT.exists() or MANUSCRIPT.exists():
        raise FileExistsError(ROOT)
    release, ctx, inv, groups, errors = collect()
    assert not errors, errors
    before = native.files(ctx.image)
    rows = [r for records, _ in groups.values() for r in records]
    edited = [r for r in rows if r["decision"] == "revision"]
    assert len(groups) == 20
    assert {(r["route"], r["block"], r["source_reference"]["record_index"]) for r in rows} >= EDITS.keys()
    changed = dict(native.transform(ctx.image, edited))
    paths = [f"/data/SC{i}.DK4" for i in range(4)]

    def banks(assets):
        return [native.IlnkContainer.parse(assets[f]).blocks for f in paths]

    oldbanks = banks(before)
    staged_banks = banks(before | changed)
    config = base.load(parent.MANIFEST)["relocations"][native.ARM]["reviewed_name_integration"]["catalog"]
    assert native.catalogue(ctx.arm, config, oldbanks) == native.catalogue(ctx.arm, config, staged_banks)
    for (route, blk), (records, original) in groups.items():
        block = staged_banks[route][blk]
        commands, speeches = native.raw_speeches(ctx.arm, block, inv)
        fields = ("offset", "word", "native_extent", "ancestor_0100_offsets")
        speech = [r["current_reference"] for r in records if r["decision"] == "revision"]
        nested = {r["command_offset"] for r in speech}
        nested.update(at for r in speech for at in r["ancestors"])
        for a, b in zip(original, commands, strict=True):
            assert all(a[k] == b[k] for k in fields)
            if a["offset"] not in nested:
                assert a["whole_command_hex"] == b["whole_command_hex"]
        for row, final in zip(records, native.references(commands, speeches), strict=True):
            assert final["raw_hex"] == row.get("target_hex", row["current_hex"])
            assert final["complete_preamble_hex"] == row["current_reference"]["complete_preamble_hex"]
            row["staged_reference"] = final | dict(block_sha256=native.digest(block))
    credits = {(r["file_path"], r["id"]) for r in base.load(base.LEDGER)[base.CONTEXT]["integrated_record_keys"]}
    assert all((r["file_path"], r["id"]) in credits for r in rows)
    pictures = validate_native(ctx, edited)
    for path, blob in changed.items():
        ctx.image.replace_file(path, blob)
    assert {p for p, value in native.files(ctx.image).items() if value != before[p]} == changed.keys()
    ROOT.mkdir(parents=True)
    ctx.image.save(ROM)
    for path in changed:
        ctx.image.replace_file(path, before[path])
    assert bytes(ctx.image.rom.save()) == parent.ROM.read_bytes()
    sheets = FunctionType(layout.contact_sheets.__code__, vars(layout) | dict(ROOT=ROOT))(pictures)
    candidate = base.digest(ROM)
    base.save(MANUSCRIPT, dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
        encoder="dialogue-relocatable-v1", review_gates=list(native.GATES), candidate_sha256=candidate,
        previous_sha256=release["candidate_sha256"], records=rows, zero_new_credit=True))
    base.save(STORED, dict(candidate_sha256=candidate, previous_sha256=release["candidate_sha256"],
        target_ARM9_sha256=native.digest(ctx.arm), target_story_archive_sha256={p: native.digest(b) for p, b in changed.items()},
        whole_parent_inverse=True, sheets=sheets, preview_count=len(pictures), manuscript_sha256=base.digest(MANUSCRIPT)))
    print(len(rows), "speeches;", len(edited), "revisions;", len(pictures), "revised display previews")


if __name__ == "__main__":
    main()
