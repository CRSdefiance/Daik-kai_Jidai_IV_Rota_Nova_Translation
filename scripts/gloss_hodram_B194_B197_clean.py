"""Source-first meanings for medicine, dye, tobacco and chili market conversations."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import save

ROOT = Path('work/analysis/Hodram_B191_B210_clean_20261104')


if __name__ == '__main__':
    output = ROOT / 'B194_B197_clean_meaning_decisions_v1.json'
    assert not output.exists()
    save(output, dict(blocks={
        '194': dict(context='Two speakers gossip about the wealthy master of this mansion and the reported cure of an unexplained illness with commercially sold medicine. Excitement about a reputed cure-all leads them to seek it; the system predicts medicine demand in Havana.',
            notes=['Retain the report/reputation framing; do not name the illness or medicine, confirm universal effectiveness, or introduce a doctor.', 'The mansion\'s 旦那 is its master/householder, not an invented king, noble rank or family relation.'], meanings=[
                'One speaker asks whether the other has heard the news.',
                'The other asks what news.',
                'The first means the story about the master of this mansion.',
                'The other asks whether this is about his illness of unknown cause.',
                'The first confirms that is the story.',
                'The other says everyone knows that much.',
                'The first asks whether the other knows what happened afterward.',
                'The other repeats afterward as a question.',
                'The first says the illness was reportedly cured in one go by medicine sold commercially.',
                'The other incredulously asks whether commercially sold medicine cured an illness with an unknown cause.',
                'The first confirms that is the report and calls it an amazing story.',
                'The other agrees it is amazing, but asks whether it is true.',
                'The first says it apparently is true, and the medicine also has a reputation for working on every illness.',
                'The other is impressed and wants some medicine like that too.',
                'The first suggests going to buy it.',
                'The other enthusiastically agrees to go.',
                'System forecast: medicine may become fashionable/in demand in Havana.',
            ]),
        '195': dict(context='A reluctant square shopkeeper and an insistent subordinate discuss a dye needed for a particular color. The subordinate repeatedly insists on buying before competitors exhaust the supply and reassures the sulking shopkeeper about profit. The system predicts dyes in Calicut.',
            notes=['親父さん is familiar address to the proprietor here, not a proven father relationship.', 'No particular dye/color name, price, purchasing quantity or monopoly is supplied. Keep the repeated doubtful question/insistent answer pattern.'], meanings=[
                'The shopkeeper concludes that only that dye can produce this color.',
                'The subordinate agrees and warns that people from other shops will buy up the supply unless it is purchased now.',
                'The shopkeeper hesitates with an objection.',
                'The subordinate challenges the lack of urgency and says it will be too late after the dye sells out.',
                'The shopkeeper doubts it will sell out just because they do not rush to buy immediately.',
                'The subordinate insists otherwise: it is extremely popular and will soon be gone.',
                'The shopkeeper asks doubtfully whether that is so.',
                'The subordinate emphatically says yes.',
                'The shopkeeper gives in and leaves the matter to the subordinate.',
                'The subordinate asks the proprietor not to sulk and insists that securing this color will surely be profitable.',
                'The shopkeeper repeats the doubtful question.',
                'The subordinate again insists that it is so.',
                'System forecast: dyes may become fashionable/in demand in Calicut.',
            ]),
        '196': dict(context='One speaker asks a port worker about tobacco and admits never having tried it. The port worker applies exaggerated social pressure and offers a chance to try it; the system forecasts tobacco in Istanbul.',
            notes=['Keep the port worker\'s speculative exaggeration that perhaps everyone else in town has tried it. It is peer pressure in dialogue, not a narrator\'s established census.', 'The source says smoking tobacco, without specifying cigarettes, cigars, pipes, packs, age or a purchase.'], meanings=[
                'Asks whether the other has ever smoked tobacco.',
                'The port worker asks in surprise whether the speaker has not tried it yet.',
                'Admits not having had an opportunity and therefore never having tried it.',
                'The port worker marvels at this despite its popularity and suggests the speaker may be the only person in the city who has not tried it.',
                'The speaker hesitantly wonders whether that is true and says there is a desire to try it too.',
                'The port worker confirms, offers to let the speaker smoke and tells the speaker to follow.',
                'The speaker hesitantly agrees.',
                'System forecast: tobacco may become fashionable/in demand in Istanbul.',
            ]),
        '197': dict(context='Three Ladies discuss a delicious, stimulating meal. One reveals chili peppers as the secret, explains that they suit local ingredients and are not very expensive, then offers to teach the others because they are friends. The system forecasts chili peppers in Seoul.',
            notes=['Friendship is explicit in the final reply; no personal names, marriage, noble titles or family relationships are supplied.', 'The source says a kind of spice and local ingredients. Do not name a specific dish or turn the meal into a different commodity.'], meanings=[
                'The first Lady exclaims over the delicious meal and says it was the first time having food this wonderful.',
                'The second agrees and calls its flavor stimulating/exciting.',
                'The first asks how such delicious food can be made.',
                'The third chuckles and reveals that the secret is this ingredient.',
                'The first reacts with a puzzled question.',
                'The third calls it chili pepper, says it is reportedly a kind of spice, and explains that it goes very well with ingredients from around here.',
                'The first wonders whether it is expensive.',
                'The third says it is not particularly expensive.',
                'Relieved, the first considers trying it in tonight\'s cooking.',
                'The second wants to cook with it too.',
                'The third offers to show them how to cook with it now.',
                'The first is delighted and asks whether the offer is real.',
                'The second calls the third kind.',
                'The third says it is only natural because they are friends.',
                'System forecast: chili peppers may become fashionable/in demand in Seoul.',
            ]),
    }, clean_meanings_not_localized_dialogue_drafts=True, current_ROM_English_unconsulted_in_this_intake=True, new_credit=0))
