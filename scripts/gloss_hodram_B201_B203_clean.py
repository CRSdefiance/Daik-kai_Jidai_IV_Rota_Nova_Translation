"""Preserve the celestial-maiden ambiguity, named Namahage and portrait discovery."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B191_B210_clean_20261104')


if __name__ == '__main__':
    output = ROOT / 'B201_B203_clean_meaning_decisions_v1.json'
    captions = ROOT / 'B201_three_clean_caption_meanings_v1.json'
    assert not captions.exists()
    decisions = dict(blocks={
        '201': dict(context='A flirtatious woman offers Ian an Indian classic about a celestial maiden and a sage for 8500 gold. Ian consults the admiral. Conditional purchase, refusal and delegated-decision branches follow; in the moneyless branch she gives him the book, voices a romantic wish and vanishes. Ian wonders about a celestial maiden, then dismisses the thought. A notice reports his 魅力 increasing by one.',
            notes=['天女 and 仙人 keep their Asian/Indian cultural referents: a celestial maiden and a sage, without inventing angels, wizards, a specific religion or a book title.', '今度は says next time, not explicitly a next life. Do not invent reincarnation, a former lover, marriage or a prior relationship with Ian.', 'Ian\'s lack of romantic interest does not establish a sexual orientation or a different gender identity. The woman\'s supernatural identity remains his speculation.', 'The three menu choices buy, decline and leave the decision to Ian; the last does not explicitly command payment from personal funds.'], meanings=[
                'The woman calls out to the handsome man over there.',
                'Ian asks whether she means him.',
                'She asks him to buy this book for 8500 gold.',
                'Ian asks what sort of book it is.',
                'She describes an Indian classic telling the love story of a celestial maiden and a sage, and asks whether he wants it.',
                'Ian asks the admiral what to do.',
                'On the purchase branch, Ian decides to take the book.',
                'The woman hopes he too may be able to love a celestial maiden.',
                'Ian says, regrettably, that he has no interest in that.',
                'The woman calls it a waste, given that he is such a handsome man.',
                'On the refusal branch, Ian politely declines.',
                'The woman is disappointed and says someone else will buy it.',
                'In the delegated-decision branch, Ian would like to buy it from her but says he does not have so much money.',
                'She acknowledges his explanation.',
                'Ian apologizes for not meeting her expectation.',
                'She decides to give it to him instead.',
                'Ian reacts with surprise.',
                'She laughs softly and wishes that next time she could fall in love with a man like him.',
                'Ian stammers in astonishment that she has vanished.',
                'He wonders whether she could have been a celestial maiden, then scoffs at his own foolish thought.',
                'System notice: Ian\'s charm/charisma attribute has increased by one.',
            ]),
        '202': dict(context='An anonymous FE voice repeats a bad-child chant. Yukihisa challenges it, recognizes a Namahage, denies remembering any wrongdoing and later calls the experience a dream. Angelo reacts to something unexplained; Yukihisa calmly decides to pass an unnamed object to the admiral the next morning, leaving Angelo bewildered.',
            notes=['Retain the named なまはげ and the repeated bad-child chant; do not replace the named figure with a generic demon or invent a shrine, religion or ritual date.', 'The source leaves dream/supernatural ambiguity. No dialogue names the object or explains Angelo\'s surprise; do not invent an item, a gift-giver or an actual handover already completed.', 'Tomorrow morning is Yukihisa\'s intended timing, not a narrator report that a day passed.'], meanings=[
                'The anonymous voice calls twice, asking whether there are any bad children around.',
                'The same twice-repeated bad-child call continues.',
                'The voice asks whether the addressed person is a bad child.',
                'Yukihisa demands to know who or what the speaker is.',
                'The voice repeats the question about being a bad child.',
                'Yukihisa recognizes the addressed being as a Namahage.',
                'The voice asks the same bad-child question again.',
                'Yukihisa says there is no recollection of having done anything wrong.',
                'The voice slowly acknowledges that answer.',
                'Yukihisa pauses silently.',
                'Yukihisa considers whether it was a dream.',
                'Angelo cries out in shock, asking what this is.',
                'Yukihisa reacts with a questioning sound.',
                'Yukihisa pauses again.',
                'Yukihisa reflects that strange things do happen.',
                'Yukihisa decides to give this unnamed thing to the admiral tomorrow morning.',
                'Angelo emphatically continues asking what it is.',
            ]),
        '203': dict(context='Hodram and Gerhard respectfully discuss a portrait of ロッコ・アレムケル, a navigator who supported Portugal when it was strong in the past. Afterward Charles dismisses it as an ordinary portrait, hears a clunk, discovers a book behind it, hopes for science and is disappointed that it concerns navigation. He plans to give it to the admiral later.',
            notes=['Bind the exact established English spelling of ロッコ・アレムケル before localized approval. 殿 conveys Gerhard\'s respect without independently granting knighthood or a royal title.', 'The source does not establish the navigator\'s death, formal office, nationality, a specific campaign, or a named navy.', 'Do not name the book, invent who hid it, claim that Charles caused the noise, or change navigation into science. The disappointment is part of his characterization.'], meanings=[
                'Gerhard asks what is the matter with the admiral.',
                'Hodram says it concerns this portrait.',
                'Gerhard respectfully identifies the depicted person as ロッコ・アレムケル.',
                'Hodram confirms and calls him a navigator who supported the powerful Portugal of long ago.',
                'Gerhard agrees that the man merits respect despite being from another country.',
                'Hodram gives a brief assent.',
                'Charles wonders what the two men were looking at.',
                'Charles dismisses it as merely a portrait.',
                'A clunk/rattle sound is heard.',
                'Charles reacts in surprise and asks what that was.',
                'He realizes that something is behind the picture.',
                'He discovers a book and excitedly wonders whether it is about science.',
                'Pages are flipped/rustled.',
                'Charles is disappointed that it is a navigation book and decides to give it to the admiral later.',
            ]),
    }, clean_meanings_not_localized_dialogue_drafts=True, current_ROM_English_unconsulted_in_this_intake=True, new_credit=0)
    if output.exists():
        assert load(output) == decisions
    else:
        save(output, decisions)
    source_path = ROOT / 'clean_choice_objects.json'
    source = load(source_path)
    meanings = ['Choose to buy the offered book.', 'Decline to buy the offered book.', 'Leave the decision to Ian.']
    rows = []
    for original in source['records']:
        if original['block'] != 201:
            continue
        index = original['source_index']
        assert original['source_Japanese'] == ['買おう', '買わない', '任せる'][index]
        row = dict(original)
        row.update(source_meaning=meanings[index],
            exchange_context='Complete B201 Indian-classic offer, Ian\'s consultation, purchase/refusal/delegated branches and unexplained disappearance.',
            clean_meaning_not_localized_caption=True, current_ROM_English_unconsulted_in_this_intake=True, new_credit=0)
        rows.append(row)
    assert len(rows) == 3
    save(captions, dict(records=rows, complete_source_menus=1, source_meanings=3,
        source_object_packet=str(source_path), source_object_packet_sha256=sha(source_path.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()), new_credit=0))
