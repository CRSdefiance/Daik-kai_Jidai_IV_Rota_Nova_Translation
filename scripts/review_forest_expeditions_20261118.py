"""Review all four forest expeditions against their paired native records."""

from collections import defaultdict
from pathlib import Path

from scripts import register_bounty_assignments_20261118 as parent


base, native = parent.base, parent.native
ROOT = Path("work/forest_expeditions_source_20261118")
INDEX = ROOT / "index.json"
MANUSCRIPT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/forest_expeditions_20261118_prose_v1.json")
INDEX_SHA = "7bec66e9501758708ee5446f073b17977cdaaf0f4ec5a7c3ca36d3adbdc59c9e"

NOTES = {
    1: "A conversational warning to the admiral sets up the map requirement.",
    2: "Keep the measured warning and the address to the admiral. The speaker expects the party to lose its way.",
    3: "The informal warning sounds more immediate than the formal version. Keep the thought tied to the absence of a map.",
    4: "The speaker warns in a rougher voice that the party will get itself lost without a map.",
    5: "The firm voice treats the map as necessary for keeping their bearings.",
    6: "The child voices a direct worry about getting lost and addresses the admiral.",
    7: "The older, formal voice makes the same warning in a measured register.",
    8: "The first observation describes the thick woods and suggests that the party travel carefully.",
    9: "The more formal speaker notes the density of the woods and urges caution.",
    10: "The speaker notices the darkness and feels uneasy. The feeling belongs to the speaker.",
    11: "The speaker comments on the thick growth and hopes the party will keep its bearings.",
    12: "The curt remark conveys unease without assigning it a cause.",
    13: "This speaker simply urges everyone to proceed carefully.",
    14: "The eager child hopes the expedition will turn up something interesting.",
    15: "Keep the older speaker's formality and open-ended worry that something might emerge.",
    16: "Rafael suggests proceeding carefully after the crew's opening remarks.",
    17: "The first alarm is hesitant and calls to the admiral before pointing behind the captain.",
    18: "The speaker urgently tells the admiral to stay still, then trails off.",
    19: "The speaker stammers before directing the admiral's attention behind them.",
    20: "The cry comes first. A stammer delays the warning about what is behind them.",
    21: "A caught breath or brief interjection leads into the warning to the admiral.",
    22: "The speaker reacts with surprise and stammers through the incomplete warning.",
    23: "Keep the unspoken startled reaction separate from the following spoken alarm.",
    24: "The brief warning cuts in after the silent reaction.",
    25: "The first option offers to stand and face the bear. The concise action wording works in the choice list.",
    26: "Play dead is the familiar idiom and sets up the joke about Emilio.",
    27: "The third option signals another set of choices and leaves their actions unspecified.",
    28: "Rafael gives a short order to fire at once.",
    29: "The speaker reacts as the bear takes off. The exclamation belongs to that moment.",
    30: "The relieved speaker says plainly that the bear has gone.",
    31: "The surprised speaker calls out the retreat. Keep that reaction distinct from the formal variants.",
    32: "Keep the older speaker's surprise at the retreat. The bear is already running off.",
    33: "The child celebrates after the bear leaves.",
    34: "The notice reports apparent minor injuries among the sailors. Preserve both the uncertainty and the severity.",
    35: "The speaker stammers and reports that the bear shows no sign of leaving.",
    36: "The formal speaker reports what the bear is doing and leaves its intentions open.",
    37: "The speaker is frustrated that the bear still has not moved.",
    38: "The anxious speaker hesitates and realizes that the bear still will not move.",
    39: "The rough speaker is frustrated by the bear's persistence. Keep the contempt in the address to the animal.",
    40: "The older speaker recognizes the predicament because the bear shows no sign of leaving.",
    41: "The child addresses the bear familiarly and imagines it going home. Preserve the tentative observation.",
    42: "The formal speaker sees no sign of movement. The scene still leaves the next action uncertain.",
    43: "Rafael asks for a little longer and hushes the group.",
    44: "The silent beat stays in its own panel before the next reaction.",
    45: "The pause and then finally mark the relief after waiting.",
    46: "The speaker briefly exhales, then realizes the bear has finally given up.",
    47: "The rough speaker exhales in relief and keeps a trace of irritation.",
    48: "The snore identifies the alternate outcome without a spoken explanation.",
    49: "The captain's quick question marks the discovery of Emilio.",
    50: "The sleeping sailor's light snore answers the question directly.",
    51: "Rafael contrasts Emilio pretending to be asleep with actually falling asleep.",
    52: "The system notice keeps the exact one-day passage of time.",
    53: "This menu action means attempting to frighten the bear away. The following failure remains possible.",
    54: "The second option urges immediate flight. Run for it conveys that urgency in the menu.",
    55: "The speaker reports an attempt to frighten the bear and its failure to run.",
    56: "The speaker trails off after noticing that the attempt still failed.",
    57: "The speaker reacts incredulously. The attempt to scare the bear has failed.",
    58: "The speaker marvels at the nerve of the bear and says the attempt to frighten it failed.",
    59: "The rough register makes the observation about the bear's nerve sound like grudging admiration.",
    60: "The older speaker exclaims over the failed intimidation and asks what is wrong with the bear.",
    61: "The child is puzzled because the attempt failed to make the bear run.",
    62: "The more formal speaker observes that the bear will not flee and remarks on its boldness.",
    63: "The warning leaves the animal's danger uncertain and says that mishandling it could put the crew at risk.",
    64: "The speaker calls to the admiral, reports an attack on the expedition party and says they need to flee. The source gives no count.",
    65: "The formal speaker reacts to the attack and urges immediate escape because the others are also in danger.",
    66: "The alarm turns into a decision to give up the attempt and run. The attack is already reported and the source gives no count.",
    67: "The attack is still happening. The speaker tells the admiral to leave.",
    68: "Keep the rough interjection and the question about whether some of the group were injured.",
    69: "The urgent address to the admiral calls for escape. Keep the older voice without stiff prose.",
    70: "The child's fear becomes an urgent request to run.",
    71: "The speaker recognizes the danger and tells the admiral that flight is the better course.",
    72: "The system message reports a considerable rise in fatigue and apparent injuries. Keep the separate outcomes.",
    73: "Rafael gives the immediate command to run.",
    74: "The relieved speaker says they somehow got away and pauses to catch their breath.",
    75: "The formal variant makes a separate pause before reporting the escape.",
    76: "Panting comes first, then the tentative realization that the party is safe.",
    77: "The speaker makes a tentative assessment after getting away.",
    78: "The brief relief still leaves the speaker asking whether they lost the bear.",
    79: "The child pants and says how frightened they were.",
    80: "The formal older speaker runs out of breath, takes stock of the others and expresses relief.",
    81: "The speaker announces two milestones to the admiral. The party is out of the forest and at the ruins.",
    82: "The speaker addresses the admiral and takes in the sight of the ruins after crossing the forest.",
    83: "The relief of getting through the woods is followed by a sudden, confident recognition of the ruins.",
    84: "The speaker says they are finally out and pauses before recognizing the ruins.",
    85: "The rough speaker greets the admiral with relief before recognizing the ruins.",
    86: "The older speaker celebrates getting through the forest and asks whether those are the ruins.",
    87: "The child celebrates getting out, notices the odd stones and wonders if they are the ruins.",
    88: "The older speaker announces the crossing to the admiral, then pauses to recognize the ruins.",
    89: "Rafael asks about the group they heard about before the chant begins.",
    90: "The drawn-out voice establishes the start of the chant.",
    91: "The next voice keeps its separate prolonged cry.",
    92: "The stammer and unease work as the listeners recognize that the voices might be singing.",
    93: "The repeated motion of the sun, moon and stars and the balance of light and darkness are intentional ritual imagery.",
    94: "The single puzzled reaction falls between the chant and the crew's own question.",
    95: "The rough question guesses that the words may be a spell without identifying what they are.",
    96: "Keep the society's established name, expectation of a revelation and ambition to rule the world.",
    97: "The speaker orders prayers to start again on the eve of the revelation and threatens a sacrifice.",
    98: "The congregation's response stays brief and separate from the crew's reactions.",
    99: "The shocked question repeats the society's goal.",
    100: "The other response reacts to the threatened sacrifice and the group's seriousness.",
    101: "The society leader gives a final order about the stones and formally ends the meeting.",
    102: "Rafael notes the group's departure before the crew suggests investigating.",
    103: "The suggestion to look follows the departure and keeps the conversation moving.",
    104: "Hodram's short decision to move retains his restraint and the beat before action.",
    105: "The order to fire is immediate and plain.",
    106: "Hodram asks for quiet and patience while they wait out the bear.",
    107: "Hodram realizes that the sailor really fell asleep.",
    108: "The command to run is abrupt and urgent.",
    109: "Lil leads the group onward directly.",
    110: "Lil's immediate command refers to the bear in front of them.",
    111: "Lil hushes the party and asks them to hold still in the waiting branch.",
    112: "Lil's surprise at Emilio's absence leads directly into the sleeping reveal.",
    113: "Lil contrasts the order to play dead with actually falling asleep and ends with disbelief.",
    114: "The captain calls for flight when the situation turns dangerous.",
    115: "Maria's measured question invites the party to continue.",
    116: "Maria asks the party to endure the wait for a little longer.",
    117: "Maria recognizes that Emilio is asleep after the snore.",
}

