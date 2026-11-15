"""Individual contextual revisions and justified retentions after sealed clean-first drafting."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/Maria_B286_B302_clean_20261110')
PARTS=[r'''@286
5|R|The simple welcome naturally opens Verisa's exchange; extra excitement is unnecessary.
9|T|Restore the natural question,reported East Asian location and celadon material while matching the installed Goryeo Incense Burner identity.|FI, have you heard of the Goryeo Incense Burner, the celadon one? They say it's somewhere in East Asia.
13|D|Correct the woman's third-person self-reference and restore her wistful first-person wish and stronger divination accuracy.
29|R|Hmm is a natural understated acknowledgment from source actor0; an added question is unnecessary.
34|D|Make the remembered warning a conversational change of subject rather than a bare list marker.
38|D|Restore reported pirate activity and advice to equip properly,not merely keep equipment ready.
42|D|Restore the surprised reaction and personal caution in Rafael's source-controlled reply.
46|R|See you is a natural friendly farewell and needs no added enthusiasm.
@287
4|D|Remove the unsupported only-you claim and restore an ordinary request to accept a job.
8|D|Give Maria a complete natural question matching her curious tone rather than an abrupt isolated What.
12|D|Restore recent appearances by a band of raiders rather than a timeless summary.
16|D|Restore concern about danger;the source does not emphasize surprise about this location.
20|D|Keep gold andivory,andrestore both organized training andthe guildmaster's conversational explanation.
23|D|Restore land-combat inexperience,the separate weapons/armor shortage andthe guards' difficulty.
26|D|Make the purchase request and European availability natural,retaining five cargo holds without inventing five suits.
29|D|Keep the Mediterranean/North Sea inference andpossible delay with natural articles andMaria's voice.
32|D|Preserve willingness to wait,life-and-death stakes andthe plea not to forget in conversational speech.
36|D|Restore Maria's explicit promise to remember alongside the repeated five-hold quantity.
39|R|Please do naturally reinforces Maria's immediately preceding promise not to forget.
@288
6|R|The direct thank-you fits the armor handover without adding a new emotional beat.
10|D|Make the expansion ofthe guard causal andconversational;use Guns consistently with the installed commodity instead of narrowing to muskets.
14|D|Retain five holds anddeferred combined payment while restoring the apologetic request andregistered Guns identity.
18|D|Restore Maria's acknowledgment ofthe new goods category before agreeing.
@289
5|R|Back already is a natural surprised greeting that carries the source's quick-return observation.
9|D|Restore the apparent arms-race inference andwhat the bandits noticed,rather than asserting their actions as certain.
12|R|Now we need cannons as well naturally follows the escalation andretains the exact requirement.
15|D|Retain two holds,urgency andcombined deferred payment in an actual request rather than instructions plus a payment label.
19|D|Restore the at-once complaint that makes Maria's frustration at repeated trips specific.
23|R|Sorry.Please bear with us is a natural apologetic appeal for patience in this civic request.
26|R|Two holds is a natural resigned confirmation;the immediately preceding cannon request makes the goods unambiguous.
@290
5|R|The complete sentence preserves satisfaction andthe tentative deterrence claim through should.
9|D|Restore the closing thanks andcasual apology while preserving both reimbursement andreward.
14|R|The standard receipt is complete andpreserves77000 exactly.
36|D|Restore natural market-share wording andmatch the verified Sao Jorge place name.
47|T|Retain the direct natural question butrestore the transition into a new topic after payment.|By the way, where is the bandits' hideout?
50|R|The startled What anddirect motive question naturally convey the guildmaster's reaction without requiring a typographic stammer.
53|R|What do you think is a natural coy reply in this exchange andbetter than replacing it with a literal self-question.
57|D|Restore the teasing appraisal,reported Sahara-ruins hideout andcaution against recklessness without inventing guaranteed danger.''']

PARTS.append(r'''@291
S24_0|D|Restore the polite speaker's qualified may-get-lost warning instead of a certain outcome.
S24_36|R|The terse missing-map warning andcertain consequence form a natural firm exchange without needing the address repeated.
S24_68|R|The short direct warning naturally conveys this casual speaker's concern andpreserves the missing-map cause.
S24_104|D|Restore this speaker's personal assessment through I think rather than flattening it to certainty.
S24_140|R|The blunt two-sentence warning works for the rougher voice without adding profanity.
S24_176|D|Replace the slogan-like no-map-means construction with an older speaker's natural conditional warning.
S24_214|R|The childlike direct request to get a map matches the distinct source request rather than predicting lost travel.
S24_240|D|Restore the older formal cadence andaddress rather than reuse a generic short warning.
S348_0|R|Then let us depart is deliberate polite formality appropriate to this voice.
S348_22|R|Shall we go is an idiomatic complete departure proposal.
S348_40|R|Let's go is a natural energetic call andneeds no extra wording.
S348_56|R|Then let's head out naturally expresses this conversational departure.
S348_80|R|Let's get going is a lively rough departure call with the source's enthusiasm.
S348_100|R|Come,let us go retains the older speaker's spirited formal exhortation.
S348_124|R|Onward we go is a playful departure cry that works for the childlike enthusiasm without inventing transport.
S520_0|D|Replace the wooden Mist is here with a natural observation of fog arriving.
S520_20|D|Replace stiff Mist has come with the formal speaker's conversational observation.
S520_40|D|Restore fog's arrival without adding heaviness absent from this variant.
S520_56|R|Now we're in fog naturally expresses the unwelcome change in conditions.
S520_76|D|Give the impressed rough voice a natural That's some construction while preserving thick fog.
S520_96|D|Replace a generic stiff notice with the older voice's conversational acknowledgment.
S520_114|D|Make the child's amazement sound spoken rather than a formal Such-heavy-fog fragment.
C674_0|R|Keep going is a clear natural caption preserving the advance choice.
C674_1|D|Complete the grammatical wait-for-clearing choice instead of Wait for clear.
103|D|Restore Maria's tentative try-moving-ahead decision while preserving for now.
S758_0|R|Looks like a dead end is a natural cautious observation;the omitted dummy subject is normal speech.
S758_26|R|The restrained fragment andellipsis preserve disappointed recognition.
S758_42|D|Use the disappointed Aw rather than a neutral Oh for this casual complaint.
S758_66|R|A dead end with an ellipsis is a natural conversational reaction needing no expansion.
S758_82|R|A dead end,it seems preserves both uncertainty andthe older cadence.
S758_108|D|Restore the child's disappointed exclamation rather than reuse a neutral reaction.
S758_132|R|Well,a dead end naturally conveys this older speaker's wry recognition.
C938_0|D|Make pushing on despite the dead end explicit,distinguishing this choice fromthe earlier fog-advance menu.
C938_1|D|Use a natural detour-search caption rather than the stiff Seek a path.
143|R|Push through the trees as a question is a natural compact musing about whether they can force a way through.
S1018_0|D|Restore the polite speaker's personal offer to try the requested action.
S1018_14|R|Let's try it is a natural proposal andalready matches the independent draft.
S1018_32|D|Keep the complaint followed by the speaker's own reluctant agreement in natural casual speech.
S1018_72|D|Restore this speaker's personal willingness to give it a try rather than a generic group command.
S1018_86|D|Restore the rough speaker's all-the-way resolve rather than a generic onward call.
S1018_112|D|Replace Reckless words with an actual response to the unreasonable request andretain willingness to try.
S1018_152|D|Keep the protest andenthusiastic personal action;All right,go changes it into an instruction to others.
173|R|The standard fatigue notice is complete andpreserves the source's apparent condition.
178|R|Let's find another way is an idiomatic proposal to seek a detour,not a guarantee of success.
S1332_0|D|Describe the found fork without inventing an explicit two-path count.
S1332_30|D|Retain the branching-path report without imposing a number of paths.
S1332_58|D|Restore the closer-look discovery through a natural Look andfork report without an exact count.
S1332_94|R|The excited path-over-here fragment is natural andcomplete in this immediate discovery.
S1332_122|R|The direct exclamation works for the rough excited voice andpreserves the path's direction.
S1332_150|D|Restore the older speaker's assessment that this way appears passable rather than certain traversability.
S1332_182|R|Admiral,over here is a natural childlike beckoning call with no unnecessary added description.
S1332_210|R|A path,right here naturally conveys surprised discovery in this location.
213|R|The danger assessment andwait-for-clearing proposal already form natural coherent dialogue.
S1664_0|R|That seems best is a natural qualified agreement in the immediate choice context.
S1664_28|R|Good idea is a natural casual agreement with waiting.
S1664_42|R|Good idea also works for this conversational voice;different wording is unnecessary merely for variation.
S1664_56|R|The two short affirmative sentences naturally accept the plan.
S1664_78|R|We have little choice is an idiomatic older acknowledgment that waiting is the remaining course.
S1664_104|R|Yes,let's do that is natural simple agreement for this voice.
S1664_126|D|Keep the source's safety judgment without asserting an unqualified superlative.
242|D|Use an English ellipsis for the first separate silent waiting panel;retain the original source punctuation in evidence.
246|D|Use a longer English ellipsis for the second separate waiting panel,preserving the progression rather than deleting the pause.
253|R|The standard one-day notice is complete andaccurate.
257|D|Restore Maria's observation that the fog seems to have cleared andher renewed encouragement.
S1960_0|D|Replace telegram-like Now in view with natural spoken discovery.
S1960_18|R|There it is naturally signals the unnamed destination coming into sight.
S1960_32|R|The same brief discovery also suits the more emphatic voice without inventing a destination name.
S1960_46|T|Preserve questioning recognition ofthe unnamed destination in natural concise English.|Is that it?''')

PARTS.append(r'''@292
S24_0|D|Restore danger fromwandering without knowing the way,rather than reduce it to a missing-map status message.
S24_52|D|Preserve this speaker's protest against aimless jungle travel instead of declaring a particular map mechanically indispensable.
S24_106|D|Restore aimless wandering through this jungle andthe conversational warning.
S24_156|D|Restore the rough speaker's actual refusal,which the old general risk warning loses.
S24_214|T|Restore aimless wandering andnatural older formality without adding a map to this variant.|Admiral, it's dangerous to wander aimlessly through a jungle like this.
S24_266|D|Make the child's warning explicitly connect walking through this jungle with having no map,as this source variant does.
S24_326|D|Restore the formal older warning about wandering without direction andkeep the admiral address.
S446_0|R|Shall we go is natural conversational departure speech.
S446_16|R|Then let us go preserves the deliberate polite formality andmatches the independent draft.
S446_36|D|Make the enthusiastic call idiomatic American speech while retaining energetic movement.
S446_62|R|Then let's go is a natural friendly departure proposal.
S446_84|R|Let's go is a natural blunt departure call andneeds no extra filler.
S446_100|D|Give the older speaker a natural spoken departure instead of a stilted onward fragment.
62|R|This humidity is brutal naturally conveys Maria's reaction to the climate anddifficulty of crossing.
S666_0|R|A cave,here is natural astonished speech in this discovery;the fragment is intentional wonder.
S666_24|R|Huh?A cave naturally expresses this childlike surprise without unnecessary expansion.
89|D|Restore pitch-black intensity,which explains the next feel-or-light choice.
93|D|Replace the gendered Sir with the actual admiral address andhesitant ellipsis;the source does not call Maria male.
C770_0|D|Use the idiomatic feel-our-way expression rather than Go by touch.
C770_1|D|State the source's act ofmaking a fire/light rather than an ambiguous Use light instruction.
108|D|Restore Maria's complete personal observation andtentative proposal instead of telegram-like omitted subjects.
112|R|Hm?What's this is natural tactile surprise after the explicit feeling-in-darkness choice;the context supplies the touch.
115|D|Preserve the interrupted alarm about the crew without adding a male crewman,exact casualty count orcompleted attack outcome.
126|D|Restore Indian python specifically while keeping Samwell's uncertain afterthought.
132|D|Restore Maria's judgment that this is the wrong opponent andher order for everyone to retreat,without reducing it to a strength stat.
139|T|Retain the current generic singular sailor reference butrestore the source's apparent-injury uncertainty.|A sailor seems to have been injured.
145|R|The direct question naturally asks where the party emerged;aspect changes add no useful meaning.
S1150_0|R|Hard to say followed by seem naturally preserves uncertainty about being near the ruins.
S1150_46|R|Seems we're near the ruins is a natural cautious location report.
S1150_76|R|The hesitant maybe-near-ruins question naturally conveys this uncertain conversational voice.
S1150_142|D|Replace the awkward Ruins seem near with the speaker's uncertain assessment ofthe party's location.
S1150_180|R|Whoa andthe confirming question naturally preserve surprised rough recognition.
S1150_230|D|Restore the older speaker's initial disorientation,emergence andqualified location judgment rather than certainty.
S1150_286|D|Correct apparent arrival at actual ruins to being near them,andretain the child's uncertainty anddelight.
S1150_370|R|The complete cautious sentence andHmm already suit the formal older speaker.
174|D|Preserve making a light without inventing a specific torch absent fromthe source.
178|R|The clipped bats-now reaction andone-thing-after-another complaint naturally convey Maria's irritation.
S1688_0|R|Too many is a natural urgent exclamation in the visible bat encounter.
S1688_18|R|Way too many naturally preserves the casual speaker's intensified alarm.
S1688_38|R|The scream and enormous-swarm exclamation naturally convey alarm at an extraordinary number without an exact count.
S1688_82|R|The blunt Too many suits the rough voice's immediate alarm.
S1688_100|R|The full inability-to-advance sentence naturally preserves the bat obstruction.
S1688_170|R|The scream andDisgusting are natural childlike revulsion;do not rewrite solely for variety.
203|T|Retain the good qualified harmlessness judgment,butmake ignoring the bats andadvancing one coherent instruction.|They seem harmless. Ignore them and keep moving.
213|R|The standard fatigue notice is complete andpreserves uncertainty.
S2054_0|R|The two excited fragments naturally celebrate escaping the jungle in this immediate context.
S2054_44|R|Out of the jungle is a natural complete celebratory exclamation.
S2054_66|R|The casual We did it andescape cry preserve the relief without unnecessary added address.
S2054_102|R|Thank goodness.We're out naturally retains this speaker's distinctive relief.
S2054_132|R|The rough excited short cheers fit the successful escape andsource enthusiasm.
S2054_168|R|The older speaker can naturally share the same direct celebratory words;distinct wording is not required for its own sake.
S2054_202|R|The complete addressed celebration is natural andalready retains the admiral andjungle details.
S2332_0|D|Restore the polite speaker's qualified assessment ofhaving reached the ruins.
S2332_28|R|The ruins,Admiral naturally identifies the site with casual excitement.
S2332_50|R|There they are naturally identifies the already discussed ruins without adding distance oranother location.
S2332_70|R|Here are the ruins preserves this variant's confident identification;the draft's hedge is unnecessary.
S2332_92|D|Restore the older speaker's seems-to-have-arrived uncertainty.
S2332_120|R|The childlike admiral-addressed discovery naturally identifies the ruins;an added question is unnecessary.
S2332_142|D|Restore the formal older speaker's announcement ofreaching the destination after the difficult passage.''')

PARTS.append(r'''@293
11|R|Bring me the map first naturally conveys obtaining it andreturning to the waiting guide;it does not imply he sells it.
S96_0|D|Restore this variant's explicit disbelief about an ancient city here.
S96_56|R|The quiet ancient-city fragment andellipsis naturally convey wonder at this place.
S96_92|R|The simple discovery statement naturally acknowledges the ancient city in context.
S96_128|R|The ellipsis lets the conversational observation carry its quiet amazement without extra explanation.
S96_166|R|The same concise wondering remark works for the rougher voice without adding unrelated slang.
S96_208|R|Hard to believe is a natural spoken omission ofthe dummy subject andpreserves the older speaker's disbelief.
S96_266|D|Replace wooden stood even here with a natural childlike realization about a former town.
S96_310|D|Restore the older formal speaker's wondering To think cadence rather than a repeated generic report.
43|D|Restore the guide's correction andqualified inference fromthe map about a different island.
47|R|What is the complete natural surprised reaction andmatches the draft.
53|R|We must cross the sea clearly preserves the necessity in this formal guide's voice.
58|R|Back to port,then is a natural practical proposal in response to crossing the water.
62|D|Restore the prepared small boat andguide's intended means ofcontinuing,not just an unspecified ready boat.
65|R|The formal qualification andsecrecy sentences are natural andpreserve the party-versus-sailors distinction.
74|R|The standard one-day passage is complete andaccurate.
78|R|The guide's arrival announcement andoverland instruction already form natural coherent speech.
81|R|The excited discovery is idiomatic andexactly matches the independent draft.
S914_0|R|Admiral,the ruins is a natural immediate discovery call whose context supplies that they have found them.
S914_28|R|The same brief discovery fits this casual excited variant without requiring different words.
S914_54|R|The ruins is a natural pointing exclamation identifying the site ahead.
S914_74|D|Restore the rough speaker's apparent-discovery hedge instead of a certain finding.
S914_104|D|Restore the older speaker's seems judgment about the ruins.
S914_134|R|Admiral,those are the ruins naturally conveys the child's recognition;an added confirmation question is unnecessary.
S914_166|D|Restore the formal older speaker's cautious appears-to-have-found assessment.
110|D|Restore Maria's apparent arrival andI'm-coming response;Going in invents an entry action.
@294
4|R|Welcome is a natural warm opening in this host exchange without needing extra punctuation.
8|R|The complete question clearly preserves the village's far-northern New World location.
12|D|Restore the customer's hearsay,respected monk,the northern continent andthe religious mission in natural speech.
16|D|Restore reported disappearance andthe host's own wondering,rather than assert the fate orimply Maria knows it.
20|D|Correct Maybe to a natural I-don't-know response to the question about the monk's fate.
24|D|Restore apparent virtue andthe present hope that the people cherish him;past-tense wording prematurely suggests a settled fate.
27|D|Preserve the conditional opportunity to travel north rather than assume a planned trip.''')

PARTS.append(r'''@295
4|T|Retain the natural respectful Ms.FA address without inventing kinship;correct the mismatched full-width I while preserving the FA substitution.|Ms. FA, you're the only person I can ask to do this.
8|R|The complete concern andgrave expression fit Maria's serious response;contractions are not obligatory.
11|D|Preserve recent repeated attacks andthe coherent single unidentified-ship referent carried into the ghost-ship rumor.
15|R|Pirates is a complete natural questioning reaction andmatches the draft.
19|D|Restore the reply that this identity is the mystery andexpress the survival condition in natural speech.
22|D|Restore both patrols andhunting fleets andtheir repeated failure;keep elusiveness without making supernatural behavior evidence.
26|R|Quite skilled is a natural understated assessment ofthe unknown attacker.
30|D|Make the rough guildmaster's transition into gossip conversational rather than stiff Yet there is.
34|D|Ask naturally about the newly introduced rumor,rather than imply a choice among previously listed rumors.
38|R|Some say clearly marks the ghost-ship identity as a reported claim rather than an established fact.
41|D|Make Maria's skeptical incredulity clear in a natural confirming question.
45|D|Restore reluctant belief arising fromfailure to find a trace;Nothing else explains it is an unsupported positive conclusion andthe old request transition is wooden.
48|D|Restore a personal request to discover the attacker's identity instead of an abrupt Learn instruction.
52|R|Only investigate is a natural compact clarification ofthe job's scope.
56|D|Restore personal gratitude for defeating it without narrowing the source's defeat to a required destruction method.
59|R|Very well is a natural composed acceptance in Maria's voice.
63|D|Restore apology for an eerie job andentrusting it to her,rather than a generic good-luck sendoff.
@296
4|R|The astonished echo question,praise andreward offer naturally convey impressed thanks for the completed ghost-ship quest.
9|R|The standard receipt preserves65000 coins exactly.
31|D|Express the small Havana market-share increase as a complete natural system notice.
44|D|Restore the guildmaster's own confidence andwish to introduce someone,not an unstated third party's wish to meet her.
47|D|Replace the full-width question mark with a natural ASCII questioning reaction.
51|R|Hello is a natural short greeting;an added pause is not needed to establish the newcomer's restrained manner.
55|D|Restore Maria's identity question;And you assumes an introduction exchange absent here.
59|D|Restore the request's urgency andconfidence in her ability,without turning the ruins into a newly specified lost shrine.
63|R|Ruins is a natural surprised questioning echo.
67|D|Restore hearsay about the ancestors honoring warriors without inventing the specific building type shrine.
70|R|The legendary greatest-warrior restriction is complete andnatural;the following line explains its moral qualification.
74|D|Use the English ellipsis for the silent reaction without changing the separate source call.
78|D|Keep conviction as the speaker's belief arising fromher victory,not objective proof supplied by the ship itself.
82|R|The complete sentence naturally preserves strength,a just heart andwisdom without inventing a formal title.
86|D|Correct Maria's third-person this-woman self-reference andrestore her appreciation mixed with doubt about helping.
90|D|Restore the undertaking's vagueness instead of asserting a measured near-total lack ofknowledge.
93|D|Restore their indiscriminate requests to strong-looking people andthe candid comparison to this present request.
97|D|Make the awkward apology andpermission to fail sound like spoken politeness instead of a failure-bears-no-shame maxim.
100|D|Restore Maria's teasing letdown so the guide's next flustered correction has its source motive.
104|D|Give the guide a natural flustered self-correction,explicit wish for success andconditional reassurance.
107|R|The laugh,teasing clarification andbest-effort promise naturally resolve the misunderstanding.
110|R|Really is a natural brief relieved response;the source's stammer need not always be spelled out.
114|D|Express the partial advance andnonrepayment condition as the guide's natural personal offer.
117|R|The standard receipt preserves the separate5000-coin advance exactly.
123|T|Correct the guide's third-person this-man self-reference andretain the prerequisite,notification andcompanionship using the installed Ancient City Map title.|First, we'll need the Ancient City Map. Let me know when you have it, and I'll join you in the search.
126|D|Correct this-man self-reference to the guide's own promise to wait at this town's gate.''')

PARTS.append(r'''@297
4|D|Restore Maria's acknowledgment ofkeeping the traveler waiting alongside arrival at Guam andbeing able to go home.
7|R|Xiexie is a natural untoned romanization ofthe source's unfamiliar thanks;it preserves Maria's following noncomprehension without a gratuitous spelling change.
11|R|What is a natural brief request to clarify the unfamiliar utterance in this exchange.
15|D|Restore recognition ofthe object as a thank-you gift andgrammatical polite acceptance,rather than the dangling Gladly.
19|R|The repeated Xiexie preserves the source's two thanks andthe same romanization as the earlier line.
23|R|The well-wishing andsailing caution naturally cover the next sea journey without needing an added itinerary.
@298
4|D|Correct the reversed discovery:the alarmed guardian has been found;he is not announcing that the party found an object.
8|D|Give Maria a natural concerned question rather than an exasperated What now.
12|D|Restore the guardian's hesitant suspicion andthe established capitalized Proofs convention.
15|R|Yes is a complete direct confirmation andmatches the draft.
19|D|Restore the guardian's vow to resist even at the cost ofhis life,rather than only an archaic refusal.
22|R|The calming request andpromise not to take it by force naturally preserve Maria's ethical position.
25|D|Restore the direct connection between reassuring words andprevious conquerors taking everything;keep the source's anger without naming an unstated nation.
29|D|Correct third-person this-woman self-reference andattribute the comparison to the guardian's perception,not Maria endorsing herself as a conqueror.
33|D|Use the English ellipsis for the guardian's separate silent response.
37|D|Make Maria's decision to stop pursuing the object natural spoken action rather than a flat present-tense report.
41|D|Preserve FI andthe New World qualification,with natural alarm andthe registered Proof convention.
45|R|We cannot force them is a natural firm refusal in the already explicit handover context.
49|D|Restore other conquerors learning ofthe object,the possible seizure andthe conditional consequence for the party's efforts.
52|D|Use the English ellipsis for Maria's unresolved silent consideration,keeping the source call.
56|D|Correct guaranteed death to the source's broader harm:the people would not escape unharmed.
59|D|Express the guardian's startled accusation as a natural direct question.
62|D|Restore Maria's personal denial andhesitation;do not claim her reply clears Xien's warning ofits coercive implication.
65|D|Keep Escante's threat being gone distinct fromhis personal fate,andrestore Xien's doubt rather than certain knowledge ofSpain's future.
68|R|The surprised question about Escante is natural andmatches the independent draft.
78|R|The destruction alternative is complete,natural andexact;do not merge it with the submission branch.
84|D|Retain the separate submission alternative andMaria's own commitment to prevent abuses in the New World,not an objective guarantee ofno future violence.
91|R|The astonished echo naturally recognizes the woman admiral fromthe East without adding a title ornew biography.
94|R|The rhetorical question naturally conveys Xien's surprise that the reputation reached this place.
97|D|Restore entrusting rather than an ordinary gift andthe friend's account to this guardian,without inventing the friend's identity.
100|R|The trust declaration andhopeful May prayer naturally resolve the conflict through voluntary trust rather than force.
107|D|Restore Maria's full-effort commitment instead of weakening it to a generic promise to try.
@299
4|R|The older speaker's unfamiliar-face observation andorigin question are natural;the draft's plural faces is unnecessary.
7|R|China is the exact complete answer.
11|R|The older marveling cadence andso-far remark naturally convey amazement at the journey without inventing geography.
15|D|Restore the guessed useful instrument as something heard about,with natural older curiosity andthe source's sextant identity.
19|R|What is the exact natural surprised response.
23|R|The rumor-qualified description naturally preserves position-finding on a sea without landmarks;do not historically correct the game's sextant.
27|D|Keep the barter as a personal offer ofsomething good rather than a quest-label reward-awaits announcement.
30|D|Make Maria naturally echo something good fromthe revised offer rather than shift the unnamed object into a reward category.
34|R|Bring it and see naturally keeps the exchange item a teasing surprise without naming it.
@300
5|R|The arrival question andexchange offer are natural andkeep the received object unnamed.
13|D|Correct the reversed transaction direction:the player hands over the installed Sextant,not receives it.
@301
5|R|The formal confirmation question fits the solemn offer without naming an object absent fromthe source.
9|R|At last andthe awaited day naturally convey the long wait without inventing a duration.
12|R|The deliberate formal trust andpolite offer fit this exchange andpreserve voluntary acceptance.''')

PARTS.append(r'''@302
4|R|The surprised question naturally confirms that the party knows ofthe monk.
8|R|You do is a natural concise follow-up asking whether the villager knows him.
12|R|The complete account preserves devoted nursing,the villagers' plague description andthe village's survival without an invented diagnosis.
15|T|Retain the good older cadence andmiracle appraisal while expressing the illness subsiding rather than adding an absolute cure claim.|His medicine eased the sickness almost at once. A true miracle.
19|R|Perhaps he knew medicine is a natural musing about knowledge,not a claim offormal medical training.
23|D|Restore mineral poison in drinking water andthe villager's uncertain recollection,instead of a confident generic claim about alchemy removing poison.
27|R|The short pointing introduction naturally identifies the monk as the book's author.
38|R|The unfinished Could this be naturally preserves surprised recognition under the original Lil control.
57|T|Correct Charles's book to the book Charles mentioned,avoiding invented authorship orownership;retain the shared celebration andoriginal Lil control.|This is the book Charles mentioned! We finally found it!
64|T|Use the installed Alchemy Book title andnatural stammered scholarly excitement without changing Charles's source control.|The Alchemy Book?! I-I never thought I'd find it here!
68|R|The named question naturally asks why Charles is so excited;extra exclamation marks are unnecessary.
72|D|Restore newly discovered experimental material rather than narrow it to a chemical reagent;preserve rumor andthe New World journey.
75|T|Retain research andthe unresolved qualification,with the exact installed book title andnatural first-person speech.|My research showed I'd need the Alchemy Book to obtain that material, but...
79|D|Restore the precious-metal clue andCharles's confidence,then express muttering as natural self-talk instead of reading the stage direction aloud.
82|T|Make Maria naturally postpone the rest ofCharles's explanation,rather than promise an unrelated later conversation.|Tell me the rest later.
89|R|The complete question naturally returns the exchange to the monk's whereabouts.
93|D|Use the English ellipsis for the villager's heavy pause before revealing the death.
97|D|Replace the full-width question mark with the crew role's natural ASCII questioning reaction.
101|R|The complete sentence naturally attributes his same illness to the village water without inventing a toxin ortransmission route.
104|R|Yet,his hidden illness andevery dose given to villagers preserve the source's full self-sacrifice.
108|T|Avoid At last sounding like welcome relief;retain the source's euphemistic death,intense grief andreligious tribute.|And in the end... he passed away! He truly was a messenger of God...
111|D|Use the English ellipsis for the captain's separate silent response to the loss.
115|R|The polite entrusting question naturally speaks for the villagers andpreserves the book's transfer ofresponsibility.
118|D|Restore the captain's echo ofentrusting,not a different question about why this recipient was selected.
122|R|The complete sentence naturally preserves the book's secret ofan unseen ore without naming a metal.
125|R|The older speaker's buried-ore phrasing preserves belief that deposits exist somewhere,without an invented location.
128|R|The continuation-of-work request andfind-the-ore question naturally express the desired search without guaranteeing success.
132|R|All right.Let's do it is a natural firm acceptance closing the grief-to-renewed-purpose exchange.''')

def main():
    output=ROOT/'authored_contextual_v1.json';textpath=ROOT/'authored_contextual_v1.txt'
    assert not output.exists() and not textpath.exists();rows=[];block=None
    text='\n'.join(PARTS)
    for line in text.splitlines():
        if not line:continue
        if line.startswith('@'):block=int(line[1:]);continue
        code,*entry=line.split('|');assert entry[0] in ['R','D','T']
        assert len(entry)==(3 if entry[0]=='T' else 2)
        if code.startswith('S'):ident=f'SC3_B{block}_STYLE_'+code[1:]
        elif code.startswith('C'):ident=f'SC3_B{block}_CHOICE_'+code[1:]
        else:ident=f'DK4_MES_B{block}_R{int(code):04d}'
        rows.append([ident,*entry])
    drafts=load(ROOT/'all315_independent_drafts_v1.json')
    assert [r[0] for r in rows]==[r['id'] for r in drafts['records']] and len(rows)==315
    textpath.write_text(text+'\n',encoding='utf-8',newline='\n')
    save(output,dict(blocks=list(range(286,303)),records=rows,complete_source_current_exchanges_read=True,
        all_five_gates_still_pending=True,new_credit=0,individual_names_review_andfresh_display_pending=True,
        exact_current_names_roles_andterms_bound_not_global_UI_orfont_approval=True))
    print('Authored315 individual contextual comparisons;allgates remain pending.')

if __name__=='__main__':main()
