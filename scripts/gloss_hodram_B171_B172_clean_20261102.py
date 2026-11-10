"""Faithful clean-source meanings for two complete exchanges; no old English consulted."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B171_B190_clean_20261102')
MEANINGS = {
    171: [
        'Calls to the admiral and asks whether he wants to hear the speaker\'s sailing-ship lecture.',
        'Asks in surprise: a lecture?',
        'Says he has been unbearably bored lately; asks them to think of listening as helping someone out.',
        'Objects that the lecturer should realize whom he is trying to lecture; the admiral is already knowledgeable.',
        'Tentatively agrees with that objection.',
        'Formally says there is no need for them to hear about ships at this stage.',
        'Accepts the refusal: they look knowledgeable about ships; he will wait for a more obviously inexperienced customer.',
        'Approves their willingness to listen and says the admiral will go far.',
        'Begins by saying sails are the lifeblood of a sailing ship.',
        'Will first explain the difference between square and triangular sails.',
        'Explains that the square sail is a transverse sail, stretched across the direction in which the ship points.',
        'Explains the game\'s square-sail constraint: it cannot be turned lengthwise; it excels with a favorable wind but cannot take the best angle into a headwind.',
        'Calls the triangular sail ラテンセイル, a term used by people in the know; unlike a square sail, it is set lengthwise and cannot be turned across the ship.',
        'That is why triangular sails can take a good angle into a headwind but provide less speed with a favorable wind; checks whether the listeners follow.',
        'Moves on to sails that can be added to the ship.',
        'Identifies the upper sail as a topsail: a small transverse sail mounted high on each mast.',
        'Identifies the diagonal sail as a staysail: a small fore-and-aft sail ahead of each mast; cannot mount it ahead of a triangular sail because the two would overlap.',
        'Uses the source term スプリットセイル for the bow sail: a transverse sail on the ship\'s bow that cannot be fitted to small ships. Final English nautical term needs the established glossary.',
        'Calls the stern sail ジガースパンカー; it is fore-and-aft but effectively requires another small mast, so it fits only large ships.',
        'Asks whether they knew that a ship with two or more masts travels faster with the wind coming somewhat diagonally than directly astern.',
        'Asks one listener why that is.',
        'Answers that the masts are arranged one behind another.',
        'Agrees: with the wind directly astern, only the rear mast gets the wind and the masts forward of it are ineffective.',
        'Concludes that wind from diagonally astern gives the greatest speed, provided the sails are adjusted to match.',
        'Responds with understanding.',
        'Enthusiastically admits not having paid much attention to this before; now understands the reason.',
        'Thanks them for keeping him company and says he will get back to work.',
    ],
    172: [
        'Asks whether they too have come to see the old man Mikhail.',
        'Repeats the name Mikhail as a question.',
        'Recognizes Mikhail\'s name with alarm, tells FI not to meet him, and urgently tries to stop the visit.',
        'Had assumed that was why they came; says Mikhail is famous locally as a very knowledgeable old man.',
        'Interested, decides to meet him.',
        'Warns that they might be better off staying away if they have a woman with them.',
        'Strongly agrees that they should stay away.',
        'Is puzzled.',
        'Identifies the man they can see as Mikhail.',
        'A woman exclaims that the older man is amazing. Her familiar おじいちゃん does not establish kinship.',
        'Mikhail agrees with her admiration and gives his distinctive old-man laugh.',
        'Another woman asks him to identify another object.',
        'Identifies it as pepper fruit from a tropical tree, which becomes a spice when ground.',
        'Says it should grow well if taken to somewhere around Brunei and become a valuable trade good.',
        'Then corrects himself: it is actually rabbit droppings, and dirty. The preceding confident misidentification is the joke.',
        'The woman reacts with disgust and tells him to throw it away.',
        'Agrees and tosses it away.',
        'The first woman says he seems to know everything and asks why he is so knowledgeable.',
        'Boasts that he is a genius and few know more than he does; adds that he can even guess the woman\'s bust size.',
        'The woman squeals and calls him lecherous. She has not been identified as his granddaughter.',
        'Mikhail laughs again.',
        'Hodram thinks Mikhail seems very knowledgeable, but finds his behavior somewhat problematic.',
        'Gerhard thinks that knowledge will certainly be useful later and sees no harm in recruiting him.',
        'Hodram agrees.',
        'Mikhail asks who these men are.',
        'Hodram compliments his knowledge and introduces himself as FI FA, admiral of a fleet.',
        'Asks Mikhail to put that knowledge to work for them.',
        'Mikhail refuses: he no longer intends to leave this city and does not accept invitations from men.',
        'Gerhard respectfully presses the older man to reconsider.',
        'Mikhail is still reluctant, then suddenly notices something.',
        'Asks the name of the young woman accompanying them.',
        'Sera remains silent in her branch.',
        'Hodram explains that she cannot understand their language and that her name is Sera.',
        'In the alternate branch, Cristina/Christina hesitantly gives her name; exact approved native spelling remains to be bound.',
        'Mikhail repeats Sera\'s name familiarly in her branch.',
        'Mikhail repeats Cristina/Christina\'s name familiarly in the alternate branch.',
        'Very pleased with what he sees.',
        'Hodram is puzzled.',
        'Mikhail abruptly decides that he is coming with them.',
        'Calls drawn-out and affectionately to Sera in her branch.',
        'Calls drawn-out and affectionately to Cristina/Christina in her branch.',
        'Declares he will follow her anywhere.',
        'Sera reacts with silent alarm.',
        'Gerhard urgently asks FI to abandon the recruitment, fearing for Sera\'s safety.',
        'Cristina/Christina asks what is wrong with this old man and tells him to stay away.',
        'Julio recognizes Mikhail, calls him a lecherous old man, and explicitly tells him to keep away from Julio\'s granddaughter. This kinship is supported here.',
        'Mikhail recognizes Julio after a long absence; says Julio is also hard to kill and objects to another old man calling him old.',
        'Gerhard again urges FI not to recruit him.',
        'Mikhail refuses to give up: he has decided to go and will make his knowledge useful, so they need not worry.',
        'Hodram gives permission but starts to impose a condition.',
        'Gerhard threatens to cut Mikhail down if he touches Sera, despite Mikhail\'s age.',
        'Mikhail ignores the warning and calls to Sera again.',
        'Gerhard tries to make him listen.',
        'Hodram falls silent.',
        'Cristina/Christina threatens to run him through with her sword if he touches her.',
        'Mikhail ignores her warning and calls to her again.',
        'She exclaims that she has had enough.',
        'Julio angrily calls Mikhail a dirty old man and repeats the order to stay away from his granddaughter.',
        'Mikhail says love is free and remarks that it is fortunate Cristina/Christina does not resemble Julio.',
        'Julio tells him to shut up.',
        'System instruction: Mikhail is a learned scholar rather than a navigator, so he cannot be assigned to the deck.',
        'System instruction: with Mikhail aboard, detailed information about items is now available.',
        'System instruction: try pressing the X Button while item information is displayed.',
        'Mikhail says he cannot do shipboard work but asks them to look after him; they should call on him when they want to know about items.',
    ],
}


if __name__ == '__main__':
    packet_path = ROOT / 'clean_source_packet.json'
    target = ROOT / 'B171_B172_clean_meanings_before_English.json'
    assert not target.exists()
    packet = load(packet_path)
    rows = []
    for group in packet['groups']:
        if group['block'] not in MEANINGS:
            continue
        meanings = MEANINGS[group['block']]
        assert len(meanings) == len(group['records']), (group['block'], len(meanings), len(group['records']))
        for source, meaning in zip(group['records'], meanings, strict=True):
            assert source['source_decode_error'] is None
            rows.append(dict(id=source['id'], file_path=source['file_path'], block=source['block'],
                source_reference=source['source_reference'], source_hex=source['source_hex'],
                source_selector=source['source_selector'], source_complete_preamble_hex=source['source_complete_preamble_hex'],
                source_Japanese=source['source_Japanese'], source_meaning=meaning,
                complete_exchange_clean_context_read=True, prior_English_unconsulted=True,
                native_name_terms_preamble_localization_anddisplay_approval_pending=True))
    assert len(rows) == 91
    save(target, dict(source_packet=str(packet_path), source_packet_sha256=sha(packet_path.read_bytes()), records=rows,
        blocks=[171, 172], complete_clean_exchanges=2, source_meanings=91,
        contexts={
            '171': 'Bored sailing lecturer offers a tutorial; experienced-listener refusal and willing-listener teaching branches. Preserve practical game rules and the lecturer\'s easygoing voice.',
            '172': 'Knowledgeable but lecherous Mikhail recruitment with Sera and Cristina/Christina branches; each woman\'s reaction and companions\' objections matter. Julio\'s explicitly stated granddaughter relationship applies only to the latter branch, not the two admiring women. Preserve the pepper/droppings misidentification, discomfort, threats and item-information tutorial.'},
        remaining_ordinary_meanings=342, typed_B171_menu_meanings_pending=True,
        no_localized_English_drafts_orprior_English_comparisons=True, no_new_editorial_credit=True,
        producer_sha256=sha(Path(__file__).read_bytes()), new_credit=0))
    print('Saved91 clean meanings across two complete exchanges;342 ordinary meanings andthe B171 menu remain;no English exposure orcredit.')
