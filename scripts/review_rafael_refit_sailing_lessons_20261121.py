"""Revisit the full flagship refit and sail-rigging conversations."""
from collections import Counter
from pathlib import Path

from scripts import register_parallel_ship_lessons_20261121 as parent
from scripts.review_hodram_alexandria_tutorial_20261121 import GATES, TOKEN, logical


base, native = parent.base, parent.native
ROOT = Path("work/rafael_refit_sailing_lessons_20261121")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v3.json"
BLOCKS = ((179, 180), (), (), ())
HISTORY = Path("translations/rafael_B177_B180_integrated_final_review_v1.json")
CONTEXT = {
    179: "Manuel praises the ship as a living thing and worries he has overstepped. Janus and Rafael agree to recruit him for that care. Manuel is moved to sail again and offers optional advice on flagship rooms before turning responsibility back over to Rafael.",
    180: "A bored shipwright offers an optional lesson to pass the time. The crew can decline or hear about square and lateen sails, four extra rigs, and why multiple masts work better with wind off the quarter. Manuel supplies the reason while Janus and Cesare listen.",
}

REVISIONS = {
    179: {
        16: ("Did you want to ask us about the ship?", ("ask us about the ship?",), "Janus asks a friendly question after Rafael worries something is wrong."),
        24: ("(Huh. That's an interesting way to put it...)", (), "Janus reacts privately to Manuel talking about the ship as if she were alive."),
        27: ("Keep taking good care of her. Treat her right, and she'll serve you well. A ship's a living thing, after all.", ("she'll serve you well.", "A ship's a living thing,"), "Keep both the practical advice and Manuel's affectionate view of ships."),
        35: ("Oh, dear. Have I overstepped? It's just my own way of looking at things. Forgive me if I offended you. I'll be on my way.", ("Have I overstepped?", "my own way", "I'll be on my way."), "Preserve his concern, the apology and his attempt to excuse himself."),
        46: ("Well... You seem awfully fond of ships. I just wondered why.", ("fond of ships.",), "Janus gently invites Manuel to talk about why he cares for ships."),
        50: ("Seeing a ship takes me back. I'm Manuel. Believe it or not, I used to be a navigator.", ("used to be a navigator.",), "Preserve the memories, the introduction and his past job. Carry the whole job title with the admission."),
        59: ("FI... You don't often meet someone who cares this much about ships. Imagine having him aboard...", ("having him aboard...",), "Janus quietly puts the case to Rafael. Preserve the original given-name substitution."),
        62: ("I agree. I'd feel better knowing someone like him was looking after the ship.", ("someone like him", "after the ship."), "Rafael expressly agrees and explains his relief about entrusting the ship to Manuel."),
        67: ("In that case... Manuel, would you join our crew? We'd like you to sail with us.", ("join our crew?", "sail with us."), "Janus makes a sincere offer to sail together. No new rank or relationship is assigned."),
        75: ("Does that mean you'll come with us?", ("come with us?",), "Rafael excitedly checks whether Manuel has accepted their invitation."),
        80: ("A ship's heartbeat stirs the soul... Pardon me. It's been ages since I've sailed. I got carried away.", ("A ship's heartbeat", "Pardon me.", "I got carried away."), "Keep the ship's heartbeat metaphor, then let Manuel catch himself and explain why he is excited."),
        87: ("Well, Admiral, shall I give you a few tips on refitting the rooms on your flagship?", ("a few tips", "on your flagship?"), "His immediate offer names refitting the flagship rooms and addresses the admiral courteously."),
        102: ("Very well. I'll explain which rooms are useful on a long voyage.", ("on a long voyage.",), "The lesson begins by narrowing the advice to rooms useful on a long voyage."),
        106: ("Put someone with high Speech in the First Mate's Office or the Chapel. That can ease the sailors' discontent.", ("high Speech", "First Mate's Office", "the sailors' discontent."), "Preserve the exact skill label, both locations and the effect on ordinary sailors."),
        110: ("The crew in the Galley and Nursery can help your fleet use less water and food.", ("Galley and Nursery", "water and food."), "Preserve both room labels and both kinds of supplies."),
        114: ("Put a Surgeon in the Sickbay. They can treat fatigue, illness, and injuries among your officers and sailors.", ("a Surgeon in the Sickbay.", "officers and sailors."), "Use the actual job and room labels. Keep all three ailments and both groups."),
        118: ("A sick or injured navigator will recover faster in the Cabin or Lounge.", ("sick or injured navigator", "the Cabin or Lounge."), "Keep the two conditions, the two assignments and the faster recovery."),
        122: ("At sea, shipwrights like me fix damage from the Lumber Room. At the shipyard, we help with refits and repairs.", ("shipwrights like me", "the Lumber Room.", "refits and repairs."), "Keep the two distinct workplaces and what a shipwright does in each."),
        125: ("I went through that rather quickly. Did it help?", (), "The question checks whether the rapid explanation was useful."),
        134: ("I see. Then I'll leave it in your hands.", ("leave it in your hands.",), "Manuel accepts the refusal and leaves the decision to Rafael. Keep the ordinary phrase on one line."),
    },
    180: {
        13: ("I've been bored out of my skull lately. You'd be doing me a favor.", ("doing me a favor.",), "The bored shipwright asks Rafael to help him pass the time, in a casual voice."),
        31: ("Come now. Don't sell us short.", (), "Janus pushes back politely when the player declines the lesson."),
        46: ("When it comes to ships, we're past needing lessons.", ("we're past needing lessons.",), "Retain Cesare's confident response and keep the assertion together."),
        69: ("Let's start with the difference between square sails and lateen sails.", ("square sails", "lateen sails."), "Restore that the shipwright will explain the difference between the two sails."),
        72: ("A square sail is rigged across the ship. That's why it's a transverse sail.", ("across the ship.", "a transverse sail."), "Name the established sail and explain the rig orientation in plain speech."),
        76: ("Square sails can't turn lengthwise. They do well downwind, but you can't get the best angle in a headwind.", ("turn lengthwise.", "do well downwind", "the best angle", "in a headwind."), "Keep the rig limitation and both wind cases on one panel so the headwind limitation stays complete."),
        79: ("Old hands call that triangular sail a lateen. It runs lengthwise, so you can't turn it crosswise like a square sail.", ("triangular sail", "it crosswise", "like a square sail."), "Preserve the joking distinction between people who know the term and those who don't, then the opposite orientation."),
        85: ("Next, let's look at the extra sails you can add.", ("the extra sails",), "Move naturally from the two basic rigs to the optional sails."),
        89: ("The proper name for the upper sail is topsail. It's a small square sail rigged high on each mast.", ("upper sail is topsail.", "a small square sail", "on each mast."), "Give its proper name and keep the rig and location together."),
        93: ("A staysail is a small fore-and-aft sail set ahead of each mast. You can't put it ahead of a lateen. They'd overlap.", ("a small fore-and-aft", "ahead of each mast.", "ahead of a lateen."), "Keep the installation position and the geometric reason lateen and staysail cannot share that spot."),
        99: ("A jigger spanker is a fore-and-aft stern sail. Fitting one is like adding a little mast, so it only fits on large ships.", ("A jigger spanker", "fore-and-aft stern sail.", "large ships."), "Preserve the optional stern rig, the small-mast comparison and the restriction to large ships."),
        102: ("Did you know a ship with two or more masts sails faster with the wind off its quarter than dead astern?", ("two or more masts", "off its quarter", "than dead astern?"), "Keep the condition and wind-angle comparison as one question, which Manuel answers two panels later."),
        113: ("Right. When the wind comes straight from behind, only the rearmost mast catches it. The forward masts don't do you any good.", ("only the rearmost mast", "The forward masts", "any good."), "Keep Manuel's answer and every part of the practical explanation in the shipwright's voice."),
        116: ("That's why you're fastest with the wind at an angle from behind. You still have to set the sails to match, of course.", ("at an angle from behind.", "to match, of course."), "Close the explanation with the correct wind angle and the continued need to trim the sails."),
    },
}

