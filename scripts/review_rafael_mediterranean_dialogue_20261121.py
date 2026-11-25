"""Review four complete Rafael exchanges with the registered story formatter."""
from collections import Counter
from pathlib import Path
from types import FunctionType
import re

from scripts import prepare_london_guild_assignments_20261118 as pairing
from scripts import register_rafael_first_market_20261121 as parent
from scripts import stage_london_guild_assignments_20261118 as planner
from scripts.review_company_name_dialogue_20261121 import GATES, TOKEN, logical


base, native = parent.base, parent.native
ROOT = Path("work/rafael_mediterranean_dialogue_20261121")
SOURCE = ROOT / "paired_source.json"
OUTPUT = ROOT / "contextual_review_v2.json"
BLOCKS = ((47, 48, 49, 50), (), (), ())
CONTEXT = ("Rafael's Mediterranean debrief and early crew exchanges.",) * 4
SCENES = {
    47: "After Hayreddin grants passage, the crew weighs Pasha's strength, when to trade, and why the larger cities are still worth visiting. Two original paths distinguish Pasha alone from Pasha and Valdes.",
    48: "Julio's errand in Athens leads to Hans and Arcadius joining the crew. Claudio's skepticism gives way to admiration. The discussion then moves from the legend of the Proofs to a rumored lead in southern Africa and Hans's practical role.",
    49: "Lil confronts Rafael about trading in the North Sea. Camille tries to soften her approach, and Rafael gradually recognizes the proposed pact. The crew then weighs whether to seek opportunities elsewhere.",
    50: "Lil concedes that Rafael outmaneuvered her and gives him a tool for deciphering the map. Lil and Camille know what their preparations and congratulations mean. Rafael plays along and leaves puzzled.",
}

