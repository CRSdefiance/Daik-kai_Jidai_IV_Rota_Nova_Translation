"""Author complete source-first logical dialogue; comparison and display remain pending."""
from copy import deepcopy
from pathlib import Path
import re
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_hodram_B231_B250_scope_v1 import ROOT

MEANINGS=ROOT/'all225_clean_meanings_before_English.json'
OUT=Path('translations/hodram_B231_B250_clean_drafts_v1.json')
TEXT={
231:{5:"Admiral, got a minute?",9:"What is it?",13:"I just heard about an animal called an armadillo. Do you know it? They say its hide is harder than iron.",17:"And?",21:"Well, apparently someone once made a shield from its hide. They called it the Armadillo Hide.",24:"What about this shield?",28:"Oh, come on! It's harder than iron! Don't you want it? A shield like that would really help in a fight.",31:"True. Where can we find it?",34:"Well... all I know is that it's hidden somewhere in Africa.",38:"That's not much to go on.",42:"I know, but...",46:"Don't look so disappointed. I'll keep it in mind. We may find it if we're lucky.",49:"Yeah."},
232:{5:"Admiral, got a minute?",9:"What is it?",13:"I just heard about something called a giant tortoise. Do you know it? They say its shell is harder than iron.",16:"And?",20:"Well, apparently someone made a shield from its shell. Everyone called it the Giant Tortoise Shield.",23:"Hm? This sounds familiar... Didn't you tell me something like this about an armadillo?",27:"Did I? I don't remember.",31:"Never mind. What about this shield?",34:"Don't you want it? A shield like that would really help in a fight.",38:"You said exactly the same thing about that armadillo.",41:"Did I? Well, never mind that!",45:"...Where can we find it?",48:"All I know is that it's hidden somewhere around the Indian Ocean.",51:"That's not much to go on.",55:"...I know, but...",59:"Don't look so disappointed. I'll keep it in mind. We may find it if we're lucky.",62:"Yeah."},
233:{5:"Admiral, got a minute?",9:"What is it?",13:"Do you think phoenixes really exist, Admiral?",17:"I don't know. If they do, I'd like to see one. What brought this on?",21:"I heard there's a helmet made of iron forged in a phoenix's flames. A Phoenix Bascinet, I think they called it.",24:"Let me guess. You want us to get it because it would help in a fight?",27:"Wow! How did you know?",31:"You've made similar suggestions before.",34:"Have I? You've got a good memory.",38:"Where is it, then? Don't tell me it's somewhere in Africa or India again.",42:"Of course not! It's in Britain.",46:"Oh... you've narrowed it down quite a bit this time.",49:"That's right! I did some research myself. At first, all I knew was that it was somewhere in northern Europe.",53:"I see. Well done.",57:"Heh heh. Thanks.",61:"All right. In recognition of your efforts, Samwell, I'll keep this Phoenix Bascinet in mind.",65:"Great! I hope we find it!"},
234:{5:"Admiral, have you heard of Herophilus?",9:"No, I haven't. What about him?",12:"He was a physician long ago. He left us the world's oldest medical text.",16:"Oh?",20:"They say it describes ways to keep the sailors from tiring so quickly...",24:"Oh... a remarkable book. If that's true, I'd certainly like to have it.",27:"So would I.",31:"But how would we find it? Do you have any leads?",35:"Well... it was a long time ago, but I seem to recall hearing that someone had seen it in the far reaches of the Mediterranean.",39:"Anything else?",43:"...That's all.",47:"I see. That's not much to go on.",50:"I'm sorry.",54:"There's no need to apologize.",58:"Yes...",62:"So if we want it, we'll have to go looking in the Mediterranean."},
236:{5:"Admiral, may I have a moment?",8:"Hm?",12:"Well, I found an interesting scrap of writing in the library at Alexandria the other day.",16:"A scrap of writing?",20:"It described a mysterious chisel said to have been used by Phidias, the legendary sculptor of ancient Greece.",23:"A chisel, eh?",27:"Yes. His soul is said to have entered it after his death. Anyone who uses it is believed to gain a miraculous gift for sculpting.",30:"It's supposed to be buried somewhere on the Balkan Peninsula, near Greece. Unfortunately, the writing gave no precise location.",33:"Manuel... are you hoping to use this chisel for ship repairs?",37:"Why not? They say the Romans had a policy of using even kings as tools. Now that's an extravagant tool!",40:"A ship is a fine work of art, too. And the finer the tools, the better. If you get the chance, do look for it."},
238:{27:"I am currently in West Africa. I heard a strange account from some sailors here and thought I should pass it along.",31:"Recently, a Spanish merchant convoy was attacked by pirates on its way from the New World to West Africa.",35:"The merchants were badly outmatched and tried to flee, but their ships were slower. It seemed only a matter of time before the entire convoy was destroyed.",38:"Yet when they reached the waters far west of Lisbon, they reportedly heard an unearthly roar.",41:"For some reason, the sound roused the sailors. They fought like lions and held their own against the pirates.",44:"They held out until the Spanish navy happened to pass by. The pirates scattered and fled, and the merchant convoy escaped the danger.",47:"The sound has yet to be identified. Whether it was a natural phenomenon with a scientific explanation remains unclear.",50:"It is certainly an intriguing account. You may find it worth investigating. Charles Jean Rochefort.",57:"It sounds rather dubious... but I'm interested in how it roused the sailors."},
239:{27:"Hey, Admiral! How are you and everyone doing?",30:"India's an amazing place! I couldn't begin to explain it all... Oh, right! I heard an interesting rumor.",33:"It's about a statue of a sacred beast, made during the Gupta dynasty. Apparently, it can see the future.",36:"Sounds fishy, right? But this is India! Nothing would surprise me here. Maybe it's true.",39:"I thought that with this thing, I might even beat Fernando at gambling. Or is that wishful thinking?",42:"Trouble is, I can't find it for sale anywhere. I haven't even met anyone who's seen it.",46:"Admiral, why not look for it if you've got some time? Even if you don't use it for gambling, it could come in handy!",49:"Whoops, nearly time to sail! Hope you find that treasure. See you! Jam Jack Ludwyan.",64:"Ha! He'll need another five hundred years to stand a chance against me, even with that thing!",70:"Heh. Must he write his letters just as he speaks? Still, he did take the trouble to send a report. We may as well investigate."},
240:{5:"Hmph! What are those men talking about?!",8:"What's wrong, Cesare? Why are you so angry?",11:"The sailors are chattering away about utter nonsense!",14:"What nonsense?",18:"Instead of working! An arrow that pierces demons, indeed! Oh, that's the name of the item: the Demon-Piercing Arrow. Such a grand name!",21:"I'm not following you... What is this Demon-Piercing Arrow?",24:"It's a legendary arrow said to have been used by an angel to slay a demon, yes indeed.",28:"They say it makes its bearer a brilliant archer. The men are wondering whether it works with cannon, too, instead of maintaining the ship!",31:"They'd be far better off practicing their cannon fire than wasting time on such talk!",35:"As if something so useful would be lying around Britain! Yet they say it's on Skye, or that someone saw it on Lewis...",38:"They get so excited over these silly rumors! If it were so close, surely someone would have found it by now!",41:"... (There's no point saying anything to him right now.)",44:"Those men are always like this! Grumble... grumble..."},
241:{5:"Ow! ...Ow, ow, ow...",9:"Janus? What happened?",12:"Oh, it's nothing serious. I caught my hand on a mast fitting while doing some maintenance.",16:"Hey there. What's wrong?",19:"Well... you see...",23:"One of my navigators seems to have injured his hand.",26:"That's no good. Here, let me have a look.",29:"...Ow.",33:"Hmm. Comes with being a sailor, a cut like that.",36:"Heh heh. I've got some good gloves that'll keep that from happening.",40:"Gloves?",44:"You bet! You won't find gloves this handy just anywhere. Now, give me a moment... Where'd I put them?",47:"Oh, no! Don't tell me I dropped them somewhere!",50:"That's no help at all.",54:"Ah, sorry. If I did drop them... Oh, that's right! It was somewhere around Denmark!",58:"Denmark?",62:"That's right! The Jutland Peninsula, no doubt about it! It's true! You've got to believe me!",66:"All right. We'll look for them.",70:"You believe me? Good! If you find them, they're yours.",74:"They don't fit my hands, so I was going to sell them anyway. But I can vouch for how well they work!"},
242:{6:"Oh, welcome!",10:"Oh! That ornament you're carrying... May I see it?",14:"This?",18:"I knew it! Where did you find this?",21:"Some thug called Gabriel had it...",24:"It's mine! It was my treasure, but someone stole it a while ago...",28:"Dad bought it for my birthday because I love roses. It was so precious to me.",32:"I see. Then it's found its way back to its rightful owner.",36:"You handed over the Frozen Rose.",45:"Thank you! I'd given up hope. I never thought I'd hold it again!",49:"I must give you something to thank you...",53:"The guild already paid me for catching Gabriel. That's reward enough.",57:"{MACRO:FI}...!",61:"Goodbye, then.",72:"Oh, wait!",76:"You and your crew explore the world, don't you?",79:"Have you been to the church outside town? It's made of wood, which is unusual in Europe.",84:"Overlooking what's right under my nose... I hadn't thought of it. I'll pay it a visit.",93:"Thank you so much! Come again, won't you?"},
243:{6:"Admiral!",10:"What is it?",14:"Look at this! What a magnificent figurehead!",17:"Well done finding it.",21:"Oh, Father!",25:"It has a regal air... Is there a story behind it?",29:"No particular history. But...",32:"But?",36:"Only someone the figurehead itself takes a liking to can carry it away.",40:"People have tried taking it, but most leave empty-handed and injured.",44:"And when someone who has taken it dies, it somehow returns to this church.",48:"Oh...?",52:"Would you like to try?",56:"Ha! No, thank you! I want nothing to do with something so strange. Right, Admiral?",60:"Hmm...",64:"You're not considering it, are you, Admiral?!",79:"All right. Everyone, give me a hand!",83:"I'm telling you, don't do it!",87:"You can head back ahead of us, if you like.",91:"I'll help! That's what you want, isn't it? Honestly!",95:"Heave! Heave! Heave!",114:"Whoa!",126:"Run!",133:"It seems you were not worthy of it.",137:"Ow, ow, ow...",143:"It seems the figurehead has accepted you.",146:"We were just lucky.",150:"There's no need to be modest.",154:"No... I can't think of any other explanation. I believe we were simply lucky.",158:"In any case, I'm glad for you. May God bless you.",163:"{MACRO:FI}'s Spirit increased by 1!",174:"A wise decision.",178:"That's right! For a moment, I thought you were going to suggest taking it!",182:"May God bless you."},
244:{6:"Oh, you've come to see me again!",10:"Have you ever seen gold dust?",14:"?",18:"A sailor who went to the New World told me about a river there with gold dust flowing through it.",22:"Doesn't it sound romantic, just picturing it?"},
245:{7:"Why, {MACRO:FI}!",11:"Are you interested in ancient civilizations, too? There are ruins right here in town.",14:"You didn't know? They're very close. See that hill over there? That's where they are."},
246:{7:"Have you been to the pyramids yet?",11:"No.",15:"Since you're here, you really must see them at least once. I'll tell you how to get there. Go on, take a look!",18:"I see. I'll keep that in mind."},
247:{6:"Welcome, {MACRO:FI}. Another lovely day, isn't it?",10:"Oh, have you visited the ruins near town? Some say they were once King Solomon's treasury.",13:"Oh?",17:"It's perfect picnic weather today. Why not take a little trip?"},
248:{5:"I'd like you to take on a job.",9:"There's a village called Rio de Janeiro, far to the west across the Atlantic from here. I'd like you to take a survey party there.",12:"A survey party?",16:"You can carry them as sailors. When you stop by the tavern, hire a few more sailors than usual.",20:"Across the Atlantic... in the southern part of the New World, then. That's quite a distance.",24:"That's precisely why I'm asking you.",28:"The survey will need funding, too, so take a little extra money with you."},
249:{12:"If I remember correctly... Rio de Janeiro is in the southern part of the New World.",18:"How's the survey of Rio de Janeiro coming along? It's far to the west, across the Atlantic from here."},
250:{5:"Thank you. Here are your expenses and your reward. Take them.",10:"You received 42,000 gold coins.",34:"Your market share in Sofala increased slightly!",52:"Have you ever visited the ruins near town?",55:"Legend has it they were once King Solomon's treasury. You should take a look."}}

