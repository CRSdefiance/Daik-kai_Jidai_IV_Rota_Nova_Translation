"""Clean whole-exchange meanings and exact prices for the six-step seller scene."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B191_B210_clean_20261104')


if __name__ == '__main__':
    output = ROOT / 'B198_B200_clean_meaning_decisions_v1.json'
    caption_output = ROOT / 'B200_twelve_clean_caption_meanings_v1.json'
    assert not output.exists() and not caption_output.exists()
    save(output, dict(blocks={
        '198': dict(context='Two speakers discuss having tried a drink called 清酒 and agree to go drinking. Julio overhears and excitedly identifies it as the legendary drink he seeks, addressing FI as admiral and rushing to buy it. The system forecasts 清酒 in Hangzhou.',
            notes=['清酒 needs its established trade-good term bound before localized approval. Preserve the rice ingredient and cultural identity; do not invent a brand or a distillation process.', 'Julio\'s conclusion about the legendary drink is his excited inference, not narrator confirmation that an ordinary trade good is a unique treasure.'], meanings=[
                'One speaker says a drink called seishu/清酒 was tried the other day.',
                'The port worker says it was tried too.',
                'The first speaker says it is quite good.',
                'The port worker says it is reportedly made from rice.',
                'The first is surprised that it is made from something like rice.',
                'Talking about it has made the port worker want a drink, so the other is invited for one now.',
                'The first speaker likes that idea.',
                'With that decided, the port worker urges going quickly.',
                'Julio reacts with amazement, says this must be the legendary drink, and asks Admiral FI whether that was heard.',
                'Julio can no longer sit around and announces immediately going to buy this drink called 清酒.',
                'System forecast: 清酒 may become fashionable/in demand in Hangzhou.',
            ]),
        '199': dict(context='A port worker and a tavern patron smell a house-special dish, order one, taste it and enthusiastically praise it. The barkeep says it contains plenty of cheese. Their decision to spread the word leads to a cheese forecast for Veracruz.',
            notes=['The dish is not named; do not invent pizza, fondue, a recipe, separate portions or extra ingredients.', '親父 addresses the barkeep familiarly, not a father. だまされたと思って is an invitation to try despite doubt, not an admission of actual fraud.'], meanings=[
                'The port worker notices what seems to be a pleasant smell and asks about it.',
                'The patron sniffs and agrees.',
                'The port worker asks the barkeep what the smell is.',
                'The barkeep says it is the house specialty, full of cheese and delicious.',
                'The patron questions whether it is really good.',
                'The barkeep says not to ask something so obvious.',
                'The port worker orders one for the two of them as well.',
                'The barkeep asks for just a short wait and promises to bring it right away.',
                'The barkeep announces that the order is ready.',
                'The port worker marvels at how quick it really was.',
                'The barkeep urges trying it first, even if they remain doubtful.',
                'The port worker agrees.',
                'The port worker chews the food.',
                'The patron chews the food.',
                'The port worker gives an elongated, enthusiastic exclamation that it is delicious.',
                'The patron excitedly agrees that it is excellent.',
                'The barkeep confidently says the reaction proves the earlier claim.',
                'The port worker feels compelled to tell everyone about it.',
                'The patron agrees and tells the barkeep the dish is certain to become hugely popular.',
                'System forecast: cheese may become fashionable/in demand in Veracruz.',
            ]),
        '200': dict(context='The source Shady Man offers Hodram an unnamed useful item for200000 gold. A sequence of six conditional buy/decline menus can lead through offers of100000,70000,50000,40000 and30000 gold, with optional companions offering parenthetical advice. Purchase and walk-away endings differ. A displayed one-point FI魅力 increase occurs in the early successful-sale branch; exact state-award conditions remain governed by the original commands.',
            notes=['All six menu labels literally mean buy/do not buy at the current offer. Do not rename the last refusal Haggle when the seller can walk away.', 'Carlo says at least two more price reductions should be possible after the first halving; he does not assert an exact total number of bargaining rounds.', 'Do not name the item, invent its effect, or make conditional companion asides a simultaneous conversation. Keep their parenthetical/private character.', 'Bind the exact English UI name for 魅力 before localized approval; it is a character attribute, not morale or money.'], meanings=[
                'The seller thinks Hodram looks wealthy and gives a long peculiar laugh.',
                'Hodram responds with a silent pause.',
                'The seller offers something good for200000 gold and repeats the long laugh.',
                'Fernando challenges whether the seller is overcharging.',
                'On this purchase branch, the seller calls the buyer generous and promises the thing will surely be useful.',
                'System notice: FI\'s charm/charisma attribute has increased by1.',
                'The seller gives in to the refusal and offers a price of100000 gold, again laughing.',
                'Carlo privately tells the admiral that halving the price at once shows a large markup and suggests at least two more rounds of bargaining are possible.',
                'On this purchase branch, the seller laughs, acknowledges the buyer\'s skill and promises the thing will be useful.',
                'The seller next offers70000 gold with the peculiar laugh.',
                'Fernando privately says that, in the same position, one more bargaining attempt would be made.',
                'On this purchase branch, the seller hands over the item, promises usefulness and laughs.',
                'The seller calls the buyer surprisingly grasping and offers50000 gold with a shorter laugh.',
                'Julio privately says one more attempt to hold out would be made.',
                'Yifa privately urges getting the price reduced further.',
                'On this purchase branch, the seller acknowledges a shrewd negotiator and hands over the item.',
                'The seller hesitantly states40000 gold, pauses and gives a brief laugh.',
                'Carlo privately judges that this may be a good point to buy.',
                'On this purchase branch, the seller had thought the buyer would never buy and now hands over the item.',
                'The seller begs for a purchase and says30000 gold will do.',
                'Julio privately doubts the price will go any lower.',
                'On this purchase branch, the seller clicks the tongue, complains about selling too cheaply, and tells the buyer to take good care of the item.',
                'In the refusal ending, the seller says it seems the buyer lacks an eye for value.',
                'The seller dismisses the buyer and says the item will be sold to someone else.',
            ]),
    }, clean_meanings_not_localized_dialogue_drafts=True, current_ROM_English_unconsulted_in_this_intake=True, new_credit=0))
    source_path = ROOT / 'clean_choice_objects.json'
    source = load(source_path)
    rows = []
    prices = {218: 200000, 582: 100000, 832: 70000, 1156: 50000, 1370: 40000, 1588: 30000}
    for row in source['records']:
        if row['block'] != 200:
            continue
        assert row['source_Japanese'] == ['買う', '買わない'][row['source_index']]
        value = dict(row)
        price = prices[row['source_command_offset']]
        value.update(source_meaning=('Buy the offered unnamed item' if row['source_index'] == 0 else 'Decline the offered unnamed item') + f' at the current asking price of{price} gold.',
            exchange_context='Complete B200 six-price purchase/refusal exchange and conditional companion asides; refusal can cause a lower offer or the final walk-away, according to original branches.',
            all_source_indices_andliteral_captions_preserved=True, clean_meaning_not_localized_caption=True,
            current_ROM_English_unconsulted_in_this_intake=True, new_credit=0)
        rows.append(value)
    assert len(rows) == 12
    save(caption_output, dict(records=rows, complete_source_menus=6, source_meanings=12,
        source_object_packet=str(source_path), source_object_packet_sha256=sha(source_path.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()), new_credit=0))
