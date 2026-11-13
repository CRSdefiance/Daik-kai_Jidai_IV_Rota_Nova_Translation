"""Complete the remaining exchanges against their sealed source-first drafts."""
from scripts.write_rafael557_contextual_slice_v2 import write_slice
DECISIONS={};OVERRIDES={}
def block(number,text):
    for line in text.strip().splitlines():
        index,decision,reason=line.split('|',2)
        ident=f'DK4_MES_B{number}_R{int(index):04d}'
        assert ident not in DECISIONS
        DECISIONS[ident]=('retention' if decision=='K' else 'revision',reason)
def wording(number,index,text):OVERRIDES[f'DK4_MES_B{number}_R{index:04d}']=text
def choice(number,offset,index,decision,reason,english=None):
    ident=f'SC0_B{number}_CHOICE_{offset}_{index}'
    DECISIONS[ident]=(decision,reason)
    if english:OVERRIDES[ident]=english

block(146,"""
6|K|The quiet full-name identity check suits Uddin's measured entrance; keep FU dynamic and leave its display-width proof pending.
10|K|The short reciprocal question is natural when addressed by an unknown visitor.
15|R|Restore Uddin's first-person introduction instead of This man, and use the bound Abraham Ibn Uddin spelling.
18|R|Restore Rafael's hesitant courtesy rather than a flat Hello.
23|R|Make the report of FO's growing reputation and extensive business idiomatic rather than Your business seems broad.
26|K|Rafael's modest denial naturally answers the compliment.
31|R|State the request to discuss something naturally instead of the awkward isolated request formula.
34|K|The private impression of quiet dignity explains why the following choices concern whether to accompany Uddin.
50|R|Make clear that Uddin is asking Rafael to travel a little way; the request itself does not make a journey.
53|K|The hesitant agreement and invitation to lead on naturally accept the journey.
58|R|Use the approved Guild role label and a natural invitation to meet at the Basra Guild.
62|R|Keep Rafael's confirmation of the meeting place and normalize the approved Guild label.
66|R|Correct the unnatural third-person This man waits to Uddin's intention to go ahead and wait.
69|R|Use a natural polite farewell instead of the abrupt Yes. Later.
73|R|Translate the farewell as a farewell, not an order to Go.
85|K|The refusal branch clearly explains that Rafael must consult the crew rather than decide alone as admiral.
90|R|Restore Uddin's first-person interest in Rafael's judgment and natural apology instead of an agentless passive.
""")
wording(146,15,"Forgive me. I should have introduced myself. I conduct a little business out of Basra. My name is Abraham Ibn Uddin.")
choice(146,404,0,'revision','The source expresses feeling unable to refuse, not finding no reason to refuse; keep the internal hesitation.')
choice(146,404,1,'revision','Uddin seems intimidating to Rafael; avoid asserting that he looks dangerous, and phrase the internal decision naturally.')

block(147,"""
7|K|The stammered admiration suits Rafael's reaction to the impressive reception.
12|R|Retain the natural apology and address as FO's leader; correct the unintended full-width F in Forgive and I in I, without claiming the ASCII name macros were broken.
15|R|Make Rafael's respectful self-correction natural without inventing a formal Commander rank for the company head.
19|R|Use a natural formal transition to the purpose of the meeting.
23|K|The hesitant assent preserves Rafael's nervousness.
28|R|Restore the explicit request to form an alliance; the current fragment can sound as though Uddin is asking Rafael to clarify someone else's proposal.
32|K|The short Pact echo expresses Rafael's uncertainty about the proposed agreement.
43|R|Make Uddin's acknowledgment of the abrupt, forward request natural first-person speech.
47|K|The measured acknowledgment of the seriousness of an alliance suits Uddin and allows Rafael time to decide.
53|R|Replace This man with Uddin's personal admission that he investigated what happened in Africa.
56|R|Restore first-person understanding and the deliberate request despite Rafael's concern, avoiding the unnatural passive and third-person self-reference.
62|K|The source-bound silent pause preserves Rafael's uncertainty; the ellipsis is deliberate punctuation.
67|K|The lack of demand for an immediate answer, time to think, and arranged lodging are clear in Uddin's measured formal speech.
70|K|Ibn Niyadi's concise guidance naturally directs the visitor without inventing an occupational label.
74|K|The quiet thanks naturally accepts the hospitality.
""")
wording(147,12,"Forgive me for startling you, FI... or perhaps I should call you FO's leader.")

