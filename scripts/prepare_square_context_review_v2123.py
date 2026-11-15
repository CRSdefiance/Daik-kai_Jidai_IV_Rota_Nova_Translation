"""Fresh whole-exchange Square review against clean Japanese, with four revisions."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/square_context_review_v2123')
DOC=Path('translations/square_contextual_editorial_manuscript_v1.json')
TEXT={698:"Everyone's after the trading rights in West Africa. The region produces ivory and gold, after all...",701:"Don't blame others for your misfortune. It's all the result of karma from a past life.",718:"Admiral Hayreddin took his name from the man he called his father. The man was so great, the Ottomans made him Sultan of Algiers!",740:"Really? I owe you one! Let's bring new trends to towns all over the world!"}
NOTES={
656:'The complete retail-only response naturally explains the merchant\'s limitation without inventing a refusal to sell one particular good.',
657:'The sailor question leads naturally into the recommendation to use the trade house for bulk business. Retain both the familiar question and the specific alternative venue.',
658:'All right renders the modest bochibochi assessment, then hoping a good deal comes along preserves the wistful commercial wish. The conversational answer sounds natural after the business inquiry.',
659:'The concise confirmation is a natural spoken question with an implied subject. It preserves handing out the goods without charge, without adding recipients absent from this voice variant.',
660:'You\'d like and correct? preserve the more deferential confirmation of the same free-distribution choice. Do not flatten it into the blunt variant.',
661:'As samples preserves this voice\'s stated purpose, rather than adding the residents or another unspoken recipient. The concise confirmation is natural within the distribution choice.',
662:'For nothing, then? preserves the rougher speaker\'s blunt confirmation without gratuitous insults. The subject is the goods selected for distribution.',
663:'The townspeople and free distribution are both explicit; the final then? preserves the older speaker\'s confirming tone without an invented family address.',
664:'The townspeople, free gift and conversational right? preserve the youthful casual voice and the decision being confirmed.',
665:'Free samples and then? preserve both the sample purpose and the more formal confirming register. No identity or title is assigned from the voice index alone.',
666:'The invitation and separate No charge today! preserve the lively distribution pitch and its limited present occasion. Free sample is idiomatic.',
667:'Everyone, please and don\'t be shy preserve the dignified public invitation and reassurance that taking a free sample is welcome.',
668:'Come take a look! and just for you! retain the energetic hawker\'s attention-getting and special-offer effect. Free samples states what the scene is offering.',
669:'Please try one! is a natural gentle invitation, and the second sentence explains that it is a sample. Free is supported by this zero-price distribution exchange.',
670:'Try this! followed by the free offer and take one keeps the rough friendly public pitch brisk and direct.',
671:'Here, give this a try! and free right now preserve the older speaker\'s warm invitation, sample purpose and present offer without inventing a kinship address.',
672:'Free samples here! and Now is your chance retain the sing-song hawker\'s drawing attention and immediate opportunity to try the goods. The free condition belongs to the native distribution exchange.',
673:'Please take one and Free samples available now retain the polite older-register public invitation, sample nature and current opportunity.',
674:'Free? Then I\'ll try it! naturally answers the announcement with surprise and willingness to sample. It preserves the exchange\'s reason for the response.',
675:'The direct invitation, supplied product and emphatic quality claim preserve the hawker\'s sales pitch. Keep the runtime product substitution exactly once.',
676:'Delicious dishes naturally conveys the proposed excellent tastes made with the goods. Ma\'am is an idiomatic address to the woman being hailed, without inventing a spouse relationship.',
677:'The fashions and decor, predicted social attention and playful challenge all remain. Fancy yourself a lady or gentleman? preserves the sales patter rather than asserting the listener\'s rank.',
678:'The aroma and flavor lead into the promise of relief from everyday fatigue. Perk you right up preserves that effect in natural sales language, followed by the repeated invitation.',
679:'The lecture pitch preserves the crowded age of new inventions and industries, its claimed value and the warning about missing profit through delay. Worth your time is idiomatic.',
680:'The cure-all claim remains deliberate hawker hyperbole; Humor me and give it a try conveys the idiomatic request to take a chance on the sample. Do not sanitize the fictional sales claim.',
681:'The interested hesitation leads to checking the supplied good and trying to sell it around the supplied town. Keep both substitutions in order and the exploratory rather than guaranteed-profit intent.',
682:'The merchant treats war as more urgent than ordinary business and wishes for peace soon. Least of my worries naturally preserves the shift in concern.',
683:'People collapsing in an epidemic leads to the offended challenge to the business question. Retain the anger and immediate health situation.',
684:'Food comes first preserves the correction of priorities, and the second sentence gives the original survival reason in ordinary speech.',
685:'Just look around! and I can\'t stop smiling preserve the prosperous merchant\'s delighted answer without inventing an exact profit figure.',
686:'Don\'t ask and the rhetorical question preserve the exasperated inability to conduct business under the current conditions.',
687:'The ship on the regular route and everyone\'s difficulty are both preserved. In a bind gives the social consequence without inventing cargo or casualties.',
688:'Retain the source\'s union of England, Scotland and Wales, optimistic future and cheer for the Queen. Do not silently substitute a modern constitutional or geographic account.',
689:'The recent independence from Spain and preceding long war remain clear in a natural explanatory sentence. Preserve the game\'s temporal viewpoint.',
690:'The League\'s former dominance leads into its diminished position after the route to India and the New World were discovered. Faded naturally preserves the declining influence.',
691:'The Kalmar Union and its Denmark/Norway members remain explicit, along with Sweden\'s recent independence from it. No extra political detail is added.',
692:'The opening question and until recently retain the retrospective regret about Portugal\'s former maritime dominance.',
693:'The question about Spain\'s prosperity leads into the reported empire epithet. Keep the rhetorical question and the saying attributed to other nations.',
694:'Lost their hold on eastern trade naturally conveys the Italian city-states\' lost commercial position after the India route opened. Genoa and Venice remain the examples.',
695:'The occupation and claim about the churches becoming mosques are the source speaker\'s account. Retain the game\'s stated claim without adding historical corrections or stronger moral language.',
696:'Both the former Constantinople name and the source\'s Eastern Roman/Byzantine capital description remain. This is an in-world historical explanation, not an added modern history lesson.',
697:'The cities under Ottoman rule lead into the pirates\' apparent deference to the Sultan. Seem to preserves the source qualification, rather than asserting a command relationship as proven.',
698:'Revise the stiff everyone seeks ... because construction to conversational competition for trading rights, followed by the ivory-and-gold explanation. Preserve the region, commodities, commercial motive and trailing reflective tone.',
699:'Muslim powers preserves the religious-political grouping and former control of regional trade without inventing a specific dynasty or state.',
700:'Infidel and the refusal to continue talking retain the speaker\'s deliberate religious hostility. Do not soften it into a neutral traveler greeting or add a punishment.',
701:'Revise karma in your past life to the result of karma from a past life. The speaker\'s moral instruction still links present misfortune to past-life karma, preserving the cultural concept and causal direction in natural English.',
702:'The former submission of nearby kingdoms and the Ming Empire\'s vanished glory remain explicit. Bowed to and not a trace convey the contrast naturally.',
703:'The Majapahit kingdom\'s former regional power and fall under pressure from Muslim powers remain, without inventing a particular campaign or conqueror.',
704:'The former prosperity, present eunuch domination and worsening government disorder build into the speaker\'s dismay. Keep that progression and the final judgment.',
705:'Yi Seong-gye, founder status, unified nation and approximate two-century interval are all retained. Do not insert a modern date or replace the game\'s time reference.',
706:'The long warring-states era and imminent end are preserved by finally ending. It remains an observation about the era, without an invented named victor.',
707:'Did you know? and pirates from all over Europe preserve the conversational introduction and broad European origin of Caribbean piracy.',
708:'The source explicitly calls Cortes an admiral and says the conquest was followed by many conquistadors arriving. Retain those in-world facts and approved spelling without adding an unsolicited historical correction.',
709:'The former pirate, naval admiral role and Queen\'s knighthood are retained as hearsay. Knighted idiomatically conveys receiving Sir; no inherited nobility is invented.',
710:'Even young women and Times certainly have changed! preserve the speaker\'s surprise at women entering maritime trade. This is the speaker\'s attitude, not an added authorial judgment.',
711:'Respect for Speyer\'s effort leads into the wish for more realism. Retain both sides and the regretful trailing thought, rather than turning it into an insult.',
712:'The new Swedish naval fleet\'s self-sufficiency motto and operating funds from trade and privateering remain hearsay. Privateering preserves the source distinction from generic piracy.',
713:'The distinguished ancestor, Portuguese command and Indian Ocean remain clearly attached to the earlier man. They say preserves the report rather than asserting an unverified personal memory.',
714:'Formidable ships expresses the heavy strength of the Spanish navy\'s fleet composition that motivates the Invincible Armada epithet. Valdes\'s command and the nickname remain explicit.',
715:'Former wide commercial reach leads into the cocky Mediterranean image. As if the sea belonged to the company conveys the source attitude without inventing sovereignty.',
716:'Still rich in profitable trade goods preserves the continuing advantage attributed to Athens. As always retains the familiar emphasis.',
717:'The short complete statement preserves Ottoman control of the eastern Mediterranean in the merchant\'s matter-of-fact voice.',
718:'Revise the unsupported father-in-law narrowing. The clean term giri-no-chichi admits several non-birth paternal ties, and the searched clean routes establish no spouse or adoption detail. The man he called his father preserves the recognized paternal relationship without choosing marriage, adoption or upbringing. Keep inherited name and Ottoman appointment attached to that earlier man; the original admiring merchant tone remains.',
719:'The miser complaint retains Silveira\'s much greater wealth relative to the speaker and peers, the emphatic cheapness and the exasperated close.',
720:'Countless crimes lead to the community\'s fearful deliberate silence. The rhetorical question keeps the unspecified consequences of defiance unspecified.',
721:'More than hold his own preserves the equal-or-better military comparison with Europe. Keep the speaker\'s confidence and mark Arab royalty as rumor.',
722:'Sit back as money rolls in naturally conveys the source idiom of effortless comfort. The envious response remains without an invented income amount.',
723:'The tough patriotic characterization and mercilessness toward outsiders remain distinct. Outside his circle naturally conveys everyone other than his own associates.',
724:'Stop at nothing preserves ruthless commercial methods, followed by the sudden confidential aside asking that the source be concealed.',
725:'The speaker rejects the prejudice about a female ruler and wishes the admiral who routs Japanese pirates ruled the country. Both descriptions refer to the same woman; no extra identity or relationship is inserted.',
726:'Whether Hideyoshi or Kurushima and every time preserve the defiant willingness to drive either opponent away, without inventing an achieved battle result.',
727:'The defeat by Nobunaga precedes Kurushima\'s fascination with ironclads. Obsessed preserves the emphatic fixation and They say marks hearsay.',
728:'Can\'t resist gold or anything that glitters naturally preserves Maldonado\'s weakness for shiny valuables. No particular treasure is invented.',
729:'Keep both Mexico and Peru, the expected future appointment and I hear. The appointment remains a rumor about the future, not a promotion already completed.',
730:'Something in the supplied category market preserves the prediction that one of its goods will become fashionable. Keep the full runtime category substitution and future trend rather than narrowing it to a specific product.',
731:'I think and will sell well preserve the speaker\'s opinion about the supplied good. The substitution is unchanged and no guaranteed windfall is added.',
732:'Looks like and a while yet preserve the tentative forecast that the current trend will continue.',
733:'The wondering question preserves uncertainty about the supplied good\'s craze ending soon. Die down is natural for a fad losing momentum.',
734:'The need to make money before the fad fades leads into being busy. Retain both the commercial urgency and the flustered aside.',
735:'The grateful statement credits the player and predicts everyone\'s recovery. Future will recover preserves the original result being anticipated, without a new medical mechanic.',
736:'With this introduces the relief supplied, followed by avoidance of starvation. The explicit serious consequence remains and is not reduced to mere hunger.',
737:'Shouldn\'t have to worry ... anymore preserves relief from stock shortages and the source\'s qualified future expectation.',
738:'The hearty thanks leads directly into getting to work. Straight to work preserves the immediate intent and brisk merchant voice.',
739:'Hey, sailor! introduces the favor naturally. The request retains the square in another town and the fact that any other town will do; it adds no destination or reward.',
740:'Revise fashion to new trends because the exchange concerns spreading commodity trends and is not restricted to clothes. Keep the delighted acceptance, debt of gratitude and expansive call to bring those trends to towns around the world.',
741:'I see acknowledges the refusal, then the complete apology preserves the merchant\'s courtesy. Imposing on you naturally conveys having made an unreasonable request.',
742:'The urgent request for the supplied item leads into the proposed local specialty made possible by it. Both item and commodity substitutions remain in original order; no purchase price or guarantee is invented.',
743:'The surprised confirmation builds into emphatic praise of the player\'s kindness. You\'re the best! preserves the exuberance without inventing a relationship.',
744:'The refusal response turns into a direct miser accusation. Retain the merchant\'s sting and humor rather than making it politely neutral.'}
if __name__=='__main__':
 assert not ROOT.exists()and not DOC.exists();ROOT.mkdir(parents=True)
 packet=read('work/analysis/market_context_source_v2108/market656_764_clean_current_context_catalog.json');catalog={r['message_ID']:r for r in packet['records']};originals={}
 for name in ('shop_town_editorial','shop_business_editorial','giveaway_editorial','product_pitches_editorial','country_editorial','regional_rumors','town_events_release','town_responses','category_dialogue','specialty_question'):
  p=Path('translations')/(name+'_manuscript_v1.json')
  for r in read(p)['records']:
   if r.get('message_id')in range(656,745):originals[r['message_id']]=(p,r)
 assert set(NOTES)==set(originals)==set(range(656,745))
 records=[]
 for n in range(656,745):
  p,old=originals[n];r=deepcopy(catalog[n]);gloss=old['source_meaning']
  if n==718:gloss='Admiral Hayreddin inherited the name of his giri-no-chichi, a father through a non-birth tie whose exact type is not specified here. That earlier man was so distinguished that the Ottomans appointed him Sultan, or king, of Algiers.'
  if n==740:gloss='Delighted acceptance and gratitude for passage; a rousing call to carry the fresh breath of new trends to towns around the world. The trend is not restricted to clothing fashions.'
  english=TEXT.get(n,' '.join(r['current_stored_English'].split()))+'{PAD}'
  r.update(id=f'COMMON_MESSAGE_{n}',message_id=n,japanese=r['clean_Japanese'],english=english,speaker=old['speaker'],context=old['context'],source_meaning=gloss,localization_note=NOTES[n],editorial_decision='revise'if n in TEXT else'retain-wording',previous_manuscript=str(p),previous_manuscript_sha256=sha(p.read_bytes()),review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status='fresh-source-context-prose-reviewed-native-and-representative-actual-release-pending')
  if n not in TEXT:r['fresh_retained_wording_justification']=NOTES[n]
  records.append(r)
 doc=dict(format='dk4-common-entry-manuscript-v1',translation_policy='natural-dialogue-v2',encoder='dialogue-fixed-v1',target_locale='en-US',file_path='/COMMON/MESFILE.DK4',review_gates=['source','context','localization','naturalness','formatting'],source_ROM_sha256=packet['source_ROM_sha256'],current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],source_COMMON_sha256=packet['source_COMMON_sha256'],current_COMMON_sha256=packet['current_COMMON_sha256'],current_ARM9_sha256=packet['current_ARM9_sha256'],records=records,revised_IDs=sorted(TEXT),retained_count=85,formatting_review_pending=True,conversation_groups=[dict(name='Retail referral and conditional business responses',IDs=[656,657,658,*range(682,688)],flow='Shop selection -> retail limitation or bulk-trade referral; business inquiry selects exactly one current-state response.'),dict(name='Free distribution confirmations, announcements and customer answer',IDs=list(range(659,675)),flow='Distribution choice -> one adviser confirmation -> acceptance -> one public announcement -> customer willingness. Voice alternatives are not consecutive speakers.'),dict(name='Commodity demonstrations and interested merchant response',IDs=list(range(675,682)),flow='Selected good and category determine one pitch; follow-up retains the good and proposed market town.'),dict(name='Independent regional history and rivalry replies',IDs=list(range(688,730)),flow='Original town-share/region selector chooses country account or rival rumor. Each is one complete answer to the inquiry, not a long consecutive speech by one person.'),dict(name='Trend forecasts and town relief replies',IDs=list(range(730,739)),flow='Specific trend state or supplied relief selects the applicable forecast or grateful result; do not concatenate independent alternatives.'),dict(name='Passage request and answer',IDs=[739,740,741],flow='Trend-spreader asks for passage to another town square; accept leads gratitude and mission, refuse leads courteous apology.'),dict(name='Local-specialty item request and answer',IDs=[742,743,744],flow='Merchant requests the required item to create a supplied local specialty; accept leads exuberant thanks, refuse leads the miser complaint.')],neighbor_context_IDs=[655,745,746],no_new_review_or_completion_credit_until_ledger_reconciliation=True,all_native_formatting_revised_ROM_and_release_checks_pending=True,full_goal_complete=False)
 # Formatting remains false until consumer and native page checks pass.
 save(DOC,doc);save(ROOT/'source_context_review.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),revised_IDs=sorted(TEXT),retained_count=85,all89_clean_source_and_current_refs_present=True,relationship718_specific_marriage_or_adoption_not_proven=True,lexical_reference=dict(title='Shogakukan Digital Daijisen: gifu',url='https://kotobank.jp/word/%E7%BE%A9%E7%88%B6-475463',scope='Dictionary supports multiple non-birth paternal ties; it does not identify the game character\'s specific tie.'),full_goal_complete=False))
 print(dict(fresh_reviewed=89,revisions=sorted(TEXT),justified_retentions=85,formatting_and_integration_pending=True))
