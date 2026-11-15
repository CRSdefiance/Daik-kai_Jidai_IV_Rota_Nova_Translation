"""Clean meanings for the pirate confrontation and four town commodity exchanges."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B171_B190_clean_20261102')
MEANINGS = {
    179: [
        'Hodram recognizes the woman.',
        'The woman recognizes him as belonging to FO and says she did not expect to meet him here.',
        'Gerhard demands to know why she keeps following their fleet.',
        'She teasingly calls him an uncouth older man for opening with that question; no uncle relationship is established.',
        'Claims she had hoped they could enjoy a pleasant time together.',
        'Gerhard angrily asks what is wrong with this woman.',
        'She laughs at how stiffly military he is and says he cannot take a joke.',
        'Gerhard suspects that she lay in wait here to assassinate them; this is his accusation, not an established plan.',
        'Hodram remains silent.',
        'Her subordinate boasts that the visitors are only two men while his side has dozens.',
        'Gerhard condemns that as cowardly.',
        'The woman reprimands エンジェル, asking sarcastically when he became so important; exact approved name remains to be bound.',
        'The subordinate falters and tries to explain.',
        'She tells him not to interrupt and orders him back.',
        'He hastily obeys.',
        'She warns the visitors not to misunderstand.',
        'Her pride would not permit her to kill them here.',
        'Hodram dryly asks whether pirates have pride too.',
        'She declares that pirates have their own honor, which another seafarer should understand; she will settle matters at sea.',
        'Hodram accepts the future challenge.',
        'She tells him to prepare for that day using a threatening idiom, then suddenly notices something. Do not render the idiom as literal neck washing.',
        'Hodram asks what caught her attention.',
        'She remarks on his fine sword.',
        'Realizes he is the one who possesses it, laughs, and promises to make it hers someday; the immediate referent is the sword, not an invented romance.',
        'Hodram says he has no idea what she means.',
        'She says he will understand eventually and orders her men to withdraw.',
        'Her crew answers with a collective shout.',
        'Hodram finds her strange but acknowledges her leadership.',
        'Gerhard thinks she could easily command a fleet or two.',
        'Hodram reflects on the idea of a pirate\'s honor.',
    ],
    180: [
        'An imperious woman announces that bananas are the coming fashion.',
        'The man repeats bananas as a question.',
        'She is sure that their flavor will be a hit.',
        'He remains skeptical.',
        'She insists that if she says they will sell, they will.',
        'He accepts this and asks what she wants done.',
        'She orders him to buy as many bananas as possible.',
        'He gives a weary acquiescence.',
        'She repeats that the age of bananas is coming and gives an affected, triumphant laugh.',
        'System forecast: bananas look likely to become fashionable in セビリア; preserve the game\'s commodity and likelihood rather than guaranteeing a boom.',
    ],
    181: [
        'The imperious woman announces that tomatoes are the coming fashion.',
        'The man questions the appeal of such a bright-red food.',
        'She loves that passionate red, which reminds her of a consuming romance in her youth; no spouse or identity for that lover is stated.',
        'He responds with dry, unenthusiastic politeness.',
        'She orders him to start making and selling tomato dishes immediately.',
        'He agrees.',
        'She urges him not to miss the tomato trend.',
        'He again gives a weary acquiescence.',
        'She encourages him to work hard and gives the same affected laugh.',
        'System forecast: tomatoes look likely to become fashionable in ジェノヴァ.',
    ],
    182: [
        'The first woman declares that baking one\'s own bread is best.',
        'The second agrees and says her husband was delighted too. Here the husband relationship is explicit, rather than inferred from a generic speaker label.',
        'The third asks whether homemade bread really tastes that good.',
        'The first insists that it is wonderful and seeks the second\'s agreement.',
        'The second agrees and says even the bakery on the corner cannot compare.',
        'The third decides she may try baking it herself.',
        'The first encourages her.',
        'The second offers to teach her.',
        'The third is delighted by the offer.',
        'The first proposes going to buy the ingredients at once.',
        'The second asks what they need.',
        'The third says wheat first. This ties the baking conversation to the exact wheat trade commodity; do not invent a different flour commodity or preparation process.',
        'System forecast: wheat looks likely to become fashionable in Amsterdam.',
    ],
    183: [
        'One man notices that the other still drinks that old drink.',
        'The other challenges him: what is wrong with that?',
        'The first says nothing is wrong, but wine is the current drink of choice.',
        'The second asks whether wine tastes good.',
        'The first declares it excellent.',
        'The second asks whether it really is that good.',
        'The first says that with wine he feels he needs nothing else.',
        'The second decides to try it and calls to the barkeep for a glass of wine; マスター is an occupational address, not an invented rank.',
        'The barkeep acknowledges the order.',
        'The second gulps down the drink; preserve the comic drinking sound or an equivalent effect.',
        'The first asks his verdict.',
        'The second enthusiastically declares it delicious and orders another glass.',
        'The first asks for one too.',
        'System forecast: wine looks likely to become fashionable in サン＝ジョルジェ; exact approved city spelling remains to be bound.',
    ],
}


if __name__ == '__main__':
    packet_path = ROOT / 'clean_source_packet.json'
    output = ROOT / 'B179_B183_clean_meanings_before_English.json'
    assert not output.exists()
    packet = load(packet_path)
    rows = []
    for group in packet['groups']:
        if group['block'] not in MEANINGS:
            continue
        assert len(group['records']) == len(MEANINGS[group['block']])
        for source, meaning in zip(group['records'], MEANINGS[group['block']], strict=True):
            rows.append(dict(id=source['id'], file_path=source['file_path'], block=source['block'],
                source_reference=source['source_reference'], source_hex=source['source_hex'],
                source_selector=source['source_selector'], source_complete_preamble_hex=source['source_complete_preamble_hex'],
                source_Japanese=source['source_Japanese'], source_meaning=meaning,
                complete_exchange_clean_context_read=True, prior_English_unconsulted=True,
                native_name_terms_preamble_localization_anddisplay_approval_pending=True))
    assert len(rows) == 77
    save(output, dict(source_packet=str(packet_path), source_packet_sha256=sha(packet_path.read_bytes()), records=rows,
        blocks=[179, 180, 181, 182, 183], complete_clean_exchanges=5, source_meanings=77,
        contexts={
            '179': 'A teasing pirate leader rebukes her subordinate, rejects an unfair land attack on principle, promises a sea confrontation and notices Hodram\'s sword. His suspicion and dry respect differ from Gerhard\'s alarm.',
            '180-181': 'The same imperious woman and reluctant man drive two commodity fashions; keep their recurring comic pattern without inventing a marriage or noble title.',
            '182': 'Three women move from praising homemade bread to offering instruction and buying wheat. Preserve the actual activity and the resulting trade-goods forecast.',
            '183': 'A skeptical drinker is won over by wine; use the conversational escalation and drinking beat before the town trend forecast.'},
        additional_context_before_final_localization='Bind the pirate identity/FO/sword and repeated town roles to clean/current native consumers; do not infer the FE woman\'s name from another storyline.',
        no_localized_English_drafts_orprior_English_comparisons=True, no_new_editorial_credit=True,
        producer_sha256=sha(Path(__file__).read_bytes()), new_credit=0))
    print('Saved77 further clean meanings;350 speech meanings andtwo captions saved;83 ordinary meanings remain.')
