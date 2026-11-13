"""Full79-speech Hamburg recruitment exchange and both choices: prose review only."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Hamburg_prose_v1950')
SOURCE=Path('work/analysis/lil_Hamburg_source_v1949/all79_source_native_context_and_two_choices.json')
DOC=Path('translations/lil_hamburg_recruitment_editorial_manuscript_v1.json')
CHOICES=Path('translations/lil_hamburg_recruitment_choices_editorial_draft_v1.json')

# Keyed by the exact clean-source record index; reviewed in the full exchange.
# R preserves existing wording, normalizing only storage whitespace/punctuation.
LINES={
5:('V',"Shipping's booming here, too. We might find some capable officers.",'Lil notes that shipping thrives in this town too and suggests capable officers may be present.','Restore the shipping industry,too andpossibility. 航海士 arethe named officers distinguished fromhired水夫 sailors inB24,not aninvented naval commission.'),
22:('V',"Let's look for a cook instead. {MACRO:FI}'s cooking is awf...",'Emilio would rather find a cook and begins calling Lil\'s cooking bad before being cut off.','Use natural eager speech andanunfinished criticism that prompts her retort. Preserve FI;do not invent astrike orlet him finish the insult.'),
26:('R',"Be grateful you get food at all!",'Lil tells Emilio to be grateful merely to have something to eat.','Retain the complete natural indignant response. Its context connects directly tohis unfinished food complaint.'),
37:('V',"An officer, huh... Oh, I know!",'Camille considers looking for an officer and has an idea.','Keep the reflective-to-excited progression andthe established officer/sailor distinction.'),
41:('V',"There's someone here I really look up to. He helped me out for a bit. Should we ask him to join us?",'Camille says someone he respects lives here,helped him briefly in the past,and might be invited aboard.','Restore personal admiration,the brief prior help andthe invitation. Do not invent a father,formal teacher,permanent mentorship orother relationship.'),
44:('R',"What sort of man is he?",'Lil asks what kind of person Camille means.','Retain the existing natural inquiry. The surrounding exchange identifies the person asa man;no added biography isneeded.'),
48:('V',"I'll tell you when we meet him. I hope he's doing well!",'Camille postpones explaining until they meet and hopes the man is well.','Restore the explicit promise totell her later;the oldYou can judge changed the immediate speech act. Keep the warm anticipation.'),
51:('R',"Think this is the place...",'Camille tentatively recalls the location.','Retain the idiomatic conversational fragment anduncertainty;the unfinished phrasing suits recalling the house.'),
56:('V',"...Who is it?",'Gerhard asks who is there after a pause.','Use the natural question inthis arrival/doorway context,not anisolated Who. Preserve the brief pause aspunctuation,not authored layout.'),
60:('V',"Admiral Ardelknatts! It's been so long!",'Camille enthusiastically greets Admiral Ardelknatts after a long time apart.','Use the approved native Ardelknatts spelling. Admiral isexplicit in提督;do not invent Lord orGrandAdmiral.'),
63:('R',"Ah! You are...",'Gerhard recognizes the visitor vaguely but cannot recall his name.','Retain the unfinished recognition. The following introduction andmemory apology complete its meaning without inventing additional words.'),
66:('V',"I'm Camille Overijssel! You helped me out for a little while, sir!",'Camille introduces himself by name and recalls the brief help he received.','Preserve the source two-part name without adding the catalog middle name. Restore the brief extent ofthe help andnormalize the legacyfull-width I.'),
69:('V',"Ah, yes... Perhaps it's my age, but I'm getting quite forgetful. Forgive me.",'Gerhard recalls Camille,suggests age may explain his forgetfulness,and apologizes.','Keep the tentative age explanation rather than assert a proven cause. His formal butwarm greeting precedes the later confrontation.'),
73:('R',"Not at all! Glad to see you looking well!",'Camille rejects the need for an apology and is glad Gerhard appears well.','Retain the natural polite enthusiasm andordinary subject elision. This isCamille\'s deferential greeting,not a newmedical claim.'),
76:('V',"You've grown into a fine man. And who is this? Your wife?",'Gerhard praises Camille\'s maturity and asks whether the woman with him is his wife.','Preserve the mistaken marriage question asa question,not anactual relationship. Restore agrammatical complete question inhis measured voice.'),
79:('R',"What?! No! What are you saying, old man?!",'Lil denies being Camille\'s wife and rudely challenges the older man.','Retain the natural shocked denial andrude address. おじさん establishes no literaluncle relationship.'),
83:('R',"!",'Gerhard reacts with a brief startled exclamation.','Preserve the source punctuation-only reaction without inventing speech. Normalize the legacyfull-width exclamation toEnglishASCII.'),
87:('V',"Don't talk to the admiral like that! A-admiral, I'm so sorry!",'Camille reprimands Lil and nervously apologizes to the admiral.','Restore his flustered stammer andthe two immediate addresses. His respect isalready explicit;no newrank orrelationship isadded.'),
91:('V',"This is {MACRO:FI} {MACRO:FA}. I'm sailing aboard her ship now.",'Camille introduces Lil by her first and last names and says he now sails on her ship.','Preserve both genuine FI/FA macros,the possessive ship andcurrent affiliation. Use acomplete natural first-person sentence.'),
94:('V',"You work for a woman like this? How lamentable.",'Gerhard disapproves of Camille working under a woman such as Lil.','Preserve the condescending gendered wording andformal rare wordlamentable,which Fernando echoes andLil challenges. Do not erase his initial prejudice orassert Lil\'s age.'),
106:('V',"Couldn't agree more. 'Lamentable' is right.",'Fernando agrees with Gerhard\'s judgment and echoes the word lamentable.','Give Fernando a casual dry echo ofthe formal word. The shared wordmust survive becauseit drives Lil\'s next response andGerhard\'s vocabulary insult.'),
120:('R',"Really? Life here is fun.",'Emilio disagrees because he enjoys being with them.','Retain the simple optimistic counterpoint toFernando. The opinion remains Emilio\'s,not anobjective claim about every crew member.'),
126:('R',"Lamentable?! What do you mean by that?",'Lil angrily challenges the word Gerhard used.','Retain the existing natural reaction andthe lexical link tothe two preceding lamentable lines. The next vocabulary jab supplies the joke.'),
129:('V',"Precisely what I said. You have no manners toward your elders, and a meager vocabulary besides.",'Gerhard says he meant the literal word and criticizes Lil\'s manners toward her elders and her vocabulary.','Keep both insults andhis deliberately formal diction. Elders fits this encounter;superior could imply anunproved command relationship.'),
133:('V',"To think Camille would be content serving the likes of you. How far he's fallen.",'Gerhard says Camille has fallen by being content to serve someone like Lil.','Restore his explicit judgment andapprovedCamille. It setsup her defense ofCamille rather than adefense ofher own manners.'),
136:('R',"!",'Lil reacts sharply to the insult to Camille.','Retain the punctuation-only offended beat. Normalize the full-width glyph without inventing a spoken line.'),
140:('V',"Hold on! You're saying some pretty rude things yourself!",'Lil objects that Gerhard himself is saying harsh things.','Keep the reciprocal accusation ofrudeness after his manners lecture,not merely ageneric complaint.'),
144:('V',"I'm merely stating the facts.",'Gerhard insists he has only stated facts.','Use a complete natural sentence inhis formal voice. This ishis claim,not narrator endorsement.'),
148:('R',"Say whatever you like about me! But my lack of manners has nothing to do with Camille!",'Lil says Gerhard may criticize her,but her bad manners have nothing to do with Camille.','Retain the complete natural defense andits explicit distinction. She accepts responsibility forher own manners without accepting his judgment ofher friend.'),
151:('R',"...",'Gerhard pauses silently after Lil\'s defense.','Retain the silent beat;do not supply thoughts orsoften his response with invented dialogue. Normalize the ellipsis forEnglish storage.'),
155:('V',"Camille hasn't fallen at all! That's just slander!",'Lil denies that Camille has fallen and calls the accusation mere slander.','Preserve the direct callback toGerhard\'s fallen judgment andher defense ofCamille. Avoid implying he has fallen merelyless than Gerhard claims.'),
159:('R',"Hmm...",'Gerhard considers her response.','Retain the brief thoughtful reaction. Its position begins his reassessment rather than outright agreement yet.'),
163:('R',"{MACRO:FI}...",'Camille responds emotionally by saying Lil\'s name.','Retain the genuine FI macro andthe unfinished response. Do not invent a romantic orfamilial interpretation.'),
167:('V',"That was uncalled for. You're right.",'Gerhard admits his words were wrong and that Lil is right.','Make the apology natural andclear while retaining its limited subject:his unfair words aboutCamille. Do not turn itinto instant friendship withLil.'),
170:('R',"!?",'Lil reacts with surprise to the apology.','Retain the surprised punctuation beat without inventing speech;normalize the two full-width punctuation glyphs.'),
174:('V',"(He apologized... I wasn't expecting that.)",'Lil privately thinks the apology is a little unexpected.','Preserve the parenthetical internal thought andmild surprise. Do not replace itwith a declaration that shelikes ortrusts him.'),
177:('R',"Admiral... we came hoping to ask for your help.",'Camille explains that they came hoping to enlist Gerhard\'s cooperation.','Retain the natural deferential request. The next explanation concerns inviting himaboard,not inventing a separate mission.'),
181:('R',"...",'Gerhard waits silently.','Retain the pause asanindependent conversational beat;do not invent assent before the later conditional offer.'),
185:('V',"{MACRO:FI}, this is Admiral Gerhard Ardelknatts.",'Camille introduces Gerhard Ardelknatts to Lil as an admiral.','Use the approved full native name andretain FI. Admiral isexplicit;Lord andformalGrandAdmiral are not introduced.'),
188:('V',"He's a great naval admiral. He used to lead the strongest private fleet of pirate hunters.",'Camille praises him as a great naval admiral who formerly led the strongest private fleet specializing in pirate hunting.','Restore naval admiral,strongest,private fleet andits specialization. Past command doesnot establish retirement orloss ofrank;great isCamille\'s praise,not aformalGrandAdmiral title.'),
191:('V',"There was a time when every pirate from the North Sea to the Mediterranean lay low. That was his fleet's doing.",'Camille says every pirate from the North Sea to the Mediterranean once lay low because of Gerhard\'s fleet.','Preserve both named seas,the extent andthe causal attribution. 鳴りをひそめた meanslay low,not physically vanish orbe annihilated.'),
194:('V',"A naval admiral... So that's why you wouldn't tell me about him beforehand.",'Lil realizes his naval-admiral background explains why Camille withheld his identity until the meeting.','Restore the specific withheld information andits timing. Do not invent a newpast experience toexplain her reaction.'),
198:('V',"If I'd said he was military, you'd have been biased. I wanted you to meet him and see what a remarkable man he is...",'Camille expected Lil to be prejudiced if told the man was military and wanted her to experience his admirable qualities in person.','Preserve the military prejudice andhis intended reason forthe meeting. Military includes naval service;do not turn Gerhard into anarmy soldier.'),
201:('R',"...",'Lil falls silent after Camille\'s explanation.','Retain the independent silence. Do not invent agreement,forgiveness oradditional military history.'),
205:('V',"Camille.",'Gerhard addresses Camille by name.','Replace the superseded Kamil spelling withapprovedCamille;the restrained direct address remains.'),
209:('R',"Yes, sir! Sorry! She spoke so rudely...",'Camille responds and again apologizes for the rude way Lil spoke to the admiral.','Retain his natural flustered apology. Sir isrespectful address here,not a newly bestowed rank.'),
212:('V',"Never mind that. I'm a little curious why you've chosen to serve this woman.",'Gerhard puts the earlier rudeness aside and says he is a little curious about Camille\'s choice to work under Lil.','Keep the softened curiosity andchoice rather than issue aninterrogation. No longer calling hera girl allows the source tonal shift toremain visible.'),
216:('R',"What?",'Camille is surprised by the question.','Retain the natural short surprised response;the preceding question gives its referent.'),
220:('V',"{MACRO:FI}, was it?",'Gerhard checks that he heard Lil\'s name correctly.','Use a natural tentative name check andpreserve FI rather than the clipped Called construction.'),
223:('R',"Yes.",'Lil confirms her name.','Retain the complete natural acknowledgment ofthe preceding name question.'),
227:('V',"Your words were heartfelt. You may lack manners, but you do seem to care for your friends.",'Gerhard says Lil\'s words were sincere and that despite her poor manners,she seems to care about her friends.','Preserve his measured seem judgment andthe explicit friends,without turning itinto romance,kinship orunconditional praise.'),
231:('R',"...",'Lil pauses after Gerhard\'s assessment.','Retain the silent reaction rather than invent ananswer orinstant affection.'),
235:('V',"I doubt we'll get along, but if Camille is aboard, I'm willing to join your crew.",'Gerhard doubts he and Lil will get along,but offers to sail aboard her ship if Camille is there.','Retain the conditional offer andremaining dislike;use approvedCamille. Do not rewrite itas admiration forLil orassume a permanent prior mentorship.'),
239:('R',"Admiral! Really?!",'Camille enthusiastically checks that Gerhard means the offer.','Retain the natural surprised excitement andthe title he hasbeen using throughout the conversation.'),
243:('R',"Yes, if your admiral agrees.",'Gerhard confirms his offer if Lil,their admiral,accepts.','Retain the natural conditional response;it leaves the decision withLil rather than force her acceptance.'),
247:('R',"{MACRO:FI}! Please say yes!",'Camille eagerly asks Lil to approve the offer.','Retain the idiomatic enthusiastic appeal andFI. It conveys the repeated source confirmation question without adding a promise.'),
250:('V',"I can't imagine ever liking this man, either, but...",'Lil likewise cannot imagine growing fond of Gerhard,but begins to qualify her objection.','Keep the mutual nature oftheir dislike with either andthe unfinished concession. Do not smooth away the friction that survives recruitment.'),
253:('R',"{MACRO:FI}!",'Camille urgently addresses Lil by name.','Retain the genuine name macro andexclamation;normalize the full-width punctuation without inventing another plea.'),
257:('R',"I know. If Camille admires you that much, you must have some good qualities.",'Lil accepts that someone Camille admires so much must have some good qualities.','Retain the complete existing wording anddirect address toGerhard after acknowledging Camille. Normalize only the legacyfull-width I glyphs;the trust isplaced inCamille\'s judgment,not sudden liking forGerhard.'),
260:('V',"We did it! Admiral Ardelknatts, thank you! Please keep teaching me!",'Camille celebrates,thanks Admiral Ardelknatts and asks for continued guidance.','Retain the already-natural enthusiastic wording while correcting the surname toapprovedArdelknatts. Continued guidance isexplicit;no lifelong teacher relationship isasserted.'),
264:('V',"Come now, no more 'Admiral.' She's the one in command now.",'Gerhard asks Camille to stop calling him admiral because Lil is now the commander of this crew.','Preserve the change inshipboard address without inventing atransfer offormal naval rank. His gentler correction prepares the first-name joke.'),
267:('R',"Oh, right... How about Gerhard?",'Camille realizes the address issue and asks whether Gerhard is acceptable.','Retain the natural first-name permission question. Dropping the source honorific inEnglish doesnot invent family familiarity;Gerhard explicitly accepts the form ofaddress.'),
270:('R',"Ha ha! Never thought that day would come.",'Gerhard laughs that he did not expect Camille to address him this way.','Retain the warm amused fragment inits explicit first-name context. No age,death orretirement claim isadded.'),
273:('R',"Admiral, at your service.",'Gerhard formally greets Lil as admiral and offers cooperation aboard.','Retain the natural courteous formula andthe source title. The scene hasjust established Lil\'s command;no noble orfamily relationship isintroduced.'),
276:('R',"...Likewise.",'Lil hesitantly reciprocates Gerhard\'s greeting.','Retain the awkward polite brevity,which suits her reluctant acceptance. It doesnot erase her preceding dislike orcreate anewcommand hierarchy.'),
281:('V',"{MACRO:FI}, this is our chance! Let's ask Ardel... er, Gerhard to teach us how to fight.",'Camille suggests taking this opportunity to learn fighting from Ardelknatts,correcting himself mid-surname to Gerhard.','Restore the abbreviated-surname/first-name correction,not just aflat tutorial offer. Ardel... isatruncation ofapprovedArdelknatts,not a newname. Preserve FI.'),
295:('V',"Hmm... Very well. I'll explain a few things.",'Gerhard agrees to give a brief explanation.','Use a natural measured lesson opener rather than the awkward command Hear a short lesson.'),
298:('R',"Start with naval gunfire. Let me explain the standard crossing-the-T tactic.",'Gerhard begins with naval gunfire and offers to explain the standard T-crossing tactic.','Retain the clear established naval term andnatural lesson opener. Incontext this introduces the topic,not anorder tostart anactual battle.'),
302:('V',"Try to avoid the enemy's sides, where its guns can reach you. Move to its bow or stern, turn your broadside toward it and fire.",'Gerhard advises avoiding enemy gun range along the sides where possible,positioning ahead or behind,and firing with one\'s own broadside facing the enemy.','Preserve the qualification,enemy range,both front/back positions andown broadside orientation. Do not invent agunfire button orchange the tactic.'),
305:('R',"Sounds complicated...",'Lil finds the explanation confusing.','Retain the idiomatic baffled response. Do not replace confusion withanassertion that sheunderstands the tactic.'),
308:('V',"Just steer the ship; the gunners will fire automatically. Assign an officer with good aim to a Battery for better results.",'Gerhard says movement is enough for the gunners to fire and a high-accuracy officer in the gun battery improves effectiveness.','Keep automatic firing andthe skill/assignment benefit. Battery isthe current source-locked UI label;officer preserves航海士 rather than confusing named crew withhired sailors.'),
312:('V',"In battle, set your course and sail direction just as you do when sailing. Your guns fire automatically when an enemy enters range.",'The system explains that battle uses ordinary course and sail-direction controls,and shooting starts automatically when an enemy is in range.','Preserve both controls,the normal-sailing comparison andthe exact automatic-fire condition. FE isaseparate native system/tutorial panel,not progressive character dialogue.'),
315:('V',"If you want to focus on boarding, have a town shipyard convert a cargo hold into Quarters for marines.",'Gerhard suggests remodeling a cargo hold into marine quarters at a town shipyard for a boarding-focused approach.','Keep the conditional strategy,location,refit andcargo-hold conversion. Quarters isthe current native UI name for海兵詰所;for marines preserves its source function.'),
318:('V',"For better results, hire plenty of sailors and station an officer who's skilled with a sword in the Quarters as Boarding Leader.",'Gerhard recommends more hired sailors and a strong swordsman officer assigned as boarding leader in the marine quarters.','Preserve both staffing requirements,the skill,the room andexplicit role. Use verifiedQuarters/Boarding Leader andgender-neutral officer;do not invent a captain rank orguarantee victory.'),
322:('V',"Select an officer who's skilled with a sword and assign them to the Quarters.",'The system suggests selecting an officer good at sword fighting and assigning that officer to the marine quarters.','Restore the named officer andactual assignment action,using currentQuarters. No generic fighter recruitment,gender ornewstat threshold isinvented;preserve the FE consumer.'),
325:('V',"When ships touch, boarding combat begins automatically. Your Boarding Leader should be a big help.",'The system says contact automatically begins boarding combat and the boarding leader is expected to play an active part.','Keep the contact trigger,automatic combat andqualified should. The oldleader commands the attack replaced expected usefulness withaguaranteed action.'),
329:('V',"That's how it works. Do you understand?",'Gerhard concludes the explanation and asks whether Lil understands.','Use a complete natural question rather than bark Understand. This retains his measured teaching tone after accepting her command.'),
333:('V',"Y-yes... sort of.",'Lil hesitantly says she has a vague understanding.','Restore the uncertainty of何となく;mostly overstated howmuch sheunderstands. Keep the initial hesitation.'),
342:('V',"Even if you'd rather not fight, sometimes battle is unavoidable. Never neglect your preparations.",'Gerhard warns that combat can be unavoidable even without a wish to fight,and urges careful preparation.','Keep the conditional lack ofdesire andneed toprepare. The oldseek peace invented anactive pacifist goal;no successful battle outcome isclaimed.'),
}

def retained_canonical(value):
    value=value.replace('Ｉ','I').replace('！','!').replace('？','?').replace('…','...')
    value=' '.join(value.split())
    for token in('FI','FA','FO'):value=value.replace(token,'{MACRO:'+token+'}')
    return value

if __name__=='__main__':
    assert not ROOT.exists()and not DOC.exists()and not CHOICES.exists()
    packet=read(SOURCE)
    assert len(packet['records'])==len(LINES)==79
    assert {r['record_index']for r in packet['records']}==set(LINES)
    assert [r['English']for r in packet['native_current_terms']]==['Boarding Leader','Gunner','Quarters','Battery']
    current=NdsImage.open(packet['candidate'])
    clean=NdsImage.open('work/clean.nds')
    block=IlnkContainer.parse(current.read_file('/data/SC2.DK4')).blocks[74]
    jp=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[74]
    assert sha(block)==packet['current_block_sha256']and sha(jp)==packet['clean_block_sha256']
    names={2:'Lil Argot',9:'Camille Overijssel',14:'Emilio',16:'Gerhard Ardelknatts',20:'Fernando',254:'System tutorial;original FE modal consumer'}
    rows=[]
    for sequence,source in enumerate(packet['records']):
        row=deepcopy(source)
        decision,english,gloss,note=LINES[row['record_index']]
        ja,at=row['source_reference']['offset'],row['current_reference']['offset']
        raw,old=bytes.fromhex(row['source_hex']),bytes.fromhex(row['current_text_hex'])
        assert jp[ja:ja+len(raw)]==raw and block[at:at+len(old)]==old
        assert all(row['source_Japanese'].count(k)==english.count('{MACRO:'+k+'}')for k in('FI','FA','FO'))
        if decision=='R':assert retained_canonical(row['current_stored_English'])==english,(row['id'],'retention wording mismatch')
        prefix=int(row['source_presentation_prefix_hex'],16)
        row.update(english=f'{{SPEAKER:{prefix:02X}}}'+english+'{PAD}',speaker=names[prefix],
            source_meaning=gloss,localization_note=note,editorial_decision='retain-wording'if decision=='R'else'revise',
            contextual_review_sequence_index=sequence,
            context=('CompleteHamburg recruitment exchange,both tutorial choices andall battle explanations reviewed together:wife misunderstanding,Lil\'s defense ofCamille,Gerhard\'s limited apology,past fleet command,mutual dislike,conditional recruitment andexplicit change ofaddress. '
                'Military prejudice andformal deference remain distinct fromnewrespect. No marriage,literaluncle,formalGrandAdmiral rank,retirement orpermanent past mentorship isinvented. '
                'CurrentBattery/Quarters/Boarding Leader terms are source-bound;officers andhired sailors remain distinct. NewB74 native formatting/private-control approval andregistered integration remainpending.'),
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False))
        rows.append(row)
    choices=[]
    for source,text in zip(packet['choices'],('Yes, please.','No need.'),strict=True):
        row=deepcopy(source)
        assert row['current_reference']['text'].rstrip()==text
        row.update(english=text,speaker='Lil Argot',editorial_decision='retain-wording',
            source_meaning='Lil agrees to ask for the battle lesson.'if row['option_index']==0 else'Lil declines the optional explanation because they can manage without it.',
            localization_note='Retain the existing natural short menu reply. Remove authored trailing storage spaces only;both labels preserve the source option order andthe choice tohear orskip the battle lesson.',
            context='CompleteB74 recruitment andbattle-tutorial exchange reviewed. Original actualdefault0 Yes,please reaches the full lesson;No need has source-only branch coverage until typed native checks.',
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False))
        choices.append(row)
    revised=sum(r['editorial_decision']=='revise'for r in rows)
    retained=81-revised
    ROOT.mkdir(parents=True)
    common=dict(translation_policy='natural-dialogue-v2',target_locale='en-US',file_path='/data/SC2.DK4',block=74,
        review_gates=['source','context','localization','naturalness'],formatting_review_pending=True,
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        current_ROM=packet['candidate'],current_ROM_sha256=packet['candidate_sha256'],
        source_clean_ROM_sha256=packet['source_clean_ROM_sha256'],
        approved_names=['Rafael','Hodram','Joakim','Maria','Camille','Gerhard Ardelknatts'],full_goal_complete=False)
    save(DOC,dict(**common,format='dk4-editorial-source-manuscript-v1',encoder='dialogue-fixed-v1',
        dialogue_profile='lil-opening-editorial-native-v1',status='79-source-full-exchange-prose-reviewed;B74-native-and-release-pending',records=rows))
    save(CHOICES,dict(**common,format='dk4-editorial-typed-choice-manuscript-v1',encoder='dialogue-relocatable-v1',
        status='two-source-context-choice-labels-retained;native-and-release-pending',records=choices))
    save(ROOT/'source_context_and81_prose_reviews.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        choices=str(CHOICES),choices_sha256=sha(CHOICES.read_bytes()),source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        reviewed_speeches=79,reviewed_choices=2,proposed_revisions=revised,justified_retentions=retained,
        all_retained_wordings_equal_current_after_only_whitespace_ASCII_I_and_punctuation_normalization=True,
        all_FI_FA_FO_macro_counts_preserved=True,full_context_relationships_names_and_current_UI_terms_reviewed=True,
        scoped_B74_progressive_FE_native_fonts_choices_relocation_and_release_pending=True,
        no_ROM_orledger_completion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_prose_records=81,speeches=79,choice_labels=2,proposed_revisions=revised,
        justified_retentions=retained,no_completion_credit=True))
