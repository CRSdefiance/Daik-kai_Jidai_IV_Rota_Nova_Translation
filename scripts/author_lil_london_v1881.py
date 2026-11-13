"""Fresh contextual London localization; display/control approval remains separate."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

SOURCE = Path('work/analysis/lil_London_source_v1879b/all111_clean_current_native_source_context.json')
DOC = Path('translations/lil_london_editorial_manuscript_v1.json')
ROOT = Path('work/analysis/lil_London_prose_v1881')

# Each entry follows the complete original spoken sequence, including optional
# crew exchanges and the dinner branch. Glosses precede localization decisions.
# R retains wording after contextual review; V revises it. ASCII punctuation is
# normalized separately from wording, never used to conceal a prose revision.
LINES = [
('R',"...?",'Lil notices something and reacts with an uncertain question.','Retain the brief questioning reaction;normalize only ellipsis and question punctuation.'),
('V',"{MACRO:FI}! Look at that ship's flag!",'Fernando alerts Lil to the flag on the ship.','Restore the explicit ship reference;his urgency begins the recognition exchange.'),
('V',"That flag with a skull in a goblet... That's Clifford's ship. He's the English Crown's pirate...",'Lil recognizes the skull-in-a-glass flag and the ship of Clifford,the English royal pirate.','Preserve the emblem andCrown affiliation without inventing a specific monarch;complete the ship identification.'),
('R',"No mistake--the Galahad!",'Fernando identifies the ship as the Galahad with certainty.','Retain the emphatic nautical identification andestablished ship spelling.'),
('R',"Galahad? Does it taste good?",'Emilio mistakes the unfamiliar ship name for something edible.','Retain the natural food joke;its setup andFernando\'s retort work asan exchange.'),
('V',"You idiot! It's not food!",'Fernando calls Emilio foolish and says the Galahad is not food.','Use Fernando\'s blunt contraction rather than a stiff explanatory sentence.'),
('V',"Admiral, let's get out of this town! Nothing good will come of getting mixed up with him!",'An unidentified crew voice urges the admiral to leave town quickly and avoid involvement.','Preserve the explicit admiral address andurgent suggestion without inventing anamed crew speaker.'),
('V',"This is bad, {MACRO:FI}! We have to get out of town. They say he's a really nasty piece of work...",'Camille urgently warns Lil to leave because Clifford is said to be very wicked.','Keep the town,urgency andhearsay in youthful anxious speech.'),
('V',"Is this Clifford fellow really that bad?",'The unidentified man asks whether Clifford is really so terrible.','Keep the casual question;the scene later identifies the stranger asClifford,buthisFE display role remains unverified.'),
('V',"This is your first time here, isn't it? They say James Clifford's a terror of a pirate. Even crying babies go quiet at his name.",'Lil assumes the stranger is new here and repeats the frightening reputation of James Clifford.','Localize the crying-child idiom aspart ofthe exaggerated reputation,setting up the monster joke.'),
('V',"They say he's a towering giant with three eyes and a mouth that stretches from ear to ear. He pours human blood into a goblet and drinks it!",'Rumor describes Clifford as a huge three-eyed man with an ear-to-ear mouth who drinks human blood from a glass.','Preserve every grotesque detail andthe rumor framing;do not make the description a narrator fact.'),
('V',"Come on, is that even a human being?",'The stranger questions whether the described creature is human.','Preserve the incredulous challenge that invites Lil\'s further exaggeration.'),
('V',"But he wiped out an entire fleet all by himself! He has to be a monster!",'Lil insists that someone who destroys an entire fleet alone must be a monster.','Keep her childish insistence andreasoning;this isher claim,not verified battle history.'),
('V',"Me, a monster...? Ha ha ha! Well, that's a new one.",'The man reveals that the monster description concerns him and laughs at the predicament.','Make the self-reference clear for Lil\'s delayed recognition;localize his amused embarrassment naturally.'),
('V',"I know, right? It's unbelievable! ...Hm?",'Lil initially agrees with the stranger\'s reaction,then realizes something is wrong.','Preserve her mistaken agreement andthe beat before recognition without manual layout breaks.'),
('V',"Me...? Wait, are you...? C-Clifford?!",'Lil catches his self-reference and realizes the man may be Clifford.','Keep the startled repetition andstammered name rather than adding information shehas not heard.'),
('V',"What?! This pretty boy is Clifford?!",'Fernando is astonished that the gentle or pretty-looking man is Clifford.','Restore優男 asFernando\'s dismissive contrast tothe monstrous rumor;do not add weakness asafact.'),
('V',"What? This man is Clifford?!",'Gerhard is astonished that this man is Clifford.','Preserve the surprise with his more restrained vocabulary rather than giving himFernando\'s insult.'),
('V',"More or less... Though calling me a monster seems a little harsh.",'Clifford confirms his identity while objecting lightly to being called a monster.','Maintain his easy amusement andunderstatement;do not manufacture anger.'),
('V',"Th-this is bad, {MACRO:FI}... Apologize to him, quick!",'Camille tells Lil the situation is bad and urges a quick apology.','Restore his flustered opening andretain the genuine captain-name macro.'),
('V',"I-I'm sorry... I never thought the famous Clifford would look so ordinary... Oh!",'Lil apologizes but blurts out surprise at how ordinary the famous Clifford looks.','Preserve her accidental second insult andlate realization,which prompts Camille\'s rebuke.'),
('R',"{MACRO:FI}!",'Camille sharply calls Lil\'s name after her tactless apology.','Retain the brief exclamation;the surrounding lines supply the admonishment.'),
('V',"It's all right. I don't mind. More to the point, you're {MACRO:FI} {MACRO:FA}, aren't you?",'Clifford dismisses the offense and asks whether she is Lil Argot.','Preserve the reassurance andboth genuine name macros;the familiarity begins his invitation.'),
('R',"You know about us?",'Lil asks whether Clifford knows about their group.','Retain the existing natural surprised question andplural group reference.'),
('V',"Well, yes. You hear all sorts of things in my line of work.",'Clifford confirms that his work brings him many kinds of information.','Restore the confirmation andcasual first-person voice.'),
('V',"You're not planning to go after {MACRO:FO}, are you...?",'Lil fears Clifford may attack or interfere with her company.','Keep the worried inference asaquestion andpreserve the company-name macro.'),
('V',"Come now. The idea that I crush anything and everything is just a rumor.",'Clifford says his indiscriminate destructive reputation is only rumor.','Make his claim personal andcomplete without endorsing it asnarrator truth.'),
('R',"Really...?",'Lil responds skeptically to Clifford\'s denial.','Retain the natural skeptical question;the ellipsis carries her hesitation.'),
('V',"Believe me or not, that's up to you. Either way, I'd like to talk to you.",'Clifford leaves belief to Lil but says he wants to talk.','Avoid the unrelated English idiom believe it or not;retain her freedom to disbelieve andhis intention.'),
('V',"Talk about what?",'Lil asks what Clifford wants to discuss.','Restore the object ofher question rather than the ambiguous isolated What?'),
('V',"I'd rather not discuss it here... Come to my home tonight. I'd like us to talk over dinner.",'Clifford prefers another setting and invites them home that evening to talk over dinner.','Preserve the location reluctance,time,home,dinner anddiscussion without adding secrecy details.'),
('R',"Huh? Did you say dinner?!",'Emilio excitedly reacts to hearing that dinner is offered.','Retain the natural food-focused interruption,which recalls his earlier Galahad joke.'),
('V',"Yes. I'll see that you're well looked after as my guests.",'Clifford promises to entertain them as guests.','Express the host\'s assurance naturally without inventing a menu oraccommodation.'),
('R',"All right.",'Lil agrees to the dinner invitation.','Retain the short complete acceptance;her excitement comes inthe following exchange.'),
('V',"Tonight, then. I'll be expecting you.",'Clifford confirms the evening visit and says he will wait for them.','Restore the expectation omitted fromthe current short farewell.'),
('V',"Camille, did you hear? Dinner! A pirate who works for the Crown must have a huge mansion! Ooh, I can't wait!",'Lil excitedly imagines a royal pirate\'s large residence and anticipates dinner.','Keep her speculative mansion andexcitement;Crown avoids the unsupported king wording inthe current translation.'),
('V',"I can't wait either! Let's hurry up and go!",'Emilio shares Lil\'s excitement and wants to go soon.','Restore his agreement withLil rather than converting the wish into aquestion.'),
('R',"Wait... Are you going dressed like that?",'Camille asks whether Lil intends to attend in her current clothes.','Retain the natural tactful question that initiates the clothing discussion.'),
('V',"Huh? What's wrong with these clothes?",'Lil asks whether her present clothing looks strange.','Keep the clothing focus;the current generic Something wrong? loses the reason forher surprise.'),
('V',"Listen... He may be a pirate, but he serves the English Crown. In other words, he's a nobleman.",'Camille explains that despite being a pirate,Clifford serves England directly and is a noble.','Preserve the source\'s explicit noble status asCamille\'s explanation;do not turn noble into amoral adjective.'),
('V',"Well, yes. I suppose so.",'Lil agrees with Camille\'s assessment without understanding the implication.','Remove the unsupported dismissive So what? while preserving her casual response.'),
('V',"We're visiting a nobleman's home. I don't think you should wear the same clothes you wear at sea.",'Camille says Lil\'s sailing clothes are unsuitable for visiting a noble\'s home.','Keep his gently critical personal advice andthe sea-clothes comparison.'),
('V',"Oh... You're right. What should we do?",'Lil accepts the point and asks what they should do.','Use a natural acknowledgment rather than the stiff That is true.'),
('V',"Hmm... First, we need to find you a dress. Let's ask a tailor to make one in a hurry.",'Camille proposes arranging a dress and asking a tailor for a rush job.','Preserve the sequence andproposal;the evening deadline isalready established andneed notbe restated asanew claim.'),
('R',"Okay!",'Lil enthusiastically agrees to Camille\'s plan.','Retain the existing idiomatic enthusiastic response.'),
('V',"We managed to get it ready in time for tonight.",'Camille says the preparations just managed to meet the evening deadline.','Restore acomplete conversational observation andthe shared achievement.'),
('R',"Waiting took forever!",'Emilio complains of being worn out by the wait.','Retain the existing impatient exaggeration after the preparations finish.'),
('V',"Still... I have to say, I'm surprised...",'Camille expresses surprise on seeing Lil dressed up.','Restore his first-person reaction so the line reads asspoken English.'),
('R',"Heh. Well?",'Lil playfully asks how she looks.','Retain the short teasing invitation forhis opinion;the visual andprior line establish the subject.'),
('V',"Amazing what a nice dress can do.",'Camille uses the proverb about fine clothes improving even an unremarkable wearer.','Localize the backhanded compliment byeffect;its tactlessness explains Fernando\'s thought andLil\'s disappointed answer.'),
('V',"... (Idiot! Choose your words, Camille!)",'Fernando silently thinks that Camille is foolish and should choose his words.','Keep the thought inparentheses andthe source pause;do not render it asan aloud insult.'),
('R',"I was a fool to ask Camille...",'Lil regrets asking Camille for his opinion.','Retain the natural deflated response tothe backhanded compliment;normalize only the fullwidth pronoun I.'),
('V',"Ah, you're here.",'Clifford greets their arrival.','Use awarm casual greeting rather than the flat You came.'),
('V',"I'm {MACRO:FI} {MACRO:FA}. Thank you for inviting us to dinner.",'Lil formally introduces herself by full name and thanks Clifford for the dinner invitation.','Restore the polite introduction andexplicit dinner;keep both name macros.'),
('V',"My... I almost took you for a young lady from a fine family. That dress suits you.",'Clifford says he thought she might be a well-bred young lady and compliments her appearance.','Preserve the flattering social comparison without inventing actual ancestry oratitle forLil.'),
('V',"Hee hee. You're quite the charmer, Clifford.",'Lil laughs and tells Clifford he speaks flatteringly.','Use acomplete flirtatious compliment that fits her pleasure;no newromantic relationship isasserted.'),
('V',"I wish a certain someone would take a lesson from you.",'Lil indirectly wishes Camille would learn from Clifford\'s flattering manner.','Preserve the pointed indirect comparison rather than explain the target aloud.'),
('R',"...",'Camille has a silent reaction to Lil\'s pointed remark.','Retain the silence,normalizing punctuation only;do not invent anapology orjealous reply.'),
('R',"Come inside.",'Clifford invites them into his home.','Retain the natural host\'s invitation.'),
('V',"What a feast! There are more dishes than I can count...",'Lil marvels at the feast and the countless dishes.','Restore the explicit exaggeration about the number ofdishes.'),
('R',"A-amazing...",'Fernando is awed by the feast.','Retain the existing stammered reaction andrestraint.'),
('V',"I've never seen any of this food before! I don't know what to try first... Munch, munch... It's so good!",'Camille is unfamiliar with all the dishes,cannot choose,and then eats and praises the taste.','Preserve the full emotional progression fromwonder todelighted eating;keep the source eating sounds.'),
('R',"Delicious! Every dish is wonderful!",'Emilio says every dish tastes good.','Retain his existing enthusiastic food praise without adding specific dishes.'),
('V',"Emilio, you're not a pig! At least use a knife and fork!",'Fernando scolds Emilio for eating without using a knife and fork.','Preserve the blunt pig comparison andminimum-manners scolding inFernando\'s informal voice.'),
('R',"Hm. Quite good.",'Gerhard gives the food measured approval.','Retain the concise formal judgment,distinct fromEmilio\'s excited praise.'),
('V',"Ha ha ha! I'm glad you're enjoying it. Help yourselves.",'Clifford laughs and encourages his guests to eat without restraint.','Keep the genial host\'s full reassurance andinvitation.'),
('V',"Now, about what I wanted to discuss...",'Clifford tries to begin the discussion for which he invited them.','Keep the unfinished lead-in that Lil interrupts about her dress.'),
('R',"Wait. This dress is too tight...",'Lil interrupts because her dress feels constricting.','Retain the direct natural complaint;the following lines deal withchanging clothes.'),
('R',"Oh, honestly, {MACRO:FI}...",'Camille reacts in exasperation to Lil\'s interruption.','Retain the natural exasperation andgenuine name macro.'),
('V',"Ha ha ha! There's no need to force yourself. Go and change in the back.",'Clifford tells Lil not to endure discomfort and offers a place farther inside to change.','Keep his easy hospitality;do not invent aspecific bedroom orprivate relationship.'),
('V',"Whew. These clothes suit me much better than that dress. Sorry to keep you waiting.",'Lil says her usual clothes suit her better than the dress and apologizes for the delay.','Restore the explicit comparison while keeping her relieved,unselfconscious voice.'),
('R',"Now, down to business.",'Clifford resumes the main subject after Lil changes.','Retain the idiomatic transition;it works after his earlier interrupted lead-in.'),
('V',"Did you know a man named Pedro Valdes has been appointed commander in chief of the Spanish navy? He's one of the strongest commanders they've ever had.",'Clifford reports Valdes\'s appointment and rates him among the top one or two commanders in the navy\'s history.','Preserve the appointment,full name,naval command andhistorical comparison without claiming unmatched strength.'),
('R',"That news reached me too.",'Gerhard confirms that he has heard the report.','Retain the natural measured confirmation suitable forGerhard.'),
('V',"Spain... The last thing we need is for that Armada to get even stronger.",'Lil dreads the Spanish Armada growing more powerful.','Use natural apprehensive speech;retain the already formidable fleet andfurther growth.'),
('V',"Exactly. And the same goes for me.",'Clifford shares Lil\'s concern about Spain\'s strength.','Complete the personal agreement without making his fleet already afraid.'),
('V',"What? You're kidding! They say your fleet's invincible and doesn't even consider the Spanish navy a threat!",'Lil is surprised because Clifford\'s forces are reputed invincible and unconcerned with Spain.','Preserve her disbelief andthe reputation framing;remove the inherited broken isolated fleet line.'),
('V',"Even so, with that man in command...",'Clifford hesitates because Valdes himself is the opponent.','Do not invent fleet-wide fear fromthe source\'s understated unfinished concern.'),
('V',"He's that formidable...?",'Lil realizes Valdes must be a formidable opponent.','Make her inference aquestion anduse natural contraction.'),
('V',"So here's my proposal. Why don't you join forces with me?",'Clifford proposes cooperating with Lil.','Keep the proposal asan invitation rather than anorder.'),
('R',"With us? What do you mean?",'Lil asks what cooperating with her group would mean.','Retain the complete natural surprised question.'),
('V',"If we work together, even they won't be so quick to move against us. Don't you agree?",'Clifford argues that cooperation would deter Spanish action against them.','Preserve the conditional deterrence andquestion without promising anabsolute guarantee.'),
('V',"Hmm. Not a bad idea, but...",'Gerhard acknowledges that the plan is not bad but hesitates.','Complete his measured evaluation while preserving the unfinished reservation.'),
('V',"Maybe you're right. But taking on the Spanish navy... I don't think I...",'Lil considers the plan but falters at the idea of defeating the Spanish navy.','Retain her unfinished hesitation instead ofturning it into afirm declaration ofcollective inability.'),
('V',"Come now. I'm not asking you to do that.",'Clifford says he is not asking Lil\'s group to defeat the navy.','Keep responsibility forhis ownrequest;the old Nobody expects that asserted what everyone thinks.'),
('R',"Then what?",'Lil asks what he actually wants.','Retain the curt natural follow-up that suits her directness.'),
('V',"Listen. You join forces with me, and we keep their movements in check.",'Clifford explains that their cooperation will restrain Spanish movements.','Make the joint role clear without changing deterrence into ademand foropen war.'),
('V',"That's all?",'Lil asks whether that is the whole request.','Use the natural incredulous response to the limited task.'),
('V',"That's enough. Look, it's a big world. Together, we keep his forces in check while each of us expands into other regions.",'Clifford says containment will suffice while each expands elsewhere in the wide world.','Preserve joint containment andseparate expansion;not asequence requiring Spain tobe contained first andthen abandoned.'),
('V',"Oh, I see! Instead of staying in the North Sea, we each head for places like Africa and India!",'Lil understands that both can expand beyond the North Sea toward Africa and India.','Restore India rather than the vague East;Clifford\'s following lines specify their different destinations.'),
('R',"Makes sense.",'Fernando acknowledges the logic.','Retain the idiomatic brief agreement.'),
('R',"Right.",'Clifford confirms Lil\'s understanding.','Retain the concise reply;the next line elaborates the plan.'),
('V',"I'll follow England's policy and head for the New World. You'll follow the Dutch policy of expanding south, through Africa to India and Asia.",'Clifford will follow English policy toward the New World,while Lil follows Dutch southern expansion through Africa,India and Asia.','Restore every named destination andthe two countries\' policies;do not reduce the New World towest oromit India.'),
('V',"And once we've built up our strength...",'Clifford leaves the consequence of accumulating strength for Lil to supply.','Keep the shared conditional setup that shecompletes inthe next speech.'),
('R',"Someday we can defeat that mighty Armada!",'Lil concludes that eventually they could defeat the Spanish Armada.','Retain the enthusiastic completion ofhis unfinished thought;it states their aspiration incontext.'),
('R',"Right. You learn fast.",'Clifford confirms and compliments Lil\'s quick understanding.','Retain the lightly patronizing encouragement that suits his persuasive manner.'),
('R',"But...",'Lil raises a remaining objection.','Retain the brief hesitation;the next question invites her concern.'),
('V',"Hm? Is there a problem?",'Clifford asks whether something is wrong.','Use acomplete natural question instead ofthe clipped article-less fragment.'),
('V',"I don't know if I can trust you...",'Lil doubts whether she should trust Clifford.','Restore her personal uncertainty rather than directly accuse him ofuntrustworthiness.'),
('V',"Come now. I am an English gentleman, after all.",'Clifford invokes his status as an English gentleman.','Restore the missing predicate andhis self-assured appeal torespectability.'),
('V',"That doesn't prove a thing.",'Lil says being an English gentleman is irrelevant to whether he can be trusted.','Use her natural blunt dismissal;Gerhard\'s optional reply develops the same concern aboutmere words.'),
('R',"Words alone prove nothing...",'Gerhard points out that words can claim anything.','Retain the natural skeptical observation matching the trust exchange.'),
('V',"Then I could give you the Crimson Dye as a token of friendship.",'Clifford offers the Crimson Dye as a sign of friendship.','Preserve the conditional offer andfriendship rather than replacing it withalready established trust;use the current approved item name.'),
('V',"Dye...? What's that?",'Lil asks what the dye is.','Keep the question aboutthe object,not the oldunsupported question aboutits use.'),
('V',"They say it's the key to deciphering a map to hidden treasure. So? Will you join forces with me?",'Clifford says the dye is reportedly a key to decoding a treasure-location map and asks whether Lil will cooperate.','Preserve hearsay anddeciphering anexisting map;do not invent that the dye creates orreveals amap.'),
('V',"For now, it looks like we'll have to trust him...",'Fernando says they apparently have little choice but to trust Clifford for the time being.','Restore the provisional fornow andqualified assessment.'),
('V',"...All right.",'Lil reluctantly agrees.','Preserve her hesitation;the older bright Okay did not carry the same emotional beat.'),
('V',"That's the spirit! Let's make this work!",'Clifford welcomes her agreement and anticipates their cooperation.','Use his upbeat casual voice without inventing anexisting partnership history.'),
('V',"I'd rather you kept out of the New World. The people dug in there are my prey. Don't go picking fights with them on your own.",'Clifford asks Lil not to interfere much in the New World because the entrenched groups are his targets.','Keep the territorial possessiveness andprey metaphor;retain the specific ban onunilateral fighting.'),
('V',"The tavernkeeper has the Crimson Dye. Go to the tavern in Amsterdam.",'Clifford says the Amsterdam tavernkeeper holds the dye and directs Lil there.','Keep both the holder andprecise destination;remove inherited broken line aroundthe item name.'),
('V',"All right. But let me be clear: if you betray me, I'll never forgive you!",'Lil agrees but warns that she will not forgive betrayal.','Preserve her actual warning rather than inventing physical retaliation fromyou will regret it.'),
]

if __name__ == '__main__':
    assert not DOC.exists() and not ROOT.exists()
    packet = read(SOURCE)
    assert len(LINES) == len(packet['records']) == 111
    records = []
    for i,(source,(decision,english,gloss,note)) in enumerate(zip(packet['records'],LINES,strict=True)):
        row = deepcopy(source)
        prefix = row['source_presentation_prefix_hex']
        row.update(source_meaning=gloss,english=f'{{SPEAKER:{prefix.upper()}}}'+english+'{PAD}',
            editorial_decision='retain-wording' if decision=='R' else 'revise',localization_note=note,
            context=('LondonB26 complete111-speech conversation reread inoriginal order withallconditional crew/dinner exchanges. '
                'Recognition andgrotesque rumor becomeClifford\'s amused reveal;dinner/clothing teasing leads intoa wary anti-Spanish cooperation proposal andAmsterdam dye direction. '
                'Each line isreviewed withits neighboring responses andnative branch ancestry;no newkinship orromantic relation isasserted. '
                'Allsource bytes andpreambles arepreserved;newscene control mapping,native format andrepresentative gameplay remainpending.'),
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            contextual_review_sequence_index=i,display_mapping_pending=prefix in ('97','fe','1c','10'))
        if prefix=='fe':
            row['speaker']='Clifford, initially an unidentified stranger;FE presentation unverified'
            row['speaker_context_basis']='The stranger\'s first-person monster response andLil\'s next recognition identify the same conversational speaker;not anapproved native portrait/name mapping.'
        elif prefix=='97':
            row['speaker']='Unidentified crew voice;97 presentation unverified'
        records.append(row)
    revised = sum(r['editorial_decision']=='revise' for r in records)
    retained = 111-revised
    ROOT.mkdir(parents=True)
    doc = dict(format='dk4-editorial-source-manuscript-v1',translation_policy='natural-dialogue-v2',
        target_locale='en-US',encoder='dialogue-fixed-v1',dialogue_profile='lil-opening-editorial-native-v1',
        file_path='/data/SC2.DK4',review_gates=['source','context','localization','naturalness'],
        formatting_review_pending=True,status='all111-source-prose-context-reviewed;native-display-andrelease-pending',
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        source_clean_ROM_sha256=packet['source_clean_ROM_sha256'],current_ROM=packet['candidate'],
        current_ROM_sha256=packet['candidate_sha256'],approved_names=['Rafael','Hodram','Joakim','Maria','Camille'],
        speaker_catalog=packet['native_speaker_catalog'],records=records,
        no_fixed_allocation_trimming_no_production_insertion=True,
        runtime_controls_preserved_but_unapproved_new_scene_controls_not_formatted=True,
        full_goal_complete=False)
    save(DOC,doc)
    save(ROOT/'all111_contextual_source_prose_review.json',dict(manuscript=str(DOC),
        manuscript_sha256=sha(DOC.read_bytes()),source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        complete111_exchange_and_neighbor_responses_read=True,revisions_proposed=revised,justified_retentions=retained,
        source_macro_counts_preserved=all(all(r['source_Japanese'].count(k)==r['english'].count('{MACRO:'+k+'}') for k in ('FI','FA','FO')) for r in records),
        pending_control_families=['0x97 crew voice','0xFE anonymous-to-Clifford exchange','0x1c Clifford','0x10 Gerhard exact B26 scope'],
        pending_display_font_bounds_pagination_relocation_andrepresentative_scene=True,
        no_ROM_orregistry_orcompletion_count_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_prose_reviews=111,proposed_revisions=revised,justified_retentions=retained,formatting_andrelease_pending=True))
