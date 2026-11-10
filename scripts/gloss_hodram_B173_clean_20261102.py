"""Clean-only meanings for Mikhail's full treasure-information conversation."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B171_B190_clean_20261102')
MEANINGS = [
    'Hodram asks whether something is wrong with Gerhard.',
    'Gerhard greets the admiral; he wants to investigate the objects called 覇者の証 but is troubled by the identity of the person who knows about them.',
    'Hodram asks what the problem is.',
    'Mikhail boasts that the knowledgeable person is none other than himself.',
    'Hodram understands why Gerhard was hesitant.',
    'Gerhard regrets that it had to be this particular man.',
    'Mikhail asks whether Gerhard has something to say to him.',
    'Gerhard hastily denies an objection and politely professes admiration for Mikhail\'s knowledge, but remains uneasy.',
    'Hodram sets that aside and asks Mikhail to tell them about it.',
    'Mikhail laughs and asks whether Admiral FI is interested in 覇者の証.',
    'Hodram does not want irrelevant learned chatter, but wants to know what purpose these objects serve.',
    'Mikhail explains that they are treasures scattered among the different sea regions, said to fall into the hands of whoever rules the seas.',
    'According to ancient writings, there are seven treasures in all, and the seven ancient sages marked their locations on various maps.',
    'Says the person who eventually masters each sea is destined to obtain its map; this is a reported legend, not independent proof of fate.',
    'Hodram finds mere treasure somewhat disappointing.',
    'Gerhard respectfully objects: obtaining them would let FI claim supremacy over the world\'s seas in name and reality, making this a major undertaking for their fleet.',
    'Hodram considers the idea of proof of sovereignty over the seas.',
    'Gerhard asks him to consider the people who follow Admiral FI.',
    'Hodram realizes that a clear objective would give his followers more motivation.',
    'Gerhard confirms that this is what he means.',
    'Mikhail asks why the two are whispering together and whether they are overwhelmed by his knowledge.',
    'Gerhard hastily acknowledges him and asks him not to cause trouble aboard ship.',
    'Mikhail tells him not to worry and laughs.',
    'Hodram asks respectfully whether Mikhail knows how all of the treasures can be collected.',
    'Mikhail says first to become the strongest power in the relevant sea region; influential local people often possess clues to its treasure.',
    'If an evil-minded person holds such a clue, that person will probably have to be defeated. Do not expand this into a requirement to defeat everyone.',
    'Hodram pauses silently.',
    'Next, discover the ruins hidden in the various cities and solve the mystery of the sealed treasure.',
    'Gerhard asks how they are supposed to find those ruins.',
    'Mikhail begins to explain what he himself would do.',
    'Gerhard waits for the explanation.',
    'Mikhail says that, naturally, he would turn to women.',
    'Gerhard angrily draws out Mikhail\'s name, interpreting this as another lecherous diversion.',
    'Mikhail tells him to calm down: a large city should provide some clue about nearby ruins.',
    'Tavern women hear sailors from across the world every day, so their information is extremely valuable.',
    'Of course, such important information probably will not be given away for nothing.',
    'Hodram concludes that some sort of payment is needed.',
    'Mikhail asks him to think more romantically: gifts should be given without expecting anything in return, merely to win a woman\'s heart; his self-serving laughter undercuts the claim.',
    'Hodram dryly asks whether winning her heart is itself something in return. This is the punchline to the professed selflessness.',
    'Mikhail catches himself, admitting that he has said something he should not.',
]


if __name__ == '__main__':
    packet_path = ROOT / 'clean_source_packet.json'
    output = ROOT / 'B173_clean_meanings_before_English.json'
    assert not output.exists()
    packet = load(packet_path)
    group = next(g for g in packet['groups'] if g['block'] == 173)
    assert len(group['records']) == len(MEANINGS) == 40
    rows = []
    for source, meaning in zip(group['records'], MEANINGS, strict=True):
        rows.append(dict(id=source['id'], file_path=source['file_path'], block=173,
            source_reference=source['source_reference'], source_hex=source['source_hex'],
            source_selector=source['source_selector'], source_complete_preamble_hex=source['source_complete_preamble_hex'],
            source_Japanese=source['source_Japanese'], source_meaning=meaning,
            complete_exchange_clean_context_read=True, prior_English_unconsulted=True,
            native_name_terms_preamble_localization_anddisplay_approval_pending=True))
    save(output, dict(source_packet=str(packet_path), source_packet_sha256=sha(packet_path.read_bytes()), records=rows,
        complete_clean_exchanges=1, source_meanings=40,
        context='Gerhard reluctantly seeks Mikhail\'s expertise; Hodram adopts the treasure search as a clear goal for his followers. Mikhail mixes practical map/ruin/tavern clues with his lecherous persona; Hodram punctures his claim of selfless gift-giving.',
        treasure_English_terminology_not_finalized_by_source_gloss=True,
        no_localized_English_drafts_orprior_English_comparisons=True, no_new_editorial_credit=True,
        producer_sha256=sha(Path(__file__).read_bytes()), new_credit=0))
    print('Saved40 further clean meanings;131 speech meanings andtwo menu meanings now saved;302 ordinary meanings remain.')
