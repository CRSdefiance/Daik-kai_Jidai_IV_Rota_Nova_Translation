"""Fresh complete-exchange SC0 B44 editorial manuscript; no release authorization.

The source gloss, proposed wording and individual decision are authored below.
Equals retains the normalized existing English, not its old layout bytes.
"""
from collections import Counter
from pathlib import Path
import re

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/rafael_opening_contextual_v1994')
PACKET = Path('work/analysis/editorial_source_census_v1992/SC0_block044_raw_source.json')
BATCH = Path('translations/rafael_opening_contextual_editorial_manuscript_v1.json')
CHOICES = Path('translations/rafael_opening_contextual_choices_editorial_draft_v1.json')

# ordinal | source gloss written before localization | English (=retain) | reason
TEXT = r"""
0|Claudio brushes aside questions: just go and Rafael will understand.|=|The repeated urging and promised explanation keep Claudio's impatient enthusiasm before the ship reveal.
1|Claudio asks FI what he thinks of seafaring men.|=|Men of the sea fits Claudio's romantic ideal and sets up Rafael's uncertain reply.
2|Rafael hesitates: it is hard to say what he thinks.|=|The hesitant answer leaves Claudio room to launch into his heroes rather than rejecting seafaring outright.
3|Claudio names Prince Henry and Duke Leon and admires how impressive they are.|=|Both named historical/story figures and Claudio's excited admiration remain; no extra title or relationship is supplied.
4|Claudio declares that the sea is a man's romantic dream.|=|A man's greatest adventure naturally conveys his boastful romantic ideal in this exchange.
5|Rafael thinks Claudio has started his usual speech again.|=|The familiar weary aside contrasts naturally with Claudio's enthusiasm.
6|Rafael asks how they can go to sea without even having a ship.|=|The practical objection prepares the surprise reveal and preserves the missing ship as the problem.
7|Claudio complains that Rafael has no romance when he is talking about his dreams.|=|Can't a man dream carries the playful complaint without importing a new ambition.
8|Claudio announces that they have arrived.|=|The abrupt arrival shifts from argument to the reveal without explaining it early.
9|Janus greets the arriving pair.|=|The mild greeting establishes Janus's calm contrast with Claudio.
10|Rafael reacts with emphatic surprise before he can name what he sees.|!!|Use American punctuation while keeping the separate wordless surprise beat.
11|Rafael slowly recognizes a ship.|=|A ship and the ellipsis preserve the stunned recognition; the source's leading blank rows are staging rather than English prose.
12|Claudio asks whether Rafael is surprised and announces the ship's name, Carteira.|=|The reveal, already chosen name and showman's flourish all work naturally.
13|Claudio and Janus took over a discarded near-scrap ship and repaired it.|We took in an old wreck that was practically scrap. Janus and I fixed her up.|Keep both men as joint repairers and avoid making acquisition a chance discovery or Janus merely a helper.
14|They cannot sail immediately, but will someday after saving money.|=|The delay and savings condition remain clear before Rafael's sudden decision.
15|Rafael quietly proposes going.|=|The spare line preserves the reversal from skeptic to the keenest member.
16|Janus is startled by Rafael's proposal.|=|The short surprised question fits his interruption.
17|Claudio is startled too.|=|Huh keeps his rougher voice distinct from Janus's What.
18|Rafael reminds Claudio that he wanted to go to sea and says asking Julio should solve the money problem.|Didn't you say we should go to sea, Claudio? If it's money we need, we can ask Julio!|Restore the reminder and Rafael's confident proposal; he is not merely agreeing or predicting a possible loan.
19|Rafael announces that he is going straight to Julio now.|=|The immediate departure fits his new urgency without inventing kinship with the older man.
20|Claudio calls after FI.|=|The first interrupted call starts Claudio's failed attempt to stop him.
21|Rafael asks Janus and Claudio to keep repairing the ship and says he is counting on them.|Janus, Claudio, keep working on the repairs! I'm counting on you!|Continue the work rather than assigning a new rank or responsibility; preserve the departing appeal.
22|Claudio calls FI again and asks him to wait.|=|The second call escalates the first naturally while preserving FI.
23|Claudio ruefully observes that Rafael has ended up the most eager of them.|=|The irony completes the earlier argument about dreams and practicalities.
24|Janus laughs that Rafael has caught Claudio's specialty: once inspired, he cannot sit still.|Ha! Looks like he picked up your habit of charging ahead. Once he makes up his mind, he can't sit still.|Retain the working idiom and restore the amused laugh that softens Janus's teasing.
25|Claudio says Rafael has always been that way despite appearances, then asks about repairs.|=|The character observation and immediate practical topic change both remain.
26|Janus says repairs are almost finished, though he did nearly all the work.|=|The restrained complaint punctures Claudio's earlier joint-repair boast without overplaying resentment.
27|Claudio tells Janus not to quibble because he enjoyed the work.|=|The casual deflection and affectionate teasing sound natural together.
28|Janus laughs, concedes the point and suggests following Rafael to Julio.|=|The concession resolves the teasing and moves the group toward the next exchange.
29|Claudio insists he needs to accompany and look after FI.|=|His protective boast is clear without turning friendship into a family relationship.
30|Janus indulgently acknowledges Claudio and urges them to go.|=|All right and Come on capture his gently dismissive response and the scene transition.
31|Julio assumes Claudio is seeking yet another advance, scolds him and demands to know its use.|What?! Another advance, Claudio? The nerve of you! What do you need it for this time?|Remove an invented flat refusal and waste claim; Julio is scolding a familiar repeat borrower before hearing the plan.
32|Claudio protests at Julio suddenly shouting and rudely calls him an old man.|...Don't start yelling at us, old man!|Preserve the startled pause and rude response without adding that nobody has spoken yet.
33|Rafael apologizes for making an unreasonable request.|=|The polite apology contrasts with Claudio's attack and begins Rafael's own appeal.
34|Julio recognizes Rafael as the boy from the FA household.|=|The FA boy naturally identifies the household without inventing a different relation or title.
35|Rafael apologizes for his impoliteness.|=|Barging in is a natural apology for this abrupt approach and fits the immediate situation.
36|Claudio says this time is different and serious, then rudely demands a loan instead of stinginess.|=|The insistence and rude demand preserve the comic reason Julio distrusts him.
37|Julio has never seen Claudio do honest work and says expecting trust is naive.|I've never seen you do an honest day's work. And you expect me to trust you?|Keep this as Julio's experience and accusation rather than an omniscient fact that Claudio has never worked.
38|Janus observes that Claudio's everyday behavior is the reason.|=|Reap what you sow conveys the dry observation in familiar American English.
39|Claudio growls in frustration.|=|The brief growl holds his frustration before Rafael takes over.
40|Rafael pleads with Julio, says the idea was his and asks whether it is absolutely impossible.|Please, Julio! This was my idea! ...Is there really no way?|Restore the earnest question rather than changing it into a polished appeal for persuasive words.
41|Julio hesitates because it is a large amount, even for FI, and asks what his father says.|Hmm... It's a lot of money, even with you asking, FI. What does your father say?|Preserve the hesitation and personal regard; asking for the father's view does not presume consent has been requested.
42|Rafael refuses to rely on his father for this, promises repayment and pleads again.|I don't want to rely on my father for this. I promise I'll pay you back! Please!|Keep Rafael's own resolve and personal promise; do not assert that the father is excluded as an established fact.
43|Julio admires Rafael's wish for independence and resolve but still hesitates.|=|The praise and trailing reservation make his later change of heart credible.
44|Claudio says they will stop asking and orders FI and Janus to leave.|=|His irritated retreat interrupts the unsuccessful appeal and preserves both companions.
45|Janus tells Claudio he understands and asks not to be dragged.|=|The physical dragging joke remains mild and immediate.
46|Rafael apologizes once more for the unreasonable request and takes his leave.|=|The courteous departure contrasts with Claudio's anger and motivates Julio's reconsideration.
47|Julio falls silent after they leave.|...|Keep the separate reflective silence using American ellipsis punctuation.
48|Claudio sighs that his exit sounded fine but asks what they should do now.|=|The rueful admission undercuts his grand exit without inventing a plan.
49|Janus asks FI why he does not ask his father for help.|FI, why won't you ask your father for help?|Correct whether to why; Rafael has just explicitly said he does not want to rely on his father.
50|Rafael says his father always treats him as a child and would surely oppose him going to sea.|My father still treats me like a child. He'd never agree to let me go to sea.|Opposing a seafaring venture is broader than forbidding him merely to board a ship.
51|Rafael says nothing will change unless he does something here and now.|Nothing will change unless I do something right now!|Preserve Rafael's personal determination instead of shifting the subject to the whole group.
52|Claudio praises FI's spirit and says that is how a man should be.|=|The masculine boasting echoes his earlier romantic speech and stays part of his characterization.
53|Janus approves the spirit but notes that money is needed and spirit alone cannot suffice.|=|Courage won't cover the cost is a natural dry rejoinder to Claudio's boast.
54|Claudio asks Janus not to mention that and sighs that steady effort may be the only way.|=|The deflation and resigned need to earn the money continue the practical-versus-romantic exchange.
55|Julio calls out to the departing group.|=|The drawn-out call naturally interrupts their discussion.
56|Rafael notices Julio and wonders what he wants.|=|The question preserves Rafael's uncertainty before the reversal is explained.
57|Julio is relieved they have not left yet.|=|The repeated Good preserves his relieved, older voice without invented family address.
58|Janus politely asks what Julio wants.|=|The short question keeps the scene moving toward the loan reveal.
59|Julio says he has thought things over.|I've been thinking it over...|Replace an unnecessarily formal statement with Julio's hesitant conversational lead-in.
60|Claudio impatiently tells the old man to hurry up and say it.|=|Out with it already preserves the rude impatience that fuels their later quarrel.
61|Julio collects himself, addresses FI and offers something.|=|The short offering keeps the money reveal for Rafael and the next system panel.
62|Rafael is startled by what he has been given.|=|The unfinished recognition naturally leads into the money notice.
63|The party receives 30000 gold coins.|=|The exact amount and receipt remain intact; FE is a distinct system-panel control, not a portrait selector.
64|Having handed over the money, Julio insists on repayment with interest.|=|Both principal and interest survive, preserving that this is a loan rather than a gift.
65|Rafael stammers assent and promises to work hard.|=|The stammer and eager promise fit his relief at obtaining funds.
66|Julio worries about what will become of his funds and has decided to watch over them.|Still, I worry about what'll become of my money. So I've decided to keep an eye on it.|Keep the joke's object as the money and leave the boarding revelation to Rafael's puzzled beat and Julio's next line.
67|Rafael is puzzled by Julio's decision.|??|Keep the separate puzzled beat with American punctuation.
68|Julio explains that he is saying he too will board the ship.|Don't you understand? I'm sailing with you.|Avoid adding self-description as this old man; the reveal is his joining the voyage.
69|Rafael asks if Julio really means it.|=|The delighted disbelief follows the explicit boarding reveal.
70|Janus is reassured to have a veteran navigator aboard.|=|The experience and reassurance remain without inventing a new military rank.
71|Julio is embarrassed at being called a veteran and admits he has been away from sailing.|=|The modest laugh-inducing qualification follows Janus's praise naturally.
72|Claudio skeptically asks whether the old man will really be useful.|=|The rude doubt immediately punctures the praise and prepares Janus's correction.
73|Janus asks Claudio to stop being rude and says Julio is famous as a navigator too.|=|Enough, Claudio carries the rebuke; renowned navigator retains the relevant credential.
74|Julio tells FI that he will be the ship's captain.|=|This rank is explicit in the source and is essential to Rafael's later captain's order.
75|Rafael is astonished because the ship was Janus and Claudio's work.|=|The repair wording recalls the ship reveal and explains Rafael's reluctance without claiming ownership transfer.
76|Julio lends on trust in FI FA as leader of FO, making Rafael responsible.|I'm lending this money because I trust you, FI FA, as the leader of FO. You're responsible.|Correct the implication that the loan is made to the company; preserve personal trust, all three macros and Rafael's responsibility.
77|Rafael is flustered at being called leader of FO.|=|The startled fragments convey his reluctance without making him accept the title yet.
78|Julio says making a name among the world's renowned seafarers requires that much spirit.|=|The ambition and scale remain in an idiomatic challenge; no new conquest goal is invented.
79|Julio explicitly makes FI FA captain of the ship, admiral of the fleet and leader of FO.|So, FI FA, you're captain of this ship, admiral of the fleet, and leader of FO.|Keep the three distinct explicit roles; command its fleet obscured the named admiral role that Julio is spelling out.
80|If Claudio were leader, Julio would make him work for free for life should anything go wrong.|Or would you rather put Claudio in charge? If anything goes wrong, he'll be working for me for free for the rest of his life...|Preserve the conditional threat and unpaid work, rather than converting it into a general debt-repayment prediction.
81|Julio asks whether Claudio is still willing under those terms.|=|The pointed question completes the threat and directs Claudio's retreat.
82|Claudio stammers refusal, insists FI should lead and seeks Janus's agreement.|=|The comic reversal, FI macro and appeal to Janus remain natural.
83|Janus agrees that being a leader does not suit him.|=|The understated refusal reinforces his calmer voice and leaves Rafael in charge.
84|Rafael still tries to object.|=|The unfinished objection preserves his hesitation before Julio's reassurance.
85|Julio reassures him that making an effort is enough.|=|Just give it your best naturally softens the preceding formal responsibilities.
86|Rafael finally understands and says he will try.|All right! I'll give it a try!|Keep his personal acceptance and tentative resolve rather than shifting to a group declaration.
87|Julio is satisfied and tells him to use the money as initial operating funds.|Good. Put that money to use as your starting capital.|Keep the instruction to use the funds, not just a prediction of what they will be.
88|Rafael thanks Julio and promises to use the money carefully.|Thank you! I'll use it wisely!|Every coin will count implied thrift; the source explicitly promises careful use.
89|Janus expresses gratitude for all Julio has done.|=|The direct thanks naturally sums up the money, guidance and participation without enumerating invented benefits.
90|Claudio says the old man has a surprisingly good side.|=|The backhanded compliment deliberately reignites their bickering.
91|Julio objects to the young upstart speaking so grandly.|=|Young pup and high and mighty keep the generational sparring without inventing kinship.
92|Claudio angrily says he was giving the old man a compliment.|What was that, you old fossil? I was giving you a compliment!|Restore Claudio's stated defense; he does not demand gratitude in the Japanese.
93|Julio says Claudio needs to suffer a little before appreciating his greatness.|=|The exaggerated threat and self-importance are part of the comic quarrel.
94|Claudio challenges Julio to a fight.|=|The short challenge naturally escalates their exchange.
95|Julio chuckles that he will not lose to someone like Claudio.|=|The boastful older voice answers the challenge without claiming a specific past fight.
96|Rafael asks both men to stop.|=|The first polite intervention precedes his stronger captain's order.
97|Julio refuses and says he will not be satisfied until he punches Claudio once.|No! I won't be satisfied until I've given this fool a good punch!|Keep the explicit physical threat; knocking sense into him softened and recast his stated motive.
98|Claudio taunts Julio that he must want to break his own finger bones.|Oh yeah? You want to break your fingers that badly?|Make clear the taunt is that Julio will hurt his own fist, not a new threat that Claudio will deliberately break his fingers.
99|Rafael loses patience, invokes his captain's authority and orders the quarrel to stop.|Enough! Captain's orders: stop fighting!|Keep the emotional escalation and explicit order that sets up both men's identical response.
100|Claudio instantly agrees if the captain says so.|=|The identical mock-obedient response must match Julio's next line for the imitation joke.
101|Julio gives the same obedient response as Claudio.|=|Retain exactly the same words as Claudio so the following copying accusation makes sense.
102|Claudio accuses the old man of copying him.|=|The accusation correctly follows their deliberately identical replies.
103|Julio snorts that he would never imitate someone like Claudio.|Hmph! As if I'd ever imitate you.|Keep the denial as Julio's own stance rather than a claim about nobody ever imitating Claudio.
104|Janus ruefully remarks on the pair.|=|What a pair conveys his amused exasperation and releases the quarrel's tension.
105|Julio dismisses the fool, says preparation is most of the job and proposes gathering voyage necessities.|=|Good preparation is everything idiomatically conveys the preparation proverb; the next clause preserves the voyage setup.
106|Julio warns that there is much to do and tells Rafael to follow closely.|There's a lot to do, so stay close and pay attention.|Keep the workload explicit while retaining the mentor's practical instruction.
107|Rafael eagerly asks to be taught.|=|The eager assent confirms his willingness to learn after accepting command.
108|Claudio complains that Julio knows a little about ships and already acts like FI's teacher.|=|The grumbling teacher complaint preserves jealousy without inventing family ties; literal teacher address is supported here.
109|Janus tells Claudio to stop the smart remarks and come along.|=|Enough chatter is a natural mild rebuke that ends the bickering and moves them on.
110|Janus proposes beginning voyage preparations.|=|The clear practical instruction opens the tutorial selection exchange.
111|Janus asks whether to learn preparations from Julio or prepare for departure independently.|=|Both options are explicit and parallel; the following short labels remain unambiguous in context.
112|Julio agrees to begin preparations and says to visit the trading post first.|=|The first destination and preparation order remain unchanged.
113|Julio advises visiting at least the trading post, tavern and square before departure in any town.|Before leaving any town, you should at least visit its trading post, tavern, and square.|Preserve the advice and at-least qualification rather than presenting a rigid mandatory list.
114|Julio is pleased by Rafael's confidence and encourages him to do his best.|Oh! That's reassuring. Well, give it your best!|Acknowledge confidence in the independent-preparation branch without adding an instruction to depart immediately.
"""