RETENTIONS = {
    179: {
        5: "Manuel opens by observing that the ship has been cared for.",
        8: "His suggestion that she could use work naturally leads into Rafael's concern.",
        11: "Rafael wonders whether the stranger has noticed something wrong with their ship.",
        20: "Manuel identifies the owners and praises the ship as full of life. This sets up Janus's aside.",
        30: "Rafael's silent reaction gives Manuel room to worry he has overstepped.",
        38: "Janus calls Manuel back with the original hesitation.",
        42: "Manuel gives Janus the opening to ask about his interest in ships.",
        54: "Rafael quietly acknowledges Manuel's experience before Janus makes the case.",
        71: "Manuel's wistful return to sea and his recognition of the young crew's passion retain their emotional progression.",
        84: "Manuel thanks them warmly and clearly accepts the offer.",
        93: "The courteous positive option answers Manuel's offer directly.",
        95: "The courteous refusal declines the advice without reversing the recruitment.",
        128: "His conclusion entrusts the fleet to the admiral and urges careful planning of refits.",
    },
    180: {
        5: "The shipwright directly invites the admiral to take the lesson. His informality establishes the voice.",
        8: "Rafael's brief response conveys surprise at being addressed out of nowhere.",
        19: "The polite acceptance clearly asks to hear the lesson.",
        21: "The polite refusal fits the original response and still makes the choice clear.",
        34: "Manuel quietly agrees with Janus after the player declines.",
        52: "The shipwright concedes their experience and jokes he'll wait for someone greener.",
        63: "The shipwright praises the interest behind the player's decision to listen.",
        66: "The short maxim leads naturally from the acceptance to how the sails work.",
        82: "The headwind and following-wind contrast answers the previous panel, and the whole check-in tag fits.",
        96: "The spritsail's name, direction, bow mounting and small-ship restriction are all intact.",
        106: "The shipwright turns the explanation into a question for Manuel.",
        110: "Manuel tentatively gives the exact reason: the masts line up fore and aft.",
        120: "Janus acknowledges the explanation with a brief, emphatic reply.",
        132: "Cesare admits he never gave it much thought and is excited to finally see why it works.",
        139: "The casual thanks and return to work close the exchange. A native reflow of this wording reproduced the existing breaks byte for byte.",
    },
}


