"""Review the port warning and Sera's first exchanges with Hodram."""

from scripts import review_hodram_B131_B132_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, paired = previous.base, previous.ROOT, previous.paired
OUTPUT = ROOT / "B141_B142_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    141: "Gerhard doubts Diogo's intentions after Maldonado's fall. A townsperson overhears them and explains what the nominal change of ruler means for people who still live under extortion.",
    142: "Hodram reassures an unidentified girl after she escapes captivity, learns of Espinosa's involvement, and considers gaining experience elsewhere. Gerhard or Manuel challenges his reluctance to take her aboard. Hodram communicates first by gesture, then learns Sera's name. Charles returns with news of the prisoners and his own private interest in the New World.",
}
DECISIONS = {
    141: """
5|||Gerhard asks if Escante genuinely means to work with them. His uncertainty follows the apparent alliance.
9|Hard to say. I'd give it even odds.|I'd give it even odds.|Hodram bases his answer on a fifty-fifty judgment. The conversational estimate stays deliberately inconclusive.
12|||Hodram hopes Escante is not using Maldonado's loss of power to pursue a scheme. The speculation belongs to Hodram.
16|I've heard people are still being exploited, even in the areas freed from Maldonado's pirate rule.|still being exploited,;Maldonado's pirate rule.|Gerhard cites reports of continued suffering and exploitation after liberation. His evidence remains hearsay.
19|||Gerhard suspects Escante may be repeating the conduct they opposed. Keep the possibility distinct from certainty.
22|||Hodram suspects that exploitation is widespread across the New World and will be hard to solve. His statement keeps the broader extent and the qualification.
25|||The townsperson overhears the conversation and checks that this is the crew who defeated Maldonado.
29|||Hodram confirms the deed in a short answer and lets the townsperson explain why it matters.
33|While you're at it, you could take down Escante, too.|While you're at it,;take down Escante, too.|The townsperson suggests treating Escante the same way. The dry phrasing carries bitterness rather than implying an agreed mission.
36|How do you mean?|How do you mean?|Gerhard asks what the suggestion means. The direct question opens a space for the man's explanation.
40|You said it yourselves. Maldonado and Escante are cut from the same cloth.|You said it yourselves.;cut from the same cloth.|The townsperson uses a familiar comparison to say the rulers are of the same kind.
44|Makes no difference who's in charge. We live with threats and shakedowns either way. It's hell.|who's in charge.;threats and shakedowns;It's hell.|The townsperson describes the same threats and extortion under either ruler. His bitter conclusion stays personal.
48|||Hodram lets the man's testimony hang without answering. The separate silence gives the exchange its weight.
""",
    142: """
5|Girl from Abroad: Ah...|Girl from Abroad:|The embedded label identifies an unfamiliar girl from another country before she gives her name. The role caption and her initial hesitation stay separate on screen.
8|What's wrong? You're safe while you're in town. Even slave traders won't break the law in front of a crowd.|safe while you're in town.;slave traders;in front of a crowd.|Hodram says she is safe in public because the traders will not openly break the law there. His reassurance is local to the town.
11|Girl from Abroad: ...|Girl from Abroad:|The unidentified girl falls silent after Hodram tries to reassure her. Keep the same label and preserve a genuine pause.
14|||Hodram realizes she may not understand his words. The hesitation lets the player see that he has yet to solve that problem.
19|||Gerhard announces that they have identified the smuggling fleet. Preserve the subject and the military address.
22|||Hodram prompts Gerhard to continue. The short reaction leaves the information with him.
27|||Gerhard says the fleet apparently works for Geronimo de Espinosa. Keep the approved name and his qualifier.
31|||Hodram recognizes the name and reacts with a pause followed by an exclamation.
44|||Manuel has heard of Espinosa. His brief remark stays distinct from Gerhard's list of rumors.
51|||Gerhard cites the long-standing rumors of trafficking, drugs and poaching. Keep all three attributed to rumors.
54|In public, he's a powerful man with a grip on most of Africa's trade. We've made a dangerous enemy.|most of Africa's trade.;made a dangerous enemy.|Gerhard contrasts Espinosa's public trading power with the rumors. He concludes they now face a dangerous opponent.
70|He's far too powerful for us to take on right now.|far too powerful;right now.|Hodram gauges Espinosa against their current strength. The judgment is about when they can take him on.
73|||Gerhard leaves a separate moment of silence after Hodram concedes their disadvantage.
84|||Hodram recalls the pirate's advice about making a name in the Caribbean and considers giving his crew experience in the New World.
87|||Gerhard says they cannot hope to beat Espinosa if they cannot manage a voyage of that distance. Keep the condition and its implication.
90|We could get some practice by taking on Caribbean pirates.|taking on Caribbean pirates.|Hodram proposes fighting Caribbean pirates to train the crew. Keep the specific region and target.
93|||Gerhard praises the idea and suggests that trade on the round trip could bring in money to arm the fleet. The outcome is still a possibility.
109|Girl from Abroad: ...|Girl from Abroad:|Her silence shows she is still with them before Gerhard notices her again. Keep the same heading.
112|||Gerhard notices that the girl has remained near the crew. His question fits the interruption.
116|||Hodram says she has been following him wherever he goes. He names no relationship or motive for her.
126|I suppose that's that. Maybe you were meant to meet. Why not let her stay with you, Admiral?|meant to meet.;stay with you, Admiral?|Gerhard advises letting her stay after she chooses to follow Hodram. His register remains more measured than Manuel's alternative.
132|||Manuel gives the same advice in a chuckling, easy register. Keep fate as his interpretation rather than a fact.
139|||Hodram objects to taking a civilian aboard and adds his objection to taking a woman aboard. Preserve his own attitude and the period setting.
148|||Gerhard challenges the consequences of leaving her and warns that her appearance makes her an obvious target. The warning stays in his voice.
151|||Hodram pauses to consider Gerhard's warning. The short hesitation precedes the diverging replies.
155|It's your call, Admiral. I'll go get ready to sail.|It's your call, Admiral.;get ready to sail.|Gerhard leaves the decision with Hodram and returns to departure preparations. His response ends this version of the advice.
159|You'd leave her here? That tavern is full of predators. Do you really think a pretty young woman with no one to turn to will be safe alone?|That tavern is full of predators.;with no one to turn to;be safe alone?|Manuel makes his own warning more pointed and asks whether she would be safe by herself. Keep his appraisal and concern, with no new statement about her background.
162|...What's with that grin?|What's with that grin?|Hodram notices Manuel's expression and challenges him after the warning. The pause keeps his suspicion distinct from the spoken question.
165|Oh, nothing at all. I'd best get back to getting us ready to sail. Heh heh.|nothing at all.;ready to sail.|Manuel laughs off the implication and excuses himself to finish preparing. His chuckle preserves the contrast with Gerhard's response.
169|||Gerhard again leaves the decision to Hodram and excuses himself. Preserve its own alternative.
176|||Hodram admits he does not know what to do. The pause shows his reluctance before he asks her.
179|Girl from Abroad: ...|Girl from Abroad:|The girl remains present and silent while Hodram considers what to ask. Preserve the heading through this pause.
182|...Do you want to... come with us?|come with us?|Hodram hesitates twice while inviting her along. His imprecise attempt to communicate leads to the nod.
186|Girl from Abroad: ... (She nods.)|Girl from Abroad:;(She nods.)|She nods without speaking. Retain the action in parentheses and the label because she has yet to give her name.
189|||Hodram is startled by the nod and asks whether she understands. He has not yet concluded she understands his words.
192|Girl from Abroad: ...|Girl from Abroad:|Her silence leaves the startled question unanswered.
195|||Hodram infers that she read his expression and gestures. The uncertainty belongs to his interpretation.
199|||He decides that she can stay until they learn who she is. Keep the temporary condition and the grudging beginning.
203|||Hodram asks what to call her and tries the direct word name. Preserve the brief transition from decision to introduction.
206|Girl from Abroad: ?|Girl from Abroad:|The question mark is the girl's only response to the request for her name. Retain the heading and the silent confusion.
209|||Hodram recognizes that the first attempt did not work. His short reaction leads to a demonstration.
213|||Hodram gives his own name as an example and repeats it three times. All three original FI substitutions belong to the speech.
217|Girl from Abroad: ...FI...?|Girl from Abroad:|She tries his name uncertainly for the first time. Preserve the original single FI and the pauses.
220|||He encourages her and repeats his name. Keep the original FI substitution in its own turn.
223|Girl from Abroad: FI...|Girl from Abroad:|She manages his name but trails off. Preserve one runtime name and her continuing hesitation.
226|||Hodram asks whether she understands. His short question gives her room to try again.
230|Girl from Abroad: FI!|Girl from Abroad:|She says his name with new confidence. Keep one runtime name and the exclamation.
233|||Hodram thinks she understands, gives his name once more, and asks for hers. The original FI remains separate from her reply.
237|Girl from Abroad: ...|Girl from Abroad:|She hesitates again when asked for her own name. The heading still reflects what the crew knows.
240|||He rephrases the question and asks what to call her. The patient repetition fits his attempt to communicate.
243|Girl from Abroad: ...Sera.|Girl from Abroad:|She finally says her given name while the original embedded label is still active. Preserve the transition to the visible Sera nameplate on the later native command.
246|...Sera? Is that your name?|Is that your name?|Hodram repeats the sound and checks that he heard her name correctly. The tentative question fits his first success.
250|||Sera hesitantly gives her full name. Preserve every part of Sera Altos Shahrbaraz in the spoken introduction and the move to her native nameplate.
253|||Hodram stumbles over the full name and checks that he can call her Sera. His hesitation and the recurring given name fit the scene's humor.
258|||He notices her smile and remarks on it. The surprise is a distinct beat before Charles interrupts.
270|||Charles asks for Hodram's attention. The uncertain call interrupts him.
274|||Hodram reacts with a short startle before replying to Charles. Keep both visible punctuation marks.
278|||Charles asks what is wrong. His short question fits Hodram's reaction.
282|||Hodram says it is nothing and asks why Charles came. His initial pause preserves the abrupt shift back to duty.
286|||Charles reports that the prisoners have all been released. Keep the distinction from an instruction to free them.
290|||Hodram is pleased and commends Charles. His brisk change of tone leaves Charles momentarily confused.
293|||Charles's silent questions convey his confusion. Keep them as a separate response.
317|||Charles remembers that he wanted to ask about travel to the New World. His interested question opens the final exchange.
320|||Hodram confirms the plan briefly. His hesitation reflects the abrupt change of subject.
324|||Charles is pleased that it is true. The repetition shows interest without revealing the reason.
327|Why? Is there something you want to see in the New World?|something you want to see;in the New World?|Hodram suspects Charles has something particular in mind. The conversational follow-up leaves it to Charles to say what it is.
330|Oh, it's nothing. Just something personal. So we're really going...|Just something personal.;we're really going...|Charles keeps his reason private and repeats his interest in the news. The last thought leaves Hodram puzzled.
333|||Hodram's silent question ends the scene without resolving Charles's private interest.
""",
}
review = checked_text(previous.review, {"len(records) == 77": "len(records) == 81"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::port-and-Sera", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

