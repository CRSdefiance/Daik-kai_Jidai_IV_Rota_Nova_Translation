"""Faithful whole-exchange meanings before consulting this batch's current-ROM English."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import save

ROOT = Path('work/analysis/Hodram_B191_B210_clean_20261104')


if __name__ == '__main__':
    output = ROOT / 'B191_B193_clean_meaning_decisions_v1.json'
    assert not output.exists()
    save(output, dict(blocks={
        '191': dict(context='A coughing speaker and a square shopkeeper discuss a rumored effective medicine made with almonds; a system forecast then connects almonds to a possible Malacca boom. The medicine is unnamed and its effectiveness is reported hearsay, not an independently established medical fact.',
            notes=['The repeated cough sounds belong to the sick speaker and should retain their comic/physical rhythm.', '流行 first suggests an illness going around, then a market fashion. Preserve the progression without naming a disease, remedy or medical authority.'],
            meanings=[
                'Says the cough has been bad lately, then coughs twice.',
                'Asks whether the coughing speaker is all right.',
                'Says yes, all right, though it is a little painful/difficult; coughs twice.',
                'Now that the other speaker mentions it, the shopkeeper has seen many people coughing lately.',
                'Wonders whether some nasty illness is going around.',
                'The shopkeeper heard somewhere that there is a good medicine.',
                'Excitedly asks whether that is true and what medicine it is; coughs twice.',
                'The shopkeeper forgot its name but heard that it uses almonds.',
                'Repeats almonds as a surprised question.',
                'The shopkeeper remembers because the thought of using almonds in medicine was surprising.',
                'Asks whether it works; coughs twice.',
                'The shopkeeper heard that it works unbelievably well and is selling very well.',
                'The coughing speaker decides to look for it.',
                'The shopkeeper offers to look for it too.',
                'Thanks the shopkeeper and coughs twice.',
                'System forecast: almonds may become fashionable/in demand in Malacca.',
            ]),
        '192': dict(context='A source-identified daimyo admires a crafted glass object while a source-identified Japanese guild head responds deferentially. The daimyo wants glass from all over the city for a collection; the system forecasts glass demand in Osaka. Neither a royal identity nor an employment relationship beyond the visible deference is invented.',
            notes=['ギヤマン is explicitly glossed ガラス in the source. Preserve the glass referent and the Japanese cultural register without asserting that it is necessarily cut glass or a diamond.', 'Actor150 is clean-table ギルドの元締め, not an invented samurai retainer. Actor130 is 大名, not a king.'],
            meanings=[
                'The daimyo enthusiastically calls the object wonderful, truly a work of art.',
                'The guild head respectfully agrees with what the daimyo says.',
                'The daimyo assumes such an excellent item must have been made by a renowned artisan.',
                'The guild head respectfully confirms that.',
                'The daimyo had no idea this sort of object was fashionable.',
                'Asks what the object is called.',
                'The guild head respectfully calls it giyaman, with the source explanatory gloss glass.',
                'The daimyo thoughtfully repeats the unfamiliar name giyaman.',
                'Decides to add it to the collection and orders glass from all over the city to be gathered.',
                'The guild head emphatically and deferentially accepts the order.',
                'System forecast: glass may become fashionable/in demand in Osaka.',
            ]),
        '193': dict(context='A guild head and a square shopkeeper politely discuss collecting fine ceramics and complain that ignorant fashion-followers buy them up. A trader then points them out to a port worker as buyers of worthless ceramics at an absurd price, and the two decide to approach them. The joke turns the collectors\' own pretensions back on them; the system forecasts ceramics in Hamburg.',
            notes=['The first pair are the clean-table guild head147/shopkeeper82; the second pair are trader104/port worker113. Do not swap their conversations or invent personal names.', 'The trader\'s previous transaction is tied to the pointed-out group without inventing which individual made a separate purchase or an unsupported count of sales.', 'だんな is a familiar customer address here, not a new social rank or family relationship.'],
            meanings=[
                'The guild head says that the sought-after object was finally obtained the other day.',
                'The shopkeeper recognizes the topic as ceramics.',
                'The guild head says it was indeed a first-rate piece, just as expected.',
                'The shopkeeper praises that and politely asks to see it sometime.',
                'The guild head warmly invites the shopkeeper to visit the speaker\'s home.',
                'The shopkeeper remarks that the recent fashion for collecting ceramics makes good pieces harder to obtain.',
                'The guild head says that people who do not understand value apparently buy them up merely because they are fashionable.',
                'The shopkeeper calls that a real nuisance.',
                'The guild head completely agrees.',
                'Elsewhere in the same exchange, the trader directs the port worker\'s attention to the men over there.',
                'The port worker asks whether the trader means the pair and what is the matter.',
                'The trader says worthless ceramics were recently bought from the trader for an unbelievable price; the reference points back to the pair.',
                'The port worker calls them good customers and, being short of money, suggests going over to speak to them.',
                'The trader likes that idea.',
                'The port worker says it is settled and urges going over.',
                'The trader calls out to a customer in a familiar, wheedling manner.',
                'System forecast: ceramics may become fashionable/in demand in Hamburg.',
            ]),
    }, clean_meanings_not_localized_dialogue_drafts=True, current_ROM_English_unconsulted_in_this_intake=True, new_credit=0))
