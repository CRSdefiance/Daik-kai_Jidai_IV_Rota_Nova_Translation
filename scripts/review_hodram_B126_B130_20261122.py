"""Review Rafael's knife, the sail tutorial, Diogo's claim, and Julio's request."""

from scripts import review_hodram_B120_B122_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B126_B130_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    126: "The discoverers are offered the knife. Rafael defers to Hodram, who wants him to receive credit. Claudio proposes a trade between the knife and the pay, and the party agrees.",
    127: "Hodram orders the fleet under way. The crew's questions and the original speakerless tutorial explain D-pad, stylus, sail angle and speed controls, then Gerhard talks about facing the Hanseatic League.",
    129: "Diogo claims control of New World trade on linked encounter paths. His derision gives way to his plan to break from Spain and become emperor. Hodram and Gerhard challenge his claim.",
    130: "Julio remembers Cristina and proposes bringing her along. Hodram learns she is Julio's granddaughter, an able swordswoman, and in London.",
}
DECISIONS = {
    126: """
6|||The speaker reacts to the discovery without naming the object immediately. The existing unfinished exclamation fits the scene.
10|||The speaker says the finders are entitled to keep the knife. The idiomatic causal phrasing does not change the ownership claim.
13|||Rafael defers to the captain identified by FI because he could not have found the object alone. Preserve both the controlled name and the humility.
17|We worked together to get this far. It wouldn't be fair to leave you out.|worked together;leave you out.|Hodram insists their cooperation earned Rafael recognition. He objects to leaving Rafael out before Claudio proposes how to divide the reward.
21|||Rafael's brief hesitation lets Claudio step in. Preserve his visible name separately from the captain-name substitution he just used.
26|How about this? You keep the knife, and we'll take the full pay for this job.|You keep the knife,;the full pay|Claudio suggests they give Hodram the knife and get all the pay in exchange. Both parts of the bargain are explicit.
29|||Rafael stammers in surprise at Claudio's intervention. Use Claudio's approved name and preserve the startled rhythm.
34|||Hodram checks whether the terms suit Rafael. The short question lets Rafael consider the offer.
38|What?! Of course I'd be grateful... Are you sure, though?|I'd be grateful...;Are you sure, though?|Rafael welcomes the offer but checks twice that Hodram means it. The full trailing question stays together.
43|||Hodram says they can earn more money and accepts the terms. The calm statement leaves room for Claudio's reaction.
46|Now that's what I call character! I'm impressed!|that's what I call character!;I'm impressed!|Claudio praises Hodram's good character in an approving and slightly showy burst. The source gives no preceding prediction about his choice.
49|||Rafael's grateful reply accepts the agreement. The direct thanks suit the moment.
60|||The speaker suggests heading back because the others in the fleet must be waiting. Keep the assumption expressed as must.
""",
    127: """
5|Raise anchor! Unfurl the sails!|Raise anchor!;Unfurl the sails!|Hodram orders both the anchor raised and the sails opened. The second order remains more specific than the general instruction to depart.
21|||Manuel asks the admiral for the heading. The seafaring term is idiomatic and introduces the steering help.
28|||The speakerless instruction names both supported steering methods. Keep the control names used elsewhere.
31|||This notice explains pressing the D-pad toward the desired heading or touching the screen. The actions remain distinct.
42|||Charles asks for sail-handling orders in addition to steering. His reminder leads into the trim instructions.
49|||The notice explains use of L and R to adjust sail angle and the benefit to speed.
53|||The next instruction gives the exact left and right button mapping. Preserve all four directions and controls.
57|||The notice explains automatic sail control while steering by stylus and how tapping the flagship stops the fleet.
61|||The tutorial explains how to read the speed bar and maximize its length. It gives a concrete display cue without adding a numerical value.
64|This time we'll crush those Hanseatic ships and teach Martin Speyer to stop underestimating us!|those Hanseatic ships;Martin Speyer;stop underestimating us!|Gerhard wants to defeat the Hanseatic ships and show Martin Speyer the cost of looking down on them. The naval taunt stays directed at the named opponent.
""",
    129: """
5|Well, well. Mr. FA.|Mr. FA.|Diogo recognizes Hodram by the protected surname and uses a formal address. The source honorific here provides no naval rank.
16|||Hodram asks what Diogo wants. His guarded opening suits a speaker who has been approached.
20|I'm afraid no one is allowed to trade in these waters. Leave at once.|in these waters.;Leave at once.|Diogo declares his ban applies to everyone and orders the crew to leave immediately.
24|||Hodram denies needing Diogo's permission to trade in the New World. His answer challenges the asserted authority.
27|||Diogo responds condescendingly before offering an explanation. The existing question fits the first path.
38|||Hodram asks what Diogo wants on the other encounter path. Keep the terse request separate.
42|||Diogo pretends he lent them the Caribbean and now wants it back. The English preserves his deliberately false premise.
45|||Hodram challenges the claim rather than accepting any loan. Keep the incredulous echo.
48|||Diogo savors the question before choosing to explain. The colloquial laugh carries the pause.
53|||Hodram finally names Diogo and calls out his true motives. Retain the approved full name.
56|||Hodram says Diogo used their forces to remove his old enemy Maldonado and suspects a larger plan. The conclusion remains Hodram's deduction.
60|||Diogo acknowledges Hodram's insight with a dismissive laugh and begins to explain.
69|We'll found a new empire independent of Spain. And I'll be its first emperor.|independent of Spain.;its first emperor.|Diogo announces a plan to form an independent empire and names himself as its future first emperor. The forceful delivery preserves his confidence.
73|||The wordless reaction follows Diogo's declaration. Leave the moment separate from his next claim.
77|The whole New World will belong to the new empire, along with all its trading rights. No one will be allowed to trade without our permission.|the new empire,;all its trading rights.;without our permission.|Diogo claims both territory and all trading rights for his empire. The ban on other trade depends on its permission.
80|||Hodram starts a short angry reply. His interrupted reaction stays distinct from Gerhard's next objection.
84|||Gerhard calls Diogo's assertion outrageous. The existing one-word rejection fits the change of speaker.
94|I've had enough of you. Get out of my sight!|I've had enough of you.;Get out of my sight!|Diogo dismisses their presence as an irritation and orders them away. The shared phrasing stays identical across the two matching source branches.
105|I am grateful you drove off that parasite Maldonado. That left me free to prepare for independence.|drove off that parasite;prepare for independence.|Diogo sneers at Maldonado while thanking them for driving him off. He explicitly links their help to his freedom to work on independence.
108|||Diogo abruptly says he has no further use for them. The terse order keeps the shock of his reversal.
119|So you mean to break away and crown yourself emperor? Ambitious. Boast before you've pulled it off and you might live to regret it.|crown yourself emperor?;live to regret it.|Hodram recognizes the scope of Diogo's ambition and warns him about boasting before achieving it. The future remains conditional.
127|I've had enough of you. Get out of my sight!|I've had enough of you.;Get out of my sight!|Diogo uses the same contemptuous dismissal in this route. Keep it identical to the corresponding source branch without collapsing the commands.
""",
    130: """
5|||Julio begins to remember something before identifying Cristina. The trailing phrase leaves Hodram room to react.
9|||Hodram's silent question keeps the exchange moving with a brief reaction.
13|Yes, that's it! Let's bring Cristina along.|Let's bring Cristina along.|Julio remembers Cristina and settles on bringing her along. The short burst sounds like an idea clicking into place.
16|||Hodram asks who Cristina is because Julio has only just named her.
20|||Julio identifies Cristina as his actual granddaughter and says she is skilled with a sword. The existing idiom keeps his pride and her ability.
23|||Hodram asks where she is now. The simple question follows the introduction.
27|||Julio names London as her present location. No further details are needed.
31|All right. Let's head to London.|head to London.|Hodram agrees to go to the place Julio has just named. His reply commits to the trip.
""",
}
review = checked_text(previous.review, {"len(records) == 51": "len(records) == 53"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::knife-sails-Diogo-and-Cristina", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

