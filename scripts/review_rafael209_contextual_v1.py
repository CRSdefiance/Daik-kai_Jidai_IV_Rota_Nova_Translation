"""Individual whole-exchange comparisons after the sealed clean-source drafts."""
from scripts.write_rafael557_contextual_slice_v1 import write_slice

DECISIONS={}
OVERRIDES={}
def block(number,text):
    for line in text.strip().splitlines():
        index,decision,reason=line.split('|',2)
        ident=f'DK4_MES_B{number}_R{int(index):04d}'
        assert ident not in DECISIONS
        DECISIONS[ident]=('retention' if decision=='K' else 'revision',reason)
def wording(number,index,text):OVERRIDES[f'DK4_MES_B{number}_R{index:04d}']=text

block(141,"""
6|K|The rough admiration suits Claudio's reaction to the ship without adding a technical claim.
18|R|Preserve the new type of ship, rather than merely a newly built ship; keep the startled stammer.
24|K|The brief exclamation naturally follows the identification of the ship.
29|K|Julio's recognition of Hayreddin's parting gift is clear in the exchange.
33|K|Rafael's hesitant question prompts the companions' explanation naturally.
38|K|The qualified suspicion correctly proposes a different target from Spain, not an additional target.
49|K|The disbelief answers Julio's unsettling inference without inventing its conclusion.
56|K|The surprised reaction fits the escalating realization.
61|R|Restore Claudio's shared inference and questioning confirmation instead of a flat statement of Hayreddin's intentions.
65|K|The interrupted protest preserves Rafael's reluctance without turning it into a command.
69|R|Restore the reported plan to absorb the Algiers pirates into the military; the current version misleadingly suggests annexing Algiers itself.
73|K|The independent pirate king's refusal to serve another remains clear and appropriately grave.
77|R|Opposing the Ottoman Empire is the source's constraint; avoid implying Hayreddin has already accepted Ottoman rule.
80|K|The speculative recognition of Rafael's potential remains tentative and personal.
84|K|Claudio's rough encouragement and direct question naturally draw Rafael into the decision.
87|K|The hesitant assent preserves Rafael's emotional progression.
100|K|The short self-directed inspection remark fits the move to examining the ship.
107|R|Localize the excited correction from admiral to company leader as boss, avoiding an invented formal military promotion.
110|K|The resigned opening turning into a rally fits Rafael's response to the crew.
114|K|The crew's enthusiastic answer completes the rally naturally.
""")
wording(141,107,"Admiral! I mean, boss! Let's do it, FI! Let's defeat Pasha's forces!")

block(142,"""
5|R|Use the bound item name Red Dye and preserve its role as the key to deciphering a map, before the experiment succeeds.
9|K|The natural suggestion connects the dye to the approved Old Parchment from the ruins.
13|R|Use Rafael's conversational enthusiasm rather than stiff formal phrasing as he agrees to try coloring it.
18|K|The short surprised exclamation fits the experiment's sudden result.
22|K|The excited confirmation accurately reports the newly appeared map.
26|R|Use the established Proof shorthand and idiomatic map to the Proof in the North Sea.
""")
wording(142,5,"This Red Dye is the key to deciphering the map to the Proof...")

