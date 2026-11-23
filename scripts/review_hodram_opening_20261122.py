"""Review the remaining early Hodram exchanges from their exact clean Japanese."""

from collections import Counter

from scripts import pair_hodram_opening_20261122 as paired
from scripts.review_rafael_B221_B224_20261122 import precedent


base = paired.base
OUTPUT = paired.ROOT / "contextual_decisions_v4.json"
CONTEXTS = {
    24: "Defeated Hernan tries to save face. Hodram responds with instructions pending his transfer to the Athens guild.",
    25: "Iscal protests his defeat and cries out. Hodram orders the return to Stockholm, then the crew finds the unusual plate.",
    26: "Gerhard waits for their quarry to show himself. Hodram sees the mission as the start of a campaign against pirate fleets.",
    27: "Defeated William Clive shrieks and curses. Hodram wants the Havana guild to take him promptly.",
    41: "Seven physical lookout reactions, across the original eight slots, signal the arrival of a monster fish.",
    42: "The crew issues a territorial warning. Afterward Hodram rallies his crew around building Sweden's navy, then turns to state rewards and the Hanseatic report.",
    44: "Lil challenges Hodram's presence in her trading territory. Camille tries to calm her, Gerhard takes offense, and Hodram stops the confrontation.",
    45: "A port worker tells Hodram where the head of the Argot Company is waiting.",
    46: "Lil challenges Hodram to a treasure race. She offers the key to the map and claims the winner will rule the North Sea.",
    47: "When Hodram gets there first, Lil turns a grudging concession into a demand that he beat everyone else.",
    48: "Lil finds Ullr's Bow first. She teases Hodram and names Amsterdam as the place to meet if he wants it.",
    49: "Lil offers the regional Proof in exchange for a wristband. Her bargaining bravado gives way to open delight when Hodram has it.",
    50: "Lil recognizes that Hodram returned with the requested wristband and immediately completes the exchange.",
    52: "The port worker asks whether Hodram intends to make an enemy of Hayreddin's faction. The choices lead to advice or a warning about the risk.",
    53: "The port worker reports that the Ottomans have finally put out word for Hodram, then tells him to watch himself.",
}

