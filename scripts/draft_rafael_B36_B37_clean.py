"""Localize the complete pirate encounters independently of current English dialogue."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104')
DRAFTS={
36:[
    "Admiral! We've sighted what looks like an enemy fleet!",
    "What could that fleet be?",
    "Pirates?",
    "I hope this doesn't mean trouble.",
    "If they're pirates, we won't be able to avoid a fight.",
    "Hm?! Those are the Algiers pirates... Could it be him?",
    "The Algiers pirates?",
    "They raid around Algiers, using the North African coast as their base.",
    "So they are pirates!",
    "Aw, come on! Trouble already?!",
    "And... yes, it is him! Barbarossa Hayreddin!",
    "Is he strong?",
    "Hayreddin's men stand head and shoulders above the other Algiers pirates! They're immensely powerful, and utterly merciless...!",
    "You're kidding, right?!",
    "They say even the Ottoman Turks have a hand in his activities. They're the strongest power in the Mediterranean right now.",
    "So these guys guard the entrance, and their boss sits at the far end of the Mediterranean!",
    "If we're to trade in the Mediterranean, we'll first have to find some way of dealing with him. He controls Gibraltar...",
    "Whew. We've got quite a road ahead of us.",
    "For now, we'd best worry about getting out of this.",
    "Sure, but how?",
],
37:[
    "Admiral {MACRO:FI}, what shall we do?",
    "Julio, I heard the Algiers pirates and Spain don't get along...",
    "They prey chiefly on Spanish ships. I expect they'll clash with Admiral Valdes, commander of the royal navy, before long.",
    "And I've heard Spanish pressure has been making it harder for Portuguese fleets to trade lately...",
    "Maybe we can work something out, since we have the same enemy? You know, the enemy of my enemy is my friend?",
    "Aw, come on. You're being naive! These are pirates!",
    "Oh dear. This doesn't look good...",
    "You there! What are you doing in the southern Mediterranean?!",
    "Ugh! They've spotted us!",
    "Well, how are we going to get out of this?",
    "I hear he's a proud man. Looking ready to run may only make us easier prey. Best to face him with our heads held high.",
    "Heads held high...? ...All right. Ahem.",
    "We are... Portuguese voyagers sailing the world under the banner of defeating Spain and restoring Portugal...",
    "We are {MACRO:FO}!",
    "And I am Admiral {MACRO:FU}!",
    "Oh! Very impressive!",
    "Bravo! Bravo! (Clap, clap, clap!)",
    "Are you an idiot?! We'll kill you all!!",
    "Oh, that didn't work... We're done for...",
    "Wait, Salid.",
    "You said something about defeating Spain, did you?",
    "Y-yes, we did.",
    "Ha ha ha! How entertaining! You mean to take on the Spanish Armada? Ha ha ha!",
    "W-what's so funny?!",
    "...You'd do well to watch your mouth.",
    "Clau! Leave this to {MACRO:FI}. Come now, this is your chance to show what our leader can do. Good luck!",
    "Hmph... Fine. Good luck, {MACRO:FI}.",
    "All right. It's a gamble, but... Here goes.",
    "Hey, where'd all that bravado go? If you mean to beat the Armada, you must at least be ready to stand against us!",
    "Th-that's exactly right!",
    "Quite a bold claim. But try it as you are now, and it'll get you killed.",
    "Exactly! Now is not the time!!",
    "What?",
    "Ha ha ha! Then when will the time be right?",
    "We'll gain experience and train! We'll become strong enough to face even you on equal terms!",
    "Ha ha ha! Who'd be fool enough to stand by and let someone else rise to power?",
    "The Algiers pirates are more timid than I'd heard. Afraid you won't be able to beat us once we're stronger?",
    "What did you say?!",
    "Then let us travel freely through these waters! One day, we'll defeat the Spanish Armada!",
    "You little...! Don't push your luck!!",
    "You... You called yourself {MACRO:FI}, didn't you?",
    "Ha ha ha! Entertaining! Very entertaining, youngster!",
    "Admiral!",
    "Very well. Explore, trade, and gain the strength to live up to those words. When you're ready, I'll take you on.",
    "Admiral Hayreddin!",
    "Do you expect me to take fledglings like these seriously?",
    "What? N-no, I...",
    "It's fine. A game like this could be entertaining now and then.",
    "...Yes, sir. Understood.",
    "You may travel through the Mediterranean. But do your trading in other seas.",
    "W-what?",
    "Do you think you can handle angering both Valdes of Spain and the Ottoman Turks? Neither is as forgiving as I am.",
    "If you aspire to rule the Mediterranean, make a name for yourselves elsewhere first. I have no patience for needless trouble.",
    "Let's see... One more thing...",
    "Y-yes?",
    "If Spanish ships attack you, my fleet will come to your aid. But only in our waters.",
    "What?! Really?!",
    "Don't count on it every time. I'm a busy man, you know.",
    "Th-thank you!!",
    "Of course, encroach on our territory and I'll take it as a challenge. I'll show no mercy.",
    "O-of course!",
    "Hmph. Perhaps you could...",
    "No, never mind... Grow strong enough to entertain me. And make very sure you keep your promises.",
    "...I understand. You have my word.",
    "Good. We're leaving, men!",
    "Aye!",
    "That was some bluff! You've got guts, {MACRO:FI}!",
    "That's quite a promise you secured.",
    "Whew... I surprised myself. Now that it's over, I'm starting to feel scared.",
    "Heh. Maybe you're the kind who comes through when it counts.",
    "Splendid!",
    "Thanks, everyone. But after all that talk, I'd better work hard and get stronger.",
],
}

if __name__=='__main__':
    output=ROOT/'B36_B37_92_logical_English_drafts_v1.json'
    assert not output.exists()
    source=ROOT/'B36_B41_175_complete_clean_meanings_v1.json'
    binding=ROOT/'B36_B41_source_identity_andFU_checkpoint_v1.json'
    gloss,identities=map(load,[source,binding])
    assert gloss['all175_meanings_saved_before_current_English_dialogue_comparison'] and identities['FU_expands_complete_full_name_not_first_name']
    names={r['actor_ID']:r['text'] for r in identities['current_consumer_bindings'] if r['consumer']=='progressive-nameplate'}
    rows=[]
    for block in [36,37]:
        originals=[r for r in gloss['records'] if r['block']==block]
        assert len(originals)==len(DRAFTS[block])
        for row,english in zip(originals,DRAFTS[block],strict=True):
            assert '\n' not in english and '{LB' not in english and '{PAD}' not in english
            assert all(english.count('{MACRO:'+m+'}')==row['source_macros_complete'][m] for m in ['FI','FA','FO','FU'])
            note='Whole-exchange localization preserves the danger, bluff, conditional agreement and relief. No authored wrapping or allocation-driven shortening. Current English dialogue comparison and all formatting remain pending.'
            if row['id']=='DK4_MES_B37_R0099':note+=' FU remains the complete full-name substitution; its measured 13-byte default is not replaced with FI.'
            rows.append(dict(**row,english=english,speaker=names[row['source_selector']],context=row['exchange_context'],
                localization_note=note,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
                current_English_comparison_pending=True))
    assert len(rows)==92
    save(output,dict(format='dk4-clean-logical-English-drafts-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        source=str(source),source_sha256=sha(source.read_bytes()),identity_binding=str(binding),identity_binding_sha256=sha(binding.read_bytes()),
        blocks=[36,37],records=rows,logical_drafts_saved=92,current_ROM_English_dialogue_not_consulted=True,
        current_comparison_andfresh_formatting_andrelease_pending=True,new_credit=0,guide_photos=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('92 whole-exchange logical drafts saved;native identities/FI/FO/FU preserved;current-English comparison still pending.')