def main():
    assert not OUTPUT.exists()
    packet, release, history = map(base.load, (SOURCE, parent.RELEASE, HISTORY))
    assert packet["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert packet["clean_sha256"] == release["clean_input_sha256"] == base.digest(native.CLEAN)
    rows = []
    for group in packet["groups"]:
        route, path, block = (group[key] for key in ("route", "file_path", "block"))
        historical = {r["source_reference"]["offset"]: r for r in history["records"] if r["block"] == block}
        assert not (REVISIONS[block].keys() & RETENTIONS[block].keys())
        assert REVISIONS[block].keys() | RETENTIONS[block].keys() == {r["source_record_index"] for r in group["records"]}
        for entry in group["records"]:
            index, selector = entry["source_record_index"], entry["selector"]
            prior = historical.pop(entry["source_offset"])
            assert prior["source_Japanese"] == entry["Japanese"] and prior.get("source_selector") == selector
            current = logical(entry["current_English"])
            edit = REVISIONS[block].get(index)
            english, phrases, note = edit or (current, (), RETENTIONS[block][index])
            assert TOKEN.findall(entry["Japanese"]) == TOKEN.findall(current) == TOKEN.findall(english)
            leading = "" if selector is None else f"{selector:02x}"
            refs = {side: dict(file_path=path, block=block, offset=entry[f"{side}_offset"],
                              command_offset=entry[f"{side}_command_offset"],
                              archive_sha256=group[f"{side}_archive_sha256"], block_sha256=group[f"{side}_block_sha256"],
                              exact_hex=leading + entry[f"{side}_body_hex"]) for side in ("source", "current")}
            rows.append(dict(id=prior["id"], file_path=path, route=route, block=block, source_record_index=index,
                native_command_word=entry["native_command_word"], native_slots=entry["slots"], source_selector=selector,
                kind="typed-choice-label" if selector is None else "progressive",
                source_reference=refs["source"], current_reference=refs["current"],
                source_hex=refs["source"]["exact_hex"], current_hex=refs["current"]["exact_hex"],
                Japanese=entry["Japanese"], previous_English=current, english=english,
                speaker=prior["speaker"], context=CONTEXT[block], source_meaning=prior["source_meaning"],
                localization_note=note, protected_phrases=list(phrases), review=dict.fromkeys(GATES, True) | {"formatting": not edit},
                decision="revision" if edit else "retention",
                finding="retention" if not edit else "wrap" if english == current else "prose and wrap"))
        assert not historical
    assert len(rows) == 62
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
        target_locale="en-US", review_gates=GATES, previous_sha256=release["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"], source_packet=str(SOURCE), source_packet_sha256=base.digest(SOURCE),
        records=rows, decisions=dict(Counter(row["decision"] for row in rows)),
        findings=dict(Counter(row["finding"] for row in rows)), new_editorial_credit=0,
        status="Contextual review complete. Revisions await native verification."))
    print(f"Reviewed {len(rows)} records in the complete refit and sail-rigging lessons.")


if __name__ == "__main__":
    main()