block(148,"""
5|R|Use Uddin's natural question after giving Rafael a night to consider, rather than the abrupt Your decision.
9|K|Rafael's considered acknowledgment naturally leads into the alliance choice.
13|K|The measured invitation to hear the answer suits Uddin's formal manner.
17|K|Retain the source's deliberate pause before the player's choice.
33|K|The expression of trust and willingness to cooperate naturally accepts the alliance.
37|K|The surname address and courteous invitation to discuss business preserve Uddin's manner without inventing a military rank.
40|K|The nervous but clear agreement suits Rafael's response.
45|R|Restore Uddin's first-person arrangement and complete request to escort FA to the reception room, rather than clipped location fragments.
48|K|The concise acknowledgment naturally answers the escort instruction.
53|R|Restore power around India rather than a claim of ruling all Hindustan; the source explicitly supports Lord for Nagalpur here.
57|R|Use natural formal language for money worship and greedy business practices, rather than the calqued enslaved by gold.
62|K|The distinction between formidable company wealth and the owner's lack of character preserves Uddin's judgment.
66|R|Preserve the qualified expectation of defeating him in time rather than making an unqualified immediate assurance.
69|K|The brief assent naturally follows the proposal.
74|K|The transition accurately signals a condition that may concern Rafael.
77|K|Rafael's question correctly anticipates the issue of what happens after Nagalpur's defeat.
82|R|Keep the alliance ending and absence of a written contract; request a later nonaggression agreement without inventing the act of signing one.
85|R|Use nonaggression pact rather than truce: the companies are agreeing not to attack after the alliance, not ending an existing war.
90|R|Correct company base to Arabia rather than Uddin's birthplace, preserve limited shared markets, and avoid granting ownership of every other port.
93|K|Rafael's paraphrase accurately checks the restriction on Arabian markets without turning it into complete exclusion.
97|K|The reciprocal promise not to obstruct Rafael's company clearly states the other side of the arrangement.
121|K|The system notice accurately identifies the Muscat market share transferred by Uddin.
152|R|Use natural grammar for Uddin granting some of his Socotra market share to the player.
163|K|The confirmation and question naturally check for any remaining conditions.
167|R|Use a natural formal apology for taking up Rafael's time rather than Pardon the trouble.
170|R|Make the response to the apology idiomatic and preserve FO's modest size and commitment to help.
174|R|Restore the missing first-person perspective in Uddin's thanks and expectation.
177|R|Use Rafael's ordinary contraction in the enthusiastic call to defeat Nagalpur.
182|R|Replace the unnatural Together, onward with Uddin's complete formal call to join forces.
196|K|The brief confirmation naturally checks the alternate refusal choice.
200|K|The polite apology suits Rafael's refusal.
213|K|The reference to unhealed African wounds preserves Uddin's inference without asserting a new event.
216|K|Rafael's unfinished denial naturally challenges that inference.
224|R|Preserve Uddin's respect for the decision, but restore enemies rather than mere rivals and Indian Ocean rather than Hindustan's ocean.
228|R|Make Rafael's nervous request to go easy on them idiomatic and explicitly reciprocal in context.
232|K|The simple farewell naturally closes the refusal branch.
""")
choice(148,112,0,'revision','Use a spoken first-person acceptance that flows into Rafael\'s expression of trust, rather than an interface instruction.')
choice(148,112,1,'revision','Keep the source\'s courteous reluctance in Rafael\'s spoken refusal rather than an impersonal menu command.')

block(149,"""
5|R|Use the approved Evergreen Lotus Leaf name and the established Proof shorthand in a natural question about whether it is a map.
10|K|Claudio's compressed confidence in Uddin's information suits his informal voice.
13|R|Give Rafael a natural first-person question about what to combine with the leaf.
32|K|Janus's suggestion is natural and uses the approved Kushan Platter name.
40|K|Arcadius's separate alternative suggestion is natural and uses the same approved item name.
46|R|Restore Rafael's invitation to try the experiment and observation that nothing happens, rather than an order and a bare Nothing.
50|K|Claudio's direct question naturally marks the failed first attempt before the later water clue.
""")
wording(149,5,"I've been wondering... This Evergreen Lotus Leaf is a map to the Proof, right?")

