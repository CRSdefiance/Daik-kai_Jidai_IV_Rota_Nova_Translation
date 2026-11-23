"""Review Sera's pauses, the assembled maps, and the later discovery exchanges."""

from scripts import review_hodram_B131_B132_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B143_B150_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    143: "Sera seems to have disappeared while Hodram waits over a drink. He finds her with Rafael, whose silence and smile are separate beats. He leaves with Sera without learning what passed between them.",
    144: "Hodram and Gerhard fit together the two parts of a stone tablet and recognize a map to Africa's Proof of Conquest.",
    145: "A tavern worker demands payment from Nagarpur. Hodram listens to Nagarpur's complaints and suggests he start again. Gerhard and Charles respond to the change in Nagarpur.",
    146: "Hodram and Gerhard combine the Evergreen Lotus Leaf and Kushan Platter. The leaf takes up water and its veins reveal a map.",
    147: "A tavern worker tells Hodram about the Lotion Jar. Charles guesses at its contents and the worker shares a story about an ancient king.",
    148: "Gerhard or Charles suggests putting the Ancient Kingdom Coin in the Lotion Jar. The two versions differ in their reasoning and reactions, but the result is the same map.",
    149: "The crew recognizes the workshop that made the iron-plated ship. Hodram weighs its limits, and different speakers point out a more practical use of the armor technique.",
    150: "Either Charles or Julian realizes that the Tang Bamboo Craft matches the Bamboo Assembly Plan. Disassembly reveals a map. The two versions preserve the crewmates' separate ways of speaking.",
}
DECISIONS = {
    143: """
5|||Hodram notices Sera is missing and calls her name. Preserve his initial sound of surprise.
8|||He wonders where she has gone. The direct question fits the growing gap in their conversation.
17|||The tavern worker asks whether he is looking for anyone. The neutral wording suits the ordinary exchange.
23|||Charles asks if something is wrong after seeing Hodram's reaction. The established line leaves the reason unstated.
30|||Hodram brushes off the concern and predicts Sera will return while he drinks. Keep it as his expectation.
33|||The three visible rows of ellipses stage consecutive beats of waiting with no dialogue. The Japanese deliberately gives the same silent row three times. Retain the layout for dramatic timing.
37|||Hodram reflects that Sera has been away a while. The pause and line follow the earlier beats rather than opening a new subject.
40|||The second independent silence extends the wait. Keep it separate from the earlier multirow passage.
44|...What am I going to do with that girl?|that girl?|Hodram's resigned fondness and impatience prompt him to go looking. The remark establishes no relationship beyond the situation.
49|||Hodram calls for Sera and asks where she is. The separate search call follows his decision to look.
53|||The punctuation marks a moment of uncertainty after the search call. Keep both the hesitation and the question.
66|||The single silent beat precedes Hodram spotting her. Preserve its separate source command.
71|Sera.|Sera.|He addresses Sera after finding her. The added sentence punctuation gives the name a finished audible cue.
75|Oh, FI.|Oh, FI.|Sera answers with recognition and the original controlled name. The gentle acknowledgment keeps her ready reaction in this particular scene.
79|||Rafael's own silent turn is a distinct native actor-zero display. Do not treat it as Hodram or collapse it into Hodram's next line.
84|||Hodram wonders if Sera and the man know each other, then doubts it. The uncertainty belongs to his own observation.
87|(He smiles.)|(He smiles.)|Rafael smiles instead of speaking. A simple sentence in parentheses makes the separate stage direction read naturally without changing the fixed speaker.
92|||Hodram absorbs the response in a quiet sound. Keep the separate beat before Sera speaks again.
96|||Sera calls to Hodram using the exact FI substitution and makes it a question.
100|||Hodram asks her to come along. The plain cue ends the encounter.
104|||Sera acknowledges and goes with him. The brief response fits her established speech in this scene.
""",
    144: """
5|We've got both pieces now, the Upper Stone Tablet and the Lower Stone Tablet.|the Upper Stone Tablet;the Lower Stone Tablet.|Hodram identifies the two pieces by their exact catalogue names. Keep both names and the fact that they have now collected them.
8|||Gerhard reasons that the pieces were once one tablet. The existing English preserves his inference.
11|||Hodram proposes fitting the pieces together. The trailing pause leads into the reveal.
15|||Hodram identifies the combined pieces as a map to Africa's Proof. The tone lifts slightly on recognition.
18|That settles the map. Now let's go find the Proof of Conquest.|Now let's go find;the Proof of Conquest.|Gerhard says discovering the map is only one step and urges a search for the Proof itself. The next task stays explicit.
""",
    145: """
5|||The tavern worker bluntly tells Nagarpur to pay his tab and leave. The phrasing sets the humiliating tone of the encounter.
8|||Nagarpur recoils in a short frightened sound. The reaction fits the brusque treatment.
12|||Gerhard begins recognizing someone without saying his name. The quiet prompt lets Hodram name him.
16|||Hodram identifies Nagarpur after a pause. Preserve the approved name and the frank recognition.
20|||Nagarpur recognizes the controlled FI name and blames Hodram for what has happened. The stammer carries both shock and resentment.
23|||Nagarpur says his associates abandoned him and grouses about losing his fine food. The petty grievance is part of his characterization.
26|You brought this on yourself. The people around you only wanted your money.|brought this on yourself.;only wanted your money.|Hodram holds Nagarpur responsible and says his old associates cared only for his wealth. The direct English preserves his admonition.
29|They left when your money ran out. Money can't buy a genuine bond. You see that now, don't you?|your money ran out.;a genuine bond.;You see that now, don't you?|Hodram links the desertions to lost wealth and says money cannot buy real relationships. Keep his concluding tag together.
32|||Nagarpur answers with silence. Preserve this space for the point to sink in.
36|Once you see that, you can start over.|you can start over.|Hodram makes starting again conditional on Nagarpur recognizing what went wrong. The plain language offers a way forward.
39|||Nagarpur makes an unhappy sound, then says farewell with the original FI name. Keep the change from accusation to departure open.
42|Admiral, what you said really moved me.|really moved me.|Gerhard admires Hodram's words and says they affected him. The short reply sounds sincere.
53|||Charles is impressed that Hodram reached Nagarpur and says he is glad to have followed him. The existing language fits his warmer commentary.
""",
    146: """
5|||Hodram is sure the leaf represents the Indian Ocean's Proof, but he does not yet know the next step. Keep both the exact title and the unfinished thought.
9|||Gerhard cannot see how to combine the leaf and the Kushan Platter. Keep the approved item title and his uncertainty.
13|||Hodram proposes water in the Kushan Platter and floating the leaf on it. The pause makes it a trial rather than an instruction known to work.
17|||Gerhard sees the water bring out a map from the leaf's veins. The active phrasing preserves the visual effect and discovery.
21|||Hodram considers the Indian Ocean's Proof within reach. The short note of satisfaction belongs to this reveal.
""",
    147: """
5|Hey, is that a Lotion Jar? I hear the stuff inside can dissolve any metal except gold.|stuff inside;any metal except gold.|The tavern worker recognizes the item and shares the striking property as hearsay. The casual opening carries the speaker's amazement.
8|Really? That's the first I've heard of it.|the first I've heard of it.|Hodram is surprised and says the claim is new to him. The idiom reads as a response to the rumor.
20|||Charles wonders whether the liquid is a kind of acid and what it is made of. Keep both thoughts speculative.
26|||The tavern worker says an ancient king supposedly used it to expose fake goldwork. Keep the attribution and purpose.
""",
    148: """
11|||Gerhard brings up the Ancient Kingdom Coin after considering something. The formal address fits his version of the opening.
16|||Charles introduces the same item in a separate call. Keep the exact title and the second speaker.
22|||Hodram asks why the coin came up. The short question works with either opening.
32|||Gerhard formally suggests soaking the coin in the Lotion Jar. Keep the original item title and tentative tone.
37|||Charles makes the same suggestion as the result of his own thinking. His first-person setup distinguishes the alternative.
44|That's a new idea. But the whole coin could dissolve.|the whole coin could dissolve.|Hodram acknowledges the originality of the suggestion and names the risk. He makes no prediction that the coin will be destroyed.
54|Doing something is better than sitting here without a plan, wouldn't you say?|without a plan, wouldn't you say?|Gerhard argues for action over waiting with nothing to try. The rhetorical question keeps his respectful appeal.
59|||Charles acknowledges that science does not rule out the risk, then recommends trying it anyway. Keep the distinction from Gerhard's argument.
66|||Hodram considers the case and agrees to an experiment. The leading pause leaves a moment for his decision.
76|Then let's dip the coin in the liquid...|the coin in the liquid...|Gerhard narrates the action using the original object. Keep the trailing anticipation and the separate speaker.
81|Then let's dip the coin in the liquid...|the coin in the liquid...|Charles has the same action and wording in his own branch. Keep the separate source command.
87|||Hodram notices a map where part of the coin dissolved. The surprise and result remain explicit.
97|||Gerhard declares the problem solved and proposes finding the Southeast Asia Proof. Keep the exact region.
103|I knew the science would hold up! Now we can find Southeast Asia's Proof of Conquest!|the science would hold up!;Proof of Conquest!|Charles claims scientific vindication with excitement. His response differs from Gerhard's and leads to the same search.
""",
    149: """
17|||The sailor recognizes the workshop and blurts out how impressive it is. Preserve the workshop's connection to the specific ship.
23|||Janus is more voluble than the sailor. His two exclamations and recognition suit this alternative.
32|Ohhh! Ab-so-lutely magnificent! Why, this is the workshop that built that iron-plated ship!|Ab-so-lutely magnificent!;that iron-plated ship!|The speaker draws out the praise and turns the recognition into a performance. The syllable breaks preserve the exaggerated delivery of the Japanese.
39|||Hodram reasons that the need for rowers would make ocean voyaging difficult. The existing conditional judgment gives the crew a reason to propose a different use.
55|||The sailor suggests using the same technique for the fleet's armor. The casual delivery remains distinct from the other responses.
60|But we could use this technique to make our ships' armor even stronger!|make our ships' armor;even stronger!|Janus acknowledges the limitation and highlights the benefit for armor. The suggestion answers Hodram's concern.
68|But this technique can still make our ships' armor stronger!|make our ships' armor stronger!|Manuel makes the same practical point in his own body. Keep the separate nameplate and the sense of a further improvement.
74|||Hodram considers the proposal in a brief response. The quiet beat leads into the status notice.
78|||The speakerless notice announces that additional armor can now be installed. Keep the distinction between unlocking installation and actually installing it.
""",
    150: """
11|||Charles calls the admiral over after noticing something about the Tang Bamboo Craft. The item name stays whole and the thought stays unfinished.
17|Admiral, about this Tang Bamboo Craft...|this Tang Bamboo Craft...|Julian begins his own explanation of the same item. The direct address is present in his original opening.
23|||Hodram admires the object's complexity and asks what stands out. His question gives either crewmate room to explain.
32|||Charles sees a connection to the Bamboo Assembly Plan and thinks it gives steps for taking the craft apart. Keep his inference and the exact plan name.
38|||Julian poses the same idea more casually as a question and a bet. That contrast is useful characterization.
45|||Hodram invites the crewmate to try it. The short question keeps their initiative with them.
55|Really? All right, here goes...|All right, here goes...|Charles sounds surprised to get permission and then accepts it. The ordinary spoken phrase replaces a stiff formal formula.
60|||Julian is delighted and says he enjoys this kind of thing. His energetic answer stays distinct.
72|There. I've got all the pieces apart. Wait, there's something drawn on the back of the bamboo.|all the pieces apart.;back of the bamboo.|Charles confirms the whole object is dismantled and notices a drawing on the reverse. His focus shifts from the procedure to the find.
78|All done! It's all in pieces now. Huh? There's something drawn on the back...|It's all in pieces now.;drawn on the back...|Julian celebrates completion before noticing the drawing. The casual language preserves his change in attention and the same physical discovery.
85|||Gerhard identifies the image as a map in a short exclamation. The line lets Hodram identify the destination.
89|||Hodram concludes that the map shows the East Asia Proof and understands how the craft was designed to conceal it. The existing pause suits him piecing it together.
""",
}
review = checked_text(previous.review, {"len(records) == 77": "len(records) == 83"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::Sera-and-discoveries", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

