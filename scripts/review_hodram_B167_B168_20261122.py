"""Review Cesare's ship tutorial and the recovery of the Elysion."""

from scripts import review_hodram_B164_B166_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B167_B168_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    167: "Hodram invites Cesare to join the crew and keep looking for his lost ship. Cesare offers a practical lesson on choosing ships. Hodram can hear the whole lesson or excuse him to make departure preparations.",
    168: "A tip near Lisbon leads Cesare to his beloved ship. He boards in excitement and startles Rafael's crew. They verify the carving before Cesare offers to leave the ship with them. Rafael gives it back, and Claudio reluctantly agrees.",
}
DECISIONS = {
    167: """
SC1_B167_CHOICE_1308_0|||Listen answers Cesare's offer directly and opens the optional ship lesson. It works alongside Skip as standard menu language.
SC1_B167_CHOICE_1308_1|||Skip clearly declines the optional advice without implying disagreement. Cesare then gets ready to sail.
""",
    168: """
5|||Cesare is still wondering where his ship has gone after all their searching. His possessive phrasing fits the affection he expressed when they met.
15|||Gerhard is worried because pirates usually take the gold and cargo and abandon the ship. His account suggests a likely outcome while leaving room for the new lead.
19|||Cesare is distressed by the thought that his ship was discarded. The halting response leaves space before the sailor interrupts.
23|||The sailor addresses Gerhard and relays a recent sighting near Lisbon. Keep the report secondhand and geographically limited.
27|||Gerhard's short exclamation marks his surprise at the tip. He has just described why recovering the ship would be unlikely.
31|What? The Elysion's somewhere near here?!|somewhere near here?!|Cesare repeats the ship's name and the possibility that it is close. His excitement makes the next search feel urgent.
34|||Gerhard proposes searching the harbor once. The separate command has a different entry condition from the repeat search below.
40|Let's search the harbor again.|search the harbor again.|Gerhard calls for a renewed search in the alternate path. Again keeps the player's earlier search meaningful.
46|||Cesare agrees straight away. His simple assent leaves the effort to the following scenes.
55|No luck. She's not here either...|not here either...|Cesare reports another failed search and trails off in disappointment. His attachment makes the feminine ship reference consistent with the discussion.
59|Don't lose heart. We'll find her someday.|Don't lose heart.;find her someday.|Gerhard offers Cesare reassurance after the empty search. It is a promise about trying again, in his measured voice.
70|||Charles offers to help look as well. The brief support belongs to him, apart from Gerhard's encouragement.
77|She ought to be somewhere nearby. Now it comes down to your luck. Keep your hopes up.|somewhere nearby.;comes down to your luck.|Gerhard reminds Cesare the ship should be close and leaves the remaining search to luck. Preserve the condition without making discovery certain.
81|||Cesare responds quietly after being encouraged. The pause retains his discouragement before the next attempt.
93|||Gerhard has seen nothing himself and asks whether Cesare had better luck. The question immediately triggers the garbled reaction.
96|||The original string of symbols represents Cesare's speechless shock. Preserve the source glyph sequence and existing punctuation so Gerhard can ask what happened.
100|||Gerhard cannot make sense of the symbols and asks Cesare what is wrong. Keep the question separate from his later guess.
104|||Cesare stammers the ship's name and repeats it when he recognizes her. Keep both calls, which alarm the crew aboard.
107|What's happened? Have you found her?|Have you found her?|Gerhard follows his first question with the guess that Cesare has finally found the Elysion. The pronoun refers to the same vessel as in the search.
118|Looks that way. He let out a yell and climbed right aboard...|let out a yell;climbed right aboard...|Charles thinks Cesare found her because he yelled and boarded. His observational tone leads into the agitated voices on the ship.
124|||Claudio reacts to a stranger suddenly boarding and wonders whether he is a thief. Preserve the embedded Claudio caption and stammer.
127|||Rafael repeats the possibility of a thief in surprise. Retain his separate embedded caption and the immediate echo.
130|||Cesare can only call out the ship's name. The embedded Cesare caption and exclamation keep his focus clear.
141|Well, this is getting out of hand...|getting out of hand...|Charles sees the commotion growing and observes it in his usual mild voice. His concern leads to Gerhard intervening.
147|||Gerhard realizes he needs to stop Cesare and calls to him. The short command keeps the urgency before the direct appeal.
150|Cesare! Easy now. Calm down!|Easy now.;Calm down!|Gerhard calls Cesare by name and repeats the instruction to steady him. He is no longer speaking about Cesare to Charles.
153|Oh... I'm sorry. The moment I saw the Elysion, my mind went blank...|saw the Elysion,;my mind went blank...|Cesare apologizes after calming down and explains that the sight overwhelmed him. The hesitation keeps the apology sincere.
157|What the heck is going on?|What the heck is going on?|Claudio brusquely asks who or what has interrupted them. The colloquial frustration distinguishes him from Rafael's next introduction.
161|||Rafael gives his name and identifies his company, then asks who the visitors are. The polite introduction follows Claudio's less welcoming reaction.
166|||Gerhard apologizes and gives his full name and the original company substitution. The reply mirrors Rafael's introduction at the proper register.
170|||Rafael recognizes the company after hearing its name. Leave his thought open and keep the same runtime company substitution.
174|||Gerhard formally introduces Cesare by his approved full name. The visitor gets an identity before the question about his conduct.
177|I'm sorry I lost my composure...|lost my composure...|Cesare repeats his apology to the ship's crew. The fuller sentence restores his courtesy now that he has calmed down.
181|||The crew member asks plainly why Cesare came aboard. The question lets Cesare give his side of the story.
185|This is the Elysion. She was my ship...|She was my ship...|Cesare identifies the ship before explaining that she once belonged to him. The pause makes it a difficult admission.
188|What are you talking about? This ship's ours!|ship's ours!|Claudio protests in plain speech. His certainty establishes the conflict without introducing a new claim to legal title.
191|Hang on, Claudio. He might be right.|Hang on, Claudio.;He might be right.|Rafael asks his familiar crewmate to pause and considers Cesare's claim. Using Claudio's familiar given name keeps the address natural.
195|We found her washed up on the beach. She'd been abandoned, remember?|washed up on the beach.;She'd been abandoned, remember?|Rafael reminds Claudio that the ship had been abandoned and had washed ashore. The question appeals to what they both know.
199|Even so... Does he have anything to prove it?|Even so...;anything to prove it?|The crewmate asks for evidence before accepting Cesare's account. Keep the polite hesitation.
202|Proof... Can you think of anything, Cesare?|think of anything, Cesare?|Gerhard turns the request for evidence over to Cesare. Addressing him by name makes that handoff clear.
206|||Cesare repeats the idea of proof, then remembers something. Keep the jump from hesitation to recognition.
209|||Cesare says he carved Good Luck into the side of the ship. The literal inscription matters to the next verification.
212|||The crew member asks Claudio to look at the side. The polite request makes Claudio's grumbling his own choice.
216|||Claudio objects at being picked to check the carving. His direct questions and trailing complaint lead to the admonition.
219|We need to know if he's telling the truth. A man doesn't do himself any favors griping over every little thing.|telling the truth.;every little thing.|The crewmate insists they verify the claim and chides Claudio for grumbling. The gendered rebuke belongs to the source speaker.
222|Tch... Fine. You don't go easy on people, do you?|Tch... Fine.;go easy on people, do you?|Claudio gives in while complaining that his crewmate works people hard. The tag keeps it as a grouse, apart from the instruction he follows.
225|I checked. I can't believe it. It's really carved into the side!|I can't believe it.;carved into the side!|Claudio confirms the carving after checking. His disbelief is a reaction to the evidence that overturns his earlier certainty.
228|Y-you found it?!|Y-you found it?!|Cesare stammers while asking if Claudio really saw the carving. His reaction marks how hard he finds it to believe the confirmation.
240|That's wonderful!|That's wonderful!|Charles celebrates the confirmation. Keep the congratulation general because it is the proof, not a new discovery by Charles.
247|||Gerhard congratulates Cesare in his own voice. The separate turn gives Cesare the chance to respond.
251|||Cesare can barely get out an answer. The stammer and pause fit his response now that the claim is proven.
255|||The crewmate starts to reckon with what the proof means for them. Leave the thought unfinished so Claudio can say what is at stake.
259|Ah, this is a mess... We can't get by without this ship now.|can't get by without;this ship now.|Claudio says the ship has become indispensable to their crew. His frustration acknowledges the proof while resisting its consequences.
263|You're right about that... What do you want to do, Cesare?|right about that...;What do you want to do, Cesare?|Gerhard concedes the crew's need and leaves the decision to Cesare. His question stays measured and direct.
266|||Cesare decides to leave rather than take the ship from another crew. He says seeing her again is enough after a long hesitation.
270|||Cesare asks the people aboard to take care of the ship. His request preserves both the hesitation and the ship's name.
281|||Charles quietly says Cesare's name in response to the gesture. The moment needs no added explanation.
288|Are you sure?|Are you sure?|Gerhard checks that Cesare is willing to walk away. The plain question gives the decision the weight it deserves.
292|||Cesare quietly confirms his decision. The pause gives Rafael room to call him back.
296|Wait... This is your ship, isn't it?|This is your ship, isn't it?|Rafael asks Cesare to acknowledge the claim now that it has been proven. His hesitation and tag keep the manner considerate.
300|||Cesare concedes he once owned her. His qualification follows the decision to leave the ship with them.
304|Then take the Elysion. Please.|take the Elysion.|Rafael offers the ship outright. His separate polite request matches the sincerity of the offer before Claudio's protest.
308|What are you saying? It's our ship! What are we supposed to do?|What are you saying?;What are we supposed to do?|Claudio objects to giving away a ship they need, emphasizing what it is and asking what will happen to the crew.
312|||Rafael says they will find a way and that he understands how Cesare feels. His appeal asks Claudio to agree to giving the ship back.
317|...You're too soft for your own good. All right.|too soft for your own good.;All right.|Claudio sighs at Rafael's generosity but agrees. His familiar reproach is affectionate in the context of yielding to him.
320|||Cesare can hardly believe he may take the ship. The stammer puts his disbelief ahead of his thanks.
324|Sure. We'll leave her tied up here at the dock.|leave her tied up;at the dock.|Rafael confirms the gift and says where they will leave the ship moored. His casual assurance answers Cesare's hesitation.
329|Th-thank you! I get to sail with the Elysion again!|Th-thank you!;the Elysion again!|Cesare stammers his thanks and celebrates voyaging with his ship again. The speech continues his habit of treating her as a companion.
341|||Charles shares Cesare's relief. Keep his short celebration separate from Gerhard's formal thanks.
348|You have my thanks as well. You're a generous man for someone so young.|my thanks as well.;for someone so young.|Gerhard thanks Rafael and remarks on how generous he is for his age. The comparison stays with the person singled out by the source.
351|||Rafael modestly tries to brush off the praise. The stammer makes space for Gerhard to go on.
356|||Gerhard tells him not to be modest and says he reminds him of his own admiral. The existing cloth idiom conveys an affinity without suggesting a relationship.
359|||Gerhard says he is honored to have met Rafael and bids him farewell. Preserve the polite given-name address.
363|||Cesare thanks Rafael's crew again in an emphatic final turn. The brief line closes the exchange.
""",
}
review = checked_text(previous.review, {"len(records) == 41": "len(records) == 76"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::cesare-and-the-elysion", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

