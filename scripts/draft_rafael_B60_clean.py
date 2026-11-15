"""Localize all alternative Pereira negotiation paths before current-English comparison."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.gloss_rafael_B51_B59_clean import ROOT

DRAFTS = [
"{MACRO:FA}?!", "Did you bring the Proof?", "I found a key to help us locate the Proof of Conquest.", "...Hmm.",
"I found the Proof of Conquest in East Asia, as promised.", "...Good. It's genuine, all right.", "All right. Come with me.",
"I've probably told you this before, but my position means I can't help you openly.", "...",
"But we both want to take down Kuhn and Spain. Common enemies, you might say.",
"Isn't that reason enough? Can't we make an agreement and defeat Kuhn and Spain together?",
"If only it were that simple.", "It isn't?", "Then let me ask you straight. What's your real enemy? ...Think carefully before you answer.",
"Huh? Our real enemy...",
"Well, well. You really mean to take on Spain's Invincible Armada? Even Albuquerque's joined their side, you know.",
"Yes. I'm completely serious!", "...Interesting. And if I refuse to help? Would you still do it?",
"...Then we'll have to manage without you. It may take longer, but we'll defeat Spain and restore Portugal ourselves.",
"...", "Well, that makes things simple.", "Hm?",
"Too many hypocrites out there waving the flag without the guts to back it up. Throw in with men like that, and a dozen lives wouldn't last you.",
"Looks like I was worrying over nothing. You'll do just fine.", "Come on! We'd better finish off Kuhn and get back home!",
"Pereira...!", "Right. This is for you.", "What's this...?",
"I'm told it's a key you need to decipher the map to a Proof of Conquest. Show me you're worthy of it.",
"You're sure we can have it?", "Yeah. Doesn't interest me. Who's got time to collect all seven? It's yours now.",
"...All right. Then I'd like us to make an agreement against Kuhn, here and now.", "And then?",
"Let's work together and defeat Kuhn first.",
"So we won't have to worry about what's behind us. Even I'd have my hands full taking him on alone.",
"If I were the king of Spain, I'd do everything I could to strip Portugal's royal family of its right to the throne for good. We don't have much time.",
"By defeating Kuhn, I want us to gain enough strength to take on Spain's Valdes, even on our own.",
"What?! On your own?! Have you lost your minds?",
"You're responsible for this region, Pereira. You can't simply abandon your post.",
"To hell with my post! We're about to rise up against the king of Spain!",
"...If this plan fails, you'll lose your position as governor of Indochina for good.",
"Ha ha ha! Is that what you're worried about? I know that perfectly well!",
"No! If we aren't strong enough, we need someone we can still entrust Portugal's future to!", "...!",
"All of Europe covets the Spice Islands. If we can hold on to them, the day will come when we can face even Spain as equals.",
"If you'll be Portugal's last stronghold, we can give this fight everything we've got.", "...Heh.",
"Ha ha ha! You're a remarkable one! I have to hand it to you!",
"All right, you've got it! I'll put my faith in you. Leave the rest to me!", "Yes! Thank you!",
"Hm? What do you mean?", "We'll leave Southeast Asia immediately.", "And then?",
"We'll sail to Europe to defeat Spain's Valdes.", "Hold on. You're doing what?",
"If I were the king of Spain, I'd do everything I could to strip Portugal's royal family of its right to the throne for good. We don't have much time.",
"True enough... So you're leaving Kuhn for later?",
"No. I'm leaving everything here to you, Pereira. As governor of Indochina, you're responsible for Southeast Asia.",
"Oh... I see. You want me to watch your backs.",
"Yes. If we know this region is in good hands, we can face Valdes with all our strength.",
"Ha ha! You're quite something! You've already made me a piece in your grand strategy, eh?",
"All right. Leave it to me. But what happens if I drive Kuhn out myself?",
"You've given me the key to the Proof of Conquest. I have no objection to leaving this region's trading rights to you.",
"Ha ha ha! Is that charity? Don't worry about it. You can always come back and take Southeast Asia from me, too!",
"I-I wouldn't...", "Business is fair, isn't it? Free competition, right?", "Y-yes, but...",
"In return, you'd better finish off Valdes. Understood?", "Of course!",
"Restoring our homeland, eh? You just might be able to do it... Yes, you might.", "...",
"Let me put it another way. {MACRO:FA}, who's the strongest power in the world right now?",
"Whoever's got the biggest trading sphere, obviously. Us, or...",
"No. That's not what I mean. If someone really set out to conquer the world, who'd be in the best position to do it?",
"Spain... with the Invincible Armada?", "There's some truth to that... {MACRO:FA}, you know the Spice Islands, don't you?",
"Yes. They're around here.", "That's right. To Europe, the Spice Islands are treasure islands. You understand?", "...Yes.",
"And it's not just the spices. The goods from these parts bring in enormous profits. If whoever controls them used that wealth to start conquering...",
"They could take over the world...", "Exactly.", "...Antony Kuhn... King of the world? Not a chance in hell!",
"God might allow it, but I won't!", "So controlling the Spice Islands means controlling the world...",
"Can't just put that down to good luck.", "Looks like you're starting to get the picture.",
"The reason I'm not fighting Kuhn all-out right now is that if I lose, there'll be no one left to stop him.", "...",
"Restoring our homeland is a fine thing. But we can't get so caught up in it that we let him take the whole world.",
"Then what should we do...?",
"Go and defeat Spain's Valdes! Once you've proved yourselves there, we'll have a fighting chance against Kuhn together!",
"Valdes's fleet... Spain's Invincible Armada...",
"If I were the king of Spain, I'd do everything I could to strip Portugal's royal family of its right to the throne for good. There's no time to waste.",
"Once Spain's been brought to heel and Portugal's restored, I can give you my full support.", "Yes... That makes sense.",
"Valdes ought to know where the Mediterranean's Proof of Conquest is. If you can't beat that little mustached bastard, you won't beat Kuhn in a hundred years!",
"...All right. We'll defeat Valdes and come back. I promise!", "I'm counting on you, Admiral {MACRO:FA}!",
]

NOTES = {
    21:'Keep finding the key distinct from the alternative branch’s delivery of the actual Proof.',
    31:'Keep the actual Proof delivery andEast Asia location distinct from the key-only alternative.',
    111:'Preserve Albuquerque’s explicitly reported alignment with Spain;do not invent capture ordefeat.',
    140:'Localize halfhearted patriotic posturing as flag-waving without courage;keep Pereira’s distrust andmortal stakes.',
    165:'Preserve the map-deciphering key andPereira’s worthiness challenge without making him a monarch.',
    173:'Retain Pereira’s disinterest andthe explicit total of seven.',
    208:'Preserve permanent loss of the Portuguese royal family’s succession rights,without inventing Rafael’s ancestry.',
    225:'Use the source’s brief profanity to convey Pereira’s angry rejection of concern for his post.',
    238:'Retain Rafael’s contingency plan for Portugal rather than make this a claim that Pereira is already a rebel.',
    246:'Retain European demand,control of the Spice Islands andthe future possibility of facing Spain as equals.',
    250:'Use last stronghold as the source metaphor;do not invent a fortress location.',
    314:'Keep Pereira’s amused game-piece metaphor for being included in Rafael’s strategy.',
    322:'Keep the clue key andtrading rights as distinct things;no ownership of the whole territory is invented.',
    327:'Keep Pereira’s joking permission to defeat him later;do not turn it into a declaration of hostility.',
    354:'Retain the repeated emphasis on this group’s potential without confirming royal descent.',
    399:'Preserve that products beyond spices also generate immense wealth andcould finance conquest.',
    411:'Use established Antony Kuhn spelling andClaudio’s vehement rejection;no new formal royal title is assigned.',
    451:'Preserve the conditional consequence if Pereira loses,not a claim that nobody else could ever defeat Kuhn.',
    486:'Preserve reported clue knowledge andthe mustache insult/hundred-year taunt as Pereira’s speech.',
}

if __name__ == '__main__':
    output = ROOT / 'B60_99_logical_English_drafts_v1.json'; assert not output.exists()
    source = ROOT / 'B51_B60_source_identity_checkpoint_v1.json'; binding = load(source)
    originals = [r for r in binding['records'] if r['block']==60]
    assert len(originals)==len(DRAFTS)==99
    names = {r['actor_ID']:next(c['text'] for c in r['current_consumers'] if c['consumer']=='progressive-nameplate') for r in binding['name_bindings']}
    records = []
    for row,english in zip(originals,DRAFTS,strict=True):
        assert '\n' not in english and '{LB' not in english and '{PAD}' not in english
        assert all(english.count('{MACRO:'+key+'}')==count for key,count in row['source_macros'].items())
        note = NOTES.get(row['source_reference']['record_index'],'Natural complete-exchange wording preserves this source intent: '+row['source_meaning'])
        records.append(dict(**{k:v for k,v in row.items() if k!='review'},english=english,speaker=names[row['source_selector']],
            context=row['whole_exchange_context'],localization_note=note,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            current_English_comparison_pending=True,complete_native_preamble_choice_branches_andfresh_formatting_pending=True))
    save(output,dict(format='dk4-clean-logical-English-drafts-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        source=str(source),source_sha256=sha(source.read_bytes()),records=records,logical_drafts_saved=99,
        all_branch_alternatives_remain_separate=True,current_story_English_unconsulted=True,
        established_Kuhn_spelling_requires_saved_exact_field_receipt_before_final_review=True,
        current_comparison_native_controls_display_andrelease_pending=True,new_credit=0,guide_photos=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('Saved99 complete branching-negotiation drafts;245 source-first drafts now saved,all display/current comparisons pending.')
