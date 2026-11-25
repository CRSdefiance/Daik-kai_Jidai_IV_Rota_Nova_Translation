"""Draft Phidias’s chisel and both complete letters from clean Rafael source."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.draft_rafael_B241_B244_clean_v1 import ROOT
from scripts.seal_clean_independent_drafts_v1 import seal
from scripts.write_rafael_B221_B240_contextual_v1 import digest

CONTEXT = {
    245: 'Manuel tells Rafael about a scrap he found in the Alexandria library. It describes a chisel linked to Phidias and a rumor about where it lies. Rafael realizes Manuel is thinking of ship repair. Manuel answers with a wry remark about the Romans and an earnest defense of shipbuilding as an art.',
    247: 'Charles writes from West Africa. He reports a Spanish merchant convoy’s escape after an unearthly cry rallied its sailors, then distinguishes the account from what can be explained. The crew announces the letter in eight native voice slots. Keep the letter’s separate full signature.',
    248: 'Jam writes to the crew from India. His statue story turns into a joke about finally beating Fernando at gambling. He invites Rafael to look for it for other reasons and signs before putting out to sea. Fernando scoffs and Rafael is amused but curious. Keep the letter’s separate full signature.',
}
DATA = {
    245: {
        5: ('Manuel asks politely for a word.', 'Admiral, might I have a word?'),
        8: ('Rafael asks what it is.', 'What is it?'),
        13: ('Manuel found an interesting scrap of paper the other day in the library at Alexandria.',
             'Well, the other day I found an interesting scrap of paper in the library at Alexandria.'),
        17: ('Rafael asks what sort of scrap.', 'A scrap of paper? What was on it?'),
        22: ('The note described a mysterious chisel said to have been used by the legendary sculptor Phidias in ancient Greece.',
             'It described a mysterious chisel that Phidias, the legendary sculptor of ancient Greece, supposedly used to make his works.'),
        25: ('Rafael considers the chisel.', 'A chisel...'),
        30: ('People believe Phidias’s soul passed into the chisel after his death and gives its user miraculous ability in shaping forms.',
             "Yes. They say his soul passed into the chisel after he died. The belief is that anyone who uses it can sculpt with miraculous skill."),
        33: ('It is reportedly buried somewhere near Greece on the Balkan Peninsula. The scrap gives no exact location.',
             "The chisel is supposed to be buried somewhere on the Balkan Peninsula near Greece. The note doesn't say exactly where."),
        36: ('Rafael suspects Manuel wants to repair ships with the chisel.', "Manuel, you're not thinking of using that chisel to fix ships, are you?"),
        41: ('Manuel sees no harm. He says Rome once made a policy of using even kings as tools and jokes how grand that sounds.',
             "Why not? I hear the Romans once had a policy of making tools out of kings. A king for a tool! Now that's grand, isn't it?"),
        44: ('A ship is a fine work of art too, so better tools are worth having. Manuel asks him to look if the chance arises.',
             "A ship's a work of art in its own right. The finer the tools, the better. If you get the chance, have a look for it, would you?"),
    },
    247: {
        27: ('Charles is in West Africa and passes along a strange account he heard from sailors there.',
             "I am in West Africa at present. The sailors here told me a curious story that I thought I would pass along."),
        31: ('Very recently pirates attacked a Spanish merchant fleet on its way from the New World to West Africa.',
             '...Just the other day, pirates attacked a Spanish merchant fleet sailing from the New World to West Africa.'),
        35: ('Outmatched, the merchants tried to flee, but their slower ships seemed doomed to be wiped out.',
             'The merchants were badly outmatched. They tried to flee, but their ships were slower, and it seemed only a matter of time before the whole fleet was lost.'),
        38: ('Far offshore to the west of Lisbon, they say they heard a roar that seemed unearthly.',
             'But when they reached the open sea far west of Lisbon, they say they heard an unearthly roar.'),
        41: ('For some reason the sound rallied the sailors. They fought fiercely and stood up to the pirates.',
             'Something about that sound rallied the sailors. They fought like lions and held their own against the pirates.'),
        44: ('They held out until the Spanish navy happened past. The pirates scattered and the convoy escaped.',
             'They held out long enough for the Spanish navy to happen by. The pirates scattered, and the merchant fleet managed to escape.'),
        47: ('The sound’s true nature is still unknown, including whether science can explain it as a natural phenomenon.',
             'What the sound really was, or whether there is a scientific explanation for it as a natural phenomenon, is still unknown.'),
        50: ('Charles finds the story intriguing and suggests that the admiral might enjoy investigating. His full signature is on its own line.',
             'Still, it is a rather intriguing story. You might find it worth investigating. Charles Jean Rochefort'),
        57: ('Rafael calls it strange and admits it piques his interest.', "What a strange story. ...Hmm. It does make me curious."),
    },
    248: {
        27: ('Jam greets the admiral and everyone else and asks how they are doing.', 'Hey, Admiral! How is everybody doing?'),
        30: ('India impresses Jam more than he can say in a word. He remembers an interesting rumor.',
             "Boy, India's quite a place. I couldn't sum it up in a word if I tried... Oh, right. I heard an interesting rumor."),
        33: ('A statue of a supernatural beast made during the Gupta dynasty is said to show the future.',
             "It's about a statue of a mythical beast from the Gupta dynasty. Supposedly the thing can see into the future."),
        36: ('Jam knows it sounds dubious, but figures anything could happen in India and it might be true.',
             "Sounds fishy, right? But this is India. Nothing would surprise me here. It might even be true."),
        39: ('Jam wonders if it could help him beat even Fernando at gambling, then asks if he is being naive.',
             "I figured with that thing, I might even beat Fernando at gambling. Wishful thinking, huh?"),
        42: ('Jam cannot find it for sale or meet anyone who has actually seen it.',
             "Trouble is, nobody's selling it, and I can't find anybody who's even seen it."),
        46: ('Jam suggests Rafael look if free. It might be useful for other things besides gambling.',
             "Admiral, how about looking for it if you've got some time? I mean, even if you don't use it to gamble, it could come in handy, right?"),
        49: ('Jam needs to sail soon, wishes the crew luck finding the treasure, says goodbye, and signs on a separate row.',
             "Oops, I'd better put out to sea soon. Hope you find the treasure. See you around. Jam Jack Ludwyan"),
        64: ('Fernando scoffs that Jam is five hundred years too early if he thinks he can beat him with that thing.',
             "Hah! He thinks he can beat me with that thing? Give him another five hundred years."),
        70: ('Jam is the same in a letter as ever. Rafael finds the story of the statue odd enough to consider looking.',
             "Even in a letter, Jam's still Jam. ...But it does sound like a strange statue. Maybe I'll look for it sometime."),
    },
}
VOICE = [
    ('Attentively announces the letter.', 'Admiral, a letter came in from {name}.'),
    ('Announces the correspondence formally.', 'Admiral, we have received a letter from {name}.'),
    ('Gives a plain announcement shared by two voice slots.', "Admiral, there's a letter from {name}."),
    ('Politely tells the admiral a letter has come for them.', 'Admiral, a letter for you from {name}.'),
    ('Casually tells the admiral they have a letter.', "Admiral, you've got a letter from {name}."),
    ('Calls attention to the letter in an older voice.', "Here's a letter from {name}, Admiral."),
    ('Calls out the news in a youthful voice.', 'Admiral! {name} sent you a letter!'),
]


def main():
    speech = ROOT/'B245_B248_clean_speech_drafts_v1.json'
    style_path = ROOT/'clean_style_objects.json'
    out = ROOT/'B245_B248_clean_drafts_v1.json'
    assert not out.exists()
    seal(ROOT, speech.name, DATA, CONTEXT, {}, __file__, 30)
    prose, styles = map(load, (speech, style_path))
    alternatives = []
    for block, sender in ((247,'Charles'),(248,'Jam')):
        source = [row for row in styles['records'] if row['block'] == block]
        for voice, (row, (meaning, draft)) in enumerate(zip(source, VOICE, strict=True)):
            assert row['source_style_indices'] == ([2,7] if voice == 2 else [voice])
            assert not any(row['source_macros'].values())
            alternatives.append({**row,'source_meaning':meaning,'independent_English':draft.format(name=sender),
                'context':CONTEXT[block], 'speaker':'Runtime-selected crew voice. Exact identity binding pending.',
                'review':dict(source=False,context=False,localization=False,naturalness=False,formatting=False),
                'current_English_comparison_pending':True,'complete_native_style_binding_andformatting_pending':True,
                'native_literal_token_counts':{},'new_credit':0})
    assert len(alternatives) == 14
    records = prose['records'] + alternatives
    assert len(records) == len({row['id'] for row in records}) == 44
    save(out, {**prose, 'records':records,'records_count':44,'physical_style_alternatives':14,
        'style_alias_slots':16,'prior_reviewed_B246_retained_as_context_only':True,
        'evidence':{**prose['evidence'],str(speech):digest(speech),str(style_path):digest(style_path)}})
    print('Sealed 44 clean-only drafts across B245, B247 and B248.')


if __name__ == '__main__':
    main()