block(151,"""
5|K|The urgent call and word from home naturally begin the crisis.
8|K|The short instruction to read the dispatch suits the urgent situation.
13|R|Preserve the dispatch's reported uncertainty and the specific fact that Spain's king is also officially King of Portugal.
17|K|Claudio's brief shocked reaction fits the news.
29|K|Janus's separate shocked reaction fits the alternate companion branch.
36|K|The interrupted reference to Portugal as their homeland naturally conveys Claudio's alarm.
46|R|Make clear that Portugal still exists in name, avoiding the confusing On paper, yes answer to whether their country is gone.
52|R|Apply the same clear nominal-existence distinction to Arcadius's separate explanatory line.
58|K|The question clearly asks whether Portuguese factions are now subordinate to Spain.
63|R|Preserve appears to have sided with Spain and identify the national fleet under Dinis de Albuquerque; do not present the incomplete report as settled fact.
66|K|The source-bound wordless exclamation conveys shock; retain the deliberate punctuation.
71|R|Restore Claudio's angry insult rather than the unnatural mild phrase That Albuquerque.
101|K|Janus's silent pause preserves the reaction without adding a comment.
108|K|Rafael's sympathy for Albuquerque's constrained choice naturally explains why he will not blame him.
113|R|Retain Claudio's natural protest and refusal; correct the unintended full-width I to ASCII I.
117|R|Restore Rafael's explicit first-person Portuguese identity, pride, and refusal to take the Spanish king's orders instead of the unnatural This heart declaration.
129|K|Arcadius's source-bound silence prepares the personal disclosure about Greece.
133|K|Claudio's concern naturally asks Arcadius why the news affected him.
137|R|Use natural homeland language for Greece's fall to the Ottomans and the personal understanding of Rafael's pain.
140|K|Claudio's silence leaves room for the emotional disclosure.
147|K|The brief question naturally expresses Rafael's uncertainty about what to do.
152|K|The time and supply costs of rushing home and the appeal to FI are clear and conversational.
155|R|Replace the awkward our strength can't beat Spain phrasing with a natural assessment that their forces cannot defeat Spain's reinforced fleet.
160|K|The need to preserve their hard-won progress in Asia clearly adds a second reason to stay.
171|K|Claudio's anger at surrendering FO's rights naturally supports the decision to retain their position.
176|K|Julio's familiar Aye and practical refusal to give away Asia suit his older voice.
183|K|The deliberate pause gives Rafael time to reach his decision.
188|R|Use a personal decisive announcement and preserve the dramatic hesitation before not going back; ordinary wrapping remains the formatter's task.
201|R|Restore Janus's startled question before addressing the admiral.
208|K|Claudio's challenge preserves the fear that staying might mean giving up, prompting Rafael's explanation.
212|K|The firm refusal to give up and plan to grow stronger in Asia before restoring Portugal are clear and naturally emphatic.
224|K|Arcadius's source-bound wordless exclamation preserves the response to Rafael's resolve.
239|K|Janus's separate surprised response fits the alternate branch.
246|K|Claudio's enthusiastic approval captures the encouragement without a literal gendered idiom.
256|R|Use natural excited language about a big ambition rather than the stilted getting grand.
261|R|Make Carlo's separate response a natural complete observation instead of This grows grand.
267|K|The direct challenge to Spain's fleet conveys Rafael's resolve without literally translating the idiom about washing one's neck.
293|R|Restore the specific Indochina governorship and correct the full-width I while preserving the qualified recollection and FI address.
297|K|The quiet countryman echo naturally considers the possibility of a Portuguese ally.
302|K|The suggestion of allying through shared nationality is clear and appropriately tentative.
306|R|Restore Rafael's promise to consider the suggestion rather than the vaguer Perhaps.
314|R|Restore the specific Indochina governor and correct the full-width I while keeping Julio's qualified recollection and FI address.
317|K|The repeated countryman echo is natural in this distinct alternate branch.
322|K|The Malacca location, possible shared feelings, and possibility of an alliance remain appropriately qualified.
325|K|The brief acknowledgment naturally receives Julio's advice.
330|K|Claudio's familiar old man address and question about Julio's Spanish nationality preserve the source's loyalty concern without implying kinship.
334|R|Retain Julio's warm my boy correction to admiral and personal loyalty; correct the unintended full-width I.
337|K|Rafael's quiet thanks naturally acknowledges Julio's loyalty.
""")
wording(151,113,"FI! Not you too! I won't accept this!")
wording(151,334,"Helping you matters far more to me than those details, FI, my boy... I mean, Admiral.")

