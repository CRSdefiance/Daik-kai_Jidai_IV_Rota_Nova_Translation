"""Review the Letzel and Camille scenes and the armadillo rumor in every route."""

from inspect import getsource
from struct import unpack_from

from scripts import prepare_naturalist_aliases_and_shield_20261119 as paired
from scripts import review_story_short_phrase_wraps_20261119 as workflow

base, native, parent = paired.base, paired.native, paired.parent
ROOT, SOURCE = paired.ROOT, paired.SOURCE
OUTPUT = ROOT / "contextual_review_v3.json"
NAMES = workflow.NAMES
DEFAULT_NAMES = NAMES.with_name("default_character_names_20261115_v1.json")

RAFAEL = """Rafael sees Athens as a place for learning and philosophy.
The city's scholarly atmosphere makes Janus feel as though he ought to study.
The precise agreement suits the speaker's earnest anticipation of learning.
Claudio's complaint concerns the other speaker's stiff manner.
The quick rebuke follows Claudio's familiar grousing.
Rafael backs up the rebuke without escalating it.
The repeated assent lets Claudio concede with mock obedience.
Julio takes the opportunity to investigate the Proof of Conquest.
Claudio sounds out the unfamiliar term.
Rafael remembers Julio had an errand and asks about it.
Julio names the Proof in this alternative introduction.
Use the full title while Rafael still has to learn what it means.
Julio explains that finding out is exactly his purpose.
The question marks preserve the silent beat of confusion.
Julio asks them to wait and says he will return soon.
Rafael agrees tentatively while still puzzled.
Rafael notices the commotion before he knows what it is.
The sailor dismisses the request and tells him to try elsewhere.
The stranger will take any place aboard to reach a faraway country.
Preserve the dismissive challenge about his age and swabbing the deck.
His plea answers the sailor's objection.
Rafael intervenes politely and asks what happened.
The stranger recognizes that Rafael has just come in by ship and requests passage.
The sailor warns Rafael that the stranger expects free passage.
Rafael makes sure the man wants to go to sea and considers taking him.
Claudio objects to bringing another old man aboard.
The stranger hears the hesitation as a likely refusal.
Rafael asks for his reason before deciding.
Bind the introduction of Hans Letzel to actor 75 and keep his work as a naturalist.
Hans sees the whole world as his field of study and begs for the chance to see it.
Claudio pauses before unexpectedly siding with Hans.
Rafael has understood the explanation and is waiting for the response.
Claudio's enthusiastic approval reverses his earlier objection.
Rafael checks that he heard Claudio correctly.
Claudio admires his resolve to risk the voyage at his age and finish the research.
Rafael agrees and courteously invites Hans aboard by name.
Hans checks the invitation and thanks him.
He admits he is asking another favor and addresses the admiral.
Rafael gives him room to ask.
Hans hesitates before asking for passage for one other person.
Keep Rafael's silent bafflement.
Hans pauses before calling his promising assistant a young man, then asks for an introduction.
Keep Arcadius Eudoxios and the formal introduction.
Janus's private aside notes his slender build.
Claudio teases Janus for making the observation when Janus is slight himself.
Rafael clears his throat at the asides.
Hans repeats his hesitation about young man and praises more than the assistant's dedication.
Arcadius knows a little about navigation and expects to learn from the others.
Rafael puts Arcadius at ease by saying they are just getting started too.
Arcadius is relieved by the reassurance.
Hans celebrates the start of the voyage with everyone aboard.
Janus looks forward to the trip.
Rafael asks Claudio to agree that having a learned scholar aboard is reassuring.
Claudio gives the doctor and then the assistant their own encouragement.
Hans answers the encouragement with confidence.
Arcadius gives a quieter, courteous acknowledgment.
The offscreen call interrupts the group.
Rafael recognizes Julio as he arrives.
Julio spots the person he was looking for.
Hans greets Julio with surprised warmth.
Julio confirms he was looking for Hans.
The punctuation preserves Claudio's wordless confusion.
Rafael is surprised that Hans is the person Julio was looking for.
Julio knows Hans and explains that he has studied the Proof for years.
Hans is surprised to learn the others are interested in the Proof too.
Rafael has not yet heard enough to be interested and asks what the Proof is.
Arcadius explains the legend of regional treasures for those who rule the seas.
Hans distinguishes the remaining mystery from a possible lead.
Julio is surprised that Hans may have found something.
The account distinguishes seven treasures, the places designated for them and maps of different shapes.
The person who comes to rule each sea is destined to receive its map.
Rafael considers what it would mean to collect the treasures themselves.
Julio explains that this would make them rulers of the seas in name and fact.
Rafael lets the idea sink in before committing.
Rafael proposes winning the treasures through the crew's own efforts.
Claudio teasingly calls Rafael the eager one and wants to see a Proof firsthand.
Keep the uncomplicated resolve on this path.
The alternative joins the hunt to a future challenge to Hayreddin.
Arcadius echoes Hayreddin in surprise.
Hans wonders aloud what sort of ship he has joined.
Julio laughs and jokes that Hans has noticed too late how fearless Rafael is.
Hans is amused by the spirit of youth.
Keep the report a rumor and keep the Proof title together in the southern Africa lead.
Rafael's short question asks whether the rumor is true.
Hans cannot vouch for the rumor but thinks Africa may yield a clue.
Rafael decides to head for Africa.
The distinct speakerless notice announces that Hans Letzel has joined.
The notice explains why Hans cannot be assigned on Deck.
The follow-up states the new access to detailed item information.
The notice tells the player to press X while viewing item information.
Hans offers to answer item questions while admitting he cannot take on shipboard work."""

