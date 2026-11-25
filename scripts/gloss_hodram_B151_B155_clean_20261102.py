"""Save faithful complete-exchange meanings before consulting prior English."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B151_B170_clean_20261102')
MEANINGS = {
    151: [
        "The ceremonial knife and sun-patterned sheath have uncannily matching dimensions, as though they form one set.",
        "Agrees, tentatively suggesting that they may originally have belonged together.",
        "Decides to try putting the knife into this sheath, then reacts in surprise.",
        "Cries out and asks what is happening.",
        "Light is coming from the sheath; it is so dazzling that he cannot keep his eyes open.",
        "Asks what on earth just happened.",
        "Calls attention to the blade: a pattern has suddenly appeared on it.",
        "Astonished; supposes this is the map for the New World's 覇者の証, while still finding the phenomenon hard to comprehend.",
    ],
    152: [
        "Reports that someone in Alexandria said they were waiting for the addressee.",
        "Echoes Alexandria with surprise or questioning interest.",
    ],
    153: [
        "Checks that the addressee belongs to {MACRO:FO}, then grants entry.",
        "Addresses the person who rules the Mediterranean and bestows this object on them.",
        "Asks who this speaker is.",
        "Identifies himself only as someone who has long resisted Ottoman rule.",
        "Asks whether this means that this person helped Sera and the others.",
        "Declines to discuss details; urges the addressee to solve it and quickly find the Proof.",
        "Says others have also escaped Ottoman rule, as his group has; tells the addressee to search the ruins in Turkey.",
    ],
    154: [
        "Is certain that the patterned cloth is the map for the Mediterranean's 覇者の証, but cannot yet make sense of it.",
        "Observes that it does not look like a map in its present state.",
        "Suggests using the previously mentioned brass lamp, perhaps to reveal hidden writing by heating it.",
        "In the parallel suggestion, proposes heating the cloth with the brass lamp.",
        "Agrees to try; describes heating the cloth with the lamp.",
        "Exclaims at the result.",
        "Celebrates success.",
        "Praises Charles; says they now have the map for the Mediterranean's 覇者の証.",
        "Cheerfully celebrates having guessed correctly.",
        "Praises イファ; says they now have the map for the Mediterranean's 覇者の証.",
    ],
    155: [
        "Casually addresses {MACRO:FA} and asks whether he has heard the news.",
        "Reports hearsay that a new town has recently been established here on the Black Sea.",
        "Asks the town's name.",
        "Recalls the name uncertainly as Abkhaz.",
        "Repeats Abkhaz; says this is the first he has heard of it.",
        "Sera reacts with sudden recognition or surprise.",
        "Asks what is wrong, addressing Sera.",
        "Haltingly asks {MACRO:FI} to take her to that town.",
        "Agrees without objection and asks whether she knows something about it.",
        "Haltingly says it is her country and that everyone is building it again together.",
        "Surprised, asks whether this could be her homeland.",
        "She nods.",
        "Understands that her companions are building a town in her homeland.",
        "Reasons that it should be nearby if it is on the Black Sea; tells Sera they are going.",
        "Answers with an eager yes.",
    ],
}
CONTEXT = {
    151: 'Complete artifact-pair discovery: matching dimensions lead to a trial, blinding light, a new blade pattern and a tentative map interpretation. Preserve the unexplained phenomenon; do not add an unsheathing or projection action absent from these lines.',
    152: 'Complete short notification and surprised echo. The messenger reports a waiting person in Alexandria; no identity, office or relationship is supplied here.',
    153: 'Complete guarded meeting with a long-standing opponent of Ottoman rule. The gift and clues are explicit; his identity and the details of helping Sera remain deliberately withheld. Do not invent a priesthood, royal office, kinship or ethnicity.',
    154: 'Complete heat-revelation exchange, including parallel Charles/イファ suggestions and corresponding praise. Keep alternatives structurally distinct rather than presenting both as consecutive events. The lamp heats the cloth; the source does not state that it burns up or is destroyed.',
    155: 'Complete Black Sea rumor, Sera recognition and decision to visit. Preserve hearsay and uncertainty about the town name, Sera’s hesitant speech, the rebuilding of her homeland and her affirmative reaction. Her country does not establish royalty or a relationship to any ruler.',
}


def main():
    path = ROOT / 'B151_B155_42_clean_meanings_before_English.json'
    assert not path.exists()
    packet_path = ROOT / 'clean_source_packet.json'
    packet = load(packet_path)
    records = []
    for group in packet['groups']:
        block = group['block']
        if block not in MEANINGS:
            continue
        assert len(group['records']) == len(MEANINGS[block])
        for original, meaning in zip(group['records'], MEANINGS[block], strict=True):
            records.append(dict(id=original['id'], file_path=original['file_path'], block=block,
                source_reference=original['source_reference'], source_hex=original['source_hex'],
                source_Japanese=original['source_Japanese'], source_selector=original['source_selector'],
                source_complete_preamble_hex=original['source_complete_preamble_hex'],
                source_0100_ancestors=original['source_0100_ancestors'], source_macros=original['source_macros'],
                source_meaning=meaning, exchange_context=CONTEXT[block], earlier_English_unconsulted=True,
                native_speaker_item_terms_localization_andformatting_pending=True, new_credit=0))
    assert len(records) == 42
    save(path, dict(source_packet=str(packet_path), source_packet_sha256=sha(packet_path.read_bytes()),
        records=records, complete_exchanges=[151, 152, 153, 154, 155], source_meanings=42,
        not_final_localized_English_orfive_gate_approval=True, remaining_ordinary_meanings=592,
        typed_caption_meanings_pending=8, earlier_English_unconsulted=True, new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('Saved42 clean-first meanings across five complete exchanges;592 ordinary/eight caption meanings remain;no prior English orcredit.')


if __name__ == '__main__':
    main()
