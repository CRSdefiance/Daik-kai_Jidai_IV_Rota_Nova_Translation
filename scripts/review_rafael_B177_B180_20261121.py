"""Review Cesare, Fernando, and Manuel as complete exchanges and carry the sailing lesson forward."""

from collections import Counter

from scripts import pair_rafael_B177_B180_20261121 as paired
from scripts import review_rafael_B170_B176_20261121 as prior
from scripts import review_rafael_B180_tutorial_20261121 as tutorial


base, TOKEN = paired.base, prior.TOKEN
OUTPUT = paired.ROOT / "contextual_decisions_B177_B180_v2.json"

WRAPS = {
    "DK4_MES_B178_R0089": (["Losing like that", "burns me up!", "Let's play again!"],
        "Keep the familiar substituted address and Claudio's whole rematch request. The frustration no longer starts with a broken phrase."),
    "DK4_MES_B178_R0269": (["Pick up on things like that", "your opponent's moves."],
        "Give Fernando's observation and the opponent's moves their complete phrases."),
    "DK4_MES_B179_R0059": (["You don't often meet", "cares this much about ships."],
        "Let the private address stand before Janus begins. The first phrase after it reads as a complete thought."),
}

DECISIONS = {
    177: """
5|||Janus recognizes Alexandria in a quiet arrival line, leaving room for Rafael to describe the port.
9|||Rafael observes the port's activity without turning it into a claim about its economy.
15|||Janus notices the stranger approaching and alerts Rafael.
18|||Cesare's half-formed question registers recognition before he explicitly names the ship.
22|||Rafael politely asks what prompted the stranger's reaction.
27|||Cesare stammers, then recognizes the ship with absolute certainty.
30|||Cesare sees through the alterations, then lets his affection for the Elysion show openly.
34|Huh? You knew her just by looking at her?|looking at her?|Janus is taken aback that Cesare recognized a ship by the familiar traces that survived the alterations.
37|Excuse me. Do you know this ship?||Rafael asks what the ship means to the stranger, prompting the introduction.
43|||Cesare identifies himself by name and explains that he used to own the ship.
47|||He says pirates took his ship and that he survived their attack.
51|||Cesare makes the loss personal by naming the Elysion again and admitting how much he grieved.
55|I heard she'd been abandoned. I searched day and night, certain I'd see her again someday!|day and night,|He reports what he heard and gives both the effort and the faith that kept him searching.
58|She was mine, yes! Of course, I'd never ask you to give her back.|give her back.|Cesare confirms the earlier ownership and makes clear that he has no intention of reclaiming her.
61|||His only request is to sail aboard his beloved ship again. Keep the request directed at the group.
65|||Janus latches onto the word former and shifts eagerly from surprise to questions.
68|I can't make sense of some of her fittings. There are things aboard I haven't seen in any book. Am I right?|her fittings.;in any book.|Janus has tried to understand the ship and asks whether its features go beyond what the books describe.
72|||Cesare recognizes the significance of Janus noticing the unusual fittings and compliments his knowledge.
76|Oh, I wouldn't go that far... Come with me! You've got to show me how this works!|Come with me!|Janus's modest denial gives way to the impatient invitation that draws Cesare away.
80|||Cesare's enthusiastic and formally phrased agreement matches Janus's interest.
83|||Janus realizes that he forgot to introduce himself in his enthusiasm.
86|||Cesare repeats his own name for Janus and keeps his courteous manner.
90|Take this spot here. It looks odd, doesn't it? Is there another mechanism behind it?|looks odd, doesn't it?|Janus points out a particular spot and asks whether it hides another mechanism.
94|||Cesare is pleasantly surprised again and starts explaining what the part does.
97|||The hidden Extra Armor mounting point is the answer to Janus's question.
100|Press that little bump. Click! Just like that!|Just like that!|Cesare demonstrates the button and voices the little click in the Japanese.
104|||Cesare leaves the result hanging a beat before Janus sees it.
108|||Janus repeats the prompt and then reacts in surprise as the mechanism works.
114|||The speakerless notice reports the newly available Extra Armor refit without naming an extra action.
117|||Janus stammers with excitement and asks if the method can be used on other ships.
121|||Cesare gives an emphatic confirmation rather than adding a new qualification.
125|||Janus is delighted and starts leading Cesare farther inside.
129|||Rafael tries to call Janus back by name, a short interruption neither man hears.
134|||Rafael sighs in resignation once the pair have left him behind.
139|Janus went ahead and decided all that on his own. So... does that mean Cesare's joining us?|Cesare's joining us?|Rafael's complaint points to Janus rushing ahead and his uncertainty about whether Cesare has actually joined.
144|||Cesare addresses the admiral and politely offers advice about choosing ships, setting up the menu.
2278_0|||Listen directly accepts the offered lesson and fits the first native choice slot.
2278_1|||Skip declines the offered lesson in the second slot without promising any other action.
162|||Cesare takes the refusal as assurance that the admiral already has his own principles and admires that.
166|||Cesare leaves to prepare to sail after the refusal. His farewell is cheerful and a little formal.
176|||This small transition lets Cesare gather his thoughts before starting the accepted lesson.
180|If you're still signing deals with new towns and opening trade routes, a new ship can wait. A one percent share only lets you buy one to five units of trade goods.|signing deals;opening trade routes,;one percent share;one to five units|The first advice gives the early trading condition and the exact one percent and one-to-five figures. The second page starts on the purchasing limit.
183|||Growing market share allows larger purchases and gives the player a reason to buy a ship.
187|||The short instruction gives size and price as the first considerations.
190|||The two criteria lead directly to the consequence of staffing a ship the player cannot fill.
193|||Retain each price band as spoken. The source leaves gaps between the examples and supplies no currency label here.
196|||Cesare explains why a cheap small ship is useful even if the player's budget is tight.
199|||He recommends moving up to a medium ship after trade gives the player money to spare.
203|||Medium ships come with two or three masts in this explanation. The faster option comes with a staffing cost.
206|||Keep the five-hold maximum and the conditional advice about omitting the two combat rooms.
209|Want to open a route to a distant town? Add supply holds so you can stay at sea longer.|Add supply holds|Cesare ties extra supplies to the ability to reach more distant destinations.
212|||Taking on another faction is the condition in Cesare's advice to buy large ships.
215|||Cesare says to equip at least the flagship and names the two rooms it needs for combat.
218|||The budget comparison preserves the combined cost and cargo capacity of two medium ships against one large ship.
221|You'll want to switch to large ships eventually. If you plan to form regional fleets, hang on to your old medium ships.|regional fleets,|Cesare distinguishes an eventual upgrade from the option of keeping older ships for regional fleets.
224|||Cesare finishes his own advice and uses the same preparation and farewell as on the refusal path.
""",
    178: """
11|||Fernando insists that now the visitor is here, he should give the game a try.
16|||Fernando notices a new face and proposes exactly one drink as the wager, then makes the game sound easy.
20|||The rules identify turn-taking and each permitted number of coins.
24|||The player who takes the last coin loses. The casual question invites the player into the game.
356_0|||The first native choice clearly accepts the one-drink wager and the game.
356_1|||The second native choice politely turns down the invitation.
52|Here you are buying me a drink again. I almost feel bad. Well, don't mind if I do. Ah, that's good!|I almost feel bad.;Ah, that's good!|Fernando teases the repeat loser, then accepts and enjoys the drink.
64|Remember, FI? Always leave them a multiple of four plus one. That's how you win.|a multiple of four plus one.;That's how you win.|Janus refers back to the exact one-more-than-a-multiple-of-four strategy and uses the original given-name substitution. Keep the arithmetic in one phrase.
67|||Rafael acknowledges Janus's reminder and admits the mistake with a little embarrassment.
75|Heh. If I see you again, I'll give you another game. Thanks for the drink.|Thanks for the drink.|Fernando leaves the rematch open and thanks Rafael before parting.
79|||Fernando ascribes the result to bad luck and claims the drink succinctly.
89|||Claudio calls Rafael by his substituted name, resents the loss and wants an immediate rematch.
93|||Rafael slows Claudio down because Fernando looks like a capable gambler.
97|||Fernando admits his confidence and dismisses luck alone as a complete explanation.
100|||Janus repeats the last idea and audibly realizes there may be a strategy.
103|||Claudio asks what Janus has noticed so the explanation can start.
107|||Keep the given-name token and Janus's excitement that he may have discovered a winning strategy.
111|||Rafael's quick response conveys surprise and draws the explanation forward.
116|||Janus tells Rafael which total to leave the opponent and why that eventually forces them to take the last coin.
120|||Rafael admits he is not following so Claudio can ask for a simpler version.
124|||Claudio asks for plain language without disputing the advice itself.
127|All right, let's try an example. Say there are five coins left and your opponent takes one. What would you do?|five coins left;What would you do?|Janus gives the exact five-coin setup and asks Rafael to supply a legal answer.
131|||Rafael correctly subtracts one from five and says he would take three of the four remaining coins.
136|||Janus resets the five-coin example and changes only the opponent's move to two.
139|||Rafael says he would take two, then sees why the opponent must face five coins.
143|||Janus gives a brief confirmation once Rafael reaches the answer.
147|||Rafael reasons through the nine-coin example aloud. Keep its explicit one-plus-four-plus-four breakdown and the result of leaving five.
151|||Janus addresses the admiral and credits him with catching on quickly.
155|||Claudio protests that he lost the thread while the other two worked it out.
158|||Janus needles Claudio by name after the explanation. The question fits the familiar exchange.
161|Shut up! You two went and figured it out without me. That's what bugs me!|without me.;That's what bugs me!|Claudio resents the other two sharing an understanding he was left out of.
168|||Fernando enjoys the free drink and offers another game whenever the group feels like it.
181|||Fernando concedes after the unfamiliar experience of losing, then offers the agreed drink.
192|||Rafael passes on the drink in this branch and probes Fernando's claim that he rarely loses.
196|||Fernando names both qualities he says matter, setting up his claim to possess them.
199|||The boast that he was born to gamble follows directly from claiming both insight and luck.
203|I couldn't say how lucky you are. Can you really read people that well?|read people that well?|Rafael questions the particular skill he is about to watch Fernando demonstrate.
207|||Fernando cautions against judging people by their outward appearance before giving an example.
211|||Fernando points out the couple and notes that their voices cannot be heard. His question asks Rafael to infer what they're saying.
214|They're talking about how much they love each other, aren't they?|aren't they?|Rafael guesses romantic talk. His assumption is exactly what Fernando is about to overturn.
218|||Fernando treats the example as basic and correctly identifies the breakup conversation.
222|||Rafael's puzzled reaction invites Fernando to let the couple demonstrate it.
227|||Fernando simply tells Rafael to watch before their words come into focus.
231|||The woman has heard enough, rejects his attitude, and accuses him of selfishness. Her generic nameplate remains appropriate.
234|||The man returns the accusation in direct language. The matching nameplate adds no information about the relationship.
237|||She reacts coolly and proposes that they stop seeing each other. The breakup confirms a relationship without establishing marriage.
240|||He agrees that the relationship is over if they both feel the same way.
243|...||Rafael's wordless reaction after the breakup uses the surrounding dialogue's ellipsis glyphs.
248|||Fernando asks for acknowledgment after the couple confirms his read.
252|||Rafael is impressed and asks how he figured it out.
257|||Fernando points to her clenched fist under the table, gives his inference, and contrasts it with romantic talk.
261|||He adds that the man never once looked at her and frames it as a question Rafael can answer.
265|That's amazing! You noticed all of that?|You noticed all of that?|Rafael's second reaction expresses surprise at how much detail Fernando saw.
269|||Fernando explicitly connects reading those signs to anticipating an opponent's moves.
272|||He adds his self-proclaimed luck to his observational skill as the second reason he wins.
275|||Rafael promptly invites Fernando aboard and says how valuable the skill would be.
279|Whoa. Where'd that come from?||Fernando reacts to the abrupt invitation before deciding what would persuade him.
283|Well, I've got time on my hands. I'll flip this coin. Heads, and I'll come with you.|time on my hands.;I'll come with you.|Fernando explains why he might go and puts his decision to a coin toss with the stated heads condition.
289|||Rafael turns down the offered drink and presses the recruitment invitation in this variant.
294|||Fernando recognizes the repeated request and theatrically asks the coin to decide again.
320|||The losing flip prompts Fernando to decline. He connects bad luck to whether he would entrust his life to Rafael.
336|||The winning flip leads directly to Fernando accepting and framing the decision as a wager of his life.
339|Name's Fernando Dias! Chalk it up to luck!|Fernando Dias!;Chalk it up to luck!|Fernando introduces himself with the approved surname and calls the turn of events another instance of luck.
342|||Rafael's brief welcome lets Fernando's stronger introduction close the recruitment beat.
357|||Fernando's irritated complaint about business or gambling being slow fits this short alternative without naming a specific loss.
""",
    179: """
5|||Manuel studies the ship and comments on its good upkeep before suggesting improvements.
8|||His observation that the ship needs a little work trails off as the others approach.
11|Huh? Is something wrong with our ship?|with our ship?|Rafael is puzzled by the unsolicited inspection and asks whether Manuel sees a problem.
16|Can we help you with something?||Janus courteously asks why Manuel has taken an interest in the ship they just identified as theirs in the preceding question.
20|||Manuel asks whether they own it and calls it a fine, lively ship, prompting Janus's reaction.
24|||Janus privately marks the unusual phrasing without explaining away Manuel's philosophy.
27|||Manuel urges ongoing care and says a ship will return it in service, then calls it a living thing.
30|...||Rafael pauses after Manuel's unusual claim. Keep the silence with an ASCII ellipsis.
35|||Manuel suspects he has overstepped, explains that it is his own belief and apologizes before taking his leave.
38|||Janus stammers and asks him to wait, suddenly more interested in the stranger.
42|What is it?||Manuel simply asks why he has been stopped, leaving Janus room to explain.
46|Well... You seem awfully fond of ships. I was curious.|I was curious.|Janus expresses his interest indirectly, without demanding an explanation from someone he has just met.
50|||A ship brings back memories for Manuel. He introduces himself by given name and says he used to be a navigator.
54|||Rafael's quiet acknowledgment lets Janus turn to him about the recruitment idea.
59|||Janus calls Rafael by the given-name substitution and leaves the idea of having Manuel aboard hanging a beat.
62|||Rafael agrees and backs the idea for the practical reason that Manuel would care for the ship.
67|||Janus asks Manuel directly and respectfully to join their crew and sail with them.
71|Back to sea again... I can see how much you love it. It stirs something in me, too.|It stirs something|Manuel is moved by their enthusiasm for the sea and hears the prospect as a return to a life he knew.
75|||Rafael hears the apparent change in Manuel and asks if he will accept.
80|||Manuel's image of a ship's heartbeat preserves his character. He catches himself and explains how long it has been since he sailed.
84|||He accepts warmly and thanks the group for offering him a place aboard.
87|||Manuel addresses the admiral and introduces the optional flagship room-refitting advice.
1452_0|||The first caption is a courteous acceptance of Manuel's exact offer.
1452_1|||The second caption is a polite refusal suited to the relationship and its branch.
102|||Manuel opens the accepted lesson by explaining that these are rooms for long voyages.
106|||Keep both rooms, the Speech stat and the effect on crew discontent. Manuel's recommendation applies to whoever is assigned there.
110|||The assigned people in the Galley and Nursery reduce consumption of water and food. Keep the two resources explicit.
114|||The Surgeon in Sickbay treats the three named conditions in both groups of crew members.
118|||Keep the recommendation to assign a sick or injured navigator to one of the two named rooms for faster recovery.
122|A shipwright like me can repair the ship at sea from the Lumber Room. We also help with refits and repairs at the shipyard.|from the Lumber Room.;refits and repairs;at the shipyard.|Manuel distinguishes repair at sea through the assigned room from a shipwright's two kinds of work at the shipyard.
125|||Manuel admits the explanation was quick and asks if it helped.
128|||He connects the fleet's fate to the admiral's decisions and urges careful planning of refits.
134|Very well. I'll leave it to you.||On the refusal path Manuel acknowledges the choice and leaves the decisions in the admiral's hands. Keep the acknowledgment and the courtesy on one line.
""",
}


