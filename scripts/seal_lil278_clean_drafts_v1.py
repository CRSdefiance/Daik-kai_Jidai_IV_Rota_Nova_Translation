"""Bind the authored Lil B299–B311 glosses and drafts to the clean packet."""
from pathlib import Path
import subprocess
import sys

from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/Lil278_B299_B311_clean_20261110')
DRAFTS = Path('translations/editorial_checkpoints/Lil278_clean_20261110_v1')
CONTEXTS = {
    '299': "A forest expedition encounters a giant snake. Fighting drives it off and some sailors appear injured. Lil bolts in the flight branch and apologizes after Camille rallies the party. Later she gets stuck in mud. Her companions suspect a bottomless bog, help her out, and spot something ahead.",
    '300': "A contact tells Lil about the Colosseum after hearing she is looking for ruins and reminds her to buy a map. The echo question carries selector CF.",
    '301': "The party rations water and loses visibility in a sandstorm. At an oasis a short rest prompts grumbling. The longer rest passes one day and recovers sailor fatigue. The crew later spots something as they approach the edge of the desert.",
    '302': "A dancer thanks Lil for helping her improve. She relays a rumor about treasure at a mosque far inland that honors a king from long ago. Recognition by the king is a reported condition.",
    '303': "A patron relays that the Basra guild was looking for Lil.",
    '304': "Basra will host an Indian Ocean spice exhibition with sales. Venue preparations leave the organizers short of sale stock. Lil must bring one cargo hold each of nine distinct spices in one shipment because there is nowhere to store staggered deliveries.",
    '305': "Separate conditional reminders identify each missing spice. A complete delivery yields payment and reward of 40,000 gold coins, plus a slight Basra share gain. The guild contact offers a reportedly valuable item from an unspecified source and leaves its identity unstated in this exchange.",
    '306': "A map check and farewell precede a missing bridge over a fast river. Flood damage is conjecture. The upstream log-bridge detour costs a day and sailors appear tired. The other branch proposes crossing on foot, then finds a ferry and pays 100 gold coins. The final object spotted remains implicit.",
    '307': "A temple invitation reminds Lil of the golden temple on her map. The contact recognizes it and offers to accompany her partway. The map guides the rest of the trip.",
    '308': "Lil recalls she is supposed to buy rice.",
    '309': "Lil returns with the rice and is reprimanded for her manners. The next errand is tea and sugar, again at her own expense. She questions the offerings and protests that she is not Buddhist.",
    '310': "Two conditional reminders lead to the return with tea and sugar. Lil's strained politeness leads into the lesson on humility and courtesy. The elder gives directions to a village far northeast of China near icy seas, by an eastern coastal peak at the base of a large peninsula. Preserve the danger warning and the instruction to keep the Proof from people with evil intent. The 20,000 gold reimburses purchases and pays for the errands. Lil catches herself mid-question and protests being treated like a child.",
    '311': "Eight voices recall the clan guarding the map to the Proof and the village far northeast of China. They propose visiting with distinct degrees of urgency, curiosity and certainty.",
}


def main():
    packet = ROOT / 'clean_source_packet.json'
    authored = ROOT / 'authored_B299_B311_v1.json'
    output = ROOT / 'clean_part_B299_B311_v1'
    assert not authored.exists() and not output.exists()
    records = []
    for filename in ['B299_drafts.txt', 'B300_B305_drafts.txt', 'B306_B311_drafts.txt']:
        for line in (DRAFTS / filename).read_text(encoding='utf-8').splitlines():
            short_id, meaning, english = line.split('|')
            prefix = 'DK4_MES_' if '_R' in short_id else 'SC2_'
            records.append([prefix + short_id, meaning, english])
    source_ids = [r['id'] for group in load(packet)['groups'] for r in group['records']]
    assert len(source_ids) == 278 and [r[0] for r in records] == source_ids
    save(authored, dict(contexts=CONTEXTS, records=records, whole_clean_exchanges_read_before_drafting=True,
        current_English_not_consulted=True, new_credit=0))
    subprocess.run([sys.executable, '-m', 'scripts.save_clean_editorial_part_v3', '--packet', str(packet),
        '--authored', str(authored), '--out', str(output)], check=True)
    subprocess.run([sys.executable, '-m', 'scripts.seal_clean_editorial_parts_v2', '--packet', str(packet),
        '--parts', str(output), '--expected-records', '278'], check=True)


if __name__ == '__main__':
    main()