block(143,"""
5|R|Remove unsupported noble Lord; use Albuquerque's source-supported admiral title and the guard's respectful greeting.
8|K|The polite thanks naturally answers the guard's invitation.
21|K|The quiet observation conveys Arcadius's impression of the palace.
28|R|Give Claudio a conversational reaction to the intimidating surroundings while retaining that they have done nothing wrong.
40|K|Julio's practical advice suits his experienced, reassuring role in the exchange.
55|R|Restore Cristina's curious recognition of the royal palace rather than a bare location statement.
63|K|The welcoming address and uncertain recollection of Rafael's surname fit Albuquerque's introduction.
67|R|Retain the natural formal introduction and dynamic full-name substitution; replace the unintended full-width I with ASCII I.
71|K|Claudio's impressed aside responds naturally to Rafael's polished introduction.
82|R|Make Arcadius's discreet request to let the principals speak natural while keeping the formal manner.
89|K|The dismissal of ceremony and thanks explain why Rafael need not keep addressing Albuquerque ceremoniously.
93|R|Restore Rafael's courteous inquiry instead of the abrupt and unnatural Your purpose.
98|K|The question about Portugal's commercial code clearly introduces the official explanation.
102|K|The concise admission of limited knowledge suits Rafael's honesty.
106|R|Replace the calqued welcome for honesty with natural formal reassurance and the promise of a simple explanation.
110|K|The courteous invitation to explain is natural in this formal conversation.
115|R|Preserve national prosperity and inhumane commercial practices without imposing the narrower modern legal label crimes against humanity.
118|K|The short question naturally requests the examples given immediately afterward.
123|R|State the trade in slaves and drugs and the military intelligence discovery, without narrowing the source military to the navy.
126|K|Portugal's declining honor and the transition to Albuquerque's plan are clear in the current formal speech.
129|R|Unpack the commission into natural sentences while preserving promising navigators, trading territory, and taking Espinosa into custody.
133|K|Rafael's uncertain question expresses the scale of the task without changing it.
137|R|Remove the invented self-description as an old man and make the reassurance about support natural before summoning Silveira.
140|R|Use a natural acknowledgment and courteous invitation to enter rather than a clipped command to the arriving merchant.
144|R|Restore Fernan Silveira's explicit spoken full-name introduction.
149|K|The brief acknowledgment accepts the merchant's arrival before his formal greeting.
153|R|Translate the interrupted health greeting naturally instead of an unfinished English blessing.
157|K|The interruption of formalities and introduction of FI FA as promising flow naturally together.
160|R|Retain Rafael's nervous introduction and both name substitutions; replace the two unintended full-width I letters with ASCII I.
165|K|The surname introductions and statement that they will work together remain clear after Fernan's full-name introduction.
168|K|The straightforward question naturally prompts clarification of the arrangement.
173|R|Correct no small contribution: Fernan is boasting, not describing modest gifts; restore first-person speech and avoid an invented donation.
177|K|Albuquerque's dry acknowledgment of the scale of Fernan's business preserves the restrained response to the boast.
181|K|The fawning thanks leads naturally into Albuquerque's interruption.
185|K|The curt dismissal preserves Albuquerque's impatience with flattery.
189|R|Restore fellow Portuguese and circumstantial evidence, which explain this particular constraint on military action.
192|K|The possessive my Africa preserves Fernan's boast and motivates Albuquerque's following aside.
196|K|The private echo and irritated move onward preserve the comic reaction to Fernan's possessiveness.
200|K|The direct request for objections fits the formal commission.
204|K|No correctly answers the English question about objections, preserving the Japanese assent in context.
209|R|Retain the natural invitation and laugh; correct San Jorge to the bound place name Sao Jorge.
233|R|Retain the clear market-share notification; correct the place name to Sao Jorge.
244|K|The official order clearly introduces the king's campaign funds.
247|R|Use the natural acknowledgment Yes, sir to answer the order.
251|K|The surname call identifies the first recipient of the funds.
255|K|The deferential thanks suits Fernan's formal behavior here.
258|K|The system notification identifies Silveira as recipient without inventing an amount.
263|K|The surname call identifies Rafael as the next recipient.
267|K|The hesitant thanks retains Rafael's modest response to the grant.
274|R|Make the player recipient explicit and preserve the King of Portugal, the campaign purpose, and the exact 50,000 amount.
278|K|The reported intelligence remains qualified and the instruction to prepare the fleet is clear.
282|R|Restore a natural personal expectation of full cooperation instead of the wooden passive Much is expected.
285|K|The concise acknowledgment answers Albuquerque's instruction.
290|K|Fernan's deferential acceptance suits his formal register.
294|K|The brief dismissal naturally ends the official audience.
299|K|The conversational question smoothly opens Fernan's naval-combat lesson.
302|K|The modest elliptical answer is natural in response to the question about skill.
307|R|Use natural appreciation of honesty and remove again, since Fernan was absent for Albuquerque's earlier exchange.
311|K|Retain the source's deliberate wordless pause as Rafael's embarrassed silence; this is punctuation, not untranslated prose.
316|K|The concise reassurance naturally prepares Rafael to accept instruction.
319|K|The uncertain acknowledgment preserves Rafael's hesitation.
324|K|The formal explanation of Albuquerque's request establishes Fernan as the appointed instructor.
328|K|The hesitant echo naturally expresses Rafael's surprise at being taught.
332|K|The enemy-power question clearly introduces the strategic lesson about defeating Espinosa.
336|K|The naive investment proposal is clear and sets up the necessary correction.
340|K|The partial approval followed by the limit on investment accurately motivates both choice responses.
354|R|Remove unsupported Lord and ask naturally about the player's prior attempt to reduce Albuquerque's Lisbon market share.
358|K|The short admission directly answers Fernan's question about investment.
363|K|The prerequisite of being at war before using investment to drive out the rival is clearly stated.
367|R|Make Rafael's deduction that war must be declared explicit rather than an isolated infinitive.
372|R|Correct the tutorial actor: the player's First Mate writes the declaration at the Guild; it is not a guild employee. Preserve attacking the fleet as the alternative.
375|K|The informal acknowledgment suits Rafael's growing understanding.
380|R|Clarify whose reputation and market share fall, and that affected cities are near the naval battle.
383|R|Use the natural secure a contract with a city and preserve the need to act immediately before investing.
387|R|Make Rafael's internal realization about gaining a contract in a fully monopolized city idiomatic without changing the mechanic.
392|K|The investment-only limit on dissolving Espinosa's company is clear and prompts the next question.
395|K|The concise request for clarification naturally leads into the headquarters exception.
400|R|Clarify that investment cannot completely expel the enemy from its home base, rather than implying no market-share reduction there is possible.
403|R|Preserve trading first to accumulate fleet and investment funds; avoid requiring the player to build ships rather than prepare a proper fleet.
406|K|The respectful admiral-and-surname thanks is natural American address and clearly closes the lesson.
412|K|The alternate knowledgeable-player branch conveys approval and the possibility that the lesson was unnecessary.
416|K|Rafael's awkward apology naturally answers Fernan's comment in the alternate branch.
424|K|The reassuring dismissal and call to defeat Espinosa together resolve the awkwardness warmly.
427|R|Replace the unnatural answer Likewise to an invitation to cooperate with a clear courteous acceptance, retaining the approved surname address.
""")
wording(143,5,"You are Admiral FA of FO, I take it. Admiral Albuquerque is expecting you. Please go inside.")
wording(143,55,"Hmm. So this is the royal palace...")
wording(143,67,"I'm FU. You sent for me, sir?")
wording(143,115,"Private trading companies now do business abroad, contributing to our nation's prosperity. Some, however, engage in inhumane practices.")
wording(143,137,"Ha ha ha! I'm not asking you to do it without support. I'm not that unreasonable. ...Bring in Mr. Silveira!")
wording(143,140,"Yes, sir! ...Mr. Silveira, please come in.")
wording(143,144,"Fernan Silveira, reporting.")
wording(143,160,"It's... nice to meet you... I'm FI FA.")
wording(143,209,"My base is Sao Jorge. Visit whenever you like. Ha ha ha!")
wording(143,233,"Silveira shared his Sao Jorge market share with you.")
wording(143,354,"Were you able to reduce Admiral Albuquerque's market share in Lisbon just by investing?")
wording(143,372,"Correct. There are two ways: attack their fleet at sea, or go to the Guild and have your First Mate write a declaration of war.")
wording(143,427,"I look forward to working with you, Admiral Silveira.")
DECISIONS['SC0_B143_CHOICE_3804_0']=('retention','Why not naturally asks why investment alone is insufficient at this exact branch point; the question follows record 340, not the earlier general strategy question.')
DECISIONS['SC0_B143_CHOICE_3804_1']=('revision','Make prior knowledge explicit so this option clearly skips the detailed lesson rather than merely acknowledging Fernan\'s statement.')
OVERRIDES['SC0_B143_CHOICE_3804_1']='I already know.'

