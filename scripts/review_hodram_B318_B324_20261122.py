"""Review the overseas guide, northern village, survey, and alchemy exchanges."""
from scripts import review_hodram_B316_B317_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text

base, ROOT = previous.base, previous.ROOT
OUTPUT = ROOT / "B318_B324_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    318: "The guide relocates the search to another island and has arranged a boat. On arrival the party can meet another searcher, Rafael, and eventually finds the ruins.",
    319: "A hostess passes on the story of the missing monk and asks the captain to inquire if he reaches the village.",
    320: "A village elder asks where Hodram comes from and offers a trade for his sextant.",
    321: "The elder receives the sextant and gives the promised item.",
    322: "The survey party goes ashore and receives funds. The sailor asks the captain to report to the Sofala guild.",
    323: "A speaker recognizes the purpose of the visit and entrusts the object to the visitors.",
    324: "A villager tells of the monk who saved the village and died. Charles recognizes the Alchemy Book, and Hodram promises to continue the search for the unknown ore.",
}
DECISIONS = {
    318: """
12|First, find the map to the ruins.|the map to the ruins.|The guide asks the party to obtain the map before they begin the search.
SC1_B318_STYLE_96_0|||The speaker can hardly believe an ancient city once stood in such a spot.
SC1_B318_STYLE_96_56|||The measured voice reflects on the city with an unfinished thought.
SC1_B318_STYLE_96_92|||The casual speaker realizes there really was an ancient city here.
SC1_B318_STYLE_96_128|||The crew member quietly marvels at finding an ancient city here.
SC1_B318_STYLE_96_166|||The rougher voice expresses surprise that an ancient city could once stand here.
SC1_B318_STYLE_96_208|||The older voice finds the former city hard to believe.
SC1_B318_STYLE_96_266|||The youthful speaker marvels that there used to be a town this far out.
SC1_B318_STYLE_96_310|||The formal crew member reflects on the vanished city in a thoughtful voice.
44|Well... According to the map, the ruins don't seem to be on this island.|According to the map,;don't seem to be;on this island.|The guide cautiously says the map puts the ruins off the current island.
48|||The captain reacts with surprise before hearing what travel is required.
54|||The guide says they will have to cross the sea.
59|||The captain reasons that they ought to return to port to do so.
63|||The guide has already arranged a small boat and plans to continue in it.
66|Only your party qualifies. Please keep the sailors from finding out where the ruins are.|Only your party qualifies.;finding out where the ruins are.|The guide restricts eligibility to the party and asks that the crew not learn the ruin's location.
75|One day passed.|One day passed.|Keep the exact one-day notice and use the same wording as the other expedition results.
79|We've arrived. We go on foot from here.|We go on foot from here.|The guide confirms arrival and says the rest of the journey will take place on land.
82|||The unexpected voice stammers in surprise before Hodram recognizes him.
94|||Hodram recognizes Rafael of the Castor Company and asks why he is here. Keep both approved names.
100|||Hodram asks the stranger who he is in the alternate introduction.
109|He asked me to look for the ruins. I got lost along the way...|look for the ruins.;lost along the way...|Rafael refers to the person with Hodram and admits he lost his way during the search.
114|So they asked you too. Anyone who looks strong enough, was it?|they asked you too.;was it?|Hodram recalls the earlier explanation that the request went to anyone who seemed suitable.
117|||The guide apologizes and says he accompanied the party once the people he asked stopped sending word.
121|||Rafael accepts the blame for his own failure and speaks modestly.
125|All right. We'll look for it together.|look for it together.|Hodram sees that working together can solve the problem and accepts the other searcher.
128|||The guide agrees in a short reply.
132|||Rafael agrees that they should search together.
136|||The guide bursts out that they have found the site he sought.
SC1_B318_STYLE_1420_0|||The polite crew member reports finding the ruins to the admiral.
SC1_B318_STYLE_1420_28|||The casual crew member cheerfully announces the find.
SC1_B318_STYLE_1420_54|||The crew member points out the ruins to the admiral.
SC1_B318_STYLE_1420_74|||The rough voice gives its tentative identification in plain language.
SC1_B318_STYLE_1420_104|||The older speaker says they appear to have found the ruins.
SC1_B318_STYLE_1420_134|||The youthful lookout recognizes the ruins in a direct statement.
SC1_B318_STYLE_1420_166|||The formal crew member gives a measured report about the discovery.
165|||Hodram responds that he is coming when called to the ruins.
""",
    319: """
5|||The hostess welcomes the captain warmly before asking about the village.
9|||She asks about a village far north in the New World. The casual phrasing fits her question.
13|A customer told me a respected monk from this town sailed to the northern continent long ago to spread his faith.|A customer told me;a respected monk;the northern continent;to spread his faith.|She attributes the story to a customer and preserves the monk's local origin, destination and purpose.
17|||She says the monk vanished after finding the village and wonders what happened.
21|||The captain cannot tell her what happened. The short reply suits his uncertainty.
25|I hear he was a man of great virtue. I hope the people where he went to preach have taken to him.|a man of great virtue.;went to preach;have taken to him.|She passes on the monk's reputation for virtue and hopes he has earned the affection of the people where he went.
28|||She asks the captain to inquire about the monk if he ever has a chance to travel north.
""",
    320: """
5|||The elder observes that the visitor is unfamiliar and politely asks where he is from.
8|||Hodram names Sweden and places it in northern Europe without added biography.
12|||The elder has never heard of Sweden and infers it must be very far away.
16|Ah, I see. You have one of those handy sextants, don't you?|those handy sextants, don't you?|The elder infers the travelers carry a sextant and asks a question to confirm it.
20|||Hodram's brief surprise gives the elder room to explain.
24|I've heard those things can tell you where you are at sea, even with no landmarks. Or something like that.|where you are at sea,;even with no landmarks.;Or something like that.|The elder describes the reported use of a sextant and keeps his uncertainty about the details.
28|||The elder asks for the sextant and offers something good in exchange without naming it yet.
31|||Hodram echoes the elder's promise in a question.
35|Bring it here and you'll find out.|you'll find out.|The elder keeps the exchange a surprise until the sextant arrives.
""",
    321: """
6|Ah, you brought it! Here, take this in exchange.|you brought it!;take this in exchange.|The elder recognizes the delivered sextant and gives the promised exchange item.
14|||The result notice uses the exact item label and records its handover.
""",
    322: """
SC1_B322_STYLE_8_0|||The polite voice announces that they will put the survey party ashore.
SC1_B322_STYLE_8_26|||The crew member announces the survey party is going ashore now.
SC1_B322_STYLE_8_48|||The rough crew member promptly names the group they will drop off.
SC1_B322_STYLE_8_70|||The older crew member calls for the survey party to go ashore.
SC1_B322_STYLE_8_90|||The youthful announcement keeps the name of the survey party clear.
SC1_B322_STYLE_8_112|||The formal crew member signals that the survey party is going ashore.
71|||The notice records the separate outcome in which all the current funds go to initial expenses.
76|||The other notice gives the survey party exactly 1,000 gold coins for initial expenses.
83|||The sailor announces the survey has commenced and asks for a report to the Sofala guild.
""",
    323: """
6|||The speaker asks if the object is what the visitors came to find.
10|After all this time... The day has finally come.|After all this time...;finally come.|This speaker reflects on the long wait and recognizes that it has ended.
13|||The speaker decides to trust the party and formally offers them the item.
""",
    324: """
5|||The villager is surprised the visitor knows the monk and asks about it.
9|||Hodram realizes the villager recognizes the monk and checks what he knows.
13|An illness swept through our village. He couldn't bear to see us suffer, so he stayed and nursed us. Without him, we'd all have died.|swept through our village.;see us suffer,;we'd all have died.|The villager remembers the epidemic, the monk's concern and devoted care, and says it spared the village from being wiped out.
16|His medicine cleared up the sickness almost at once. It was a miracle.|cleared up the sickness;almost at once.;It was a miracle.|The villager recalls how soon the illness receded after they took the monk's medicine and calls it a miracle.
20|||Hodram asks whether the monk knew medicine.
24|No, he called it alchemy. Something about getting rid of the poisonous minerals in our drinking water...|he called it alchemy.;the poisonous minerals;in our drinking water...|The villager reports the monk's own explanation as something only partly understood.
28|||The villager shows the book and says the same monk wrote it.
39|||The crew member recognizes something about the book and pauses in excitement.
58|||The crew member recognizes the book from Charles's description and celebrates.
65|||Charles blurts out the approved book title and stammers at finding it here.
69|||Hodram asks Charles what has made him react this way.
73|||Charles explains he had heard of a new material in the New World and believed it was relevant to his experiments.
77|||His investigation led him to the book as necessary to obtain the material. The sentence trails off into his speculation.
81|I'm sure it's a clue to some precious metal! Now if I could just work out how to use it... (muttering)|some precious metal!;how to use it...|Charles is sure the book is a clue to a valuable metal, then thinks aloud about how to use it.
84|||Hodram apologetically cuts off Charles's explanation to return to the villager.
90|||He asks where the monk is now, shifting attention from the book to its author.
94|||The villager's silence marks his reluctance before the revelation.
98|||The crew reaction gives the villager room to explain.
102|||The villager says the monk drank the local water and developed the same illness.
105|Even then, he kept his illness secret and gave every bit of medicine he made to the people here!|kept his illness secret;every bit of medicine;the people here!|The villager explains that the monk hid his illness and gave all his medicine to the villagers.
109|And in the end, he passed away... That man truly was a messenger of God.|he passed away...;a messenger of God.|The villager reluctantly reports the monk's death and expresses his religious gratitude.
112|||The silent reaction gives the death time to register.
116|||The villager hesitantly asks the group to take responsibility for the book.
119|||Hodram echoes the request as a question before the villager explains.
123|||The villager says the book holds the secret of an ore nobody has seen before.
126|||The villager thinks the ore lies somewhere in the world. The location remains unknown.
129|||The villager asks the party to find the ore and carry on the monk's research.
133|||Hodram promises that they will find it. His solemn assurance suits the request.
144|Of course! I'll leave no stone unturned!|leave no stone unturned!|Charles excitedly commits to a thorough investigation.
148|||Hodram tells Charles that finding the ore will earn him command of a fleet in the region and the freedom to study it.
""",
}
review = checked_text(previous.review, {"len(records) == 127": "len(records) == 96"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::island-village-survey-alchemy", "exec"), scope)
if __name__ == "__main__":
    scope["main"]()
