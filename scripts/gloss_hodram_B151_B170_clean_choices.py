"""Bind each source menu choice to its complete exchange before localized captions."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B151_B170_clean_20261102')
DECISIONS = [
    ('SC1_B167_CHOICE_1308_0', '聞く', 'Choose to hear Cesare’s ship-selection advice.', 'Cesare requests permission to offer an opinion; this selects the full tutorial.'),
    ('SC1_B167_CHOICE_1308_1', '聞かない', 'Choose not to hear the advice.', 'Cesare politely accepts that the admiral has his own principles and prepares to depart; no insult or promise to listen later is stated.'),
    ('SC1_B169_CHOICE_356_0', '受ける', 'Accept Fernando’s coin-game wager.', 'The stake is a drink, and the player taking the last coin loses; this is not acceptance of recruitment.'),
    ('SC1_B169_CHOICE_356_1', '受けない', 'Decline the coin-game wager.', 'This refuses the proposed game, not the man’s later shipboard offer.'),
    ('SC1_B170_CHOICE_894_0', 'ありますが…', 'Tentatively acknowledge having some good alcohol.', 'Responds to Julio’s demand and intuition about the party’s drink; it does not assert expertise in tasting or a named variety.'),
    ('SC1_B170_CHOICE_894_1', 'ないですよ', 'Deny having any.', 'Julio accuses the speaker of lying, leading to the alternative voyage/recruitment route; his accusation is not independent proof.'),
    ('SC1_B170_CHOICE_1314_0', '自分の知らないことを素直に聞く', 'Sincerely ask about something the questioner does not know.', 'This chooses a receptive request for knowledge, which Julio approves.'),
    ('SC1_B170_CHOICE_1314_1', '知っていることを聞いて技量を試す', 'Ask about something the questioner already knows in order to test Julio’s ability.', 'This is a deliberate test, not simply asking what Julio knows; he detects the intention and insists on teaching the questioner.'),
]


def main():
    source_path = ROOT / 'clean_choice_objects.json'
    output = ROOT / 'eight_clean_caption_meanings_before_English.json'
    assert not output.exists()
    source = load(source_path)
    by_id = {r['id']: r for r in source['records']}
    assert len(by_id) == len(DECISIONS) == 8
    records = []
    for record_id, expected, meaning, context in DECISIONS:
        row = by_id[record_id]
        assert row['source_Japanese'] == expected
        records.append(dict(**row, source_meaning=meaning, exchange_context=context,
                            localized_caption_andnative_formatting_pending=True))
    save(output, dict(source_choice_objects=str(source_path), source_choice_objects_sha256=sha(source_path.read_bytes()),
        records=records, source_meanings=8, complete_choice_objects=4, earlier_English_unconsulted=True,
        not_final_localized_captions_orfive_gate_approval=True, new_credit=0, producer_sha256=sha(Path(__file__).read_bytes())))
    print('Saved all8 source caption meanings with complete-exchange decisions; no localized captions,prior English orcredit.')


if __name__ == '__main__':
    main()
