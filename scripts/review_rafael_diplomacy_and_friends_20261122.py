"""Revisit Rafael's complete Pereira, Eirene and Charlotte conversations."""

from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from types import FunctionType

from scripts import register_current_story_wraps_20261122 as parent
from scripts import review_current_story_wraps_20261122 as established


base, native = parent.base, parent.native
ROOT = Path("work/analysis/rafael_diplomacy_and_friends_20261122")
REVIEW = ROOT / "contextual_review.json"
PREFLIGHT = ROOT / "native_preflight.json"
ARCHIVE = "/data/SC0.DK4"
CONTEXTS = {
    60: "Pereira verifies the Proof or its key, tests Rafael's reasons for opposing Spain, and answers the player's approach to the fight with Kuhn. Rafael wants to restore Portugal without leaving the Spice Islands exposed. The two consider who stays behind and when to challenge Valdes or Kuhn.",
    63: "Clau confronts Rafael over asking Eirene to do heavy work. Rafael talks privately with Eirene, who appears publicly as Arcadius, and receives reassurance instead of blame. Clau is cheerful after dinner as she predicted.",
    64: "The crew intervenes in a predatory bargain. Charlotte takes offense at Rafael's offer, returns to apologize and make a proper sale, and tells him how her Romani community was tricked into moving to the New World. Clau softens as he learns what her request cost her.",
}