def from_choices(group):
    entries = [line.split("|", 3) for line in DECISIONS[group["block"]].strip().splitlines()]
    for row, (key, replacement, protected, note) in zip(group["records"], entries, strict=True):
        choice = row["selector"] is None
        lookup = row["id"].split("CHOICE_", 1)[1] if choice else str(int(row["id"][-4:]))
        assert key == lookup
        old = " ".join(row["current_English"].split())
        english = replacement or old
        phrases = protected.split(";") if protected else []
        assert note and row["earlier_source_meaning"] and all(p in english for p in phrases)
        yield row | dict(previous_English=old, english=english, protected_phrases=phrases, localization_note=note,
            decision="revision" if english != old else "retention",
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False))


def normalize(row, names):
    selector = row["selector"]
    choice, system = selector is None, selector == 254
    speaker = "Player choice" if choice else "System panel" if system else names[selector]
    assert TOKEN.findall(row["english"]) == TOKEN.findall(row["previous_English"]) == TOKEN.findall(row["Japanese"])
    classification = "retention"
    if row["decision"] == "revision":
        classification = "glyph" if row["previous_English"] == "…" and row["english"] == "..." else "wording"
    ident = row["id"]
    if ident in WRAPS:
        assert classification == "retention"
        terms, note = WRAPS[ident]
        assert all(term in row["english"] for term in terms)
        row = row | dict(decision="revision", protected_phrases=terms, prose_retention_reason=row["localization_note"],
                         localization_note=note)
        classification = "wrap-only"
    if ident == "DK4_MES_B180_R0089":
        row = row | dict(decision="revision", english="An upper sail is called a topsail. It's a small square sail set high on each mast.",
            protected_phrases=["called a topsail.", "small square sail"],
            localization_note="Name and describe the topsail in two complete thoughts. Its name and small square shape stay together.")
        classification = "wording"
    prefix = "" if choice else f"{selector:02x}"
    source, current = [prefix + row[key + "_reference"]["exact_body_hex"] for key in ("source", "current")]
    return row | dict(route=0, source_selector=selector, native_slots=row["slots"],
        source_hex=source, current_hex=current, speaker=speaker, context=row["earlier_context"],
        source_meaning=row["earlier_source_meaning"], finding=row["localization_note"], change_class=classification,
        kind="typed-choice-label" if choice else "system-FE" if system else "progressive")


