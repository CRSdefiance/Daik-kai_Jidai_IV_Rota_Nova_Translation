"""Review the full jungle and cave decision trees in their four narrative contexts."""

from collections import defaultdict
from pathlib import Path

from scripts import prepare_jungle_caves_20261118 as current
from scripts import review_london_guild_assignments_20261118 as binder


base, parent = current.paired.base, current.parent
SOURCE = current.ROOT / "paired_source.json"
SOURCE_SHA = "4657e1210c9af213a9629cb56a1be7a69e03e4d2acb5f27ff112d46bb646f520"
OUTPUT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/jungle_caves_20261118_prose_v3.json")
HISTORY = ("rafael_B301_B320_integrated_final_review_v1.json", binder.HISTORY[1],
           binder.HISTORY[2], binder.HISTORY[3])

# Order follows the first occurrence of each original Japanese body and native
# word in the hash-bound four-route packet. Variants remain separate records.
NOTES = (
    "A straightforward warning against wandering aimlessly through the jungle. Keep the direct address to the admiral.",
    "The speaker warns about losing direction in a jungle like this. Keep the polite, measured warning.",
    "A familiar voice stresses how risky it is to wander without a plan.",
    "The speaker expects the party to get lost without a map. Keep the practical condition.",
    "The rough warning calls anyone who wanders blindly through here reckless.",
    "The older speaker cautions against wandering through the jungle without knowing the way.",
    "The child dreads entering the jungle without a map. Keep the plea and the childlike address.",
    "The formal companion warns of the danger of wandering without a clear route.",
    "Rafael spontaneously says the jungle makes him uneasy.",
    "Claudio agrees and presses the party to keep moving.",
    "Rafael notices the cave with a short, uncertain pause.",
    "Claudio asks whether they should go in. Keep his casual question.",
    "Rafael agrees reluctantly because turning back also sounds unpleasant.",
    "Claudio treats the decision as settled and immediately urges them on.",
    "The cave confirms the earlier unease. Keep the short spoken reaction.",
    "Rafael agrees and wants to get through quickly.",
    "The companion asks the others to slow down because the dark makes footing uncertain.",
    "The growl interrupts the conversation without naming the animal.",
    "Something is present, and the companion has a bad feeling.",
    "The formal companion's apprehension sounds ominous. No literal omen is identified.",
    "The speaker hesitates before admitting there is something in the cave.",
    "The speaker seeks confirmation and voices unease. Keep the full question tag.",
    "The rough voice is sure something is there and dislikes what that means.",
    "The older voice senses something and feels uneasy without estimating their chances.",
    "The child looks for agreement and admits that the presence scares him.",
    "The party's sudden reaction includes the original stammer at the creature's appearance.",
    "The first native choice calls for an attack. Keep the short command.",
    "The second native choice calls for retreat. Keep the immediate one-word command.",
    "Rafael urgently calls for someone to shoot.",
    "The short roar follows the order to shoot. It remains a sound rather than a speech.",
    "The cry marks a hit or sudden distress. It doesn't identify a wound.",
    "Claudio swears when the animal proves quick.",
    "The first forceful objection warns of a high risk of hitting the crew in the cramped cave.",
    "The second objection trails off on the danger of hitting one's own side.",
    "A familiar objection makes the cramped space and accidental injury explicit.",
    "The speaker urgently tells the others to hold their fire because they could hit each other.",
    "The rough voice is emphatic about the danger to the crew.",
    "The older companion judges it impossible to fire safely in such a tight place.",
    "The alarmed child addresses the admiral and fears someone on their side could be shot.",
    "The formal companion objects emphatically to the high risk of friendly fire.",
    "Rafael recognizes that they are only adding casualties and explicitly tells the crew to use swords.",
    "Keep the exertion audible before the relieved report that they managed to defeat it.",
    "This restrained version simply says they managed to defeat it.",
    "This panting voice is still uncertain that they have brought it down.",
    "This exhausted speaker thinks they have defeated it. Keep the qualified relief.",
    "The rough voice announces the victory tersely.",
    "The older voice pants and expresses emphatic relief after finally defeating the animal.",
    "The child celebrates and exclaims about how strong the tiger was.",
    "The formal voice pants before affirming that they have managed to defeat it.",
    "The system reports that quite a few members of the crew appear injured.",
    "The companion thinks the animal wasn't hungry and observes that it isn't following.",
    "This speaker cautiously interprets the animal's behavior. The absence of pursuit is immediate, with no promise about what it will do.",
    "The familiar voice infers it wasn't hungry because it isn't chasing them.",
    "The speaker conjectures that the tiger wasn't hungry and is relieved to have escaped pursuit.",
    "The rough companion infers it wasn't hungry and is relieved they escaped.",
    "The older speaker calls it a tiger and draws the same inference from the lack of pursuit.",
    "The child calls it a tiger and points out that it isn't chasing them.",
    "The formal companion qualifies the inference and notes they are clear of pursuit.",
    "A short exclamation releases the tension after escaping.",
    "Rafael spots light and realizes they can get out of the cave.",
    "Hodram finds the jungle unsettling. Keep his restrained delivery.",
    "The companion agrees and hopes that nothing happens.",
    "Hodram notices the cave with a short pause.",
    "The companion considers the cave deep but believes it is their only way to continue.",
    "The more hopeful companion thinks the cave could be a shortcut to the destination.",
    "Hodram briefly considers the suggestion before continuing.",
    "The companion addresses Hodram by his first-name control and politely warns about slippery moss.",
    "Hodram acknowledges the warning with a quiet pause.",
    "Hodram's order to shoot is short and forceful.",
    "Hodram's frustration is brief after seeing the animal dodge.",
    "Hodram realizes more people will be hurt and orders a switch to close combat.",
    "A small reaction gives way to Hodram's observation of light.",
    "The companion recognizes the light as their route out.",
    "Lil complains about snakes and bugs and floats the idea of staying in town.",
    "The first reply says having the admiral with them affects morale.",
    "This companion reacts to Lil's suggestion with disbelief.",
    "The familiar voice asks who would lead them without Lil.",
    "The speaker objects because the party would have no one to lead it.",
    "The rough companion reacts bluntly to the suggestion of staying behind.",
    "The older voice predicts a drop in morale if Lil stays behind.",
    "The child pleads with Lil to come along.",
    "The formal companion is incredulous at the idea of a party without its admiral.",
    "The companion addresses Lil by her first-name control and insists she must come as admiral.",
    "Lil agrees in exasperation and repeats the point to show she already understands.",
    "The companion reins in the argument and reassures her that she can just come along.",
    "Lil reacts to the darkness by abruptly proposing they go back.",
    "A companion rejects turning back because there is no alternative to entering.",
    "The second companion refuses plainly and urges them to keep going.",
    "The familiar voice treats the suggestion as a joke and wants to get inside promptly.",
    "This reply also treats it as a joke, with a direct address to Lil as admiral.",
    "The rough companion says it is too late to back out and tells the party to move.",
    "The older voice bluntly dismisses the idea of turning back.",
    "The child admits being scared and still asks Lil to go in together.",
    "The formal companion gently objects and tentatively proposes entering.",
    "The flustered companion wants Lil to say 'Let's go' as expected.",
    "Lil's stammer makes her agreement reluctant.",
    "The companion asks Lil directly whether she is afraid of caves. Keep the name control.",
    "Lil stammers through her denial and calls on Camille to go.",
    "Lil is still distressed by the dark once inside.",
    "Mikhail treats the darkness as an opportunity. Keep his exaggerated excitement.",
    "Mikhail hums and calls to the captain in a singsong voice. Keep the runtime name and the teasing familiarity.",
    "Mikhail's pleased response sets up the interruption.",
    "The other speaker interrupts hesitantly and leaves the object of 'my' unsaid. Keep the ambiguity.",
    "Mikhail realizes his mistake and gives a brief, awkward apology.",
    "Lil screams and urgently asks someone to shoot.",
    "Lil is taken aback by the animal's speed.",
    "Lil sees that people keep getting hurt and proposes fighting with swords instead.",
    "Lil's fear gives way to open relief when she sees a ray of light.",
    "Maria remarks on both the humidity and the oppressive, muggy air.",
    "The older companion attributes the conditions to the jungle, warns about wild animals, and urges caution choosing the path.",
    "Maria notes that the cave looks deep and lets the thought trail off.",
    "The older companion concludes they need to go through the cave.",
    "Maria agrees and tells the party to proceed.",
    "Maria issues the short order to shoot after the creature appears.",
    "Maria responds with frustration when the animal moves too fast.",
    "Maria sees that casualties are mounting and proposes switching to close combat.",
    "The companion addresses Maria by her first-name control and calls attention to light.",
    "Maria recognizes that they can finally get out of the cave.",
)