CAMILLE = """The largest power in Southeast Asia is gone, and Lil can trade freely.
Lil's brisk rally keeps the momentum after the fall of the company.
The alternate outcome keeps Lil's exuberant realization that no one can object to her trading.
The same rally also fits this alternate outcome.
The third outcome places the Kuhn Company under Lil's authority and gives her freedom to trade.
Camille stammers, which prompts the concern that follows.
Lil notices his color and asks what's wrong.
The older sailor offers fatigue from the voyage as a possibility.
Camille stammers and insists nothing is wrong.
Lil accepts the answer uncertainly, then demands to know who the stranger is.
In the recognition branch, Lil breaks off on spotting someone she knows.
The abrupt demand comes from a crewmate who recognizes the visitor.
Kuhn heard the rumors but hardly dared to believe it was this person.
Lil is still unsure who the man is in this branch.
Lil recognizes and names Kuhn in the other branch.
Camille's silence delays the acknowledgment.
Kuhn hesitates and asks Camille to confirm the name Marinus.
Camille acknowledges the name quietly.
Lil is baffled that Camille answered to another name.
The alternate reaction asks how Camille knows Kuhn.
The crewmate asks what kind of connection the two have.
The startled companion asks what is going on.
Camille addresses Lil by the entered name and explains that there is a story behind it.
Kuhn supplies the explicit father-son relationship.
Lil repeats the newly revealed relationship in disbelief.
The other branch names Antony Kuhn as Camille's father.
The crewmate repeats Camille's earlier claim that his father was dead.
The companion struggles to believe the revelation.
Retain Marinus Kuhn here as the name Camille discloses himself.
Camille appeals to his father to earn an honest living again, as he once did.
Kuhn concedes the possibility while insisting on his own methods.
Camille appeals to Dad in a single word.
Kuhn intends to start from scratch and has not given up.
The silence leaves room for Kuhn to offer the object.
Kuhn asks Marinus to keep the object, which he no longer needs.
Camille asks what it is.
Kuhn says he acquired it when he was young.
Camille asks whether his father can go back to the kind man he remembers.
Kuhn's refusal is short and final.
Camille urges his father to start over with his mother.
The pause before asking about Camille's mother shows Kuhn's change of subject.
Camille answers simply that his mother is well.
Kuhn is relieved but says that too much time has passed to go back.
Camille's unfinished address follows Kuhn's refusal to turn back.
Keep the father's last request and his use of Marinus.
Camille agrees and gives his father a personal farewell.
Lil resumes calling him Camille and asks about what happened.
Camille apologizes and sets a boundary about discussing his past.
Lil acknowledges his request quietly.
The crewmate asks everyone to give him room and recognizes the need for privacy.
The last reassurance leaves the decision to tell them with Camille."""

