"""Review Ian's book purchase, the namahage, and the portrait discovery."""

from scripts import pair_hodram_B201_B220_20261122 as paired
from scripts import review_hodram_B200_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = paired.base, paired.ROOT
OUTPUT = ROOT / "B201_B203_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    201: "A woman offers Ian an Indian classic about a celestial maiden and a sage. Ian asks Hodram whether to buy it. The scene branches into acceptance, refusal, and Ian's own decision. When Ian cannot afford it, she gives him the book and disappears after saying what sort of man she would like to fall in love with. Ian briefly wonders about her identity.",
    202: "A namahage repeats a rough ritual challenge. The woken sailor asks who is there, recognizes the figure, and answers seriously. He takes the encounter for a dream until another crewmate reacts to the object they find. He decides to give it to the admiral and the other man repeats his question.",
    203: "Hodram recognizes Rocco Alemkel in a portrait and Gerhard shares his respect for the navigator. Charles wonders what they were looking at, discovers a book behind the portrait and flips through it. He loses interest when it turns out to be about navigation and plans to give it to the admiral.",
}
DECISIONS = {
    201: """
5|||The woman singles Ian out as handsome from the start. The playful address sets up her return to the same compliment.
9|||Ian checks whether she is talking to him. The surprised question fits the sudden address.
14|Care to buy this book for 8,500 coins?|buy this book;8,500 coins?|Keep her friendly sales pitch and the exact price of 8,500. Coins follows the nearby merchant event's wording for money.
17|||Ian asks what kind of book it is before making any decision. His restrained question gives her room to explain.
21|||The pitch names the Indian classic and lets the two figures' love story speak for itself. The separate question invites Ian to decide.
24|||Ian turns to the player for guidance. Admiral is his source form of address.
SC1_B201_CHOICE_230_0|||The first caption orders the purchase, with Ian accepting on the next turn.
SC1_B201_CHOICE_230_1|||Pass is a natural brief refusal and matches the paired purchase controls.
SC1_B201_CHOICE_230_2|||The third option puts the decision in Ian's hands. Keeping his name makes the difference from the first two options clear.
45|||The approved purchase leads Ian to accept the offer. The simple answer fits his direct delivery.
49|I hope you fall in love with a celestial maiden yourself.|fall in love;with a celestial maiden yourself.|The woman's wish echoes the book's story and points the comparison at Ian. It leaves her identity unresolved.
53|||Ian declines her offer courteously. His stated lack of interest is separate from his later concern about price.
57|Oh, what a shame. And such a handsome man, too.|what a shame.;such a handsome man, too.|She laments the refusal and returns to the compliment that opened the encounter. The playful delivery leaves his rejection intact.
64|||Ian politely turns the offer down on this branch. The brief refusal belongs to him.
68|||She accepts the refusal with regret and plans to sell the book to someone else.
74|||Ian would like to buy it but lacks that much money. The phrasing makes his financial reason distinct from the outright refusal.
77|I see.||She takes in what he said before he apologizes. A brief acknowledgment suits her response.
81|||Ian apologizes because he cannot meet her expectations. His polite wording sets up her unexpected generosity.
85|Then it's yours.||She gives him the book openly after he says he cannot pay. The familiar wording makes the gift clear.
89|||Ian's short surprise fits the offer and gives the woman the next turn.
93|||She laughs and says whom she would like to fall in love with next time. The existing wording expresses a wish without making a claim about the two of them.
97|Sh-she vanished...|Sh-she vanished...|Ian stammers when she disappears. Vanished carries the abrupt strangeness that leads him to wonder if she was the kind of figure from the book.
101|Could she have been a celestial maiden? Heh... What a foolish thought.|a celestial maiden?;What a foolish thought.|Ian briefly entertains the possibility, then chides himself. Keep both his uncertainty and his self-reproach.
109|||The notice grants Ian one Charm point. It gives his fixed name and the exact gain in the established stat format.
""",
    202: """
10|||The rough voice asks twice if there are any bad children present. Keep the repeated formula that gives the entrance its rhythm.
14|||The same question repeats in the next call. Equal wording preserves the deliberate echo.
18|||The voice addresses the woken sailor directly. This is the first single challenge, distinct from the doubled call.
22|||The sailor asks who is there before he recognizes the figure. The short alarm suits the sudden intrusion.
26|||The figure repeats the same challenge after being asked to identify itself.
30|...You're a namahage!|a namahage!|The sailor recognizes the Japanese figure and names it. Keep namahage as the specific cultural reference and leave the pause before recognition.
34|||The figure asks the same direct question again. It keeps up the call until it receives an answer.
38|||The sailor answers sincerely that he recalls no wrongdoing. The formal answer stays in his voice.
42|||The creature registers his answer with a brief, drawn acknowledgment before the ensuing silence.
49|||The silence marks the end of the encounter before the sailor tries to explain it.
53|Was it a dream?|Was it a dream?|The sailor wonders whether the encounter was a dream. His question is tentative and brief.
65|||A second crewmate reacts to the object in surprise and asks what it is. He has a distinct outburst.
72|||The first man notices something too. The interjection leaves space for his next silence.
76|||The pause marks his effort to take in the unexpected evidence.
80|Strange things do happen.|Strange things do happen.|He concedes that the peculiar event happened after all. The quiet reflection contrasts with the other man's alarm.
84|||He intends to give the object to the admiral the following morning. The timing and recipient remain explicit.
95|||The second man asks what the object is again because he still has no answer. The repeated question is the comic close.
""",
    203: """
5|||Gerhard sees Hodram looking at something and asks the admiral what has caught his attention.
9|||Hodram directs Gerhard to the portrait. The brief answer lets Gerhard recognize the subject by name.
14|||Gerhard names Rocco Alemkel, a known figure both men can recognize. Keep the established spelling.
18|Yes. He was a navigator back when Portugal was a great power. He helped keep it that way.|a navigator;Portugal was a great power.;helped keep it that way.|Hodram recalls a navigator who supported Portugal in its powerful days. The second sentence makes his contribution explicit.
21|Indeed. He was from another country, but I respect him all the same.|from another country,;respect him all the same.|Gerhard agrees and states his respect despite their different countries. Keep the personal judgment without assigning Rocco a rank.
24|||Hodram gives a brief affirmation of Gerhard's assessment, ending their exchange.
28|||Charles wonders what attracted the two men's attention. His curiosity follows their conversation.
32|Hm. It's just a portrait.|just a portrait.|Charles initially sees nothing in the picture worth the attention. The understatement sets up the surprise behind it.
36|||The speakerless sound marks the sudden movement of the portrait. Clatter gives that cue in a readable single word.
40|||Charles reacts to the sound with a short expression of surprise before he sees what is behind the portrait.
44|||Charles notices something behind the picture. His hesitation preserves the unfolding discovery.
48|||Charles recognizes a book and immediately hopes it is about science. His excitement sets up the disappointment after checking.
51|||The speakerless rustling is the sound of flipping through the book, between the question and the identification.
55|Aw, it's about navigation. I'll give it to the admiral later.|it's about navigation.;give it to the admiral|Charles is disappointed that it is about navigation and decides to give it to the admiral later. The finding and intended handover stay distinct.
""",
}

review = checked_text(previous.review, {"len(records) == 36": "len(records) == 55"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::book-namahage-and-portrait", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