# Record | faithful meaning | replacement when needed | protected phrase groups | reason
DECISIONS = {
    60: """
6|Pereira recognizes Rafael by surname.|||Keep the abrupt recognition and surname substitution.
17|He asks if Rafael brought the Proof.|||Proof is already understood in their exchange.
21|Rafael has the required key for the search.|||The distinction between the required key and the Proof itself matters.
25|Pereira considers what he has been told.|||The brief hesitation fits before the conditional confirmation.
31|Rafael found the promised Proof in East Asia.|||Keep the named region and the promise.
35|Pereira verifies that the Proof is authentic.|||All right carries his matter-of-fact confidence.
41|Pereira invites them to follow.|||The casual invitation respects his clipped register.
44|His position prevents him from helping openly.|||Keep the difference between public support and private sympathy.
48|Rafael pauses before answering.|||The silent reaction is the entire beat.
53|Kuhn and Spain are enemies to both of them.|||The repetition turns a shared goal into a blunt statement of common enemies.
57|Rafael asks why a shared enemy cannot justify an alliance.|||The questions keep his earnest reasoning and name both enemies.
62|Pereira says the situation is more complicated.|||The clipped answer sets up Rafael's question.
66|Rafael asks why.|||The simple challenge follows directly.
71|Pereira asks who Rafael's true enemy is and tells him to think first.|||The two questions and direct instruction retain the pressure of the challenge.
75|Rafael repeats the question to himself in surprise.|||The unfinished thought lets the choices follow.
111|Pereira asks if they dare oppose Spain's Armada after Albuquerque joined Spain.|||The familiar reminder preserves the political and personal stakes.
114|Rafael says they are entirely serious.|||The emphatic reply suits him.
119|Pereira checks if they would act without his help.|||His apparent withdrawal is a test and the questions preserve that turn.
123|Rafael vows to defeat Spain and restore Portugal even without aid.|||Keep the time contingency and the two objectives.
127|Pereira takes a beat before answering.|||The original silence marks a change in his judgment.
131|Pereira says this makes the decision simple.|||The change of tone follows Rafael's conviction.
135|Rafael is puzzled.|||The single question mark conveys wordless surprise.
140|Pereira says opportunistic patriots make dangerous allies.|||Waving the flag and the dozen-lives exaggeration carry his contempt.
143|Pereira realizes his worry was needless and expresses confidence in Rafael.||worrying over nothing.;You'll do just fine.|Keep the informal reassurance and put each thought together.
147|He urges them to beat Kuhn and get back to Portugal.||finish off Kuhn;back to Portugal!|Keep his urgency and give the linked actions readable wraps.
150|Rafael reacts to Pereira with feeling.|||His surname is a respectful direct address here.
155|Pereira hands over the item.|||The short commands let the action convey the gift.
160|Rafael asks what he has been given.|||The hesitation reads as surprise.
165|It is said to be a key to deciphering the Proof map and Rafael should earn it.|||The key retains its exact function and the challenge keeps Pereira's voice.
169|Clau asks if they can keep the gift.|||The blunt question is natural and leaves ownership with Pereira until he confirms.
173|Pereira has no interest in collecting seven and gives it to them.||collect all seven?|Use the space in the shared gift exchange without weakening his dismissive joke.
177|Rafael asks to make a pact against Kuhn then and there.||here and now.|Keep the immediate request and avoid weakening the emphatic time phrase.
182|Pereira asks what Rafael proposes.|||The question invites the next decision.
201|Rafael proposes joining forces and defeating Kuhn first.|||The existing two lines express the proposal and its first objective without an awkward split.
205|Defeating Kuhn would secure their rear, and Pereira would struggle against him alone.|So we won't have to worry about him at our backs. Even I'd have a hell of a time taking him on alone.|at our backs.;taking him on alone.|This branch proposes removing the threat, while the later branch specifically asks Pereira to stay and handle it.
208|Rafael would expect Spain's king to end the Portuguese royal family's claim permanently.|||The hypothetical first person and the urgent conclusion are both necessary.
212|Victory over Kuhn would give Rafael the strength to face Valdes unaided.|||The order and the promise to fight without Pereira are clear.
217|Pereira thinks fighting alone is reckless.|||The rapid objections convey his disbelief.
220|Pereira is responsible for these waters and cannot leave his post at will.|||The post is a concrete responsibility in Rafael's argument.
225|Pereira is ready to rebel against Spain and dismisses the concern about his office.|||The outburst carries the force of his swear and the confrontation.
229|Failure would cost him the governorship of Indochina permanently.|||Keep the specific post and the permanent consequence.
234|Pereira laughs because he already knows the risk.|||The rhetorical question makes his reaction recognizable.
238|Portugal needs someone to entrust its future to if Rafael fails.|||Rafael's sharp correction explains that he is protecting more than a title.
242|Pereira reacts without words.|||Keep the abrupt visual reaction.
246|Europe wants the Spice Islands and holding them might let Portugal match Spain one day.|||The hypothetical time horizon and equal terms stay intact.
250|Rafael can fight wholeheartedly if Pereira stays as Portugal's last defense.|||The appeal depends on the prior explanation of the islands, and the existing voice is earnest.
255|Pereira gives a short amused sound.|||A beat before his louder laugh fits the change in mood.
259|Pereira laughs and admires Rafael's thinking.|||Piece of work works as admiring surprise in this sequence.
263|Pereira commits to Rafael and takes responsibility for what follows.|||Betting on you captures the decision without changing the agreement.
267|Rafael accepts and relies on him.|||The respectful assent follows naturally from Pereira's offer.
273|Pereira asks what Rafael means.|||The surprise introduces the alternate plan.
277|Rafael intends to leave Southeast Asia immediately.|||Keep both the region and the timing.
281|Pereira prompts Rafael to finish.|||And then is an appropriately short prompt.
285|Rafael plans to face Valdes in Europe.|||The target and intended destination remain plain.
289|Pereira is taken aback.|||A repeat question carries surprise rather than confusion about the words.
293|Spain's king has an incentive to extinguish Portugal's royal claim, so time is short.|||Retain the matching speech from the first plan.
297|Pereira asks whether the plan means putting Kuhn off.||you're leaving Kuhn for later?|Carry the complete question across the turn after his acknowledgment.
301|Rafael entrusts the Southeast Asian waters and Kuhn to the governor of Indochina.||governor of Indochina.;leaving it all to you.|Pay off his No and carry the title and delegation as complete phrases.
306|Pereira understands that he is being asked to hold their rear.||cover your rear.|The speaker now really is being entrusted with the rear, and his rough voice works.
309|With someone he trusts looking after these waters, Rafael can commit fully against Valdes.|Yes. If we know these waters are in good hands, we can give Valdes everything we've got.|in good hands,|These waters refers to the same jurisdiction in the preceding line, and Rafael speaks with trust.
314|Pereira laughs that Rafael already has him figured in as a piece in the plan.|||The board metaphor is readable and preserves the playful discovery.
318|He agrees, then asks what happens if he drives Kuhn out himself.|||The new condition leads directly to the trading-rights answer.
322|Rafael has the key and can concede the region's trading rights.|||Concession and gift remain distinct from each other.
327|Pereira jokes about pity and challenges Rafael to take the region from him too someday.|||The mock-offense is clearly playful in this exchange.
330|Rafael stutters in protest.|||Keep the interrupted objection.
335|Pereira appeals to fairness and free competition in trade.||to be fair, right?|Keep his leading question and the brief follow-up together on their respective rows.
338|Rafael agrees reluctantly before trying to object.|||The stammer keeps his embarrassment.
343|Pereira insists that Rafael see to beating Valdes.||take down Valdes. Got it?|The obligation is blunt and the final tag follows the order.
346|Rafael agrees without reserve.|||The immediate response closes the agreement.
354|Pereira considers whether Rafael's crew really could restore Portugal.|||The repetition is his change from doubt to measured belief.
362|Pereira pauses before changing questions.|||Keep the thought beat.
366|Pereira asks Rafael by surname who has the world's greatest power.|||Preserve FA and the superlative in his question.
370|Clau assumes power means the largest trading network and considers his own company.|||The unfinished alternative permits Pereira to interrupt.
374|Pereira means who has the best chance of conquering the world.|||The clarification reframes commercial influence as strategic advantage.
377|Rafael guesses Spain and its Armada.|||The question keeps it tentative.
382|Pereira grants the point and asks if Rafael knows the Spice Islands.|||The source surname and conversational handoff are intact.
386|Rafael identifies the islands as nearby.|||The simple confirmation preserves the immediate geography.
391|Pereira says the Spice Islands are a treasure to present-day Europe.|||The valuation comes from Europe and the final question keeps Rafael engaged.
394|Rafael says yes after a pause.|||Keep the hesitation as he realizes the stakes.
399|The region's goods yield vast profits that could finance conquest.|||The trailing thought gives Rafael the chance to finish the argument.
402|Rafael realizes its ruler could take over the world.|||The realization answers Pereira's unfinished line.
407|Pereira confirms Rafael understands.|||The blunt confirmation is characteristic.
411|Clau is outraged by the idea of Antony Kuhn ruling the world.|||The incredulous repetition and rough dismissal work together.
423|Jam says he himself would never allow it even if God did.|||This optional reaction preserves his personal resolve and the religious image.
430|Rafael realizes supremacy in the Spice Islands may mean supremacy in the world.|||His paraphrase emphasizes the conclusion, and the conditional is right.
442|Fernando says it cannot be explained by luck alone.|||The optional remark keeps his practical skepticism.
448|Pereira sees that Rafael grasps the situation.||you're starting to get the picture.|The conversational phrase should read without a break after you're.
451|Pereira avoids open war with Kuhn because nobody could stop Kuhn if Pereira lost.||I'm holding back;no one left to stop him.|Protect the admission and its consequence while preserving the two sentences.
454|Rafael digests the warning silently.|||The pause prepares Pereira's next teaching point.
459|Restoring Portugal matters but fixation on it could hand Kuhn the world.||all we think about,;hand him the world.|Protect the conditional thought and its consequence without altering the warning.
462|Rafael asks what they should do.|||The concise question fits the shift to an actionable plan.
467|Pereira orders Rafael to beat Valdes and gain the skill to take on Kuhn together.|||Keep the preparatory fight and explicit future partnership.
470|Rafael thinks of both Valdes's fleet and Spain's Armada.|||The two distinct opponents should remain separate as he weighs the plan.
474|Pereira says he would permanently deprive Portugal's royal house of its claim.|||The parallel with Rafael's earlier reasoning is clear and the urgency is direct.
477|Pereira can offer full help once Spain is checked and Portugal restored.|||Preserve both conditions and the scope of support.
481|Rafael accepts the logic.|||His quiet acknowledgment leaves room for the last clue.
486|Valdes should know where the Mediterranean Proof is, and Kuhn is harder still.|||The mustache insult and hundred-year exaggeration keep Pereira's voice.
489|Rafael promises to come back after defeating Valdes.|||The promise concludes the strategic exchange naturally.
493|Pereira relies on Rafael and addresses him as Admiral by surname.|||The title and FA substitution are supported by the source.
""",
    63: """
5|Clau calls Rafael by given name and asks him to come to the inn.|||Keep the private invitation and original given-name substitution.
9|Rafael is surprised but agrees.|||The brief affirmative follows naturally.
14|Clau tells Rafael to spare a thought for her.||think about her for a second?|The unresolved her starts the quarrel, and the complete question belongs together.
18|Rafael needs to know what Clau is referring to.|||The puzzled questions keep that he has not recognized the reason.
22|Clau names Eirene and asks about the heavy work.||help with the heavy lifting;didn't you?|Move the work and confirmatory tag in whole phrases.
25|Rafael says she only helped a little.|||His defensive minimization is the point.
30|Clau says Eirene is less robust and deserves special consideration.|That's not the point! Eirene isn't as healthy as the rest of us. You've got to look out for her!|look out for her!|The comparison is about her health and resilience in context. Keep his emphatic rebuke.
34|Rafael explains that circumstances called for it.|||His hesitant defense invites the angry reply.
38|Clau rejects the idea that a reason excuses everything.|||The pointed question lets him raise his voice without new accusations.
41|Rafael protests the intensity of Clau's anger.|||The simple complaint escalates the row naturally.
46|Clau withdraws and tells Rafael to do as he likes.|||The curt dismissal preserves his mood.
52|Arcadius asks what's wrong using Rafael's given name.|||Keep the concerned question and FI.
55|Rafael recognizes Arcadius and says something is on his mind.|||His public address is still Arcadius here.
60|Arcadius heard Claudio raising his voice.|||The tentative report avoids claiming to have heard the content.
63|Rafael worries that Arcadius overheard the substance of the argument.||Did you hear what|The aside starts the reaction; keep the question lead in one row.
67|Arcadius did not hear the actual words.|||Couldn't make out the words is natural and gives Rafael room to explain.
71|Rafael asks for a private word.|||The short request signals that he is preparing to confide in her.
75|She agrees after a beat.|||The reply keeps the quieter pace.
79|Rafael uses Eirene privately and says they were talking about her.|||The name switch marks the change of register.
84|Eirene is surprised to be the subject.|||Me is the right brief reaction.
88|Rafael reports Clau's anger and reminds her of her helping with heavy work.|||The remembered incident stays the same as in the argument.
92|Nobody else was there, and refusing would look odd given her public identity.||Wouldn't it look odd;didn't help?|Keep the start of the question together. The dialogue keeps Eirene's reasoning about the disguise.
95|Rafael says he gave Clau that explanation but could not calm him.|||Keep the practical defense and unresolved anger.
100|Eirene listens silently.|||The silence leaves space for Rafael to continue.
104|Clau shouted one-sidedly and walked out.|||Stormed out is a natural reading of the abrupt angry exit.
108|Rafael thought he was looking after Eirene as well and feels unfairly treated.||looking out for you too,|His defensive turn is vulnerable here and the words already capture it.
113|Eirene apologizes for the difficulty caused by concealing that she is a woman.|||The current line keeps her responsibility in her own voice and preserves FI.
117|Rafael denies she's to blame and apologizes for venting.|||The informal apology acknowledges her kindness.
122|Eirene recognizes how hard he works as admiral.|||Keep the rank supported by the source and his original given name.
126|His efforts are why the crew feels safe on the ship.||we all feel safe at sea.|The warm reassurance is faithful and fits as a complete statement.
130|Rafael is embarrassed by the unexpected compliment.|||Making me blush is conversational and keeps his curiosity.
134|Eirene says nothing is wrong and asks him not to overwork himself.|||Keep the gentle turn of concern and FI.
138|Rafael says her name softly.|||This beat belongs to the emotional exchange and should remain short.
143|Eirene tells him he can lighten his worries by talking to someone.|||Even if you're just venting fits the situation.
146|Rafael compares her to a big sister.|||Like makes the simile explicit without suggesting actual kinship.
150|Eirene is surprised by the comparison.|||The short question suits a tentative response.
154|Rafael already feels better and thanks her for listening.|||The informal thanks pays off her advice without added intimacy.
159|Eirene apologizes for the trouble she feels she caused.|||The exchange of apologies keeps her concern distinct from Rafael's.
162|Rafael and Clau have never had a fight this bad, and he still does not know how to handle it.||never fought like this before.;and I still don't.|Keep the confession and afterthought in natural groups.
166|Eirene predicts Clau will forget about it after eating.|||The casual advice sets up the later comic proof.
170|Rafael doubts it.|||The small question keeps the conversational rhythm.
175|Eirene says that Claudio is easy to read and suggests eating.|||The restrained joke translates his simplicity without belittling him.
179|Clau asks Rafael cheerfully whether he ate enough.|||The given-name substitution and loud greeting show the prediction was right.
182|Rafael gives a nervous yes and starts to address him.|||The stutter and trailing name show uncertainty.
186|Clau asks why Rafael looks strange.|||The joking wording maintains his good mood.
189|Rafael stammers and says he noticed Clau's good mood.|||Keep the evasive impression rather than making it a reconciliation speech.
193|Clau shrugs off the odd reaction and goes on ahead.|||The abrupt departure fits the prediction.
197|Rafael realizes Eirene was right and Clau has forgotten the quarrel.|||The first clause and ellipsis keep the realization quiet.
202|Rafael marvels at how well Eirene reads Clau and wonders about her scholarly insight.|||The half-serious question preserves the little joke without inventing a relationship.
""",
    64: """
5|Rafael is surprised to find a village here.|||The informal surprise works as the opening.
9|Clau finds the village lonely and lacking life.|||He judges how the village looks without making claims about its people.
12|Rafael notices that ships from other countries berth here too.||There are ships;docked here, too.|Avoid leaving There at the end of the first row.
17|Rafael notices the commotion over there.|||The question captures surprise without assuming its cause.
21|Clau guesses that something has happened.|||Looks like trouble is a natural cue to investigate.
25|Rafael suggests going to see.|||The quick invitation moves them into the scene.
31|Charlotte says the trader previously offered more money.|||She challenges a lower offer without implying a sale was completed.
35|The trader will not offer a penny more for today's lot.|||The familiar idiom preserves his dismissal and temporal distinction.
39|Charlotte insists she selected the village's best goods.|||The question and emphatic claim give her a credible defense.
43|The trader repeats her claim with skepticism.|||The trailing line sets up the aggressive demonstration.
47|The trader calls the goods flimsy and roughly demonstrates it to justify the insultingly low price.||I'm not paying full price;See? See?!|The physical demonstration is already implied in the exchange. Keep his refusal intact.
51|Charlotte tells him to stop damaging the villagers' work.|||The sharper threat and reason make sense after the demonstration.
55|The trader yells in pain and lashes out at her.||What the hell are you doing,|Use more of the first row so the emphatic question reads through to its coarse address.
58|Charlotte cries out.|||The brief exclamation carries the immediate reaction.
62|Rafael intervenes and says a man should not hit a woman.|||The line reflects Rafael's stated objection in the source.
67|Clau challenges the trader to take him on instead.|||A blunt challenge fits the intervention.
71|The trader makes a dismissive sound.|||The short reaction closes his part in the confrontation.
75|Clau observes the man bolted.|||The gruff dismissal is natural.
79|Rafael checks whether Charlotte is all right.|||The immediate concern should remain direct.
84|Charlotte does not answer.|||The silence gives the crew a moment to change tack.
88|Clau condemns the treatment and asks if the man picked a fight.|||The question shows that he witnessed the conflict without knowing its origins.
91|Rafael sees the goods and offers to buy them as a favor.|||Help you out leaves the unintended condescension that Charlotte reacts to.
95|Charlotte indignantly echoes his offer to help.|||Echoing the same words in English lets the line land as a direct reaction.
98|She says a sheltered young man cannot understand her and rejects pity.|||Rich boy preserves the pointed assumption she voices, and her refusal is direct.
102|Clau is outraged that their help earned a scolding.|||Tongue-lashing fits his irritation and the informal line.
106|Rafael privately wonders whether their manner offended her.|||The self-question begins his realization without immediately blaming her.
111|Clau thinks a rescuer deserves better than abuse.|||The current line captures how he sees the situation at this point.
114|Rafael steers Clau toward a meal and a chance to cool off.|||The light line turns the exchange without dismissing Charlotte outright.
119|Julio reacts to the report at the meal.|||The acknowledgment introduces the recollection naturally.
123|Clau repeats how angry he is with Charlotte.|||A rhetorical question and a dismissive tag fit his continuing indignation.
126|Rafael recognizes that offering a favor probably sounded patronizing.|||The callback to help her out is deliberate and clear.
130|Rafael admits feeling sorry for Charlotte, understands her anger and worries he hurt her.|||The anxious questions preserve the emotional progression before reassurance.
134|Arcadius asks Rafael to stop dwelling on the past.|||Keep the gentle address and given-name substitution.
138|Arcadius says the important thing after recognizing an error is to avoid repeating it.|||The current advice sounds kind and practical.
141|Julio says helping those in need is part of who Rafael is.|||The personal our and FI keep Julio's warm solidarity.
144|Julio says the approach was clumsy but Charlotte likely understood the good intention.|||He reassures Rafael without denying the mistake.
147|Rafael thanks the others.|||The softened reaction fits the reassurance.
152|Clau objects to being insulted without thanks and starts to shift the blame.|||The cut-off conclusion makes his next retreat believable.
155|Clau gives up arguing and calls his shipmates a bunch of softies.|||The affection beneath the complaint is already audible.
158|Clau is full after the meal.|||The short contented reaction resets the scene.
162|Charlotte hesitantly calls for their attention.|||The stammer-like start conveys her effort to come back.
166|Rafael is surprised.|||A short response leaves room for Clau's recognition.
171|Clau recognizes Charlotte and calls her rude.|||The wording is echoed by Arcadius later, which preserves the mild rebuke.
174|Charlotte timidly asks Rafael to buy the goods after all.|||The unfinished, halting line fits her shift in attitude.
177|Clau calls out the reversal after her emphatic refusal.|||The incredulity and admonishment preserve his anger.
181|Charlotte says the purchase is voluntary.|||The nervous acknowledgment respects the previous insult and her lack of leverage.
184|Clau says that much is obvious and defers to Rafael.|||Keep FI and the agency of Rafael's reply.
187|Rafael will decide after inspecting the goods and asks her to bring them to the port office.|||The location and the conditional approach remain plain.
191|Charlotte thanks him and promises to bring the goods for him to see.|||Her eager answer matches Rafael's restrained offer.
194|Rafael warns that the answer may disappoint her.|||No promise to buy is the specific immediate uncertainty.
198|Charlotte is taking a chance and has nothing to lose by asking.|||The colloquial line conveys the meaning of ダメモト.
202|She struggles to find the words before apologizing.|||The two audible hesitations let the apology build.
206|Charlotte apologizes for earlier and stammers.|||The direct apology has a different tone from her first encounter.
210|Rafael is caught off guard.|||The interjection is a natural small beat.
215|Charlotte says she will see them later.|||The quick exit follows her embarrassment.
219|Julio sees that Charlotte is good at heart after all.||She's got a good heart after all.|Keep the full recognition together after his brief response to the apology.
222|Arcadius calls Clau's label for Charlotte harsh.|||The exact echo of rude woman helps connect the remarks.
225|Clau protests that Charlotte insulted them on her way out.|||His account is emotional and follows his earlier complaint.
229|Clau calls it nerve to reject pity and then ask them to buy.|||The two quoted fragments work as his paraphrase of her reversal.
232|Arcadius reframes her behavior as courage.|||The short line answers Clau without a lecture.
235|Julio points to her embarrassment and says she put pride aside for her family and village.|||The physical detail and beneficiaries explain why her asking was brave.
239|Rafael agrees that Charlotte is a good person.|||The soft assessment follows Julio's compassionate explanation.
244|Clau sees what they mean.|||The hesitation marks the moment he reconsiders.
248|Clau abruptly urges the crew to prepare to unload.|||Keep his energetic reversal and the direction of the cargo movement.
252|Rafael says Clau is getting ahead of the negotiations.|||The reference to price is natural in the trading sequence.
256|Clau offers that Rafael can skip the inspection and buy everything.|||Keep the original given name and Clau's assertiveness without turning his suggestion into an order.
260|Rafael is startled and stammers Clau's name.|||The line is a reaction to the emotional reversal.
265|Julio admits Clau is pushy and says he likes his directness.||That's what I like about Clau.;right to the point.|The compliment and its reason deserve complete reading groups.
269|Arcadius agrees.|||The short assent answers Julio's affectionate aside.
274|Rafael confirms their deal.|||A firm statement establishes where the transaction becomes real.
279|Charlotte thanks him and looks forward to reporting back to the village.|||Keep the communal purpose that motivates her trip.
283|Rafael offers his own given name and asks hers.|||The introduction and original substitution are both present.
287|She repeats Rafael's given name and introduces herself as Charlotte.|||Preserve FI and the agreed spelling Charlotte.
290|Rafael asks why she and her people built on such unproductive land.|||The question opens her account and the reference to the village is clear.
295|Charlotte identifies her people as Romani and recalls their travels through Europe.|||Romani fits the self-identification and is consistent with her account of prejudice.
298|She remembers keeping up as a child while her mother held her hand.|||The personal memory carries the transition to the migration story.
301|Someone invited them to resettle in the New World.|||Leaving the unidentified promoter unnamed retains what Charlotte knows.
305|The recruiters told them about plentiful gold and vast untilled fertile land.||gold everywhere,;no one had touched.|Keep the abundance, fertile land and promises as reported speech. Miles suits the colloquial claim of a vast area.
309|The group pooled the little money they had and agreed to cross the ocean.|||Scraped together conveys the hardship without inventing a sum.
313|Her parents and the others hoped to have land and a village of their own.|||The hopeful phrasing is a deliberate contrast with the next beat.
316|Hope quickly gave way to despair.|||The simple sentence lets the realization land.
319|Digging blindly turned up no gold mines and there was wilderness as far as they could see.|||The English keeps the futility of the effort and the barren setting.
322|Rafael condemns the deception used to take their money.|||The accusation goes to the recruiters' motive and follows her account.
326|The community encouraged each other and decided to establish a village despite its despair.|||Kept each other going carries the collective effort.
330|They had never owned land and struggled to grow crops after settling.|||The hardship is her report about this group, and the chronology remains clear.
333|Rafael asks whether they considered returning to their country.|||His well-meant assumption sets up her correction.
337|Charlotte says the Romani have no country of their own to go back to.||There's nowhere to go back to.|Keep Romani and Charlotte's reply in her own voice without breaking There's from its clause.
340|They were blamed for missing things and for serious diseases.|||The existing parallel does not repeat the label as a slur.
343|Charlotte says people in Europe regarded them as something filthy.|||Like we were dirt expresses the prejudice from her perspective.
347|Rafael listens in silence.|||The silence gives her account room before the recovery.
352|Two or three years ago the harvest finally fed them and they had a village of their own.|||Preserve the timeline, self-sufficiency and pride.
355|A ship stopped about a year ago and made barter for new goods possible.|About a year ago, a ship happened to stop here. We've been trading for new goods ever since.|trading for new goods|The account is about exchange of goods in context, and the phrasing sounds like Charlotte telling the story.
358|Even so, traders often pay next to nothing, as the earlier offer illustrates, and the villagers have little choice.|Even so, we often have to sell for next to nothing. You saw what it's like. We don't have much choice.|next to nothing.;You saw what it's like.|The comparison is to how that trader behaved, and this scene shows his offer ending without a sale.
363|Charlotte tells Rafael she was truly happy when he stood up for her.|||Keep FI, the stutter-like hesitation and her relief.
367|She never expected anyone to come to her defense.|||Stand up for me ties the gratitude directly to the confrontation.
370|Rafael regrets hurting her when he first spoke.|||He reflects on his own comment without conflating it with the trader's abuse.
375|Charlotte says Rafael meant well and that she should have thanked him.|||The mutual recognition pays off both apologies.
379|Charlotte asks him to return to the village.|||The small question is warm without adding romance.
383|Rafael readily agrees.|||The simple promise begins naturally.
388|Charlotte needs to hear he means it.|||The single question preserves the tender uncertainty.
392|Rafael gives his word.|||The very short reply answers her directly.
397|Charlotte playfully insists and says she will wait.|||The voice becomes bright now that they trust one another.
401|Rafael says goodbye.|||The casual farewell fits their new rapport.
406|Charlotte calls after him to remember the promise.|||The echo is more natural in English than a repeat of the earlier imperative.
410|After Charlotte goes, Rafael realizes Clau heard them.|||The sudden recognition turns the private moment into a crew discussion.
414|Clau says the story made him tear up.|||The rough interjection preserves his earnest comic shift.
418|Arcadius says Charlotte suffered both in Europe and in the New World.|||The sympathetic line keeps the two locations distinct.
422|Rafael realizes Arcadius was there too.|||The surprised question follows directly from finding Clau.
427|Arcadius apologizes for listening and says curiosity got the better of him.|||The quiet explanation fits the apology without adding a motive.
439|Rafael recalls fearing loss of his place when Spain seemed about to annex Portugal.|||The conditional political context supports his reflection without asserting an outcome.
444|Rafael contrasts his fear with Charlotte's community never having had a place of their own.|||The land of their own links to her account rather than making the claim literal homelessness.
451|Clau asks Rafael to find something they can do for the village.|||Keep FI and the emphatic desire to help.
455|Arcadius suggests helping the village develop, even if it can only happen later.||help the village grow.;find a way to help someday.|The useful phrase groups keep the proposal and the hopeful future timing clear.
458|Rafael agrees to work on it.|||His affirmative answer carries the crew's decision.
462|Rafael pauses after the decision.|||The silence begins the shift back to his own thoughts.
467|Rafael says Charlotte's name thoughtfully.|||The short beat preserves contemplation without deciding what he feels.
472|Arcadius calls Charlotte sincere and a lovely person.|||The current compliment and second brief thought convey her openness.
476|Clau agrees.|||His short assent shows how far his attitude has shifted.
480|Rafael agrees softly.|||The quiet response fits before his private question.
485|Rafael wonders what the crew can do to help with its own efforts.|||The parenthetical thought returns to the practical offer instead of ending on romance.
""",
}