def main():
    packet, lesson, release = map(base.load, (paired.PAIRED, tutorial.OUTPUT, paired.parent.RELEASE))
    assert packet["candidate_sha256"] == lesson["candidate_sha256"] == base.digest(paired.parent.ROM)
    assert packet["release_proof_sha256"] == base.digest(paired.parent.RELEASE)
    assert lesson["paired_source_sha256"] == base.digest(paired.PAIRED)
    names = {r["actor_ID"]: r["progressive_nameplate"]
             for r in base.load(prior.CATALOGUE)["source_and_current_default_name_fields"]}
    records = []
    for group in packet["groups"]:
        if group["block"] == 180:
            drafts = lesson["records"]
            for source, draft in zip(group["records"], drafts, strict=True):
                assert all(draft[k] == value for k, value in source.items())
        else:
            drafts = from_choices(group)
        records.extend(normalize(row, names) for row in drafts)
    assert len(records) == 183 and sum(r["kind"] == "typed-choice-label" for r in records) == 8
    assert len({r["id"] for r in records}) == len(records)
    assert not OUTPUT.exists()
    counts = Counter(row["change_class"] for row in records)
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=["source", "context", "localization", "naturalness", "formatting"],
        previous_sha256=packet["candidate_sha256"], previous_registry_sha256=release["registry_sha256"],
        source_packet=str(paired.PAIRED), source_packet_sha256=base.digest(paired.PAIRED),
        earlier_glosses=str(paired.EARLIER), earlier_glosses_sha256=base.digest(paired.EARLIER),
        records=records, findings=dict(counts), new_editorial_credit=0,
        status="Contextual review complete. Stored formatting, gameplay and release checks pending."))
    print(f"Reviewed {len(records)} records. {dict(counts)}")


if __name__ == "__main__":
    main()
