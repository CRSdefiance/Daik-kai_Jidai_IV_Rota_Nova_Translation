"""Localize complete source exchanges, preserving optional dialogue and explicit uncertainty."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104')
DRAFTS={
38:[
    "Admiral! It's a Spanish fleet!",
    "You Portuguese brats! Is it true you've joined forces with pirates to defy the Kingdom of Spain?!",
    "What?! Where did you hear that?",
    "Well? Depending on your answer, hundreds of cannon may open fire on that pitiful fleet of yours!",
    "Ugh... Doesn't look like we can bluff our way out of this one.",
    "This is bad. We might not be strong enough to win yet...",
    "Hah! Come and get us!",
    "Hmm. The strength doesn't quite match the bravado...",
    "Admiral! We've spotted another fleet!",
    "Is this it for us?!",
    "Ah?!",
    "Ah?!",
    "Pedro. Do you really think I need children to help me deal with the likes of you?",
    "Hayreddin!!",
    "Grr! You... Barbarossa!!",
    "If you've nothing better to do, I'll give you someone to play with.",
    "...The Algiers pirates mean to make an enemy of the Spanish navy?",
    "Who you are makes no difference. Any fool who sails through these waters is fair game for us.",
    "...Tch!",
    "You're in the way. Go.",
    "Thank you!! All right, everyone! Full speed! We're leaving these waters!",
    "Now then... Shall we begin?",
    "Grr... Barbarossa! I'll withdraw this time, but I'll make you regret making an enemy of us!",
],
39:[
    "Admiral, is that a Dutch merchant ship over there? It seems to be signaling us.",
    "Hmm. What could it be? Can you make it out?",
    "Aye! I'll decode the signal!",
    "Admiral {MACRO:FI}, that ship over there... Is it a Dutch merchantman? It seems to be signaling us.",
    "Hmm. Can you make it out, Janus?",
    "Let's see... I'll try decoding the signal.",
    "A fight?! Now we're talking!",
    "Barbarian...",
    "Huh? You say something?",
    "Oh, you heard that?",
    "Clau! We aren't traveling the world just to pick fights with everyone!",
    "Yeah, yeah, Admiral {MACRO:FI}. I know.",
    "So, what does it say?",
    "They're telling us to dock at Amsterdam!",
    "Ah, I've got it... They seem to be telling us to dock at Amsterdam. What shall we do?",
    "Hmm. What should we do?",
    "Shall we call at Amsterdam and see?",
    "It's suspicious... But I'd rather comply than risk an ambush out here.",
    "(Huh. Arcadius has a good head for strategy, too.)",
    "Their fleet's not all that big, is it? Forget 'em. We'll force our way through!",
    "I'll count on you if it comes to that, Clau. But...",
    "Let's be cautious here. We'd better call at port.",
],
40:[
    "Well. You've grown stronger.",
    "H-Hayreddin...!",
    "You've exceeded my expectations. Ready to make your bid for the Mediterranean at last, are you?",
    "...Yes. I don't know how it'll turn out yet, but that's my intention.",
    "...The Ottoman Pasha forces are powerful. You understand that?",
    "...Of course.",
    "I see... Then stop by the... dock in Algiers.",
    "What?",
    "I'll show no mercy when we next meet for battle.",
    "Th-that's just what I want!",
    "Ha ha ha! That's a good look in your eyes!",
],
41:[
    "Hey, Hans. Isn't it about time we found a lead on that Proof in Africa?",
    "Impatience will get you nowhere.",
    "But... how should we go about looking for a lead?",
    "First and foremost, you need strength worthy of someone who would rule the seas. Without it, the Proof will never reveal itself to you.",
    "Strength? You mean having a huge fleet?",
    "Or... becoming an accomplished navigator?",
    "Perhaps he means financial strength.",
    "Hmm... Could it mean having a great trading sphere?",
    "Everyone has a different interpretation. Perhaps it means all of those things.",
    "Wow... That sounds like a long way off.",
    "But strength alone is not enough.",
    "What?! There's more?",
    "This is only my own theory, mind you...",
    "I believe the secrets of the Proofs are likely sealed within ruins around the world.",
    "Ruins...?",
    "Indeed.",
    "Where would we find those ruins?",
    "In or near the great cities at the heart of each cultural region, I should think.",
    "That still doesn't tell us how we're supposed to find them.",
    "Some of the people who live there should know. First, you must earn the townspeople's trust.",
    "Their trust...?",
    "Ruins and old churches are symbols of their religion and culture. They won't readily share their locations with outsiders like us.",
    "Listen to the townspeople's requests. Help those in difficulty. If corrupt merchants or military men are making them suffer, put those villains in their place...",
    "Huh... Sounds like charity work.",
    "In any case, someone who would rule the seas needs the character to earn the trust of many people.",
    "Whew... Becoming a ruler of the seas sounds like hard work.",
    "Ho ho ho! Naturally. No one has managed it yet, after all.",
],
}

if __name__=='__main__':
    output=ROOT/'B38_B41_83_logical_English_drafts_v1.json'
    assert not output.exists()
    source=ROOT/'B36_B41_175_complete_clean_meanings_v1.json'
    binding=ROOT/'B36_B41_source_identity_andFU_checkpoint_v1.json'
    terminology=Path('translations/rafael_B48_contextual_final_review_v1.json')
    approved=load(terminology)
    examples=[r for r in approved['records'] if r['id'] in ['DK4_MES_B48_R0071','DK4_MES_B48_R0092','DK4_MES_B48_R0370']]
    assert len(examples)==3 and all('Proof' in r['english'] for r in examples)
    gloss,identities=map(load,[source,binding])
    names={r['actor_ID']:r['text'] for r in identities['current_consumer_bindings'] if r['consumer']=='progressive-nameplate'}
    rows=[]
    for block in [38,39,40,41]:
        originals=[r for r in gloss['records'] if r['block']==block]
        assert len(originals)==len(DRAFTS[block])
        for row,english in zip(originals,DRAFTS[block],strict=True):
            assert '\n' not in english and '{LB' not in english and '{PAD}' not in english
            assert all(english.count('{MACRO:'+m+'}')==row['source_macros_complete'][m] for m in ['FI','FA','FO','FU'])
            note='Complete-exchange natural American English drafted from clean Japanese; source companion branches, facts and uncertainty retained. No authored wrapping or allocation-driven shortening. Current-English comparison and formatting remain pending.'
            if block==40:note+=' Later rematch chronology is not represented as first-voyage activation. Pasha identifies the Ottoman force, not Janus Pasar.'
            if block==41:note+=' Proof uses the established B48 shorthand for Proof of Conquest; the broader terminology question stays separate. Rule the seas renders the nautical ambition of 覇者 without assigning a formal rank.'
            if row['id']=='DK4_MES_B39_R0112':note+=' Internal thought uses Arcadius by name and adds no gender inference.'
            rows.append(dict(**row,english=english,speaker=names[row['source_selector']],context=row['exchange_context'],
                localization_note=note,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
                current_English_comparison_pending=True))
    assert len(rows)==83
    save(output,dict(format='dk4-clean-logical-English-drafts-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        source=str(source),source_sha256=sha(source.read_bytes()),identity_binding=str(binding),identity_binding_sha256=sha(binding.read_bytes()),
        existing_Proof_terminology_reference=str(terminology),existing_Proof_terminology_reference_sha256=sha(terminology.read_bytes()),
        existing_Proof_examples=[dict(id=r['id'],source_reference=r['source_reference'],english=r['english']) for r in examples],
        blocks=[38,39,40,41],records=rows,logical_drafts_saved=83,current_ROM_English_for_these_four_exchanges_not_consulted=True,
        current_comparison_andfresh_formatting_andrelease_pending=True,new_credit=0,guide_photos=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('83 complete-exchange drafts saved;approved Proof shorthand/conditional companions/uncertainty preserved.')
