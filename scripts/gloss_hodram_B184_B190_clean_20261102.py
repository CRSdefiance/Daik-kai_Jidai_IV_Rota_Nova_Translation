"""Clean meanings for the remaining seven whole town exchanges in this intake."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B171_B190_clean_20261102')
MEANINGS = {
    184: [
        'A politely affected woman asks whether the other noticed how lovely someone smelled.',
        'The other woman agrees that she noticed too.',
        'The first wonders what the fragrance was.',
        'The second does not know, but is sure that scent will become fashionable.',
        'The first decides that they must get it before everyone else.',
        'The second agrees.',
        'The first proposes summoning the courage to ask the wearer the next time they meet.',
        'The second approves and agrees to do so.',
        'The first offers a genteel farewell.',
        'The second returns the farewell.',
        'System forecast: 香料 look likely to become fashionable in Lisbon. The exchange concerns a worn fragrance; bind the exact registered goods/category terminology before final wording.',
    ],
    185: [
        'One woman asks whether another saw the bright-red ruby.',
        'The second says it was magnificent.',
        'A third woman asks what they are discussing.',
        'The first identifies the necklace worn by the lady they all know of; no name or noble rank is stated.',
        'The third recalls its large, beautiful stone.',
        'The second wishes that, just once in her life, a man would give her such a gift; no husband is specified.',
        'The first agrees and sighs.',
        'The second sighs too.',
        'The third sighs as well; preserve the three-person comic beat.',
        'System forecast: rubies look likely to become fashionable in Athens.',
    ],
    186: [
        'One woman asks whether the other has heard that the princess is to become engaged; this rank is explicitly supported.',
        'The second has heard and asks whether the fiancé is a duke\'s son; both the title and family relationship are source facts.',
        'The first reports that the engagement ring supposedly costs enough to buy a mountain; preserve the extravagant comparison as gossip.',
        'The second thinks that is fitting for a duke and wonders when they can see the princess wearing the jewel.',
        'The first thinks it will be soon and predicts that more women will want that gemstone after seeing it.',
        'The second says waiting until it is fashionable will be too late and asks which gemstone it is.',
        'The first does not know and wants to find out at once.',
        'System forecast: gemstones look likely to become fashionable in London. Do not invent a particular gem or name the royal couple.',
    ],
    187: [
        'A listener notices the commotion.',
        'The first art enthusiast declares something wonderful.',
        'The second questions that judgment.',
        'The first predicts that the artist will be remembered by posterity.',
        'The second responds unenthusiastically.',
        'The first recommends buying the artist\'s work now.',
        'The second prefers a different painting.',
        'The first says it is not bad but cannot match his preferred artist.',
        'A third enthusiast contradicts both of them and praises another work.',
        'The first insists on buying his favored artist\'s painting regardless.',
        'The second will take a work by the painter of his own preferred picture.',
        'The third chooses his preferred work.',
        'The shopkeeper thanks them for their business.',
        'A slamming sound marks their departure; source onomatopoeia バタンッ.',
        'The shopkeeper is relieved that they finally left and wishes they would stop arguing in his shop every time.',
        'The listener asks the shopkeeper what all the commotion was about.',
        'The shopkeeper calls it a rich person\'s pastime.',
        'The listener repeats that as a question.',
        'The shopkeeper explains that collecting paintings is fashionable lately.',
        'The listener remarks that it is a cultured hobby.',
        'The shopkeeper privately adds that few of the collectors actually have a discerning eye.',
        'The listener laughs at the shopkeeper\'s bluntness.',
        'The shopkeeper quickly asks him to keep that comment secret.',
        'The listener assures him he understands.',
        'System forecast: paintings look likely to become fashionable in Basra.',
    ],
    188: [
        'The woman enjoys her tea and calls it wonderful.',
        'The man agrees that tea is excellent.',
        'She wonders why something so delicious had not become fashionable before now.',
        'He agrees and says other people must lack good taste.',
        'She remembers that their household is running low on tea and asks him to buy more tomorrow. Shared household wording supports closeness but does not explicitly establish marriage.',
        'He readily agrees to buy it.',
        'She says tea is delicious and soothing.',
        'He says they cannot live without tea; affectionate hyperbole, not a medical claim.',
        'System forecast: tea looks likely to become fashionable in Sofala.',
    ],
    189: [
        'The woman complains of the bitter cold.',
        'The man says it has not been this cold for a long time.',
        'She wants a fur coat and feels she will freeze in this weather.',
        'He has heard that the cold is boosting fur sales and prices.',
        'She has heard that too and again complains of the cold.',
        'He hopes it warms up soon.',
        'She agrees but still wants fur while it remains cold.',
        'System forecast: furs look likely to become fashionable in Stockholm.',
    ],
    190: [
        'The imperious woman decides that the food lacks sweetness.',
        'The man repeats sweetness as a question.',
        'She insists that such a light/plain flavor will not satisfy customers and extravagantly emphasizes the borrowed word sweet.',
        'He gives an unconvinced response.',
        'She insists she must be right because she says so.',
        'He asks how he should make it sweeter.',
        'She tells him that figuring it out is his job; do not invent a recipe or ingredient.',
        'He gives a weary acquiescence.',
        'She insists that sweet things are certain to become fashionable; this is her confident claim.',
        'He again acquiesces wearily.',
        'She repeats her emphasis on sweetness, tells him to work hard and gives her recurring affected laugh.',
        'System forecast: sweet things look likely to become fashionable in Alexandria. Bind the exact goods/category terminology; no sugar ingredient is named in the dialogue.',
    ],
}


if __name__ == '__main__':
    packet_path = ROOT / 'clean_source_packet.json'
    output = ROOT / 'B184_B190_clean_meanings_before_English.json'
    assert not output.exists()
    packet = load(packet_path)
    rows = []
    for group in packet['groups']:
        if group['block'] not in MEANINGS:
            continue
        assert len(group['records']) == len(MEANINGS[group['block']])
        for source, meaning in zip(group['records'], MEANINGS[group['block']], strict=True):
            incidental = source['id'] == 'DK4_MES_B188_R0022'
            rows.append(dict(id=source['id'], file_path=source['file_path'], block=source['block'],
                source_reference=source['source_reference'], source_hex=source['source_hex'],
                source_selector=source['source_selector'], source_complete_preamble_hex=source['source_complete_preamble_hex'],
                source_Japanese=source['source_Japanese'], source_meaning=meaning,
                complete_exchange_clean_context_read=True, current_ROM_English_unconsulted=True,
                earlier_user_English_screenshot_incidental_exposure=incidental,
                clean_meaning_before_any_English_exposure_claimed=not incidental,
                native_name_terms_preamble_localization_anddisplay_approval_pending=True))
    assert len(rows) == 83
    save(output, dict(source_packet=str(packet_path), source_packet_sha256=sha(packet_path.read_bytes()), records=rows,
        blocks=[184, 185, 186, 187, 188, 189, 190], complete_clean_exchanges=7, source_meanings=83,
        context='Town fashions arise through genteel gossip, competitive art collecting, a close pair\'s tea/cold-weather talk and the recurring imperious woman\'s demands. Preserve each small comic progression and distinguish characters\' certainty from the system\'s tentative forecasts.',
        incidental_exposure=dict(id='DK4_MES_B188_R0022', source='Earlier user screenshot of Woman in a Couple and the tea-shopping line in this conversation.',
            no_current_ROM_English_extraction=True, exact_source_meaning_reread=True,
            no_blanket_draft_before_all_prior_English_exposure_claim=True),
        no_localized_English_drafts_orcurrent_ROM_English_comparisons=True, no_new_editorial_credit=True,
        producer_sha256=sha(Path(__file__).read_bytes()), new_credit=0))
    print('All433 clean speech meanings andtwo caption meanings saved;one earlier user screenshot exposure disclosed;no current-ROM English orcredit.')