STYLE={0:"Admiral, there's a letter from {author} for you.",1:"Admiral, a letter from {author} has been delivered.",
2:"Admiral, you've got a letter from {author}.",3:"There's a letter for you from {author}, Admiral.",
4:"Got a letter from {author} for you, Admiral.",5:"A letter has come for you from {author}, Admiral.",
6:"Admiral! A letter from {author} came for you!"}
NOTES={
(231,21):'Use the existing Armadillo Hide item label; its iron-hard quality is explicitly preserved in both surrounding speeches. Flag the shorter catalogue label for scoped term review.',
(232,23):'Keep the hesitant callback to the earlier armadillo pitch rather than supplying the exact item title the admiral cannot recall.',
(232,38):'The repeated sales pitch is the joke; the admiral now confirms his suspicion.',
(233,24):'Turn the admiral’s accurate prediction into a dry, natural rhetorical question.',
(233,46):'An initial pause conveys his surprise without an awkward literal syllable stutter.',
(234,12):'Retain the character’s historical claim, without adding a claim that the book survives or externally endorsing the claim.',
(234,35):'Keep all three limits: an old memory, secondhand report, and vague location.',
(236,37):'Preserve the reported Roman policy and Manuel’s joke taking the tool metaphor literally; do not add a toolbox or a new political explanation.',
(238,35):'Fighting strength is overwhelmingly different; do not invent a numerical disadvantage. Correct the provisional context word outnumbered to outmatched.',
(238,50):'Preserve the full signature using the previously reviewed Charles Jean Rochefort form; ordinary line breaks remain the formatter’s job.',
(239,36):'Keep Jam’s exuberant period perspective as his own speech, including uncertainty; do not turn it into narrator-level cultural fact.',
(239,49):'Use the previously reviewed full form Jam Jack Ludwyan in the signature, with the casual farewell intact.',
(239,64):'Keep the five-hundred-year boast while expressing the too-early idiom as natural American hyperbole.',
(239,70):'Express the criticism as spoken style carried into writing, preserving its contrast with Jam’s deliberately casual letter.',
(240,18):'Retain the mid-rant clarification that the grand phrase is the item’s name; use the bound Demon-Piercing Arrow form.',
(240,35):'Keep Cesare’s skepticism and both specific island rumors; do not declare the item nonexistent or replace Britain with a narrower place.',
(240,41):'Keep the inner thought in parentheses, following the source pause; it is not a spoken attempt to stop the rant.',
(241,16):'Localize the familiar address without inventing brotherhood, age or a rank.',
(241,74):'Keep both the poor personal fit and the intended sale, without inventing a price or charging the party.',
(242,28):'Dad is supported by the explicit father/daughter source statement; preserve the birthday purchase and love of roses.',
(242,32):'Use a warm declaration of reunion before the source’s separate physical handover notice.',
(242,53):'The refusal is restrained and courteous: the guild has already paid for Gabriel’s capture.',
(242,57):'Keep the flustered name-only response and FI substitution; do not add a new title or romantic declaration.',
(242,84):'Localize the lantern-base-dark idiom as overlooking what is right under one’s nose.',
(243,21):'Father is the source’s conventional clerical address, not a new biological relationship.',
(243,133):'Keep the priest’s assessment within the failed attempt branch; it does not describe the successful or refused outcomes.',
(243,163):'Use Spirit for the permanent attribute, distinct from the current Mood condition; keep FI and the exact one-point increase.',
(244,10):'Use gold dust for the alluvial grains of gold; preserve the material rather than merely describing sand as gold-colored.',
(248,9):'Preserve the source’s village designation and westward Atlantic clue; do not import modern Rio geography or new sailing directions.',
(250,10):'Keep the exact 42,000-coin award with American thousands punctuation.',
(250,34):'Preserve the slight but unspecified market-share gain and source port name; do not invent a numeric percentage.'}

