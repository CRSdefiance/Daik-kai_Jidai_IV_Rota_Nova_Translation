"""Record the contextual revisit of Cesare's three remaining Alexandria scenes."""
from collections import Counter
from pathlib import Path

from scripts import register_hodram_alexandria_tutorial_20261121 as parent
from scripts.review_hodram_alexandria_tutorial_20261121 import GATES, TOKEN, logical


base, native = parent.base, parent.native
ROOT = Path("work/parallel_ship_lessons_20261121")
SOURCE, BINDING = ROOT / "paired_source.json", ROOT / "current_candidate_binding.json"
OUTPUT = ROOT / "contextual_review_v1.json"
BLOCKS = ((177,), (), (164,), (135,))
PRIOR = {
    0: "rafael_B177_B180_integrated_final_review_v1.json",
    2: "lil_B164_editorial_manuscript_v10.json",
    3: "maria_B125_B136_final_review_v1.json",
}
CONTEXT = {
    0: "Cesare recognizes his lost Elysion. Janus draws him into a conversation about her fittings, unlocking extra armor. Rafael is left wondering if Cesare has just joined them. Cesare then offers optional ship-buying advice.",
    2: "Cesare mistakes Lil's figure of speech for a belief that the Earth has an edge. Camille sees a use for Cesare's travels and invites him aboard. Lil reluctantly agrees, and Cesare offers optional ship-buying advice.",
    3: "Maria and her companions rescue Cesare from men he offended by correcting them about the shape of the Earth. Maria values his curiosity and ship knowledge and hires him as navigator. The script continues into his ship-buying advice without a text choice in this block.",
}

