"""Review Rafael's palace audience, combat lesson and subsequent alliances."""

from pathlib import Path

from scripts import register_rafael_rescue_and_lessons_20261121 as parent
from scripts import review_rafael_rescue_and_lessons_20261121 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
CATALOGUE, GATES = precedent.template.CATALOGUE, precedent.template.GATES
TOKEN, logical, plan_progressive = precedent.TOKEN, precedent.logical, precedent.plan_progressive
ROOT = precedent.ROOT.with_name("rafael_B141_B160_followup_20261121")
SOURCE, OUTPUT = ROOT / "paired_source_registered_parent.json", ROOT / "rafael_palace_and_alliance_review_v2.json"
PRIOR = Path("translations/rafael_B141_B160_final_review_v1.json")
NAMES = Path("translations/rafael_B141_B160_scoped_names_final_v1.json")
BLOCKS = (tuple(range(141, 150)), (), (), ())
CONTEXTS = {
    141: "The crew finds a ship Hayreddin left them and considers what his gesture asks in return.",
    142: "Claudio suggests applying the Red Dye to the Old Parchment. A map appears and they recognize the North Sea clue.",
    143: "Albuquerque asks Rafael and Silveira to take Espinosa's trading territory and detain him. Outside the audience, Silveira offers an optional lesson about war, contracts and market share. Both replies join the shared farewell.",
    144: "The crew admits the two tablet pieces are unreadable separately. Fitting them together reveals a new mark that points to the Proof in Africa.",
    145: "Claudio drags Rafael along to invite Arcadius to eat. They learn Eirene's identity. She and Hans explain why she chose the disguise and the two visitors agree to keep her secret.",
    146: "Uddin gives his name and business location and discreetly asks Rafael for time. Rafael can agree to meet at the Guild in Basra or excuse himself to consult the crew.",
    147: "At the meeting, Uddin addresses Rafael with greater formality and proposes an alliance. He gives Rafael a night to consider it. The alternate rationale remembers the events in Africa.",
    148: "Uddin waits for Rafael's decision. On acceptance, they discuss Nagalpur, Arabian markets, a later nonaggression pact, and two shares. On refusal, Uddin suggests they pursue supremacy as rivals.",
    149: "The crew tries to combine the Evergreen Lotus Leaf with the Kushan Platter. Nothing happens yet.",
}