block(152,"""
6|K|The opening warning is natural and sets Pereira's confrontational tone.
11|R|Restore the complete question Who are you, which Pereira explicitly echoes in his reply; Who alone could ask who gave the warning.
15|R|Make Pereira's sarcastic echo and trading challenge idiomatic without adding the current little whelp age insult.
18|R|Use the source's familiar Clau nickname as Rafael orders him to stand back.
22|K|The irritated sound naturally conveys Claudio's reaction.
26|K|The question correctly recognizes Rafael as the admiral.
30|R|Keep Rafael's firm but polite request that Pereira introduce himself first, rather than the abrupt Your name.
34|K|The clipped self-introduction is natural for Pereira's rough manner and uses the approved Duarte Pereira name.
38|R|Restore the source's identification as Portugal's governor of Indochina rather than only regional governor.
42|K|The astonished recognition of Admiral Pereira naturally follows the introduction.
47|K|The fame-precedes-me expression and question about his purpose naturally introduce the territorial demand.
50|R|Preserve the source's named Estado institution together with the explanatory trading sphere in Southeast Asia.
54|R|Remove the added age qualification young; Pereira is sarcastically praising Rafael's understanding before ordering him out.
57|K|The appeal to fair competition between Portuguese companies preserves Rafael's conciliatory approach.
62|K|Pereira's rhetorical dismissal of equal terms naturally answers the proposal of fair competition.
65|K|The blunt declaration of an unfair world suits Pereira's worldview.
68|K|Rafael's source-bound silence leaves space for Pereira's threat.
73|K|The drive-out-or-be-driven-out challenge and rough laugh preserve the zero-sum threat.
77|K|The taunt about Portugal's takeover correctly challenges Rafael's appeal to nationality.
81|K|The silent reaction preserves Rafael's discomfort about Portugal.
86|R|Frame exclusive control as Pereira's demand, not an established fact that Southeast Asia already belongs solely to his company.
90|K|The short monopoly question naturally checks the meaning of the demand.
95|K|The rough laugh and confirmation clearly affirm that demand.
98|K|The appeal not to fight while their homeland is lost preserves Rafael's urgency.
103|R|Restore Pereira's conflicted feelings and personal pride in Portugal rather than the calqued Proud Portugal fragment.
106|K|Rafael's proposed alliance and unfinished restoration appeal naturally follow Pereira's admission.
111|R|Restore the instruction to calm down and remove the added explanatory sentence about one king wearing two crowns from this line.
114|K|The interrupted protest preserves Rafael's unwillingness to accept the distinction.
119|R|Make Pereira's condescending understanding natural personal speech rather than Your meaning is clear.
123|K|The source-bound silence preserves Rafael's frustration.
128|R|Restore Pereira's position as Portuguese governor of Indochina and the resulting absolute authority of Spain's king, not merely an unexplained regional title.
131|R|Correct the stray Japanese glyph replacing the opening of So and express the risk of aiding dangerous dissidents naturally.
136|R|Clarify that people's livelihoods depend on Pereira and make his personal responsibility natural rather than the stiff They need my care.
140|R|Use established Antony Kuhn, restore Indonesia, and preserve the conditional offer to help against the Dutch opponent.
144|R|Use established Kuhn and make the political limit on aid natural and explicit.
147|K|The question correctly isolates the refusal to help fight Spain.
152|K|The brief answer naturally confirms Rafael's understanding.
156|K|Rafael's silence preserves the disappointment before Pereira's advice.
161|K|The apology for complaining and instruction to go east and grow stronger are clear and suit Pereira's rough voice.
164|K|The surprised echo naturally questions the direction east.
169|K|The promise to talk afterward and curt dismissal naturally end Pereira's exchange.
176|K|Claudio's reluctant acknowledgment that the older man has a point naturally follows the confrontation.
180|R|Keep Rafael's contemplative East echo instead of making it another direct question after Pereira has left.
185|K|The question to FI naturally asks what going east means in practice.
189|K|The deliberate pause leaves room for the companions' interpretation.
200|R|Keep the proposed East Asia Proof interpretation tentative and use the established Proof shorthand; it is the companions' inference, not an explicit demand Pereira made.
207|R|Apply the same appropriately qualified interpretation to Arcadius's distinct alternate occurrence.
214|K|Claudio's concern about the difficulty and unknown duration naturally challenges the inference.
217|R|Keep the need for at least a clue and the qualified fear that Pereira will not take them seriously, avoiding the current stronger may never acknowledge us.
221|K|Claudio's rough acknowledgment that they need Pereira as an ally fits the political constraint and move to action.
225|R|Use the source's familiar Clau nickname and Rafael's complete first-person encouragement before sailing for East Asia.
""")
wording(152,140,"Now, if you're taking on that Dutch bastard Antony Kuhn in Indonesia, there might be something I could do...")
wording(152,144,"That's world politics for you. As things stand, Kuhn is Spain's enemy, too. I can help you defeat him, but I can't support you in anything else.")