# Changes prompted by reading the first native proofs at full size.
REFINEMENTS = {
    (60, 143): ("", "", "Retain the reassurance. Keeping worrying over nothing intact and letting You'll do just fine stand alone uses three short but complete reading beats."),
    (60, 147): ("", "get back to Portugal!;finish off Kuhn", "Keep the urgency and the two connected actions. Avoid a break inside get back."),
    (60, 173): ("", "collect all seven?;It's yours now.", "Give the refusal, rhetorical question and final gift their own beats."),
    (60, 205): ("Then we won't have to watch our backs. Even I'd have a hell of a time taking him on alone.",
                "watch our backs.;a hell of a time;taking him on alone.",
                "Taking Kuhn out removes a threat at their backs. The later branch is where Pereira is asked to stay and handle it himself."),
    (60, 301): ("No. You're governor of Indochina. You're responsible for these waters, so I'm leaving it all to you.",
                "No. You're governor of Indochina.;responsible for these waters,;leaving it all to you.",
                "Rafael names the governor's actual office, connects it to jurisdiction and clearly entrusts the area to him."),
    (60, 306): ("", "", "Retain the earlier wrap at the natural boundary before the infinitive. This branch actually asks him to cover their rear."),
    (60, 309): ("Yes. If we know these waters are in good hands, we can give Valdes everything we've got.",
                "are in good hands,;everything we've got.", "His trust in Pereira lets him focus entirely on Valdes."),
    (60, 335): ("", "", "The first part of the existing question is left open for the conversational right? The separate free-competition question is already intact."),
    (60, 448): ("Looks like you're catching on.", "", "The idiom suits Pereira's plainspoken approval and keeps his qualified Looks like."),
    (60, 451): ("", "I'm holding back;there'll be no one;left to stop him.", "Keep the reason for restraint and the absence of anyone able to stop Kuhn."),
    (60, 459): ("", "if that's all we think about,;hand him the world.", "Maintain the full condition and its consequence."),
    (63, 22): ("", "had Eirene help;heavy lifting;didn't you?", "Keep Eirene and her role in the lifting together, as well as the pointed question tag."),
    (63, 126): ("", "", "Retain the earlier setup and complete reassurance on the second row. No emphasis or short tag is stranded."),
    (63, 162): ("", "never fought like this;didn't know what to do,;and I still don't.", "Keep the revelation and hesitation intact without dividing what to do."),
    (64, 55): ("Ow! What the hell are you doing?!", "", "The shout and profanity already make the trader's contempt clear. Dropping the stilted vocative avoids carrying that implication in unnatural English."),
    (64, 305): ("They said there was gold everywhere and miles of fertile land no one had touched.", "there was gold everywhere;fertile land;no one had touched.",
                "Charlotte remembers what the recruiters told them, with both gold and uncultivated land in the sales pitch."),
    (64, 358): ("Even so, we often have to sell for next to nothing. You saw what it's like. We don't have much choice.",
                "next to nothing.;You saw what it's like.;We don't have much choice.",
                "The comparison is to the trader's offer and his behavior. The earlier confrontation ended without a sale."),
    (64, 455): ("Let's see what we can do to help the village grow. Even if we can't help now, maybe we'll find a way someday.",
                "help the village grow.;if we can't help now,;find a way someday.",
                "Arcadius offers a practical next step and leaves open the possibility that they can only help later."),
}


