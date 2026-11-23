"""Review Maria's Hangzhou invitation, bargain, rewards and warning."""

from types import SimpleNamespace

from scripts import pair_hodram_opening_20261122 as pairing
from scripts import review_hodram_B65_B70_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base = previous.base
ROOT = pairing.ROOT.with_name("hodram_B71_B90_followup_20261122")
paired = SimpleNamespace(PACKET=ROOT / "paired_source_registered_candidate.json",
                         CARRY=ROOT / "prior_contextual_decisions.json")
OUTPUT = ROOT / "B71_B74_contextual_v2.json"
GLYPHS = set()
CONTEXTS = {
    71: "A messenger tells Hodram that Admiral Maria Li expects him in Hangzhou. He does not know why she called him.",
    72: "Xien ushers Hodram in. Maria congratulates him and proposes he defeat the pirates threatening the coast. He needles her about manipulating him, then agrees because the offer serves him too.",
    73: "Maria congratulates Hodram and delivers the promised reward. In the separate acknowledgment she recognizes his command of these waters and offers the object.",
    74: "Maria mentions trouble in the Mediterranean and suggests Hodram return there after finding the treasure. He leaves the decision open.",
}
DECISIONS = {
    71: """
7|||The messenger respectfully calls the admiral by his runtime surname. His rank is already established.
11|||Hodram's initial puzzled reaction gives the messenger room to continue.
15|Admiral Maria Li is waiting for you in Hangzhou.|Admiral Maria Li;in Hangzhou.|The messenger identifies Maria by her rank and both names, then states where she is waiting.
18|||Hodram is puzzled by the summons. The existing normal question glyph fits the silent turn.
""",
    72: """
6|||Xien recognizes Hodram by surname, relays that Admiral Li wants to see him, and courteously leads the way.
10|||Maria says she heard he finally defeated Kuhn and congratulates him directly.
13|||Hodram's silence leaves Maria to read his face. Preserve the original standalone pause.
17|What's wrong? You don't look too pleased.|too pleased.|Maria notices his glum look and asks why, just after congratulating him.
21|What will you use me for this time?|use me for this time?|Hodram suspects another favor and asks with dry irritation.
25|||Maria calls him suspicious with feigned surprise. The existing phrasing fits her ease.
29|Well, let it go. We ended up with a foothold in Southeast Asia.|ended up with a foothold;in Southeast Asia.|Hodram brushes aside the accusation and acknowledges how things turned out for his own side.
33|So you're saying our interests lined up?|our interests lined up?|Maria asks if he means that both of their interests were served.
36|||Hodram allows the possibility in one word. The existing brevity fits his qualified answer.
40|||Maria is pleased to hear it and uses the opening to raise one more proposal. The current phrasing makes the transition smoothly.
44|||Hodram was expecting this and has no need to spell out his suspicion again.
48|Have you heard of the wako?|the wako?|Maria introduces the group term retained in the other route. Her explanation follows Hodram's puzzled reaction.
51|||Leave his simple question mark before Maria defines the term.
55|The Ming keep their ports closed, so they have no navy. Japanese pirates take advantage of that. They plunder the mainland coast. They're called wako.|keep their ports closed,;have no navy.;Japanese pirates;advantage of that.;They plunder the mainland coast.;They're called wako.|Maria links the Ming maritime restrictions to the lack of a navy in her account. She explains that Japanese pirates exploit it to plunder the mainland coast and names them.
58|||Maria names Sojin Kurushima as their leader and says protecting people from his raids was her reason for building a private fleet. The existing pause invites Hodram's conclusion.
62|||Hodram concludes that Maria wants him to defeat Kurushima and asks her to confirm it.
65|||Maria promises a reward and says she thinks something he wants is in Japan. The reward and the qualified hunch remain separate.
69|Something I'm looking for? Heh... You take me too lightly. What am I, your hunting dog?|Something I'm looking for?;You take me too lightly.;What am I, your hunting dog?|Hodram echoes her suggestion with a low laugh, says she is underestimating him, and compares her treatment of him to using a hunting dog.
73|That's a cynical way to see it. I'm offering you the right to trade with Japan.|That's a cynical way to see it.;the right to trade with Japan.|Maria recognizes his uncharitable interpretation and points to the commercial right she is offering.
77|||Hodram replies sarcastically to what he reads as condescension. The short thanks in the existing wording carries it.
81|...Would you rather pass?|Would you rather pass?|Maria pauses, then tests whether he means to turn her down. This is a question from Maria, with no player menu here.
85|I've come all the way to the eastern edge of the world. I mean to make something of it. But it doesn't have to be Japan.|the eastern edge of the world.;make something of it.;doesn't have to be Japan.|Hodram intends to have something to show for coming this far east. Japan need not be his target.
88|||Maria is willing to take him on if he wants a fight with her instead. The unhurried wording leaves the challenge implicit.
91|Confidence or a bluff? I'd love to know. But I have no quarrel with you for now. No need to get worked up.|Confidence or a bluff?;I'd love to know.;for now.;No need to get worked up.|Hodram is curious whether she means it, says he has no reason for a quarrel at present, and asks her to cool down.
94|||Maria's silence comes before he openly accepts the practical case for the offer.
98|||Hodram already knows accepting would benefit him most. The current account of his quick decision and self-interest reads naturally.
102|What a formidable woman... Now I know what it feels like to dance to someone else's tune.|What a formidable woman...;dance to someone else's tune.|Hodram recognizes how well she has steered him. Keep the idiom conveying that he is moving to her direction.
106|Listen. Sit back and watch. You won't have to lift a finger while I clear out those pirates.|Sit back and watch.;lift a finger;clear out those pirates.|He insists he will handle the pirates himself and tells Maria to stay out of it. Her response does not accept his instruction unconditionally.
110|||Maria lightly questions whether she really will sit out. Keep the teasing doubt.
114|With that fearless smile behind me, I can make all the bold speeches I want. How reassuring.|that fearless smile;all the bold speeches;How reassuring.|Hodram says that knowing her fearless smile is behind him makes it easy to boast. The last sentence retains the irony.
117|||Maria calls out his sarcasm without losing the conversational tone.
""",
    73: """
28|||Maria addresses him as admiral by surname and praises his work. The wording keeps both.
31|||Hodram is already angry and warns her not to go further. The pause and direct tone fit.
35|My apologies. Here's the reward I promised. Please take it.|the reward I promised.;Please take it.|Maria apologizes and explicitly hands over the promised reward. The instruction to accept it belongs in the English.
56|Looks like it's time I recognized you as master of these waters. Please take this.|master of these waters.;Please take this.|Maria says the time has come to acknowledge his control of this sea region, then offers the object.
""",
    74: """
58|The Ottomans are making troubling moves in the Mediterranean. Why not go back after you find that treasure?|troubling moves;in the Mediterranean.;you find that treasure?|Maria reports unsettling activity by the Ottoman Empire and makes her suggestion conditional on finding the treasure.
62|||Hodram acknowledges how well informed she is and says he will remember the advice. He makes no commitment to return right away.
""",
}

review = checked_text(previous.review, {
    'pending = {row["id"]: row for row in carry["pending_records"]}':
        'pending = {row["id"]: row for row in carry["pending_records"] if row["block"] in CONTEXTS}',
    "len(records) == 125": "len(records) == 41",
})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::contextual-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
