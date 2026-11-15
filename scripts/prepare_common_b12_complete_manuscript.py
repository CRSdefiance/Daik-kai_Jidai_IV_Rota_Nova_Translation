"""Review every B12 native message from clean Japanese for full fidelity."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_common_printf_late_manuscript import TEXT as LATE_TEXT

TEXT = {
    958: ("In %s, spread bad rumors about %s. Is that right?", "Confirms spreading damaging rumors in the first town about the second party."),
    959: ("In %s, I should spread bad rumors about %s, correct?", "Confirms the speaker should spread damaging rumors, town first and target second."),
    960: ("In %s, shall I spread bad rumors about %s?", "Asks whether to spread damaging rumors in the first town about the second party."),
    961: ("In %s, spread bad rumors about %s, is that right?", "Older voice confirms spreading damaging rumors, town first and target second."),
    962: ("In %s, say %s is a terrible person. That's the rumor to spread, right?", "Youthful confirmation of a rumor calling the second party terrible in the first town."),
    963: ("In %s, we are to spread bad rumors about %s, correct?", "Formal older confirmation of damaging rumors, town first and target second."),
    973: ("Which town's broker shall we bribe?", "Formal question selecting the town whose broker will be bribed."),
    976: ("Which town's broker are we to bribe?", "Older question selecting a broker by town."),
    977: ("Which town's broker should we bribe?", "Youthful broker-bribery town selection; phonetic Japanese wording does not change the act."),
    978: ("In %s, bribe %s's broker. Is that your order?", "Confirms broker bribery with the first place and second affiliation in source order; actual values still need classification."),
    979: ("In %s, we are to bribe %s's broker. Is that correct?", "Formal confirmation of bribing the second affiliation's broker in the first place."),
    980: ("In %s, we're bribing %s's broker. Is that right?", "Informal confirmation of broker bribery, retaining source argument order."),
    981: ("In %s, I should bribe %s's broker. Is that right?", "Rough voice confirms the broker-bribery order, retaining source argument order."),
    982: ("In %s, bribe %s's broker. Is that your order?", "Older broker-bribery confirmation, retaining source argument order."),
    983: ("In %s, we're bribing %s's broker. Is that right?", "Youthful broker-bribery confirmation, retaining source argument order."),
    985: ("With this crowd, we can't talk privately. Let's try another day.", "Crowds prevent a confidential conversation; proposes another day."),
    986: ("Admiral, with this crowd, we can't talk privately. Let's come back another day.", "Addresses the admiral; crowds prevent confidential conversation; proposes another day."),
    989: ("I'm %s. You're %s? I'll remember your name. Come by anytime. You're always welcome!", "The speaker gives their name, learns and remembers the listener's name, and welcomes future visits."),
    990: ("%s? What a nice name! I'm %s. It's a pleasure to meet you.", "Compliments the listener's name before introducing the speaker and offering a friendly greeting."),
    991: ("Are you rich? I'm jealous! I wish I could find someone nice and be happy soon.", "Asks about wealth, expresses envy, and wishes to find a good romantic match and happiness soon."),
    992: ("Listen to my song. It's called fado. La la la...", "Invites the listener to hear a fado song and begins singing."),
    993: ("I fall in love so easily, and it always goes wrong.", "The speaker falls in love readily but repeatedly has disappointing outcomes."),
    994: ("Sorry, I must head home early today. My younger siblings are waiting for me.", "Apologizes for leaving early today because younger sisters and brothers await at home."),
    995: ("It's such a nuisance when people get drunk and fall asleep.", "Complains about people who get drunk and fall asleep."),
    996: ("Sailors risk their lives. I admire them! I must work harder too, so my parents can have an easier life.", "Admires sailors risking their lives and resolves to work harder to ease the parents' lives."),
    997: ("My age? Hehe... How old do I look?", "Playfully asks the listener to guess the speaker's age."),
    1000: ("You're giving me something this expensive? Oh, thank you!", "Surprised and grateful to receive such an expensive gift."),
    1001: ("Oh, thank you... You shouldn't trouble yourself.", "Thanks the listener while saying they need not strain themselves for the gift."),
    1002: ("Are you calling me Venus? Hehe... I like the sound of that.", "Playfully accepts a flattering comparison to Venus."),
    1003: ("Let's drink and have some fun!", "Invites lively drinking and celebration."),
    1004: ("I always walk in the garden on holidays. The flowers and trees cleanse my heart.", "Always strolls in the garden on holidays and feels spiritually refreshed by flowers and trees."),
    1005: ("I baked a pie. Stay and have some!", "Offers some freshly baked pie and invites the listener to stay."),
    1006: ("I can't stand stingy people. You're not like that, are you?", "Strongly dislikes stinginess and asks whether the listener is different."),
    1007: ("La la la... The woman in this song awaits her lover's return from sea. Loving a sailor is so hard...", "Sings, explains that the song concerns a woman awaiting her seafaring lover, and laments loving a sailor."),
    1008: ("Hey, tell me about foreign lands!", "Eagerly asks for stories about other countries."),
    1009: ("I love this town. It's always lively! Gloomy towns get me down.", "Likes this town because it is lively and feels depressed by gloomy towns."),
    1010: ("Exploring ruins sounds like fun. Seeing ancient culture and everyday life seems rather romantic.", "Finds investigating ruins appealing and glimpses of ancient culture and life romantic."),
    1011: ("Some people know nothing of fashion. I'd hate to walk beside them.", "Dislikes being seen walking with people ignorant of current fashion."),
    1012: ("You're wonderful... Strong, kind...", "Admires the listener's strength and kindness."),
    1013: ("If something's troubling you, shall I tell your fortune? Oh, you have no worries?", "Offers fortune-telling for worries, then reacts to the listener having none; no invented card method."),
    1014: ("Tired, aren't you? I'll indulge your whims... just a little.", "Flirtatiously offers to indulge the tired listener a little."),
    1015: ("Men sail while women stay home? That's outdated! Don't you think women should enter public life too, now that times are changing?", "Rejects the old division of seafaring men and homebound women, advocating women entering society in the coming era."),
    1017: ("Sailors are so wonderful! Have you seen dolphins? What about whales?", "Admires sailors and asks whether the listener has seen dolphins and whales."),
    1018: ("Tell me about pirates! What ships do they sail? Are they really strong?", "Requests pirate stories, asking about their ships and strength."),
    1019: ("Animals are being hunted for their fur lately. Why do people do such cruel things?", "Questions the cruelty of recent animal hunting for fur."),
    1028: ("Did you know? A village near %s can supply you.", "Offers information about a village near the substituted location where supplies can be obtained."),
    1029: ("Have you heard? There's a village near %s where you can get supplies.", "Informal seafaring voice shares news of a supply village near the substituted location."),
    1030: ("They say an unfamiliar fleet is anchored at %s.", "Hearsay about an unfamiliar fleet anchored at the substituted location."),
    1031: ("An unknown fleet is bound for %s.", "Reports an unidentified fleet traveling toward the substituted location."),
    1032: ("Some strange fleet is headed to %s.", "Rough voice reports an unidentified fleet going toward the substituted location."),
    1033: ("An unknown fleet is anchored at %s.", "Reports an unidentified fleet anchored at the substituted location."),
}


def main():
    clean = NdsImage.open('work/clean.nds')
    entries = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),
                                     clean.read_file('/__arm9__.bin'))
    selected = [e for e in entries if e.block == 12]
    text = {i: value for i, value in LATE_TEXT.items() if entries[i].block == 12}
    text.update(TEXT)
    assert set(text) == {e.message_id for e in selected}
    rows = []
    for e in selected:
        english, meaning = text[e.message_id]
        rows.append({
            'id': f'COMMON_MESSAGE_{e.message_id}', 'message_id': e.message_id,
            'block': e.block, 'record': e.record_index,
            'source_hex': e.text.hex().upper(), 'japanese': e.text.decode('cp932'),
            'previous_japanese': entries[e.message_id - 1].text.decode('cp932'),
            'next_japanese': entries[e.message_id + 1].text.decode('cp932'),
            'english': english.replace('I', 'Ｉ').replace('F', 'Ｆ') + '{PAD}',
            'source_meaning': meaning,
            'speaker': 'Crew member, informant, narrator or tavern hostess',
            'context': (f'Independent native message {e.message_id}, COMMON B12 '
                        f'R{e.record_index}. Entire block freshly reviewed from clean '
                        'Japanese, including every packed neighbor and source argument.'),
            'localization_note': ('Natural English preserves all source facts, feelings, '
                                  'questions and uncertainty. Rumor and bribery orders '
                                  'are distinguished. First place and second affiliation '
                                  'arguments remain in source order; actual broker values '
                                  'still require runtime classification. Tavern dialogue '
                                  'retains younger siblings, parental support, fashion, '
                                  'ancient culture, gifts, fado and supply-village details. '
                                  'No invented kinship, rank, gender or fortune-telling '
                                  'method. I/F use existing safe full-width Latin glyphs. '
                                  'One paragraph; formatting and allocation await review.'),
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False},
        })
    payload = {
        'format': 'dk4-common-entry-manuscript-v1',
        'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
        'encoder': 'dialogue-fixed-v1',
        'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'status': 'draft-awaiting-native-repack-and-formatting-review', 'records': rows,
    }
    Path('translations/common_b12_complete_manuscript_v1.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Complete B12:', len(rows), 'native entries;',
          sum(len(r['english'].removesuffix('{PAD}').encode('cp932')) for r in rows),
          'prose bytes before native prefixes and NULs')


if __name__ == '__main__':
    main()