# An empty replacement preserves the installed paragraph. The third field protects phrases.
DECISIONS = """
143 5|From FO, Admiral FA? Admiral Albuquerque is expecting you. Please go in.|Admiral FA?;Admiral Albuquerque|The guard confirms the company and surname, names Albuquerque, and shows his visitor in.
143 8|||Rafael answers the guard with a short formal thanks.
143 21|||Arcadius takes in the imposing setting with a deliberately restrained remark.
143 28|We haven't done anything wrong, but places like this make me nervous.|make me nervous.|Claudio admits that palaces make him uneasy even with a clear conscience.
143 40|Stand up straight and you'll be fine.|you'll be fine.|Julio reassures Claudio with practical advice in his familiar older register.
143 55|Hmm. So this is the royal palace...|the royal palace|Cristina takes a guarded look at the palace before the audience.
143 63|Ah, there you are! Let's see... Mr. FA, was it?|Mr. FA, was it?|Albuquerque's easy greeting gives way to uncertainty about the surname.
143 67|||Rafael supplies his exact full-name substitution and uses respectful address.
143 71|Listen to you, FI! You sounded so dignified!|Listen to you, FI!|Claudio admires how well Rafael has risen to the formality of the occasion.
143 82|Ahem. This isn't our conversation. Let's stay quiet.|Let's stay quiet.|Arcadius signals that the other companions should stay out of the audience.
143 89|No need to call me sir. I sent for you, after all. Thank you for coming.|Thank you for coming.|Albuquerque rejects the honorific Rafael actually used and takes responsibility for summoning him.
143 93|||Rafael politely brings the conversation to the reason for the summons.
143 98|||Albuquerque asks about Portugal's commercial code before explaining the policy.
143 102|||Rafael admits limited knowledge instead of pretending to know the law.
143 106|Well, I appreciate your honesty. I'll spare you the legal details and give you the gist.|give you the gist.|Albuquerque softens the formality after Rafael's candid reply and promises the simple version.
143 110|||Rafael invites him to continue in the same courteous register.
143 115|These days, private trading companies do business abroad and help our nation prosper. Some of them resort to inhumane practices.|inhumane practices.|Albuquerque acknowledges the firms' contribution before distinguishing the abuses.
143 118|||Rafael asks what inhumane practices Albuquerque means.
143 123|Enslaved people and drugs. Our military found Espinosa's company trading in both in southeastern Africa.|southeastern Africa.|The accusation identifies both trades, how the military uncovered them and the exact region. The finding stays with the accusation on one page.
143 126|Portugal's honor will suffer if this goes on. That's where you come in.|That's where you come in.|The damage to Portugal's standing leads straight to the task he is assigning.
143 129|You're among our most promising navigators. Take all their trading territory and take Espinosa into custody.|trading territory;into custody.|Albuquerque wants the whole trading sphere taken and Espinosa detained. The assignment fits on one page.
143 133|Do you really think we can do that?|we can do that?|Rafael doubts the scale of the task, giving Albuquerque reason to reveal his help.
143 137|Ha ha! You won't have to do it without help. I'm not that unreasonable. Send in Mr. Silveira!|Send in Mr. Silveira!|Albuquerque's laugh, reassurance and summons shift the attention to Silveira.
143 140|Yes, sir! Mr. Silveira, you may come in.|Mr. Silveira,|The guard answers Albuquerque first, then extends the invitation to Silveira.
143 144|||Silveira announces himself by his full registered name and sounds formally on duty.
143 149|||Albuquerque gives a short acknowledgment before Silveira begins his greeting.
143 153|Your Excellency, I trust you're in the best of health...|in the best of health...|Silveira uses the source's elaborate greeting. Albuquerque cuts him off in the next line.
143 157|Never mind the formalities. This is FI FA, a young man with a great deal of promise.|FI FA,|Albuquerque cuts short the greeting, names Rafael through both substitutions and vouches for him.
143 160|P-pleased to meet you. I'm FI FA.|FI FA.|Rafael stumbles through the formal introduction but gives the substituted name in full.
143 165|Mr. FA, this is Fernan Silveira. You'll be working together.|Fernan Silveira.|Albuquerque supplies Silveira's name and assigns a partnership rather than a command hierarchy.
143 168|How exactly would that work?|would that work?|Rafael asks what the proposed partnership entails.
143 173|Well, I do business around southwestern Africa and, ah, I've made no small contribution to our country.|southwestern Africa|Silveira's affected hesitation sets up his boast. His region is southwest, distinct from Espinosa's.
143 177|Ahem. You certainly do a great deal of business.|a great deal of business.|Albuquerque confirms the scope of the business without endorsing Silveira's claim of public service.
143 181|Oh, you're too kind...||Silveira takes the dry qualification as praise and begins another flourish.
143 185|||Albuquerque interrupts the repeated flattery with a brusque order.
143 189|Crooks or not, our army can't openly attack fellow Portuguese on circumstantial evidence alone. We need you.|circumstantial evidence|The limitation applies to open military action against fellow Portuguese. Albuquerque's reason for asking for help stays with the legal restriction.
143 192|Heh heh. With the two of us together, I'll drive Espinosa out of my Africa!|my Africa!|Silveira takes personal possession of Africa even while talking about the alliance, prompting the aside.
143 196|(His Africa?) Hmph. Well, that's settled, then.|that's settled, then.|Albuquerque privately echoes Silveira's possessive boast before moving on.
143 200|||Albuquerque asks for objections before treating the agreement as final.
143 204|||Rafael's hesitant negative correctly answers the localized question.
143 209|I make my base in Sao Jorge. Stop by whenever you like. Ha ha ha!|Sao Jorge.|Silveira names his base and gives Rafael an invitation with his booming laugh.
143 233|Silveira gave you part of his market share in Sao Jorge.|market share in Sao Jorge.|The system notice names the giver, the partial transfer and its location without repeating share.
143 244|Now then, the king has provided funds for the campaign. Bring them in.|funds for the campaign.|The king supplied the war funds and Albuquerque orders them brought in.
143 247|||The guard answers the order crisply.
143 251|||Albuquerque calls Silveira forward to receive his share.
143 255|||Silveira's formal thanks fits the ceremony.
143 258|||The system identifies Silveira as recipient without inventing a sum for him.
143 263|||Albuquerque addresses Rafael by the original surname substitution to call him forward.
143 267|Yes, sir. Thank you...|Thank you...|Rafael is still hesitant while receiving the reward.
143 274|||The notice preserves 50,000 gold, the king as donor, and the campaign against Espinosa.
143 278|||The admiral distinguishes intelligence about Espinosa's fleet from his own order to arm well.
143 282|||Both captains are told to cooperate and trusted with the assignment.
143 285|||Rafael gives a short formal acknowledgment.
143 290|||Silveira's formal assent distinguishes him from Rafael while retaining the command relationship.
143 294|||Albuquerque dismisses both visitors with the original abruptness.
143 299|||Silveira's casual opening and Rafael's name introduce the question about naval ability.
143 302|||Rafael candidly admits his limits in a short response.
143 307|||Silveira recognizes the same honesty Albuquerque noticed earlier.
143 311|...||Rafael's silence gives Silveira room to reassure him. Use the dialogue's standard ellipsis glyphs.
143 316|There's no shame in that. You can learn as you go.|learn as you go.|Silveira reassures Rafael that he can learn from here onward.
143 319|||Rafael's uncertain reaction prompts Silveira to explain why he brought up the lesson.
143 324|Admiral Albuquerque asked me to teach you a few things, FI.|a few things, FI.|Silveira names who asked and preserves his conversational use of Rafael's name.
143 328|You're going to teach me?||Rafael echoes the offer in surprise rather than reciting a tutorial label.
143 332|Yes, starting with how to beat Espinosa. Do you know how to take down a rival faction?|how to beat Espinosa.;a rival faction?|The immediate task frames a broader lesson about an opposing faction.
143 336|You mean drive Espinosa out of the towns? Couldn't we just keep investing there?|keep investing there?|Rafael proposes successive investments. Silveira explains the missing prerequisite next.
143 340|You've got the right idea. But investment alone won't do it.|investment alone|Silveira credits part of Rafael's answer and gives the player a reason to ask for more.
143 345|||The short question asks why the proposed investment is insufficient and opens the full lesson.
143 347|||The confident answer skips the explanation while preserving its original choice slot.
143 354|Think of Lisbon. Could you cut into Admiral Albuquerque's market share there just by investing?|Admiral Albuquerque's market share;just by investing?|Silveira uses a real earlier example to show why investment alone fails. Keep the market share term and whose share it is together.
143 358|||Rafael recognizes the example and gives the direct negative answer.
143 363|||The lesson explicitly requires a state of war before investment can displace the rival.
143 367|||Rafael draws the exact conclusion about declaring war.
143 372|Exactly. You can attack their fleet at sea, or have your First Mate send a declaration of war through the Guild.|First Mate;through the Guild.|Retain both paths and the installed role label. The Guild's Send Documents menu leads to Declare War.
143 375|||Rafael's short acknowledgment fits the practical instruction.
143 380|When you're at war, winning a battle at sea hurts the enemy's reputation and costs them a little market share in nearby towns.|market share in nearby towns.|The reputation and share penalties follow a naval victory during war and apply in the towns near the battle.
143 383|Move quickly to get a contract in one of those towns. Then you can drive the enemy out by investing.|get a contract;by investing.|The order matters. The win opens an opportunity for a contract, after which investment can displace the rival.
143 387|(I see! This would get us a contract even in a town another faction controls completely!)|controls completely!)|Rafael sees that the technique extends to towns with an existing monopoly, without adding a new rule.
143 392|Still, you can't put Espinosa Co. out of business by investing alone.|out of business;by investing alone.|Silveira adds the crucial exception. Keeping the fixed company name inside the sentence also avoids ambiguous punctuation.
143 395|Why's that?||Rafael invites the explanation of the exception.
143 400|You can't drive a rival from its home base with investment alone. In the end, you have to beat them at sea.|its home base;beat them at sea.|The home-base limitation is explicit and the final victory must be at sea.
143 403|If you aren't sure you can win at sea yet, trade for a while with the campaign funds. Save enough to outfit a fleet and invest in towns.|the campaign funds;invest in towns.|The loss of confidence concerns winning a battle. Silveira advises using the funds as trading capital for ships and investment.
143 406|Thank you for the lesson, Admiral Silveira.|Admiral Silveira.|Rafael thanks Silveira specifically for the lesson on the branch where he heard it.
143 412|Well, I'm glad to have an ally like you. I suppose you didn't need my lesson after all.|my lesson after all.|On the short branch Silveira reads Rafael's answer as confidence and gently needles him about it.
143 416|Oh... I'm sorry.|I'm sorry.|Rafael backs off his confidence and apologizes directly to Silveira.
143 424|Never mind that, FI. Let's take down Espinosa together!|Never mind that, FI.;Let's take down Espinosa together!|Silveira brushes off the apology and returns to the common objective. The substituted name stays with the reassurance.
143 427|||Rafael answers by welcoming the partnership and using Silveira's supported title.
144 5|||Rafael is thinking aloud before Claudio asks what's wrong.
144 10|||Claudio asks what is wrong using Rafael's runtime name.
144 14|Clau, these two tablets make up a map, right?|make up a map, right?|Rafael checks his understanding of both pieces before he explains the problem.
144 19|What are you talking about? Of course they do.|Of course they do.|Claudio's incredulity sets up the obvious remedy.
144 28|I looked at the Upper Stone Tablet and the Lower Stone Tablet. I still have no idea where the Proof is.|Upper Stone Tablet;Lower Stone Tablet;where the Proof is.|Rafael names both registered pieces and admits that neither tells him where to look.
144 35|The Upper Stone Tablet and the Lower Stone Tablet, yes. Still, I can't tell where the Proof is from these.|Upper Stone Tablet;Lower Stone Tablet;where the Proof is|Janus names both pieces and independently reaches the same initial conclusion.
144 48|What are you doing? Of course they don't make sense if you look at them one at a time!|one at a time!|Claudio states what is obvious to him in the bluntest variant.
144 54|Could it be because we're looking at them separately?|looking at them separately?|Arcadius suggests the same solution as a more courteous question.
144 60|You're right! Let's put them together. This is the upper half, so it goes here...|the upper half,|Rafael accepts the suggestion and starts with the upper half.
144 65|And the other one goes below it?|goes below it?|Claudio checks how the lower half fits in the sequence.
144 69|||Rafael agrees and leaves the placement hanging until the physical result.
144 80|They fit perfectly! Wait, what?!|Wait, what?!|Rafael's satisfaction gives way to surprise once the pieces begin to join.
144 86|Look! The two tablets are joining together!|are joining together!|Janus calls attention to the pieces fusing as it happens.
144 92|||Claudio's spontaneous excitement suits the first sight of the tablets joining.
144 96|The two pieces fused into one...|fused into one...|Rafael recognizes that they are now a single tablet.
144 106|||Claudio spots the mark and confidently says it was absent before.
144 112|Wait. Doesn't this look like some kind of mark? Was that there before?|Was that there before?|Janus expresses the same discovery with more uncertainty about whether it is new.
144 119|||Rafael's short question gives the visual discovery a beat.
144 130|That's it! This mark shows where to find Africa's Proof of Conquest!|Proof of Conquest!|Rafael identifies the mark as a location and names the regional Proof.
144 137|C-could this show us where the Proof is?|where the Proof is?|Janus follows the same clue more tentatively and retains his brief stammer.
144 144|Th-that's amazing!||Claudio's excitement briefly catches in his throat.
144 154|All right, let's get going!||Claudio wants to depart right away after interpreting the map.
144 160|Come on, FI, Clau! Let's go find it!|Let's go find it!|Janus urges both companions to act and keeps Rafael's name substitution.
144 166|Yeah, let's go!||Rafael agrees with the group's excitement.
145 6|||Claudio casually gets Rafael's attention using his name.
145 10|||Rafael responds with their familiar nickname.
145 15|Let's get a bite to eat. Oh, we'd better ask Julio along, too.|a bite to eat.;better ask Julio along, too.|Claudio remembers Julio mid-invitation. The familiar Japanese address does not establish kinship with Claudio.
145 19|Right. He was mad when we forgot to invite him last time.|when we forgot|Rafael recalls what happened the last time they left Julio out.
145 23|Exactly. Julio never forgets a thing like that.|never forgets|Claudio grouses affectionately about how long Julio remembers a slight.
145 27|||The casual suggestion shifts the focus to Arcadius without assuming he is with them.
145 30|||Rafael's echo conveys surprise at Claudio's proposal.
145 35|Yeah, he never comes along. We'll drag him out if we have to. Then we can talk man to man.|talk man to man.|Claudio thinks he is asking another man to open up. His assumption is part of the setup.
145 39|He likes being alone. We ought to consider how he feels.|how he feels.|Rafael considers Arcadius's feelings before Claudio misuses the same premise.
145 43|I am! That's exactly why I'll drag him out if I have to. Now, he said he was going to the inn...|to the inn...|Claudio turns Rafael's concern into a reason to insist and remembers where Arcadius went.
145 47|You never give up, do you?|do you?|Rafael reacts to Claudio's pushiness without turning it into a serious quarrel.
145 52|||The speakerless knock sets the scene at the door without adding a narrator.
145 56|||Claudio trails off halfway through the name on seeing something unexpected.
145 62|||Claudio's startled stammer stops before he identifies what he saw.
145 66|Th-that was Arcadius, wasn't it?|wasn't it?|Rafael stammers and asks rather than making an early declaration.
145 70|||The short squeal marks Arcadius's surprise before either visitor speaks again.
145 74|Did you see that?||Claudio checks what Rafael saw.
145 78|||Rafael's stammer confirms it without explaining more.
145 83|||Claudio realizes they may have intruded on something private.
145 87|||The second stammer repeats that response while Rafael is still at a loss.
145 93|!!||Hans's wordless reaction marks his surprise before he addresses the two visitors. Use the same exclamation glyph as the surrounding English.
145 97|||Hans's urgent call identifies both men at the door.
145 101|||Claudio recognizes Hans without implying a family relationship.
145 105|D-don't tell me you saw...||Hans fears they already saw her and trails off before naming what happened.
145 109|||Rafael hesitates because he does not know how to answer.
145 114|Well, I wouldn't exactly say we saw...||Claudio tries to avoid admitting what they saw before she interrupts.
145 118|Both of you... could you come in?|could you come in?|She invites them in so the conversation can continue privately.
145 122|Eire... I mean, A-Arcadius!||Hans starts with her real given name before reverting to the disguise.
145 125|It's all right, Hans. Come on in.|Come on in.|She indicates he no longer needs to hide it from these two and repeats the invitation.
145 131|||Claudio agrees with a short stammer.
145 135|Okay.||Rafael's quiet agreement follows Claudio into the room.
145 140|...||Hans stays silent while she begins the explanation. Use the dialogue's standard ellipsis glyphs.
145 144|So you saw me.||She states the obvious gently rather than asking the men to justify what they saw.
145 148|||Rafael starts to deny it but cannot finish the thought.
145 153|||Claudio makes a second aborted denial before she reassures them both.
145 157|It's all right. Yes, I'm a woman. Arcadius is a name I made up. My real name is Eirene.|My real name is Eirene.|Eirene chooses to explain the alias and give her real name herself.
145 161|I usually keep watch at the door. And of all the days to leave it unwatched...|keep watch at the door.|Hans explains his usual precaution and regrets the rare lapse without inventing why he was away.
145 165|I'm sorry. I didn't want to bother you every time, Doctor. I thought I'd be all right this once.|this once.|Eirene addresses Hans by his role and admits she thought she could manage without asking him again.
145 168|Why did you dress as a man?|dress as a man?|Rafael asks about her reason after she has chosen to tell them.
145 173|Yeah, seems a shame to have to do that.||Claudio chimes in bluntly before she explains her decision.
145 177|When I decided to sail with Hans, I made up my mind to dress as a man.|made up my mind|She describes the disguise as her own decision, made when she chose to sail with Hans.
145 180|There are a lot of rough men at sea. Who knows what some of them might do to a woman in their midst?|a woman in their midst?|Hans voices the risk that motivated the precaution without telling them a specific assault occurred.
145 184|There may be men like that, but there's nobody like that on our crew.|on our crew.|Claudio acknowledges the danger and defends his own companions.
145 188|That's right. They're good people. A little odd, some of them, but good people.|but good people.|Rafael agrees and plays down the crew's faults as eccentricities.
145 193|You're right. I guess I worried for nothing...|worried for nothing...|Hans concedes that he misjudged this particular crew.
145 196|Yes. FI, Clau, everyone's been so kind. Clau can be a little... rough around the edges, though.|rough around the edges, though.|Eirene confirms the crew's kindness, then gently singles out Claudio's rough manners.
145 199|||Claudio's yelp interrupts the serious conversation at exactly the right moment.
145 203|...Am I really that rough around the edges?|rough around the edges?|Claudio echoes the exact phrase after the initial outrage subsides.
145 207|We can talk about that later. Did you ever think about dressing as a woman again?|dressing as a woman again?|Rafael defuses Claudio's reaction and returns to whether she considered ending the disguise.
145 212|How could I tell everyone after all this time that I'm really a woman?|after all this time|She explains why revealing herself now feels awkward.
145 215|We'd be admitting we didn't trust any of you. That would be hard to explain.|didn't trust any of you.|Hans says why revealing the motive would embarrass them and upset the crew.
145 219|||Her direct request makes clear she wants both men to keep the secret.
145 222|Of course. I won't tell anyone.|I won't tell anyone.|Rafael gives a personal assurance that he will not tell the others.
145 226|Y-yeah. We'll keep it to ourselves.|keep it to ourselves.|Claudio adds his agreement with a lingering stammer.
145 229|||Eirene's simple thanks closes the scene without a new demand or explanation.
146 6|||Uddin quietly confirms the full runtime name and leaves the player's reply to identify him. Keep the established punctuation and full-name layout.
146 10|Who might you be?||Rafael returns the question politely without pretending to recognize the visitor.
146 15|Forgive me. I do a little business out of Basra. My name is Abraham Ibn Uddin.|Abraham Ibn Uddin.|Uddin uses his full spoken name, situates his business in Basra and understates its size.
146 18|Oh. P-pleased to meet you.||Rafael is taken a little off guard by his caller's formal introduction.
146 23|I've been hearing a great deal about FO for some time. You seem to be doing quite a bit of business.|quite a bit of business.|Uddin has been hearing reports often. His remark identifies the scale of the business rather than assessing its success.
146 26|Oh, I wouldn't say that...||Rafael deflects the compliment modestly before Uddin asks him for a word.
146 31|There's something I'd like to discuss with you. Do you have a moment?|Do you have a moment?|Uddin makes a discreet request and lets Rafael decide how to reply.
146 34|(He's quiet, but there's something commanding about him. All right...)|something commanding about him.|Rafael notices Uddin's imposing manner without assigning him a rank.
146 40|||Rafael feels that he can hardly refuse. That hesitation distinguishes the affirmative choice.
146 42|||Rafael finds the stranger intimidating. The caption voices his thought before his polite refusal.
146 50|I'm afraid I'll have to ask you to come a little farther.|a little farther.|Uddin warns courteously that the meeting will require the visitor to go on a bit farther.
146 53|Y-yes, of course. I'll come with you.|I'll come with you.|Rafael agrees before Uddin specifies where they will meet.
146 58|||Uddin names the Guild and Basra without implying that they have to travel there together.
146 62|The Guild in Basra. Understood.|The Guild in Basra.|Rafael confirms the meeting place in his own words.
146 66|||Uddin confirms he is going ahead and will wait there.
146 69|||Rafael politely takes his leave until the agreed meeting.
146 73|||Uddin's short farewell mirrors Rafael's.
146 85|I'm sorry, but I should speak to my crew first. I can't make a decision like this on my own.|speak to my crew first.;on my own.|Rafael uses crew consultation as his reason to decline, despite his authority as admiral.
146 90|I was hoping to hear what you thought. Well, forgive me. I expect we'll meet again someday. Goodbye.|we'll meet again someday.|Uddin wanted Rafael's own judgment. He checks himself, apologizes, and leaves open the chance of another meeting.
147 7|||Rafael's stammer and amazement register the setting before Uddin speaks.
147 12|Forgive me for startling you, FI. I'll call you the head of FO from now on.|the head of FO|Uddin moves from the personal name to a formal acknowledgment that Rafael heads the substituted company. The company suffix stays inside the sentence.
147 15|||Rafael returns the more formal address while keeping the correction audible.
147 19|I'll get straight to the point.|straight to the point.|Uddin says he wants to move directly to why he arranged the meeting.
147 23|||Rafael's stammer shows he is still taken aback.
147 28|||Uddin asks the other company to ally with his own.
147 32|An alliance...?||Rafael echoes the same term Uddin just introduced.
147 43|I can see why you're wary. I know it's a lot to ask so suddenly.|a lot to ask so suddenly.|Uddin recognizes both the abrupt timing and the boldness of the request.
147 47|An alliance is a serious decision for any company. You can't make it lightly.|make it lightly.|Uddin acknowledges the weight of the decision in the branch that does not cite Africa.
147 53|I can see why you're wary. I've looked into what happened to you in Africa.|what happened to you in Africa.|Uddin knows about Rafael's prior experience in this branch and says he investigated it.
147 56|I understand why you'd be wary of another alliance. I'm asking you to consider this one all the same.|all the same.|Uddin recognizes the reason for hesitation while making a deliberate request anyway.
147 62|...||Rafael's silence lets Uddin recognize that he needs time. Use the dialogue's standard ellipsis glyphs.
147 67|You don't have to answer now. Sleep on it. That's all I wanted to ask. I've arranged a room for you. Go on, get some rest.|Sleep on it.;I've arranged a room for you.|Uddin wants an overnight decision and has arranged lodging. He dismisses Rafael courteously.
147 70|||The escort briefly directs him toward the accommodation.
147 74|||Rafael follows with a subdued thanks.
148 5|||Uddin asks for the decision after giving Rafael time to think.
148 9|Yes. I've thought it over...||Rafael begins his answer and hesitates before the choice appears.
148 13|Very well. What have you decided?||Uddin prompts for the decision without presuming Rafael's answer.
148 17|...||The pause leaves the decision to the player. Use the dialogue's standard ellipsis glyphs.
148 24|||The acceptance plainly gives assent and fits the original result slot.
148 26|||The polite refusal is clear in the original slot and still fits Rafael's speech.
148 33|I'm putting my trust in you. I look forward to working together.|look forward to working together.|Rafael commits personally to the alliance and expects cooperation from both sides.
148 37|I'm pleased, Mr. FA. Shall we talk business?|I'm pleased, Mr. FA.;talk business?|Uddin responds warmly and addresses Rafael formally by his substituted surname before asking to negotiate.
148 40|Y-yes, of course.||Rafael stammers his assent to starting negotiations.
148 45|Let's continue in another room. Please show Mr. FA to the reception room.|the reception room.|Uddin makes the instruction to the attendant explicit and keeps the surname substitution.
148 48|||Ibn Niyadi promptly acknowledges the order.
148 53|||Uddin gives the registered Nagalpur name, supported title and exact area of influence.
148 57|The man worships money. His grasping way of doing business has caused us no end of trouble.|no end of trouble.|Uddin judges Nagalpur's greed and lack of dignity through his methods and their consequences.
148 62|His company is wealthy, and that makes him dangerous. As for his character, there's very little to admire.|very little to admire.|Uddin distinguishes the considerable power of Nagalpur's company from his opinion of its head.
148 66|||Uddin expects a shared effort to succeed in time.
148 69|||Rafael is listening and gives a brief assent.
148 74|||Uddin anticipates a concern and lets Rafael identify it.
148 77|||Rafael brings up the future of the agreement once Nagalpur is defeated.
148 82|Exactly. You saw that coming. Our alliance ends there. We have nothing in writing. I'd like a nonaggression pact after that.|nothing in writing;nonaggression pact|Uddin confirms the alliance's end, the lack of a written agreement, and the proposed successor arrangement.
148 85|||Rafael echoes the unfamiliar proposal as a question.
148 90|I'm based in Arabia. Our companies can share those markets, within reason. What you do in other cities and ports is up to you.|within reason.|The arrangement limits coexistence in Uddin's home region and leaves other cities and ports to Rafael's discretion.
148 93|So you want us to limit how much business we do in Arabia.|business we do in Arabia.|Rafael confirms what the restriction means in practice.
148 97|That's right. And I give you my word we won't stand in your way.|we won't stand in your way.|Uddin reciprocally promises his company will not interfere.
148 121|Uddin gave you part of his market share in Muscat.|market share in Muscat.|The system identifies the partial transfer and its location without duplicating the word share.
148 152|Uddin gave you part of his market share in Socotra.|market share in Socotra.|The second transfer uses the same distinct location and parallels the Muscat notice.
148 163|||Rafael accepts the terms and asks whether there is anything else to discuss.
148 167|No, that's all. Thank you for coming to see me.|Thank you;coming to see me.|Uddin closes the discussion by acknowledging the trouble Rafael took to meet. The thanks begins a complete line.
148 170|The pleasure's mine. FO is still small, but you can count on us.|you can count on us.|Rafael returns the courtesy, describes his company modestly and promises its support.
148 174|Thank you. I'm counting on you.|I'm counting on you.|Uddin thanks Rafael and expresses confidence in him.
148 177|||Rafael ends with an immediate call to act together against Nagalpur.
148 182|Agreed. We'll move forward together.|move forward together.|Uddin accepts Rafael's call and confirms the campaign will be shared.
148 196|||Uddin asks to confirm his understanding of the refusal.
148 200|||Rafael answers with a deferential apology before Uddin reacts.
148 213|Still smarting from what happened in Africa, then?|what happened in Africa, then?|Uddin conjectures that the earlier experience still hurts.
148 216|No, that isn't what I meant...||Rafael starts to reject Uddin's explanation for his decision.
148 224|I respect your judgment. We'll be rivals now, both after control of the Indian Ocean. An odd way to put it, isn't it?|the Indian Ocean.;isn't it?|Uddin treats Rafael as a worthy rival in the competition for supremacy and checks his phrasing on the same page.
148 228|Y-yes... Go easy on us, all right?|Go easy on us, all right?|Rafael nervously acknowledges the phrasing and uses a small joke to soften the farewell.
148 232|Farewell, then.||Uddin ends the refusal branch with a firm leave-taking.
149 5|I keep thinking about this Evergreen Lotus Leaf. It's a map to the Proof, right?|Evergreen Lotus Leaf.;to the Proof, right?|Rafael identifies the exact item and asks whether it really represents the map.
149 10|If Uddin says it is, it must be.|it must be.|Claudio trusts Uddin's word and gives Rafael a concise answer.
149 13|||Rafael wonders which object they need to combine with the leaf.
149 32|||Janus proposes the correct registered item label as a question.
149 40|||Arcadius's same suggestion keeps the same item label and courteous tone.
149 46|Let's put the leaf on the platter and see... Nothing's happening.|Nothing's happening.|Rafael attempts the simple placement before observing that it has no immediate effect.
149 50|Well, what do we do now?|what do we do now?|Claudio asks for another step after the obvious test fails.
"""


