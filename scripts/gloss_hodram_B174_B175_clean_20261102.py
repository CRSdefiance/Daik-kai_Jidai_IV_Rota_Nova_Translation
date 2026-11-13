"""Clean-source meanings for Yifa and her senior fellow student's complete scenes."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B171_B190_clean_20261102')
MEANINGS = {
    174: [
        'The woman calls flirtatiously to the handsome man nearby. お兄さん is a familiar address, not evidence of a brother.',
        'Hodram does not respond.',
        'She insistently calls to him again.',
        'Hodram realizes she means him.',
        'Gerhard asks what the young woman is doing there.',
        'She hushes them and says she has a certain predicament.',
        'Assuming they are sailors, asks whether they will let her aboard their ship.',
        'Gerhard finds the request abrupt and wonders what to make of her.',
        'Hodram asks what the predicament is and why she wants to board the ship.',
        'She slipped away from her teacher; if found, she will be taken back.',
        'Hodram thinks running away sounds serious and asks what she studies.',
        'She cheerfully identifies her subject as 道術, Taoist arts; preserve this cultural/martial context rather than substituting an invented religion.',
        'Says she does not dislike studying those arts, but sometimes finds it a drag.',
        'She was caught skipping practice and severely scolded; complains that her teacher is inflexible.',
        'Decided to travel the world while training so she can prove her teacher wrong; asks whether that is admirable.',
        'Gerhard grumbles about young women these days.',
        'Hodram admires her determination to prove herself, but asks how proficient she actually is in these arts.',
        'Offers a small demonstration and asks Gerhard to ready his sword, addressing him as おじさん; this does not establish an uncle relationship.',
        'Gerhard is startled by that address and checks that she means him.',
        'She confirms and warns him to prepare himself.',
        'Gerhard braces himself.',
        'She gives a prolonged martial cry.',
        'Hodram is puzzled.',
        'Gerhard is puzzled too, thinking that nothing has happened.',
        'She suddenly cries that he has left himself open.',
        'Gerhard reacts to the sudden attack.',
        'She compliments his dodge and identifies her technique as an immobilizing/binding art.',
        'Gerhard repeats that claim skeptically; he does not really understand what she means.',
        'She laughs and presents the exchange as evidence that her arts are mysterious.',
        'Gerhard explains that this was not what he meant.',
        'Hodram notes that closing on Gerhard so quickly is no easy feat; she seems skilled at judging fighting distance.',
        'Gerhard agrees that she evidently has received some kind of training.',
        'Hodram once had a teacher who told him to go to sea; that advice made him the man he is now.',
        'Disapproves of her leaving without telling her teacher but assumes she has some resolve; asks her name.',
        'She gives her name as イファ; final native approved English spelling remains to be bound.',
        'Hodram explains that his ship belongs to the navy and asks whether she still wants aboard.',
        'She understands that he means his ship is strict too; she enthusiastically accepts the challenge.',
    ],
    175: [
        'A voice begins a respectful address, only its ending audible.',
        'Hodram remains silent.',
        'The voice respectfully calls to FI.',
        'Hodram stirs and responds questioningly.',
        'The visitor apologizes for appearing suddenly and says he is not suspicious.',
        'Introduces himself as サンヒョン, Yifa\'s senior fellow student. 兄弟子 is an apprenticeship relationship, not a biological brother.',
        'Having learned that Hodram will take Yifa into his care, came to offer a brief greeting.',
        'Hodram starts to repeat the connection to Yifa.',
        'The visitor takes responsibility for insufficient guidance, saying that is why Yifa grew up so unrestrained.',
        'Says it is unacceptable that she left the mountain without the teacher\'s permission to escape training, and even went abroad.',
        'Yifa apparently does not know that people of their country are forbidden to travel abroad.',
        'Hodram asks whether the visitor intends to take her back.',
        'He cannot: her violation of the national prohibition is serious, and their school has expelled her.',
        'Formally says he no longer has any connection with her.',
        'Nevertheless, they grew up together from childhood like a real brother and sister. The explicit simile reinforces that they are not stated to be biological siblings.',
        'Worries constantly that someone so immature will misbehave in front of others.',
        'Acknowledges that it is a selfish request but asks Hodram to guide Yifa so she does not stray from the right path.',
        'Also asks, if possible, that she continue training after leaving the mountain and heed their teacher\'s instructions.',
        'Earnestly entrusts Yifa to Hodram\'s care.',
        'Hodram wonders whether what just happened was a dream.',
        'It was a strangely vivid dream.',
        'Yifa bursts in with an exuberant good morning and begins urging them to depart.',
        'She abruptly reacts in shock.',
        'Hodram asks what is wrong.',
        'She senses the presence of her senior fellow student.',
        'Hodram reacts and asks whether, unlikely as it seems, his name is サンヒョン.',
        'She is startled that Hodram knows the name.',
        'Hodram realizes the man really is her senior fellow student; explains that he gave that name in a dream and asked him to look after her.',
        'She softly addresses the senior student by name with a brotherlike familiar form; preserve warmth without inventing literal kinship.',
        'She believes he used their arts to come and see them.',
        'Hodram questions the mention of those arts and inwardly thinks: this again.',
        'Passes on the message that she should follow their teacher\'s instructions even after leaving the mountain.',
        'She fondly laughs at how he never stops worrying about her.',
        'Hodram pauses and asks what is the matter.',
        'She resolves to train hard because she does not want to disappoint him.',
        'Hodram chuckles but warns her not to neglect shipboard duties for training; he will not go easy on her because she is a woman.',
        'She emphatically says she knows.',
    ],
}


if __name__ == '__main__':
    packet_path = ROOT / 'clean_source_packet.json'
    output = ROOT / 'B174_B175_clean_meanings_before_English.json'
    assert not output.exists()
    packet = load(packet_path)
    rows = []
    for group in packet['groups']:
        if group['block'] not in MEANINGS:
            continue
        assert len(group['records']) == len(MEANINGS[group['block']]) == 37
        for source, meaning in zip(group['records'], MEANINGS[group['block']], strict=True):
            rows.append(dict(id=source['id'], file_path=source['file_path'], block=source['block'],
                source_reference=source['source_reference'], source_hex=source['source_hex'],
                source_selector=source['source_selector'], source_complete_preamble_hex=source['source_complete_preamble_hex'],
                source_Japanese=source['source_Japanese'], source_meaning=meaning,
                complete_exchange_clean_context_read=True, prior_English_unconsulted=True,
                native_name_terms_preamble_localization_anddisplay_approval_pending=True))
    assert len(rows) == 74
    save(output, dict(source_packet=str(packet_path), source_packet_sha256=sha(packet_path.read_bytes()), records=rows,
        blocks=[174, 175], complete_clean_exchanges=2, source_meanings=74,
        contexts={
            '174': 'A lively runaway Taoist-arts student seeks passage. Her distraction-and-rush demonstration shows martial training without resolving Hodram/Gerhard\'s skepticism about supernatural claims. Hodram remembers his own mentor and offers strict naval service.',
            '175': 'Her restrained senior fellow student visits in an apparent dream. Their school expelled her for leaving the country; his formal severance conflicts with his affectionate concern. They grew up like siblings, not stated blood relatives. Her bravado softens into resolve, and Hodram maintains shipboard discipline.'},
        no_localized_English_drafts_orprior_English_comparisons=True, no_new_editorial_credit=True,
        producer_sha256=sha(Path(__file__).read_bytes()), new_credit=0))
    print('Saved74 further clean meanings;205 speech meanings andtwo menu meanings now saved;228 ordinary meanings remain.')
