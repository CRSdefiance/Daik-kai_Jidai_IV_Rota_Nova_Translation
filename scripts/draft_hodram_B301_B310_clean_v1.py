"""Write logical American English from the sealed Japanese meanings, before current dialogue."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.gloss_hodram_B301_B310_clean_v1 import ROOT,OUT as MEANINGS

OUT=Path('translations/hodram_B301_B310_clean_drafts_v1.json')
DRAFT={
301:{6:"Oh, {MACRO:FI}! Perfect timing.",9:"Have you heard of the Colosseum?",13:"The Colosseum?",
17:"It's a ruin from Roman times. I heard you were looking for ruins, so I thought I'd tell you about it.",
21:"That helps. Let's go take a look right away.",24:"Take care. And don't forget to buy a map."},
302:{71:"We have a long way to go. Make the water last.",108:"This sandstorm won't let up. We press on.",
137:"The sailors seem fatigued. Some appear to have dropped out.",141:"We'd better let it pass. We'll wait a little.",
180:"We cannot wait any longer. We press on through the sandstorm.",187:"The sailors seem fatigued.",
193:"Going on through this sandstorm would be unwise. We have no choice but to wait for it to pass.",
203:"One day passed.",207:"It seems to have let up."},
303:{6:"Oh, {MACRO:FI}! Welcome!",9:"Thanks to you, my dancing has really improved!",12:"Let me tell you something good to thank you.",
16:"Far inland from this town, there's a mosque dedicated to an old king. They say there's a wonderful treasure there.",
20:"The rumor is, only someone the king recognizes can claim it. Why not go and try?"},
304:{12:"Did you bring the map?",16:"No... I forgot it.",30:"Well, this is where we part. Have a safe trip!",35:"Thank you.",
98:"We go through the swamp.",129:"That should have saved us quite a journey.",133:"Yes. We should be there soon.",
137:"The sailors seem fatigued.",148:"We cannot cross this swamp. We'll turn back and take another route.",155:"One day passed.",
159:"We seem to have taken quite a detour.",162:"Yes, though we should be arriving about now...",168:"A-Admiral! There it is!"},
305:{6:"Oh, {MACRO:FI}!",10:"I'm going to visit a temple today. Want to come?",13:"Unfortunately, I'm not Buddhist...",
17:"That's all right. We're just going to look around.",20:"Come to think of it...",24:"Is the golden temple on this map near there?",
27:"Golden? Oh! That temple. It's not nearby, but...",31:"Let's go part of the way together. After that, just follow your map. It should take you there."},
306:{13:"The monk at Kinkaku-ji asked us to find some memento of a Yuan emperor.",
19:"Kublai's Greatsword... So this is the Yuan emperor's memento the monk at Kinkaku-ji spoke of."},
307:{12:"The monk at Kinkaku-ji asked us to find some memento of a Yuan emperor.",16:"We must make sure it's unequipped as well.",
30:"Hello?",34:"So, you've come... Ah! That's it!",38:"Yes. You should be able to manage.",
42:"Far northeast of China, near the icy sea, seek a small village. A clan that guards the map should live there.",
45:"Far northeast of China...",49:"At the base of a vast peninsula. Look at the foot of a high mountain on its eastern coast.",
52:"It is so remote that an ordinary ship may struggle to reach it. Take this journey lightly, and none of you will return alive.",55:"...",
59:"Listen well. Never give the Proof to anyone with evil intentions. Nor must you fall prey to evil desires yourself.",
62:"I will keep that firmly in mind."},
308:{},
309:{89:"Eek! Aaaah!",94:"Calm down.",98:"W-what are you going to do?",117:"Leave it to me. I'll drive it off.",
140:"Gah! I let my guard down.",167:"It is only a scratch. Don't worry.",174:"{MACRO:FI} has been injured.",
178:"Form up! We'll break through together!",226:"Are you all right?!",249:"If I hadn't lost my balance... I am truly sorry.",
273:"I see.",280:"The sailors seem fatigued.",285:"That wolf seems hungry. We'd better run. Hurry!",
294:"The sailors are fatigued. Some appear to have dropped out."},
310:{6:"Welcome, {MACRO:FI}.",9:"You want to know where the city gate is?",13:"We're actually not supposed to tell foreigners, but...",
16:"Well, with all the pressure from abroad, this country's isolation is mostly in name now anyway. All right. I'll tell you, but keep it quiet."},
}

STYLE={
(302,24):[
"Admiral, without a map, we could lose our way...","Admiral, we need a map here.",
"Admiral, we can't go on without checking a map!","Admiral, we need a map first, or we'll get lost.",
"Admiral, going on without a map is a bad idea.","Admiral, we'll lose our way without a map.",
"Admiraaal, we'll get lost without a map!","Admiral, without a map, we will lose our way."],
(302,392):["It's very hot here.","Hot...","Whew, it's hot!","It really is hot here.","It's so damn hot!","It is terribly hot here.","Whew! It's hot!","My, it is hot here."],
(302,596):[
"A fierce sandstorm. If we go on, we could lose our way. What should we do?",
"A fierce sandstorm... We could lose our way if we go on... Admiral, what shall we do?",
"What a sandstorm! We'll get lost for sure if we go on! What do we do?",
"What a terrible sandstorm. I'm worried we'll lose our way if we go on... Admiral, what do you think?",
"That's one hell of a sandstorm. We could get lost in it... Still going?",
"A fierce sandstorm indeed. We may lose our way if we go on. What do you propose?",
"What a sandstorm... I think we'll get lost for sure if we go on... What should we do?",
"A fierce sandstorm. Going into it is as good as losing our way. Shall we proceed all the same?"],
(302,1320):["I see... Then let's try going on.","...If you say so, Admiral. Let us proceed.","Oh... All right. Let's go, then.",
"I see... All right. Let's go on.","All right, got it. Let's go.","I understand your decision, Admiral. Let us try going on.",
"You think so...? Well, let's go on anyway.","I see. Understood. Let us try going on."],
(302,1786):[
"...This sandstorm shows no sign of letting up at all. What should we do?",
"...The sandstorm does not seem likely to let up. Admiral, what shall we do?",
"...Hmm. It might not stop, even if we wait longer. What do we do?",
"...This sandstorm doesn't look like it's going to let up at all. What should we do?",
"...Doesn't look like this sandstorm's letting up. What's the plan, Admiral?",
"...Hmm. The storm shows no sign of easing. What do you propose?",
"...Hmm. It might not stop even if we wait longer. What should we do?",
"...This sandstorm does not seem likely to let up. What shall we do?"],
(302,2582):[
"I think we should be out of the desert soon...","We ought to be out of the desert by now...",
"We should be out of the desert by now...","We should be out of the desert by now, shouldn't we...?",
"We should be getting out of this desert soon...","We ought to be clear of the desert shortly...",
"The desert should be ending by now...","We should be out of the desert shortly..."],
(302,2900):[
"Admiral! Please look over there!","Admiral! Please look over there!","Admiral! Look at that!","Admiral! Look at that!",
"Admiral! Take a look at that!","Admiral! Look there!","Admiraaal! Look over there!","Admiral! Over there!"],
(304,164):["Well, let's go.","Well, let's go.","Come on, let's go!","Well, let's go.","Well, let's get going.","Shall we be off, then?","Off we go!","Well, shall we set out?"],
(304,296):[
"There's a swamp ahead. What should we do?","A swamp ahead... What shall we do?","We've run into a swamp. What do we do?",
"Oh, a swamp. What should we do?","We've hit a swamp. What's the plan?","A swamp, I see. What do you propose?",
"Huh? We've run into a swamp! What should we do?","Well, well, a swamp lies ahead. What shall we do?"],
(304,638):[
"It's surprisingly shallow.","It's shallower than I expected.","It's surprisingly shallow! What a relief.","It's surprisingly shallow. That's a relief.",
"Huh. It's surprisingly shallow.","Oh, surprisingly shallow indeed.","Huh? It's shallower than I thought!","It's shallower than expected."],
(308,8):[
"Admiral, we really must visit the clan guarding the map to a Proof. Their village was far northeast of China, wasn't it?",
"Admiral. We should visit the clan guarding the map to a Proof as soon as possible. We were told their village lies far northeast of China.",
"Admiral, I wonder what the clan guarding the Proof's map is like. Their village was far northeast of China, right? Shall we go now?",
"Admiral, let's visit the clan guarding the Proof's map before we forget. Their village was far northeast of China, wasn't it?",
"Admiral, let's go see the clan guarding the Proof's map soon. They're in a village far northeast of China, right?",
"Admiral, about that Proof... We ought to visit the map's guardians soon. Shall we head for that village far northeast of China?",
"Admiraaal, aren't you curious about the people guarding the Proof's map? Let's go to that village they say is far northeast of China!",
"Admiral, I am curious about the Proof's map. Shall we visit the village where its guardian clan lives? It was... far northeast of China, yes?"],
(309,24):[
"Admiral, we'll get lost without a map.","Admiral, we will get lost without a map.","Admiral, isn't going without a map a bad idea?",
"Admiral, we could lose our way without a map.","Admiral, going without a map is asking for trouble.","Admiral, we'll lose our way without a map.",
"Admiraaal, we need a map to go on!","Admiral, without a map, we will lose our way."],
(309,322):["Well, let's go.","Well, let's go.","Come on, let's go!","Well, let's go.","Well, let's get going.","Shall we be off, then?","Come on, let's go!","Well, let's go."],
(309,422):[
"A-Admiral! A wolf!","Hm! A wolf!","A-Admiral! It's a wolf!","Aaaah! A wolf!!",
"Whoa! A wolf's appeared!","A-Admiral! A wolf!","Waaah! It's a wolf!","A-Admiral! There's a wolf!"],
(309,810):[
"Ah! Admiral! Look out!","Ah! Admiral! Look out!","Admiral! Watch out!","Admiral! Be careful!",
"Look out!","Admiral! Look out!","A-Admiral! Watch out!","Ah! Admiral! Look out!"],
(309,1006):[
"Are you all right?!","Are you all right?!","Are you okay?!","Are you all right?!","Are you all right?!",
"Are you all right?","Are you okay?","Are you all right?!"],
(309,1214):["Look out!","Look out!","Look out!","Look out!","Watch it!","Look out!","Watch out!","Look out!"],
(309,1278):["Gah!","Gah!","Gah!","Aaaaah!","Gah!","Gyaah!","Waaaah!","Gah!"],
(309,1368):[
"Ugh! I-I'm managing...","Ugh! I-I'm managing...","Ow! Ow, ow...","Ahh! It hurts...",
"Ugh! I-it's nothing serious!","Ugh! I-I'm all right...","Waaah! I'm not all right!","Ugh! I-I'm managing..."],
(309,1590):[
"It'll be all right with prompt treatment. The wolf has fled, too.",
"Admiral... Please don't worry. Prompt treatment will heal the wound. The wolf has fled, too.",
"It's all right! We just need to treat it right away. The wolf's gone, too.",
"We just need to treat the wound right away. At least the wolf is gone now.",
"Don't worry! A wound like that will heal if we treat it right away. The wolf's gone, too.",
"Do not dwell on it. Prompt treatment will keep such a wound from becoming serious. The wolf has gone, so that settles that.",
"It'll be fine if we treat it right away! The wolf ran off, too. That's a relief!",
"It is all right. A wound like that will heal with prompt treatment. The wolf has fled as well."],
(309,2364):[
"Hah, hah, hah! We should be safe here.","Hah, hah, hah! We should be safe here.","Hah, hah, hah! Are we safe here now?",
"Hah, hah, hah! We should be safe here now, shouldn't we?","Hah, hah, hah! We're safe here now, right?",
"Wheeze... Wheeze... W-we're safe now...","Hah... Hah... We've run far enough to be safe, right?",
"Hah, hah, hah! We should be safe here now."],
(309,2758):[
"We should be out of the forest soon.","We should be out of the forest soon.","We're nearly out of the forest, aren't we?",
"We should be out of the forest soon.","We should be getting out of this forest soon.","We ought to be clear of the forest soon.",
"The forest must be ending now, right?","We should be out of the forest soon."],
(309,2938):[
"Admiral, it's coming into view!","Admiral, it's coming into view!","That's it, Admiral!","Admiral, it's in sight!",
"Admiral, it's coming into view!","Admiral, there it is!","We found it, Admiral!","Admiral, it's coming into view!"],
}

CAPTIONS={(302,1226):['Keep going','Wait for it to pass'],(302,2272):['Go into the sandstorm','Wait a little longer'],
    (304,576):['Enter the swamp','Turn back'],(309,738):['Drive it off','Fight','Run']}

def main():
    assert not OUT.exists();meanings=load(MEANINGS);reference=load(ROOT/'draft_name_reference_v2.json')
    assert meanings['records_count']==234 and meanings['current_story_English_compared']==0
    names={r['actor_ID']:r for r in reference['records']}
    assert {k:next(f['RAM_text'] for f in names[k]['fields'] if f['column']==0) for k in [137,192,197,201,203]}=={
        137:'Senior Monk',192:'Matilda',197:'Safia',201:'Mihwa',203:'Sakura'}
    item=next(r for r in load('translations/all_item_names_arm9_v1.json')['records'] if r['id']=='DK4_ITEM_POINTER_045')
    assert item['english']=="Kublai's Greatsword"
    voices={1:'Hodram is restrained, decisive and practical; courteous to the monk, with dry objections to the temple visit and sincere concern after an injury.',
        16:'Gerhard is courteous and practical; preserve his equipment reminder and qualified travel expectations without inventing Lord or a new rank.',
        137:'The Senior Monk is terse and authoritative, giving precise directions and a moral warning without an invented office, doctrine or regional name.',
        151:'The sailor reacts in fear and asks about the plan; the generic role does not create a personal identity.',
        192:'Matilda is warm and helpful; familiarity and a useful lead do not establish romance or a shared expedition.',
        197:'Safia is upbeat and grateful. Preserve improved dancing and the reported treasure lead without inventing a specific prior lesson or romance.',
        201:'Mihwa is conversational and discreet. Preserve the closed-door-policy qualification as her in-game account, not an external historical assertion.',
        203:'Sakura is friendly and matter-of-fact, gently dismissing the religious objection. Her offer is only to travel partway.',
        207:'Preserve the captain-role puzzled echo without assigning a new speaker.',
        208:'Preserve the source companion reaction; exact runtime participant and voice binding remain pending.',
        254:'Preserve the precise status notice, uncertainty, departure versus death, time or captain-name substitution.'}
    rows=[]
    for original in meanings['records']:
        row=deepcopy(original);kind=row.get('kind');block=row['block']
        if kind=='actor-style-alternative':
            values=STYLE[(block,row['source_command_offset'])];indices=row['source_style_indices']
            assert len(values)==8 and len({values[i] for i in indices})==1
            english=values[indices[0]];speaker='Native companion role '+str(row['source_selector'])
            note=row['source_meaning']+' Preserve all exact physical aliases and the register without inventing age, gender, kinship or party membership.'
        elif kind=='typed-choice-label':
            english=CAPTIONS[(block,row['source_command_offset'])][row['source_index']];speaker='Choice caption'
            note='Preserve this menu’s original order and branch meaning in the complete exchange.'
        else:
            index=row['source_reference']['record_index'];english=DRAFT[block][index]
            speaker='Native system panel' if row['source_selector']==254 else 'Source actor '+str(row['source_selector'])
            note=voices[row['source_selector']]
            if (block,index)==(307,16):note+=' This explicitly preserves the equipment-removal requirement.'
            if (block,index)==(307,30):note+=' The entrance greeting is not an apology.'
            if (block,index)==(309,174):note+=' FI names the injured captain; do not change it to a crew-wide injury.'
            if block in [306,307]:note+=' Kinkaku-ji and the item45 memento require final scoped terminology binding; do not invent a named ship class or village.'
        english.encode('ascii');assert english.strip()==english and '\n' not in english
        assert not any(t in english for t in ['{LB','{ALIGN','{PAD}','%'])
        assert all(english.count('{MACRO:'+m+'}')==row.get('source_macros',{}).get(m,0) for m in ['FI','FA','FO']),(row['id'],english)
        row.update(english=english,speaker=speaker,context=row['exchange_context'],localization_note=note,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            clean_first_draft_not_final_comparison_approval=True,current_English_conversation_comparison_pending=True,
            source_names_terms_anddisplay_still_require_scoped_current_binding=True,new_credit=0)
        rows.append(row)
    assert len(rows)==234 and sum(r.get('kind')=='actor-style-alternative' for r in rows)==152
    assert sum(r.get('kind')=='typed-choice-label' for r in rows)==9
    save(OUT,dict(translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],records=rows,records_count=234,
        ordinary_drafts=73,physical_style_drafts=152,typed_caption_drafts=9,source_meanings=str(MEANINGS),source_meanings_sha256=digest(MEANINGS),
        all234_logical_drafts_written_before_current_ROM_story_English_intake=True,
        prior_names_andnonstory_terms_consulted_as_references=True,no_blanket_claim_of_no_historical_English_exposure=True,
        provisional_source_Meihua_reconciled_to_existing_Mihwa_without_rewriting_gloss=True,
        current_English_comparisons=0,current_comparison_name_term_formatting_andrelease_gates_pending=True,
        no_ordinary_manual_breaks_padding_alignment_ornew_story_fact=True,full_goal_complete=False,new_credit=0,guide_photos=False,
        evidence={str(p):digest(p) for p in (MEANINGS,ROOT/'draft_name_reference_v1.json',ROOT/'draft_name_reference_v2.json',ROOT/'clean_name_fields.json',Path('translations/all_item_names_arm9_v1.json'),Path(__file__))}))
    print('Sealed234 source-first logical drafts. Current-ROM comparisons, scoped names/terms and display gates remain.')

if __name__=='__main__':main()