FINAL_LINES = {
    (60, 147): ("", "Come on! We'd better finish off Kuhn;get back to Portugal!", REFINEMENTS[60, 147][2]),
    (60, 173): ("Yeah. I'm not interested. Who'd bother collecting all seven? It's yours now.",
                "Who'd bother collecting all seven?;It's yours now.", "The rhetorical question keeps his dismissal aimed at the effort of finding all seven, then he gives it away."),
    (60, 205): ("That'll get him off our backs. Even I'd have a hell of a time taking him on alone.",
                "That'll get him off our backs.;Even I'd have a hell of a time;taking him on alone.", REFINEMENTS[60, 205][2]),
    (60, 301): ("No. You're governor of Indochina. You're in charge of these waters. I'm leaving it all to you.",
                "No. You're governor of Indochina.;You're in charge of these waters.;I'm leaving it all to you.", REFINEMENTS[60, 301][2]),
    (60, 451): ("", "from an all-out fight with Kuhn.;If he beats me, there'll be no one;left to stop him.", REFINEMENTS[60, 451][2]),
    (60, 459): ("I want Portugal restored, too. But if that's all we think about, we could hand him the world.",
                "I want Portugal restored, too.;if that's all we think about,;we could hand him the world.",
                "The blunt opening fits Pereira and preserves his shared patriotism before the broader warning."),
    (63, 22): ("", "had Eirene help;with the heavy lifting;the other day, didn't you?", REFINEMENTS[63, 22][2]),
    (63, 30): ("That's not the point! Eirene isn't as healthy as the rest of us. You've got to look out for her!",
                "Eirene isn't as healthy;You've got to look out for her!", "Clau is speaking about Eirene's health in the context of strenuous work. Keep his force and the full rebuke."),
    (63, 108): ("", "I thought I was looking out for you;too, Eirene. It's not fair...", "Keep the intent and the frustration as complete reading groups."),
    (63, 162): ("", "Clau and I have never fought;like this before.;what to do, and I still don't.", REFINEMENTS[63, 162][2]),
    (64, 55): ("Ow! The hell are you doing, woman?!", "Ow! The hell are you doing, woman?!", "The clipped, rude question keeps the trader's aggressive direct address and immediate pain."),
    (64, 455): ("Let's see how we can help this village grow. If we can't do anything right now, maybe we'll find a way someday.",
                "Let's see how we can help;this village grow.;If we can't do anything right now,;maybe we'll find a way someday.", REFINEMENTS[64, 455][2]),
}


