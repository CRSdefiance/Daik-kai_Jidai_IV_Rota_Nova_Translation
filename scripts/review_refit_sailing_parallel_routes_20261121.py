"""Review the four parallel sailing and refit lessons against their clean scenes."""
from collections import Counter
from pathlib import Path

from scripts import register_fernando_parallel_routes_20261121 as parent
from scripts import register_rafael_refit_sailing_lessons_20261121 as rafael
from scripts.review_hodram_alexandria_tutorial_20261121 import GATES, TOKEN, logical


base, native = parent.base, parent.native
ROOT = Path("work/analysis/refit_sailing_parallel_routes_20261121")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v1.json"
BLOCKS = ((), (171,), (166, 167), (138,))
FILES = {
    171: "hodram_B171_B190_contextual_final_review_v1.json",
    166: "lil_B166_contextual_final_review_v1.json",
    167: "lil_B167_contextual_final_review_v1.json",
    138: "maria335_B137_B151_integrated_final_review_v1.json",
}
CONTEXT = {
    171: "A bored shipwright offers Hodram a sailing lesson. Manuel bristles at the offer on the refusal path. When Hodram accepts, the shipwright explains four extra rigs and asks Manuel why an angled tailwind works better.",
    166: "Manuel worries that Lil's poorly maintained ship is crying. Camille and Fernando challenge Lil, then Camille persuades Manuel to take care of the ship. Manuel offers optional refit advice for long voyages.",
    167: "A bored shipwright offers Lil a sailing lesson. The crew pushes back when she declines. When she accepts, his practical rigging advice leads to a question Manuel answers.",
    138: "Xien spots Manuel admiring Maria's ship. Manuel's eye for its neglected maintenance impresses the pair. Maria invites him to return to life at sea, and he offers optional refit advice.",
}

# Only shared teaching lines use Rafael's verified wording. Each route's
# introductions, reactions, choice labels and character beats are reviewed below.
SAILS = {
    68: (69, "Introduce the square and lateen distinction using the same terms as the refit help."),
    71: (72, "Explain why a square sail is transverse in the shipwright's plain voice."),
    75: (76, "Preserve the square sail's limited rotation and its performance in both wind directions."),
    78: (79, "Restore the old hands' name for a triangular sail and retain the difference in orientation."),
    81: (82, "Preserve the lateen's good headwind angle and lower speed with a following wind. Keep the check-in together."),
    84: (85, "Move from basic sails to the optional rigs."),
    88: (89, "Name the topsail formally and preserve its square shape and position high on each mast."),
    92: (93, "Keep the staysail's position ahead of a mast and the overlap that prevents pairing it with a lateen."),
    95: (96, "Name the spritsail, its crosswise bow mounting and the small-ship restriction."),
    98: (99, "The jigger spanker is like adding a small mast. Preserve the comparison and the large-ship restriction."),
    101: (102, "Keep the two-mast threshold and the wind-angle comparison in a single question."),
    105: (106, "The shipwright turns the wind example into a question for Manuel."),
    109: (110, "Manuel gives the cause tentatively. Keep the established fore-and-aft language."),
    112: (113, "The rearmost mast catches wind directly astern, so the forward masts don't help."),
    115: (116, "Explain the best wind direction and preserve the need to trim the sails to match."),
}
REFIT = {
    (134, 78): (87, "Address the admiral and ask permission to explain how to refit rooms on the flagship."),
    (149, 93): (102, "Narrow the lesson to rooms useful on long voyages."),
    (153, 97): (106, "Use the Speech, First Mate's Office and Chapel labels. Someone with high Speech can help ease sail crew discontent in either room."),
    (157, 101): (110, "Use the canonical Galley and Nursery names and keep both water and food consumption."),
    (161, 105): (114, "Use Surgeon and Sickbay as displayed in the game. Preserve fatigue, illness, injuries, and both groups who benefit."),
    (165, 109): (118, "Use Cabin and Lounge. Preserve the faster recovery for a sick or injured navigator assigned there."),
    (169, 113): (122, "Keep the Lumber Room repairs at sea distinct from refits and repairs at the shipyard."),
    (172, 116): (125, "Manuel asks whether his quick explanation was useful."),
    (175, 119): (128, "Manuel gives responsibility back to the admiral and encourages careful refits."),
    (181, 125): (134, "Manuel accepts the refusal and lets the admiral make the decision."),
}