REVISIONS = {}


def revise(group, routes, text):
    for route in routes:
        assert (group, route) not in REVISIONS
        REVISIONS[group, route] = text


revise(4, (1,), "Admiral, we'll get ourselves lost without a map.")
revise(8, (1,), "These woods are thick. Let's be careful.")
revise(15, (0, 1, 2, 3), "A dense forest indeed. I hope nothing comes out...")
revise(17, (1,), "A-Admiral, behind you...")
revise(19, (1,), "A-Admiral... Behind you...")
revise(21, (1,), "Hm! Admiral, behind you...")
revise(22, (1,), "Whoa... B-behind you...")
revise(25, (1, 2, 3), "Stand and fight")
revise(27, (1, 2, 3), "Try something else")
revise(29, (3,), "Ah! It's running away!")
revise(31, (3,), "Oh! There it goes!")
revise(33, (1,), "Hooray! It's gone!")
revise(34, (2, 3), "Some sailors seem to have suffered minor injuries.")
revise(36, (1, 3), "Admiral... The bear shows no sign of leaving.")
revise(38, (1,), "A-Admiral... It's no use. This bear just won't move.")
revise(39, (1,), "A-Admiral... It's no use. That damn bear won't leave.")
revise(41, (0, 1), "A-Admiral... Mr. Bear doesn't look like he wants to go home.")
revise(42, (1, 3), "Hmm... That bear shows no sign of moving.")
revise(45, (1,), "Whew... It finally gave up.")
revise(46, (1,), "Whew... It's finally given up.")
revise(47, (1, 2, 3), "Whew... The damn thing finally gave up.")
revise(54, (1, 2, 3), "Run for it")
revise(56, (2, 3), "Even trying to scare it off didn't work...")
revise(57, (1,), "What's with this thing? We tried to scare it, but it won't run!")
revise(58, (1, 2, 3), "What nerve! We can't scare it off!")
revise(59, (1, 3), "This bear's got guts. It won't run!")
revise(60, (0, 1, 2), "Come now! It won't run, no matter how we try to scare it! What's the matter with it?")
revise(61, (1,), "Huh? We tried to scare it, but it won't go away!")
revise(62, (1,), "Even after all that, it won't flee... A bold creature indeed.")
revise(63, (3,), "Admiral, this is bad! It might be a man-eater! If we take it on, we're the ones in trouble!")
revise(64, (0, 1, 3), "Admiral, look out! Damn... It's attacked our crew! We have to run or we could get hurt too!")
revise(65, (0, 1, 3), "Look out! Oh no... The crew's been attacked! Let's get out of here! We're in danger too!")
revise(66, (0, 1, 2, 3), "Look out, Admiral! This is bad. It's attacked our crew! Forget it, let's run!")
revise(67, (1,), "Admiral, look out! It's attacking our crew! We'd better run!")
revise(69, (1, 3), "Look out! Admiral, we'd best run!")
revise(70, (2,), "It's dangerous! Come on, let's run!")
revise(76, (0, 1, 2), "Huff... Huff... Looks like we made it...")
revise(78, (3,), "Whew... Did we lose it?")
revise(79, (0, 1), "Huff... Huff... That was so scary...")
revise(80, (1,), "Oh, I'm out of breath... Everyone seems safe. Thank goodness.")
revise(81, (1,), "Admiral, we're out of the forest! We've reached the ruins.")
revise(82, (1,), "We're through the woods, Admiral. So these are the ruins...")
revise(83, (0, 1, 2, 3), "Out of the forest at last... Oh! Admiral, these are the ruins!")
revise(84, (1,), "We're finally out of the woods. So these are the ruins...")
revise(85, (0, 3), "Hey, Admiral! We're out of the woods! Yep, those are the ruins!")
revise(86, (3,), "Ah, we've made it out of the forest. Hmm... Are those the ruins?")
revise(87, (0, 1), "Yay! We're out of the forest! Um... Lots of funny stones over there. Are those the ruins?")
revise(88, (1,), "Admiral, we're through the forest. Oh... So these are the ruins...")
revise(101, (0,), "Until then, stay away from the great stones! That concludes today's meeting!")
revise(104, (1,), "Let's move.")


