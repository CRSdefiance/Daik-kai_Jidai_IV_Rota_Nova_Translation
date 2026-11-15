"""Individual comparisons after reading all337 source/current/draft exchanges."""
from scripts.maria337_contextual_writer_v1 import write

# R retains current prose, D selects the independent draft, T supplies a contextual amendment.
SPECS={
125:'''4|R|Retain the governor's natural recognition of Admiral FA.
7|R|Retain the clear thwarted coup and credit to the fleet; this does not claim Spain lost control.
10|R|Retain the governor's restrained formal transition to the remaining concern.
14|D|Normalize the questioning reaction to the dialogue's ASCII glyph style.
18|D|Restore hearsay and an unidentified person; the key was sought by Escante, not established as his owned treasure.
22|D|Restore Maria's specific suspicion that this is the Proof map.
25|D|Replace the location-label fragments with Xien's natural reaction to the difficult journey.''',
126:'''4|D|Restore Xien's recollective lead-in and exact-fit suggestion; bind both provisional item names before approval.
8|D|Restore Maria's recognition rather than the flat size label.
12|D|Replace Shall the blade enter the sheath with Xien proposing and trying the action himself.
15|D|Give the elder's startled exclamation a consistent voice.
21|D|Restore Maria asking Xien what he did, not merely asking what happened.
25|D|Preserve his uncertainty and the reassurance that opening their eyes is safe.
29|D|Give Maria's discovery and timing question a complete spoken progression.
33|R|Retain the idiomatic puzzled question, which fits the unexplained light and map.
37|D|Preserve the full Proof of Conquest term and distinguish the map from the treasure.
40|D|Make Xien's baffled causal recap conversational rather than ending in the label No sense at all.''',
127:'''4|D|Restore Al's defiant refusal to be underestimated, rather than the unrelated Think again.
7|D|Use a direct firing instead of the unnatural Someone like you is fired.
12|D|Replace submissive ordered-to-leave phrasing with Al's angry decision to walk out.
15|D|Give Xien's sympathetic observation a natural conversational sentence.
18|R|Retain Maria's concise, idiomatic question about the man's build.
22|D|Connect the physical admiration, temper and anticipated trouble in Xien's considered voice.
26|D|Replace the ambiguous hard man with Maria's pointed question about managing difficult people.
29|T:You've got confidence, I'll give you that. ...Wait, are you Admiral FA? I'll warn you now: he won't be easy to handle.|Repair the full-width I and localize the fleet-leader address consistently as Admiral; preserve the warning and casual guildmaster voice.
32|R|Retain the skill question; the surrounding recruitment and reply make fighting the clear subject.
36|R|Retain the guildmaster's natural rough speech and undefeated-fighter observation.
39|D|Replace the erroneous solitary period with Xien's interested reaction.
43|D|Restore Xien's address and Maria's clear invitation to catch up with the man.
47|D|Give Maria a natural spotted-him remark rather than the label There.
51|D|Restore Al asking their purpose rather than a contextless What.
55|D|Make the job offer a natural direct statement in Maria's voice.
59|D|Preserve Al's surprised hiring question and demand to know her identity.
62|D|Restore Maria's conversational description of her private fleet without adding an official commission.
66|R|Retain the natural startled recognition of the known Admiral FA.
69|D|Replace the unidiomatic Good. Easy. with recognition making her explanation easier.
72|D|Restore Maria's personal need for strong fighters and confident invitation, replacing the passive warrior requirement.
76|R|Retain Al's blunt disbelief about fighting Western enemies; the rough question suits his voice.
80|D|Make the provocation about her judgment of him explicit rather than an unspecified mistake.
83|D|Keep the enthusiastic acceptance and boast in Al's rough spoken register.
87|D|Restore Xien's natural request for the still-unknown name.
91|R|Retain Al's terse self-introduction; a name alone suits this blunt man.
95|D|Replace Empty boasting is hated with Maria's personal warning and expectations.''',
128:'''4|R|Retain Angelo's idiomatic quick apology after the encounter.
8|D|Normalize the silent reaction without altering its pause.
12|R|Retain Yukihisa's clear question in response to Maria noticing the pendant.
16|D|Restore the inferred ownership and the portrait being inside the pendant.
21|D|Replace precious woman with a natural tentative guess about someone dear to him.
24|R|Retain Maria's natural practical proposal to return the pendant.
29|R|Retain the Italian exclamation and anguished sister/pendant connection.
32|D|Make the frantic search intelligible English rather than disconnected denials.
35|D|Restore Yukihisa explicitly identifying the man they need.
39|R|Retain the already natural frantic pendant cry, identical to the independent draft.
42|R|Retain the complete formal summons, calming request and courteous return question; the diction suits Yukihisa.
46|R|Retain the excited portrait/pendant recognition without adding new information.
50|R|Retain Maria's clear surprised clarification that the pictured woman is his sister.
53|D|Replace the impersonal search-continues wording with Angelo's own concern and ongoing search.
57|D|Give Maria's sympathetic acknowledgment and wish a warm spoken form.
62|D|Restore the request to hire him, modest prior sailing experience and promise of usefulness.
65|D|Angelo wants to search with them; do not turn the line into an order for Maria to conduct the search.
69|T:What say you, Admiral?|Retain Yukihisa's distinctive formal phrasing while restoring the supported address to Maria.
73|D|Preserve Maria's thoughtful agreement and sense of an encounter with meaning.
77|D|Keep Angelo's joyous Italian exclamation and introduce himself in a complete personal sentence.
80|D|Repair both full-width I characters while preserving FI/FA and the reciprocal welcome.''',
129:'''4|R|Retain the quiet, natural request for a private word that opens the confession.
8|R|Retain Maria's simple accepting response and hesitation.
12|D|Clarify Xien offering privacy, rather than an ambiguous general departure.
16|D|Restore Angelo's wish for everyone to listen; use Xien rather than inventing a grandfather relationship.
19|R|Retain Xien's brief assent before the serious disclosure.
23|R|Retain the hesitant sister-name lead-in; its unfinished rhythm fits the confession.
27|R|Retain the clear reminder of their promise to help in the established search context.
30|D|Use a natural contraction in Angelo's correction rather than stiff separate declarations.
34|R|Retain the restrained Bianca-is-gone disclosure, which leaves Maria to seek clarification.
38|R|Retain Maria's natural echo question, identical to the independent draft.
42|D|Preserve his only family, illness and exactly three years, in Angelo's own emotional voice.
45|D|Restore the contradiction with what he said about searching, rather than only asking about a past search.
48|D|Restore Angelo's first-person inability to accept the death instead of an impersonal passive truth.
52|D|Restore his self-deception and his own worldwide search, replacing the passive world was searched.
55|R|Retain Maria's sympathetic name-only response, identical to the independent draft.
59|D|Restore the fever and Angelo's collapse, both lost by When laid low.
63|D|Preserve the sister's reported advice as personal speech, without explaining it as a dream or living return.
66|D|Normalize the quiet silence to the established ASCII style.
70|D|Preserve Xien's present concern for Angelo in the reported sister encounter, without forcing it into past tense.
74|D|Keep the encouragement to live for his late sister in natural elder speech.
78|D|Make Maria's reassurance warm and personal; the crew-as-family bond is explicit in Japanese.
82|D|Replace Stay with me from now on with Angelo's natural request for continued companionship.
85|T:We'll be counting on you, too.|Give Maria's reciprocal welcome warmth appropriate to the family reassurance rather than businesslike Likewise.
89|T:... (Bianca... I'm sorry. From now on... I'll live for you, too.)|Preserve the private-thought parentheses and restore Angelo's active promise instead of This life will be lived.''',
130:'''4|D|Restore that Carlo wants his usual order or amount, not merely a usual type of cinnamon.
8|D|Restore Maria's private recognition of another customer; Guest incorrectly suggests lodging.
12|D|Use a natural merchant acknowledgment and price presentation rather than label-like instructions.
16|R|Retain the merchant customer's natural clipped surprise at a price increase.
20|R|Retain Adil's casual denial and same-as-always claim, which set up the bargaining.
23|D|Keep Carlo's amused familiarity and knowledge of Adil's wholesale cost explicit.
26|R|Retain Adil's short protesting interruption in the negotiation.
30|R|Retain the clear harvest/demand bargaining argument and idiomatic you-can-do-better request.
34|D|Replace the compressed supplier slogan with Carlo's natural alternative-shopping leverage.
38|D|Give Adil's reluctant concession a spoken rhythm rather than broken notes.
42|R|Retain Carlo's complete, natural question about Adil's fever.
45|D|Replace complaints about my trade with Adil's personal defensiveness about his business.
48|D|Make Carlo's shift from bargaining to concern clear and conversational.
51|D|Preserve Adil dismissing the concern before noticing his own chills.
54|D|Restore Carlo postponing his own purchase to tomorrow and asking Adil to close for today.
57|D|Keep Adil's agreement and apology to the waiting visitors in his informal voice.
63|R|Retain Carlo's natural apology and recognition of their trading purpose.
66|R|Retain Maria's idiomatic brief question; Adil's illness is clear from the complete exchange.
70|R|Retain the concise answer identifying the complexion as Carlo's clue.
82|T:Sharp eyes. I'd say he's a match for me.|Preserve Fernando's boastful comparison without downgrading Carlo to nearly as good when the source says a match.
88|D|Use Maria's natural contraction and personal uncertainty about noticing the illness.
92|D|Restore Carlo as the person sensitive to others' health, replacing the subjectless fragment.
96|R|Retain Maria's natural parenthesized surprise; it remains an internal reaction.
100|D|Restore tomorrow morning, the trade house and tentative offer to make up for the delay, rather than promising repayment.
103|D|Agree to the future plan naturally rather than sounding as if they must leave immediately.
107|R|Retain the innkeeper's warm, natural thanks for yesterday.
111|R|Retain Carlo's clear question about Adil; a contraction is optional here.
115|R|Retain the colloquial answer that he is resting at home as a precaution.
118|D|Use recovery language suited to illness rather than the more injury-associated heals.
122|D|Restore the innkeeper's own ignored advice and unfinished account of Carlo's timely help.
126|D|Use lifesaver as natural gratitude rather than unnecessarily asserting a proven near-death medical event.
130|D|Make Carlo's appreciation and redirection of the thanks to the delayed visitors flow naturally.
134|R|Retain the clear apology and modest unspecified gift offer; no item or family relationship is added.
140|D|Preserve Carlo's consideration for their time and invitation to shop first without issuing label-like orders.
144|R|Retain Adil's natural greeting and apology on returning.
147|R|Retain the innkeeper's sharp recognition of his disobedient return, identical to the draft.
151|R|Retain Carlo's natural insistence that Adil should be resting in bed.
154|D|Replace prime business with Adil's idiomatic refusal to stay in bed on a good trading day.
158|D|Give the innkeeper a natural direct rebuke rather than talking abstractly about a hopeless man.
162|D|Preserve Carlo's relief and warning in a warm spoken rhythm.
166|D|Restore Carlo postponing his own visit and asking Adil to serve these people.
169|T:Take good care of your family and your health. I'll be seeing you.|Keep the thematic family/health advice without the unnatural English form of address Travelers.
172|D|Normalize Maria's thoughtful silence.
177|R|Retain the natural request to wait, identical to the independent draft.
181|R|Retain Carlo's brief attentive response, identical to the draft.
185|R|Retain Maria's complete, polite recruitment offer and recognition of his trading skill.
189|R|Retain Carlo's natural surprise at the sudden offer.
193|D|Thinking since yesterday is not a fully formed plan made yesterday; restore her ongoing consideration.
196|D|Make Carlo's merchant-versus-sailor objection personal and natural.
199|D|Use an idiomatic business-talent explanation instead of the translated market-prices-yes phrasing.
203|D|Normalize Carlo's silent hesitation.
207|R|Retain the two clear questions about sailing alone and leaving family; neither assumes an invented relationship.
210|D|Restore a year ago rather than the potentially different calendar statement last year, and retain the grief-stricken pause.
213|D|Normalize Maria's silent reaction to the loss.
218|D|Restore Carlo taking responsibility for neglecting his daughter rather than hiding it in a passive care-was-neglected construction.
221|T:I didn't act in time, and my wife caught it, too... I lost them both.|Keep delayed action and transmission without inventing a completed treatment; retain Carlo's first-person responsibility and both deaths.
225|R|Retain Maria's natural, brief sympathetic reaction to the tragedy.
229|D|Restore the personal emptiness of his work and the resulting concern for others' health.
232|D|Reconnect Maria's realization explicitly to his concern for the shopkeeper.
236|D|Ask naturally about returning home rather than presenting the label Your homeland.
240|R|Retain the grief-stricken short clauses about Venice's happy memories and inability to live there alone.
244|D|Normalize the pause before Maria's compassionate proposal.
248|D|Preserve the conditional companionship offer rather than diagnosing hurt in a translated rhetorical question.
252|D|Normalize Carlo's questioning reaction.
256|D|Make Maria's shared-life and new-family invitation warm and personal rather than an abstract rule about crews.
260|R|Retain Carlo's natural hesitant realization that they are offering to become his family.
264|D|Replace Should that suit you with a warm voluntary invitation.
268|R|Retain Carlo's quiet gratitude and clear acceptance; the surrounding invitation supplies what he accepts.
271|R|Retain the concise self-introduction and welcome; bind Sinato to approved name consumers before final approval.''',
131:'''4|D|Preserve Maria's tentative self-assessment rather than stating that she definitely drank too much.
8|R|Retain Cristina's informal agreement and new-music reaction in the drinking context.
13|D|Use music for the source tune and avoid assuming that anyone is singing.
16|D|Preserve Cristina recognizing the tune and briefly excusing herself.
19|R|Retain Maria's natural question about the unexpected reaction.
24|D|Replace Wow, that woman with a natural cheering patron's admiration.
27|D|Praise her dancing in spoken English rather than the abstract pair Beautiful and skilled.
32|R|Retain Maria's simple admiring response to the performance.
36|D|Preserve both patrons' shared cheers and elongated bravo in natural English stage-caption form.
39|D|Localize the written applause cue without inventing a native sound effect or extra speaker.
43|D|Restore Cristina's spontaneous inability to resist a favorite tune, rather than flat subjectless declarations.
46|D|Restore the comparison with Eastern dances; new passion generally is a broader, different claim.
49|R|Retain the complete, natural identification of flamenco and its cultural context.
52|D|Restore Maria's wish to see the dance again, not the ambiguous instruction Again someday.''',
132:'''4|D|Retain Jam's exuberant response to Calicut's heat without adding the claim that the city is the best.
15|R|Retain Richard's restrained formal complaint that the climate does not suit him.
20|D|Replace the weather-label fragment with Xien's natural agreement.
27|T:The scenery's quite different here.|Remove the unsupported directional addition south while preserving the observed change in scenery.
30|D|Make Jam's excited discovery and appetite conversational rather than announcing Meals for sale.
34|R|Retain Xien's attempted interruption and dry recognition that Jam has already rushed off.
37|R|Retain Maria's exasperated understatement in the complete rushed-off context.
41|R|Retain the natural urgent call to the admiral for help; elongating it is optional.
44|R|Retain Xien's natural recognition question, identical to the independent draft.
47|D|Replace Rare words from him with an idiomatic observation about Jam unusually asking for help.
58|D|Make Yukihisa's food-related hypothesis a complete question, not diagnostic labels.
65|D|Restore Jam's embarrassed disbelief at being caught by a child.
70|D|Use bet in Samwell's childlike speech while preserving the provocative he's-mine claim that the next lines question.
74|R|Retain Xien's natural shocked question without adding an unnecessary description.
78|R|Retain Maria's clear question about what the ownership claim means.
82|D|Clarify that Jam was the promised winner of the food bonus, keeping his temptation and unfinished explanation.
86|R|Retain Xien's natural objection to the claimed consequence of losing the bet.
90|D|Preserve exactly ten heads and Jam's promise in Samwell's direct childlike explanation.
93|D|Restore the normally qualifier and Jam's curse rather than implying ten heads is literally impossible.
97|R|Retain Samwell's natural smug insistence that it happened.
100|R|Retain Maria's direct, idiomatic command to inspect the coin.
104|R|Retain Samwell's nervous refusal and stammer; stronger punctuation is not required.
107|D|Restore Xien's suspicion of cheating, not merely a general comment that it is odd.
111|R|Retain Jam's angry cheating question and immediate demand to see the coin.
114|R|Retain the short startled cry during the coin seizure.
118|D|Normalize Jam's wordless exclamation to ASCII.
122|D|Make Samwell admit that they caught him, replacing the awkward Caught fragment.
126|T:You've stacked two coins together. Heads on both sides.|Preserve the specific stacked-coin mechanism and double-headed result in Xien's explanation.
130|R|Retain Jam's idiomatic curse and angry little-cheat accusation.
133|R|Retain the child's flippant laugh and apology.
137|R|Retain Jam's clear, natural rejection of the inadequate apology.
140|D|Make Samwell's attempt to reverse the wager sound like a child's crafty suggestion.
143|D|Restore Xien asking what Samwell proposes to do, rather than an ambiguous What now.
147|D|Restore the boy's explicit first-person offer to do anything if they take him.
158|D|Preserve Yukihisa's judgment of the maneuver as brazen, rather than generic admiration for boldness.
172|D|Retain Richard's pompous rhetorical doubt about usefulness in a natural spoken question.
175|D|Use the idiom You're one to talk to make Jam's private accusation of hypocrisy clear.
181|R|Retain Xien's idiomatic exasperation and speechlessness.
187|D|Restore Samwell as the one claiming competence; the subjectless current wording could describe the travelers instead.
191|D|Preserve Jam's eager first-person intention to work Samwell hard and his request to the admiral.
195|D|Normalize Maria's uncommitted silence.
199|R|Retain Xien's firm, natural veto in response to Jam's request.
203|D|Restore the child's pleading address to the admiral and drawn-out appeal.
207|R|Retain Jam's natural plea followed by the comic realization that Samwell is pleading too.
210|D|Keep the elephants and desire to travel in a child's direct voice rather than poetic lands-are-calling phrasing.
214|D|Make Maria's considered assent to the request natural after her pause.
218|R|Retain the clear joyful celebration; the exact stammer is optional in English.
222|R|Retain Xien's natural incredulous question and the FI substitution.
225|D|Use run rings around and real gem to preserve the outmaneuvering and valuable-find idioms naturally.
229|R|Retain Jam's natural realization that he may have been used and his final curse.
233|D|Preserve Samwell's joy, first voyage and introduction in a natural childlike exchange.
238|R|Retain Maria's simple, reserved welcome after the boisterous introduction.
242|D|Use the natural nautical dead-weight idiom for Xien's continuing skepticism.''',
133:'''5|D|Restore the apparently/not-yet nuance while keeping the absent referent neutral; do not invent a named man or woman.''',
134:'''5|D|Independently restore the uncertain absent-party report with a neutral referent; this separate source record is not duplicate credit.''',
135:'''4|D|Use the rough attention shout supplied by the Japanese rather than adding the distinct spoken taunt Take that.
8|R|Retain the natural panicked cry for help; Cesare's formal pedantry emerges in the subsequent explanation.
18|R|Retain Richard's short startled question in its optional reaction path.
24|D|Restore Xien asking what is happening rather than only repeating What.
31|D|Preserve Maria pointing out the beating over there in natural contracted speech.
35|R|Retain the complete elder's observation and offer of aid; the formal diction suits Xien.
39|R|Retain Maria's brief assent, identical to the draft.
51|D|Restore Yukihisa joining the others, rather than potentially proposing to act alone.
68|D|Preserve the elder's supported young-man address and concerned inquiry.
72|T:Ow... Not... very well, I'm afraid.|Keep Cesare's pained hesitation and polite formality without the unnatural not very all right construction.
76|D|Make Maria's question explicitly about the past fight, not a general reason to fight.
88|D|Preserve the tentative observation about villains and set up Yukihisa's later parallel about eccentrics.
95|R|Retain Cesare's natural hesitant lead-in before the explanation.
99|D|Normalize Maria's silent prompt.
104|R|Retain the clear flat-world claim; world is a natural equivalent for Earth in this statement.
107|R|Retain Xien's short prompt asking him to continue.
111|D|Restore Cesare's personal intention to correct their error and his emphatic certainty, rather than an impersonal requirement.
114|R|Retain Maria's dry, paused prompt for what followed.
118|D|Restore Cesare as the person who began explaining; an explanation did not begin by itself.
122|D|Keep the men's rejection and attack directed at Cesare in complete personal narration.
126|D|Clarify Xien's incomplete understanding before the crucial blunt quote, rather than judging the event inherently illogical.
129|D|Make Cesare's reply grammatically follow Xien's first-person lack of understanding.
133|D|Restore Cesare owning his blunt correction; this first-person delivery drives the social joke.
137|R|Retain Maria's concise, natural deduction that the men became angry.
141|D|Restore the comic astonishment that she could deduce their reaction.
144|R|Retain Xien's dry, natural comment that anyone would know.
148|R|Retain Cesare's idiomatic formal puzzlement, fitting his literal-minded confusion.
151|D|Keep Cesare's first-person indignation and expectation of gratitude in natural emphatic speech.
154|D|Restore personal gratitude for learning and the revealed truth in an intelligible sentence.
166|D|Restore too to connect Yukihisa's eccentric remark to his earlier villains-everywhere observation.
172|D|Praise the thirst for knowledge while preserving Xien's unfinished reservation, rather than generic Learning is good.
176|D|Normalize Maria's thoughtful pause.
180|D|Ask naturally about knowledge of ships rather than the compressed Do you know ships.
184|D|Preserve the explicitly supported past captain role and refitting hobby in Cesare's own voice.
195|D|Keep Yukihisa's personal disbelief rather than assert that the true past captaincy is absurd or false.
202|T:I see... Then there shouldn't be a problem.|Give Maria's practical assessment a natural sentence while preserving its tentative seems-no-problem quality.
205|D|Normalize Cesare's questioning reaction.
216|R|Retain Richard's natural formal objection to taking this man aboard.
222|D|Restore Xien questioning Maria's intention directly, with FI preserved.
229|D|Restore Maria's personal fondness for his curiosity and compassionate assessment of his personality.
241|R|Retain Yukihisa's dry brief agreement about the difficulty of ordinary life for him.
255|D|Repair the missing article and preserve Richard's formal disbelief about Maria's unusual kindness.
260|D|Distinguish Xien's elder, softhearted observation from Richard's alternative wording.
266|R|Retain Cesare's hesitant attempt to get their attention, identical to the draft.
270|D|Make Maria's apology for leaving him out of the discussion natural and past-directed.
273|R|Retain the clear question about her admiral role after his hesitant attention request.
276|D|Ask whether he has heard of FO, rather than imply personal acquaintance with an organization.
280|R|Retain Cesare's clear formal recognition and both FI/FA substitutions.
284|D|Make Maria's recognition-to-recruitment progression natural without changing the navigator offer.
288|D|Preserve his enthusiastic acceptance in the distinct formal register used by Cesare.
291|D|Complete Maria's decision naturally before the concise request for his name.
294|D|Restore a full personal introduction and grateful tone; the Cesare surname remains provisional until approved consumer binding.
297|D|Replace the ungrammatical what did Admiral like with Xien's natural inability to see her reason.
309|R|Retain Yukihisa's concise formal comic agreement that her reasoning is baffling.
321|R|Retain the natural transition into Cesare's practical advice.
325|D|Preserve the contract/route-building phase and one-percent/one-to-five rule in natural instructions; exact goods unit needs UI binding.
328|D|Keep the transition to buying ships as shares and purchasable goods grow, without forcing a singular added ship.
332|R|Retain the clear, complete instruction to consider size and price first.
335|D|Restore inability to buy enough goods and extra crew needs explicitly, avoiding the added assertion about specific wage costs.
338|D|Repair the run-on price explanation while preserving all three exact source ranges and their gaps.
341|R|Retain the natural small-ship affordability and fleet-capacity advice in the cargo-trading context.
344|D|Replace once cash grows with a natural transition after trading creates spare funds.
348|D|Repair the missing sentence boundary and preserve two/three masts, speed and extra sail crew.
351|D|Restore up to five as the maximum cargo spaces and keep the noncombat condition; room labels await exact UI binding.
354|D|Keep the advice conditional on opening distant routes rather than asserting every long route requires extra holds.
357|R|Retain the complete concise advice about large ships for conflict with another power.
360|D|Remove armed guns and make the flagship equipment/winning connection natural and precise.
363|R|Retain the clear two-medium versus one-large price/cargo comparison and reminder about available cash.
366|D|Restore eventual replacement and the optional retention of old ships; local/regional fleet terminology remains to bind.
369|D|Remove unsupported sir to the female captain and replace This man with Cesare preparing departure himself.''',
136:'''10|D|Restore the visitor's arrival and Fernando's natural insistence on playing, not a generic demand to accept.
15|D|Make the drinking wager and simple-game invitation clear, friendly gambler speech.
19|D|Explain alternating one-to-three choices naturally without inventing the starting coin count or first player.
23|R|Retain the complete, natural last-coin-loses rule and invitation to begin.
SC3_B136_CHOICE_356_0|D|Replace the corrupted caption 産es with the source-supported acceptance; native provider and first glyph still need fresh verification.
SC3_B136_CHOICE_356_1|D|Replace the corrupted caption 札ecline with the source-supported refusal; preserve index/order and verify the whole first glyph.
46|D|Make Fernando naturally claim the drink he won rather than the fragment Then a drink.
50|R|Retain the idiomatic drink appreciation, thanks and casual farewell.
59|D|Use Fernando's natural admission that he has not lost in a while, instead of the label A rare loss.
69|D|Make Maria's teasing assessment, refusal of alcohol and confidence question a natural exchange.
73|D|Use sharp eye as conversational gambling vocabulary that carries through his later observational demonstration.
76|D|Replace Both belong to me with a natural first-person boast.
80|D|Keep Xien's skeptical echo consistent with Fernando's sharp-eye wording.
84|R|Retain the natural idiom about not judging by appearances.
88|D|Restore asking Maria to guess the distant couple's topic, rather than asking for inaudible words as known fact.
91|R|Retain Maria's natural tentative proposal guess; the couple context supplies its romantic sense.
95|R|Retain Fernando's confident, idiomatic elementary-case deduction.
99|D|Normalize Maria's silent question.
103|R|Retain the natural invitation to watch, identical to the independent draft.
107|D|Make the woman's rejection of his thinking clear rather than an inability to understand his reasoning.
110|R|Retain the man's natural curt counteraccusation and reciprocal selfishness claim.
113|D|Use the idiom see each other for their dating relationship rather than a generic future meeting.
116|D|Preserve their mutual agreement to end the relationship explicitly.
119|D|Normalize Maria's silent reaction to the confirmed breakup.
123|R|Retain Fernando's natural confident called-it response after the confirmation.
127|R|Retain Maria's idiomatic amazement and question about how he knew.
131|T:Her fist was clenched under the table. She was holding back her anger. She wasn't talking about love.|Keep the physical clue and deduction as natural speech instead of a stage-pose label or advice about how to discuss love.
135|T:And he never even looked at her. Does that look like a man sitting across from the woman he loves?|Preserve avoidance of her gaze without the possessive phrase his woman or adding a narrower eye-contact-only claim.
139|R|Retain Maria's natural surprised recognition of how much he observed.
143|T:With an eye like mine, I can read my opponents.|Restore Fernando using his own skill rather than insight acting by itself, without inventing a specific card game.
146|D|Preserve his claim that observation plus his luck wins, rather than luck alone being the actor.
149|T:Quite a talent. Why not join FO and put it to the test?|Make the invitation explicit and avoid the unnatural my before the substituted organization name.
153|R|Retain the natural colloquial surprise at the sudden offer.
157|D|Restore Fernando choosing to toss the coin and personally joining on heads, rather than abstract action notes.
163|D|Give Maria's repeated refusal of alcohol and recruitment request natural impatience while preserving FO.
167|D|Restore Fernando offering another toss, not telling Maria to ask the coin herself.
192|R|Retain the gambler's clear conditional refusal to entrust his life to someone unlucky.
208|D|Replace the passive life-gets-wagered construction with Fernando's committed personal wager.
211|D|Restore the explicitly spoken Fernando Dias introduction, rather than replacing his first name with a repeated surname.
214|R|Retain Maria's natural welcome after the successful recruitment.
228|R|Retain the idiomatic poor-pickings complaint without inventing recent numerical losses.''',
}

def parse():
    decisions={}
    for block,spec in SPECS.items():
        rows={}
        for line in spec.splitlines():
            k,action,reason=line.split('|',2); k=int(k) if k.isdigit() else k
            assert k not in rows and reason.strip()
            text=None if action=='R' else 'D' if action=='D' else action.removeprefix('T:')
            assert action in ['R','D'] or action.startswith('T:')
            rows[k]=(text,reason)
        decisions[block]=rows
    return decisions

if __name__=='__main__':write(parse(),'all337_contextual_proposals_v1.json',__file__)