# A missing replacement means the prose works and only the wrapping changes.
EDITS = {
    47: {
        5: ("I still can't read Hayreddin, but we should be able to sail the Mediterranean now.",
            ("I still can't read Hayreddin,", "we should be able to sail", "the Mediterranean now."), "Keep Julio's guarded relief and his uncertainty about Hayreddin. Passage is the practical gain."),
        17: ("Right. If pirates like that attack every time we enter the Mediterranean, we won't last long.",
             ("every time we enter", "the Mediterranean,", "we won't last long."), "Restore the region Janus names and keep his dry prediction together."),
        44: (None, ("steer clear of the Ottomans.", "It's too risky."), "Julio's calm warning fits the abrupt change from relief to caution. Keep the warning phrase together."),
        53: ("Pasha's Ottomans hold roughly the eastern half of the sea. If they come after us, we probably can't win.",
             ("Pasha's Ottomans", "the eastern half of the sea.", "If they come after us,", "we probably can't win."),
             "Restore Julio's assessment as probable, and keep the approximate territory and the risk of being targeted."),
        63: ("Then we'd better leave the Mediterranean for later. Pasha's Ottoman forces have too much sway there.",
             ("the Mediterranean for later.", "Pasha's Ottoman forces", "have too much sway there."), "Name Pasha's Ottoman force in the original one-faction branch and keep Rafael's conclusion intact."),
        70: ("Valdes's Spanish forces and Pasha's Ottoman forces have a lot of sway there. We'd better leave it for later.",
             ("Valdes's Spanish forces", "Pasha's Ottoman forces", "have a lot of sway there.", "We'd better leave it for later."),
             "Preserve both powers in this separate branch. Keep its decision to postpone the Mediterranean together."),
        77: ("We shouldn't push for trading contracts. Better to avoid provoking them.",
             ("We shouldn't push", "for trading contracts.", "Better to avoid provoking them."), "Keep the advice against forcing contracts and Julio's practical reason for restraint."),
        81: ("We can't skip the big cities. We might find skilled navigators. At least we can look for recruits.",
             ("We can't skip the big cities.", "We might find skilled navigators.", "At least we can look for recruits."),
             "Keep the limited reason for visiting and the possibility of finding skilled people."),
        102: ("Yeah. If we're heading into other waters, we'll need stronger ships. We'd better toughen up, too.",
              ("into other waters,", "we'll need stronger ships.", "We'd better toughen up, too."), "Keep Claudio informal and preserve both kinds of preparation."),
        106: ("Exactly. And remember to recruit navigators when you visit the big cities.",
              ("recruit navigators", "visit the big cities."), "Keep Julio's reminder and the actual purpose of visiting the larger towns."),
        122: ("Well, things are about to get busy.", ("things are about to get busy.",), "Janus anticipates the work ahead as Rafael starts to feel its weight."),
    },
    48: {
        56: ("Clau, you're always complaining.", ("Clau, you're always complaining.",), "Rafael uses the familiar form Clau in the Japanese. Keep it consistent with their opening exchange."),
        71: ("Good timing. I'll go look into the Proof of Conquest.", ("look into", "the Proof of Conquest."),
             "Give Julio a conversational reason to leave. Keep the established name together."),
        81: ("Oh, that's right. Julio, what was that errand?", ("what was that errand?",), "Keep the original callback to Julio's errand when this branch is used."),
        86: (None, ("look into", "the Proof of Conquest."), "Keep the full name with its article and preserve this alternate introduction."),
        125: (None, ("anywhere will do!", "a faraway country."), "Keep Hans's eagerness and the two examples of where he is willing to travel aboard the ship."),
        217: (None, ("young... man.", "introduce yourself."), "The hesitation is Hans's joke. Keep his wording and audible pause together before introducing Arcadius."),
        247: (None, ("his dedication to learning.", "a promising... young man."), "The repeated hesitation is intentional. Keep the whole description and the parallel to Hans's introduction."),
        250: (None, ("I still have a lot to learn", "from all of you."), "Arcadius credits a little preparation and politely asks to keep learning from the group."),
        280: ("I'm glad we have a scholar like him aboard. Aren't you, Clau?", ("a scholar like him aboard.", "Aren't you, Clau?"),
              "Rafael wants his friend's agreement that a learned scholar is a welcome addition. Keep the familiar name."),
        284: ("Yeah, I guess. Good luck with your research, Doctor! Oh, and you too!", ("Good luck with your research,", "Oh, and you too!"),
              "Claudio softens after hearing Hans out. Keep his quick addition for the assistant separate from his well-wishing."),
        327: ("Oh! You're interested in the Proof too?", ("You're interested", "in the Proof too?"), "Make Hans's excited question idiomatic and keep the subject of his research."),
        366: (None, ("We'll earn them ourselves!",), "Keep Rafael's earnest resolve as a complete sentence after the initial burst of enthusiasm."),
        406: ("I heard a rumor the other day that someone took one of the Proof of Conquest maps to southern Africa.",
              ("I heard a rumor the other day", "took one of", "the Proof of Conquest maps", "to southern Africa."),
              "Keep the date relative, identify what was taken and preserve that Hans heard a rumor."),
    },
    49: {
        20: ("You gotta be blunt about this! Camille, stay out of it.", ("You gotta be blunt about this!", "Camille, stay out of it."),
             "Keep Lil's blunt point and her separate order to Camille, who is trying to avoid a fight."),
        43: ("Need something?! Who said you could trade in the North Sea?!", ("Who said you could trade", "in the North Sea?!"),
             "Preserve Lil's indignant echo and the question of who granted permission."),
        51: ("Sorry, but... I'm still trying to figure out what's going on.", ("I'm still trying to figure out", "what's going on."),
             "Keep Rafael trying to defuse the argument while admitting he does not follow it."),
        122: (None, ("All right, let me explain.",), "Keep Lil's brusque decision to explain together after she decides Rafael seems decent."),
        126: (None, ("a pretty big area, right?",), "The short question tag is Lil's invitation to agree. Keep it with what she is asking about."),
        213: ("Ugh. You really take the wind out of my sails.", ("the wind out of my sails.",),
              "Lil loses momentum when Rafael takes her challenge at face value. Keep her exasperation and the change in tone."),
        244: ("It's a big world! Look past this sea. Sail west to the New World or go unravel the mysteries of the far east!",
              ("Look past this sea.", "to the New World", "the mysteries of the far east!"), "The alternatives keep Lil animated. Keep the destination and her second example readable."),
        259: ("If you want to take us on, that's another story. We've got plans of our own. Got it?",
              ("want to take us on,", "that's another story.", "plans of our own."), "Keep Lil's challenge and veiled response in the original conditional warning."),
        336: ("Then we've got the same enemy! No point fighting each other. Yes, that's it!",
              ("we've got the same enemy!", "No point fighting each other.", "Yes, that's it!"), "Keep both sides' common enemy and Lil's quick agreement with her own conclusion."),
        363: (None, ("You understand, don't you?", "We're busy too, so see you around!"), "Keep Lil's check for agreement together before she ends the discussion on her own terms."),
    },
    50: {
        37: (None, ("We haven't finished", "getting ready yet!"), "Camille has caught up with Lil and reminds her that preparation is unfinished. Keep the negative verb together."),
        49: ("That's right. I suppose it's been a while, in a way. Ha ha.", ("it's been a while,", "in a way. Ha ha."),
             "Restore Camille's tentative greeting on seeing Rafael again and keep the awkward little laugh."),
        53: (None, ("being rude again, are you?",), "Camille's worry is a single teasing question. Keep the tag attached."),
        73: ("Well, I guess I've found something to live for besides making money.", ("something to live for", "besides making money."),
             "Lil hints at a different way to live without explaining what has changed."),
        103: (None, ("I have no idea what she means...)",), "Keep Rafael's private bewilderment inside the original parentheses after his startled reply."),
        114: (None, ("Lil, Camille, thank you!", "live up to your expectations!"),
              "Keep both names and Rafael's sincere promise. His confidence lands before the private question that closes the scene."),
    },
}