block(153,"""
5|K|The dirty-coin observation is natural and uses the approved Ancient Kingdom Coin name.
9|K|Claudio's casual proposal to polish it uses the approved Lotion Jar label without asserting what the liquid chemically is.
12|R|Make Rafael's decision to try the unknown liquid natural first-person speech; do not infer acid or milk from the item name.
17|R|Use a conventional repeated rubbing sound for the source action.
22|K|The warning to FI not to get carried away and the dissolving observation preserve Claudio's alarm.
26|K|The alarm turning into puzzlement fits Rafael's discovery.
30|R|Use a natural observation that another pattern is appearing, preserving the tentative map identification.
40|K|Claudio's explanation correctly ties the Southeast Asia map reveal to the surface dissolving.
46|K|Arcadius's distinct alternate explanation correctly states the same reveal with a more measured trailing pause.
53|R|Use the established Proof shorthand and the source's discovery of its location, not a newly invented kind of Proof.
57|K|Rafael's relief that the whole coin did not dissolve naturally closes the failed-polishing discovery.
""")

block(154,"""
5|K|Claudio's observation that Spain is ahead in these waters is natural and appropriately qualified.
8|K|Rafael's agreement and hope of catching up preserve his optimism.
13|R|Restore the key condition of obtaining the Proof first, which is necessary for Claudio's proposed reversal.
24|K|Rafael's duty to restore Portugal and refusal to yield the region preserve his motivation.
28|R|Replace the unnatural double-negative response about a dream meaning nothing with Claudio's grudging understanding and determination.
35|K|The barkeep's nationality observation and FO question naturally open the local account.
39|R|Use a hesitant acknowledgment rather than adding an adversative but where Rafael is simply confirming his identity.
44|K|The quiet warning, Maldonado territory, and question about his reputation flow naturally together.
60|R|Give Rafael a natural complete question about bad reports rather than the stilted Bad rumors fragment.
67|K|The alternate admission of barely knowing Maldonado naturally precedes the explanation of his reputation.
76|R|Apply the same natural reputation question to this distinct alternate occurrence.
84|R|Make the personal decision to trust FO natural first-person speech instead of the clipped Telling you opening.
88|K|Claudio's concern about the strength of the hatred naturally prompts the account of Maldonado's conduct.
91|R|Ask naturally why everyone hates him, retaining Rafael's polite request to explain.
95|K|The account of violent control backed by Spain's Crown preserves the source's political context.
99|R|Use indiscriminate attacks on passing merchant ships rather than asserting literally every merchant ship is attacked.
102|K|The pirate comparison naturally responds to the described raids.
107|R|Preserve the effect on sailors and the barkeep's own livelihood, using suffering business rather than the broader claim that all our trade is ruined.
111|R|Restore Claudio's question about trusting them so easily instead of making it unsolicited advice not to trust them.
114|R|Use the barkeep's personal knowledge and a qualified expectation that they would not mistreat residents, not an assertion of established behavior.
117|K|The source-bound pause gives Rafael time to consider the account before the choice.
140|K|Claudio's quiet FI address preserves the hesitation branch; the trailing ellipsis is deliberate punctuation.
144|K|The speculation about a wider New World problem remains tentative and does not assert unsupported events elsewhere.
148|R|Preserve that defeating Maldonado alone may not solve the whole problem, rather than the stronger claim that it may solve nothing.
152|K|The polite inability to help immediately fits the cautious branch without inventing a kinship from the source address.
157|K|The subdued reaction naturally expresses the barkeep's disappointment.
161|K|Claudio's acknowledgment of useful information and question to FI naturally soften the refusal.
164|R|Make Rafael's sympathetic understanding and hope of doing something soon natural without promising a firm intervention date.
169|K|The barkeep's hope that they differ from Maldonado's men preserves his wary trust.
185|R|Address the barkeep directly as you, preserving the source's recognition of his trust rather than speaking about him in the third person.
190|R|Restore the specific New World peace objective in Rafael's rally to the companions.
195|K|Claudio's rough assent naturally supports Rafael's decision to act.
199|K|The barkeep's hopeful anticipation fits the intervention branch without adding a guaranteed outcome.
""")
choice(154,1562,0,'retention','The direct promise to defeat Maldonado naturally commits to the intervention branch and matches Rafael\'s following rally.')
choice(154,1562,1,'revision','Use a hesitant internal question about what they should do, keeping the deliberative tone rather than the abrupt What now.')