# A line can need a wording revision, a wrap-only revision (None), or retention.
# Keep the two forms of Cesare's geography joke recognizably related.
REVISIONS = {
    0: {
        9: ("It's a busy port.", "Rafael is reacting to a thriving port, in his easygoing opening voice."),
        27: ("Th-this ship! There's no mistaking her!", "Keep Cesare's stammer and the certainty of his recognition."),
        30: ("She's changed here and there, but I'd know her anywhere. Oh, my beloved Elysion!", "He recognizes traces of the ship underneath her alterations and addresses her affectionately."),
        34: ("Huh? You can recognize a ship by her looks?", "Janus reacts to Cesare describing the ship as though she were a person."),
        37: ("Excuse me. What is it about our ship?", "Rafael politely asks why this stranger has stopped them."),
        43: ("Forgive me. I'm Cesare Tony. This ship used to be mine.", "Move naturally from his apology and introduction to his former ownership."),
        55: ("I heard she'd been abandoned, so I searched for her day and night! I knew I'd see her again someday.", "Preserve the rumor, his constant search and his confidence that they'd meet again."),
        65: ("So you're her former owner... Wait! I've got so many questions for you!", "Janus latches onto the practical opportunity, leaving Rafael out of the decision."),
        68: ("I've been trying to figure her out. Are there fittings on this ship that aren't in any of my books?", "Janus is baffled by undocumented mechanisms and asks Cesare directly."),
        76: ("Oh, I wouldn't go that far... Here, come with me! I have so much to ask you!", "Preserve Janus's quick modesty followed by his eagerness to get answers."),
        90: ("Take this spot, for instance. It looks a little odd. Is there a mechanism here too?", "The odd spot is the first concrete example and sets up the hidden armor mount."),
        94: ("Ah, you noticed that too? What you have there is...", "Cesare is impressed and delays the reveal just long enough for his demonstration."),
        100: ("You take this little bump and give it a push. Just like that!", "Make his playful demonstration audible without claiming that the game makes a click."),
        108: ("Then what? Whoa!", "Janus finishes his question just as he sees the mechanism work."),
        117: ("Th-that's amazing! Could we do that to other ships too?", "Keep the stammer and Janus's question about applying the same refit elsewhere."),
        125: ("That's incredible! Come on, let's look farther inside...", "Janus presses on with the tour while Rafael is left to call after him."),
        139: ("He went and decided all that himself. So... does this mean Cesare's joining us?", "Rafael's rueful uncertainty lands as the scene's joke. Janus has acted ahead of him."),
        144: ("Oh, Admiral. May I offer some advice on choosing ships?", "A courteous change of subject and a clear optional tutorial offer."),
        150: ("Listen", "The Japanese caption names the action taken, matching the equivalent Hodram choice."),
        152: ("Skip", "The player declines the advice while the recruitment itself proceeds."),
        162: ("I see! I underestimated you. You have your own way of doing things. I admire that!", "Retain Cesare's sincere, slightly overdone praise for the player's independence."),
        166: ("I'll get ready to sail, then. Until later!", "Close the declined lesson courteously and keep his next action."),
    },
    2: {
        5: ("So this is Alexandria. It's a pretty big city.", "Lil takes in the place with casual surprise."),
        8: ("Africa's so big, I bet it has lots of cities like this.", "Camille speculates in response to Lil's impression of Alexandria."),
        15: ("I'll be blunt. You're wrong!", "Cesare barges in with his emphatic correction. Match his report of the same opening in Maria's route."),
        25: ("You're wrong because you're wrong! The Earth doesn't have an edge. It's round! Everybody knows that by now!", "Preserve Cesare's pedantic circular retort and the connection to Lil's figure of speech."),
        31: ("I... was only correcting a mistake.", "Cesare answers as if the merits of the correction settle the question of his interruption."),
        42: ("Indeed. I've traveled the world and acquired a wealth of knowledge.", "Cesare answers Camille with pride and a slightly formal cadence."),
        46: ("Wow. You really like to learn, huh?", "Camille is impressed by Cesare's curiosity. The tone is friendly and disarming."),
        54: ("He just picked a bad moment. Besides, wouldn't it help to have someone who's seen so much of the world?", "Camille defuses the quarrel and connects Cesare's firsthand experience to their needs."),
        66: ("What?", "Cesare's surprise follows Camille's unexpected invitation. Use the single question mark elsewhere in the exchange."),
        77: ("Oh, splendid! You're an admiral? Please let me sail with you!", "Cesare's enthusiasm rises as he realizes who can take him aboard."),
        80: ("Camille! What am I supposed to do with him?", "Lil appeals to Camille after he puts her on the spot."),
        83: ("If he's sailed around the world, he has experience at sea. He could probably help out aboard, don't you think?", "Camille gives his practical reason and invites Lil to agree."),
        89: ("Ugh, this sounds exhausting already. All right. You're hired.", "Lil gives in without losing her reluctance or dry humor."),
        92: ("Many thanks! I'm Cesare Tony.", "Keep his gratitude and introduction in a brisk formal register."),
        103: ("Oh, Admiral. May I offer some advice on choosing ships?", "Once he is aboard, Cesare courteously offers the optional lesson."),
        109: ("Listen", "Match the action named by the Japanese caption and by Hodram's and Rafael's menus."),
        111: ("Skip", "Labels declining the advice. Recruitment still proceeds."),
        121: ("I see! I underestimated you. You have your own way of doing things. I admire that!", "Preserve the same generous reaction and exaggerated formality as his response on Rafael's route."),
        125: ("I'll get ready to sail, then. Until later!", "Close the declined lesson courteously and keep his next action."),
    },
    3: {
        4: ("Hey, you!", "The sailor's shout interrupts the scene and signals that someone is being accosted."),
        35: ("He doesn't look like he can defend himself. Shall we help?", "Xien sizes up the victim and suggests intervening."),
        51: ("Picking on the weak? Unforgivable! I'll come with you!", "Keep Yukihisa's indignation and willingness to help."),
        72: ("Ow... I can't say I am.", "Cesare directly answers whether he's all right. Let the dry understatement carry the joke."),
        76: ("Why were those men after you?", "Maria asks about the incident with the men they just stopped."),
        111: ("The Earth is round! Everybody knows that by now! I thought I'd set them straight.", "Preserve Cesare's certainty and his belief that correcting them was helpful."),
        118: ("I started explaining. Then, all of a sudden, they began acting very strangely.", "Cesare understates the reaction before describing the blows."),
        122: ("They glared at me. One said, \"Who asked you?\" Then they came at me swinging...", "Progress from the hostile look to the rebuke and the assault."),
        133: ("All I said was, \"I'll be blunt. You're wrong!\" And then...", "Recreate the tactless opening from Lil's scene and let the others infer what happened."),
        137: ("And that's when they got angry.", "Maria supplies the obvious next step before Cesare can."),
        144: ("Anyone could have guessed.", "Xien's dry aside answers Cesare's amazement in an idiomatic voice."),
        151: ("They were wrong! I set them straight! Shouldn't they be thanking me?", "Keep the comic reversal from the attack to Cesare's expectation of thanks."),
        154: ("I'd thank anyone who corrected me! I'd have learned one more truth about the world!", "Show Cesare's sincere enthusiasm for learning, even when corrected."),
        166: ("Hmm. Every country has its eccentrics, too.", "Echo Yukihisa's earlier remark about villains with a dry reversal."),
        184: (None, "Cesare's past command and refitting hobby answer Maria clearly. Keep both facts and reflow the second sentence."),
        195: ("Him? A captain? I can hardly believe it.", "Keep Yukihisa's disbelief close on the heels of Cesare's proud answer."),
        216: ("Admiral, you're not thinking of taking him aboard, are you?", "Richard asks with concern. Keep the tag with its question where the native layout allows."),
        222: ("FI, you don't mean to take him aboard, do you?", "Xien addresses Maria by the original given-name substitution. His wording remains distinct from Richard's."),
        229: ("Yes. I like his curiosity. Besides, with that personality, I doubt he has an easy time fitting in.", "Maria admires his inquisitiveness and sees how hard it would be for him to fit into ordinary life."),
        255: ("Honestly... The admiral has a soft spot for the strangest people.", "Richard recognizes Maria's kindness toward an unlikely recruit."),
        260: (None, "Retain Xien's parallel reaction and reflow the phrase without an isolated ending."),
        270: ("Oh, forgive us. We've been talking around you. What is it?", "Maria turns back to Cesare after his hesitant interruption."),
        280: ("Then you must be Admiral FI FA?", "The two original name substitutions carry Cesare's recognition."),
        284: ("You've heard of me? That makes things easier. Want to join us as a navigator?", "Maria makes the offer herself and preserves the actual shipboard role."),
        288: ("Yes! I'd be delighted! Please let me sail with you!", "Cesare eagerly accepts the offer and repeats his desire to go aboard."),
        294: ("Cesare Tony! Thank you ever so much!", "Keep his name and his exuberant gratitude."),
        297: ("Hmm. What does the admiral see in him? I can't figure it out...", "Xien still cannot fathom Maria's choice after the introduction."),
    },
}

