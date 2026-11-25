"""Review Rafael's homeland crisis, Charlotte's message, and the map discoveries."""

from scripts import register_rafael_palace_and_alliance_20261121 as parent
from scripts import review_rafael_palace_and_alliance_20261121 as precedent
from scripts.source_locked_derivation_v5118 import checked_text
from types import FunctionType


base, native, ROOT = parent.base, parent.native, precedent.ROOT
SOURCE = ROOT / "paired_source_B150_B160_final_candidate.json"
OUTPUT = ROOT / "rafael_homeland_and_maps_review_v3.json"
PRIOR, NAMES, CATALOGUE = precedent.PRIOR, precedent.NAMES, precedent.CATALOGUE
TOKEN, logical, plan_progressive = precedent.TOKEN, precedent.logical, precedent.plan_progressive
BLOCKS = (tuple(range(150, 161)), (), (), ())
CONTEXTS = {
    150: "The innkeeper explains why people floated objects in the platter. Rafael tries the lotus leaf, and Hans explains the two keys needed for each region's map.",
    151: "News of Spain's king taking the Portuguese crown shocks the fleet. Rafael decides to build strength in Asia before returning, and alternate companions suggest the governor of Indochina.",
    152: "Pereira challenges Rafael's trading rights, explains what the new crown means for his office, and offers limited help against Kuhn. The crew infers what going east might accomplish.",
    153: "Rafael applies the liquid, which dissolves the surface of the coin and reveals the map to the Southeast Asian Proof of Conquest.",
    154: "A barkeep confides what Maldonado is doing. Rafael either commits to act or voices doubts about the scale of the problem and the fleet's readiness.",
    155: "The crew overhears a guarded exchange about Escante's plans. Claudio wants to act before Escante grows stronger. Rafael weighs the danger of making another enemy.",
    156: "Maldonado resents Escante and intends to cooperate temporarily to clear rivals from his path. Rafael's crew debates what that means for them.",
    157: "The ceremonial knife fits the sheath. A flash startles Rafael, then the crew spots the map on the blade.",
    158: "Rafael asks about crops for Charlotte's village. Claudio suggests corn and gently teases him about why he wants to help.",
    159: "Arcadius talks privately with Rafael about Charlotte's fear and delivers Charlotte's spoken message. Rafael uses Eirene's name privately after she has finished.",
    160: "Janus or Yifa uses the assembly plan to take the bamboo craft apart. The party recognizes the exposed map to the East Asian Proof.",
}

