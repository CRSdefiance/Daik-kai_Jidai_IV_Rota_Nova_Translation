"""Source/context-reviewed Tavern continuation, not a release approval.

Formatting and runtime selection remain false until the actual consumers pass.
No manual line breaks, cosmetic padding or shortened legacy allocations are used.
"""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_continuation_v768')
MANUSCRIPT = Path('translations/tavern_continuation_editorial_manuscript_v2.json')
TEXT = {
851: "%s has a fleet docked at %s.",
852: "It looks like it'll cost %s gold. Is that all right?",
853: "Looks like it'll cost %s gold. Is that okay?",
854: "That'll cost %s gold. Is that all right?",
855: "Looks like it'll cost %s gold. Okay with you?",
856: "It looks as though it'll cost %s gold. Is that all right?",
857: "Looks like it'll cost %s gold. Is that okay?",
858: "It looks like it'll cost %s gold. Would that be all right?",
859: "Barkeep, a round of the same for everyone, please.",
860: "Barkeep, a round of the same for everyone.",
861: "Barkeep, could everyone have the same, please?",
862: "Barkeep, please give everyone the same.",
863: "Have you heard? Someone may have spotted a rare item called %s in %s...",
864: "Barkeep, a round of drinks for everyone, please.",
865: "Drinks for everyone!",
866: "Barkeep, drinks for everyone, please.",
867: "Barkeep, serve everyone a drink, please.",
868: "It came from a drunk, so I wouldn't trust it. Still, someone like you might make sense of it.",
869: "Certainly. Everyone, this round's on %s!",
870: "%s, here's a tip. They say a rare treasure called %s is hidden in %s.",
871: "Bravo! A round of applause for %s!",
872: "This round's on %s. Enjoy!",
873: "%s, with your skills, I'm sure you'll find it.",
874: "Whoo! Really?! Thanks so much! You're a class act! How generous!",
875: "%s, there's something I'd like you to hear...",
876: "I hear %s has a fleet looking for you. You'd better be careful.",
877: "%s, have you heard the news?",
878: "%s, a fleet from %s is after you.",
879: "By the way, I hear %s has a fleet heading to %s.",
880: "Word is, %s has a fleet heading to %s.",
881: "From what I've heard, %s has a fleet docked at %s.",
882: "A friend says %s has a fleet docked at %s.",
}
GLOSSES = {
851: 'A company fleet is anchored at the named town; relaxed feminine ending.',
852: 'Polite estimate of the gold cost, asking whether it is acceptable.',
853: 'Casual estimate of the gold cost, asking whether it is okay.',
854: 'Feminine cost statement, followed by a polite request for approval.',
855: 'Casual masculine estimate of the gold cost, seeking agreement.',
856: 'Older speaker estimates the gold cost and asks for approval.',
857: 'Young speaker estimates the money needed and gently asks if it is okay.',
858: 'Formal estimate of the cost, asking whether the player minds.',
859: 'Rafael asks the barkeep to give everyone the same thing.',
860: 'Hodram asks the barkeep to give everyone the same thing.',
861: 'Lil warmly asks the barkeep to give everyone the same thing.',
862: 'Maria politely asks the barkeep to give everyone the same thing.',
863: 'Asks if the listener has heard the uncertain report of someone seeing a rare item with the supplied name in a supplied region.',
864: 'Rafael asks the barkeep for drinks for everyone.',
865: 'Hodram calls for drinks for everyone.',
866: 'Lil asks the barkeep to give everyone drinks.',
867: 'Maria asks the barkeep to serve everyone a drink.',
868: 'The report came from a drunk and cannot be trusted, but someone of the player\'s ability might understand something from it.',
869: 'The barkeep formally acknowledges the request and announces that the named admiral is providing everyone a round.',
870: 'Addresses the player and offers a useful rumor: a rare treasure with the supplied item name is hidden in a supplied region.',
871: 'Cheers and applause, praising the named admiral with a gendered familiar form of address.',
872: 'The barkeep announces that today\'s drinks are on the named admiral and invites everyone to enjoy themselves.',
873: 'Addresses the player and expresses confidence that a person of their skill will find it.',
874: 'A surprised, enthusiastic thanks, praising the player\'s style and generosity.',
875: 'Formally addresses the admiral by surname and introduces something the speaker wants them to hear.',
876: 'Reports that a company fleet is following the player\'s whereabouts and advises caution.',
877: 'Casually addresses the player and asks whether they have heard.',
878: 'A company fleet is pursuing the player; the second source argument is a vocative addressing the player, not a third person.',
879: 'A polite aside reports hearsay that a company fleet is heading for a town.',
880: 'A casual aside reports overheard news that a company fleet is heading for a town.',
881: 'Politely reports that, from what the speaker has heard, a company fleet is anchored at a town.',
882: 'Reports news from a companion that a company fleet is anchored at a town.',
}
ARGUMENTS = {
851: ['organization_name', 'town_name'],
**{n: ['native_fullwidth_cost'] for n in range(852, 859)},
863: ['item_name', 'private_full_region_phrase'],
869: ['admiral_surname'],
870: ['player_vocative', 'item_name', 'private_full_region_phrase'],
871: ['admiral_surname', 'source_gendered_address_unused_in_English'],
872: ['admiral_surname', 'source_gendered_address_unused_in_English'],
873: ['player_vocative'], 875: ['admiral_surname'], 876: ['organization_name'],
877: ['player_vocative'], 878: ['organization_name', 'player_vocative'],
**{n: ['organization_name', 'town_name'] for n in range(879, 883)},
}
RETAINED = {865, 871, 872, 874}