CURRENT_RETENTIONS = {
    48: {
        17: "Janus's first-person reaction conveys the city's scholarly atmosphere.",
        92: "The complete Proof of Conquest name follows Julio's explanation and makes Rafael's question easy to follow.",
        140: "Hans recognizes Rafael as someone from the ship that just arrived, then asks to come aboard.",
        144: "The Port Worker's warning uses Captain as in the source and preserves the request for a free passage.",
        167: "The specialist's enthusiasm leads into a direct plea to travel and see the world.",
        189: "Claudio's sudden admiration keeps Hans's age, resolve and the risk of the voyage explicit.",
        192: "Rafael's open welcome follows Claudio's change of heart and the small stutter softens it.",
        200: "Hans asks a second favor courteously with the source's form of address.",
        324: "Julio recognizes Hans and explains their acquaintance and the length of his research.",
        331: "Rafael answers the question about interest with a plain admission that he does not know what the Proof is.",
        347: "Hans attributes the seven treasures and differently shaped maps to the ancient text.",
        354: "The unfinished thought conveys Rafael's realization before Julio answers it.",
        370: "Keep Claudio's given-name substitution, teasing opening and practical demand to see a Proof.",
        393: "Hans's alarm is an amused reaction to the crew's ambitions after he comes aboard.",
        438: "Keep the X-button instruction on the item information screen and preserve the speakerless notice.",
    },
    49: {
        5: "Rafael notices the noise and uses the Market name shown in town.",
        15: "Camille invokes a familiar warning that is still meant to prevent the fight.",
        47: "Claudio's patronizing address and threat fit his reply to Lil's challenge.",
        90: "Lil dismisses Camille's advice and plainly asserts which company claims these waters.",
        107: "The hesitation and then short confirmation convey Claudio's response to Lil's doubt.",
        187: "Rafael's practical objection turns on the trading contract. The current three lines keep the contract and his whole question together.",
        271: "Lil is briefly caught off guard by the idea that she's the one asking a favor.",
        275: "Rafael's teasing observation recognizes Lil's pride and leads into her indignant reply.",
        311: "Julio's aside preserves the name substitution and the practical suggestion to earn money somewhere else.",
        388: "Claudio makes his disagreement clear, then gives Rafael the decision and agrees to follow it.",
    },
    50: {
        40: "Camille's polite recognition preserves the dynamic surname.",
        61: "Camille understands why Lil gave Rafael the item and uses his surname at runtime.",
        82: "Lil's incredulous question follows Rafael's apparent realization while leaving the subject implicit.",
        108: "Camille makes a courteous exit with Lil and addresses Rafael by his substituted name.",
    },
}


def earlier_words(row):
    words = row.get("logical_English") or row["english"]
    words = re.sub(r"\{MACRO:([A-Z]+)\}", r"\1", words)
    return logical(re.sub(r"\{(?:SPEAKER:[A-Z0-9]+|PAD)\}", "", words)).replace("…", "...")