EDITS = {}


def revise(index, routes, english):
    for route in routes:
        assert (index, route) not in EDITS
        EDITS[index, route] = english


revise(2, (2,), "Admiral, it's dangerous to wander aimlessly through a jungle like this.")
revise(3, (0, 2), "Admiral, we can't just wander through a jungle like this! It's too dangerous!")
revise(7, (1, 2), "Admiral, I don't wanna go in there without a map!")
revise(8, (0, 2), "Admiral, we'd be taking a risk to wander through a jungle like this without a clear route.")
revise(13, (0,), "I suppose so. I don't want to go back the way we came...")
revise(20, (1, 3), "...Something's in here. This doesn't bode well...")
revise(22, (1, 2, 3), "There's something in here, isn't there? I've got a bad feeling...")
revise(23, (3,), "Something's in here, all right. I don't like this one bit...")
revise(24, (0, 1), "...There's something in here with us. I've got a bad feeling...")
revise(25, (1, 2), "There's... there's something here, right? I've got a bad feeling...")
revise(26, (1,), "Th-there it is!")
revise(33, (3,), "Don't shoot! In a space this tight, we're far too likely to hit one of our own!")
revise(34, (3,), "No! It's so cramped in here, we could shoot one of our own...!")
revise(35, (3,), "Don't! In a space this tight, we might shoot one of our own!")
revise(36, (1, 3), "No, don't shoot! You could hit one of us in a space this tight!")
revise(37, (3,), "Don't! You fire in here, you'll hit one of us!")
revise(38, (3,), "Hold your fire! It's too cramped to shoot without hitting one of our own!")
revise(39, (2,), "Admiral! It's too cramped! We might shoot one of our friends!")
revise(40, (1, 2, 3), "Absolutely not! In a space this tight, we'd be far too likely to shoot one of our own!")
revise(42, (0, 1, 2, 3), "Huff... Huff... We managed to bring it down...")
revise(44, (0, 1, 2, 3), "Huff... Huff... We got it... I think...")
revise(45, (0, 1, 2, 3), "Huff... Huff... Looks like we got it...")
revise(47, (0, 1, 2, 3), "Huff... Huff... We finally brought it down!")
revise(49, (0, 1, 2, 3), "Huff... Huff... We managed to defeat it!")
revise(50, (1, 3), "Quite a few sailors seem injured.")
revise(52, (2,), "Seems it wasn't hungry after all. It's not following us.")
revise(53, (1, 2), "Guess it wasn't hungry after all. It's not chasing us.")
revise(55, (3,), "It's not chasing us, so I guess it wasn't hungry. We got lucky.")
revise(56, (1,), "Since it isn't chasing us, I suppose the tiger wasn't hungry.")
revise(58, (2,), "It would seem it wasn't hungry after all. It isn't pursuing us.")
revise(61, (1,), "This jungle is unsettling...")
revise(67, (1,), "Watch your step, FI. The moss is slippery.")
revise(71, (1,), "Hmph... We'll only get more people hurt. Switch to close combat!")
revise(72, (1,), "Hm... There's a light over there.")
revise(73, (1,), "We can get out of the cave now.")
revise(78, (2,), "Admiral, you can't stay behind. Who'll lead us?")
revise(80, (2,), "It'll be bad for morale if you don't come with us, Admiral.")
revise(90, (2,), "Quit kidding around, Admiral. Let's get inside!")
revise(91, (2,), "Too late for that. Let's get going, Admiral.")
revise(94, (2,), "Come now, Admiral. Shall we go in?")
revise(95, (2,), "W-what are you saying? You're supposed to say, 'Let's go!'")
revise(100, (2,), "It's so dark in here... Here's my chance!")
revise(101, (2,), "Hmm-hmm-hmm... Oh, FI...")
revise(106, (2,), "What?! It's so fast!")
revise(107, (2,), "We'll only get more people hurt. Let's use our swords!")
revise(109, (3,), "It's so humid... The air feels stifling.")
revise(110, (3,), "That's the jungle for you. Wild beasts lurk here, Admiral. We should choose our path carefully.")
revise(116, (3,), "We'll only get more people hurt. Let's switch to close combat!")
revise(117, (3,), "Wait, FI... I can see light over there.")
revise(118, (3,), "We can get out of this cave now...")