EDITS = {
    171: {
        5: ("Admiral. Want a sailing lesson?", (), "Start with the shipwright's direct, informal offer."),
        12: ("I've been bored out of my skull lately. You'd be doing me a favor.", ("doing me a favor.",), "His boredom explains why he calls the lesson a favor."),
        45: ("When it comes to ships, we're past needing lessons.", ("we're past needing lessons.",), "Cesare confidently backs the refusal in his own style."),
        51: ("Fair enough. You look like you know your ships. I'll wait for somebody who looks a little greener.", ("looks a little greener.",), "The shipwright backs off with a casual joke about finding a beginner."),
        65: ("A sailing ship lives by its sails.", (), "Keep the old hand's simple lead-in to the rigging lesson."),
        138: ("Thanks for hearing me out. Well, back to work.", ("back to work.",), "Close with the shipwright's thanks and his return to work."),
    },
    166: {
        5: ("Maybe the sails are in the wrong place... No, could it be...", ("the wrong place...",), "Manuel is thinking aloud and changes his mind before Lil interrupts."),
        20: ("Maybe some extra sails... Or a different type of basic sail...", ("extra sails...", "type of basic sail..."), "Keep the two possible refits distinct without introducing a new sail category."),
        27: ("More gun batteries would make her stronger... Or maybe a different kind of cannon.", ("More gun batteries", "kind of cannon."), "Preserve adding batteries and changing cannon type as alternatives Manuel considers."),
        44: ("I can't see a ship without wondering what I'd do with her. Old habits from my days at sea...", ("Old habits", "my days at sea..."), "Manuel admits old sea habits explain the stream of suggestions."),
        52: ("This may be none of my business, but your ship is crying. Please take better care of her.", ("your ship is crying.", "better care of her."), "Keep the recurring image of the crying ship and Manuel's plea."),
        60: ("I've said more than I should. Please don't take it the wrong way. I'll be on my way.", ("don't take it the wrong way.", "I'll be on my way."), "Manuel apologizes before leaving, even after Lil calls him back."),
        68: ("What are you talking about? He's amazing! FI, we could use someone like him aboard.", ("someone like him aboard.",), "Camille disagrees with Lil and keeps the original given-name address."),
        75: ("FI, you don't take care of her at all. That's why the ship's crying.", ("at all.", "the ship's crying."), "Camille explicitly connects Lil's lack of care to Manuel's metaphor."),
        98: ("Don't just shrug it off! We need someone who'll love the ship in your place, FI.", ("love the ship", "in your place,"), "Camille rebukes Lil's shrug and proposes someone who will care for the ship in her place."),
        102: ("Then she'd stop crying, I'm sure of it. Come on, can we ask him to sail with us?", ("can we ask him", "to sail with us?"), "Camille keeps the crying metaphor and asks for permission."),
        106: ("Hmm... If you think it's a good idea, Camille, then fine.", ("a good idea,",), "Preserve Lil's reluctance and eventual trust in Camille's judgment."),
        109: ("Excuse me, would you look after our ship?", ("look after our ship?",), "Camille politely asks for help with their ship without inventing a relationship."),
        116: ("I'm sure you're just as capable as those of us still sailing. Someone who loves ships like you do couldn't forget the sea.", ("still sailing.", "couldn't forget the sea."), "Camille argues for Manuel's continuing competence from his obvious love of ships."),
        119: ("Well, you've got a point...", ("you've got a point...",), "Manuel is beginning to yield."),
        130: ("Let me introduce myself properly. Manuel Almeida, at your service.", ("Manuel Almeida,", "at your service."), "Keep his full established name in the formal second introduction."),
    },
    167: {
        5: ("Admiral. Want a sailing lesson?", (), "Keep the shipwright's brief offer in the same everyday voice."),
        12: ("I've been bored out of my skull lately. You'd be doing me a favor.", ("doing me a favor.",), "The shipwright wants someone to teach because he's bored."),
        30: ("Come now. Don't sell us short.", ("Don't sell us short.",), "Janus takes mild offense at the shipwright's assumption."),
        45: ("When it comes to ships, we're past needing lessons.", ("we're past needing lessons.",), "Cesare confidently backs Janus on the refusal path."),
        51: ("Fair enough. You look like you know your ships. I'll wait for somebody who looks a little greener.", ("looks a little greener.",), "Keep the shipwright's casual retreat and joke about beginners."),
        138: ("Thanks for hearing me out. Well, back to work.", ("back to work.",), "Close with his thanks and return to work."),
    },
    138: {
        4: ("FI, there's someone by our ship.", ("by our ship.",), "Xien calls Maria's attention to the stranger using her original given name."),
        20: ("But this ship... Wait. Are you Admiral FA?", ("Are you Admiral",), "Manuel interrupts his thought as he recognizes Maria. Keep the original family-name form."),
        26: ("She could use a little more care... Give her some attention, or she'll start crying.", ("a little more care...", "she'll start crying."), "Manuel says the ship has been neglected and introduces the crying-ship metaphor."),
        37: ("I'm Manuel. I used to be a navigator. Forgive me for speaking out of turn...", ("used to be a navigator.", "speaking out of turn..."), "Keep his introduction, earlier role, and apology together."),
        41: ("He's right about the upkeep. Anyone who can spot that at a glance knows ships.", ("at a glance",), "Xien agrees with the diagnosis and sees skill in Manuel's immediate observation."),
        45: (None, ("a deep love of ships.",), "Maria's observation is accurate and natural. Keep the love-of-ships phrase together."),
        48: ("You love ships so much. Why did you stop being a navigator? Would you mind telling me?", ("stop being a navigator?",), "Keep Maria's curiosity about why Manuel left navigation, and the polite invitation to explain."),
        74: ("Thank you. Being around ships is what I live for. I'd be delighted to sail with you.", ("what I live for.", "to sail with you."), "Manuel accepts with gratitude and keeps ships as his reason for doing so."),
    },
}

