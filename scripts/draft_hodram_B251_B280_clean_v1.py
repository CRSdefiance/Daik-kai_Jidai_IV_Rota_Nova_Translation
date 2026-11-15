"""Write complete clean-first logical drafts; comparison and display approval remain pending."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.gloss_hodram_B251_B280_clean_v1 import ROOT,OUT as MEANINGS

OUT=Path('translations/hodram_B251_B280_clean_drafts_v1.json')
DRAFT={
251:{5:"What is it, Admiral?",9:"Do you feel anything when you look at this statue? A strange warmth, perhaps...",15:"A statue? Where?",18:"There.",22:"Let me see...",26:"Oh, it's a figurehead! Such intricate craftsmanship! Hmm... Yes, I do sense something from it!",33:"Is it famous?",37:"No, I've never heard of it. Wait... Are you thinking of taking it?",53:"It is a magnificent figurehead. With it on our ship, surely we'd enjoy its blessing. But may we really take it without permission?",56:"It would be sheer folly to leave such a fine figurehead on land. Don't you agree?",60:"How kind of you, Admiral! Well, let's get it moved at once!",64:"I do apologize, figurehead, but would you come with us?",67:"Then I shall watch over you.",70:"W-what was that? Whose voice was that?!",73:"What are you doing? Hurry up and give me a hand.",76:"But I just heard a voice...",80:"Are you half asleep?",85:"{MACRO:FI}'s Luck rose by 1!",89:"Cesare's Luck rose by 1!",92:"?? (Whose voice was that? It was so warm and full of compassion...)",99:"Yes, you're right. (Though it is a little disappointing...)",103:"Shall we head back to town?",110:"Yes, let's. (Such a magnificent statue. Just looking at it seemed to cleanse my heart...)",113:"{MACRO:FI}'s Charm rose by 1!",117:"Cesare's Charm rose by 1!"},
252:{6:"Admiral, over here! There's something written on the wall!",9:"A piece of ice floats in a vessel filled to the brim with water. When the ice melts, what happens to the water level?",12:"If it rises, press the front stone. If it falls, press the left stone. If it stays the same, press the right stone.",31:"This is the answer!",53:"Wrong, then. This place is dangerous. Back to town!",68:"This is the answer!",90:"Wrong, then. This place is dangerous. Back to town!",106:"Melting the ice cannot change the water level.",112:"Hey, the wall's opening...!",116:"?!",120:"Admiral! There's a strange statue here!",123:"Where?",127:"Here. Looks like a figurehead...",130:"Crack! Crack!",134:"W-what the hell?!",138:"Was it you who awakened me?",142:"Waaaah! A-Admiral!",145:"Answer me!",160:"Then I shall let you wield my power!",164:"Huh?",168:"You may take the statue in which my power dwells. Once it is yours, leave this place at once!",174:"...What was that all about? We're not going to get cursed for using this thing, are we?",178:"Who knows? I couldn't tell you, either.",184:"You say I awoke on my own?! You think you can insult me and simply walk away?!",195:"ROOOOAAAR!!",207:"A-Admiral! Let's get out of here!",212:"Everyone, run!",223:"Hah... hah... Whew! That was close!",226:"Huh? Ugh... My body feels so heavy..."},
253:{7:"Oh, {MACRO:FI}! Welcome!",10:"Are you looking for ruins? There are some nearby, too.",13:"I don't usually tell foreigners, but I'll make an exception for you."},
254:{6:"Welcome, {MACRO:FI}.",9:"Oh? You're looking for ruins all over the world? Hmm... There aren't any particularly famous ones in this town."},
255:{6:"Why, {MACRO:FI}.",10:"Oh? You're looking for ruins all over the world? I'm sorry, but there aren't any particularly famous ones in this town."},
256:{5:"I've got a job for you: finding someone. Interested?",9:"I'd like you to find a Dutch nobleman named Yuris Huygens.",12:"He's a noble, but he loves going off on long trips and never comes back to his estate. His people have been complaining.",16:"I've heard he was seen in Syracuse..."},
257:{6:"Ah, there you are! You're Mr. {MACRO:FA}, right? The London guild was looking for you."},
258:{5:"If I remember correctly, this is where I'll find that Yuris fellow.",8:"Ah, the beauty of ancient Roman civilization!",12:"Excuse me. Do you know someone named Yuris around here?",15:"Such strength... Such grace...",19:"...Hey, are you listening?",23:"Yes, I hear you. I'm Yuris.",27:"You are?! Now that you mention it, there is something rather elegant and aristocratic about you...",31:"You can't afford to idle here. Your people are complaining that their lord went away and hasn't come back.",34:"Oh, no! I'd forgotten all about my estate! Please take me back there.",37:"Well, let's return to London first. Then we'll see."},
259:{5:"Ah, Yuris. What have you been doing all this time, forgetting your duties? Your people are in quite a bind.",9:"I'm sorry. When I go on a long trip, I get carried away and lose track of everything... I'll go back at once.",13:"Honestly... Well, you must be tired after the journey. Rest here a while before you go home.",17:"Oh, I nearly forgot. Here's a little something for your trouble. Take it.",21:"Received 11,000 gold coins.",49:"Your market share in London increased slightly!",60:"Oh, excuse me. Looks like a customer.",64:"Hey, are you out of maps?",68:"You people again? Yeah, they're all gone.",71:"What a useless shop.",75:"...",79:"You're the ones who bought them all!",82:"Maps?",86:"Maps to some ruins. A strange bunch has been hanging around there lately, making a nuisance of themselves with the people nearby.",90:"Are the ruins close to here?",94:"They're quite far away, but with a map, they're easy to reach. Trouble is, those people bought every last one.",97:"Other towns might still have some, though.",100:"I see..."},
260:{12:"I must go to Syracuse and find this Yuris.",17:"I've heard Yuris was seen in the square in Syracuse."},
261:{6:"Sir, I've got a favor to ask.",10:"If you come across a fellow named Gabriel Cardocci from Italy, would you bring him back here?",14:"He broke an agreement. Seems he headed for the Caribbean..."},
262:{6:"Come to think of it, the Stockholm guild was looking for a sailor to take on a job."},
263:{12:"I must find this Gabriel. He should be in the Caribbean.",17:"Still haven't found Gabriel? He ought to be in the Caribbean."},
264:{5:"Sir, you really must settle up today. Do you even know how big your tab is?",9:"I told you, I'll pay next time! Have I ever skipped out on a bill?",12:"You've never paid, either.",15:"Is there a man named Gabriel Cardocci in town?",18:"The one and only Gabriel Cardocci! Who the hell are you?",21:"I hear you broke a guild agreement.",25:"S-so what if I did?! It's none of your business!",28:"Enough excuses. You're coming with me to the Stockholm guild.",32:"H-hey, let go!",36:"W-wait! What about his tab?",41:"Admiral, he was hiding this. Looks like it's stolen."},
265:{5:"I've brought Gabriel.",9:"Back at last, are you? Now hand over that money you pocketed behind our backs.",13:"I-I'll pay you next time. I promise...",17:"I heard that excuse at the tavern, too. Well, I'll leave you to it.",21:"Hold on! I can't send you away empty-handed, Mr. {MACRO:FA}. Please, take this.",26:"Received 22,000 gold coins.",49:"Your market share in Stockholm increased slightly!",60:"We'll leave that stolen item with you. If its owner can't be found, you may do as you like with it."},
266:{6:"There's a man I need you to take down. I'm counting on you.",9:"He's a Portuguese named Julian Vermeer, a traitor who sided with Spain against his own country. I hear he's working as some sort of courier in the Mediterranean."},
267:{5:"Well, Julian's been caught at last! Look at the state of you!",8:"D-damn you! Let me go!",12:"Thanks for your hard work. We'll handle the rest. Here, take this.",16:"Received 32,000 gold coins.",41:"Your market share in Sao Jorge increased slightly!",59:"Say, if you want to see the mosque deep in the Sahara, take a map and set out through the city gates."},
268:{12:"Julian's cargo fleet is in the Mediterranean, if I remember correctly.",24:"Hurry up and catch that traitor Julian. I hear he's working as some sort of courier in the Mediterranean."},
269:{6:"The Sao Jorge guild was looking for you."},
270:{6:"Hey, you've got a heart, haven't you?",9:"Someone wants revenge on the English outlaw who killed her father. Lend her a hand, would you?",13:"The outlaw's name is Plett Perrault. You'll do it, won't you?"},
271:{5:"Plett, you bastard! How dare you show your face, you murdering...",8:"H-hey, I'm sorry, all right...?",12:"I don't think saying sorry settles a murder.",15:"Thank you. As for what happens to him, I'll leave that to the daughter who asked us for help.",19:"I never expected you to bring him in alive! You've earned a generous reward. Take it.",23:"Received 35,000 gold coins.",48:"Your market share in Hangzhou increased slightly!",66:"Oh, have you been to the Forbidden City? It's worth seeing at least once. It's a little way from here, though.",69:"Just don't tell the officials you heard about it from me."},
272:{12:"I must deal with that outlaw Plett soon.",25:"Hurry up and catch that outlaw Plett."},
273:{5:"I've got a job for you. I know I can count on you. Bring in a wanted man named Jean Ramusio.",9:"We were after him for smuggling, but he routed the force we sent against him in India.",13:"Seems he's got a fleet to rival a pirate's. Take this seriously. Here's an advance.",23:"Received 15,000 gold coins."},
274:{5:"Ah, the smuggler! Finally caught you, have they?",8:"Everyone says I'm a smuggler, but it's all a misunderstanding. Every last bit of it. I'm the one who's been put out, you know!",11:"You certainly know how to talk. Try thinking about the trouble you cause other people for a change.",15:"Then what am I supposed to do?!",19:"Work honestly. That's all I'm asking. And don't tell me that's what you've been doing all along.",22:"...I can't?",26:"...Sorry you had to put up with him. Here's a little something for your trouble.",30:"Received 75,000 gold coins.",55:"Your market share in Basra increased slightly!",73:"Let me tell you something. There's a mosque far inland from here, with an incredible treasure hidden inside.",76:"They say you have to earn the approval of the king enshrined there to get the treasure. Might be worth a try for someone like you."},
275:{12:"I was to defeat Jean's fleet in India.",17:"It seems Jean is hiding in India."},
276:{5:"Mr. {MACRO:FA}, I've got a favor to ask. I know I can count on you.",8:"What is it?",12:"I want you to catch a wanted man: Jacob Portunto, a Dutch smuggler.",16:"He used to be a petty thug, but apparently he struck it rich in Africa. Now he fancies himself a proper pirate.",19:"Here's an advance. He's more than we can handle, but you should be able to manage him. Do what you can.",28:"Received 16,000 gold coins."},
277:{5:"Ah, you're back.",9:"My cargo...",13:"What are you talking about?! It all belonged to other people in the first place!",16:"I owe you one for catching him. Here's a little something. Take it.",19:"Received 72,000 gold coins.",44:"Your market share in Calicut increased slightly!",62:"I've got some special information for you.",66:"Try setting out on an expedition through the city gates. They say a building out that way has an incredible treasure hidden inside.",77:"Don't forget to get a map before you set out."},
278:{12:"I must find that wanted man Jacob's fleet.",25:"Still haven't found Jacob?"},
279:{5:"Hmm... What am I going to do? I suppose I'll have to ask you...",8:"Please, take down a Spanish pirate named Hernan Berio.",11:"He's been causing trouble for every merchant around here, but mention his name and everyone gets too scared to take the job.",15:"They say he's been prowling the Mediterranean lately. I'm counting on you. Here's an advance.",24:"Received 30,000 gold coins."},
280:{5:"Make way for the great Hernan Berio!",8:"Even tied up, you're still playing king. Unbelievable.",11:"You've finally caught Hernan! I knew asking you was the right choice. Well done! Take this.",14:"Received 110,000 gold coins.",40:"Your market share in Athens increased slightly!",58:"Say, have you been to this town's famous landmark yet?",61:"A landmark?",65:"Well, go and have a look. It's practically the symbol of the town."}}

STYLE={0:"Admiral, the ceiling is collapsing! It's dangerous here!",1:"Admiral, we're in danger! The ceiling is collapsing!",2:"Admiral, this is terrible! The ceiling is collapsing!",3:"Admiral, look out! The ceiling is collapsing! Let's run!",4:"Look out! The ceiling's coming down!",5:"Admiral, the ceiling's coming down! We'd best make a run for it.",6:"Aaaah! The c-ceiling's falling!",7:"The ceiling is collapsing, Admiral. It's dangerous to stay here."}
NOTES={
(251,33):'Ask about renown without inventing an item title that neither speaker knows.',
(251,56):'Preserve the captain’s rationalization about a figurehead left on land, letting Cesare’s exaggerated praise carry the joke.',
(251,64):'The ceremonious address to an object is intentional personification; do not add a gender, divine name or title.',
(251,67):'This is a compassionate in-world voice through the FE consumer, not a neutral system notification.',
(251,92):'Keep the spoken puzzle and private thought distinct with the original parenthetical function; do not state that Hodram heard the voice.',
(251,99):'This belongs to the leave-it branch; retain the contrast between spoken agreement and private disappointment.',
(251,110):'Retain the cleansing-heart impression as Cesare’s thought, without identifying the statue’s religion.',
(252,9):'Preserve the singular floating ice and vessel filled to the brim. This is a wall inscription, not explanatory narration or an added hint.',
(252,12):'Keep rises/front, falls/left, unchanged/right exactly; the preceding inscription supplies the pronoun’s water-level antecedent.',
(252,138):'Use a commanding, formal supernatural voice without gratuitous thou/thee syntax.',
(252,168):'Preserve permission to take the statue and the order to leave after taking it; do not imply prior ownership.',
(252,174):'The curse is Fernando’s anxious question, not a confirmed narrator diagnosis.',
(252,226):'Describe physical heaviness only; do not invent paralysis, a named curse or a changed statistic.',
(253,13):'Retain the explicit foreigner distinction as the hostess’s usual practice and her friendly exception.',
(256,9):'Use the existing Yuris Huygens spelling from scoped name metadata; full native/public name qualification still follows.',
(258,15):'Keep the aesthetic strength/grace contrast as deliberate distraction in the complete exchange.',
(258,31):'Keep his responsibilities and subjects’ complaints without inventing an aristocratic title or an uprising.',
(258,37):'London is the next step, not proof of reaching the estate or a promise of a further escort.',
(259,71):'Use a direct rude insult rather than an untranslated tongue-click.',
(259,79):'The guildmaster’s angry rebuttal comes after his silence and remains directed at the buyers; do not invent their group affiliation.',
(259,94):'Preserve distant ruins, a map making travel easy, and every local map being bought up.',
(261,10):'Use established Gabriel Cardocci rather than silently revising the name from a provisional Romanized gloss; review the name separately in scope.',
(264,9):'Keep the boast about never defaulting so the tavernkeeper’s literal never-paid comeback lands.',
(264,12):'Retain the short, dry contradiction; do not invent a payment or excuse for the debt.',
(264,18):'The one-and-only formulation conveys the source’s inflated self-reference, followed by its rude challenge.',
(264,41):'The property only appears stolen here; do not identify an unspoken item or owner.',
(265,17):'Recognize the repeated tavern excuse and naturally ask to be released from further involvement.',
(265,60):'Keep the object entrusted conditionally: the owner must remain unfound before the party can dispose of it as desired.',
(266,9):'Keep Portuguese origin, alleged betrayal in favor of Spain and reported courier-like work. These are the guildmaster’s claims, not added historical assertions.',
(270,9):'Use someone/her to preserve the explicit father/daughter revenge request without inventing the daughter’s age or name.',
(271,5):'Leave the angry insult unfinished, as in the source; the murder is already explicit in the linked request.',
(271,15):'The daughter decides his fate; do not invent an execution, pardon or legal sentence.',
(271,19):'A live capture was unexpected and earns generosity; do not reinterpret the earlier defeat request as requiring death.',
(271,69):'Keep discretion toward officials without inventing an official prohibition or a travel permit.',
(273,9):'The expedition was defeated in India; do not invent deaths or guarantee the target’s current position.',
(274,19):'Keep the preemptive rejection of his expected excuse, which sets up the next short question.',
(274,22):'The short reply asks whether he cannot use that excuse; it is the punchline, not a new objection to honest work.',
(274,76):'Retain the enshrined king and approval condition without assigning a religion or claiming a living ruler.',
(276,16):'Keep reported African success and pirate pretensions rather than creating a formal pirate rank.',
(277,13):'Preserve the correction of Jacob’s possessive claim: the cargo belonged to others.',
(277,66):'The source says only a building; do not identify the site or name its unspoken treasure.',
(279,8):'Retain the current Hernan Berio spelling; the provisional Berrio in the source gloss is not a new approved name.',
(280,8):'Keep the king comparison as dry ridicule of a bound braggart, not a real title.',
(280,65):'Keep the landmark unnamed. Its identity must not be imported from external knowledge.'}

def main():
    assert not OUT.exists();meanings=load(MEANINGS);rows=[]
    voice={1:'Hodram stays restrained, direct and dryly observant.',13:'Cesare stays courteous and expansive, with expressive surprise and private asides.',20:'Fernando stays colloquial, brash and easily alarmed.',64:'Yuris stays dreamy and politely oblivious until his sudden realization.',67:'Gabriel is boastful and defensive, reusing his debt excuse.',63:'Julian is an angry captured opponent.',65:'Plett’s weak apology does not erase the explicit killing.',66:'Jean is a fast talker whose excuses invite a deadpan reply.',68:'Jacob’s possessiveness is undercut by the guildmaster.',72:'Hernan grandstands even in captivity.',92:'The tavernkeeper is patient but firm, with a dry comeback.',113:'The port worker is friendly and colloquial; the role does not imply kinship.',114:'The port worker is occupational and colloquial; regional metadata is not a biography.',147:'The guildmaster is practical and conversational, with stronger language when provoked.',148:'The guildmaster is direct, earthy and grateful; metadata supplies no religious speech style.',149:'The guildmaster is blunt and compassionate in the revenge request, then morally indignant.',151:'The retainer reports a concrete discovery plainly, without inventing rank.',178:'The visitor is curt and rude; the source role alone does not prove cult affiliation.',189:'Wanda’s response is warmly regretful.',190:'Julia is welcoming and matter-of-fact.',200:'Titis makes a friendly personal exception.',207:'The source captain role’s short reaction stays short; native role resolution is still required.',254:'Preserve the specific FE role: system notice, inscription, voice or sound.'}
    for original in meanings['records']:
        row=deepcopy(original);kind=row.get('kind');block=row['block']
        if kind=='actor-style-alternative':
            english=STYLE[row['source_style_indices'][0]];note=row['source_meaning']+' Retain this complete physical alternative and its exact source alias slot.'
        elif kind=='typed-choice-label':
            labels={(251,432):["That's right","Of course not"],(252,270):['Front stone','Left stone','Right stone'],(252,1606):['Yes','No']}
            english=labels[(block,row['source_command_offset'])][row['source_index']];note='Preserve the source choice identity, order and branch meaning in the complete exchange.'
        else:
            index=row['source_reference']['record_index'];english=DRAFT[block][index];note=NOTES.get((block,index),voice[row['source_selector']])
        english.encode('ascii');assert english.strip()==english and '\n' not in english and not any(t in english for t in ['{LB','{ALIGN','{PAD}','%'])
        assert all(english.count('{MACRO:'+m+'}')==row.get('source_macros',{}).get(m,0) for m in ['FI','FA','FO']),(row['id'],english)
        if '{MACRO:FA}' in english:note+=' FA is the native surname substitution (Bergstrom in this route context), not a faction name or a new rank; retain its original token.'
        if row.get('source_selector')==254:
            index=row['source_reference']['record_index']
            speaker=('Wall inscription' if block==252 and index in [9,12] else 'Sound effect' if block==252 and index in [130,195] else 'Figurehead voice' if (block,index) in [(251,67),(252,138),(252,145),(252,160),(252,168),(252,184)] else 'Native system panel')
        else:speaker='Choice caption' if kind=='typed-choice-label' else 'Native companion role '+str(row['source_selector']) if kind=='actor-style-alternative' else 'Source actor '+str(row['source_selector'])
        row.update(english=english,speaker=speaker,context=row['exchange_context'],localization_note=note,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),clean_first_draft_not_final_comparison_approval=True,
            current_English_conversation_comparison_pending=True,source_names_terms_anddisplay_still_require_scoped_current_binding=True,new_credit=0)
        rows.append(row)
    assert len(rows)==216 and sum(r.get('kind')=='actor-style-alternative' for r in rows)==16 and sum(r.get('kind')=='typed-choice-label' for r in rows)==7
    save(OUT,dict(translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        records=rows,records_count=216,ordinary_drafts=193,physical_style_drafts=16,typed_caption_drafts=7,source_meanings=str(MEANINGS),source_meanings_sha256=digest(MEANINGS),
        all216_logical_drafts_written_before_current_story_English_intake_in_this_batch=True,
        prior_names_consulted_only_as_names_not_story_English=True,no_blanket_claim_of_no_historical_English_exposure=True,
        current_English_comparisons=0,current_comparison_name_term_formatting_andrelease_gates_pending=True,
        no_ordinary_manual_breaks_padding_alignment_ornew_story_fact=True,all_source_selectors_complete_preambles_macros_andaliases_preserved_in_reference=True,
        full_goal_complete=False,new_credit=0,guide_photos=False,
        evidence={str(p):digest(p) for p in (MEANINGS,ROOT/'clean_name_fields.json',ROOT/'draft_name_reference_v1.json',Path('guide/research/player-terminology-reference.json'),Path(__file__))}))
    print('Sealed all 216 clean-first English drafts; contextual comparison and scoped native checks remain.')

if __name__=='__main__':main()