# The clean lesson keeps the same sequence and facts across all three versions.
# Recheck each route's Japanese before reusing the teaching voice.
LESSON = (
    ((180, 140, 325), "You don't need more ships just to sign deals with new towns and open trade routes. With a one percent share, you can buy only one to five units of trade goods.", "Separate the two complete thoughts at a page boundary. Keep the exact share and purchase range."),
    ((183, 143, 328), "Once your market share grows and you can buy more goods, it's time to buy a ship.", "Make the threshold depend on market share and access to more goods."),
    ((187, 147, 332), "Start with the ship's size and price.", "Cesare introduces both purchasing factors before giving the trade-off."),
    ((190, 150, 335), "Buy a ship your market share and budget can support. Otherwise you'll need more sailors for a ship you can't fill.", "Keep both limiting factors and the mismatch between crew and cargo. Give the consequence as one thought."),
    ((193, 153, 338), "Price gives you an idea of size. Under 5,000 is small, 10,000 to 20,000 is medium, and over 50,000 is large.", "Keep the source's exact examples and their strict inequalities."),
    ((196, 156, 341), "Small ships are cheap. Even when funds are tight, they let you add cargo space to your fleet.", "Keep the low-budget advantage and the exact kind of capacity gained."),
    ((199, 159, 344), "Once you've traded for a while and have money to spare, trade up to a medium ship.", "Keep the proceeds from trading as the reason for upgrading."),
    ((203, 163, 348), "Medium ships have two or three masts. The ones with three are faster, but they need more sail handlers.", "Keep both mast counts, the speed trade-off and the required crew role."),
    ((206, 166, 351), "Refit for up to five cargo holds. If you won't fight for a while, skip marine quarters and gun batteries.", "Preserve the refit ceiling and make the peace-time exception concrete."),
    ((209, 169, 354), "To open a route to a distant town, add more supply holds. That lets you sail much farther.", "Keep the benefit to long voyages, and the established supply-hold term."),
    ((212, 173, 357), "If you take on another faction, you'll need large ships.", "Shift the advice from trade to fighting another faction."),
    ((215, 177, 360), "Equip at least your flagship with marine quarters and gun batteries. It'll be hard to win at sea without them.", "Keep the minimum flagship recommendation and the hard-fought naval victories."),
    ((218, 180, 363), "Consider what you can afford. Two medium ships cost less and carry more trade goods than one large ship.", "Keep both advantages for the same two-to-one comparison."),
    ((221, 183, 366), "You'll move up to large ships. Planning to form regional fleets? You could keep your medium ships.", "All three sources give the option of keeping old medium ships for regional fleets."),
    ((224, 186, 369), "That's all my advice. I'll get ready to sail. Until later!", "Close in Cesare's courteous voice, preserving his immediate plans."),
)
PHRASES = (
    ("just to sign deals", "With a one percent share,", "one to five units"),
    ("your market share grows", "buy more goods", "time to buy a ship."),
    ("size and price.",),
    ("your market share", "Otherwise you'll need more sailors", "a ship you can't fill."),
    ("Under 5,000", "10,000 to 20,000", "over 50,000"),
    ("Even when funds are tight,", "cargo space"),
    ("money to spare", "to a medium ship."),
    ("two or three masts.", "more sail handlers."),
    ("up to five cargo holds.", "If you won't fight for a while,", "marine quarters", "gun batteries."),
    ("a distant town,", "add more supply holds."),
    ("another faction", "large ships."),
    ("at least your flagship", "marine quarters", "gun batteries."),
    ("Two medium ships", "more trade goods", "one large ship."),
    ("move up to large ships.", "Planning to form regional fleets?", "keep your medium ships."),
    ("That's all my advice.", "I'll get ready to sail."),
)

