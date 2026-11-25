"""Review the Black Sea settlement, the royal summons, and Emilio's introduction."""

from types import SimpleNamespace

from scripts import pair_hodram_next_20261122 as intake
from scripts import register_hodram_B71_B80_20261122 as parent
from scripts import review_hodram_B71_B74_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = previous.base, previous.ROOT
paired = SimpleNamespace(PACKET=ROOT / "B81_B90_exact_current.json", CARRY=ROOT / "B81_B90_carried_decisions.json")
OUTPUT = ROOT / "B81_B84_contextual_v2.json"
GLYPHS = {"DK4_MES_B81_R0047", "DK4_MES_B82_R0041"}
CONTEXTS = {
    81: "Sera returns home to the Black Sea. Gerhard wonders how the legend traveled and Hodram cautions him against prying. Sirwood is helping rebuild, and Hodram offers to help the settlement defend itself.",
    82: "Hodram delivers the promised firearms. Sera interprets for Sirwood, who takes them to see the new building. Gerhard and Hodram discuss investment, and Hodram offers the first contribution.",
    83: "The port worker delivers the king's summons in two alternate greetings. The familiarity varies and the person doing the summoning stays the same.",
    84: "A bullfight draws a lively crowd. Gerhard explains the roles and assumes Hodram wants the star performer. Hodram approaches Emilio instead. The conversation pivots from Emilio's fear of sailing to the prospect of feasts.",
}
DECISIONS = {
    81: """
5|||Sera recognizes her own home. The simple wording and pause suit her return.
9|||Hodram acknowledges it quietly before Gerhard raises his question.
13|Still, I don't understand. How did the legend of the Indian Ocean's Proof of Conquest reach this place?|I don't understand.;Proof of Conquest;reach this place?|Gerhard is puzzled that the legend of the specific Indian Ocean proof is known here. The revised question carries the complete name.
17|||Gerhard points to the great distance from the Indian Ocean to the Black Sea. The existing line keeps both places and the reason for his doubt.
20|||Hodram concedes the point when Gerhard puts it that way. The unfinished thought leaves the question open.
24|||Sera is puzzled. The ordinary question glyph is already consistent with English speech.
28|Looks like she can't tell us.|Looks like she can't tell us.|Hodram concludes Sera is unlikely to know the answer. The colloquial qualification stays in his voice.
31|It's the legend that puzzles me. Maybe her people came from somewhere around the Indian Ocean...|the legend that puzzles me.;around the Indian Ocean...|Gerhard offers a possibility about the group's origins, based on the legend. His uncertainty is important to Hodram's next answer.
35|||Hodram calls it only a possibility and tells Gerhard against probing out of curiosity. The direct admonition fits the exchange.
39|||Sirwood's greeting remains in the original untranslated symbols, with the sequence and punctuation unchanged.
47|FI...|FI...|Sera addresses Hodram by his given name and pauses. Use the usual English ellipsis with the substituted name.
54|There's still so little here. It'll take time for this town to grow.|so little here.;for this town to grow.|Gerhard sees that little is built and expects development to take time. He does not declare the site empty.
57|||Hodram points to the limited population and money. The existing wording explains why progress is slow without faulting the people.
60|Even so, they're terribly exposed. If the Ottomans attack again, this place won't stand a chance.|terribly exposed.;the Ottomans attack again,;won't stand a chance.|Gerhard argues the settlement is vulnerable to another Ottoman attack. His warning is conditional.
64|||Hodram concedes the point, makes defense the first priority and suggests starting with firearms. The wording keeps the step provisional.
68|||Sera tells Hodram he does not have to do so much. The given name and pause carry her hesitance.
71|||Hodram calls this Sera's homeland, warns against losing it again, and says that weapons are needed for self-defense. His plain wording keeps the warning serious.
75|||Hodram considers five cargo holds' worth. Preserve the exact quantity and unit and the pause as he thinks.
78|||Sirwood's reply keeps the original circle and crosses and the trailing pause. It stays unintelligible to Hodram.
82|Don't worry. We're with you. Keep at it and build your town.|We're with you.;build your town.|Hodram assures the group of support and encourages them to keep building. They remain responsible for their own town.
""",
    82: """
5|||Sirwood greets them with another exact untranslated sequence. Preserve the symbols and exclamation.
9|||Hodram says he brought the firearms and thinks they will help the settlement defend itself. The qualification fits what he can promise.
12|||Sirwood gives an opaque response which Sera interprets in the next line. Keep all five symbols in order.
16|||Sera addresses Hodram by his given name, relays that Sirwood wants them to follow, and asks if he is willing.
20|||Hodram agrees and wants to know what Sirwood is taking them to see. The slight hesitation fits.
24|||Sirwood signals them again in his own language. The preceding ellipsis and the two symbols stay intact.
28|||Sera points out the destination using one word. The pause fits her economical speech.
32|||Hodram admires the building and acknowledges their effort. The existing compliment follows the reveal.
35|You could almost call it a palace. They might even attract military investment here.|call it a palace.;military investment here.|Gerhard says the building is nearly a palace and could serve to draw military investment. He does not rename it or promise money.
38|||Hodram says investment could help the town develop. The brief, conditional conclusion reads naturally.
41|FI...|FI...|Sera says only his given name and trails off. Use the usual English ellipsis with the substitution.
45|I'll make the first investment. You could put it toward building a trade house.|make the first investment.;building a trade house.|Hodram offers to invest first and suggests a trade house as a possible use. Match the established two-word term.
""",
    83: """
12|||In this version the port worker confirms the runtime surname and identifies the king of Sweden. His casual delivery fits the source.
18|||The second version is a welcome back and a summons from the king. It keeps the surname and speaks more familiarly without inventing a new rank.
""",
    84: """
5|||Charles notices the posted notice and asks about it. The brief question brings Gerhard's reaction forward.
9|||Gerhard asks about the poster and recognizes the bullfight himself. Keep the beat between the two reactions.
12|We've got the chance. Want to go see it?|Want to go see it?|Charles proposes taking the opportunity to see the bullfight, in a more spontaneous voice.
16|||Hodram comes upon a large crowd. The short exclamation suits his first impression.
20|||Charles is struck by the crowd's energy. The existing brief exclamation keeps his enthusiasm.
24|||Gerhard says Spain is the dominant power just now. The phrasing avoids reading his generalization as ownership of every country.
27|The poster says their most popular bullfighter is up today.|most popular bullfighter;is up today.|Charles credits the poster for the claim that the crowd favorite is appearing that day.
32|||A spectator laughs loudly as the performance begins. The existing regular English laugh suits the beat.
36|||The crowd calls for the performer to make them laugh again. Retain the taunt before Hodram asks which performer this is.
40|||Hodram assumes the man they are watching is the favorite and asks. The question gives Gerhard a reason to explain.
44|||Gerhard corrects his assumption and names the picador. Keep the recognized name of the role.
48||main attraction,;the finishing blow.|Gerhard explains the picador wears the bull down before the matador delivers the finishing blow. Keep the matador's description together through the wrap.
52|||Emilio cries out as he tries to handle the bull. Preserve the wordless shout and its intensity.
56|Ha ha ha! Look at that fool playing with the bull! Whoa! He threw it!|playing with the bull!;He threw it!|The spectator mocks Emilio at first, then reacts excitedly when he sends the bull flying.
60|||Emilio gives a different guttural shout. Keep it separate from the crowd's laughter.
64|||The spectator laughs again after Emilio's shout. The repeated laugh belongs to the crowd.
68|Get out of the ring already!|out of the ring already!|A spectator heckles the performer to leave. The bullring is established by the surrounding exchange.
76|||The trader announces that the headliner is finally entering. The two excited sentences fit the change of performer.
80|||The guildmaster reacts with a brief approving yell. Keep it as a crowd reaction.
84|||A spectator exclaims that the anticipated performer is finally here. The existing two words fit.
88|||The port worker cheers loudly. Retain the spoken cheer distinct from the later chant.
92|||Another spectator cheers along with the crowd. The uncomplicated exclamation reads naturally.
96|||The trader calls for a good performance. The short shout fits the crowd rather than a private conversation.
100|||A spectator shouts Bravo. The reaction suits the performance, with the original emphasis.
104|||The port worker joins the chorus. Keep the repeat as a separate speaker turn.
109|||The speakerless panel marks the restless murmur. The brief sound cue works without identifying an individual speaker.
113|...I think I'll ask him to join us.|ask him to join us.|Hodram considers inviting the man while leaving his identity unstated. That gives Gerhard room to assume he means the star.
117|||Gerhard questions whether Hodram is serious. The existing quick reaction hands the floor back.
121|||Hodram calls this sort of talent hard to find. The existing line keeps his assessment and the mistaken assumption intact.
125|||Gerhard doubts a bullfighter would help them. The original question still sounds like his reasoning through the offer.
129|||Hodram says yes without explaining who he means. Keep the short reply so the surprise plays on the next turns.
133|Got a moment?|Got a moment?|Hodram approaches the man he meant to recruit and asks for his attention.
137|||Emilio answers with a puzzled sound. The response gives Gerhard time to realize whom Hodram picked.
141|What?! ...You mean him?|You mean him?|Gerhard is flustered because Hodram chose the other man. The surprised question makes the reversal clear.
144|||Hodram invites Emilio to sail the open sea. The direct offer sets up Emilio's misunderstanding about food.
147|||Emilio sounds frightened of a ship and then says it does not sound tasty. The existing deadpan phrasing gives the joke room.
150|No, the ship won't taste good. But sail with us and you can feast on good food from all over the world.|the ship won't taste good.;feast on good food;all over the world.|Hodram plays along with the misunderstanding, then promises the prospect of good food from around the world if Emilio sails.
154|||Emilio catches the mention of good food. The stammer and chuckle keep his sudden interest audible.
158|That's right. There are all kinds of food out there.|all kinds of food|Hodram confirms the variety around the world after already naming the places broadly.
161|R-really? All kinds of food? Then I'll go! To sea, anywhere!|All kinds of food?;To sea, anywhere!|Emilio stumbles over his excitement and agrees he would even go to sea. The short last beat makes the comic switch clear.
169|||Emilio stammers before giving the full approved Emilio Ferog. Keep the uncertainty in his introduction.
173|||Hodram welcomes Emilio by his given name. The existing brief closing fits after the decision is made.
""",
}


def bind_packet():
    original = base.load(previous.paired.PACKET)
    original_receipt = base.load(previous.paired.CARRY)
    previous_release = base.load(parent.RELEASE)
    assert previous_release["predecessor"]["candidate_sha256"] == original["candidate_sha256"]
    assert original_receipt["source_packet_sha256"] == base.digest(previous.paired.PACKET)
    packet = intake.pairing.source_and_current(parent, range(81, 91))
    for before, current in zip(original["groups"][10:], packet["groups"], strict=True):
        assert (before["block"], before["source_block_sha256"], before["current_block_sha256"]) == (
            current["block"], current["source_block_sha256"], current["current_block_sha256"])
    assert sum(len(g["records"]) for g in packet["groups"]) == 306
    base.save(paired.PACKET, packet)
    carry = intake.pairing.prior_decisions(packet, paired.PACKET, intake.PACKAGES)
    assert len(carry["reused_records"]) == 9 and len(carry["pending_records"]) == 297
    base.save(paired.CARRY, carry)


review = checked_text(previous.review, {"len(records) == 41": "len(records) == 76"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::contextual-review", "exec"), scope)


if __name__ == "__main__":
    bind_packet()
    scope["main"]()
