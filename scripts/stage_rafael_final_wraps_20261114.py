"""Review the remaining flagged wraps on Rafael's route."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import register_rafael_quest_wraps_20261114 as parent
from scripts import stage_rafael_quest_wraps_20261114 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, sha, prior = previous.base, previous.sha, previous.prior
FILE, ARM, CLEAN, IlnkContainer = previous.FILE, previous.ARM, previous.CLEAN, previous.IlnkContainer
ROOT = Path('work/rafael_final_wraps_20261114_v1')
CAPTURE = ROOT / 'rafael_startup/capture_report.json'
RUNTIME = ROOT / 'rafael_native_context.json'
REVIEW = parent.TRIAGE.with_name('rafael_final_wraps_context_v1.json')
PROOF = ROOT / 'stored_and_native.json'
SIGNED_LETTER = (235, 48)

DECISIONS = {
    SIGNED_LETTER: ('Ian', None,
        'Ian politely suggests Rafael look into the matter if it interests him, then signs the letter.',
        'The wording suits his understated invitation. Keep the break between the condition and question, and the indented signature on its own row as in the clean letter.',
        ('If it interests you,', 'why not look into it?', 'Ian Dukov')),
    (312, 234): ('Rafael', "Really? The map says this is the right way. Let's keep going.",
        'Rafael doubts they are off course because the map indicates this direction, so he decides to continue.',
        'Keep his mild uncertainty and use a complete instruction after the map reading.',
        ('this is the right way.', "Let's keep going.")),
    (313, 22): ('Safia', "I only just started. I'm not very good yet. I danced for a customer once. Guess word got back to the lord...",
        'Safia says she has only just begun and is no expert. She happened to show a customer her dancing, and word apparently reached the lord.',
        'Make the thing she showed explicit and keep her modesty and uncertainty before the rumor grows out of hand.',
        ("I'm not very good yet.", 'I danced for a customer once.', 'word got back to the lord...')),
    (314, 21): ('Safia', "A mosque far inland honors a king from long ago. They say it holds quite a treasure.",
        'Safia tells Rafael about a mosque far inland that honors a former king and is rumored to hold a wonderful treasure.',
        'Treat the treasure as hearsay. Her next line explains who is said to be worthy of taking it.',
        ('a mosque far inland', 'a king from long ago.', 'They say it holds quite a treasure.')),
    (316, 18): ('Rafael', "One of the missing explorers!",
        'Rafael confidently takes the cry for help to be the voice of one of the lost explorers.',
        'Keep the immediate recognition after the cry and Claudio’s call to the explorer.',
        ('the missing explorers!',)),
    (317, 6): ('Barkeep', "...That's what I figured.",
        'The barkeep says the report confirms his suspicion.',
        'Use a quiet confirmation before Rafael asks how they can appease the king.',
        ("That's what I figured.",)),
    (317, 103): ('Claudio', "Wait. Are we entertaining a guest? No, this is more like babysitting. Is that really gonna work?",
        'Claudio likens the proposal first to entertaining a guest and then to babysitting, and doubts it will work.',
        'Keep his comic self-correction and colloquial doubt. The barkeep answers that sincerity is what matters.',
        ('entertaining a guest?', 'more like babysitting.', 'Is that really gonna work?')),
    (318, 79): ('Rafael', "...Guess that's the wrong scent.",
        'Rafael thinks the scent is wrong after the spirit rejects the attempt.',
        'Keep the tentative conclusion and refer to the scent as in the incense sequence.',
        ("that's the wrong scent.",)),
    (318, 141): ('Al', "'Praise be to Allah, Lord of heaven and earth. And our leader, foremost among those sent to earth...'",
        'Al reads a formal invocation praising Allah as Lord of heaven and earth, then begins a reference to the leader of those sent to earth.',
        'Preserve Allah, the devotional register, the leadership wording and the unfinished quotation. The next reading gives the tale’s title.',
        ('Praise be to Allah,', 'Lord of heaven and earth.', 'And our leader,', 'those sent to earth...')),
    (318, 151): ('Rafael', "'Scheherazade said, O fortunate king, I have heard that long ago...'",
        'The reading quotes Scheherazade addressing the fortunate king and introducing what she heard happened long ago.',
        'Keep the name, ceremonial address and unfinished opening. The existing breaks separate the attribution and the trailing story cue from the formal address.',
        ('Scheherazade said,', 'O fortunate king,', 'that long ago...')),
    (318, 176): ('Explorer', "Thank goodness! We can finally go home!",
        'The explorer voices relief that they can at last go home.',
        'Keep the release of tension on learning the curse is lifted. He goes on to put survival ahead of treasure.',
        ('We can finally go home!',)),
    (321, 22): ('Sakura', "Speaking of India, have you heard of chintz? A beautiful fabric, I hear. Expensive, too.",
        'The mention of India reminds Sakura of chintz, which she has heard is a beautiful luxury fabric.',
        'Keep the established fabric name and describe its beauty and value as the information she heard.',
        ('have you heard of chintz?', 'A beautiful fabric, I hear.', 'Expensive, too.')),
    (322, 51): ('Rafael', "All right. How about I tell you about my home in the Mediterranean?",
        'Rafael agrees to tell Sakura about his home in the Mediterranean.',
        'Answer her request for more stories, and keep the Mediterranean as the place he calls home.',
        ('How about I tell you', 'about my home', 'in the Mediterranean?')),
    (322, 68): ('Rafael', "You're a curious one, aren't you? Next time I buy some wine, I'll bring you a taste.",
        'Rafael teases Sakura about her curiosity and offers to bring her some wine the next time he buys it.',
        'Keep the affectionate teasing and the purchase condition after her question about wine and sake.',
        ("You're a curious one, aren't you?", "I'll bring you a taste.", 'next time I buy some wine,')),
    (325, 265): ('Rafael', "My hand slipped... I'm sorry. I'm so sorry!",
        'Rafael blames himself for losing his grip and apologizes emphatically.',
        'Keep personal responsibility and both apologies so distress builds through the fallen-person branch.',
        ('My hand slipped...', "I'm sorry.", "I'm so sorry!")),
    (330, 37): ('Verisa', "I hear pirates have been running wild around here lately. Make sure you've got the right equipment.",
        'Verisa has heard of recent pirate activity in the area and urges the crew to equip themselves properly.',
        'Keep the warning as a report and the practical gear advice before Rafael promises to take care.',
        ('pirates have been running wild', 'around here lately.', 'the right equipment.')),
    (331, 26): ('Verisa', "There are ruins deep in the desert, far inland. I'm sure you'll find what you're looking for there.",
        'Verisa locates ruins far inland in the desert and expresses confidence that Rafael will find what he seeks there.',
        'Keep both the distance and the reassurance, a change from the brief silence just before this speech.',
        ('deep in the desert,', 'far inland.', "what you're looking for there.")),
    (332, 177): ('Rafael', "It's a cliff. We have to go around.",
        'The cliff leaves no option but a detour.',
        'Keep the matter-of-fact decision after the injury and fatigue reports. The following notice advances the day.',
        ('We have to go around.',)),
    (333, 152): ('Rafael', "All right, let's light a fire...",
        'Rafael decides to light a fire and trails off.',
        'Keep the tentative action cue. It is interrupted when the bats appear.',
        ("let's light a fire...",)),
    (334, 81): ('Villager', "We're here. We continue overland.",
        'The guide announces they have arrived and says they will continue by land.',
        'Let the guide signal the change of travel mode after the day passes and before they spot the site.',
        ('We continue overland.',)),
    (335, 9): ('Isabel', "Ever visited a village way up north in the New World?",
        'Isabel asks whether Rafael has visited a village in the far north of the New World.',
        'Keep her casual opening and the geographic clue before she tells the story of the missing monk.',
        ('way up north', 'in the New World?')),
    (336, 66): ('Villager', "It's an imposition, I know. Even so, I have to ask.",
        'The speaker acknowledges the imposition and makes the request despite it.',
        'Keep his deference after Claudio voices reservations and before Rafael agrees to try.',
        ("It's an imposition, I know.", 'Even so, I have to ask.')),
    (336, 89): ('Rafael', "Those ruins may hold a key to the Proof. Don't you think it's worth a try?",
        'Rafael thinks the ruins might hold a key to the Proof and that taking the chance is worthwhile.',
        'Keep it a possibility. The line invites agreement, which Arcadius and Claudio give.',
        ('a key to the Proof.', "Don't you think it's worth a try?")),
    (336, 109): ('Villager', "Thank you. Let's get started...",
        'The man thanks the crew and proposes starting at once.',
        'The brief form suits his immediate shift from thanks to the task. Keep the trailing transition.',
        ("Let's get started...",)),
    (336, 112): ('Villager', "First, a test of your swordplay. I need you to find something.",
        'The man has an object for Rafael to find as a test of his swordsmanship.',
        'Maintain the purpose and the delayed reveal. Rafael asks what it is before the man names the Tlaloc Knife.',
        ('a test of your swordplay.', 'I need you to find something.')),
    (341, 6): ('Villager', "This is what you're looking for?",
        'The villager confirms that the visitors came in search of the object.',
        'Keep a direct question before the villager reflects on the long wait and offers them the object.',
        ("what you're looking for?",)),
    (342, 78): ('Charles', "I found out I need the Alchemy Book to get that material, but...",
        'Charles’s research established that obtaining the material requires the Alchemy Book, but his account is unfinished.',
        'Keep the specific book, the unfinished thought and his excited train of thought before he mentions the clue to the metal.',
        ('the Alchemy Book', 'to get that material, but...')),
    (342, 118): ('Villager', "...Can I entrust you with this book?",
        'The villager asks if the visitors may be entrusted with the book.',
        'Keep the deliberate word “entrust” for the next speaker’s echo and the hesitant silence before it.',
        ('entrust you with this book?',)),
}


def signed_letter_layout(row):
    """Retain the source-specific signed-letter presentation byte for byte."""
    stored = bytes.fromhex(row['current_hex'])
    source_lines = row['source_Japanese'].splitlines()
    assert len(source_lines) == 3 and source_lines[-1] == '\u3000' * 9 + 'イアン・ドゥーコフ'
    assert stored == b"\x15If it interests you,\nwhy not look into it?\n                   Ian Dukov "
    lines = stored[1:].decode('ascii').splitlines()
    return dict(id=row['id'], source_kind='progressive-signed-letter', source_hex=row['source_hex'],
                English=row['english'], formatted_markup=stored[1:].decode('ascii'),
                lines=[line.strip() for line in lines], line_lengths=[len(line) for line in lines],
                encoded_hex=stored.hex(), diagnostics=[], expected_native_pages=1, native_rows_per_page=4,
                all_words_punctuation_and_macro_order_preserved=True, automatic_boundaries=[],
                manual_break_reason='Independently preserve the indented letter signature and the clause boundary before it.')


get_exchanges = FunctionType(previous.get_exchanges.__code__, previous.get_exchanges.__globals__ | globals())
compile_source = checked_text(getsource(previous.compile_rows), {
    '        layout = plan(row)': '        layout = signed_letter_layout(row) if (block, index) == SIGNED_LETTER else plan(row)',
})
env = previous.compile_rows.__globals__ | globals() | {'previous': previous.compile_rows.__globals__['previous']}
exec(compile(compile_source, __file__ + '::source-bound-signature', 'exec'), env)
compile_rows = env['compile_rows']
bind_runtime = FunctionType(previous.bind_runtime.__code__, previous.bind_runtime.__globals__ | globals())
main = FunctionType(previous.main.__code__, previous.main.__globals__ | globals())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true')
    main(parser.parse_args().preview)