RETENTIONS = {
    0: {
        5: "Janus's quiet recognition sets up Rafael's impression of the port.",
        15: "Janus is the first to notice the man approaching, beginning the encounter.",
        18: "Cesare's incomplete recognition gives Rafael room to ask what is wrong.",
        22: "Rafael's brief question keeps the attention on Cesare and the ship.",
        47: "Cesare distinguishes surviving the pirates from losing his ship.",
        51: "The beloved ship and Cesare's theatrical grief stay explicit.",
        58: "He makes clear that his ownership claim is past and asks for no return.",
        61: "His only request is permission to sail with the Elysion once more.",
        72: "Cesare recognizes the nautical knowledge behind Janus's question.",
        80: "Cesare warmly agrees to answer Janus's questions.",
        83: "The delayed introduction lands naturally after their mutual enthusiasm.",
        86: "The full name and the polite response fit Cesare's formal voice.",
        97: "The armor mount is a concrete and accurate reveal.",
        104: "Cesare suspends the sentence as he demonstrates the fitting.",
        114: "The concise system panel names the unlocked refit without changing its modal role.",
        121: "His emphatic confirmation is a brisk response to Janus.",
        129: "Rafael calls after Janus directly as the others move away.",
        134: "The understated observation gives Rafael's next line its timing.",
        176: "The short lead-in lets Cesare gather his thoughts.",
    },
    2: {
        11: "The image of land stretching to the end of the world sets up Cesare's literal objection.",
        18: "Camille is startled by the sudden interruption.",
        22: "Lil challenges the stranger's apparent attempt to pick a fight.",
        28: "Lil concedes the fact and asks whether he heard what she was actually saying.",
        34: "Lil's exasperated aside closes the argument before Camille changes tack.",
        38: "Camille turns Cesare's pedantry into a question about knowledge.",
        50: "Lil is still offended and rejects Camille's first sign of admiration.",
        58: "Lil realizes in mid-thought that Camille wants to recruit him.",
        62: "Camille extends the invitation directly.",
        70: "Lil's first remark confirms her suspicion and the second tries to interrupt.",
        74: "Camille identifies their occupation and Lil's real rank.",
        86: "Cesare's short petition uses the rank Camille just introduced.",
        95: "Camille welcomes him warmly and offers a tour of the ship.",
        98: "Lil's dry verdict carries the joke through to the tutorial offer.",
        136: "Cesare clears his throat before addressing the player.",
    },
    3: {
        8: "Cesare's distress and plea convey the danger before the party sees him.",
        18: "Richard reacts in surprise to the cry.",
        24: "Xien's question leads directly into Maria's report.",
        31: "Maria directs their attention to the man being beaten.",
        39: "The brief reply gives Maria's immediate assent to help.",
        68: "Xien checks on the injured man and naturally uses the source's age-relative address.",
        88: "Yukihisa suspects the attackers started the quarrel, setting up his later comment about eccentrics.",
        95: "Cesare hesitates before explaining the flat-Earth argument.",
        99: "Maria's question mark preserves the reaction pause.",
        104: "Cesare lays out the men's original claim plainly.",
        107: "Xien's curt prompt lets Cesare proceed with his explanation.",
        114: "Maria prompts him to get to what happened next.",
        126: "Xien still wants to know how a discussion turned into an assault.",
        129: "Cesare sincerely admits he doesn't understand either.",
        141: "Cesare's stammer preserves his comic astonishment at Maria's deduction.",
        148: "Cesare remains puzzled after everyone else guesses the motive.",
        172: "Xien gives limited credit for curiosity, leaving his concern unspoken.",
        176: "Maria's pause gives her practical change of subject room to register.",
        180: "Maria asks directly about his knowledge of ships.",
        202: "Maria judges him qualified before anyone else realizes what she has in mind.",
        205: "The punctuation conveys that Cesare is still waiting to understand her conclusion.",
        241: "Yukihisa agrees without softening Maria's blunt assessment.",
        266: "Cesare's hesitation politely reenters the crew's conversation.",
        273: "Cesare asks directly about Maria's rank.",
        276: "Xien confirms the rank and retains the original faction substitution.",
        291: "Maria closes the agreement briskly and asks for his name.",
        309: "Yukihisa's terse verdict closes the party's reaction.",
        321: "Cesare's short lead-in marks the start of the lesson.",
    },
}


