"""Review Jam's castle visit, the parrot, and the earring seller."""

from scripts import pair_hodram_B201_B220_20261122 as paired
from scripts import review_hodram_B204_B207_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = paired.base, paired.ROOT
OUTPUT = ROOT / "B208_B210_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    208: "Jam asks where to go for a walk and learns of a nearby castle. He returns with a heavy ornament and tells Hodram it was a thank-you gift. The castle guard and daimyo then discover the missing shachihoko and the foreign letter. Jam's breezy letter claims the ornaments are figureheads and admits that he took a spare.",
    209: "Angelo encounters a parrot and reacts with surprise and then delight as it repeats parts of his speech. He tries to catch it, Hodram succeeds, and Angelo gloats before the bird parrots that too.",
    210: "The seller pitches ceramic earrings to Cristina, then tells Hodram they could help him befriend a woman at a tavern and get information. Cristina and Sera are uninterested in wearing them. The seller reacts differently to interest, a complaint about the price, and doubt about his explanation.",
}
DECISIONS = {
    208: """
5|||Jam says he is bored and decides to go out. The thought sounds spontaneous and leads to his asking where to go.
9|Ma'am, is there anything worth seeing around here? I'm bored and feel like taking a walk.|worth seeing around here?;taking a walk.|Jam politely asks a stranger where he can go for an interesting walk. The boredom and form of address stay separate.
13|||The woman says the local lord's oshiro is to the east. Keep the Japanese word here so Jam can work out what she means on the next turn.
16|Oshiro...? Oh, a castle! Sure, let's see what a castle looks like around here.|Oh, a castle!;looks like around here.|Jam works out the word and decides to go see what castles look like in Japan. His quick decision preserves the joke about his earlier boredom.
19|You're late, Jam. Where have you been all day?|been all day?|Hodram points out the delay and asks where Jam has spent the whole day. The firm question sets up Jam's casual excuse.
22|Sorry, sorry. This thing's heavy.|Sorry, sorry.;This thing's heavy.|Jam repeats a careless apology and explains that the ornament was heavy. He acts as if that settles the matter.
25|||Hodram asks both what the object is and where Jam got it. Keep his two distinct questions.
28|Can't you tell? It's a figurehead! Genuine, made in Japaaaan!|It's a figurehead!;made in Japaaaan!|Jam boasts about the figurehead and deliberately draws out Japan as if pitching a product. Keep the emphatic English loan phrase's comic effect.
32|People here don't seem to know what figureheads are for. I showed them, and they gave me this as a thank-you.|what figureheads are for.;as a thank-you.|Jam claims he taught the locals how to use figureheads. He describes the object as a gift, which the following scene calls into question.
35|You taught someone? Never mind. We're leaving soon. Pack your things.|We're leaving soon.;Pack your things.|Hodram finds Jam teaching someone hard to imagine but presses on with preparations to depart. Keep the joke and practical instruction.
39|||Jam accepts the order and asks for a moment. The casual answer suits the end of their exchange.
44|M-my lord! My looord! Something terrible's happened!|M-my lord!;My looord!;Something terrible's happened!|The guard stammers and calls again before getting to the news. Keep the lengthened call and urgent warning.
47|What is it?! Why all this racket so early in the morning?|What is it?!;early in the morning?|The daimyo is irritated at being disturbed in the morning. The reaction contrasts with the guard's panic.
51|||The guard stammers through both discoveries, the missing shachihoko and a letter in foreign writing. The fixture keeps his alarm distinct from the daimyo's reply.
54|What?! The shachihoko's gone? This is serious! Find that thief, whatever it takes!|The shachihoko's gone?;This is serious!;whatever it takes!|The daimyo realizes how grave it is and orders the guard to find the thief at all costs. The charge of theft is his interpretation.
57|||The guard acknowledges the command at once. The short answer suits his deference and urgency.
61|||Jam addresses the letter to the lord in Japan. The existing salutation preserves the office and location.
65|That statue's called a figurehead. It goes on a ship, not a castle. I guess only half the story made it over here.|called a figurehead.;on a ship,;not a castle.;made it over here.|Jam gives his own explanation of the ornament and guesses the idea was only partly transmitted. The letter presents Jam's belief in his own breezy voice.
68|Oh, no need to thank me. I'll take one of the spares instead. One figurehead per ship. Remember that.|no need to thank me.;one of the spares instead.;One figurehead per ship.;Remember that.|Jam treats the spare ornament as his payment and explains the one-per-ship rule. The playful farewell anticipates the signed panel.
71|||Jam signs the letter with his established full name. Preserve the native panel's signoff and signature arrangement.
""",
    209: """
5|Flap, flap!|Flap, flap!|The first speakerless sound imitates wings beating twice. Conventional capitalization keeps it consistent with the second sound panel.
9|||Angelo exclaims when he sees the bird. Its first reply echoes only his question, so his initial cry remains separate.
13|||The parrot echoes Angelo's question without his exclamation. The established caps give the mimicked voice an immediately recognizable form.
17|Mamma mia! It talks like a person!|Mamma mia!;talks like a person!|Angelo reacts in his usual Italian interjection and marvels that the bird speaks like a human. The following parrot panel repeats the second part.
20|IT TALKS LIKE A PERSON!|IT TALKS LIKE A PERSON!|The parrot immediately repeats the substance of Angelo's outburst. Its capitalized voice keeps the exact echoed phrase apart from his interjection.
24|That's a parrot.||Hodram matter-of-factly identifies the bird. The contraction suits the quick answer while Angelo is startled.
28|||Angelo repeats the type of bird back to Hodram. The short tag makes this a question, which sets up the next echo.
32|A PARROT, EH?|A PARROT, EH?|The bird echoes Angelo's full question including the short tag. Keep his audible inflection in the echo.
36|||Angelo tells the bird to stop copying him. This direct command is immediately repeated by the bird.
40|||The parrot repeats Angelo's command verbatim in its established display style. This keeps the joke intact.
44|Oh, this is fun! I'll catch you!|Oh, this is fun!;I'll catch you!|Angelo sees the mimicry as a game and decides to catch the bird. The tone brightens from annoyance to amusement.
47|||Angelo announces his attempt and makes a short effort sound. Both fit the noisy action that follows.
51|Flap, flap! Thud! Crack! Flap! Bang! Rustle!|Flap, flap!;Thud! Crack!;Bang! Rustle!|The sounds track wings, impacts, and movement in the original order. The labels read consistently as sound effects.
55|||Hodram says he caught the parrot. The unshowy remark contrasts with Angelo's gloating.
59|||Angelo catches his breath and taunts the bird before laughing. Both questions feed into the parrot's final reply.
63|||The parrot repeats both of Angelo's taunts. It leaves out his breath and laughter, as in Japanese.
67|||Hodram gives a brief amused reaction. It closes the exchange after the bird gets the last word.
""",
    210: """
5|I've got something nice for sale. Interested?|nice for sale.;Interested?|The seller opens with a vague enticement. His question invites Cristina to ask what he is selling.
9|||Cristina repeats the seller's vague description, asking him to be specific. Her question fits the pitch.
13|||The seller produces the item and lets Cristina identify it. The single word directs her attention.
17|||Cristina recognizes what the objects are. Keep her question as the seller starts the pitch.
21|That's right. Ceramic earrings.|Ceramic earrings.|The seller confirms what Cristina sees and specifies the material. Both short beats fit the sales exchange.
25|||Cristina sees nothing unusual about the earrings at first. Her skepticism prompts his story.
29|||The seller chuckles and insists the earrings are special. His reserve sets up Cristina's question.
33|||Cristina asks what makes them different. The direct question hands the pitch back to the seller.
37|They belonged to a dancer people called the finest in the world. Legend has it you can charm any man by dancing in them.|finest in the world.;Legend has it;charm any man;dancing in them.|The seller attributes the earrings to a famously skilled dancer and presents the ability to charm as legend. Preserve who wears them and when.
40|||Hodram reacts dryly that the earrings would be wasted on him and turns to Cristina. The approved name stays in his question.
44|||Cristina is interested in improving her dancing. The turn makes clear she has no man she wants to win over that way.
56|||Hodram asks Sera next. The approved short name and question stay direct.
60|||Sera silently shakes her head. The existing stage direction avoids giving her speech.
64|...Are you sure? Well, we don't need them, then.|Are you sure?;need them, then.|Hodram checks Sera's decision and concludes they have no use for the earrings. His pause leaves room for her silent response.
70|You could give them as a gift instead. Give them to a woman at a tavern and you'll win her over in no time.|as a gift instead.;a woman at a tavern;in no time.|The seller shifts his pitch from wearing the earrings to giving them away. Keep his promise of quickly gaining a woman's goodwill as his own sales claim.
73|Win her over? And then what?|Win her over?;And then what?|Cristina questions the purpose of the seller's advice. She echoes his phrasing to make her skepticism land.
77|Then she'll tell you all sorts of things. Women at taverns know plenty.|all sorts of things.;know plenty.|The seller explains why goodwill might help with information. The line preserves the source connection to women at taverns.
SC1_B210_CHOICE_956_0|||The first caption accepts the explanation. Got it is short and leads to the purchase conversation.
SC1_B210_CHOICE_956_1|||The second caption questions the usefulness of the explanation. So what leads to the seller's separate rebuff.
92|||The seller is satisfied that the explanation was understood. His brief reply leads to Hodram's interest.
95|||Hodram decides to take the earrings, leaving the seller to quote a price. His voice remains simple and decisive.
99|That'll be 9,000 coins. It's a steal. I won't go a coin lower.|9,000 coins.;It's a steal.;a coin lower.|The seller names the exact price, describes it as unusually cheap and refuses to bargain. The sales idiom preserves his confidence.
SC1_B210_CHOICE_1126_0|||The first price caption confirms the purchase and hands off to the sale.
SC1_B210_CHOICE_1126_1|||The second caption flags the price with one colloquial word. The seller treats the objection as a refusal.
114|You've got a good eye. Here are your ceramic earrings.|a good eye.;your ceramic earrings.|The seller compliments his buyer and hands over the same ceramic earrings. The conversational wording fits the successful sale.
121|...I had you wrong. Move along. I'm not selling to you.|I had you wrong.;not selling to you.|The seller decides he misjudged this group and calls off the sale. His curt commands show how quickly his manner changes.
124|That's rude! You're the one who came up to us!|That's rude!;came up to us!|Cristina objects to being dismissed by the person who approached them. Her anger is justified by the immediate exchange.
127|||The seller calls them misers and orders them away again. Keep the insult in his voice.
130|Fine! I wouldn't buy from you anyway!|buy from you anyway!|Cristina throws the rejection back at the seller. Her retort fits the heated exchange.
141|...If you still don't get it after all that, forget it. Move along.|after all that,;forget it.;Move along.|The seller refuses to deal after the skeptical answer to his explanation. This branch is about the point of the pitch.
144|What? What was he getting at? That man is infuriating.|What was he getting at?;That man is infuriating.|Cristina remains puzzled about the seller's point and ends the exchange openly irritated.
""",
}

review = checked_text(previous.review, {"len(records) == 86": "len(records) == 68"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::castle-parrot-and-earrings", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