KEEPS = {
    171: {
        8: "Hodram echoes the unusual offer in two words.",
        18: "Listen clearly accepts the lesson.",
        20: "The brief, polite refusal clearly declines it.",
        29: "Manuel questions the shipwright's implied assessment of the crew.",
        33: "Janus agrees after a short pause.",
        62: "The shipwright encourages a willing listener in his own voice.",
        119: "Janus acknowledges the explanation simply.",
        131: "Cesare's surprise says he had never thought of it, followed by recognition.",
    },
    166: {
        8: "Lil bluntly asks what the stranger wants with the ship.",
        12: "Manuel confirms ownership and says a little work would improve her.",
        16: "The question marks show Lil hasn't caught up with Manuel's muttering.",
        23: "She tentatively tries to interrupt.",
        30: "Lil's patience runs out and she asks who he is.",
        33: "Manuel apologizes for becoming absorbed in someone else's ship.",
        37: "Manuel introduces himself and states his former job.",
        40: "Lil repeats his job with mild skepticism.",
        48: "Manuel apologizes for being forward and asks to add one thing.",
        56: "Lil calls him back before he can leave.",
        64: "Lil sums him up tersely.",
        71: "Lil asks why they need someone like Manuel.",
        87: "Fernando mischievously adds the crew's own complaint.",
        94: "Lil admits she knows nothing about machinery and tries to excuse herself.",
        112: "Manuel understands the invitation and hesitates because of his years away.",
        123: "Camille asks him to care for the ship, repeating the crying metaphor.",
        127: "Manuel thanks him and accepts the sincere offer.",
        140: "The affirmative caption answers the optional tutorial offer politely.",
        142: "Decline applies to the offered lesson after recruitment.",
    },
    167: {
        8: "Lil's short reaction preserves her surprise.",
        18: "Okay fits Lil's casual acceptance.",
        20: "The concise refusal clearly declines the lesson.",
        33: "Manuel agrees with Janus.",
        62: "The shipwright encourages her after a positive answer.",
        65: "The brief saying connects sailing ships to the discussion of rigs.",
        119: "Janus expresses quick understanding.",
        131: "Cesare says the answer explains something he hadn't considered.",
    },
    138: {
        9: "Manuel's admiration is immediately followed by misgivings.",
        12: "Maria asks why the stranger is there.",
        16: "Manuel's image of hearing the ship's heartbeat preserves his poetic voice.",
        23: "Maria confirms her identity and asks what he notices about the ship.",
        30: "Xien calls the imagery poetic without rejecting it.",
        33: "Maria asks directly who he is.",
        52: "Manuel gently avoids discussing his past.",
        56: "Maria explicitly invites him to consider returning to sea and life aboard ship.",
        59: "Manuel asks for confirmation without assuming she is offering a job.",
        63: "Maria says what she wants him to do aboard her ship.",
        66: "The silence leaves Manuel time to take in the offer.",
        70: "Maria emphasizes that the decision is his.",
        84: "The polite acceptance is clear.",
        86: "The polite refusal applies to the optional advice.",
    },
}


