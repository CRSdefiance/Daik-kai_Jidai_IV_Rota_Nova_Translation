"""Save the complete clean crown-hint and recruitment exchanges before old English."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B171_B190_clean_20261102')
MEANINGS = {
    176: [
        'Julian tells 美華 that he lives for her radiant smile; final approved native names remain to be bound.',
        'She responds familiarly to his flattery.',
        'Hodram inwardly finds the flattery painfully sugary.',
        'Julian notices that she usually smiles at this point and asks whether she has stopped liking him.',
        'She denies that; his words normally cheer her up, but something is bothering her now.',
        'There is an object she wants so much that lately she cannot stop thinking about it, asleep or awake.',
        'Julian says that expression does not suit her and asks what she wants so badly.',
        'She names 新羅の金冠, calls its name mysterious, and says she has heard it is very precious. Preserve the specific cultural item identity.',
        'Julian thinks it sounds expensive, wonders whether he can afford it, and asks where it is sold.',
        'Apparently it is not sold in shops; she has heard it is somewhere in 京城. Exact approved city/item spelling remains to be bound.',
        'On hearing it is not sold in shops, Julian suddenly thinks he knows the place.',
        'She asks whether he has an idea where to look.',
        'He asks her to leave it to him; will obtain the crown as soon as possible and restore her smile.',
        'Her smile gives him strength; he asks whether she will go on a date with him once he gets the crown.',
        'She says he is getting ahead of himself when he has not even found it; agrees only to think about the date.',
        'He celebrates as though it were a promise, asks her not to forget it, and immediately sets off for 京城.',
        'She starts to say she is counting on him, then realizes he has already left.',
        'Hodram pauses silently.',
        'She apologizes for not noticing Hodram and welcomes him.',
        'Hodram asks about the conversation he just overheard.',
        'She realizes he was listening.',
        'He asks what the crown is.',
        'She apologizes that she does not know much about it, but has heard it is very beautiful.',
        'He acknowledges that.',
        'She is surprised that someone dressed like a military man is interested in such an object; this is her observation, not a new rank.',
        'He confirms that she said it was in 京城.',
        'She confirms but has no further information.',
        'He says that is enough; he will obtain the rest of the information locally.',
        'She asks him to give it to her if he obtains it.',
        'He says only that he will consider it, not that he promises.',
    ],
    177: [
        'Hodram thinks someone here should know about the crown.',
        'The tavern woman welcomes him and offers him a drink.',
        'He accepts a drink and asks about the crown.',
        'She asks what he wants to know.',
        'He is searching for it and asks where it can be found.',
        'She thinks it is in the ruins called 武寧王陵, but does not know how to obtain it. Exact approved ruin name remains to be bound.',
        'He takes note of the named tomb.',
        'She finds the coincidence unusual: someone else asked the same question just now.',
        'Hodram wonders whether that man was called Julian.',
        'She does not remember his name, but he entered comparing her lips to rose petals; she judges him to be practiced at flirting.',
        'Hodram pauses at that recognizable description.',
        'He concludes by asking whether the man has already gone to the tomb.',
        'She thinks so; it is not eyewitness confirmation of arrival at the ruins.',
        'He says he understands and will go there himself.',
    ],
    178: [
        'Julian recognizes Hodram and thanks him for his earlier help; the actual crown-discovery event is not shown in this block.',
        'The tavern woman is surprised that they already know each other.',
        'Julian turns back to her and presents the crown as he promised.',
        'She admires its beauty, thanks him, and says she will treasure it for the rest of her life.',
        'Hodram observes that things seem to have worked out.',
        'Gerhard agrees.',
        'Hodram suggests that they leave.',
        'Julian calls for them to wait.',
        'Hodram responds questioningly.',
        'Julian tells 美華 that FI was actually the one who found the crown.',
        'She is surprised to learn that.',
        'Julian says he asked FI to let him have it.',
        'Hodram says he had told Julian that there was no need to mention this.',
        'Julian insists he cannot leave it unacknowledged and will repay him properly later.',
        'The woman softly addresses Julian, touched by his conduct.',
        'Hodram says repayment is unnecessary but is interested in Julian\'s adventurous spirit and strong sense of obligation.',
        'Julian asks to join FI\'s ship, promising to work hard.',
        'Gerhard finds the offer interesting.',
        'Julian\'s grandfather sailed all over the world; hearing those stories increasingly interested him in sailing.',
        'He wants to become an adventurer like his grandfather. This grandfather relationship is explicit.',
        'Hodram reflects on his wish to follow his grandfather\'s example.',
        'Hodram says his ship does not exist for adventure, though it does sail around the world.',
        'He will allow Julian aboard if he can work as expected.',
        'Julian celebrates and declares the arrangement settled.',
    ],
}


if __name__ == '__main__':
    packet_path = ROOT / 'clean_source_packet.json'
    output = ROOT / 'B176_B178_clean_meanings_before_English.json'
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
    assert len(rows) == 68
    save(output, dict(source_packet=str(packet_path), source_packet_sha256=sha(packet_path.read_bytes()), records=rows,
        blocks=[176, 177, 178], complete_clean_exchanges=3, source_meanings=68,
        context='Julian\'s extravagant flirting gives way to a crown search,then gratitude andhonest acknowledgment ofHodram\'s help. The woman onlyagrees toconsider a date. Hodram stays dry andpractical,valuing adventurousness andhonor whileinsisting onshipboard work.',
        additional_clean_context_needed_before_localized_approval='Find the shared ruin/crown-discovery encounter that precedes B178;these three blocks do not show how the assistance itself happened. Bind city,tomb,item andnative proper names without inventing details.',
        no_localized_English_drafts_orprior_English_comparisons=True, no_new_editorial_credit=True,
        producer_sha256=sha(Path(__file__).read_bytes()), new_credit=0))
    print('Saved68 further clean meanings;273 speech meanings andtwo captions saved;160 ordinary meanings remain.')