block(144,"""
5|K|The deliberate puzzled pause starts the tablet examination naturally.
10|K|The question expresses Claudio's concern and prompts Rafael's explanation.
14|K|The familiar Clau address and uncertain question preserve the companions' relationship and the puzzle premise.
19|K|Claudio's obvious-to-him answer naturally sets up Rafael's difficulty reading the map.
28|R|Use both approved tablet names and frame the problem as Rafael's inability to interpret them, not proof that the artifacts contain no location information.
35|R|Use the approved tablet names and preserve Janus's personal difficulty interpreting them in this alternate companion line.
48|R|Replace the unnatural separate-halves maxim with Claudio's direct, colloquial observation about looking at them separately.
54|R|Make Arcadius's tentative suggestion idiomatic while preserving the gentler voice of this alternate speaker.
60|R|Use natural enthusiasm and practical placement language instead of stiff Let us align them.
65|K|The short question naturally checks where the second tablet belongs.
69|R|Use a conversational conditional as Rafael arranges the tablets.
80|K|The excited recognition turning into surprise fits the sudden change in the tablets.
86|K|Janus's alternate observation accurately describes the tablets joining.
92|K|The brief delighted exclamation suits Claudio's reaction.
96|K|The statement clearly reports that the two tablets have fused into one.
106|R|Use Claudio's contractions and preserve the apparent new mark without the awkward Some mark appeared.
112|K|Janus's alternate observation appropriately remains uncertain about the new symbol.
119|K|The brief surprised question naturally answers the discovery.
130|R|Use the established Proof shorthand and natural wording for the mark pointing to Africa's Proof.
137|R|Retain the tentative discovery while using the established Proof shorthand and a natural location question.
144|R|Restore the excited stammer in the reaction to the discovery.
154|R|Give Claudio a natural excited departure line rather than the formal Then we leave at once.
160|K|Janus's enthusiastic invitation addresses both companions and naturally follows the discovery.
166|R|Replace the grandiose onward with Rafael's straightforward agreement to go.
""")
wording(144,28,"I've looked at both the Upper Stone Tablet and the Lower Stone Tablet, but I still can't tell where the Proof is.")
wording(144,35,"The Upper Stone Tablet and the Lower Stone Tablet... But I can't make out where the Proof is from these.")

