"""Review the church figurehead and each result of attempting to take it."""

from scripts import pair_hodram_B241_B260_20261122 as paired
from scripts import review_hodram_B241_B242_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = paired.base, paired.ROOT
OUTPUT = ROOT / "B243_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    243: "At the church, Julio notices a figurehead and alerts Hodram. The priest says people can take it only if it likes them. On the attempt branch, Julio helps despite his misgivings. On success, the priest says it accepted them and both sailors attribute the outcome to luck. Failure and declining have separate responses.",
}
DECISIONS = {
    243: """
6|Admiral!||Julio calls Hodram's attention to the figurehead with the source form of address.
10|What is it?|What is it?|Hodram asks what Julio noticed. The neutral question suits the call.
14|||Julio points out the magnificent figurehead. His excitement gives the priest a reason to approach.
17|||The priest acknowledges that they found something remarkable. The compliment fits the discovery.
21|||Julio notices the priest and addresses him as Father. This is the stated religious role.
25|||Hodram comments on the figure's regal bearing and asks about its history. Both parts fit his curiosity.
29|It has no history that I know of. But...|no history that I know of.|The priest says no origin story is known, then pauses before describing the figurehead's behavior.
32|||Julio prompts the priest to finish explaining. Keep the echo of the previous turn.
36|You can only take it if it takes a liking to you.|takes a liking to you.|The priest says the decision rests with the figurehead. Its personification is part of the story.
40|Several people have tried. Most left empty-handed and injured.|empty-handed and injured.|The priest reports prior attempts and preserves both outcomes for most people.
44|Then, when someone who took it dies, somehow it turns up here at the church again.|someone who took it dies,;here at the church again.|The priest describes the return without claiming the figurehead causes the person's death.
48|||Hodram considers what he just heard in a brief, quiet reply.
52|||The priest asks whether they want to make an attempt. The polite invitation opens the choice.
56|Ha! No, thank you. We don't need that strange thing, do we, Admiral?|that strange thing,;do we, Admiral?|Julio dismisses the idea and looks to Hodram for agreement. The tag carries his expectation.
60|||Hodram's hesitation leaves Julio uncertain about whether he will try it.
64|D-don't tell me you're thinking about it, Admiral!|thinking about it, Admiral!|Julio stammers in alarm when Hodram fails to dismiss the idea.
SC1_B243_CHOICE_674_0|||Try it tells the crew to attempt to move the figurehead. The affirmative caption fits the choice.
SC1_B243_CHOICE_674_1|||Leave it declines the priest's invitation and keeps the separate farewell branch.
79|||Hodram decides to try and asks everyone to help. His order follows the affirmative choice.
83|I-I'm telling you, don't do it!|don't do it!|Julio repeats his warning with the source hesitation even after Hodram has decided.
87|You can head back without us if you like.|head back without us;if you like.|Hodram offers Julio the option of going back first. His calm reply lets Julio choose to help.
91|Fine, I'll help! That's what you want, isn't it? Honestly!|Fine, I'll help!;want, isn't it?|Julio agrees to help while making his reluctance plain. The separate exasperated beat closes the protest.
95|||Julio calls out three times with the effort of moving the figurehead. Keep the deliberate repetition.
114|||Julio cries out when the attempt goes wrong. The wordless reaction matches his alarm.
126|||Hodram orders everyone to run. The urgent single word suits the immediate situation.
133|It seems the figurehead didn't find you worthy.|didn't find you worthy.|The priest reads the failed attempt as the figurehead's refusal. The tone stays matter-of-fact.
137|||Julio winces after the failure. The drawn-out sound gives the result a comic close.
143|||On success, the priest interprets the result as acceptance by the figurehead. Keep his interpretive wording.
146|||Julio attributes success to luck. His reply gives the priest a reason to mention modesty.
150|||The priest invites the crew to accept credit. His mild rebuke follows Julio's modest reading.
154|No... I can't think of any other explanation. We must have been lucky.|any other explanation.;must have been lucky.|Hodram agrees with Julio's account and leaves the unexplained figurehead mysterious.
158|Well, I'm glad it worked out. May God bless you all.|glad it worked out.;May God bless you all.|The priest is pleased either way and gives the group a blessing.
163|||The speakerless result preserves the playable captain's given-name substitution and one point of Spirit.
174|||The priest respects the decision to leave the figurehead. This reply belongs to the refusal branch.
178|Exactly! I was afraid you were going to take it!|afraid you were;going to take it!|Julio affirms the decision with open relief. He had been worried that Hodram would attempt it.
182|||The priest blesses the group on departure. Preserve the separate branch and the concise farewell.
""",
}

review = checked_text(previous.review, {"len(records) == 39": "len(records) == 36"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::church-figurehead", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