def read_groups():
    assert base.digest(INDEX) == INDEX_SHA
    index = base.load(INDEX)
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release["candidate_sha256"] == index["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    clean, current = [base.NdsImage.open(path) for path in (native.CLEAN, parent.ROM)]
    groups = defaultdict(list)
    for packet in index["route_packets"]:
        assert base.digest(packet["exact_packet"]) == packet["packet_sha256"]
        rows = base.load(packet["exact_packet"])["records"]
        file, block = packet["file_path"], packet["block"]
        original, stored = [native.IlnkContainer.parse(rom.read_file(file)).blocks[block] for rom in (clean, current)]
        assert native.digest(original) == packet["source_sha256"]
        assert native.digest(stored) == packet["current_sha256"]
        for row in rows:
            for blob, prefix in ((original, "source"), (stored, "current")):
                body = bytes.fromhex(row[prefix + "_hex"])
                start = row[prefix + "_reference"]["offset"]
                assert blob[start:start + len(body)] == body
            prefix_length = int("STYLE_" not in row["id"] and row["kind"] != "typed-choice-label")
            english = " ".join(bytes.fromhex(row["current_hex"])[prefix_length:].decode("cp932").split())
            assert row["english"] == english
            key = row["kind"], " ".join(row["Japanese"].split())
            groups[key].append(row | dict(route=packet["route"], block=block, file_path=file,
                earlier_ledger=packet["earlier_ledger"], earlier_ledger_sha256=packet["earlier_ledger_sha256"],
                source_block_sha256=packet["source_sha256"], current_block_sha256=packet["current_sha256"]))
    return release, groups


def compare():
    release, groups = read_groups()
    assert NOTES.keys() == set(range(1, len(groups) + 1))
    records, source_groups, used = [], [], set()
    for number, ((kind, meaning_key), owners) in enumerate(groups.items(), 1):
        note = NOTES[number]
        source_groups.append(dict(kind=kind, Japanese=meaning_key, context_note=note,
                                  records=[row["id"] for row in owners]))
        for row in owners:
            key = number, row["route"]
            prior = row["english"]
            if key in REVISIONS:
                used.add(key)
            english = REVISIONS.get(key, prior)
            decision = "revision" if english != prior else "retention"
            source_meaning = row["source_meaning"]
            context = row["context"]
            assert source_meaning and context
            records.append(row | dict(english=english, previous_English=prior, decision=decision,
                localization_note=note, review=dict(source=True, context=True, localization=True,
                                                   naturalness=True, formatting=False)))
    assert used == REVISIONS.keys() and len(records) == 370
    assert len({(r["file_path"], r["id"]) for r in records}) == len(records)
    return dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
        previous_profile=release["profile"], previous_sha256=release["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"], source_index_sha256=INDEX_SHA,
        clean_input_sha256=release["clean_input_sha256"], source_groups=source_groups, records=records,
        retrospective_review=True, formatting_and_registration_pending=True, additional_review_credit=0)


if __name__ == "__main__":
    draft = compare()
    assert not MANUSCRIPT.exists()
    base.save(MANUSCRIPT, draft)
    revisions = sum(row["decision"] == "revision" for row in draft["records"])
    print(f"{len(draft['records'])} records, {revisions} wording proposals, {len(draft['records']) - revisions} retentions")