PHRASES = (
    "a jungle like this", "without a map!", "a clear route.", "don't wanna go in there",
    "go back the way we came...", "doesn't bode well...", "isn't there?", "a bad feeling...",
    "one bit...", "space this tight", "one of our own!", "hit one of us!",
    "don't shoot!", "too cramped", "a few of the crew", "seem to be injured.",
    "hold your fire!", "close combat!", "more people hurt.", "not chasing us.",
    "wasn't hungry after all.", "watch your step, FI.", "the moss is slippery.",
    "a light over there.", "get out of the cave", "you can't stay behind.",
    "who'll lead us?", "let's get inside!", "come now, admiral.", "let's go!",
    "here's my chance!", "let's use our swords!", "the air feels stifling.",
    "wild beasts lurk here, Admiral.", "choose our path carefully.", "can see light over there.",
    "it's too dangerous!", "I've got a bad feeling...", "far too likely", "one of us",
    "you'll hit one of us!", "without hitting one of our own!", "switch to close combat!",
    "We'll only get more people hurt.", "we managed to bring it down...",
    "looks like we got it...", "we finally brought it down!", "we managed to defeat it!",
    "Let's get going, Admiral.",
)


def review_one(raw, group, prior, index, path, digest):
    route, block, word = group["route"], group["block"], raw["native_command_word"]
    selector = raw["selector"]
    prefix = bytes([selector]).hex() if word == 0x4000 else ""
    src, old = prefix + raw["source_body_hex"], prefix + raw["current_body_hex"]
    assert prior["source_hex"] == src and all(prior["review"].values())
    previous = binder.logical(raw["current_English"])
    text = EDITS.get((index, route), previous)
    assert text.isascii() and binder.logical(text) == text
    assert binder.Counter(binder.TOKEN.findall(text)) == binder.Counter(binder.TOKEN.findall(raw["Japanese"]))
    decision = "revision" if text != previous else "retention"
    note = NOTES[index - 1]
    # Each unchanged variant has the same source rationale, with its exact
    # existing wording recorded independently.
    src_ref, old_ref = (dict(file_path=raw["file_path"], block=block, offset=raw[f"{side}_offset"],
        command_offset=raw[f"{side}_command_offset"], archive_sha256=group[f"{side}_archive_sha256"],
        exact_stored_hex=encoded) for side, encoded in (("source", src), ("current", old)))
    src_ref["record_index"] = raw["source_record_index"]
    if word == 0x2100:
        src_ref["source_index"] = old_ref["source_index"] = raw["slots"][0]
    return dict(id=prior["id"], route=route, block=block, file_path=raw["file_path"],
        source_reference=src_ref, current_reference=old_ref, source_hex=src, current_hex=old,
        source_selector=selector, native_slots=raw["slots"], native_command_word=word,
        speaker=prior["speaker"], kind="typed-choice-label" if word == 0x2100 else
        "system-FE" if selector == 254 else "progressive", Japanese=raw["Japanese"],
        source_meaning=note, context=group["context"], localization_note=note,
        previous_English=previous, english=text, decision=decision,
        protected_phrases=[p for p in PHRASES if p.casefold() in text.casefold()],
        earlier_ledger=str(path), earlier_ledger_sha256=digest,
        historical_layout_matches_current=prior["planned_integrated_reference"]["exact_stored_hex"] == old,
        review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False))