# Empty replacements retain the installed logical wording. A protected phrase
# on a retained line requests a formatter-only change.
DECISIONS = {
    24: """
9|||Hernan stammers and claims he let Hodram win. The boast is an excuse after the defeat.
12|The Athens guild will hold you. Behave yourself until then.|The Athens guild will hold you.;Behave yourself until then.|Hodram states who will hold Hernan and tells him to cooperate until then.
""",
    25: """
8|Gah! I... I lost? I won't accept it! I won't!|I won't accept it!|Iscal acknowledges defeat in disbelief before twice refusing to accept it. Keep his panic and repetition.
12|||The drawn-out cry closes Iscal's part of the exchange.
16|Our mission is complete. We return to Stockholm to report to His Majesty.|return to Stockholm;report to His Majesty.|Hodram gives the exact destination and purpose of the return. The order follows Iscal's defeat.
20|||The sailor addresses the admiral and reports the find aboard the enemy ship. The exclamation suits the discovery.
26|||Hodram guesses it is part of Iscal's plunder and doubts the object is an ordinary painted plate. His uncertainty sets up the reveal.
""",
    26: """
28|You'd think he'd show himself by now...|show himself by now...|Gerhard expects to see the quarry soon and trails off when there is still no sign of him.
52|||Hodram plans to keep eliminating pirate fleets in succession. The existing wording sounds like the terse promise he makes.
""",
    27: """
9|Aaagh! Damn you! I'll curse you! I'll curse you! I'll curse you!|Damn you!;I'll curse you!|Clive's opening is a shriek followed by a drawn-out insult and exactly three curses. The repetition carries the outburst.
13|...We'd better get the Havana guild to take him soon.|the Havana guild|Hodram's pause is a dry response to the shouting. He wants the guild to take custody quickly.
""",
    41: """
SC1_B41_STYLE_10_0|Admiral! Here it comes! A monster fish!|A monster fish!|The lookout addresses Hodram and calls out the fish's arrival. Both original slots share the same urgent delivery.
SC1_B41_STYLE_10_36|||The brief yelp and exclamation fit the surprised lookout who blurts out what it is.
SC1_B41_STYLE_10_62|||Her startled cry and stammer distinguish this report from the more direct lookouts.
SC1_B41_STYLE_10_104|Admiral! A blasted monster fish!|A blasted monster fish!|Use a mild oath for the rough expression while the lookout shouts the sighting to the admiral.
SC1_B41_STYLE_10_140|A-Admiral! A monster fish!|A-Admiral!|Preserve the stammer in the address. The Japanese ending gives this voice an older cadence without asserting age.
SC1_B41_STYLE_10_166|There it is! A monster fiiish!|A monster fiiish!|The long cries and exaggerated spelling make this voice distinctly drawn out.
SC1_B41_STYLE_10_200|||The lookout delivers the arrival report with a more formal cadence. The existing complete sentence suits that delivery.
""",
    42: """
15|||Hodram's terse order starts the warning. His controlled tone gives way to the crew's shouted relay.
19|||Keep the immediate affirmative shout as a speakerless reply.
23|||Charles relays Hodram's warning order emphatically, without adding instructions.
27|||The second speakerless acknowledgment echoes the first and sounds drawn out as a call across the deck.
31|||The shouted warning identifies the patrol, territorial violation and order to stop. Keep its three distinct calls together on the speakerless panel.
34|||Hodram moves the crew into action after the warning with a brisk command.
39|||The understated praise changes the mood as Gerhard asks Hodram to address the crew.
43|||Gerhard formally invites Hodram to address the crew. The title is already established on deck.
47|||Hodram hesitates before the speech. Keep the brief grunt.
51|||Charles's silent beat leaves Hodram the floor.
55|||Manuel likewise waits for Hodram to speak.
59|You know the island nation growing so powerful in the North Sea?|the island nation;in the North Sea?|Hodram asks the crew to identify the rising island kingdom and answers in the next turn.
62|England openly permits piracy against Spanish merchant ships. The plunder steadily builds up its navy.|England openly permits piracy;Spanish merchant ships.;builds up its navy.|Hodram says England openly permits piracy against Spanish merchant shipping and turns the proceeds into naval strength.
65|Sweden means to lead in the Baltic and the North Sea. We must follow England's example and build a world-class navy.|the North Sea.;a world-class navy.|The objective is maritime leadership in both named regions and a navy of the first rank.
68|They've entrusted the whole job to us. The truth is, they don't expect much from us.|entrusted the whole job;The truth is,;they don't expect much from us.|Hodram contrasts full responsibility with his superiors' low expectations before explaining why.
72|||Gerhard has no immediate answer to Hodram's frank admission.
76|You all know we're a navy in name only. We have just one ship, the Vestaros.|a navy in name only.;the Vestaros.|Keep the name of the ship and the exact size of the fledgling fleet.
79|||The existing stopgap image conveys how their superiors view the patrol fleet while a regular navy is being formed.
82|We're a young nation. Aiding the Protestants is state policy, and it's one reason money's tight.|Aiding the Protestants;is state policy,;one reason money's tight.|Hodram names support for Protestants as a contributing constraint on the state budget.
86|We face a long, hard road. I doubt we'll get there in two or three years.|a long, hard road.;two or three years.|Hodram warns this is a long undertaking and keeps the original two-or-three-year horizon.
90|One day, the world's strongest navy will sail the Baltic. We'll build it ourselves for His Majesty and all our people to see!|the world's strongest navy;sail the Baltic.;His Majesty|Hodram imagines their own fleet on the Baltic and challenges them to show it to the king and the whole nation.
93|Our success depends on you. Keep at it with all you've got!|Our success depends on you.;Keep at it with all you've got!|Hodram ends the address by making the crew's sustained effort decisive.
96|||The speakerless cheer is the crew's answer to the end of the speech.
100|||The speakerless applause follows the cheer. The short action label suits the established staged panel.
105|||Manuel compliments Hodram's speech as something that always moves him. The plain phrase sounds spontaneous.
109|It's no exaggeration to say a speech like that is what made us want to spend the rest of our lives in this country.|no exaggeration;the rest of our lives;in this country.|Gerhard recalls that the force of Hodram's oratory helped persuade them to make their lives in the country.
113|One of your speeches, Admiral FA, was the first thing that ever made me shake with eagerness for battle.|Admiral FA,;eagerness for battle.|Charles recalls a strong physical excitement at the prospect of battle. Keep the captain's surname substitution.
116|Enough of that. Few duties are as painful as giving a speech. Anyway...|Enough of that.;giving a speech.|Hodram is uncomfortable with the praise and pivots from his most painful duties to business.
120|Word is, the state will pay us for defeating enemy fleets and pirates. How much we get depends on what we accomplish.|enemy fleets and pirates.;depends on what we accomplish.|The new policy pays state rewards according to results. Hodram reports what he has been told.
124|||Manuel's quick exclamation suits his excitement at the prospect of rewards.
128|So now we'll have a way to raise more money for the fleet.|more money for the fleet.|Charles draws the practical conclusion about increasing fleet funds.
131|At last, we can go on the offensive.|go on the offensive.|Gerhard sees the change as a chance to take the initiative rather than a command to attack immediately.
135|Check that report of Hanseatic ships trespassing in our waters. It seems we went after the wrong quarry today.|Hanseatic ships;in our waters.;the wrong quarry today.|Hodram wants the unauthorized incursion report checked promptly. His assessment of their earlier quarry remains tentative.
138|Give the crew a short rest, then get us ready to sail right away.|a short rest,;ready to sail right away.|The rest comes before immediate preparation to leave.
141|||Gerhard's formal assent fits his established manner and the closing trio of replies.
145|||Charles's nautical acknowledgment stands between Gerhard's and Manuel's.
149|||Manuel ends on the distinctive two-part nautical acknowledgment.
""",
    44: """
6|||The unidentified young woman's voice interrupts before Lil's identity is revealed.
9|||Hodram reacts in silent confusion to the sudden call.
14|That ship moored in the harbor is yours, right? What do you think you're doing?|is yours, right?;What do you think you're doing?|Lil makes sure it's his ship, then immediately challenges what he is up to.
17|||Hodram's silence prompts Lil to insist that he answer her.
25|...What are you getting at?|What are you getting at?|After the second demand for an answer, Hodram asks her to get to the point.
29|||Lil claims the place as her territory and forbids him from trading on his own initiative. The existing bluntness suits her.
33|||Camille scolds Lil for talking to a stranger that way, before trying to calm her down.
37|If we sign a trade contract, there shouldn't be a problem...|a trade contract;there shouldn't be a problem...|Hodram gives the ordinary legal condition for trading. This exact phrase sets up Lil's mocking echo.
41|"There shouldn't be a problem..." Hmph. You're so stiff. What a bore!|There shouldn't be a problem...|Lil mimics Hodram's answer, scoffs at his composure, and calls him tiresome.
45|||Camille's warning is short and anxious because Lil is making the exchange worse.
49|Oh, I get it. You're a military man. Now everyone from soldiers to explorers to pirates has to get into trade?|You're a military man.;get into trade?|Lil recognizes a serviceman and mockingly complains that soldiers, explorers and pirates all want to trade.
53|Outsiders keep muscling in on us merchants. Then they strut around like they own the place. I'm sick of it!|us merchants.;own the place.;I'm sick of it!|Lil speaks for merchants, complains about the steady intrusion, then condemns the newcomers' attitude.
56|||Camille's repeated call to Lil is a sharper intervention.
60|I've heard enough out of you!|I've heard enough out of you!|Gerhard has been listening in silence and finally snaps at Lil's insults.
64|What, you want to take me on?|you want to take me on?|Lil immediately challenges Gerhard when he snaps at her.
68|||Hodram uses Gerhard's name to stop him. The short order suits his authority and restraint.
72|But, Admiral!|But, Admiral!|Gerhard objects to the order without completing his protest. Use the established shipboard title.
76|||Lil concedes that Hodram may be more decent than she expected, before insisting the trade fight is separate.
79|That's a different matter. Get in my way and you'll regret it! Come on, Camille!|Get in my way and you'll regret it!;Come on, Camille!|Lil separates her personal impression from the business warning and orders Camille to leave with her.
88|||Camille's stammer and awkward departure follow the struggling apology.
92|||Charles's silent reaction lets the others break the tension.
104|Yikes... Sh-she's something else.|Sh-she's something else.|Manuel is rattled by Lil and keeps his stammer as the exchange breaks.
111|FI, there's a limit to what you should put up with! How could you let that woman speak to you like that?|there's a limit;like that?|Gerhard uses Hodram's name, objects to his indulgence, and calls Lil out for insulting him.
114|...I'd rather be tortured than deal with someone like her.|deal with someone like her.|Hodram answers Gerhard with a dry exaggeration about how much he dislikes that kind of confrontation.
126|Some people are best left alone. She'd be a handful if you made her mad.|best left alone.;if you made her mad.|Manuel agrees with Hodram through the meaning of the proverb and warns that an angry Lil would be trouble.
""",
    45: """
7|||The port worker uses the Argot Company as his reference and gives Amsterdam as the place to meet its boss. The informal term suits him.
""",
    46: """
6|||Lil calls Hodram to a stop before issuing the challenge.
10|I hear you're the richest person in these waters. So how about a contest?|I hear you're the richest person;in these waters.;So how about a contest?|Lil treats the rumor about his wealth as a reason to challenge him directly. Hodram echoes the word contest in the next turn.
14|||Hodram echoes the idea of a contest in puzzlement before Lil explains the stakes.
19|Here's the key to the treasure map. Whoever finds the treasure first gets to rule the North Sea!|Here's the key to the treasure map.;rule the North Sea!|Lil describes what the key does and claims the first finder will rule the North Sea.
23|This is for real. No going easy on each other! There's no way I'm losing to you!|No going easy on each other!;There's no way I'm losing to you!|Lil insists on a serious contest without either side holding back, and singles Hodram out as someone she refuses to lose to.
51|||Hodram wonders what she means by a key to a map. The unfinished question follows her abrupt departure.
""",
    47: """
6|||Lil's surprise and exasperation fit the moment she learns Hodram found the treasure first.
10|||Lil concedes and quickly shrugs it off. The next line explains how she recovers her pride.
13|You beat me. Don't lose to anyone else! Now go be the best in the world. I'll hold you to it!|Don't lose to anyone else!;Now go be the best in the world.;I'll hold you to it!|Lil turns losing to Hodram into a demand that he hold up her standards and beat everyone else.
""",
    48: """
6|||The narrator keeps the discovery qualified and uses the registered item name Ullr's Bow.
11|||Lil addresses Hodram by his given name and teases him. The giggle carries the source's singsong note.
14|If you want it, be in Amsterdam. I'll see you there.|be in Amsterdam.|Lil names Amsterdam as the meeting point, in a teasing challenge after winning.
""",
    49: """
6|There you are!|There you are!|Lil recognizes Hodram's arrival after making him come to Amsterdam.
10|||Lil gloats before stating why she will not easily part with the regional Proof of Conquest.
15|||Hodram's pause gives Lil room to reveal her proposed trade. Keep the existing ellipsis glyph.
19|||Lil hints at the one item that could get her to part with the bow. The existing line sets up the reveal naturally.
22|||The approved item name and the breezy or something preserve Lil's excited, casual delivery.
33|I hear it's somewhere in the New World. Bring it back and this is yours. Bye-bye!|the New World.;Bring it back;this is yours.|Lil has only a hearsay location and promises the exchange if he brings the wristband.
40|You already have it? Let me see, let me see!|Let me see, let me see!|Lil is surprised he already has it and impatiently asks twice to see it.
43|Wow! It really is cute! Can I have it? I'll give you the bow!|It really is cute!;Can I have it?;I'll give you the bow!|Her delighted reaction comes before a direct request and the offer Lil makes in return.
SC1_B49_CHOICE_574_0|||The concise assent answers Lil's proposed exchange and keeps the positive choice.
SC1_B49_CHOICE_574_1|||Hodram can simply refuse. The short negative leads to Lil pressing him again.
58|||Lil celebrates, tells Hodram not to take it back, and hurries off. The written lines already have her energy.
64|Whaaat?! It's a Proof of Conquest! You don't want it?|a Proof of Conquest!;You don't want it?|Lil is astonished and points out what he would be turning down. Keep the complete item class.
67|||Hodram hesitates before conceding he does want it. His reserve makes Lil's renewed insistence funnier.
71|||Lil seizes on Hodram's concession, offers the bow and asks for the wristband.
74|||The enthusiastic farewell after the second trade branch matches Lil's excitement and hurry.
81|||The speakerless transaction confirms that Hodram gave her the approved item. The same notice appears on the return path.
""",
    50: """
7|You brought it back? Let me see, let me see!|Let me see, let me see!|Lil recognizes the return with the requested item. Match her impatient repeated request when he already has it.
10|||Lil is openly delighted, hands over the bow, celebrates, and says goodbye. The existing line conveys the whole progression.
13|||Use the same transaction notice as the immediate exchange.
""",
    52: """
6|You looking to make an enemy of the Hayreddin Clan?|the Hayreddin Clan?|The worker asks whether Hodram intends to turn the established faction against him. His dropped auxiliary fits the casual tone.
SC1_B52_CHOICE_68_0|||The first answer denies hostile intent, setting up the port worker's advice to leave.
SC1_B52_CHOICE_68_1|||The second answer accepts a confrontation in the same direct tone as the question.
21|||The port worker advises leaving before the clan notices. The short imperative serves the warning.
33|||The question about a death wish gives the worker's reaction to choosing the challenge.
""",
    53: """
7|Looks like the Ottoman Empire's finally put out word for you. Watch your back.|the Ottoman Empire's;Watch your back.|The worker reports that the empire now wants Hodram and cautions him in plain language.
""",
}