# Empty replacement keeps the installed wording. The third field protects short phrases.
DECISIONS = """
152 6|||Pereira opens with a hard question about the prior warning.
152 11|||Claudio asks the stranger who he is without yet recognizing him.
152 15|'Who are you?' Some greeting. And you think you can start trading here without asking? Gwah ha ha! You've got some nerve!|without asking?;You've got some nerve!|Pereira mocks Claudio's greeting and treats the new trading venture as an affront.
152 18|||Rafael puts himself between Claudio and the confrontation.
152 22|||Claudio's clipped reaction shows displeasure before the visitor addresses Rafael.
152 26|||Pereira checks whether Rafael is the admiral with more curiosity than respect.
152 30|I am. Now I'd like to know who you are.|who you are.|Rafael is polite but insists the other man identify himself first.
152 34|||The rough apology and repeated given name make the introduction recognizable.
152 38|||Claudio realizes Pereira is the governor Portugal officially recognizes.
152 42|||Rafael's recognition gives Pereira a chance to react to his reputation.
152 47|Huh. I guess word gets around. Any idea what I'm about to tell you?|word gets around.;about to tell you?|Pereira is amused by being recognized and tests whether Rafael understands the visit.
152 50|This is about the Estado, your trading territory here in Southeast Asia...|trading territory;Southeast Asia|Rafael gives the in-game term and clarifies it from the Japanese gloss.
152 54|That's right. You're a quick one, Admiral. Then you know why I'm telling you to get out.|a quick one, Admiral.;to get out.|Pereira calls him quick before ordering him out in his usual blunt register.
152 57|We're both Portuguese companies. Couldn't we compete on fair terms?|fair terms?|Rafael appeals to common nationality as grounds for fair competition.
152 62|Fair? Where'd you get the idea the world was fair?!|the world was fair?!|Pereira scoffs at the precise principle he repeats in his next line.
152 65|The world's unfair. That's how it works!|That's how it works!|Pereira answers his own challenge and sees unfairness as the rule.
152 68|...||Rafael gives the rebuke a silent beat in the surrounding dialogue's font.
152 73|Either I drive you out or you drive me out! Gwah ha ha!|you drive me out!|Pereira states the two outcomes from his own perspective and laughs.
152 77|And that Portugal of yours has been taken over by Spain, hasn't it?|hasn't it?|Pereira uses the takeover to undermine Rafael's appeal. Keep the challenging tag together.
152 81|...||Rafael holds back after Pereira invokes the takeover. Use the surrounding ellipsis glyphs.
152 86|Either way, I want you to leave Southeast Asia to us. The Pereira Company will handle it.|Pereira Company|Pereira disguises a claim to the whole region as an offer to manage it.
152 90|You want a monopoly?|a monopoly?|Rafael questions the proposed exclusive control plainly.
152 95|||Pereira laughs and confirms Rafael's interpretation of the demand.
152 98|We've lost our country! What good does it do to fight each other now?|fight each other now?|Rafael appeals emotionally to their common loss.
152 103|I have mixed feelings, too. I was proud of Portugal. I never thought our armed forces would side with Spain.|would side with Spain.|Pereira admits his pride and surprise. The Japanese refers to the armed forces as a whole.
152 106|Exactly! We could join forces, beat Spain's army, and restore Portugal...|restore Portugal...|Rafael takes Pereira's sympathy as an opening and begins suggesting action.
152 111|Slow down. Why get so worked up? Portugal hasn't actually become Spain, has it?|has it?|Pereira distinguishes shared rule from a formal erasure of Portugal.
152 114|||Rafael's short objection is cut off by Pereira's acknowledgment.
152 119|You're young. You can't just accept it, can you? I know what you're saying.|can you?|Pereira recognizes Rafael's feeling without backing his proposal.
152 123|...||Rafael pauses when Pereira appears to understand him. Use the surrounding ellipsis glyphs.
152 128|Try seeing it from my side. I'm Portugal's governor of Indochina. Now the King of Spain's word is law for me.|governor of Indochina;word is law for me.|The obligation comes from Pereira's existing public office under Portugal and the new common king.
152 131|||Rafael voices the political consequence of Pereira backing their resistance.
152 136|People's livelihoods depend on my decisions. I've got to look after them. That's the hard part of being governor.|look after them.;being governor.|Pereira points to concrete responsibilities of his office rather than a personal excuse.
152 140|Now, if you're taking on that Dutchman Antony Kuhn over in Indonesia, I might be able to help...|Antony Kuhn;might be able to help...|Pereira names the Dutch opponent and region and offers limited, conditional cooperation.
152 144|That's politics. Kuhn is an enemy of Spain, too. We can take him down together, but that's as far as I can go.|an enemy of Spain;that's as far as I can go.|Kuhn is an enemy they can act against in common. Pereira rules out help beyond that.
152 147|So you can't help us fight Spain. Is that it?|fight Spain.|Rafael asks for a direct confirmation of Pereira's limit.
152 152|||Pereira gives the clear confirmation he has withheld until now.
152 156|...||Rafael lets the refusal settle before Pereira volunteers advice. Use the surrounding ellipsis glyphs.
152 161|Sorry for going on like that. All I can tell you now is to head east and come back stronger.|come back stronger.|Pereira moves from his own complaints to the blunt advice he can offer.
152 164|||Rafael repeats the direction because it is the one part of the advice he can act on.
152 169|||Pereira conditions another conversation on that instruction and dismisses the visitors.
152 176|I hate to admit it, but the man made sense...|made sense...|Claudio reluctantly concedes the argument rather than calling Pereira elderly.
152 180|||Rafael considers the direction aloud after the meeting.
152 185|||Claudio turns Pereira's vague advice into a question about where they are.
152 189|...||The pause gives Rafael or Arcadius time to put the pieces together. Use the surrounding ellipsis glyphs.
152 200|I think he wants us to find the Proof of Conquest in East Asia.|Proof of Conquest;in East Asia.|Rafael proposes a likely interpretation, with the exact regional objective.
152 207|He probably means for us to find the Proof of Conquest in East Asia.|Proof of Conquest;in East Asia.|Arcadius voices the alternate inference in a more deliberate register.
152 214|||Claudio agrees with the guess and emphasizes how long satisfying it could take.
152 217|We need at least a lead on the Proof. Otherwise, I don't think Pereira will take us seriously.|a lead on the Proof.;take us seriously.|Rafael sets a minimum goal without treating the whole search as easy.
152 221|Tch. I don't know what he's up to, but we need him on our side right now. Fine. Let's go!|on our side right now.|Claudio is skeptical of Pereira's motives but sees the need for his support under present conditions.
152 225|||Rafael relies on Clau and gives the East Asia departure order.
153 5|||Rafael notes the grime and names the exact Ancient Kingdom Coin.
153 9|Why don't we polish it a little? There's a Lotion Jar right there.|a Lotion Jar|Claudio suggests polishing and points Rafael to the exact second item.
153 12|What's in it? Oh, never mind. Let's try a little...|Let's try a little...|Rafael wonders about the unknown liquid, then applies it anyway.
153 17|||The rhythmic rubbing sound gives the physical action a short beat.
153 22|H-hey, FI! Quit rubbing and look at it! It's dissolving!|It's dissolving!|Claudio interrupts Rafael before too much of the coin dissolves.
153 26|||Rafael's alarm gives way to surprise when he notices something else.
153 30|Wait, there's a different pattern coming through. Looks like a map...|Looks like a map...|Rafael sees the new pattern appearing and has yet to identify it.
153 40|That's the map to Southeast Asia's Proof of Conquest! The surface had to dissolve first.|Southeast Asia's;Proof of Conquest!|Claudio recognizes the map and explains why the dissolving surface mattered.
153 46|Then this is the map to the Proof of Conquest in Southeast Asia! It's made to appear when the surface dissolves.|Proof of Conquest;Southeast Asia!|Arcadius reaches the same conclusion and describes how the map is revealed.
153 53|||Claudio celebrates having the location of the Southeast Asian Proof.
153 57|||Rafael's relief recalls the chance of destroying the entire coin.
154 5|||Claudio assesses Spain's head start in these waters and addresses Rafael by name.
154 8|||Rafael agrees that Spain is ahead and sees a chance to catch up.
154 13|||Claudio identifies getting the Proof first as the way to reverse their position.
154 24|More than anything, we have to restore Portugal. We can't give up these waters to Spain!|restore Portugal.;give up these waters|Rafael frames the rivalry in the waters in terms of restoring his country.
154 28|Well, I get why you want to restore Portugal. We'd better get on with it, then.|get on with it, then.|Claudio acknowledges Rafael's goal and resolves to act alongside him.
154 35|||The barkeep establishes why he approaches Rafael and keeps the company substitution as a genuine question.
154 39|||Rafael confirms his affiliation but is waiting to hear why the barkeep asked.
154 44|Keep your voice down. This is Maldonado's territory. Do you know his reputation?|Maldonado's territory.|The barkeep lowers his voice before bringing up the local ruler's reputation.
154 60|His reputation? Have you heard anything bad about him?|anything bad about him?|Rafael asks whether the man's reputation is a bad one.
154 67|Well, I don't really know who he is to begin with...|who he is|Rafael admits he doesn't know Maldonado before asking about him.
154 76|His reputation? Have you heard anything bad about him?|anything bad about him?|The second route leads to the same natural question and rejoins the exchange.
154 84|I'll tell you because you're with FO, but keep it quiet. Everyone around here hates Maldonado.|hates Maldonado.|The barkeep admits the local hatred because he believes Rafael represents the named company.
154 88|That's strong talk. What kind of man are we dealing with?|are we dealing with?|Claudio takes the hostility seriously and asks what kind of man inspires it.
154 91|||Rafael asks respectfully for the reason behind the hatred.
154 95|They rule the whole area by force. With Spain's crown behind them, they do what they like.|Spain's crown|The barkeep distinguishes the group's actions from the protection Spain provides.
154 99|||The attacks are indiscriminate and motivated by the group's profit.
154 102|||Rafael compares their conduct to piracy. The barkeep confirms the comparison in response.
154 107|That's exactly what they are. Sailors can't put to sea safely. It's ruining my business too.|put to sea safely.|The barkeep agrees and names both risks to sailors and harm to his own trade.
154 111|Are you sure you want to trust us that fast? We could be just as bad, you know.|you know.|Claudio doubts his confidence and offers a counterexample without claiming they're pirates.
154 114|||The barkeep bases the inference on the named company's reputation and includes the questioning tag.
154 117|...||Rafael has a quiet beat before making the choice. Use the surrounding ellipsis glyphs.
154 129|||The promise directly commits Rafael to confronting Maldonado.
154 131|||The second choice leaves him unsure and opens the explanation for waiting.
154 140|FI...||Claudio notices Rafael's hesitation. Keep the name substitution and use consistent punctuation.
154 144|I get the feeling this is happening all over the New World. It may be more than Maldonado and his men...|all over the New World.|Rafael thinks other factions may be part of the same larger problem.
154 148|Beating him might not solve it. And even if we decide to fight him, we'd need time to prepare.|time to prepare.|Rafael distinguishes the likely effect of a victory from the practical need to get ready.
154 152|Sir, after thinking it over, I don't think we can help right away...|help right away...|Rafael is respectful and declines immediate action without ruling out future help.
154 157|||The barkeep's subdued reply shows disappointment before Claudio speaks.
154 161|||Claudio thanks him indirectly and asks Rafael to agree, keeping the name token.
154 164|Yes. I see how much people here are suffering. I hope we can do something for them soon...|for them soon...|Rafael acknowledges the hardship and hopes for a future response.
154 169|I hope you aren't like those men...|like those men...|The barkeep ends the hesitant branch by hoping Rafael's company is different.
154 185|||Rafael credits the man's trust and explains why he feels obliged to act.
154 190|||The pledge names Maldonado and the New World and addresses all of Rafael's companions.
154 195|||Claudio responds with quick enthusiasm in the affirmative branch.
154 199|You'll do it? Good. I'll be waiting. Maybe we won't have to live like this much longer...|live like this|The barkeep hopes that the suffering he's described will end soon once they act.
155 5|||The sailor reports the named outfit coming into the area and keeps the slightly dismissive register.
155 9|So I hear. They say they're a tough lot to deal with.|tough lot|Blanco repeats a rumor rather than claiming he has already fought the company.
155 12|||The sailor wonders whether the news threatens the governor's undisclosed plan.
155 15|||Blanco shushes him and notes how few of the governor's men have been told.
155 19|Heh. Sorry. I just meant they might get in Governor Escante's way.|Governor Escante's|The sailor apologizes and changes from the secret itself to a possible obstacle.
155 22|||Blanco leaves that judgment to Escante rather than to the speaker.
155 26|Or we could get them on our side against Maldonado...|against Maldonado...|Blanco suggests an alliance as the reverse of treating the newcomers as an obstacle.
155 29|Either way, Governor Escante will rule the New World. And then the homeland... Oops.|rule the New World.|The sailor stops before giving away what comes next involving Spain.
155 32|If you value your life, that's enough talk.|enough talk.|Blanco's threat cuts off further details of a guarded plan.
155 35|All right, all right. Nobody's going to give up these waters without a fight, anyway.|without a fight, anyway.|The sailor backs down from the threat and shifts to a safer general observation.
155 39|Hmph. Time will tell how far FO gets.|how far FO gets.|Blanco remains doubtful about the named company. The substitution stays with its verb even at maximum name width.
155 43|||The sailor agrees with a nervous laugh and drops the subject.
155 47|FI, you heard that too, didn't you?|didn't you?|Janus checks what Rafael heard and keeps the tag in one phrase.
155 50|||Rafael identifies the subject as the governor of Mexico through a natural confirming question.
155 54|||Claudio's remark makes the suspicious situation sound like his own idiom.
155 64|||Rafael echoes the important word without claiming he knows the plan.
155 71|Who isn't trying to expand these days?|trying to expand|Julio treats expansion as ordinary and answers the crew's concern in his familiar register.
155 74|True, but what did they mean by 'the plan'?|'the plan'?|Janus agrees about ordinary expansion and points to the suspicious phrase.
155 85|It's suspicious, sure, but we shouldn't rush to make more enemies. They haven't declared war.|declared war.|Rafael weighs the overheard remark against the absence of a declaration.
155 90|Don't be naive. You heard the way they talk. We ought to do something while we can.|while we can.|Claudio wants action sooner rather than assuming a formal declaration is needed.
155 94|Once Escante has the whole New World, it'll be too late to do anything about it!|New World,;too late|Claudio warns against waiting until Escante has already taken everything. Keep the region's name on one line.
155 98|I know. We can't have Spain getting any stronger, but...|getting any stronger,|Rafael sees the risk of Spain gaining power but still hesitates to act.
155 102|Then what are we waiting for?||Claudio treats Rafael's concession as deciding the matter.
155 106|||Rafael agrees to think about it and stops short of committing the company.
155 112|We're in their way too. I suppose that's bound to happen if they want the whole New World.|the whole New World.|Rafael realizes they are the other party's obstacle and understands why.
155 117|Well then, Escante's in our way too!|in our way too!|Claudio draws the reciprocal conclusion more bluntly.
155 120|||Janus addresses Clau by nickname and checks his harsher reasoning.
155 132|Maybe it's fate. When the time comes to fight, we have to fight.|time comes to fight,|Julio treats fighting as a duty when its time comes.
155 135|Sometimes you need the strength to defeat an enemy, don't you...|don't you...|Rafael reluctantly accepts that there are moments when he needs that power.
155 150|Escante, Maldonado, they're all the same. Best to hit them early.|Best to hit them early.|Claudio lumps the two men together and wants to strike early.
155 154|I don't see another way...||Janus shares the reluctant conclusion rather than delivering an order.
156 5|So what's the story with Escante and Maldonado? Do they get along?|Escante and Maldonado?|Claudio asks about their relationship because he wonders if they might act together.
156 9|||Rafael assumes two governors in the same part of the world get along and phrases it tentatively.
156 13|||Claudio raises the joint attack as a possibility in the form of a direct question.
156 17|||Rafael doesn't want to decide before the danger materializes.
156 22|FI, you know we're in their way! Keep this up and they'll get us first!|they'll get us first!|Claudio warns Rafael that doing nothing leaves them vulnerable.
156 25|||Janus abruptly shushes both men and directs their attention to what he sees.
156 29|||Maldonado curses Escante and trails off as he guesses what the other man wants.
156 32|I'm sure of it. We can't trust Escante!|trust Escante!|The sailor agrees with the suspicion and urges distrust.
156 35|||Maldonado intervenes to say that a fight with Escante now would be ill advised.
156 39|We'll work with him for now and take down the other factions. First thing is to expand my own territory.|for now;my own territory.|Maldonado offers only a temporary partnership and states his personal priority.
156 42|True. If we fought Escante now, we wouldn't stand much of a...|much of a...|The sailor starts to state how little chance they have. Maldonado interrupts before he can say it outright.
156 45|Don't say it! Damn it, that bastard Escante makes my blood boil!|makes my blood boil!|Maldonado cuts off the assessment and blames Escante for his anger.
156 49|||Janus checks the identity of the man they overheard.
156 53|So much for Escante and Maldonado getting along.|getting along.|Rafael revises his earlier assumption about the two men.
156 57|Fighting over trade rights, maybe?|trade rights, maybe?|Janus suggests overlapping interests without claiming to know the details.
156 61|They both want the New World all to themselves.|all to themselves.|Claudio identifies the shared ambition that makes them rivals.
156 64|But he did say they'd work together for now to take down the other factions...|work together for now|Janus repeats the substance of the temporary partnership they just heard.
156 68|They'll come after us first.||Claudio is certain Rafael's company will be the first target.
156 71|||Rafael's hesitant question leaves open whether he shares that certainty.
156 76|They have nothing to gain from teaming up with a Portuguese company like ours...|nothing to gain|Janus gives the pragmatic reason he doubts an alliance with either of them.
156 79|||Rafael resolves to fight if they attack without declaring an attack of his own.
157 5|What do you think this Ceremonial Knife was used for?|Ceremonial Knife|Rafael wonders about the original purpose of the named object.
157 9|Hey, careful! A blade's a blade, however small. Put it away before you hurt yourself.|A blade's a blade,|Claudio warns Rafael despite the knife's size and follows with a practical instruction.
157 13|All right. The Sun-Crest Sheath looks about the right size. I'll put it in there...|Sun-Crest Sheath|Rafael uses the matching item's size as his reason for trying it.
157 18|||Claudio's startled stammer makes the flash sudden.
157 22|I-it's blinding!||Rafael reacts immediately to the glare with the Japanese hesitation.
157 29|Whew, I can see again. What was that light...?|What was that light...?|Rafael notices the glare has passed and wonders what it was.
157 33|||Claudio spots the dropped knife promptly.
157 37|Oh! The flash made me drop it.|made me drop it.|Rafael realizes he dropped the knife because he was startled.
157 41|||Rafael spots the map on the blade before the others recognize it.
157 46|That's a map! It must show where to find the Proof of Conquest in the New World!|Proof of Conquest;in the New World!|Claudio identifies the clue and the region with the full item term.
157 49|I think so too. Now we can find the Proof! That was strange, though...|That was strange, though...|Rafael shares the discovery but still wonders about the light.
158 5|||Rafael opens with a natural question about local crops and calls Claudio by his nickname.
158 9|||Claudio wonders what prompted the question.
158 13|Well... I thought Charlotte's village could use something new to trade.|something new to trade.|Rafael wants to help the village find a new trade good and is a little shy about why.
158 18|Hmm. What about corn?||Claudio considers the crops and suggests the installed American English item name.
158 21|Corn... Yeah, let's do that!||Rafael decides as soon as he's considered Claudio's suggestion.
158 25|Well, look at you, FI. I didn't know you had it in you!|had it in you!|Claudio teasingly implies he sees Rafael's interest without telling him what he sees.
158 29|||Rafael's stammered confusion follows Claudio's teasing.
158 34|Heh. Never mind. Just make sure you bring her the corn.|bring her the corn.|Claudio lets the implication stand and gives Rafael the practical reminder.
159 5|||Arcadius opens the private conversation with Rafael's name and asks for a moment.
159 8|||Rafael recognizes that Arcadius wants something and asks what it is.
159 13|You've seemed down lately.||Arcadius describes a change she has noticed over time.
159 17|I have? No, I'm... I'm fine.|I'm... I'm fine.|Rafael tries to deny it, with the hesitation of the Japanese.
159 21|||Arcadius names Charlotte with the right degree of certainty before Rafael admits anything.
159 25|?!||Rafael's wordless surprise is still sudden. Use the punctuation glyphs of the surrounding dialogue.
159 30|You've been thinking about her, haven't you?|haven't you?|Arcadius asks gently whether Charlotte is on his mind.
159 34|Well... I can't hide anything from you, can I?|can I?|Rafael sighs and concedes that she sees through him. Keep the familiar tag whole.
159 38|FI...||Arcadius addresses Rafael gently before he begins speaking. Use consistent punctuation.
159 42|All I do is think about her. I want so badly to do something for her, but... I just...|do something for her|Rafael admits he's preoccupied and can't finish the objection.
159 47|FI... She said, 'I think about FI every day.'|every day.|Arcadius speaks Charlotte's confession aloud. The direct quotation keeps both name substitutions without addressing Rafael in the third person.
159 51|||Rafael is genuinely taken by surprise by Charlotte's feelings.
159 56|I'm sorry. You came back looking so miserable that day, so I went to see Charlotte.|went to see Charlotte.|Arcadius apologizes for intervening and explains what prompted the visit.
159 60|If you didn't feel anything for Charlotte, FI, I was going to keep this to myself.|keep this to myself.|Arcadius explains that she was willing to protect Charlotte's confidence if Rafael didn't share her feelings.
159 63|...||Rafael listens in silence as Arcadius turns to Charlotte's fears. Use consistent punctuation.
159 68|Please forgive her for leaving so suddenly that day. She's afraid she isn't good enough for you.|good enough for you.|Arcadius asks Rafael to forgive the departure and connects it to Charlotte's fear.
159 71|||Rafael asks why Charlotte would think she wasn't good enough for him.
159 76|You come from a distinguished family, FI. That's what worries her.|That's what worries her.|Arcadius names the difference in family standing that concerns Charlotte.
159 80|I don't care about any of that!||Rafael is emphatic that his family standing has no bearing on his feelings.
159 84|Maybe so. But try to see how Charlotte feels about it.|how Charlotte feels|Arcadius accepts his reaction but asks him to consider her perspective.
159 88|||Rafael is still puzzled and asks her to explain.
159 93|Remember what she told you? Think how much it must have hurt to be treated that way in Europe.|that way in Europe.|Arcadius refers to Charlotte's own account without inventing any mistreatment beyond it.
159 96|||Rafael remembers that part of Charlotte's story and admits the point quietly.
159 101|I don't think she's used to being happy. She's afraid of losing it, and that makes it hard to take the first step.|the first step.|Arcadius explains why the risk of losing happiness can stop Charlotte from accepting it.
159 104|...||Rafael takes in the explanation before Arcadius delivers the message. Use consistent punctuation.
159 109|Anyway, the rest is from Charlotte. She asked me to give you a message.|give you a message.|Arcadius clearly changes from her own explanation to relaying Charlotte's words.
159 113|||Rafael echoes the unexpected idea of a message.
159 118|She never learned to write. She told me she never had the chance...|never learned to write.;had the chance...|Arcadius explains why Charlotte needed someone else to speak for her without blaming her. Let the first thought read as a complete sentence.
159 122|I never even thought that she might not be able to write. I didn't understand at all...|I didn't understand at all...|Rafael is startled that the possibility never occurred to him and acknowledges his misunderstanding.
159 126|'Thank you for everything, FI. My village is all right now.|all right now.|Charlotte begins with thanks and reports how the village is doing. The quotation continues on the next two panels.
159 129|I hope your country is restored too, FI. When it is...|When it is...|Charlotte shares his hope for his country and begins the condition she completes in the next panel.
159 132|If you still feel the same way you did then, please come see me.' That's all she said.|please come see me.|Charlotte's condition and invitation complete the quote before Arcadius indicates it has ended.
159 136|||Rafael says Charlotte's name rather than analyzing how he feels.
159 141|Well... I'll leave you to it.|I'll leave you to it.|Arcadius tells Rafael that she's leaving after the message, giving him room to think.
159 144|...||The moment of silence comes before Rafael uses her private name. Use consistent punctuation.
159 149|||Rafael thanks her as Eirene in private, after she entrusted him with her real name.
159 154|You're welcome. Good luck, FI. What happens with Charlotte is up to you now.|up to you now.|Eirene encourages Rafael while leaving the next action and decision with him.
160 10|Look at this. The Tang Bamboo Craft fits together exactly as the Bamboo Assembly Plan shows.|Tang Bamboo Craft;Bamboo Assembly Plan|Janus recognizes the exact relation between the two named objects.
160 13|So we can use the plan to take it apart and put it back together?|put it back together?|Rafael asks whether the plan works in both directions.
160 17|||Janus suggests trying it and begins to work through the order.
160 20|||Rafael's stammer interrupts when he notices the markings inside the large piece.
160 25|||Yifa talks through the order to herself as she works.
160 28|||Rafael notices Yifa is enjoying the work and addresses her by name.
160 33|||Yifa brags that the exact craft comes apart before Rafael misreads what happened.
160 37|||Rafael's abrupt question shows he thinks the object may have been damaged.
160 41|||Yifa denies breaking it and points him to the exact plan.
160 44|Oh, I see. The Bamboo Assembly Plan shows how to take it apart and put it back together.|Bamboo Assembly Plan;put it back together.|Rafael realizes the diagram explains both taking it apart and reassembling it.
160 48|||Yifa enjoys the process and tells Rafael when she's taken the entire object apart.
160 51|I didn't know you were so good with your hands. Wait, there's something drawn on the back of that piece.|on the back|Rafael admires Yifa's dexterity and is interrupted by what he sees on the bamboo.
160 65|What is that? It looks like a map. Could it lead to the Proof of Conquest in East Asia?|Proof of Conquest;in East Asia?|Janus wonders aloud and then proposes the exact clue.
160 69|||Rafael agrees with the inference and urges them to look right away.
160 75|Whoa! It's a map to the Proof of Conquest!|Proof of Conquest!|Yifa spots the map and recognizes what it points to immediately.
160 79|Nice work, Yifa! Let's find the Proof of Conquest in East Asia!|Proof of Conquest;in East Asia!|Rafael credits Yifa and proposes the next step.
"""


