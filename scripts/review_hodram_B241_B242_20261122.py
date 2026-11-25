"""Review Janus's injury, the missing gloves, and the Frozen Rose return."""

from scripts import pair_hodram_B241_B260_20261122 as paired
from scripts import review_hodram_B236_B240_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = paired.base, paired.ROOT
OUTPUT = ROOT / "B241_B242_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    241: "Janus catches his hand on a mast fitting while working on the ship. A nearby man checks his hand and offers to show him gloves that could have prevented the injury. Unable to find them, he remembers where he might have dropped them and promises the gloves to the crew if they find them.",
    242: "A woman recognizes the Frozen Rose as a beloved birthday gift that was stolen. Hodram gives it back and declines another reward. In gratitude she points out a wooden church near town that the crew may have overlooked.",
}
DECISIONS = {
    241: """
5|||Janus cries out, pauses and reacts to the pain. The two sounds cue Hodram to check on him.
9|||Hodram recognizes Janus and asks what happened in the same turn.
12|It's nothing serious. I caught my hand on a mast fitting while I was working on the ship.|caught my hand;a mast fitting;working on the ship.|Janus reassures Hodram and explains the accident without claiming a more specific injury.
16|||The nearby man notices the commotion and asks what is wrong. The greeting stays familiar.
19|||Janus is hesitant to explain. The unfinished answer leaves room for Hodram.
23|||Hodram identifies Janus by his crew function and says the injury is to his hand.
26|||The man expresses concern and asks to look at Janus's hand in his direct voice.
29|||Janus winces while his hand is being looked at. Keep the small pause.
33|Hmm. That's the sort of thing that happens to sailors all the time.|sort of thing;happens to sailors|The man recognizes an ordinary injury for someone who works aboard ship.
36|||The man chuckles and says he has gloves that could spare Janus this sort of injury. The sales confidence sets up his search for them.
40|||Janus repeats the object as a question. The short echo invites the man to explain.
44|You bet. You won't find gloves this handy just anywhere. Hang on... Where'd I put them?|gloves this handy;Hang on...;Where'd I put them?|The man boasts that unusually handy gloves are hard to find, then searches for his own.
47|||The man realizes he may have lost the gloves and reacts sharply. The question keeps the loss uncertain.
50|||Hodram's dry response follows the abrupt failure to produce the gloves.
54|Sorry about that. If I dropped them... Oh, I know! Somewhere around Denmark!|If I dropped them...;Somewhere around Denmark!|The man apologizes and works out where he thinks he could have lost the gloves.
58|||Janus echoes Denmark and lets the man refine the clue.
62|You bet! The Jutland Peninsula, I'm sure of it! Honest! You've got to believe me!|The Jutland Peninsula,;I'm sure of it!;believe me!|The man narrows the clue and repeatedly asks to be believed. His insistence follows the way he guessed the location.
66|All right. We'll take a look.|We'll take a look.|Hodram agrees to search without promising to find the gloves.
70|||The man is glad to be believed and offers the gloves to the crew only if they find them.
74|They don't fit my hands, so I was going to sell them anyway. But they work, and I'll swear to that.|don't fit my hands,;sell them anyway.;I'll swear to that.|The man gives his reason for selling them and vouches for their effect in his own voice.
""",
    242: """
6|||The woman greets the visitors before she notices the ornament.
10|Oh! Could I see that ornament you're carrying?|see that ornament;you're carrying?|She is surprised by what the player has and politely asks to see it.
14|||Hodram checks what she means by showing her the item. The short question fits.
18|I knew it! Where did you find this?!|I knew it!;Where did you find this?!|She recognizes the item after examining it and asks where it was found.
21|||Hodram says a thug named Gabriel had it. His unfinished delivery leaves room for her reaction.
24|It's mine! I treasured it, but it was stolen a while ago...|I treasured it,;a while ago...|She identifies herself as its owner and explains both its value to her and the theft.
28|||She explains that Dad bought the ornament for her birthday because she loved roses. The existing wording preserves the source relationship and the gift's importance.
32|I see. I'm glad it's back where it belongs.|back where it belongs.|Hodram accepts her account and is pleased that the ornament has returned to its owner.
36|||The speakerless notice names the Frozen Rose and confirms the return. Keep the approved item name.
45|||She thanks Hodram and explains that she had given up on ever holding the ornament again. Her exuberance fits the relief.
49|I ought to give you something to thank you...|give you something;to thank you...|She offers a token of thanks before Hodram mentions the guild reward.
53|||Hodram says the guild already paid him for catching Gabriel. The reply explains why he declines more.
57|||She calls after Hodram using the original given-name substitution. The punctuation expresses her emotion.
61|Take care.|Take care.|Hodram says goodbye in a familiar way. The next line interrupts his departure.
72|||She asks him to wait, moving from the declined reward to a useful tip.
76|You explore all over the world, don't you?|all over the world,;don't you?|She asks whether the crew explores the world. Keep the focus on exploration as the reason she brings up the church.
79|||She asks whether they know the church outside town and mentions its uncommon wooden construction. Keep the facts as her description.
84|Right under my nose. I hadn't thought of that. I'll go take a look.|Right under my nose.;hadn't thought of that.;go take a look.|Hodram recognizes that he overlooked a place close by and decides to visit.
93|||She thanks him again and asks him to return. The warm farewell closes the exchange.
""",
}

review = checked_text(previous.review, {"len(records) == 75": "len(records) == 39"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::gloves-and-frozen-rose", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