def main():
    assert not OUT.exists();source=load(MEANINGS);rows=[]
    for original in source['records']:
        row=deepcopy(original)
        if row.get('kind')=='typed-choice-label':
            english=["Let's try it.","Let's leave it."][row['source_index']]
            note='Keep the figurehead choice as a natural complete invitation or refusal; preserve the original two source indices.'
        elif row.get('kind')=='actor-style-alternative':
            author='Charles' if row['block']==238 else 'Jam';voice=row['source_style_indices'][0]
            english=STYLE[voice].format(author=author)
            note='Preserve this physical alternative and its original aliases; '+row['personality_voice_notes'][0]['register']
        else:
            index=row['source_reference']['record_index'];english=TEXT[row['block']][index]
            note=NOTES.get((row['block'],index),'Preserve this turn’s intent and its place in the complete exchange; '+{
                1:'Hodram stays concise, restrained and direct.',22:'Samwell stays eager and informal without forced baby talk.',
                19:'Carlo stays politely informative and then apologetic.',23:'Manuel stays affable and gently amused.',
                18:'Charles uses measured, educated letter prose.',11:'Jam keeps his casual spoken rhythm in his letter.',
                20:'Fernando’s boast remains brash.',13:'Cesare’s exaggerated formal indignation stays comic.',
                4:'Janus sounds mildly embarrassed and hurt.',113:'The port worker is friendly, colloquial and emphatic.',
                186:'Francisca sounds warm and increasingly moved.',6:'Julio is expressive, apprehensive and gruffly familiar.',
                139:'The priest is calm and politely formal.',188:'The local woman sounds curious and warmly romantic.',
                193:'The local woman sounds welcoming and helpfully conversational.',195:'The local woman’s encouragement is warmly insistent.',
                196:'The local woman sounds friendly and inviting.',147:'The guildmaster is practical and conversational.',
                254:'Use a clear native system notice, keeping its exact event or reward.'}[row['source_selector']])
        english.encode('ascii');assert english.strip()==english and '\n' not in english and not any(t in english for t in ['{LB','{PAD','{ALIGN','%'])
        expected=row.get('source_macros',{});actual={m:english.count('{MACRO:'+m+'}') for m in ['FI','FA','FO']}
        assert all(actual[m]==expected.get(m,0) for m in actual),(row['id'],actual,expected)
        row.update(english=english,speaker=('Native system panel' if row.get('source_selector')==254 else
            ('Native companion role '+str(row['source_selector']) if row.get('kind')=='actor-style-alternative' else
            ('Choice caption' if row.get('kind')=='typed-choice-label' else 'Source actor '+str(row['source_selector'])))),
            context=row['exchange_context'],localization_note=note,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            clean_first_draft_not_final_comparison_approval=True,current_English_conversation_comparison_pending=True,
            source_names_terms_anddisplay_still_require_scoped_current_binding=True,new_credit=0)
        if row['block']==238:row['context']=row['context'].replace('outnumbered','outmatched')
        if row['id']=='DK4_MES_B239_R0049':
            row['source_meaning']='Jam says it is nearly time to sail, hopes the treasure will be found, says goodbye and signs the full source name ジャム・ジャック・ルドワイヤン.'
        rows.append(row)
    assert len(rows)==225 and sum(r.get('kind')=='actor-style-alternative' for r in rows)==14
    assert sum(r.get('kind')=='typed-choice-label' for r in rows)==2
    sources=[Path('translations/hodram_B211_B230_scoped_names_final_v1.json'),Path('translations/rafael_B321_B342_scoped_names_final_v1.json')]
    save(OUT,dict(translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],records=rows,records_count=225,
        ordinary_drafts=209,physical_style_drafts=14,typed_caption_drafts=2,
        source_meanings=str(MEANINGS),source_meanings_sha256=digest(MEANINGS),
        all225_logical_drafts_written_before_current_story_English_intake_in_this_batch=True,
        prior_reviewed_names_consulted_only_as_scoped_name_references=[str(p) for p in sources],
        no_blanket_claim_of_no_historical_English_exposure=True,source_contexts_corrected_only_for_unsupported_outnumbered_word=True,
        current_English_comparisons=0,current_comparison_name_term_formatting_andrelease_gates_pending=True,
        no_ordinary_manual_breaks_padding_alignment_ornew_story_fact=True,
        all_source_selectors_complete_preambles_macros_andaliases_preserved_in_reference=True,
        excluded_completed_B237_records=18,full_goal_complete=False,new_credit=0,guide_photos=False,
        evidence={str(p):digest(p) for p in (MEANINGS,ROOT/'clean_name_fields.json',*sources,Path(__file__))}))
    print('Saved all 225 clean-first logical drafts; complete-exchange comparison, scoped terms/names and fresh display checks remain.')

if __name__=='__main__':main()
