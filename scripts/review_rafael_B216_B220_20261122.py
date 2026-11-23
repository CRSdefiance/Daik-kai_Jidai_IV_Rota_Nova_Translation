"""Review Jam's castle trip, the parrot, the earring seller, and the sword rumor."""

from inspect import getsource

from scripts import review_rafael_B211_B213_20261122 as prior_review
from scripts.source_locked_derivation_v5118 import checked_text


OUTPUT = prior_review.paired.ROOT / "contextual_decisions_B216_B220_v3.json"
WRAPS = {
    "DK4_MES_B217_R0017": (["It just talked like a person!"],
                          "Angelo's quick exclamation gets its own beat. The next row keeps the entire reply the parrot repeats."),
    "DK4_MES_B216_R0047": (["Something terrible has happened!"],
                          "Keep the guard's repeated summons separate from the full warning."),
    "DK4_MES_B218_R0093": (["Here are your ceramic earrings."], "Keep the handover on one line after his compliment."),
    "DK4_MES_B220_R0028": (["the way you carry yourself.", "you look strong, too."],
                          "Keep the comparison and the qualification readable as complete phrases."),
    "DK4_MES_B220_R0048": (["So where's the sword?"], "Keep Cristina's location question intact."),
}
DECISIONS = {
    216: """
5|||Jam decides to go wandering for something to do. The conversational opening fits his restlessness.
9|Ma'am, what's there to see here? I'm bored and could use a walk.|I'm bored and could use a walk.|Jam asks the innkeeper for a place to go and explains why. The polite address gives her no family relationship.
13|||The innkeeper points him east to the lord's castle. The wording preserves the direction and the title.
16|||Jam interprets the unfamiliar term as a castle and decides to see one for himself. Keep his moment of recognition.
19|||Rafael calls him by his usual name and sounds exasperated after searching for him.
23|||Jam apologizes twice and immediately gives the weight of the object as his excuse.
26|||Rafael stammers before asking what Jam has brought back and how it happened.
31|||Keep the triumphant Made in Japan phrasing and the figurehead claim in Jam's voice.
35|Folks here didn't seem to know what to do with a figurehead, so I showed them. They gave it to me as thanks.|with a figurehead,;so I showed them.;They gave it to me as thanks.|Jam claims to have taught the people what to do with a figurehead and says they rewarded him. Keep the account in his voice before the castle scene contradicts it.
38|||Rafael lets the explanation go and urges Jam to get ready to leave.
42|||Jam agrees and asks for only a moment.
47|M-my lord! My lord! Something terrible has happened!|Something terrible has happened!|The guard stammers and repeats the address in escalating alarm. Keep the warning together after the summons.
50|||The daimyo is irritated by the commotion so early in the morning. Keep it a reaction to the shouting.
54|Th-the shachihoko is gone! This letter's in foreign writing!|shachihoko is gone!;This letter's in foreign writing!|The guard names the missing ornament and describes the foreign lettering. Preserve the Japanese object's name and his alarm.
57|||The daimyo is shocked, treats the loss as serious, and orders the guard to find the thief at any cost.
60|||The guard acknowledges the order with an immediate, deferential reply.
64|||Keep the formal greeting as its own letter panel before Jam's casual instructions.
68|||Jam tells the lord that the ornament belongs on a ship and guesses that someone misunderstood. His confidence is part of his joke.
71|||Jam claims a spare in place of thanks, gives the one-per-ship advice and says to remember it. Keep the contradiction with his earlier gift story.
74|||Keep the casual farewell and full signature as two lines with the installed signature indent.
""",
    217: """
5|||The brief repeated flap introduces the animal before it speaks.
9|||Angelo is startled and blurts out the question that the parrot repeats next.
13|||The parrot repeats Angelo's question without his first startled exclamation. Keep the echoed words exact.
17|||Angelo's Italian exclamation and astonishment are part of his voice. The parrot picks up the human-speech observation immediately.
20|||The parrot repeats Angelo's observation word for word. Leave the preceding exclamation with Angelo alone.
24|||Rafael matter-of-factly identifies the parrot while Angelo is still surprised.
29|||Angelo repeats what he has just learned, prompting a new imitation.
33|||The parrot mirrors Angelo's observation exactly.
37|||Angelo tells the parrot to stop copying. The short imperative sets up the next gag.
41|||The parrot copies even the instruction to stop. Keep the phrasing and punctuation identical.
45|||Angelo's frustration turns into amusement and a resolve to catch the bird.
48|||Angelo starts his attempt with a brief shout.
52|||The speakerless sound panel keeps the sequence of wingbeats, impacts and rustling as both men scramble.
56|||Rafael announces that he has caught the parrot. Angelo's following boast does not change who caught it.
61|||Angelo catches his breath and playfully asks whether the bird has had enough. The parrot repeats only those questions.
65|||The parrot repeats Angelo's two questions exactly, leaving the laughter to the people.
69|||Rafael's laughter is the response to the final imitation and closes the scene.
""",
    218: """
5|I've got something good. Interested?||The seller pitches an unnamed item and asks whether they would buy it. His opening sounds like speech rather than an advertisement.
9|||Cristina's question invites the seller to show what he has.
13|Right here.||The seller presents the item without naming it before Claudio recognizes it.
17|||Claudio identifies the item as earrings. Keep the quick observation.
21|||The seller confirms that they're ceramic earrings. Preserve the material because it recurs when he hands them over.
25|||Rafael doubts the earrings are particularly rare. The question gives the seller room for his pitch.
29|||The seller's chuckle introduces his claim that they're no ordinary earrings.
33|||Cristina asks what makes them different before he tells the story.
37|||The seller cites a celebrated dancer and a legend about attracting men while dancing in the earrings. Preserve both as sales claims.
40|||Claudio jokes that they would do him no good and turns the question to Cristina by name.
44|||Cristina is curious about dancing better. She says she has no man she would go to such lengths to impress.
48|You don't have to wear them. Give them to a woman at the tavern and she'll fall for you. You'll get friendly in no time.|don't have to wear them.;Give them to a woman at the tavern;You'll get friendly in no time.|The seller offers the gift as another use and pitches a quick way to win someone over. Keep his sales claim and the phrase Cristina echoes.
51|Get friendly? What's the point?|What's the point?|Cristina echoes the salesman and questions what the supposed rapport would accomplish.
55|Once you're on good terms, you'll hear all sorts of things. The women at the tavern know what's going on.|on good terms,;all sorts of things.;The women at the tavern;know what's going on.|The seller explains the informational motive and keeps his claim about the women at the tavern in his own voice.
836_0|||The first response acknowledges the sales argument. Keep the short caption in its original slot.
836_1|||The second response challenges the point. The contrast is part of the choice.
70|||The seller takes the acknowledgment as acceptance of his argument.
73|||Rafael says he'll take them before the seller discloses the price and the player can confirm or object.
78|That'll be 9,000 gold. I'm practically giving them away. I won't take a coin less.|That'll be 9,000 gold.;I'm practically giving them away.;I won't take a coin less.|The seller names the exact price, boasts that it is a bargain, and rules out bargaining down even a single coin.
1006_0|||The first caption confirms purchase after the player hears the actual price. Keep the willing tone.
1006_1|||The second caption objects that the price is high, with the original trailing pause.
93|You've got a good eye. Here are your ceramic earrings.|Here are your ceramic earrings.|The seller compliments the buyer, hands over the item, and repeats its material without breaking up the handover.
100|||After the price objection the seller says he misjudged the group and withdraws the offer.
103|||Claudio objects to the rudeness and reminds the man that he approached them.
106|||The seller calls them cheapskates and orders them away. His tone changes sharply once the sale fails.
109|Fine by me! Let's go, FI!|Let's go, FI!|Claudio returns the dismissal and calls the player by the original customizable given name.
119|||The seller ends the less receptive path by saying he will not sell to someone who still doesn't understand. Keep it separate from the price objection.
122|Huh? What was he trying to say? What a rude man.|What was he trying to say?;What a rude man.|Cristina is baffled by the sales argument and indignant at how the seller treated them.
""",
    220: """
5|||The older man asks for a moment before saying whom he means.
9|||Cristina briefly checks that the man is addressing her.
13|||He confirms it directly before explaining what caught his attention.
17|||Cristina asks what he wants. Her matter-of-fact reply suits the brief opening.
21|You remind me of a woman pirate from years ago. She really was formidable.|a woman pirate;She really was formidable.|He remembers a formidable pirate from long ago. Keep his admiration and the reference to her as a woman.
25|||Cristina asks whether the resemblance is physical and specifically mentions her face.
28|It's the way you carry yourself. Maybe it's because you look strong, too.|the way you carry yourself.;you look strong, too.|He makes the comparison about her bearing and tentatively attributes it to her apparent strength.
32|||Cristina takes the comparison as a reason to work toward being stronger herself.
36|Oh, you want to get stronger? Why not seek her treasured sword?|Why not seek her treasured sword?|The man suggests the search after hearing what Cristina wants. He makes no claim that the sword confers strength.
40|||Cristina repeats what she has just heard, keeping the treasured sword as the subject.
44|||The old man says the pirate was said to use the sword and admits he doesn't know its value.
48|Hmm. That's interesting. So where's the sword?|So where's the sword?|Cristina is intrigued and gets directly to the location question.
51|||The man gives only the Caribbean as its location. The brevity sets up Cristina's later exasperation.
55|||Cristina echoes the broad geographic lead as she considers it.
59|She fought in a big sea battle in the Caribbean. The story goes she lost the sword in the fighting.|in the Caribbean.;The story goes;the sword in the fighting.|The pirate fought in the Caribbean battle, and the loss of the sword during the fighting is a story the man heard.
62|||Cristina expects more detail after the scant location and the account of the battle.
66|That's all.||The old man answers plainly that this is the extent of his story.
70|||Cristina asks how she's supposed to find the sword using such a broad clue. Keep her exasperation.
73|I couldn't tell you. I have a feeling you could find it.|I couldn't tell you.;you could find it.|The old man has no search method to offer, but he feels Cristina might be able to find it.
76|||Cristina says she'll remember the lead. Her answer makes no firm promise to search.
79|||The old man encourages her and voices his confidence. This is his confidence rather than confirmation of a find.
82|||Cristina thanks him simply before the final private thought.
86|||Cristina imagines the sword lost in the Caribbean and wants to see it. Keep this a private thought and the location qualified by the story.
90|||The original speakerless notice gives Cristina one point of Charm. Her fixed name fits without the customizable-name issue.
""",
}

source = checked_text(getsource(prior_review.main), {
    'len(records) == 81 and len({r["id"] for r in records}) == 81':
        'len(records) == 89 and len({r["id"] for r in records}) == 89',
    'for r in records) == 2': 'for r in records) == 4',
    'for r in records) == 6': 'for r in records) == 12',
})
scope = vars(prior_review) | globals()
exec(compile(source, __file__ + "::contextual-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