block(155,"""
5|R|Preserve the sailor's hearsay about a newly arrived outfit, rather than turning the rumor into a settled report.
9|K|The qualified report of FO's strength naturally answers the rumor.
12|R|Replace unsupported noble Lord with source-established Governor Escante while preserving the question about his plan.
15|R|Use Governor Escante and retain the warning that very few of his own people know the plan.
19|R|Use Governor Escante and preserve the sailor's rough apologetic chuckle rather than an invented frightened stammer.
22|R|Use Governor Escante for the decision-maker without inventing nobility.
26|K|The possible alliance against Maldonado remains a strategic suggestion, not an accomplished arrangement.
29|R|Use Governor Escante and preserve the interrupted homeland-related secret without completing it as independence or inventing the rest of the plan.
32|K|The threat to stop talking preserves Juan Blanco's severity without adding a formal rank.
35|K|The nervous reaction and observation that no one willingly yields the region are natural in this rough exchange.
39|K|The skeptical expectation about how far FO will get preserves the uncertain outcome.
43|R|Restore the rough chuckle and agreement rather than a frightened Yes, sir with an added form of address.
47|K|Janus's hesitant question naturally confirms that Rafael overheard the conversation.
50|R|Keep Rafael's identification of Mexico's governor as a confirming question rather than an unqualified declaration.
54|K|Claudio's stank-of-trouble idiom naturally conveys his suspicion.
64|K|The mention of a plan preserves uncertainty about its details.
71|K|Julio's reminder that all factions seek expansion naturally checks the companions' suspicion.
74|K|Janus's concern about the repeated plan reference preserves the distinction from ordinary expansion.
85|K|Rafael's caution about making enemies and lack of a declaration of war preserve his reluctance to act on suspicion alone.
90|K|Claudio's blunt call to stop such men now naturally opposes Rafael's caution.
94|R|Replace the calqued regret comes too late with Claudio's natural warning not to wait until Escante controls the whole New World.
98|K|Rafael's concern about Spain gaining more power naturally acknowledges the argument without ending his hesitation.
102|K|Claudio's concise conclusion naturally treats Rafael's concern as agreement.
106|R|Restore natural first-person speech and ordinary American think about it instead of Will think on it.
112|K|The observation that they obstruct the enemy's New World ambitions preserves the reciprocal rivalry; do not substitute the draft's stronger new assertion about their own objective here.
117|K|Claudio's reciprocal inference that Escante is in their way naturally follows Rafael's observation.
120|R|Use Janus's natural complete judgment of Clau's harshness instead of an isolated harsh fragment.
132|K|Julio's restrained reflection on fate and necessary fighting suits his older voice in this alternate branch.
135|K|Rafael's hesitant acknowledgment of sometimes needing strength to defeat an enemy preserves his reluctance.
150|K|Claudio's equation of Escante with Maldonado and call to strike early preserve his blunt position.
154|K|Janus's reluctant conclusion that action seems necessary fits the final branch.
""")

block(156,"""
5|K|The question naturally asks about the relationship between the two opposing leaders without assuming friendship.
9|R|Clarify that both rule parts of the New World and keep Rafael's speculation about getting along tentative.
13|K|The hypothetical combined attack clearly motivates Claudio's concern.
17|R|Preserve Rafael's conditional deal-with-it-then response instead of the vaguer Then we'll face it.
22|K|The direct appeal to FI and warning of being crushed convey Claudio's urgency.
25|K|Janus's hush and direction to look over there naturally start the overheard conversation.
29|R|Keep Maldonado's guess about Escante's aim explicitly tentative and leave the conclusion unfinished.
32|K|The subordinate's certainty and warning not to trust Escante preserve the disagreement in this exchange.
35|R|Restore a natural first-person statement that they cannot afford to pick a fight now instead of a subjectless fragment.
39|K|The temporary cooperation, attacks on other factions, and personal territorial ambition remain clear in Maldonado's boast.
42|R|Leave the subordinate's assessment of their chances unfinished, as Maldonado cuts it off; do not complete it as a prediction of certain defeat.
45|R|Make the command not to finish the sentence explicit and retain Maldonado's angry language without awkward repeated name fragments.
49|R|Restore Janus's confirming question about Maldonado's identity rather than an unqualified statement.
53|R|Keep Rafael's inference about their poor relations qualified instead of asserting a definite friendship status.
57|R|Restore Janus's tentative suggestion of competing vested interests, not merely the generic label rivals.
61|K|The simple claim that each wants the whole New World accurately states Claudio's interpretation.
64|K|The concern about cooperation against other factions naturally brings the overheard threat back to their own situation.
68|K|Claudio's assertion that they will be the first target preserves his confident, anxious interpretation.
71|R|Make Rafael's uncertain question a response to Claudio rather than a vague unsupported Maybe.
76|K|Janus's explanation that an alliance with them as Portuguese offers no benefit preserves the political concern.
79|R|Restore the conditional necessity of fighting if attacked, rather than a terse unconditional-sounding slogan.
""")
wording(156,57,"Competing business interests, perhaps?")

