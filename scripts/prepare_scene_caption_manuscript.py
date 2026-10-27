"""Full-source natural English for all four native scene-caption arrays."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_common_scene_caption_duplicates import CURRENT_SHA, captions

# Each line is one complete label, never a manually wrapped presentation line.
TEXT = {
    0: '''Port Town 1
Clau and Raphael
Ship Repairs
Raphael in Profile (Large)
Julio's Shop
Lil and Raffy
Meeting Room
Arcadius's True Identity 1
Arcadius's True Identity 2
A Bustling Bullring
The Matador Appears
Emilio Gets Hurt
Sickroom
Uddin and His Followers 1
Uddin and His Followers 2
Raphael and a Violin in the Moonlight 2
Raphael Playing, Up Close
Sera Listening, Up Close
Irene and a Dejected Raffy
Charlotte Appears
Charlotte Up Close
The Wilderness of the New World
Charlotte's House
Charlotte Offers Flowers
Clau Playing with Children
Maria and Raffy 1
Yukihisa Remains on Guard
Hayreddin
A Ship in Dock
Simon and Valdes
A Bustling Village
Charlotte Wearing a Flower Crown
Torchlight and Two Silhouettes
Raphael's Audience with the King
Claudio and Arcadius 1
Claudio and Arcadius 2
Claudio and Arcadius 3
Raffy and His Companions
Clau and Arcadius in a Panic
Raffy's Ending 1
Raffy and Clau's Ending
Raffy's Ending 2
Raffy and Charlotte
Clau's Happiness
Janus, Later On
The Two Share a Conversation''',
    1: '''Enemy Ships Spotted! (Large)
Hodram Appears
Aboard a Busy Ship
Hodram Rises from His Seat
Hodram Addresses His Crew
Lil and Hodram
Angelo in Battle
Angelo's Defeat
The Fleet Appears
The Captive Princess
Hodram Reaches Out
Hodram Is Wounded
Sera and a Knife
The Two Left Behind
Sera's Smile
Raphael and a Violin in the Moonlight 2
Sera Listening, Up Close
Hodram Comes for Sera
Beloved Elysion
Hodram Versus Escante
Sera's Homeland
Kamil and Hodram
Hodram and Maria
Making Up
Ironclad
Wounded Hayreddin and Hodram
Sera's Rescue
Sera and Hodram Reunite
Hodram's Audience with the King
Hodram's Farewell to Sera 1
Hodram's Farewell to Sera 2
Hodram's Farewell to Sera 3
Hodram's Farewell to Sera 4
Hodram's Farewell to Sera 5
Hodram and Gerhard
Hodram's Smile
A Ship Sails Away
Hodram Gazes at the Stars
Sera Gazes at the Stars
Sera Stands Outside the Window
A Portrait of the Two''',
    2: '''Exhausted Kamil and Energetic Lil
Lil Looks Back at Town from the Ship
Lil Sets Off
Clifford Appears
Lil in a Dress (Large)
Lil and Clifford
A Feast
Lil and Hodram
Lil Throws Her Arms Around Kamil
Ian at a Loss
Ian's Misfortune
Beautiful Ian
Lil and Samwell
Inside Kuhn's Mansion
Kamil and Hodram
Lil Is Attacked
Welcome Back, Kamil
The Kuhn Family Locket
Jam's "Yahoo!" 1
Jam's "Yahoo!" 2
The Tomato Craze
Julian's Story
Clifford Takes a Hostage
A Ship in Flames (Large)
Clifford's Death
With the Sunset at Their Backs
A Bashful Lil
Lil Gazes at Kamil
The Kiss
The Two Embrace
Lil in a Wedding Dress
The Two Face Each Other
Church
Tulips in Full Bloom (Large)
The Two Open the Church Doors
Lil in the Rain
Lil Raises Her Head
At Kamil's House
Lil and Kamil's First Meeting''',
    3: '''Maria Hears a Report (Large)
Maria Up Close
Ian and Maria
Maria Talks to Flowers and Birds
A Room in a Chinese Mansion
Yifa Appears
Yifa's Taoist Magic
Maria's Resolve
Carlo Stands Before a Grave
Ian and Samwell
A Fleet Battle
Maria in Profile
Al Leaves the Tavern
Aziza Appears
Rebellion Breaks Out
Three Allies Come to Help
An Encounter with Raphael
Janus and a Ship
Rocco's Portrait
Bianca
Angelo and Bianca
Gerhard's Mansion
Charles's Factory
A Pitiful Mivor
Cristina's Dance
Cristina Up Close
A Drowning Child
Cristina Holds a Child
You Can Do It, Mivor!
The Two Make a Good Match
Maria and Hodram
Richard Steps on a Rose
Richard's Final Moments
Maria and Her Assembled Subjects
Maria's Relaxed Smile
Maria and Her Companions at the Grand Review
Maria
An Image of Maria''',
}

NOTES = {
    (0, 26): 'Zanshin is continued alertness after a martial action; remains on guard conveys the state without unexplained Japanese terminology.',
    (2, 18): 'The source writes ヤホウ. Jam repeatedly cries Yahoo! in Lil recruitment/romance dialogue; preserve that distinctive exclamation and variant 1.',
    (2, 19): 'Same source exclamation as variant 1, preserving variant 2; see lil_deep_route_v15.json and lil_deep_route_v68.json.',
    (3, 6): '道術 describes Yifa\'s Taoist arts/magic. The source ends よ; caption wording retains the subject and art without forcing a conversational particle.',
    (3, 35): '総見式 is a grand review ceremony; the caption includes Maria and companions. Keep review neutral rather than inventing a specific fleet or army.',
}


def compile_manuscript(inventory):
    if inventory['candidate_sha256'] != CURRENT_SHA or inventory['route_caption_counts'] != {'0': 46, '1': 41, '2': 39, '3': 38}:
        raise ValueError('Complete source-locked route-caption inventory required')
    labels = {route: text.splitlines() for route, text in TEXT.items()}
    if {str(route): len(rows) for route, rows in labels.items()} != inventory['route_caption_counts']:
        raise ValueError('Every complete route caption must be authored')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    expected = {(row['route_index'], row['index']): row for row in captions(clean)}
    records = []
    for source in inventory['captions']:
        route, index = source['route_index'], source['index']
        if (route, index) not in expected or any(source[key] != expected[(route, index)][key]
                                               for key in ('pointer_field', 'offset', 'source_hex', 'japanese')):
            raise ValueError('Caption Japanese source or native ownership changed')
        english = labels[route][index]
        if not english or english != english.strip() or any(not 32 <= ord(c) <= 126 for c in english):
            raise ValueError('Captions require one complete printable ASCII label')
        records.append({
            'id': f'SCENE_CAPTION_ROUTE_{route}_{index:02d}',
            'route_index': route, 'index': index,
            'pointer_field': source['pointer_field'], 'source_offset': source['offset'],
            'source_hex': source['source_hex'], 'japanese': source['japanese'],
            'matching_common_ids': source['exact_remaining_common_ids'],
            'english': english, 'speaker': 'Scene viewer',
            'source_meaning': 'Scene caption: ' + english,
            'context': f'Native route {route} scene-viewer array entry {index}; complete caption selected and centered at y70. Not a COMMON consumer classification.',
            'localization_note': NOTES.get((route, index),
                'Fresh clean-source caption localized as a natural English title; preserve named people, action, numbered variants and large-image marker. Established route spellings retained.'),
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False},
            'presentation': 'native-scene-caption-ascii-pending-pool-and-raster-proof',
            'english_bytes_with_nul': len(english) + 1,
            'native_centering_width_pixels': len(english) * 6,
            'source_bytes_with_nul': len(bytes.fromhex(source['source_hex'])) + 1,
        })
    if len(records) != 164 or len({row['id'] for row in records}) != 164:
        raise ValueError('Complete unique caption scope required')
    return {'format': 'dk4-scene-caption-manuscript-v2',
            'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
            'status': 'source-localized-native-formatting-pending',
            'source_arm9_sha256': inventory['clean_arm9_sha256'],
            'logical_caption_count': 164, 'records': records,
            'integration_blockers': ['Complete source-pool/padding and all pointer owners must be mapped.',
                                     'Native raster/fullscreen/layout review and strict release components pending.',
                                     'Separate COMMON consumers are unresolved; no COMMON integration approval.']}


def main():
    path = Path('work/analysis/common_scene_caption_duplicates_v137.json')
    document = compile_manuscript(json.loads(path.read_text(encoding='utf-8')))
    document['source_inventory'] = {'path': path.as_posix(), 'sha256': sha(path.read_bytes())}
    output = Path('translations/scene_caption_manuscript_v2.json')
    output.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"All 164 captions localized; longest {max(row['native_centering_width_pixels'] for row in document['records'])} pixels before layout; source-pool/raster approval pending.")


if __name__ == '__main__':
    main()