MIKHAIL = """Lil asks Camille what he is doing.
Camille names the Proof of Conquest and tries to explain who has a lead.
Lil prompts him to name the person.
Mikhail announces himself theatrically and uses the entered name in his familiar greeting.
Lil accuses him of harassment and warns him about repeating the contact.
Camille tries to restrain Lil and addresses her by the entered name.
Mikhail needles Lil and treats her anger as coldness.
Camille gets flustered and switches to the full name and scholarly address of actor 76.
Mikhail is flattered by the title and directs the next question to Lil by name.
Lil points out that Camille asked the question, then asks for the explanation herself.
Keep the legend of the scattered treasures and the limits of his knowledge.
The documents name seven treasures and say the Seven Sages marked different kinds of maps.
The person who comes to rule a sea is destined to receive its map.
The native company substitution names Camille's group, and he leaves his inference unfinished.
Lil repeats the significance of the Proof.
The older crewmate gives Mikhail an affectionate, backhanded compliment.
The other speaker connects the proof to the standing of the player's company in that sea.
The blunt crewmate wants to try collecting the Proofs even before fully understanding them.
Mikhail boasts and asks whether they are impressed by his knowledge.
Lil admits he was helpful and reminds him what will happen if he touches her.
His reassurance and laugh fail to win Lil's trust.
Lil rejects the reassurance outright.
Camille returns to the question of how to collect the Proofs.
Mikhail explains the importance of control and gives influential people as a source of leads.
If a malicious person has the lead, that person may need to be defeated.
Lil reduces the advice to beating the villains.
The search continues through city ruins and the mysteries of the sealed Proofs.
Lil asks how to find the ruins.
Mikhail's one-word answer sets up the comic misunderstanding.
Lil's disbelief needs only the short reaction.
Mikhail explains where leads on nearby ruins can be found.
Lil asks him to explain what women have to do with the search.
The clue sources are the women in the taverns who hear sailors' stories.
He cautions that valuable information will cost them something.
Lil grumbles at having to pay.
Mikhail gives his exchange principle and reminds her of the value of the treasure."""

RUMOR = """Samwell asks for a moment of the admiral's time.
The captain listens and gives Samwell room to continue.
Samwell has just heard about an animal whose hide is said to be harder than iron.
The short reaction leaves the supposed fact unexplained.
The older account links the animal's hide to the shield and names the actual item.
The captain presses Samwell for the relevance of the shield.
Samwell teases the captain for missing the point and suggests the shield would help in a fight.
The captain sees the value of the shield and asks where to obtain it.
The location is only a rumor somewhere in or around Africa.
The captain points out that the lead is too vague to act on.
Samwell hesitantly admits the lead is thin.
The captain will remember the rumor and suggests they might get lucky.
Samwell's brief agreement closes the conversation."""

EXCHANGES = {
    (0, 48): (0, RAFAEL), (2, 65): (0, CAMILLE), (2, 169): (0, MIKHAIL),
    **{(route, block): (0, RUMOR) for route, block in enumerate((240, 231, 228, 201))},
}
EDITS = {}


def revise(route, block, rows):
    for index, (text, phrases) in rows.items():
        EDITS[route, block, index] = text, phrases