block(157,"""
5|K|The question about the approved Ceremonial Knife naturally opens the item experiment.
9|R|Make Claudio's safety warning natural and preserve that even a small knife is dangerous, rather than the tautology a knife is a blade.
13|K|The fitting Sun-Crest Sheath uses the approved item name and naturally leads into putting the knife away.
18|R|Retain the startled reaction but avoid identifying the blade as the light source before the source does.
22|K|The short exclamation conveys the blinding brightness without adding a claim about lost sight.
29|K|Rafael's relief after the glare and question about the light naturally follow the flash.
33|R|State that the knife is on the ground, which is what Claudio observes; Rafael explains in the next line that he dropped it.
37|R|Restore Rafael's first-person explanation of dropping it when startled rather than the subjectless Dropped it in shock.
41|R|Restore the specific discovery of a map on the blade instead of the vague on it.
46|K|Claudio's excited identification remains a confident inference about the New World map, not a newly added mechanism.
49|R|Use Rafael's natural It looks like it, preserving both the Proof discovery and lingering puzzlement about the light.
""")

block(158,"""
5|R|Use the source's familiar Clau nickname in Rafael's ordinary question about local crops.
9|K|Claudio's brief question naturally asks why Rafael is interested.
13|R|Restore Rafael's hesitant wish to help Charlotte's village produce a new trade good, rather than an impersonal Maybe statement.
18|K|The thoughtful corn suggestion naturally answers the local-crop question.
21|R|Use a natural decision to try corn as a trade crop rather than the vague use that.
25|R|Retain Claudio's natural teasing implication about Rafael's interest in Charlotte, without inventing a relationship; correct full-width I to ASCII I.
29|R|Restore Rafael's flustered stammer and natural question about what Claudio means.
34|K|The chuckling dismissal and reminder to take her corn complete the teasing exchange naturally.
""")
wording(158,25,"Well... you're not as innocent as I thought, FI!")