def reviewed_inputs():
    packet, prior, release, names, catalogue = map(base.load, (SOURCE, PRIOR, parent.RELEASE, NAMES, CATALOGUE))
    packet["groups"] = [g for g in packet["groups"] if g["block"] in BLOCKS[0]]
    prior["records"] = [row for row in prior["records"] if row["block"] in BLOCKS[0]]
    assert tuple(g["block"] for g in packet["groups"]) == BLOCKS[0]
    return packet, prior, release, names, catalogue


def all_decisions(packet):
    decisions = []
    groups = {g["block"]: {r["source_record_index"]: r for r in g["records"]} for g in packet["groups"][:2]}
    for block in (141, 142):
        p = ROOT / f"B{block}_contextual_decisions_registered_parent.json"
        draft = base.load(p)
        assert draft["paired_source_sha256"] == base.digest(SOURCE)
        assert draft["candidate_sha256"] == base.digest(parent.ROM)
        for record in draft["records"]:
            assert record["block"] == block
            row = groups[block][record["source_record_index"]]
            assert record["Japanese"] == row["Japanese"] and record["previous_English"] == logical(row["current_English"])
            phrase = {5: "deciphering the map", 26: "Proof of Conquest;in the North Sea!"}.get(record["source_record_index"], "") if block == 142 else ""
            decisions.append("|".join((f"{block} {record['source_record_index']}", record["english"],
                                       phrase, record["localization_note"])))
    return "\n".join(decisions) + "\n" + DECISIONS.strip()


source = checked_text(precedent.source, {
    'map(base.load, (SOURCE, PRIOR, parent.RELEASE, NAMES, CATALOGUE))': "reviewed_inputs()",
    "DECISIONS.strip().splitlines()": "all_decisions(packet).splitlines()",
    "len(rows) == 351": "len(rows) == 270",
})


if __name__ == "__main__":
    scope = precedent.scope | globals()
    exec(compile(source, __file__ + "::review", "exec"), scope)
    scope["main"]()