def review(edition):
    assert not REVIEW.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release["candidate_sha256"]
    assert base.digest(parent.MANIFEST) == release["manifest_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    images = [base.NdsImage.open(path) for path in (native.CLEAN, parent.ROM)]
    clean_arm, arm = [img.read_file(native.ARM) for img in images]
    archives = [img.read_file(ARCHIVE) for img in images]
    hashes = [native.digest(a) for a in archives]
    assert hashes[1] == release["target_SC0_sha256"]
    source_bank, current_bank = [native.IlnkContainer.parse(blob).blocks for blob in archives]
    actors = {r["actor_ID"]: r["progressive_nameplate"]
              for r in base.load(established.CATALOGUE)["source_and_current_default_name_fields"]}
    inventory, _, _ = native.scoped_inventory()
    rows, groups = [], []
    for number, text in DECISIONS.items():
        decisions = {}
        for line in text.strip().splitlines():
            index, gloss, english, phrases, note = line.split("|", 4)
            decisions[int(index)] = gloss, english, phrases.split(";") if phrases else [], note
        source, current = source_bank[number], current_bank[number]
        clean_commands, active_commands = [inventory(code, block)[0] for code, block in
                                           ((clean_arm, source), (arm, current))]
        assert [r["word"] for r in clean_commands] == [r["word"] for r in active_commands]
        source_controls = {r["offset"]: r for r in clean_commands if r["word"] == 0x4000}
        assert len(source_controls) == len(decisions), (number, len(source_controls), len(decisions))
        bound, _, _ = established.bind(arm, clean_arm, inventory, 0, number, source, current, decisions)
        groups.append(dict(route=0, file_path=ARCHIVE, block=number, record_ids=[f"DK4_MES_B{number}_R{i:04d}" for i in decisions],
            context=CONTEXTS[number], source_block_sha256=native.digest(source), current_block_sha256=native.digest(current)))
        for index, actor, (japanese, current_value), (sr, cr) in bound:
            prior = " ".join(current_value[1:].decode("ascii").split())
            gloss, replacement, phrases, note = decisions[index]
            if (number, index) in edition:
                replacement, protection, note = edition[number, index]
                phrases = protection.split(";") if protection else []
            english = replacement or prior
            assert english.isascii() and all(phrase in english and len(phrase) <= 36 for phrase in phrases), (
                number, index, prior, phrases)
            assert not replacement or replacement != prior
            change = "prose" if replacement else "wrap_only" if phrases else "retention"
            for ref, content, digest in zip((sr, cr), (source, current), hashes, strict=True):
                ref.update(file_path=ARCHIVE, block=number, block_sha256=native.digest(content), archive_sha256=digest)
            cr["candidate_sha256"] = release["candidate_sha256"]
            command = source_controls[sr["command_offset"]]
            sr["conditional_ancestors"] = command["ancestor_0100_offsets"]
            speaker = actors[actor]
            rows.append(dict(id=f"DK4_MES_B{number}_R{index:04d}", route=0, file_path=ARCHIVE, block=number,
                source_selector=actor, kind="progressive", speaker=speaker, source_meaning=gloss,
                Japanese=japanese[1:].decode("cp932"), previous_English=prior, english=english, protected_phrases=phrases,
                source_reference=sr, current_reference=cr, source_hex=japanese.hex(), current_hex=current_value.hex(),
                context=CONTEXTS[number], localization_note=note, change_class=change,
                decision="retention" if change == "retention" else "revision",
                review=dict(source=True, context=True, localization=True, naturalness=True, formatting=change == "retention")))
    counts = dict(Counter(row["change_class"] for row in rows))
    ROOT.mkdir(exist_ok=True)
    base.save(REVIEW, dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        translation_policy="natural-dialogue-v2", target_locale="en-US", groups=groups, records=rows, counts=counts,
        binding_reference_sha256=base.digest(established.TRIAGE), new_editorial_credit=0,
        stored_and_native_verification_of_changes_pending=True))
    print(f"Reviewed {len(rows)} records across three complete story objects. {counts}", flush=True)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("review", "preflight"))
    parser.add_argument("--edition", choices=("initial", "refined", "final", "release"), default="initial")
    args = parser.parse_args()
    if args.edition != "initial":
        ROOT = ROOT / args.edition
        REVIEW, PREFLIGHT = ROOT / REVIEW.name, ROOT / PREFLIGHT.name
    if args.action == "review":
        release_lines = FINAL_LINES | {
            (60, 147): ("Come on! We'd better beat Kuhn and get back to Portugal!", "We'd better beat Kuhn;get back to Portugal!",
                        "Keep Pereira's urgency. Beat matches the order to defeat Kuhn before they can head home."),
            (63, 14): ("", "Could you think about her;for a second?", "Let Clau's opening pause carry the tension. Keep his request and the reference to her together."),
        }
        editions = {"initial": {}, "refined": REFINEMENTS, "final": REFINEMENTS | FINAL_LINES,
                    "release": REFINEMENTS | release_lines}
        review(editions[args.edition])
    else:
        preflight = established.preflight
        FunctionType(preflight.__code__, preflight.__globals__ | globals())()
