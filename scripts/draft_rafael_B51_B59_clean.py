"""Draft nine whole source exchanges with established names and no authored wrapping."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.gloss_rafael_B51_B59_clean import ROOT

DRAFTS = {
51: [
"It's so quiet and peaceful here. All right. It's been a while since I...",
"(Hm?)", "(Smiles.)", "...? (Who is she?)", "...", "Sera.", "(Hm?)", "Oh, Hodram.",
"Who is he? Someone you know...? No, I suppose not.", "...", "...Hmm.", "Hodram?", "Let's go.", "Yes.",
"...She was beautiful. I wonder what country's princess she is.",
"But that military man beside her... Wasn't he with the Swedish navy...?",
],
52: [
"Oh, you there. Are you with {MACRO:FO}?", "Hm? Yes, I am.", "I thought so.",
"Admiral Albuquerque of the Portuguese military asked me to pass on a message if I saw you. He wants you to return home to Lisbon.",
"Hm? What could the military want with us?", "Guess we don't have much choice. Shall we head back for now?",
"It seems we have little choice. Shall we return for now?",
],
53: [
"Admiral, that reminds me. The Portuguese military's summoned us. What do you want to do?",
"I suppose we'd better go. We need to visit the palace, right?", "That's right.",
],
54: [
"Hey, you! Have you heard the news?", "Hm?",
"They say Fernan Silveira's put an end to that notorious Espinosa!", "...So that's the story going around.",
"Huh? You're a strange one, lad. Oh, never mind. I suppose Silveira's better than Espinosa, anyway. That man was nothing but trouble.",
"Well... You may be right.", "I hear he's moving the governor's office to Sofala...",
"The African governor's office...?! To Sofala?! I've got to go! Thank you!",
"Hey! ...What on earth was that all about?",
],
55: [
"Ah, {MACRO:FI}! Well done!", "Oh! Admiral Fernan! (He's here already...!)",
"You've done splendid work! I've already reported everything to His Excellency Albuquerque, so you needn't worry about a thing.",
"...Oh.", "Now, I did turn him down, you understand. But His Excellency insisted...",
"And so I've been appointed governor of Africa! Ha ha ha!", "What?!",
"The Silveira Company has taken all your market share in Sofala!",
"Well, that's luck for you. No hard feelings, eh? Ha ha ha!",
"And here's your reward from His Excellency Albuquerque. Oh, and there's no need for a gift to celebrate my appointment. I've already deducted it from your reward.",
"Of course, if you insist on giving me something more, I certainly won't object. Ha ha ha!",
"Received 3,000 gold coins...", "...Ugh! He's made fools of us!",
"Did Commander Albuquerque really decide all this?",
"Tch. That bastard must've badgered him into it. Probably fed him a pack of lies and took all the credit for beating Espinosa.",
"I never imagined he could be so underhanded... Admiral {MACRO:FI}, surely we can't let him get away with this.",
"Admiral! Looks like we've found our next target!", "Well, that settles who our next target will be.", "Huh?",
"Silveira! Now you've really got me fired up!", "We can't just sit back and take this!",
"God might forgive him, but I won't! Yahoo!", "Let's take him down!",
"...Y-yes. I don't like the idea of fighting other Portuguese, but I'd hate to back down now even more.",
"I'll never forgive you, Silveira!",
"Good grief. Putting these old bones to work again... Well, {MACRO:FI}! Let's give it our best!",
"Let's beat him! We'll show Silveira a thing or two!", "...Thank you, everyone! All right! We'll conquer Africa!",
"Let's go!", "Yeah!",
],
56: [
"Oh! You're the head of {MACRO:FO}, aren't you?", "Ah, perfect timing! Hey, you there!",
"Me? ...What can I do for you?", "Life's a lot better now than when Espinosa and Silveira were throwing their weight around.",
"It certainly is. And we have your people to thank.", "...You think so? You're making me blush.",
"Those crooked merchants were in charge so long, we nearly forgot what it meant to trust anyone.",
"You're right about that... Oh! I nearly forgot what we wanted to tell you!", "Oh?",
"...Come on, pay attention! Here, take this.", "What's this...?", "Could it be something to do with a Proof of Conquest...?!",
"Um... Where did you get this?!", "An adventurer was trying to sell it to Espinosa for a fortune.",
"Can you imagine? Making money by telling a devil like that where the Proof of Conquest is! What a terrible idea.",
"A-are you sure I can have it?", "The whole town chipped in, and we made him sell it to us. So we could give it to you.",
"Th-thank you!", "Well, it's yours now. Keep doing your best for all of us.", "I will!", "We're counting on you!",
],
57: [
"Aaaah!", "Oh no! Emilio! Are you all right?!", "Huh? Looks like the pier was rotten.", "Owww! It hurts!",
"Let me take a look.", "It hurts...", "You'd better not move it much. Let's get you to the inn for some rest.",
"Can't be helped. Here, Emilio. Hold on to me. ...Urgh! You're heavy!",
"I'm glad Emilio wasn't badly hurt! ...Oh, there's Arcadius.", "What's going on? Buying flowers?", "There's fruit, too.",
"Huh. Is it someone's birthday today?", "Hey, Arcadius! Are we having a party?", "Hm?",
"I saw you with flowers and some good-looking food. Come on, let me have some!",
"Oh, that? No, it's for Emilio. I'm going to visit him.", "Emilio? Why?", "Honestly, what are you two talking about?",
"We finally get to spend some time in town, and he can't even go out. He must be bored. That's why I'm visiting him.", "Huh.",
"Emilio likes sweet things, doesn't he? I don't know if he likes fresh flowers, but you can't get those at sea.",
"I see... So, if something happened to me... would you come visit me, too?",
"Of course. We're friends, aren't we?", "R-right... Yeah, we are...",
"N-no, it's fine. Forget it... Go on in.",
"All right... Would you like to come in too, Claudio? You might get some delicious fruit.",
"I'll pass. Let Emilio have it all. I'm sure he'll love it.", "Oh... All right, then.",
"Emilio, does your leg still hurt? I brought you a few things. Help yourself.",
"Wow, food! Thank you, Arcadius! Did you know I love flowers?",
"I didn't, actually. But I'm glad you like them. Have plenty to eat, all right?", "Hooray!",
"Oh, Clau... Were you waiting for me?", "Y-yeah... Come on, let's catch up with everyone. Let's go.",
"...All right.", "...",
],
58: [
"Admiral {MACRO:FA}, I presume?", "Oh! Who are you...?", "I used to lead the Uddin Company.", "I lead the Uddin Company.",
"Oh...! Admiral Uddin...", "You've swept across the Indian Ocean in no time. Just what I'd expect of Admiral {MACRO:FA}.",
"N-no... I was just lucky.", "There's no need to be so modest. Perhaps this, too, was meant to be.",
"Now then. I brought this for you. Please accept it as my final duty as steward of the Indian Ocean.", "Oh!",
"It's called the Evergreen Lotus Leaf. I'm told it reveals the location of the Indian Ocean's Proof of Conquest.",
"This... The leaf itself is a map...", "The Indian Ocean's Proof of Conquest should be a book called the Rigveda.",
"The Rigveda...", "I hope it proves worthy of you. Farewell.", "Huh. He's a decent fellow after all.",
"Admiral Uddin...", "Admiral Uddin... Thank you for everything. ...Goodbye.",
],
59: [
"Hold it! You there, Admiral!", "Do you mean me?",
"Yeah, you. Don't you know this whole area's the turf of Duarte Pereira, the Portuguese governor of Indochina?",
"...And?", "You'd better stay on his good side.", "...Thanks for the warning.",
],
}

SPECIAL = {
    (51,24): 'Keep the smile as a written gesture;do not invent spoken words.',
    (51,32): 'Retain the silent interval as an ellipsis;native FE layout remains pending without authored empty rows.',
    (51,75): 'Keep princess inside Rafael’s wondering speculation;do not establish a royal identity.',
    (54,35): 'Thank the older local naturally without turning おじさん into uncle.',
    (55,44): 'Keep the joke’s order:reward,unneeded gift,then revelation that the gift was already deducted.',
    (55,67): 'Keep Claudio’s accusation as conjecture rather than establish the false report as narrator fact.',
    (55,168): 'Retain Julio’s aging-body joke andfamiliar FI address without invented kinship.',
    (56,77): 'Retain collective town funding andthe pressure to sell;no theft orvoluntary donation invented.',
    (57,95): 'Friends conveys the reassurance of 仲間 in this exchange;it does not declare romance.',
    (57,119): 'Retain the comic food delight followed by the surprising genuine love of flowers.',
    (57,143): 'Keep Claudio’s silence unexplained rather than writing a confession orinner thought.',
    (58,25): 'Keep the former-leader introduction conditional anddistinct from the current-leader alternative.',
    (58,30): 'Keep current leadership conditional anddistinct from the former-leader alternative.',
    (58,68): 'Use the established global item label Evergreen Lotus Leaf;preserve the reported clue function.',
    (58,76): 'Use the established item name Rigveda for the source-named book.',
    (58,84): 'Preserve the direction of worthiness:the gift is hoped worthy of Rafael,not the reverse.',
}

if __name__ == '__main__':
    output = ROOT / 'B51_B59_146_logical_English_drafts_v1.json'; assert not output.exists()
    source = ROOT / 'B51_B60_source_identity_checkpoint_v1.json'; binding = load(source)
    names = {r['actor_ID']:next(c['text'] for c in r['current_consumers'] if c['consumer']=='progressive-nameplate') for r in binding['name_bindings']}
    item_path = Path('translations/all_item_names_arm9_v1.json'); item_doc = load(item_path)
    assert {r.get('english') for r in item_doc['records']} >= {'Rigveda','Evergreen Lotus Leaf'}
    records = []
    for block in range(51,60):
        rows = [r for r in binding['records'] if r['block']==block]
        assert len(rows)==len(DRAFTS[block])
        for row, english in zip(rows,DRAFTS[block],strict=True):
            assert '\n' not in english and '{LB' not in english and '{PAD}' not in english
            assert all(english.count('{MACRO:'+key+'}')==count for key,count in row['source_macros'].items())
            index = row['source_reference']['record_index']
            note = SPECIAL.get((block,index),'Natural complete-exchange wording preserves this source intent: '+row['source_meaning'])
            records.append(dict(**{k:v for k,v in row.items() if k!='review'},english=english,
                speaker=names[row['source_selector']] if row['source_selector']!=254 else 'System panel',
                context=row['whole_exchange_context'],localization_note=note,
                review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
                current_English_comparison_pending=True,complete_native_preamble_andfresh_formatting_pending=True))
    assert len(records)==146
    save(output,dict(format='dk4-clean-logical-English-drafts-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        source=str(source),source_sha256=sha(source.read_bytes()),item_terms=str(item_path),item_terms_sha256=sha(item_path.read_bytes()),
        records=records,logical_drafts_saved=146,current_story_English_for_these_exchanges_unconsulted=True,
        current_comparison_native_controls_display_andrelease_pending=True,
        name_artifact_findings=[dict(actor_ID=35,current_name=names[35],intended_name='Fernan Silveira',
            finding='Full-width Latin F in an otherwise ASCII name. Native source/fullname fields bound;exclusive ownership andglyph correction remain pending.')],
        no_new_name_data_orROM_orcompletion_credit=True,new_credit=0,guide_photos=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Saved146 logical English drafts;established Uddin/Rigveda/item labels kept,one Fernan full-width F finding queued;no credit.')
