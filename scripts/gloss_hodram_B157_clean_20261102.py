"""Read the complete Al recruitment as an exchange, before prior English comparison."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B151_B170_clean_20261102')
MEANINGS = [
    'The employer angrily tells the difficult employee to go wherever he likes and fires him.',
    'The dismissed man accepts the break defiantly and tells the employer to do as he pleases.',
    'Charles wonders what happened and whether there was a quarrel.',
    'Hodram heard the word fired and wonders whether the man worked as a bodyguard.',
    'Asks the employer who that man is.',
    'The employer dismisses him as good for nothing but fighting and says he fired him for not obeying orders.',
    'Hodram asks whether he is skilled.',
    'The employer notices Hodram’s interest, admits that the man’s fighting ability is superb, but complains that he ought at least to carry luggage without arguing.',
    'Charles speculates that an excellent bodyguard may still have a personality problem: perhaps excessive pride or lack of cooperation.',
    'Hodram dryly says Charles himself is hardly cooperative enough to judge others, then sets off.',
    'Charles is surprised that the admiral is serious about pursuing him.',
    'Hodram insists that he must speak to the man directly before deciding.',
    'Charles identifies him and remarks on his impressive, conspicuous physique.',
    'A silent approach or pause.',
    'The man asks what they want.',
    'Hodram observes that he appears to have trained his body extensively.',
    'The man replies dismissively that this is obvious and none of Hodram’s business.',
    'Hodram says he approached because he sees promise in the man; such an attitude will cost him opportunities.',
    'The man reacts indignantly.',
    'Hodram says he has heard that the man lost his bodyguard job and assumes he now has strength with no outlet.',
    'The man asks whether Hodram means to hire him and demands to know who Hodram is.',
    'Hodram formally introduces himself as {MACRO:FI}, an admiral in the Swedish Navy commanding a patrol fleet.',
    'The man acknowledges the admiral’s position but says he has no intention of becoming a sailor.',
    'Hodram challenges his judgment: does he rate Hodram below the employer who just fired him?',
    'Taken aback, the man protests that they have only just met and that Hodram is being hasty.',
    'Hodram uses a masculine pride/reputation challenge, saying that indecision diminishes a man.',
    'The man hesitates under that challenge.',
    'Hodram says he can help the man and demands an immediate decision if the man wishes to follow him.',
    'The man agrees to join his ship, introduces himself as Al and asks to be treated well.',
]


def main():
    output = ROOT / 'B157_29_clean_meanings_before_English.json'
    assert not output.exists()
    packet_path = ROOT / 'clean_source_packet.json'
    group = next(g for g in load(packet_path)['groups'] if g['block'] == 157)
    assert len(group['records']) == len(MEANINGS) == 29
    rows = []
    for source, meaning in zip(group['records'], MEANINGS, strict=True):
        rows.append(dict(id=source['id'], file_path=source['file_path'], block=157,
            source_reference=source['source_reference'], source_hex=source['source_hex'], source_Japanese=source['source_Japanese'],
            source_selector=source['source_selector'], source_complete_preamble_hex=source['source_complete_preamble_hex'],
            source_0100_ancestors=source['source_0100_ancestors'], source_macros=source['source_macros'],
            source_meaning=meaning, exchange_context='Dismissal, cautious inquiry,Charles/Hodram banter,a deliberately provocative approach andAl’s quick recruitment. Preserve Charles’s speculative assessment andHodram’s forceful persuasion rather than declaring the employer’s insults to be narrator facts.',
            earlier_English_unconsulted=True, native_identity_localization_andformatting_pending=True, new_credit=0))
    save(output, dict(source_packet=str(packet_path), source_packet_sha256=sha(packet_path.read_bytes()), records=rows,
        source_meanings=29, complete_exchange=157, not_final_localized_English_orfive_gate_approval=True,
        source_fidelity_notes=['R102 says Hodram can help Al;do not reverse the direction into a request forAl’s help.',
            'The Swedish Navy affiliation andpatrol-fleet admiral role are explicit source facts.',
            'The original dismissal is angry andthe negotiation challenges masculine pride;preserve tone without adding profanity,obedience demands ornew ranks.'],
        earlier_English_unconsulted=True, new_credit=0, producer_sha256=sha(Path(__file__).read_bytes())))
    print('Saved29 clean-first Al recruitment meanings;157 ordinary meanings now saved;no prior English,drafts orcredit.')


if __name__ == '__main__':
    main()
