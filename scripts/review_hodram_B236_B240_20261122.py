"""Review the sculptor's chisel, Papal States, letters, and archery rumor."""

from scripts import pair_hodram_B221_B240_20261122 as paired
from scripts import review_hodram_B230_B234_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = paired.base, paired.ROOT
OUTPUT = ROOT / "B236_B240_contextual_v1.json"
GLYPHS = {"DK4_MES_B237_R0005"}
CONTEXTS = {
    236: "A note from the Library of Alexandria gives Manuel a lead about Phidias's chisel. Hodram asks whether he wants it for ship repairs. Manuel jokes about the tools of Roman statecraft and says ships deserve fine tools too.",
    237: "Carlo meets Filippo and exchanges affectionate barbs with him. Filippo recalls his great-grandfather's story about trade in the Papal States. What starts as nostalgia ends with Carlo suggesting an item lead.",
    238: "Charles writes from West Africa to relate the story of a convoy somehow emboldened by a roar before the Spanish navy came by. His interest is in what the sound might have been. Hodram is skeptical but notes the crew's reaction.",
    239: "Jam writes a breezy letter from India about a Gupta statue rumored to see the future. He thinks of beating Fernando at gambling. Fernando scoffs and Hodram humors the lead after criticizing Jam's writing.",
    240: "Cesare is angry that the sailors are discussing a legendary arrow instead of tending the ship. He tells Hodram what they said about the arrow and its possible locations while insisting they would do better by practicing.",
}
DECISIONS = {
    236: """
5|Admiral, may I have a moment?|may I have a moment?|Manuel politely asks for time to tell Hodram about his discovery.
8|||Hodram acknowledges the request and lets Manuel continue.
12|The other day I found an interesting scrap of paper in the library at Alexandria.|scrap of paper;in the library at Alexandria.|Manuel names the time, place and piece of paper he found.
16|A scrap of paper?|A scrap of paper?|Hodram repeats the same object Manuel named, leaving the writing to the explanation that follows.
20|It tells of a strange chisel supposedly used by Phidias, the legendary sculptor of ancient Greece.|a strange chisel;used by Phidias,;of ancient Greece.|Manuel reports the note's claim and keeps the unusual quality of the tool.
23|||Hodram acknowledges the chisel with a short, questioning echo.
27|They say his spirit passed into the chisel when he died. Whoever uses it is supposed to be able to sculpt with miraculous skill.|his spirit passed;when he died.;with miraculous skill.|Manuel recounts the belief about Phidias's soul and the ability ascribed to the tool.
30|||Manuel keeps the supposed burial near Greece on the Balkan Peninsula and notes that the paper gives no exact place.
33|||Hodram asks if Manuel wants the tool for ship repairs. His practical question sets up Manuel's joke.
37|||Manuel's joke uses the literal tools of statecraft to praise an extravagant tool collection. The Roman comparison is his.
40|||Manuel treats shipbuilding as an art and suggests looking for the chisel if an opportunity comes along.
""",
    237: """
5|.........||Use ordinary English punctuation for the unusually long pause while Filippo is lost in thought.
9|||Carlo says Filippo's name and asks why he is distracted, beginning the exchange with familiar concern.
12|Huh? Oh... Carlo! It really is you! When'd you get back?|It really is you!;When'd you get back?|Filippo comes out of his reverie, recognizes Carlo in stages and asks when he returned.
16|I just stopped by on business. Filippo, you'll scare off your customers if you go around looking that vacant.|stopped by on business.;scare off your customers;looking that vacant.|Carlo says he is only visiting on business and teases Filippo about his vacant expression.
19|Mind your own business! Listen to you giving me a hard time again. You must be back to your old self.|giving me a hard time;back to your old self.|Filippo answers the jab and takes it as a sign that Carlo has recovered his old spirit.
23|||Carlo confirms he is back in action and says he is sailing aboard the group's ship.
26|Oh, customers! Sorry about that. I was off in my own world, thinking about a story my great-grandfather told me.|Sorry about that.;off in my own world,;my great-grandfather told me.|Filippo apologizes to the company and tells them why he was distracted. The family relationship is explicit in his speech.
29|||Carlo asks to hear the story, keeping the subject on Filippo's recollection.
33|||Filippo names the trade and says the pope once ruled directly over territory approaching Venice.
37|||Carlo recognizes the account and connects the old trade with the height of papal power.
40|That's right. The lords tried to outdo each other in what they gave the pope and how much of it they gave...|outdo each other;what they gave the pope|Filippo recalls lords competing in both the kinds and quantities of gifts.
43|||Filippo says his ancestors could profit from moving goods between others. His trailing turn invites Carlo to explain the later change.
47|||Carlo describes the decline of papal power and the drying up of trade with the Church.
51|That's right. Now we're back to making a living by our own efforts. I envy my great-grandfather and his lot.|making a living;my great-grandfather and his lot.|Filippo contrasts the present with the easier trade of his great-grandfather's generation.
54|||Carlo remembers stories about papal items turning up in places once under the pope's rule.
57|||Filippo jokes that an item used by the pope might carry a blessing. His own wish for help from above stays playful.
60|||Carlo echoes the thought before taking it seriously as a possible discovery.
64|Admiral, there may be something to this after all. If we found something a pope once treasured, it would be quite a discovery.|something to this after all.;a pope once treasured,;quite a discovery.|Carlo considers what it would mean to discover an object favored by a pope. The lead stays conditional.
""",
    238: """
SC1_B238_STYLE_8_0|||The plain voice announces Charles's letter and addresses the admiral directly.
SC1_B238_STYLE_8_42|Admiral, correspondence has arrived from Charles.|correspondence has arrived;from Charles.|The formal announcement uses the register already established for the same delivery type.
SC1_B238_STYLE_8_84|Admiral, you've got a letter from Charles.|you've got a letter;from Charles.|The relaxed voice reports the same event in ordinary speech.
SC1_B238_STYLE_8_122|||The courteous announcement gives the recipient and sender before the appended form of address.
SC1_B238_STYLE_8_164|Got a letter from Charles for you, Admiral.|Got a letter;for you, Admiral.|Use the brisk announcement found in Ian's corresponding crew voice.
SC1_B238_STYLE_8_202|Admiral, there's a letter here from Charles.|there's a letter here;from Charles.|Here gives the direct announcement an immediacy that suits its voice.
SC1_B238_STYLE_8_240|||Two short exclamations distinguish the eager voice without assigning an actor.
27|||Charles tells the admiral where he is and attributes the strange story to sailors there.
31|||The letter relates a recent pirate attack on a Spanish convoy traveling from the New World to West Africa.
35|The convoy was badly outmatched. The merchant ships tried to flee, but the pirates were faster. It was only a matter of time before they lost the whole convoy.|badly outmatched.;tried to flee,;the pirates were faster.;the whole convoy.|Charles spells out the closing danger caused by the pirates' superior speed and strength.
38|||The report gives the waters far west of Lisbon and the sailors' description of an unearthly roar.
41|||Charles says the sound somehow rallied the sailors. Fighting like lions preserves the source idiom's force without explaining the sound.
44|||Charles reports that the sailors held out until the Spanish navy passed by chance, scattering the pirates and letting the convoy escape.
47|No one has identified the sound yet. We don't know if it was a natural phenomenon that science could explain.|identified the sound yet.;a natural phenomenon;science could explain.|Charles leaves the roar unexplained and raises the scientific possibility without presuming it.
50|||Charles finds the story intriguing and proposes investigating. The approved full signature has its own row.
57|Sounds far-fetched... Still, I'm curious about the way it rallied the crew.|Sounds far-fetched...;rallied the crew.|Hodram doubts the report but takes interest in the sailors' reaction.
""",
    239: """
SC1_B239_STYLE_8_0|||The plain voice announces Jam's letter with the established address.
SC1_B239_STYLE_8_40|Admiral, correspondence has arrived from Jam.|correspondence has arrived;from Jam.|The formal voice uses the established wording and substitutes this sender.
SC1_B239_STYLE_8_80|Admiral, you've got a letter from Jam.|you've got a letter;from Jam.|The direct voice uses a contraction and keeps Jam as the sender.
SC1_B239_STYLE_8_116|||The courteous voice puts the letter first and the admiral's address last.
SC1_B239_STYLE_8_156|Got a letter from Jam for you, Admiral.|Got a letter;for you, Admiral.|The brisk fragment follows its pattern in the other letter announcements.
SC1_B239_STYLE_8_192|Admiral, there's a letter here from Jam.|there's a letter here;from Jam.|This familiar voice announces the presence of the letter with the same timing.
SC1_B239_STYLE_8_228|||The eager voice gives Jam's name in a short announcement after calling out to the admiral.
27|||Jam greets the admiral and asks about everyone. His letter sounds like his speech.
30|||Jam gushes about India, then remembers the rumor he meant to pass along. The sudden change of subject fits his voice.
33|It's about a statue of a sacred beast from the Gupta dynasty. They say the statue can see into the future.|a statue of a sacred beast;from the Gupta dynasty.;see into the future.|Jam relays the historical origin and the alleged power, which belongs to the rumor.
36|||Jam admits the story sounds fishy but says he could believe it in India. The enthusiasm stays his.
39|I figured with that thing I might finally beat Fernando at gambling. Getting ahead of myself, huh?|beat Fernando at gambling.;ahead of myself, huh?|Jam thinks about a personal use for the statue and questions his own optimism.
42|||Jam has found neither a seller nor a witness who has seen the statue. He has no exact lead.
46|Admiral, why not look for it if you've got some time? I mean, it might come in handy for more than gambling, right?|if you've got some time?;more than gambling, right?|Jam asks the admiral to look if free and improvises a reason beyond helping him gamble.
49|||Jam remembers he needs to sail, wishes the admiral luck and signs off with his approved full name on its own row.
64|||Fernando scoffs at the possibility of being beaten even with the statue. Keep the five-hundred-year exaggeration in his boast.
70|Heh. Can't that man write one ordinary letter? Well, he did take the trouble to report it. We may as well look into it.|one ordinary letter?;the trouble to report it.;look into it.|Hodram is amused by Jam's improvised letter but treats the effort as reason to look into the report.
""",
    240: """
5|Grr! What are those men going on about?|men going on about?|Cesare begins with an audible sign of irritation and immediately complains about the sailors.
8|||Hodram asks what has Cesare so angry, using his approved name.
11|||Cesare complains that the sailors are talking nonsense instead of working. His respectful form of address remains.
14|||Hodram prompts Cesare to explain by repeating the complaint.
18|They ought to be working! Demon-Piercing Arrow, indeed! Oh, that's what it's called, sir. Some name, isn't it?|They ought to be working!;Demon-Piercing Arrow, indeed!;Some name, isn't it?|Cesare blurts out the item name, backtracks to identify it and mocks it. Preserve the exact approved name.
21|||Hodram says he cannot follow the complaint and asks what the named item is.
24|||Cesare reports the legend of an angel using the arrow against a demon. The formal address keeps his delivery distinct.
28|They say it makes you a master archer. So the sailors wonder if it works for cannons, too. All this talk, and nobody's tending the ship!|makes you a master archer.;works for cannons, too.;tending the ship!|Cesare differentiates what the legend claims from what the sailors speculate. The neglected work is why he is angry.
31|||Cesare says cannon practice would do the sailors more good than their chatter. The complaint stays his.
35|||Cesare doubts the arrow would be lying near Britain and names the separate rumors about Skye and Lewis.
38|They get so worked up over silly rumors! If it were that close, surely someone would have it by now!|worked up over silly rumors!;someone would have it by now!|Cesare complains about their excitement and reasons that someone would already possess the arrow if it were nearby.
41|||Hodram pauses and thinks it would be pointless to interrupt Cesare. The parenthesis keeps the thought private.
44|||Cesare continues complaining, then the repeated grumbling trails off. The short written sound keeps the comic ending.
""",
}

review = checked_text(previous.review, {"len(records) == 72": "len(records) == 75"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::chisel-trade-letters-and-archery", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