def main():
    assert not OUTPUT.exists()
    if not SOURCE.exists():
        FunctionType(pairing.main.__code__, vars(pairing) | globals())()
    pack, release = map(base.load, (SOURCE, parent.RELEASE))
    assert pack["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert pack["clean_sha256"] == release["clean_input_sha256"] == base.digest(native.CLEAN)
    records, plans, previous_reviews, failures = [], {}, {}, []
    for group in pack["groups"]:
        block = group["block"]
        path = Path(f"translations/rafael_B{block}_contextual_final_review_v1.json")
        previous_reviews[str(path)] = base.digest(path)
        earlier = {r["source_reference"]["offset"]: r for r in base.load(path)["records"]}
        changes = dict(EDITS[block])
        current_notes = dict(CURRENT_RETENTIONS.get(block, {}))
        for entry in group["records"]:
            number, selector = entry["source_record_index"], entry["selector"]
            prior = earlier.pop(entry["source_offset"])
            assert entry["Japanese"] == prior["source_Japanese"] and prior["source_selector"] == selector
            assert all(prior["review"].values()) and entry["native_command_word"] == 0x4000
            japanese, current = (bytes.fromhex(entry[f"{side}_body_hex"]) for side in ("source", "current"))
            prefix = bytes([selector])
            assert prior["source_hex"] == (prefix + japanese).hex()
            english = logical(entry["current_English"])
            changed = number in changes
            revised, phrases, reason = changes.pop(number, (None, (), ""))
            retained = current_notes.pop(number, None)
            if not changed:
                assert retained or earlier_words(prior) == english.replace("…", "..."), (block, number, english)
                reason = retained or prior["localization_note"]
            paragraph = revised or english
            assert TOKEN.findall(entry["Japanese"]) == TOKEN.findall(english) == TOKEN.findall(paragraph)
            refs = {side: dict(file_path=group["file_path"], block=block, offset=entry[f"{side}_offset"],
                               command_offset=entry[f"{side}_command_offset"],
                               archive_sha256=group[f"{side}_archive_sha256"], block_sha256=group[f"{side}_block_sha256"],
                               exact_hex=(prefix + value).hex())
                    for side, value in (("source", japanese), ("current", current))}
            row = dict(id=prior["id"], file_path=group["file_path"], route=0, block=block,
                       source_record_index=number, native_command_word=0x4000, native_slots=[],
                       source_selector=selector, kind="system-FE" if selector == 254 else "progressive",
                       source_reference=refs["source"], current_reference=refs["current"],
                       source_hex=(prefix + japanese).hex(), current_hex=(prefix + current).hex(),
                       Japanese=entry["Japanese"], previous_English=english, english=paragraph,
                       speaker=prior["speaker"], context=SCENES[block], source_meaning=prior["source_meaning"],
                       localization_note=reason, protected_phrases=list(phrases),
                       decision="revision" if changed else "retention",
                       finding="prose and wrap" if revised else "wrap" if changed else "retention",
                       review=dict.fromkeys(GATES, True) | {"formatting": not changed})
            if changed:
                assert selector != 254
                try:
                    body, plan = planner.plan_progressive(row, selector, current, japanese)
                    assert body.rstrip(b" ") != current.rstrip(b" ") and plan["expected_native_pages"] == 1
                except (ValueError, AssertionError) as error:
                    failures.append((row["id"], paragraph, phrases, str(error)))
                else:
                    plans[row["id"]] = plan
                    print(row["id"], plan["lines"])
            records.append(row)
        assert not earlier and not changes and not current_notes
    assert len(records) == 195
    assert not failures, failures
    decisions = dict(Counter(row["decision"] for row in records))
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
                         target_locale="en-US", review_gates=GATES, previous_sha256=pack["candidate_sha256"],
                         previous_registry_sha256=release["registry_sha256"], source_packet=str(SOURCE),
                         source_packet_sha256=base.digest(SOURCE), earlier_contextual_reviews=previous_reviews,
                         records=records, plans=plans, decisions=decisions,
                         findings=dict(Counter(r["finding"] for r in records)), new_editorial_credit=0,
                         status="Contextual review complete. Formatting approval pending for changed text."))
    print(len(records), decisions)


if __name__ == "__main__":
    main()
