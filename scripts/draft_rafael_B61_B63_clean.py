"""Localize77 source-bound speeches as complete exchanges before older-English comparison."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_clean_20261104')
DRAFTS={
61:[
"To think I'd lose the jar to the likes of them...",
"Damn it! I'll remember this!",
"Me, beaten by the likes of them... when I was so close?!",
"Oh! Well done, Admiral {MACRO:FA}!",
"Yes, we managed it somehow... Thank you, Governor Pereira.",
"Don't mention it!",
"Don't mention it!",
"All right, no more quibbling! Do things your way. Go beat Spain, or whoever else gets in your way!",
"Governor...",
"Hey, you're all right, Pereira!",
"Ha ha ha! Governor Pereira of Indochina is always a good guy!",
"Ha ha ha! Governor Pereira of Indochina is always a good guy! Here, Admiral {MACRO:FA}. Take this.",
"You received an incredible 500,000 in military funds from Governor Pereira!",
"Whaaaaat?!",
"Well, well!",
"Whoa! Now that's generous! You're incredible, Governor!",
"YAAAHOOO!!!",
"All this...? Are you sure?!",
"Of course! Don't worry about it! Now go give it your all. I'm counting on you!",
"Yes!",
],
62:[
"No one is more worthy to command this continent's seas than you, {MACRO:FA}. Please accept this.",
"Could this be... something to do with the Proof?!",
"Oh, thank you! ...Huh?",
"He's already gone.",
"It looks like a sword scabbard, but there's no sword inside... What could that mean?",
"Could this be another key to deciphering the map to the Proof of Conquest?",
"This must be another key to deciphering the Proof of Conquest map.",
"Yeah, I'll bet it is! The New World's treasure is as good as ours!",
],
63:[
"{MACRO:FI}, got a minute? Come to the inn.",
"Hm? Sure.",
"...You ought to show a little consideration.",
"Huh? What do you mean?",
"I'm talking about Eirene. You had Eirene help with the heavy lifting the other day, remember?",
"Only a little.",
"That's not the point! Eirene isn't as tough as the rest of us. You ought to show some consideration!",
"Well... there were reasons for it.",
"And that makes everything all right, does it?!",
"...You don't have to get so angry!",
"Fine! Suit yourself!",
"...{MACRO:FI}? What's wrong?",
"Oh, Arcadius... It's just... something.",
"I thought I heard Claudio shouting a moment ago...",
"(Oh, no...) Did you hear what we were arguing about?",
"No, not that much.",
"...Can we talk for a minute?",
"Of course...",
"Listen, Eirene... that argument just now was about you.",
"...About me?",
"Clau's angry with me. Remember when you helped with the heavy lifting?",
"Oh... No one else was there. And since everyone thinks I'm a man, it would've looked strange if I hadn't helped, wouldn't it?",
"That's what I told him. We didn't have a choice. But he was furious.",
"...",
"Clau just shouted at me and stormed off without listening.",
"I thought I was looking out for you too, Eirene. It's not fair...",
"I'm sorry. Keeping it a secret that I'm a woman has made things difficult for you, {MACRO:FI}.",
"No, it hasn't. I'm sorry for complaining. Don't worry about it.",
"...You know, {MACRO:FI}, I think you're working very hard as our admiral.",
"You're the reason we can all feel safe aboard the ship.",
"You're making me blush, Eirene. What brought this on?",
"Nothing's wrong. I just don't want you pushing yourself too hard, {MACRO:FI}.",
"Eirene...",
"Don't keep your worries to yourself. Talking to someone can make you feel better, even if you just need to complain.",
"You're... like a big sister, Eirene.",
"Am I?",
"Yes. I really do feel better now. Thanks for listening.",
"No, I should be the one apologizing for putting you through this.",
"I've never had a fight like this with Clau. I just don't know what to do... What should I do?",
"Oh, that? I'm sure Claudio will be fine. Once he's had a meal, he'll probably forget all about it.",
"You think so?",
"Of course. He's really not that complicated. Come on, let's eat.",
"Hey, {MACRO:FI}! Get enough to eat?!",
"Oh, uh, yes. Clau...",
"What? Why the funny face?",
"N-nothing. I just thought you seemed in a good mood...",
"Huh? Well, whatever. I'll go on ahead.",
"Eirene was right. He's forgotten all about the fight...",
"Eirene knows Clau so well... Maybe it's because she's a scholar?",
]}
NOTES={
(61,22):'Preserve Kuhn wounded self-importance in natural first-person English;the named speaker header already binds his identity.',
(61,42):'Keep this brief reply separate from the conditionally distinct identical R64 occurrence.',
(61,64):'Keep this brief reply separate from the conditionally distinct identical R42 occurrence.',
(61,83):'Use Pereira as the familiar older-man address;no kinship ornew rank is invented.',
(61,94):'Retain Pereira deliberately boastful third-person Governor of Indochina self-description andhearty laugh.',
(61,107):'Retain the longer alternative self-boast andgift handover;do not treat it as following the shorter alternative unconditionally.',
(61,113):'Preserve500000 military funds andthe source notice surprise;do not invent a physical treasure chest orunspecified named currency.',
(61,147):'Keep Jam exuberant drawn-out cheer without introducing an unrelated cultural catchphrase.',
(62,5):'Render worthy sea leadership as praise,not a new formal royal appointment;keep the source continent reference.',
(62,34):'Retain Rafael tentative map-key inference,distinct from Arcadius more confident alternative atR40.',
(62,40):'Retain Arcadius confident map-key inference,distinct from Rafael question atR34.',
(63,22):'Keep Eirene as the privately used name bound to sourceactor8 middle field;avoid adding a gendered pronoun before the source explicitly discusses the disguise.',
(63,30):'Keep Claudio angry concern about physical toughness rather than inventing a diagnosed illness ornew family relationship.',
(63,92):'Preserve the publicly male persona andher reason for helping;do not change Arcadius public speaker control.',
(63,113):'The source explicitly identifies the concealed womanhood here;retain the apology andconsequences without inventing why the disguise began.',
(63,146):'The older-sister wording is an explicit simile,not actual kinship oran invented sibling biography.',
(63,162):'The repeated question conveys Rafael anxiety after an unusually serious quarrel;retain its emotional function without authored display breaks.',
(63,175):'Use affectionate understatement for単純;Eirene is reassuring Rafael,not delivering an unrelated insult.',
(63,202):'Preserve Rafael naive scholar explanation andthe comic uncertainty;do not substitute an invented romantic conclusion.'}

if __name__=='__main__':
    output=ROOT/'B61_B63_77_logical_English_drafts_v1.json';assert not output.exists()
    source=ROOT/'source_identity_event_andterm_checkpoint_v1.json';binding=load(source)
    names={r['actor_ID']:next(c['text'] for c in r['current_consumers'] if c['consumer']=='progressive-nameplate') for r in binding['name_bindings']}
    actor8=next(r for r in binding['name_bindings'] if r['actor_ID']==8)
    assert next(f['current_text'] for f in actor8['source_andcurrent_fields'] if f['column']==8)=='Eirene'
    keys=['id','file_path','block','source_selector','source_hex','source_complete_preamble_hex','source_reference',
        'source_Japanese','source_decode_error','source_0100_ancestors','native_extent','source_macros','source_meaning','whole_exchange_context']
    records=[]
    for block in [61,62,63]:
        rows=[r for r in binding['records'] if r['block']==block]
        assert len(rows)==len(DRAFTS[block])
        for original,english in zip(rows,DRAFTS[block],strict=True):
            assert english.strip()==english and '\n' not in english and not any(t in english for t in ['{LB','{ALIGN','{PAD}'])
            assert all(english.count('{MACRO:'+key+'}')==count for key,count in original['source_macros'].items())
            index=original['source_reference']['record_index']
            row={k:original[k] for k in keys}
            row.update(english=english,speaker=names[original['source_selector']] if original['source_selector']!=254 else 'Military-funds notice',
                context=original['whole_exchange_context'],localization_note=NOTES.get((block,index),'Natural complete-exchange wording preserves this source intent: '+original['source_meaning']),
                review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
                source_first_draft=True,earlier_English_unconsulted=True,current_English_comparison_pending=True,
                complete_native_preamble_fresh_formatting_stored_visual_andregistered_release_pending=True)
            records.append(row)
    assert len(records)==77
    save(output,dict(format='dk4-clean-logical-English-drafts-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        source=str(source),source_sha256=sha(source.read_bytes()),records=records,logical_drafts_saved=77,
        source_meanings_preceded_drafts_andcurrent_story_English_remains_unconsulted=True,
        all_conditional_alternatives_kept_separate=True,all_fifth_formatting_gates_false=True,
        no_name_data_orROM_orcompletion_credit=True,new_credit=0,guide_photos=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('77 natural-English source-first drafts sealed;all complete exchanges reviewed,older English/formatting still pending.',flush=True)
