"""Review the next eight Rafael wrap leads against the complete exchanges."""

from types import FunctionType

from scripts import register_rafael_early_phrase_wraps_20261118 as parent
from scripts import review_rafael_early_phrase_wraps_20261118 as prior

base, TOKEN, logical, GATES = prior.base, prior.TOKEN, prior.logical, prior.GATES
ROOT = parent.stage.ROOT.parent.with_name("rafael_next_phrase_wraps_20261118")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v3.json"
BLOCKS = ((81, 83, 91, 103, 129, 133, 154, 169), (), (), ())
QUEUE = parent.stage.ROOT / "followup_wrap_queue.json"
CONTEXT = {
    81: "At a bullfight in Spain the crew mistakes the comic crowd favorite for the main attraction. Julio explains the picador's role. Rafael eventually asks the picador, Emilio, to join them.",
    83: "Cristina walks around her old home port. Mivor takes her visit personally and she firmly turns him down. Her relief turns to alarm at the first sign of the drowning child. Mivor later overcomes his fear to rescue them.",
    91: "A sailor asks whether Rafael believes in miracles. Fernando objects at first. The sailor apologizes and explains that he has been looking for someone to take his charm. The two choice outcomes retain their respective notices.",
    103: "Manuel tells Rafael the rumor about the Jaguar God's Vest and jokes about losing interest. Rafael steers him back to the clue and keeps the tentative lead in mind.",
    129: "Julio checks Rafael's trading knowledge, then walks him through investment, port contracts, geographic expansion and the effect of fleet capacity on profits.",
    133: "Julio suggests his granddaughter Cristina. Arcadius quietly challenges Clau's objection and Rafael backs her before the crew agrees to look for Cristina in London.",
    154: "A tavern keeper trusts Rafael with the harm Maldonado's crew is doing. The hesitant branch admits that Rafael cannot promise immediate help. The confident branch commits to defeating Maldonado.",
    169: "Customers gossip about Ian. A man harasses and touches him, starting a confrontation. The tavern keeper is tired of trouble and lets Ian go. Watching from nearby, Rafael suggests speaking with him.",
}
NOTES = {
    81: """
54|Rafael has heard that a popular bullfighter is appearing.|The hearsay and lively anticipation prepare the crew's misunderstanding.
58|Cristina thinks the performer might be handsome.|The quick thought carries her playful excitement.
70|He says the performer is probably no match for him.|Let the understated boast follow Cristina's reply in a natural spoken rhythm.
77|Julio wants a look for himself.|The short response ushers in the crowd's reaction.
82|A spectator laughs.|The laughter supports the comic performance.
86|A spectator asks the performer to make them laugh again.|The familiar call tells the crew this performer is known for his antics.
90|Rafael is surprised and asks if this is the most popular bullfighter.|His astonishment sets up Julio's correction.
94|Julio identifies the picador as the supporting bullfighter.|Keep both Spanish terms and use two complete thoughts rather than an early comma break.
98|The picador tires the bull and the matador delivers the final blow.|The practical explanation immediately distinguishes the two roles.
102|The performer yells.|The vocalization keeps the beat in the crowd's commentary.
106|A spectator laughs at the man playing with the bull and reacts to a throw.|The reaction keeps the action and crowd's amusement without overexplaining what was thrown.
110|The performer yells again.|The second exclamation sustains the live performance.
114|Another laugh follows.|The short laugh keeps the sounds distinct.
118|The spectator yells for him to be taken out.|The direct shout prepares the entrance of the main performer.
126|A spectator announces the long-awaited main attraction.|The ordinary show language works as a contrast to the previous performance.
""",
    83: """
31|Mivor tearfully says he knew his love would reach Cristina.|The repeated beginning and stammer show his over-the-top relief.
35|Cristina asks him to stop crying because people are watching.|The stammer plays her discomfort against his public display.
38|Cristina says London is only a stop and she will travel again soon.|The three spoken beats preserve why she has appeared and what she will do.
41|Mivor is confused.|The one-word reaction gives Cristina space to clarify.
45|Cristina emphatically says that she did not return for him.|The short statement matches her exasperation.
48|She firmly rules out marrying him.|Keep her unequivocal refusal and the specific proposal.
52|Mivor whines and asks what she doesn't like about him.|The long cry keeps his dismay and the question sounds spoken.
55|Cristina says she is not considering marriage yet and asks him to give up.|Her direct boundary sets up his next reaction.
59|He finally agrees to give up and laments the end of his love.|The stammer and little asides remain in his melodramatic acceptance.
63|Cristina is relieved that he will stop pursuing her.|The one-line sigh still leads into the sudden emergency.
67|Cristina reacts to a sudden change.|The short response gives her relief an abrupt interruption.
71|Mivor breaks off his sigh in surprise.|The quick pivot matches Cristina's reaction.
75|The mother cries out for her son.|The cry establishes her relationship before she explains.
79|Cristina asks what happened.|The urgent question suits her immediate response.
84|The mother says her boy fell into the sea and pleads for help.|The location and call for help are clear.
88|Cristina calls for him to hold on and goes to help.|The reassuring promise completes the transition into the rescue.
""",
    91: """
43|The sailor says disbelievers can end up shipwrecked and calls Rafael better off.|The reversal gives Fernando a reason to be confused and introduces why the man cares about faith.
47|Fernando is surprised.|His short interjection gives the sailor room to apologize.
51|The sailor regrets shouting and says he meant no insult to the captain.|Both admissions repair the earlier offense.
55|Fernando cannot make sense of him.|The casual aside keeps the change of mood clear.
59|The sailor wants a captain who believes in miracles to have something.|The wording builds toward revealing the object.
62|He has asked as ships came in and this is exactly the hundredth person.|Keep the repeated searches at the port and the precise count as two readable thoughts.
66|Fernando asks what the item is.|The short question lets the explanation come from its owner.
70|The bullet pendant is supposed to bring miracles.|The established item name and the uncertainty are clear.
73|Rafael asks if he can accept something so valuable to the man.|The question respects the significance of the gift.
77|The sailor wants Rafael to have it and can no longer go to sea himself.|The personal reason for passing on his charm is preserved.
80|Rafael decides to accept and thanks him.|The hesitation makes the acceptance considerate.
""",
    103: """
5|Manuel asks if he can have the admiral's attention.|His short opening works before the new rumor.
9|Rafael asks what it is.|The reply quickly gives Manuel the floor.
14|Manuel proposes looking for the Jaguar God's Vest.|The exact item title establishes the subject of the rumor.
18|Rafael asks what he means.|His brief question sets up the explanation.
23|The vest is said to hold the jaguar god and be in the New World.|Keep the casual name joke and both reports as hearsay.
27|Rafael realizes Manuel has brought another rumor.|The reply links the clue to Manuel's earlier habit.
31|Manuel says this will be his last tip.|The terse limit matches his abrupt change of interest.
34|Rafael questions why it is the last one.|The echo turns toward the upcoming joke.
39|Manuel finds tracking down locations hard and has already lost interest.|Keep his quick admission of boredom after explaining the work.
42|His interests don't last, animals are boring if he can't cook them, and he'll still pass on chance tips.|The cooking joke and the distinction between seeking rumors and hearing one by chance work.
45|Rafael stammers and returns to where the vest is in the New World.|The redirect preserves his reaction to the joke.
50|Manuel guesses it is in the western part.|The hint stays tentative.
53|Rafael asks for a narrower search area.|The short complaint makes the clue's breadth clear.
57|Manuel apologizes and asks Rafael to keep what he heard in mind.|His lack of an exact location remains explicit.
60|Rafael laughs and agrees.|The brief reply ends the exchange amiably.
""",
    129: """
5|Julio asks whether Rafael knows how to make large trading profits.|His guiding question keeps the captain's given-name substitution.
20|Julio starts with the Portuguese island of Madeira, southwest of Lisbon.|The place, political ownership and direction remain explicit.
24|Madeira has goods such as sugar and may be a base for later expansion into Africa and the New World.|The two benefits and company substitution remain separate.
27|Julio urges investing while Madeira has unclaimed market share.|The condition and amount preserve the tutorial recommendation.
30|Julio says to raise funds trading among the three ports, then secure Las Palmas and Verde.|The port list and order of the two steps are clear.
33|Las Palmas and Verde are gateways between Africa and the Mediterranean; Verde yields plenty of local goods for modest investment.|Restore the gateway image and preserve the local-goods implication of investment.
36|Trade between Africa and the Mediterranean at first to fund bigger ships and buy more market share.|The causal use of profits stays explicit.
39|More cargo holds and goods available in towns mean more profit per trip.|The line keeps both constraints on the amount carried and earned.
42|Julio says to expand the trade range progressively.|The short instruction completes the first trading strategy.
45|Commercial investment can bring out new local goods even in towns with no apparent profitable ones.|The means and possibility stay within the tutorial's terms.
48|If they can spare the resources, they could try the New World without overextending.|The advice keeps Julio's caution and the possibility of expansion.
52|Rafael agrees to do his best.|The respectful commitment fits the pupil's reply.
58|Julio asks himself whether things will be all right and pokes fun at his own worry.|The self-deprecating conclusion works in his voice.
62|Julio tells Rafael to try his own approach.|The advice gives Rafael room to act independently.
""",
    133: """
14|Julio suggests bringing Cristina.|The repetition keeps his recollection before the name.
17|Rafael asks who Cristina is.|The question opens the introduction.
22|Cristina is Julio's granddaughter and skilled with a sword.|Both the stated family relationship and skill are preserved.
25|Clau objects to sailing with a woman and almost gives away what he already knows.|The boast and abrupt interruption keep his narrow view and the joke directed at him.
28|Arcadius discreetly warns Clau.|The cough and nickname keep the discreet signal.
32|Clau stammers and insists a woman aboard is a bad idea.|The tag preserves his attempt to find an ally.
35|Rafael supports the idea and sees that a swordswoman could help.|The positive reply answers Clau and keeps Rafael's practical point.
40|Clau objects again and reacts when someone hurts him.|The unassigned reaction avoids inventing who touched him.
43|Arcadius privately asks what difference it makes to have another woman aboard.|The conversational question fits the discreet joke and keeps the aside.
47|Rafael says Arcadius would be more at ease with another woman.|The private reply keeps their understanding and distinguishes it from the public agreement.
52|Arcadius clears her throat and agrees publicly.|The vocal beat separates her two kinds of response.
56|Rafael says women make the voyage more enjoyable and tries to win Clau over.|A single direct question keeps the friendly appeal after the earlier aside.
60|Clau privately complains Rafael is siding with them and gives in.|The given-name substitution and reluctant aside stay intact.
64|Clau publicly agrees if everyone insists.|The reluctant assent follows his private concession.
67|Julio is puzzled.|The silent-looking question preserves his reaction to Clau's change.
71|Rafael asks where Cristina lives.|The direct question turns the decision into action.
76|Julio says London.|The terse answer gives the destination.
80|Rafael agrees and sets their course for London.|The final line confirms their next destination.
""",
    154: """
95|Maldonado's men use force and Spain's backing to do as they please.|The description preserves the political protection behind their abuses.
99|They prey on passing merchant ships for personal gain.|The everyday idiom conveys the point of the raids.
102|Rafael compares this behavior to piracy.|The reaction gives the keeper a cue to confirm Rafael's understanding.
107|The keeper agrees and describes the danger to sailors and harm to his business.|Both consequences stay in the keeper's own account.
111|Clau questions why the keeper trusts them and suggests they might be just as bad.|The direct question challenges the distinction the keeper is drawing.
114|The keeper has heard of their company and trusts it won't mistreat residents.|The question tag and company substitution preserve his appeal.
117|Rafael considers what he heard in silence.|Preserve the pause before the choice and its original glyph.
140|Clau addresses Rafael and trails off.|The native given name and hesitation open the cautious answer.
144|Rafael suspects the problem affects the whole New World and may involve other powers.|The scope and uncertainty matter in his reasoning.
148|Beating Maldonado alone might not fix the problem and even that would need preparation.|The two reasons prevent the next line from sounding dismissive.
152|Having considered the situation, Rafael says they are unlikely to be able to help right away.|His hesitation limits the timing and still addresses the keeper respectfully.
157|The keeper responds with quiet disappointment.|The brief answer preserves the unease before Clau speaks.
161|Clau says the warning was helpful and prompts Rafael.|The given-name substitution and tag retain his prompting role.
164|Rafael says he understands what the locals are suffering and hopes to act soon.|The line keeps empathy and avoids promising an outcome in this branch.
169|The keeper hopes the crew is different from the men he described.|The conditional trust leaves the branch on the right note.
185|In the confident branch Rafael says they should honor the man's trust.|This statement turns the warning into an obligation in the other branch.
190|Rafael urges the crew to defeat Maldonado and bring peace to the New World.|The rallying answer preserves the stronger commitment in this branch.
195|Clau agrees enthusiastically.|The short agreement fits his voice and Rafael's declaration.
199|The keeper anticipates their action and hopes the misery will end soon.|The hope remains distinct from a guaranteed victory.
""",
    169: """
45|The tavern keeper asks Ian to take a drink to a different table.|The work instruction places Ian before the customer who harasses him.
48|Ian agrees.|The brief professional assent fits his manner.
52|A customer addresses Ian as a woman and leers while asking him to pour a drink.|The remark is the customer's deliberate harassment and the wording keeps it in his voice.
55|Ian does not answer.|The silence lets the customer escalate.
59|The customer leers and says Ian is pretty.|The intrusive question and tone explain Ian's mounting discomfort.
62|Ian remains silent.|Preserving the pause keeps the separation before the next insult.
66|The customer questions Ian's gender, remarks on his skin and laughs.|The existing taunt preserves the source while keeping the claim in the customer's mouth.
70|Ian tells him not to touch him.|The direct boundary motivates the startled reaction.
74|The customer cries out in pain.|The outburst follows Ian's abrupt response.
78|The customer stammers and insults Ian.|The insult preserves the escalation.
82|Ian realizes he has made a mistake.|The parenthesized outburst remains his private response.
86|The customer sarcastically complains about his treatment.|The line keeps the pretense of an aggrieved customer.
90|Ian apologizes through a pause.|The reserved apology gives the scene room to turn to the keeper.
94|Rafael asks for a drink from his table.|The interruption redirects attention without claiming Rafael witnessed a specific action.
99|The keeper acknowledges Rafael and then asks Ian to speak privately.|The shift from service to addressing Ian remains clear.
102|The keeper suggests that tavern work does not suit Ian.|Give the understated judgment a single line before he describes the problem.
106|Ian addresses the keeper respectfully.|The title of respect does not imply kinship.
110|The keeper is tired of trouble and says Ian can handle customers without a sword.|Keep the sharp distinction between Ian's reaction and how the keeper expects customers to be handled.
114|The keeper apologizes and dismisses Ian.|The phrasing sounds like a direct but reluctant dismissal.
118|Ian accepts the decision quietly.|The short reply keeps his restraint.
122|Rafael notices Ian's fair complexion and beauty and wonders why he is in this tavern.|Preserve the details Rafael notices while making his curiosity sound natural.
135|Julio says life can take many turns.|The reflective answer stays open about Ian's circumstances.
142|Clau thinks Ian seems too stiff for tavern work.|The blunt assessment provides a contrast with Rafael's curiosity.
145|Rafael proposes talking to Ian.|The question prompts action following the discussion.
""",
}
REVISIONS = {
    (81, 70): ("Well, I'm sure he's no match for me.", ()),
    (81, 94): ("That's the picador. He's the matador's assistant.", ("That's the picador.", "He's the matador's assistant.")),
    (83, 52): ("Nooo! What is it you don't like about me?", ("you don't like about me?",)),
    (83, 59): ("I... understand. I'll give up... Yes... Ah, my love is over...", ("I'll give up...", "my love is over...")),
    (83, 63): ("Whew. He won't be chasing me now.", ()),
    (91, 62): ("I ask whenever a ship comes in. You're the hundredth.", ("I ask whenever a ship comes in.", "You're the hundredth.")),
    (103, 23): ("Just what it sounds like. They say the jaguar god lives in it. I hear it's in the New World.", ("Just what it sounds like.", "the jaguar god lives in it.", "I hear it's in the New World.")),
    (103, 39): ("Finding these things takes work. I'm bored with it already.", ("Finding these things takes work.", "I'm bored with it already.")),
    (129, 33): ("They're gateways between Africa and the Mediterranean. In Verde, you can get plenty of local goods with a small investment.", ("the Mediterranean.", "local goods", "a small investment.")),
    (133, 43): ("(So what's one more woman?)", ()),
    (133, 56): ("Having women aboard will make the trip more fun. What do you say, Clau?", ("What do you say, Clau?",)),
    (154, 152): ("I've thought it over, sir. I doubt we can help right away...", ("I've thought it over, sir.", "I doubt we can help right away...")),
    (169, 102): ("Ian, this work may not be for you.", ()),
    (169, 122): ("He's so fair, and so striking. He looks out of place here. I wonder what brought him here.", ("He's so fair, and so striking.", "He looks out of place here.", "I wonder what brought him here.")),
}


def main():
    FunctionType(prior.main.__code__, vars(prior) | globals())()


if __name__ == "__main__":
    main()