def key(row):
    if row["id"].startswith("DK4_MES_"):
        return str(int(row["id"].rsplit("_R", 1)[1]))
    return row["id"]


def main():
    assert not OUTPUT.exists()
    packet, carry = map(base.load, (paired.PACKET, paired.CARRY))
    assert carry["source_packet_sha256"] == base.digest(paired.PACKET)
    pending = {row["id"]: row for row in carry["pending_records"]}
    names = {r["actor_ID"]: r["progressive_nameplate"] for r in
             base.load(precedent.prior.CATALOGUE)["source_and_current_default_name_fields"]}
    records = []
    for block, text in DECISIONS.items():
        rows = [row for row in pending.values() if row["block"] == block]
        for row, line in zip(rows, text.strip().splitlines(), strict=True):
            identifier, replacement, protection, note = line.split("|", 3)
            assert identifier == key(row) and note
            current = " ".join(row["current_English"].split())
            english = replacement or current
            phrases = protection.split(";") if protection else []
            assert all(phrase in english for phrase in phrases), (row["id"], phrases)
            assert precedent.TOKEN.findall(english) == precedent.TOKEN.findall(row["Japanese"]), row["id"]
            word, selector = row["native_command_word"], row["selector"]
            kind = {0x4100: "actor-style", 0x2100: "typed-choice-label", 0x2200: "typed-choice-label"}.get(
                word, "system-FE" if selector == 254 else "progressive")
            prefix = f"{selector:02x}" if word == 0x4000 else ""
            speaker = {"system-FE": "Speakerless panel", "typed-choice-label": "Player choice",
                       "actor-style": "Runtime-selected lookout"}.get(kind, names.get(selector, "Runtime-selected crew voice"))
            records.append(row | dict(
                kind=kind, speaker=speaker, context=CONTEXTS[block], source_meaning=note, localization_note=note,
                previous_English=current, english=english, protected_phrases=phrases,
                source_selector=selector, native_slots=row["slots"],
                source_hex=prefix + row["source_reference"]["exact_body_hex"],
                current_hex=prefix + row["current_reference"]["exact_body_hex"],
                decision="revision" if replacement or phrases else "retention",
                change_class="wording" if replacement else "wrap-only" if phrases else "retention",
                review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
            del pending[row["id"]]
    assert not pending and len(records) == 118
    findings = dict(Counter(row["change_class"] for row in records))
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
        review_gates=["source", "context", "localization", "naturalness", "formatting"],
        previous_sha256=packet["candidate_sha256"], source_packet=str(paired.PACKET),
        source_packet_sha256=base.digest(paired.PACKET), prior_contextual_receipt=str(paired.CARRY),
        prior_contextual_receipt_sha256=base.digest(paired.CARRY), records=records, findings=findings,
        new_editorial_credit=0, status="Contextual review complete. Stored formatting and gameplay checks pending."))
    print(f"Reviewed {len(records)} records. {findings}")


if __name__ == "__main__":
    main()