revise(0, 48, {
    17: ("Just being in this city makes me feel like I ought to study.", ("like I ought to study.",)),
    81: ("Oh, that's right. Julio, what was that errand you mentioned?", ("Oh, that's right.", "that errand")),
    92: ("What's the Proof of Conquest?", ("the Proof of Conquest?",)),
    125: ("The deck, the hold, anywhere will do! Just take me to a faraway country.", ("the hold", "Just take me to a faraway country.")),
    140: ("Oh! You just came in on that ship? Could you take me aboard?", ("came in on that ship?", "Could you take me aboard?")),
    144: ("I'd think twice, Captain. This old man wants a free ride!", ("I'd think twice, Captain.", "old man", "a free ride!")),
    167: ("The whole world is my subject! Please take me with you. Let me see it for myself!", ("The whole world is my subject!", "Please take me with you.", "Let me see it for myself!")),
    192: ("Y-yeah, you're right. Hans, you're welcome aboard.", ("you're right.", "you're welcome aboard.")),
    200: ("Admiral, would you mind doing me one more favor?", ("one more favor?",)),
    280: ("What do you think, Claudio? I'm glad we have a scholar aboard.", ("What do you think, Claudio?", "I'm glad we have a scholar aboard.")),
    284: ("I guess so. Good luck with your research, Doctor! Oh, and you too!", ("with your research, Doctor!", "and you too!")),
    331: ("Interested? I don't even know what the Proof of Conquest is.", ("the Proof of Conquest is.",)),
    347: ("An ancient text says there are seven treasures. The Seven Sages marked where they were to be sealed on maps of different shapes.", ("seven treasures.", "The Seven Sages", "maps of different shapes.")),
    393: ("Good heavens! What kind of ship have I gotten myself onto?", ("Good heavens!", "What kind of ship")),
    431: ("Hans isn't a navigator, so you can't assign him on the Deck screen.", ("assign him", "on the Deck screen.")),
    438: ("Press X while you're viewing item information.", ("Press X", "viewing item information.")),
})
revise(2, 65, {
    50: ("Now that the Kuhn Company is under us, we can trade freely in Southeast Asia. Let's get to work!", ("the Kuhn Company", "in Southeast Asia.", "Let's get to work!")),
    61: ("Huh? What's wrong? You look pale.", ("What's wrong?", "You look pale.")),
    93: ("Really? Well, if you say so... Oh! It's you!", ("if you say so...", "It's you!")),
    115: ("So it was you. I heard the rumors, but I never thought it could be true...", ("So it was you.", "I heard the rumors")),
    153: ("Marinus? Camille, why did you answer? I'm lost. What's going on?", ("why did you answer?", "What's going on?")),
    173: ("So what are you two to each other?", ("to each other?",)),
    198: ("Marinus... I never imagined I'd see my son again here.", ("see my son again here.",)),
    227: ("S-son?! You said he was gone. You said your father was dead!", ("S-son?! You said he was gone.", "You said your father was dead!")),
    252: ("Dad, you see it now, don't you? You can earn an honest living, just like you used to.", ("don't you?", "earn an honest living", "just like you used to.")),
    255: ("Hmph. Maybe so. But I have my own way of doing things.", ("my own way", "of doing things.")),
    262: ("I'll start over from scratch. I haven't given up yet.", ("start over from scratch.", "given up yet.")),
    282: ("Dad... Can't you be the kind father you used to be?", ("the kind father", "you used to be?")),
    301: ("Good. I'm glad. It's been a long time since then. You can't go back.", ("since then.", "You can't go back.")),
    313: ("...I will. Take care too, Dad...", ("Take care too, Dad...",)),
    324: ("...I see.", ("...I see.",)),
    336: ("Let's give him some space. Everyone has things in their past they'd rather leave alone.", ("give him some space.", "leave alone.")),
})
revise(2, 169, {
    8: ("Oh, FI. I was looking into a treasure called the Proof of Conquest. But the person with a lead is...", ("the Proof of Conquest.", "with a lead is...")),
    32: ("You're throwing me off... Mikhail... I mean, Dr. Mikhail Letzel! I wanted to ask you about the Proof of Conquest.", ("Dr. Mikhail Letzel!", "the Proof of Conquest.")),
    35: ("Well, if you call me Doctor, how can I refuse? Ahem. So the Proof of Conquest interests you, FI dear?", ("call me Doctor", "the Proof of Conquest", "FI dear?")),
    47: ("It says the map is destined to go to whoever comes to rule that sea.", ("It says the map is destined to go", "to whoever comes to rule that sea.")),
    67: ("Hmm. Even Mikhail makes sense now and then.", ("now and then.",)),
    104: ("Well? Impressed by how much I know?", ("how much I know?",)),
    115: ("I don't trust you one bit!", ("one bit!",)),
    156: ("Sailors from all over the world tell their stories to the women at the taverns every day. They're bound to know something.", ("Sailors from all over the world", "at the taverns", "know something.")),
    167: ("Everything's give-and-take. It's a small price next to what that treasure's worth.", ("give-and-take.", "a small price", "what that treasure's worth.")),
})