def main():
    assert base.digest(SOURCE) == SOURCE_SHA
    paired, release = map(base.load, (SOURCE, parent.RELEASE))
    assert paired["complete_source_current_binding"] and len(paired["groups"]) == 4
    assert paired["candidate_sha256"] == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    histories = [Path("translations") / filename for filename in HISTORY]
    indices = [binder.index_history(p) for p in histories]
    hashes = [base.digest(p) for p in histories]
    context = defaultdict(list)
    for group in paired["groups"]:
        for raw in group["records"]:
            context[raw["native_command_word"], raw["Japanese"]].append((group, raw))
    assert len(context) == len(NOTES) == 118
    records, edited = [], set()
    for position, variants in enumerate(context.values(), 1):
        for group, raw in variants:
            route = group["route"]
            prior = indices[route][group["block"], raw["source_offset"]]
            row = review_one(raw, group, prior, position, histories[route], hashes[route])
            if row["decision"] == "revision":
                edited.add((position, route))
            records.append(row)
    assert edited == EDITS.keys()
    records.sort(key=lambda r: (r["route"], r["source_reference"]["offset"]))
    assert len(records) == 259 and len({(r["file_path"], r["id"]) for r in records}) == 259
    assert not OUTPUT.exists()
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
        source_packet=str(SOURCE), source_packet_sha256=SOURCE_SHA, previous_sha256=release["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"], clean_input_sha256=release["clean_input_sha256"],
        formatting_and_registration_pending=True, additional_review_credit=0, records=records))
    print(dict(binder.Counter((r["kind"], r["decision"]) for r in records)), flush=True)


if __name__ == "__main__":
    main()