def main():
    assert not OUTPUT.exists()
    packet, binding, release = map(base.load, (SOURCE, BINDING, parent.RELEASE))
    assert binding["packet_sha256"] == base.digest(SOURCE)
    assert binding["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert packet["clean_sha256"] == release["clean_input_sha256"] == base.digest(native.CLEAN)
    rows = []
    for offset, group in enumerate(packet["groups"]):
        route, path, block = (group[key] for key in ("route", "file_path", "block"))
        verified = binding["routes"][offset]
        assert verified["path"] == path and verified["block"] == block and verified["records"] == len(group["records"])
        old_path = Path("translations") / PRIOR[route]
        old_rows = {r["source_reference"]["offset"]: r for r in base.load(old_path)["records"] if r["block"] == block}
        advice = {indices[offset]: (english, note, phrases)
                  for (indices, english, note), phrases in zip(LESSON, PHRASES, strict=True)}
        decisions = REVISIONS[route].keys() | RETENTIONS[route].keys() | advice.keys()
        assert len(decisions) == len(REVISIONS[route]) + len(RETENTIONS[route]) + len(advice) == len(group["records"])
        for entry in group["records"]:
            index, selector = entry["source_record_index"], entry["selector"]
            prior = old_rows.pop(entry["source_offset"], None)
            if prior is None:
                assert route == 2 and selector is None and index in (109, 111)
                prior = dict(id=f"DK4_MES_B{block}_R{index:04}", source_Japanese=entry["Japanese"],
                    source_selector=None, speaker="Player choice",
                    source_meaning="Choose to hear Cesare's advice" if index == 109 else "Decline Cesare's advice")
            assert prior["source_Japanese"] == entry["Japanese"] and prior.get("source_selector") == selector
            current = logical(entry["current_English"])
            if index in advice:
                replacement, reason, phrases = advice[index]
            else:
                replacement, reason = REVISIONS[route].get(index, (None, RETENTIONS[route].get(index)))
                phrases = ()
            assert reason
            revise = index not in RETENTIONS[route]
            english = replacement or current
            assert TOKEN.findall(entry["Japanese"]) == TOKEN.findall(current) == TOKEN.findall(english)
            leading = "" if selector is None else f"{selector:02x}"
            refs = {side: dict(file_path=path, block=block, offset=entry[f"{side}_offset"],
                              command_offset=entry[f"{side}_command_offset"],
                              archive_sha256=group[f"{side}_archive_sha256"], block_sha256=group[f"{side}_block_sha256"],
                              exact_hex=leading + entry[f"{side}_body_hex"]) for side in ("source", "current")}
            finding = ("retention" if not revise else "choice caption" if selector is None else
                       "wrap" if english == current else "prose and wrap")
            rows.append(dict(id=prior["id"], file_path=path, route=route, block=block, source_record_index=index,
                native_command_word=entry["native_command_word"], native_slots=entry["slots"], source_selector=selector,
                kind="typed-choice-label" if selector is None else "FE" if selector == 0xFE else "progressive",
                source_reference=refs["source"], current_reference=refs["current"],
                source_hex=refs["source"]["exact_hex"], current_hex=refs["current"]["exact_hex"],
                Japanese=entry["Japanese"], previous_English=current, english=english, speaker=prior["speaker"],
                context=CONTEXT[route], source_meaning=prior["source_meaning"], localization_note=reason,
                historical_context_reference=str(old_path) if selector is not None else None,
                protected_phrases=list(phrases), review=dict.fromkeys(GATES, True) | {"formatting": not revise},
                decision="revision" if revise else "retention", finding=finding))
        assert not old_rows
    assert len(rows) == 175
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
        target_locale="en-US", review_gates=GATES, previous_sha256=release["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"], source_packet=str(SOURCE), source_packet_sha256=base.digest(SOURCE),
        current_candidate_binding=str(BINDING), current_candidate_binding_sha256=base.digest(BINDING),
        records=rows, decisions=dict(Counter(row["decision"] for row in rows)),
        findings=dict(Counter(row["finding"] for row in rows)), new_editorial_credit=0,
        status="Contextual review complete. Revisions await native verification."))
    print(f"Reviewed {len(rows)} records across three complete exchanges.")


if __name__ == "__main__":
    main()