def all_decisions(packet):
    rows = {g["block"]: {r["source_record_index"]: r for r in g["records"]} for g in packet["groups"]}
    lines = []
    phrases = {(150, 51): "Proof of Conquest;in the Indian Ocean!", (151, 208): "are you?!",
               (151, 334): "FI, my boy...;I mean, Admiral."}
    for block in (150, 151):
        draft = base.load(ROOT / f"B{block}_contextual_decisions_final_candidate.json")
        assert draft["paired_source_sha256"] == base.digest(SOURCE)
        assert draft["candidate_sha256"] == packet["candidate_sha256"]
        for decision in draft["records"]:
            number = decision["source_record_index"]
            row = rows[block][number]
            old = precedent.logical(row["current_English"])
            assert decision["block"] == block and decision["Japanese"] == row["Japanese"]
            assert decision["previous_English"] == old
            english, note = decision["english"], decision["localization_note"]
            if (block, number) == (151, 302):
                english = "Might he join forces with us, seeing as we're countrymen?"
                note = "Janus suggests the governor as a first ally on the strength of their shared nationality."
            lines.append("|".join((f"{block} {number}", english, phrases.get((block, number), ""), note)))
    return "\n".join(lines) + "\n" + DECISIONS.strip()


source = checked_text(precedent.source, {"len(rows) == 270": "len(rows) == 287"})


if __name__ == "__main__":
    scope = precedent.precedent.scope | vars(precedent) | globals()
    scope["reviewed_inputs"] = FunctionType(precedent.reviewed_inputs.__code__, scope)
    exec(compile(source, __file__ + "::review", "exec"), scope)
    scope["main"]()