for route, block, opening, animal, shield, offer in (
    (0, 240, 5, 14, 23, 30), (1, 231, 5, 13, 21, 28),
    (2, 228, 5, 13, 21, 28), (3, 201, 4, 12, 20, 27),
):
    revise(route, block, {
        opening: ("Got a minute, Admiral?", ("Got a minute, Admiral?",)),
        animal: ("I just heard about armadillos. Know what they say? Their hides are harder than iron.", ("I just heard about armadillos.", "Know what they say?", "Their hides are harder than iron.")),
        shield: ("They say someone made a shield from an armadillo's hide long ago. They called it the Armadillo Hide.", ("an armadillo's hide", "the Armadillo Hide.")),
        offer: ("Come on, keep up! A shield harder than iron! Wouldn't you want one? It'd come in handy in a fight.", ("Come on, keep up!", "A shield harder than iron!", "Wouldn't you want one?", "It'd come in handy in a fight.")),
    })


def evidence():
    names = {r["actor_ID"]: r for r in base.load(DEFAULT_NAMES)["current_default_names"]}
    actors = (9, 22, 75, 76)
    clean, current = (base.NdsImage.open(p).read_file(native.ARM) for p in (native.CLEAN, parent.ROM))
    for actor in actors:
        for field in names[actor]["source_name_fields"]:
            at = field["ARM9_pointer_field_offset"]
            assert unpack_from("<I", current, at)[0] == field["current_pointer"]
            item = field["clean"]
            if item:
                assert clean[item["offset"]:item["offset"] + item["byte_length"]].hex() == item["hex"]
    assert [names[a]["current_consumers"][0]["text"] for a in actors] == [
        "Camille Overijssel", "Samwell Khan", "Hans Letzel", "Mikhail Letzel"]
    item_field = 1173184

    def item_name(arm):
        address, = unpack_from("<I", arm, item_field)
        offset = address - 0x02000000
        raw = arm[offset:arm.index(0, offset)]
        return dict(pointer_field=item_field, pointer=address, offset=offset, hex=raw.hex(),
                    text=raw.decode("cp932"), arm9_sha256=native.digest(arm))

    source, installed = map(item_name, (clean, current))
    assert source["text"] == "アルマジロの鉄皮" and installed["text"] == "Armadillo Hide"
    return dict(default_forms={a: names[a]["current_consumers"][0]["text"] for a in actors},
        historical_default_forms=dict(path=DEFAULT_NAMES.as_posix(), sha256=base.digest(DEFAULT_NAMES)),
        source_and_current_item=dict(source=source, current=installed),
        in_story_reveal="SC2 B65 R0249: Marinus Kuhn. Keep Camille's default nameplate.")


def main():
    source = getsource(workflow.main).replace(
        '    assert edits_seen == EDITS.keys()',
        '    assert len(records) == 230 and edits_seen == EDITS.keys()',
    ).replace(
        '        counts=dict(counts), prior_evidence=evidence,',
        '        counts=dict(counts), prior_evidence=evidence, identity_and_item=IDENTITIES,',
    )
    env = vars(workflow) | globals() | {"LIL": (), "IDENTITIES": evidence()}
    exec(compile(source, __file__ + "::paired-review", "exec"), env)
    env["main"]()


if __name__ == "__main__":
    main()