block(159,"""
5|K|The personal request to talk naturally opens the private conversation with FI.
8|R|Make Rafael's response What is it natural and less abrupt while preserving his public Arcadius address.
13|K|The quiet observation that Rafael seems down naturally invites his denial.
17|K|The emphatic denial fits Rafael's embarrassed reluctance to discuss Charlotte.
21|R|Make the inference about Charlotte a natural personal question rather than the calqued Charlotte is why.
25|K|The source-bound wordless surprise preserves Rafael's reaction; the punctuation is deliberate.
30|K|The tentative question about caring for Charlotte fits the implied affection without declaring an established relationship.
34|R|Use natural first-person admission rather than the subjectless Can't hide, retaining Rafael's acknowledgment that Arcadius understands him.
38|K|The quiet FI address preserves the sympathetic pause; the ellipsis is intentional punctuation.
42|R|Restore Rafael's personal, emotional wish to do something for Charlotte rather than a subjectless Want fragment.
47|R|Retain the effective quote and two FI substitutions; correct the unintended full-width I without inventing a stronger romantic promise.
51|K|The surprised reaction naturally answers the report of Charlotte's feelings.
56|R|Restore Arcadius's personal decision to visit Charlotte instead of the unnatural Charlotte got a visit from me.
60|R|Retain the natural conditional explanation and FI address; correct the two unintended full-width I letters.
63|K|The deliberate silence allows Rafael to take in the disclosure.
68|K|The request to forgive Charlotte and explanation of her fear preserve her insecurity without inventing a social rank.
71|K|The brief why question naturally requests the reason for her insecurity.
76|K|Old, distinguished family faithfully conveys the source background without turning it into a claim of titled nobility; retain the FI address.
80|K|Rafael's emphatic dismissal of status differences naturally answers that explanation.
84|K|The gentle request to consider Charlotte's feelings suits Arcadius's sympathetic role.
88|R|Use Rafael's natural What do you mean instead of the abrupt isolated Meaning.
93|R|Preserve that her European mistreatment must have hurt her deeply, marking the speaker's sympathetic inference rather than asserting privileged knowledge.
96|K|The quiet acknowledgment naturally recalls Charlotte's earlier account without adding details to it.
101|R|Keep the speaker's qualified understanding of Charlotte's fear and use natural emotional phrasing rather than the stiff step forward.
104|K|The deliberate silence lets the explanation land before the message.
109|R|Make the transition to Charlotte's requested message conversational instead of the formal Enough preamble.
113|R|Restore Rafael's echo of the new message topic instead of a generic What.
118|R|Preserve the reported fact that Charlotte never learned to write and her lack of opportunity, avoiding the opaque That was her world.
122|R|Restore Rafael's first-person realization and regret rather than clipped, subjectless generalizations about someone who cannot write.
126|K|The opening of Charlotte's quoted thanks and assurance about her village is clear; keep its opening quote consistent with the closing quote in record 132.
129|R|Correct the full-width I and address FI naturally inside Charlotte's continuing message; preserve restoration of his homeland as a hope and condition.
132|R|Retain the conditional invitation and the matching closing quote; correct the full-width I without adding marriage, perpetual waiting, or a guaranteed reunion.
136|K|The emotional name call naturally responds to Charlotte's message.
141|R|Make Arcadius's considerate departure personal speech rather than the impersonal Time to go.
144|K|The deliberate pause leaves Rafael space to react privately.
149|K|The private Eirene address is source-supported and appropriately follows her earlier confidence; it does not globally rename Arcadius's public label.
154|K|The farewell and reminder that what happens with Charlotte is up to FI preserve encouragement without promising an outcome.
""")
wording(159,47,"FI... 'All I think about every day is FI,' she told me. You're on her mind, too.")
wording(159,60,"If you had no feelings for Charlotte, FI, I would have kept this to myself.")
wording(159,129,"I hope your homeland will be restored too, FI. When your country is back to how it was...")
wording(159,132,"If you still feel the same as you did then, please come visit me.' ...That's all of her message.")

block(160,"""
10|K|Janus's observation is natural and uses both approved Tang Bamboo Craft and Bamboo Assembly Plan names.
13|K|Rafael's question accurately checks whether the plan allows disassembly and reassembly.
17|K|The invitation to try it and initial sequence are natural in Janus's explanatory voice.
20|R|Use Rafael's startled stammer and natural description of the big bamboo piece rather than the stiff Something is drawn formulation.
25|K|Yifa's tentative placement question naturally conveys enjoyment of taking the craft apart.
28|R|Restore Rafael's observation that she is having fun and the approved Yifa address; do not retain the provisional Ihwa spelling.
33|K|Yifa's proud explanation naturally states that the approved Tang Bamboo Craft comes apart.
37|K|The surprised question preserves Rafael's initial fear that she broke it.
41|K|The denial and instruction to consult the approved Bamboo Assembly Plan are clear and natural.
44|K|Rafael's realization correctly explains the reversible disassembly shown by the approved plan.
48|K|Yifa's enthusiastic remark and completion of disassembly fit her playful voice.
51|R|Replace the misleading Nice hands compliment with unexpected manual dexterity and a natural observation about the drawing on the back of the bamboo.
65|K|Janus's tentative identification of East Asia's Proof map remains an inference, not an invented definite artifact claim.
69|R|Make Rafael's excited agreement and immediate plan to search natural rather than Yes, surely.
75|K|Yifa's excited recognition of a Proof map naturally follows the discovered drawing.
79|R|Restore the explicit credit to Yifa and use the established Proof shorthand in the call to search East Asia.
""")
wording(160,28,"Looks like you're having fun, Yifa.")
wording(160,79,"Wonderful! Nice work, Yifa! All right, let's find the Proof in East Asia!")

if __name__=='__main__':
    write_slice('translations/rafael_B146_B149_B151_B160_contextual_review_v1.json',DECISIONS,OVERRIDES,__file__,348)