def decisions():
    verified = {(r["block"], r["source_record_index"]): r for r in base.load(rafael.REVIEW)["records"]}
    shared = {}
    for target in (171, 167):
        for idx, (ref, note) in SAILS.items():
            shared[target, idx] = verified[180, ref], note
    for (lil, maria), (ref, note) in REFIT.items():
        shared[166, lil] = shared[138, maria] = (verified[179, ref], note)
    return shared


def main():
    assert not OUTPUT.exists()
    packet, release = map(base.load, (SOURCE, parent.RELEASE))
    assert packet["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert packet["clean_sha256"] == release["clean_input_sha256"] == base.digest(native.CLEAN)
    shared = decisions()
    rows = []
    for group in packet["groups"]:
        route, path, block = (group[k] for k in ("route", "file_path", "block"))
        prior = {r["source_reference"]["offset"]: r for r in base.load(Path("translations") / FILES[block])["records"]
                 if r["block"] == block}
        scoped = {i for b, i in shared if b == block}
        edits, keeps = EDITS[block], KEEPS[block]
        assert len(scoped | edits.keys() | keeps.keys()) == len(scoped) + len(edits) + len(keeps)
        assert scoped | edits.keys() | keeps.keys() == {r["source_record_index"] for r in group["records"]}
        for entry in group["records"]:
            index, selector = entry["source_record_index"], entry["selector"]
            previous = prior.pop(entry["source_offset"])
            assert previous["source_Japanese"] == entry["Japanese"] and previous.get("source_selector") == selector
            current = logical(entry["current_English"])
            reference = None
            if index in scoped:
                parallel, reason = shared[block, index]
                assert parallel["source_selector"] == selector
                target, phrases, note = parallel["english"], parallel["protected_phrases"], reason
                reference = dict(id=parallel["id"], reference=parallel["source_reference"],
                                 manuscript=str(rafael.REVIEW), sha256=base.digest(rafael.REVIEW))
                edit = target != current
                if not edit:
                    note += " The current wording already matches the verified lesson."
            else:
                edit = index in edits
                target, phrases, note = edits[index] if edit else (current, (), keeps[index])
            english = target or current
            assert TOKEN.findall(entry["Japanese"]) == TOKEN.findall(current) == TOKEN.findall(english)
            leading = "" if selector is None else f"{selector:02x}"
            refs = {side: dict(file_path=path, block=block, offset=entry[f"{side}_offset"],
                              command_offset=entry[f"{side}_command_offset"],
                              archive_sha256=group[f"{side}_archive_sha256"], block_sha256=group[f"{side}_block_sha256"],
                              exact_hex=leading + entry[f"{side}_body_hex"]) for side in ("source", "current")}
            rows.append(dict(id=previous["id"], file_path=path, route=route, block=block, source_record_index=index,
                native_command_word=entry["native_command_word"], native_slots=entry["slots"], source_selector=selector,
                kind="typed-choice-label" if selector is None else "progressive",
                source_reference=refs["source"], current_reference=refs["current"],
                source_hex=refs["source"]["exact_hex"], current_hex=refs["current"]["exact_hex"],
                Japanese=entry["Japanese"], previous_English=current, english=english, speaker=previous["speaker"],
                context=CONTEXT[block], source_meaning=previous["source_meaning"], localization_note=note,
                shared_wording_reference=reference, protected_phrases=list(phrases),
                review=dict.fromkeys(GATES, True) | {"formatting": not edit},
                decision="revision" if edit else "retention",
                finding="retention" if not edit else "wrap" if english == current else "prose and wrap"))
        assert not prior
    assert len(rows) == 134
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
        target_locale="en-US", review_gates=GATES, previous_sha256=release["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"], source_packet=str(SOURCE), source_packet_sha256=base.digest(SOURCE),
        records=rows, decisions=dict(Counter(row["decision"] for row in rows)),
        findings=dict(Counter(row["finding"] for row in rows)), new_editorial_credit=0,
        status="Contextual review complete. Revisions await native verification."))
    print(f"Reviewed {len(rows)} records in four complete sailing and refit lessons.")


if __name__ == "__main__":
    main()
