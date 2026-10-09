"""Repair early native printf-shape defects from clean Japanese and all neighbors."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXT = {
    70: ("Shall we call at %s?", "Older courteous confirmation of calling at the named port."),
    71: ("%s sailors are unassigned. Is that all right?", "Formal confirmation with the exact number of unassigned sailors."),
    72: ("There are %s unassigned sailors. Is that okay?", "Informal confirmation with the exact unassigned sailor count."),
    73: ("%s sailors remain unassigned. Shall we proceed?", "Older voice asks whether leaving the specified sailors unassigned is acceptable."),
    74: ("We have %s sailors left over. Is that okay?", "Youthful confirmation with the exact number of excess sailors."),
    75: ("%s sailors are still unassigned. Do you approve?", "Formal older confirmation with the exact unassigned sailor count."),
    89: ("The enemy has fled!", "The enemy escaped; no substituted argument belongs to this message."),
    90: ("The town of %s has been defeated...", "Reports defeat of the named town, without substituting a fleet or inventing destruction."),
    285: ("Disband this fleet?", "Confirmation of dissolving this fleet."),
    286: ("We'll leave each ship in dock.", "Each ship will be placed in dock after the fleet is disbanded."),
    287: ("We've discovered %s!", "Reports discovering the substituted target, without inventing its type."),
    342: ("After many years in command of %s, its leader, %s...", "Ending narration names the long-led faction first and its leader second; sentence continues in the next message."),
    343: ("passed away after a full and eventful life.", "Completes the preceding subject's life story: natural lifespan fulfilled and a turbulent life ended."),
    354: ("The pact between %s and %s has been canceled.", "Reports cancellation of the pact between two named parties, preserving order."),
    355: ("%s has asked to cancel the pact!", "The named party proposed cancellation of the pact; not yet a claim it was canceled."),
    767: ("Why, it's %s and %s! Those are such fast sellers that we're often completely out of stock!", "Recognizes both offered goods and says they sell so rapidly that stock frequently runs out."),
    769: ("All right, I'll sweeten the deal. You're selling me %s and %s, and they're flying off the shelves!", "Offers favorable treatment because the customer is selling two goods currently selling rapidly. Does not invent a discount on goods the merchant buys."),
    800: ("Repairs will cost %s gold coins. Is that okay?", "Repair cost in gold coins, followed by confirmation."),
    801: ("Repairs will take one day. Please wait until they're finished.", "Repairs require a one-day wait; no printf argument belongs here."),
    802: ("I can repair it completely for %s gold coins. Shall I?", "Offers complete repairs for the specified gold amount and asks whether to proceed."),
    803: ("The same specifications as %s? That'll cost %s gold coins and take %s days to prepare. Buy it?", "Matching the first named ship's specifications costs the second gold amount and takes the third number of days; asks whether to buy."),
    846: ("Ah, '%s'? Apparently, it's very close to this town.", "The named target apparently lies very close to this town; retains uncertainty."),
    847: ("%s may catch on here. You could make a fortune if it does!", "The named good may become fashionable locally, possibly offering a large profit."),
    909: ("With 1,000 gold coins, we can confuse the enemy. What scheme shall we use?", "Fixed 1000-gold cost can disrupt the enemy; asks for the desired scheme, with no runtime price argument."),
    910: ("1,000 gold coins should be enough. What scheme shall we use?", "Asks confirmation that fixed 1000 gold is enough and which scheme to use."),
    911: ("1,000 gold coins will let us confuse the enemy. What scheme do you want?", "Rough voice names fixed 1000 gold and asks which scheme to use against the enemy."),
    912: ("1,000 gold coins is more than enough to confuse the enemy. Which scheme shall we choose?", "Older voice says 1000 gold is plenty to disrupt the enemy and asks which scheme to choose."),
    913: ("With 1,000 gold coins, we can really surprise them! What should we do?", "Youthful voice says fixed 1000 gold permits surprising the opponent; asks what to do."),
    914: ("About 1,000 gold coins will let us confuse the enemy. Which scheme shall we try?", "Formal older voice retains approximate 1000-gold cost and asks which disruptive scheme to use."),
    924: ("Which town shall we send them to?", "Older voice asks the destination town for the person being dispatched; no place argument is yet provided."),
    925: ("Which town should they go to?", "Informal question about the dispatched person's destination town."),
    927: ("Which town is to receive the rumor?", "Formal question about the town in which to spread a rumor."),
    928: ("Which town gets this rumor?", "Informal question about where to spread the rumor."),
    929: ("Where do you want that rumor spread?", "Rough voice asks in which town to spread the rumor."),
    930: ("Which town shall hear this rumor?", "Older voice asks the destination town for spreading the rumor."),
    944: ("Shall we lure %s's fleet to %s?", "Rough confirmation: first named party's fleet is to be lured to the second named destination."),
    945: ("We're luring %s's fleet to %s. Is that right?", "Older confirmation of luring the first party's fleet to the second destination."),
    947: ("We're to lure %s's fleet to %s. Is that your order?", "Formal older confirmation of fleet owner first, destination second."),
    948: ("We're to turn %s and %s against each other, correct?", "Confirms a scheme to make the two named parties fight each other; no fleet/destination relation is invented."),
}


def main():
    clean = NdsImage.open('work/clean.nds')
    entries = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),
                                     clean.read_file('/__arm9__.bin'))
    owners = {(entries[i].block, entries[i].record_index) for i in TEXT}
    selected = [e for e in entries if (e.block, e.record_index) in owners]
    assert {e.message_id for e in selected} == set(TEXT)
    rows = []
    for e in selected:
        english, meaning = TEXT[e.message_id]
        rows.append({
            'id': f'COMMON_MESSAGE_{e.message_id}', 'message_id': e.message_id,
            'block': e.block, 'record': e.record_index,
            'source_hex': e.text.hex().upper(), 'japanese': e.text.decode('cp932'),
            'previous_japanese': entries[e.message_id - 1].text.decode('cp932'),
            'next_japanese': entries[e.message_id + 1].text.decode('cp932'),
            'english': english.replace('I', 'Ｉ').replace('F', 'Ｆ') + '{PAD}',
            'source_meaning': meaning,
            'speaker': 'Crew confirmation voice, merchant, narrator or strategist',
            'context': (f'Independent native message {e.message_id}, COMMON '
                        f'B{e.block} R{e.record_index}. Repairs early omitted/moved '
                        'arguments and unrelated older text, with every packed neighbor.'),
            'localization_note': ('Fresh clean-source English restores exact sailor counts, '
                                  'town/faction/leader identities, narration continuity, '
                                  'pact cancellation versus a proposal, both goods, favorable '
                                  'selling terms, complete repairs, fixed one-day wait, '
                                  'three purchase arguments, uncertainty, fixed versus '
                                  'approximate 1000-gold costs, destinations, rumors and '
                                  'fleet-owner/destination versus two opposing parties. '
                                  'Printf order is retained. No gender or kinship is invented. '
                                  'Ending narration deliberately continues in the next native '
                                  'message as in the source; no manual breaks are authored. '
                                  'Reserved I/F use narrow full-width glyphs. Previews await review.'),
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False},
        })
    payload = {
        'format': 'dk4-common-entry-manuscript-v1',
        'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
        'encoder': 'dialogue-fixed-v1',
        'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'status': 'draft-awaiting-native-repack-and-formatting-review', 'records': rows,
    }
    Path('translations/common_printf_early_manuscript_v1.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