def main():
    packet = read(ROOT / 'source_and_neighbors.json')
    evidence = read(ROOT / 'native_context_complete.json')
    assert not evidence['remaining_context_gates']
    partial = read(evidence['prior_provider_proof'])
    assert sha(Path(evidence['prior_provider_proof']).read_bytes()) == evidence['prior_provider_proof_sha256']
    records = []
    for row in packet['rows']:
        n = row['id']
        if n not in TEXT: continue
        if 852 <= n <= 858:
            speaker = 'Assigned role3 officer; original eight-voice selector, including -1 fallback for voice1'
            context = 'Original58350 computes cost and ABF50 expands fullwidth digits. Original53CB0 resolves role3 officer, selects table02118400, and supplies exactly one amount through the original va_list to YesNo core54058/parent53D24.'
            note = 'Restore an ordinary spoken estimate/approval question with the source voice; gold is a mass noun for every numeric value. Preserve the original fullwidth amount; do not insert singular/plural coin logic or mock a new amount.'
        elif n in (*range(859, 863), *range(864, 868)):
            speaker = ('Rafael', 'Hodram', 'Lil', 'Maria')[(n - (859 if n <= 862 else 864))]
            context = 'Original four-captain selector53C6C, table021166F0 for859-862 or02116810 for864-867, through parent53C14. These are route alternatives, not four successive speakers.'
            note = 'Use natural requests with appropriate courtesy. The familiar address to the barkeep does not establish a father/uncle relationship; do not translate it literally.'
        else:
            speaker = 'Original Tavern rumor/round NPC selected by the native scene'
            context = 'Direct portrait consumer53FE4/parent54014. Source and independently supplied native caller fragments determine arguments and selectable alternatives; adjacent storage does not establish a sequential conversation.'
            note = 'Preserve the source information, hearsay and conversational tone as one ordinary American English paragraph.'
        if n in (863, 870):
            note += ' Region is a native item region index, not a town. Use private full region phrases verified from 北海/地中海/アフリカ/インド洋/東南アジア/東アジア/新大陸; preserve global short UI names. Named item phrasing works for plural, mass and singular names.'
        if n in (871, 872):
            note += ' Retain the established natural omission of the second source gendered address. The native caller still passes both surname and vocative; the English intentionally prints only the surname. No dropped fact, new rank or removed native argument is implied.'
        if n in (870, 873, 877, 878):
            note += ' Sir/Ma\'am addresses the player and is not a person being sought. Put this capitalized native vocative at sentence start.'
        if n == 878:
            note += ' Requires a narrowly scoped native argument permutation [1,0] at58070/58078; both original field values must remain exact and all other callers unchanged before integration.'
        if n in (851, 876, 878, 879, 880, 881, 882):
            note += ' Organization names are obtained from actual company virtual+8 getters, not surnames or country guesses. Preserve their complete supplied name. Use has a fleet or a fleet from to avoid the unnatural Bergstrom Fleet\'s fleet; this does not assert that there is more than one fleet.'
        if n in (879, 880, 881, 882):
            note += '7200 source fragment cases distinguish destination byte3F from docked getter34674/byte3C and formal/casual context+8. Do not conflate heading toward a town with being anchored there.'
        english = TEXT[n]
        assert english == ' '.join(english.split()) and english.isascii()
        expected = len(ARGUMENTS.get(n, [])) - int(n in (871, 872))
        assert english.count('%s') == expected
        if n in RETAINED: assert english == ' '.join(row['current_English'].split())
        records.append({'id': f'COMMON_MESSAGE_{n}', 'message_id': n,
            'interaction_group': 'Tavern-cost-rounds-treasure-and-fleet-rumor-alternatives',
            'source_hex': row['source_hex'], 'japanese': row['Japanese'],
            'source_reference': row['source_reference'], 'canonical_source_hex': row['canonical_hex'],
            'current_text_hex': row['current_hex'], 'current_English': row['current_English'],
            'current_reference': row['current_reference'], 'english': english + '{PAD}',
            'source_meaning': GLOSSES[n], 'speaker': speaker, 'context': context,
            'localization_note': note, 'decision': 'retain' if n in RETAINED else 'revise',
            'source_native_arguments': ARGUMENTS.get(n, []),
            'English_argument_source_indices': [1, 0] if n == 878 else [0] if n in (871, 872) else list(range(expected)),
            'review': {'source': True, 'context': True, 'localization': True, 'naturalness': True, 'formatting': False},
            'status': 'source-context-prose-reviewed-native-layout-runtime-gameplay-integration-pending'})
    assert len(records) == 32
    save(MANUSCRIPT, {'format': 'dk4-common-entry-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
        'encoder': 'dialogue-fixed-v1', 'target_locale': 'en-US',
        'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'status': 'research-draft-formatting-runtime-and-gameplay-pending', 'file_path': '/COMMON/MESFILE.DK4',
        'source_clean_COMMON_sha256': packet['pins'][0]['COMMON_sha256'],
        'source_canonical_COMMON_sha256': packet['pins'][1]['COMMON_sha256'], 'source_pins': packet['pins'],
        'native_context_proof': str(ROOT / 'native_context_complete.json'),
        'native_context_proof_sha256': sha((ROOT / 'native_context_complete.json').read_bytes()),
        'records': records, 'remaining_gates': ['Native printf/wrapping/complete-font preview matrix',
            'Owned no-growth runtime selector and private region providers', 'Registered integration and exact clean patch',
            'Targeted cold-boot scene/transition/state verification'], 'full_goal_complete': False})
    print('32 source/context/prose-reviewed drafts:28 revise,4 retain; no formatting or release completion claimed.', flush=True)


if __name__ == '__main__': main()
