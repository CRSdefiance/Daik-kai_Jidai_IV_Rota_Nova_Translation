"""Clean-source review of31 Tavern rumor, gift and location entries."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.context_tavern_conversations_v763 import CURRENT, ROOT
from scripts.verify_village_wrap_v608 import read, save

MANUSCRIPT = Path('translations/tavern_conversations_editorial_manuscript_v1.json')
IDS = tuple(range(820, 851))
RETAINED = (822, 824, 825, 827, 834, 839, 846, 847)
TEXT = {
    820: '%s of %s is a famous %s around here.',
    821: '%s of %s is an influential %s around here.',
    822: 'Have you visited the nearby town of %s?',
    823: "Have you heard of %s? It's a town near here.",
    824: 'Nothing much to report right now.',
    825: 'Hm?',
    826: 'Oh, I thought you could handle another drink.',
    827: "Hmm... %s, right? Here's to our new friendship!",
    828: "Have you heard of %s? It's out there somewhere, and they say it's beautiful.",
    829: "Oh, what's that?",
    830: "This? It's called %s.",
    831: "This? It's called %s.",
    832: "This? It's called %s.",
    833: "This? It's called %s.",
    834: 'How lovely!',
    835: 'Would you like it?',
    836: 'Do you like it?',
    837: 'Oh, do you like it?',
    838: 'Oh, are you interested?',
    839: 'Could this be for me?',
    840: "Really? I'm so happy! Thank you. I'll treasure it!",
    841: "I see... I'm sorry. That was selfish of me.",
    842: 'The exact location? Hmm... Somewhere around %s, I think.',
    843: 'I know of %s. You might find it %s %s and %s %s of here.',
    844: "%s? I hear it's %s %s of this town.",
    845: '%s? I think I heard it was seen %s %s of here...',
    846: "Ah, '%s'? Apparently, it's very close to this town.",
    847: '%s may catch on here. You could make a fortune if it does!',
    848: 'Sales of %s are really strong in this town right now!',
    849: 'Listen, big news! They say %s may see a boom in %s.',
    850: "They say there's a huge craze in %s for %s. Everyone's talking about it!",
}
GLOSSES = {
    820: 'The named person,a profession associated with the named town,is becoming renowned in this area.',
    821: 'The named person,a profession associated with the named town,wields influence around this area.',
    822: 'Politely asks whether the player has visited the nearby named town.',
    823: 'Casually asks whether the player knows the named town and explains that it is nearby.',
    824: 'There is no particular noteworthy information at present.',
    825: 'The player reacts with a brief questioning hm to a Tavern tip.',
    826: 'Surprised teasing that the player has less drinking tolerance than expected,after they decline another cup.',
    827: 'Checks the player\'s name and proposes a toast to becoming acquainted.',
    828: 'Asks whether the player knows the named item,which exists somewhere in the world and is reportedly beautiful.',
    829: 'Curiously asks what the object is.',
    830: 'The Rafael voice identifies the object by its supplied item name.',
    831: 'The Hodram voice identifies the object by its supplied item name.',
    832: 'The Lil voice identifies the object by its supplied item name.',
    833: 'The Maria voice identifies the object by its supplied item name.',
    834: 'The recipient admires the lovely object.',
    835: 'The Rafael voice asks whether the recipient wants the item.',
    836: 'The Hodram voice asks whether the recipient likes the item.',
    837: 'The Lil voice asks with a light interjection whether the recipient likes it.',
    838: 'The Maria voice asks with a light interjection whether the recipient is interested.',
    839: 'The recipient tentatively asks whether the player is giving the item to her.',
    840: 'Delighted acceptance,thanks and a promise to cherish the gift.',
    841: 'Disappointed acknowledgement,apology and admission that the request was selfish.',
    842: 'Considers the detailed location and tentatively gives the area around the supplied coordinates.',
    843: 'Knows of the named item and says it may be found the stated qualitative distance in each of two cardinal directions from here.',
    844: 'Responds to interest in the item with hearsay about its qualitative distance and direction from this town.',
    845: 'Vaguely recalls hearing that the item was seen the stated qualitative distance and direction from here.',
    846: 'The named item apparently lies very close to this town.',
    847: 'The commodity may become fashionable in the current town,which could be a chance for large profits.',
    848: 'The commodity is selling extremely well in the current town right now.',
    849: 'Excited reported news that the named town may soon see a fashion boom in the named commodity.',
    850: 'Reports a major current fashion boom in the named town for the named commodity and emphasizes its popularity.',
}
NOTES = {
    820: 'Keep person,town and profession in original argument order. Around here avoids incorrectly describing the person as local. Profession values need lowercase English only in this prose provider.',
    821: 'Preserve influence rather than changing it into simple fame; keep all three source arguments and their roles. No gender,rank or kinship is invented.',
    822: 'Retain the already natural complete question; native town-name bounds and macro-like data still require final formatting checks.',
    823: 'Replace the clipped Know question with a complete natural introduction; explicitly retain that the place is a nearby town.',
    824: 'Retain the natural colloquial no-news reply. No source fact or omitted useful rumor is inferred.',
    825: 'Retain the natural questioning interjection. Its original player-only53C24 wrapper differs from both the direct NPC and four-captain table wrappers.',
    826: 'The preceding59 asks the player to have another cup; declining selects826. Localize the teasing drinking remark,not combat strength. Drink stays neutral about liquor versus a regional alternative.',
    827: 'Retain the existing idiomatic toast and supplied admiral short name; the Japanese honorific creates no English title or family relationship.',
    828: 'Out there somewhere conveys the original world-wide vagueness without inventing a known location or definite ownership. Preserve hearsay about beauty.',
    829: 'Use the natural contraction in a direct curious question.',
    830: 'A common idiomatic identification handles singular/plural descriptive item labels without an invented a/the article. Japanese sentence particles do not require forced English gender differences; the following request variants keep their register.',
    831: 'The same natural identification is faithful to the terse Japanese naming statement. Preserve the independent Hodram table slot and real item argument; do not join it to neighboring entries.',
    832: 'Preserve the independent Lil table slot. The natural name construction avoids a plural-label article or verb disagreement.',
    833: 'Preserve the independent Maria table slot and feminine Japanese identification without inventing an English relationship or title.',
    834: 'Retain the short natural expression of admiration.',
    835: 'Would you like it is an idiomatic gentle offer,keeping the source want rather than merely asking for an opinion.',
    836: 'Keep the direct question about liking the object rather than changing it into the Rafael want/offer wording.',
    837: 'Preserve the light interjection and the separate question about liking the item.',
    838: 'Restore interest as the source question,not a different offer or a terse UI fragment.',
    839: 'Retain the natural tentative gift question. It remains a player Yes/No confirmation; no item is promised without that choice.',
    840: 'Restore the explicit happiness and promise to cherish the gift. The old A treasure fragment omitted that promise.',
    841: 'Keep the disappointed acknowledgement and complete apology. Selfish of me is natural English ownership of the request.',
    842: 'The original51580 returns latitude/longitude text beginning with LF and containing alignment spaces,not a region name. Keep the tentative around wording and normalize provider whitespace through the proven formatter; no translator-authored break.',
    843: 'The five source arguments are item,NS distance qualifier,NS direction,EW distance qualifier,EW direction. The qualifiers mean a little/far/very far. There are no numerical coordinates or sequential travel legs here. Private English tables must replace Japanese morphemes without altering shared N/S/E/W UI labels.',
    844: 'Preserve hearsay and the single-axis qualitative distance/direction pair. Do not turn the two source arguments into two sequential turns.',
    845: 'Keep the uncertain recollection of a sighting and the same single-axis pair. No exact numeric travel duration or destination is invented.',
    846: 'Retain the already natural nearby-item rumor and uncertainty. Keep the source item argument and current readable quotation style.',
    847: 'Retain the natural prospective trend/profit statement. May and could preserve both source uncertainties.',
    848: 'Sales of makes the sentence grammatical for both mass names and plural commodity names such as Firearms. Preserve actual current sales rather than substituting an unproven future demand claim.',
    849: 'Keep the attention-getter,reported nature and prospective boom. Original native order is town then commodity; do not exchange them.',
    850: 'Restore reported popularity and the omitted reputation sentence. A craze for works with both plural and mass commodity labels while keeping town/product argument order.',
}
ARGUMENTS = {820: ['person_full_name', 'town_name', 'localized_force_profession'], 821: ['person_full_name', 'town_name', 'localized_force_profession'],
    822: ['town_name'], 823: ['town_name'], 827: ['admiral_short_name'], 828: ['item_name'],
    **{n: ['item_name'] for n in range(830, 834)}, 842: ['native_coordinate_text'],
    843: ['item_name', 'NS_distance_qualifier', 'NS_direction', 'EW_distance_qualifier', 'EW_direction'],
    844: ['item_name', 'distance_qualifier', 'direction'], 845: ['item_name', 'distance_qualifier', 'direction'],
    846: ['item_name'], 847: ['commodity_name'], 848: ['commodity_name'],
    849: ['town_name', 'commodity_name'], 850: ['town_name', 'commodity_name']}


def main():
    proof = read(ROOT / 'native_context.json')
    assert len(proof['392_hint_provider_cases_and6_person_trend_fragments']) == 398
    assert len(proof['eight_original_four_captain_gift_voice_selections']) == 8
    assert proof['untranslated_Japanese_distance_fragments_confirmed']
    assert sha(CURRENT.read_bytes()) == proof['current_ROM_sha256']
    roms = [NdsImage.open(p) for p in ('work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds', CURRENT)]
    tables = [common_message_entries(r.read_file('/COMMON/MESFILE.DK4'), r.read_file('/__arm9__.bin'), clean=i == 0) for i, r in enumerate(roms)]
    records = []
    for n in IDS:
        jp, base, old = [t[n] for t in tables]
        assert TEXT[n].count('%s') == jp.text.count(b'%s') == len(ARGUMENTS.get(n, []))
        if n in RETAINED:
            assert TEXT[n] == ' '.join(old.text.decode('cp932').split()), n
        if 830 <= n <= 833 or 835 <= n <= 838:
            slot = n - (830 if n <= 833 else 835)
            binding = next(r for r in proof['eight_original_four_captain_gift_voice_selections'] if r['selected_ID'] == n)
            speaker = ('Rafael', 'Hodram', 'Lil', 'Maria')[slot]
            context = f'Independent captain voice{slot},original table{binding["original_table"]:#x}; parent53C14,table at formatter SP+270. Source selection is proven for all four indices; alternate complete route activation is not claimed.'
        elif n == 825:
            speaker = 'Player admiral'
            context = 'Original player-only53C24 wrapper at58004/5805C with direct825,return53C5C. Reaction to a Tavern tip,not a bare-NPC dialogue ID.'
        else:
            speaker = 'Original contextual Tavern keeper or barmaid'
            context = ('Original two-axis/single-axis item-location provider;398 total fragment cases bind actual item names and ordered qualitative directions.842 instead calls the original coordinate formatter after a position getter.' if 842 <= n <= 846 else
                'Original commodity rumor/trend provider; native threshold49/50 and actual object getters preserve town/commodity order and distinguish prospective/current reports.' if n >= 847 else
                'Original Tavern gift/rumor/drink conversation. Previous and following source selections remain independent; refusal and gift transfer have separate Yes/No paths.826 follows declining the original another-cup prompt59.')
            binding = {'parent': 0x02053FCC if n == 839 else 0x02054014, 'provider_context_report': str(ROOT / 'native_context.json')}
        records.append({'id': f'COMMON_MESSAGE_{n}', 'message_id': n, 'source_hex': jp.text.hex(), 'japanese': jp.text.decode('cp932'),
            'canonical_source_hex': base.text.hex(), 'current_text_hex': old.text.hex(), 'current_English': old.text.decode('cp932'),
            'source_reference': {'block': jp.block, 'record': jp.record_index, 'offset': jp.block_offset},
            'current_reference': {'block': old.block, 'record': old.record_index, 'offset': old.block_offset},
            'english': TEXT[n] + '{PAD}', 'source_meaning': GLOSSES[n], 'localization_note': NOTES[n],
            'speaker': speaker, 'context': context, 'native_binding': binding, 'runtime_argument_contract': ARGUMENTS.get(n, []),
            'decision': 'retain-wording' if n in RETAINED else 'revise',
            'review': {'source': True, 'context': True, 'localization': True, 'naturalness': True, 'formatting': False},
            'status': 'source-context-prose-reviewed-provider-localization-formatting-and-integration-pending'})
    save(MANUSCRIPT, {'format': 'dk4-common-entry-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
        'encoder': 'dialogue-fixed-v1', 'target_locale': 'en-US', 'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'file_path': '/COMMON/MESFILE.DK4', 'source_clean_COMMON_sha256': sha(roms[0].read_file('/COMMON/MESFILE.DK4')),
        'source_canonical_COMMON_sha256': sha(roms[1].read_file('/COMMON/MESFILE.DK4')), 'source_ROM_sha256': sha(roms[0].source.read_bytes()),
        'current_ROM_sha256': sha(CURRENT.read_bytes()), 'context_evidence': str(ROOT / 'native_context.json'), 'records': records,
        'required_provider_work': ['Private full English cardinal/distance tables for843-845; preserve shared UI labels.',
            'Lowercase profession labels only in820/821 prose.', 'Protect all substituted name bytes in direct and table-selected speech.',
            'Normalize actual coordinate-provider LF/spaces in842 and prove complete glyphs/bounds.'],
        'status': 'research-drafts-not-integrated-not-completed'})
    print('31 clean-source/context English reviews:23 revised drafts,8 retained. Provider localization,complete native formatting,registered integration and actual gameplay remain pending.', flush=True)


if __name__ == '__main__': main()