block(145,"""
6|K|The familiar greeting naturally opens Claudio's invitation.
10|K|The brief acknowledgment and question fit Rafael's everyday voice.
15|R|Use Claudio's conversational contractions and a natural reminder to invite Julio, avoiding the awkward old Julio address.
19|K|The reference to Julio's anger last time explains the reminder without inventing a relationship.
23|K|The affectionate complaint about the old man's memory fits Claudio's familiar banter.
27|K|The suggestion to invite Arcadius naturally expands the plan.
30|K|The surprised name echo prompts Claudio's explanation.
35|R|Keep the complaint about not joining their outings instead of the broader invented claim that Arcadius never socializes; use natural just-us-guys banter.
39|K|Rafael's concern about respecting Arcadius's solitude establishes his sympathetic response.
43|R|Restore Claudio's ironic claim that he is considering Arcadius's feelings and use colloquial language for fetching him at the inn.
47|K|The emphatic complaint about pushiness naturally answers Claudio's insistence.
52|R|Use the conventional English knock, knock for the source's two-knock sound.
56|K|The interrupted name preserves Claudio's sudden shock.
62|R|Render the flustered shout naturally rather than turning it into a literal interrogation.
66|K|The hesitant identity check fits what the companions have just seen.
70|K|The startled cry suits the interruption without adding visual detail.
74|K|The clipped question naturally checks that both companions witnessed it.
78|K|The hesitant answer preserves Rafael's shock.
83|R|Translate the alarm as having seen something private that they were not meant to see, rather than implying physical danger.
87|K|The repeated hesitant assent maintains their shared awkwardness.
93|K|Retain the source's deliberate wordless exclamation; full-width punctuation here conveys a reaction, not an unintended English letter or untranslated prose.
97|K|Hans's startled call addresses the two companions naturally.
101|R|Use a natural greeting to Hans instead of the unnatural epithet old Hans; do not invent a family relationship.
105|K|The hesitant question preserves Hans's fear that the secret has been seen.
109|K|The evasive hesitation suits Rafael's embarrassment.
114|K|Claudio's vague admission is appropriately awkward in this exchange and needs no invented wordplay.
118|R|Make the invitation into the room a gentle request consistent with the speaker's manner.
122|K|Hans's interrupted Eirene and correction to Arcadius preserve the private-name slip; the ASCII interruption mark is deliberate.
125|R|Remove No more hiding, which can imply the public disguise is ending even though the following exchange asks them to keep the secret.
131|K|The hesitant agreement fits Claudio's discomfort about entering.
135|K|The brief polite assent fits Rafael's response.
140|K|Retain Hans's source-bound wordless, uneasy pause as deliberate punctuation.
144|K|The quiet acknowledgment that they saw her naturally opens the explanation.
148|R|Keep Rafael's unfinished first-person denial instead of completing the denial as not me.
153|R|Restore a natural unfinished first-person denial for Claudio instead of the subjectless Saw nothing.
157|R|Restore the explicit disclosure that she is a woman and distinguish her assumed public name Arcadius from her private name Eirene.
161|R|Use first-person speech for Hans instead of a literal old man self-reference, preserving his regret about not guarding the door today.
165|R|Make Eirene's apology and reluctance to call Dr. Hans every time natural first-person speech.
168|K|The direct question about dressing as a man naturally prompts the explanation.
173|K|The tactless aside preserves Claudio's source characterization and motivates the later comment on his manners without adding a description of her body.
177|R|Restore Eirene's first-person decision made when she chose to sail with Hans; leave the following safety rationale with Hans.
180|K|Hans's worry about rough sailors is presented as a precaution, not as an allegation about this crew.
184|K|The contrast with their own crew naturally rebuts Hans's general concern.
188|K|The assurance of kindness followed by the odd-characters joke suits Rafael's gentle humor.
193|K|Hans's acknowledgment naturally concedes that his worry about this crew was unnecessary.
196|K|The specific thanks and mild tease about Claudio preserve Eirene's warmth and the exchange's comic turn.
199|K|Claudio's indignant reaction naturally answers the tease.
203|R|Correct the missing first-person subject and make Claudio's comic self-question idiomatic.
207|R|Use Rafael's gentle mediation and a natural follow-up question about resuming women's clothing.
212|R|Replace the unnatural third-person This one is a woman with Eirene's embarrassed first-person question about admitting it after so long.
215|R|Correct the grammar and make the embarrassment about admitting distrust clear in Hans's own voice.
219|K|The direct request for secrecy clearly preserves the continuing private status of Eirene's identity.
222|K|The idiomatic promise of discretion naturally answers her request.
226|K|Claudio's hesitant agreement preserves his lingering embarrassment.
229|K|The quiet thanks naturally closes the private exchange.
""")
wording(145,35,"Yeah. He hardly ever comes along. We'll drag him out if we have to and have a real talk, just us guys.")
wording(145,101,"Oh, Hans.")
wording(145,161,"I usually keep watch at the door. Of all the days...")
wording(145,203,"...Am I really that bad?")