def paragraph(value):
    return re.sub(r'\s+', ' ', value).strip()


def markup(text, prefix):
    text = re.sub(r'\b(FI|FA|FO)\b', lambda m: '{MACRO:'+m[1]+'}', text)
    return '{SPEAKER:'+prefix.upper()+'}'+text+'{PAD}'


if __name__ == '__main__':
    assert not ROOT.exists() and not BATCH.exists() and not CHOICES.exists()
    packet = read(PACKET)
    assert len(packet['records']) == 115
    entries = [line.split('|') for line in TEXT.strip().splitlines()]
    assert len(entries) == 115 and [int(r[0]) for r in entries] == list(range(115))
    ROOT.mkdir(parents=True)
    (ROOT/'complete_exchange_source_current.json').write_bytes(PACKET.read_bytes())
    records = []
    speakers = {'00':'Rafael Castor','04':'Janus','05':'Claudio','06':'Julio','fe':'System money notice'}
    for source, (ordinal, gloss, proposed, reason) in zip(packet['records'],entries,strict=True):
        old = source['provisional_current_reference']
        before = paragraph(old['body_after_first_byte_CP932'])
        english = before if proposed == '=' else proposed
        prefix = source['source_reference']['leading_byte_hex']
        assert prefix == old['leading_byte_hex']
        assert sorted(re.findall(r'\b(?:FI|FA|FO)\b',english)) == sorted(re.findall(r'FI|FA|FO',source['source_reference']['body_after_first_byte_CP932']))
        decision = 'retain-wording' if english == before else 'revise'
        records.append(dict(id=source['id'],file_path=packet['file_path'],block=44,source_ordinal=int(ordinal),
            source_reference=source['source_reference'],current_reference=old,
            source_hex=source['source_reference']['hex'],current_text_hex=old['hex'],
            source_record_index=source['source_reference']['segment_index'],record_index=old['segment_index'],
            source_Japanese=source['source_reference']['body_after_first_byte_CP932'],current_stored_English=old['body_after_first_byte_CP932'],
            source_complete_preamble_hex=source['source_reference']['complete_preamble_hex'],
            source_presentation_prefix_hex=prefix,speaker=speakers[prefix],source_meaning=gloss,
            english=markup(english,prefix),editorial_decision=decision,localization_note=reason,
            **({'fresh_retained_wording_justification':reason} if decision == 'retain-wording' else {'finding':reason}),
            context="Full Lisbon opening: Claudio's romantic boasting and Rafael's skepticism reverse at the Carteira reveal. Rafael seeks independence from his father, politely appeals for a loan, and Julio reconsiders. Personal trust makes Rafael captain, admiral and company leader. Claudio and Julio's quarrel forces him to exercise command; Janus supplies dry practical balance. Both preparation choices and their distinct responses are reviewed. No kinship inferred from familiar address.",
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)))
    common = dict(format='dk4-ilnk-translation-batch-v1',file_path=packet['file_path'],
        source_file_sha256=packet['current_file_sha256'],editorial_clean_source_file_sha256=packet['clean_file_sha256'],
        encoder='dialogue-fixed-v1',dialogue_profile='raphael-story-live',translation_policy='natural-dialogue-v2',target_locale='en-US',
        review_gates=['source','context','localization','naturalness','formatting'],
        source_ROM='work/clean.nds',current_ROM='out/all_routes_combined_v1986_candidate.nds',
        clean_block_sha256=packet['clean_block_sha256'],current_block_sha256=packet['current_block_sha256'],
        raw_source_packet=str(PACKET),raw_source_packet_sha256=sha(PACKET.read_bytes()),
        draft_only_not_registered_or_formatting_approved=True,full_goal_complete=False,
        no_new_gameplay_display_or_editorial_completion_credit=True,
        required_next_gates=['Resolve exact current B44 span at6604 and target mapping from native commands.',
            'Compile without prose layout hacks; relocate only with independently reviewed typed references.',
            'Validate controls, substitutions, complete native glyph planes, wrapping, bounds and pagination.',
            'Representative story/choice transition tests for distinct risks, then registered cumulative release and exact clean-input patch.'])
    save(BATCH,{**common,'records':records})
    native_clean = read('work/analysis/native_storyline_census_v1991/SC0_block044_clean_native.json')['typed_choice_objects'][0]
    native_current = read('work/analysis/native_storyline_census_v1991/SC0_block044_current_native.json')['typed_choice_objects'][0]
    choices = []
    for i, text, gloss, reason in (
        (0,'Ask him.','Choose to learn voyage preparations from Julio.','The preceding question names Julio; Ask him is unambiguous, natural and preserves the original eight-byte slot without invisible padding.'),
        (1,'Prepare alone.','Choose to prepare for departure independently.','The phrase directly answers the preceding question and preserves the fourteen-byte slot; alone means without tutorial guidance, not without the crew.')):
        a,b = native_clean['labels'][i],native_current['labels'][i]
        assert bytes.fromhex(b['hex']).decode('cp932') == text
        a_at,b_at = a['offset'],b['offset']
        # Exact source/current segment IDs are independently recovered from ROM bytes.
        from dk4tool.rom.nds import NdsImage
        from dk4tool.formats.ilnk import IlnkContainer
        src,now = [IlnkContainer.parse(NdsImage.open(p).read_file('/data/SC0.DK4')).blocks[44] for p in ('work/clean.nds',common['current_ROM'])]
        source_index, current_index = src[:a_at].count(b'\0'), now[:b_at].count(b'\0')
        choices.append(dict(id=f'DK4_MES_B44_R{source_index:04d}',file_path=packet['file_path'],block=44,
            source_reference=dict(offset=a_at,bytes=a['bytes'],segment_index=source_index),current_reference=dict(offset=b_at,bytes=b['bytes'],segment_index=current_index),
            source_hex=a['hex'],current_text_hex=b['hex'],source_Japanese=a['CP932'],current_stored_English=text,
            record_index=current_index,source_record_index=source_index,speaker='Choice',english=text+'{PAD}',source_meaning=gloss,
            context='Complete Lisbon opening reviewed, including the question and both preparation outcomes.',
            editorial_decision='retain-wording',fresh_retained_wording_justification=reason,localization_note=reason,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)))
    save(CHOICES,{**common,'records':choices,'source_and_current_native_choice_getters':dict(clean=native_clean,current=native_current)})
    decisions = Counter(r['editorial_decision'] for r in records+choices)
    save(ROOT/'source_prose_review_receipt.json',dict(speeches=115,choice_labels=2,decisions=dict(decisions),
        manuscript=str(BATCH),manuscript_sha256=sha(BATCH.read_bytes()),choices=str(CHOICES),choices_sha256=sha(CHOICES.read_bytes()),
        full_clean_Japanese_and_current_exchange_read=True,individual_source_glosses_and_revision_or_retention_reasons=True,
        formatting_approved=False,integrated=False,editorial_completions_added=0,ROM_changed=False,full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print(dict(records=117,decisions=dict(decisions),formatting=False,integrated=False))