block(150,"""
5|K|The innkeeper recognizes the approved Kushan Platter and naturally invites the player to hear its traditional story.
8|K|The concise question expresses interest and prompts the explanation.
13|R|Preserve the reported tradition and the practical step of filling the platter with water before floating flowers or leaves for divination.
17|R|Keep Rafael's hopeful wish and personal experiment, use the approved Evergreen Lotus Leaf name, and make floating it on water explicit.
35|R|Describe the leaf absorbing water and a pattern appearing in its veins in natural English rather than saying it drank water.
44|R|Apply the same natural absorption-and-pattern wording to this distinct alternate occurrence without conflating its source reference.
51|R|Correct southern sea to the source's Indian Ocean and use natural map-to-the-Proof wording.
69|K|The excited acknowledgment addresses Rafael naturally in this companion branch.
77|K|The same excited acknowledgment is natural in this separate alternate occurrence.
83|R|Thank the innkeeper directly and politely rather than referring to her as her while addressing her.
106|R|Preserve Hans's qualification that the maps seem divided into two and the initial need to find both keys.
110|K|The hesitant echo naturally questions the new concept of map keys.
115|R|Make clear that the correct two keys must both be obtained and combined properly before the map appears.
118|K|The inference from seven Proofs to fourteen keys is clear and arithmetically faithful.
123|K|The brief confirmation naturally answers Rafael's calculation.
127|K|The emphatic number and daunted reaction suit Claudio without altering the required total.
130|K|Hans's chuckle and bookish conditional fit his older scholarly voice and explain why the search remains unfinished.
134|R|Replace the calqued generalization about the world with Claudio's natural, rueful response about the difficulty of the task.
""")
wording(150,17,"If only it could tell us where the Proof is... Let's try floating the Evergreen Lotus Leaf on the water.")

if __name__=='__main__':
    write_slice('translations/rafael_B141_B145_B150_contextual_review_v1.json',DECISIONS,OVERRIDES,__file__,209)
