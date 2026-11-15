"""Review the full Online copy and verify the separate current DS display owners."""

from collections import Counter
from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from PIL import ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import observe_online_promotional_current_20261115 as replay
from scripts import register_about_extras_20261114 as extras
from scripts import register_visible_online_captions_v1 as guide
from scripts.checkpoint_online_gallery_current_20261114 import GUIDE_COPY_GROUPS, ONLINE
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.review_visible_online_captions_v1 import BASE, COLOR, DESCRIPTORS, complete_mask
from scripts.seal_shared_text_source_v1 import reference
from scripts.stage_extras_tie_in_20261114 import check_page
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_release_baseline import files


current = replay.current
base, stage = current.base, current.stage
OLD = Path('translations/common_online_promotional_manuscript_v2.json')
OUTPUT = Path('translations/common_online_promotional_manuscript_v3.json')
PREVIOUS_OWNER_MAP = Path('translations/editorial_checkpoints/SharedText_20261110_v1/'
                          'online_gallery_owner_reconciliation_20261114_v2.json')
DOC = Path('docs/editorial_online_promotional_current_20261115.md')
NUMBERS = range(3289, 3320)
GATES = ('source', 'context', 'localization', 'naturalness', 'formatting')
REVISIONS = {
    3289: 'Set Your Course for a World Beyond the Map',
    3290: ('Take command of your own sailing ship and set out across a boundless ocean.\n\n'
           'Form a fleet with other sailors you meet online. Unravel mysteries tied to hidden ancient arts, '
           'fight tense battles against pirate fleets, and keep sailing toward a new world of adventure.'),
    3291: 'Many Lives, Many Stories',
    3292: ('Uncharted Waters Online is a seafaring adventure RPG set in the Age of Discovery, which swept through Europe '
           'in the early 1500s. Step into the role of an adventurer, a merchant, or a soldier and make your own stories '
           'with the people who share your world.'),
    3293: 'Many Lives, Many Stories',
    3294: ('The online world spans Portugal, Spain, England, and more. Choose a homeland when you create your character.\n\n'
           'Start your seafaring life as an adventurer, merchant, or soldier in a bustling home port such as Lisbon, Seville, or London.'),
    3296: ('Explore the ports and goods near your homeland first. Once you know the local waters, trade goods and hunt pirates '
           'to hone your seamanship. In time, you can command faster, larger, and sturdier ships. '
           'Work with other players on guild assignments to build your reputation, or invest to bring more ports '
           'into your nation\'s alliance. How you make your way at sea is up to you.'),
    3298: ('Orders from the king open new waters and send you on new adventures.\n\n'
           'In foreign towns you can find rare clothing and goods, and deep inland, great ruins hold hidden treasures. '
           'Storms can stop your fleet in its tracks, and in dangerous waters you can become a privateer yourself. '
           'A life at sea is full of thrills and sights to see.'),
    3299: 'Live Your Own Way at Sea!',
    3300: ('Choose from 50 or more professions across three fields: adventure, trade, and combat. Once you have some experience '
           'at sea, visit the guild for your chosen field to change professions. A change of profession can make a big '
           'difference to which skills you learn and how your character develops.'),
    3301: 'Sail Far and Make Your Name as an Explorer!',
    3302: ('Towering ruins, legendary treasures, unfamiliar creatures, and wonders of nature await. This vast 3D world holds '
           'countless mysteries. Team up with other adventurers and set out to make great discoveries.'),
    3303: 'Trade All Kinds of Goods and Turn a Profit!',
    3304: ('There are hundreds of goods to buy and sell. The deals merchants make keep prices moving and shape the economy.\n\n'
           'Invest in towns around the world to bring them into your homeland\'s alliance. You may earn better terms '
           'and find new local specialties for sale.'),
    3306: ('Pirates lurk in the waters outside port. As a soldier, you can earn a name for yourself by escorting '
           'adventurers and merchants and defeating pirates. You and other players can even form a pirate fleet. '
           'Cannon fire and hand-to-hand fighting make fleet battles a highlight of the Age of Discovery.'),
    3308: ('Set out from one of the nations of Europe. Complete guild assignments and report your discoveries to build '
           'your reputation as a seafarer. The king can then issue orders allowing you to sail in new waters. '
           'You\'ll meet all kinds of characters in your travels, and their stories unfold according to what\'s happening in your nation.'),
    3309: 'A Changing World Brings New Adventures!',
    3311: 'Set Sail with Companions You Meet in Town!',
    3312: ('Pick up a voyage assignment from a guild and invite other players to form a fleet. Ask around in towns '
           'and use your companions\' skills, such as cartography and archaeology, to unravel mysteries and make great discoveries. '
           'A shared sunset at sea or a good talk in a tavern is its own reward along the way.'),
    3315: 'Explore the World as It Was in the Age of Discovery!',
    3316: ('The sea comes to life in all its grandeur and beauty, changing with the region and time of day. '
           'In port, you\'ll see landmarks like the Leaning Tower of Pisa '
           'and the Parthenon. Head inland through a city gate or from a landing site. Sail up the Nile, excavate pyramids, '
           'and see how far your adventures take you.'),
    3317: 'About the Online Tie-In',
    3319: ('Join the Windows edition of Uncharted Waters Online and complete a quest to receive a village name and its '
           'Promised Words.\n\nSail to that village in Uncharted Waters IV: Rota Nova and enter the Promised Words. '
           'You can then trade for new goods in the village.'),
}
NOTES = {
    3289: 'The nautical invitation keeps the map imagery and the promise of finding a world beyond it.',
    3290: 'Keep command of your own ship, forming a fleet online, the hidden ancient arts and the pirate fleet battles. The blank line follows the source’s shift from setting sail to playing together.',
    3291: 'Use the same approved English heading as the independent guide caption and the identical COMMON heading at 3293.',
    3292: 'Name the game and period, then address the reader directly. Preserve the early 1500s, Europe, all three roles and the stories players create together.',
    3293: 'The source repeats the heading at 3291 verbatim before explaining where players start. Use the same English both times.',
    3294: 'Use the game’s place names and make homeland selection part of character creation. Start the second paragraph at the switch to life in the home ports.',
    3295: 'Keep the direct invitation about how to live. This is the heading for the independent career and port-development choices.',
    3296: 'Preserve the order from exploration to practicing seamanship and handling better ships. Guild assignments build reputation, and investments can add allied ports.',
    3297: 'Keep the king’s authority and the promise of further adventures. The next paragraph describes the actual ways that access expands.',
    3298: 'Keep the king’s orders, foreign goods, inland ruins and their treasure, storms and the chance to become a privateer. The source starts a second paragraph for the examples.',
    3299: 'Make freedom at sea the invitation. The next paragraph describes the careers that let players choose how to live.',
    3300: 'Keep the inclusive quantity and all three fields. Preserve the experience prerequisite, guild change, and effects on skills and development.',
    3301: 'Make the invitation direct and keep renown as an explorer as its aim.',
    3302: 'Keep the huge ruins, treasures, unfamiliar life and natural wonders, as well as the 3D world and cooperation on discoveries.',
    3303: 'Keep the variety of goods in a direct market pitch. Turn a profit preserves the modest claim about making money while trading.',
    3304: 'Keep the large variety of goods and how merchants shape prices, then distinguish the benefits of investment in the second paragraph.',
    3305: 'Keep the energetic announcement about naval battles. The next paragraph supplies the specific actions.',
    3306: 'Keep escorts, pirate defeats, fame, forming a pirate fleet with other players, and both cannon fire and hand-to-hand combat.',
    3307: 'Keep the caption’s direct claim that the nation a player belongs to shapes the story.',
    3308: 'Keep the European starting points, guild work and discovery reports, reputation, royal permission, and events shaped by the player’s nation.',
    3309: 'Keep the relationship between world changes and the new adventures they produce.',
    3310: 'Retain the distinct effects of each player’s actions, royal orders, and player trade. Allied ports and shifting prices are concrete examples.',
    3311: 'Invite the reader to set sail with people met in town. The following paragraph gives the example of finding a guild assignment together.',
    3312: 'Keep the voyage assignment and the other players’ skills, along with the quieter pleasures of sunset at sea and talking in taverns.',
    3313: 'Retain the focus on sailing in a ship that the player makes their own.',
    3314: 'Retain the separate ship and character customization examples, including sail count, emblems, body type, clothing, hats, and the hundreds of equipment choices.',
    3315: 'Name the period already established in this guide and keep the promise of exploring its world as it was.',
    3316: 'Keep the beauty and variety of the sea, both landmarks and inland entry routes, and the Nile and pyramid examples.',
    3317: 'Keep the tie-in heading. The next paragraph identifies both games and the Windows edition.',
    3318: 'Retain the full game names, Windows edition, and the original promotional description of how the tie-in adds to Rota Nova.',
    3319: 'Use the village menu’s Promised Words terminology. Preserve the quest, the paired name and password, and the goods made available in Rota Nova. The visible DS panels give their own instructions.',
}


def replay_evidence(case, sha, evidence):
    folder = replay.ROOT / case
    report_path, trace_path, receipt_path = (folder / p for p in ('capture/capture_report.json', 'requests.json', 'terminal.json'))
    report, trace, receipt = map(base.load, (report_path, trace_path, receipt_path))
    assert report['ROM_sha256'] == receipt['ROM_sha256'] == sha
    assert report['frames'] == receipt['completed_frames'] and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and report.get('battery_save_preloaded') is None
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    assert trace['all_host_slots_restored_and_core_file_exact'] and not trace['errors'] and not trace['mismatches']
    assert receipt['COMMON_requests'] == len(trace['source_requests']) == 0 and not receipt['target_COMMON_calls']
    assert all(base.digest(p) == h for p, h in receipt['evidence'].items())
    evidence.update({str(p): base.digest(p) for p in (report_path, trace_path, receipt_path)})
    return report, receipt


def guide_pages(clean, arm, rom, previous, sha, evidence):
    report, receipt = replay_evidence('online', sha, evidence)
    proof = base.load(ONLINE)
    calls = {row['pointer']: row for row in receipt['caption_calls']}
    assert len(calls) == len(receipt['caption_calls']) == 13
    font, boxes = GameAsciiFont.from_arm9(arm), shots(report)
    pages = []
    for row, group in zip(proof['records'], GUIDE_COPY_GROUPS, strict=True):
        ref = row['registered_reference']
        category, page = row['original_category'], row['original_page']
        descriptor = DESCRIPTORS[category]
        _, table, count = unpack_from('<3I', clean, descriptor)
        assert page < count and clean[descriptor:descriptor + 12] == arm[descriptor:descriptor + 12]
        offset, pointer = ref['offset'], ref['pointer']
        field = table - BASE + page * 4
        assert unpack_from('<I', arm, field)[0] == unpack_from('<I', clean, field)[0] == pointer
        assert clean[offset:].split(b'\0', 1)[0].decode('cp932') == row['source_Japanese']
        body = bytes.fromhex(ref['stored_hex'])
        assert arm[offset:offset + len(body)] == previous[stage.ARM][offset:offset + len(body)] == body
        page_art = row['background']
        assert rom[page_art] == previous[page_art] and all(row['review'].values())
        call = calls[pointer]
        x = 128 - 3 * len(row['english'])
        assert call['PC'] == replay.playback.ONLINE and call['x'] == x and call['text'] == row['english']
        hold = boxes[row['actual_gameplay']['frame']]
        assert hold['frame'] > call['frame']
        ink, bounds = complete_mask(font, row['english'], captured(hold), x, 205, COLOR)
        assert ink == row['actual_gameplay']['complete_ink'] and list(bounds) == row['actual_gameplay']['bounds']
        evidence[hold['path']] = hold['PNG_sha256']
        pages.append(dict(id=row['id'], category=category, page=page, COMMON_IDs=list(group), pointer=pointer,
            ARM9_field=field, clean_Japanese=row['source_Japanese'], English=row['english'], glyph_pixels=ink,
            bounds=bounds, frame=hold['frame'], source_artwork=page_art, same_artwork_sha256=sha256(rom[page_art]).hexdigest()))
    assert len(pages) == 13
    return pages


def extras_pages(clean, arm, sha, evidence):
    report, receipt = replay_evidence('tie_in_advance', sha, evidence)
    assert not receipt['caption_calls']
    proof, boxes = base.load(extras.REVIEW), shots(report)
    font = GameAsciiFont.from_arm9(arm)
    pages = []
    for row in proof['records']:
        ref = row['registered_reference']
        offset, field = ref['ARM9_offset'], ref['pointer_field']
        data = bytes.fromhex(ref['exact_stored_hex'])
        japanese = bytes.fromhex(row['source_hex'])
        source_offset = row['current_reference']['ARM9_offset']
        assert clean[source_offset:source_offset + len(japanese)] == japanese
        assert unpack_from('<I', clean, field)[0] == BASE + source_offset
        assert arm[offset:offset + len(data)] == data and unpack_from('<I', arm, field)[0] == BASE + offset
        assert all(row['review'].values())
        hold = boxes[row['candidate_page']['frame']]
        counts = check_page(captured(hold), font, row['lines'])
        assert counts == row['candidate_glyph_counts']
        evidence[hold['path']] = hold['PNG_sha256']
        pages.append(dict(id=row['id'], page=row['full_sequence_order'], pointer=BASE + offset, ARM9_field=field,
            clean_ARM9_offset=source_offset, clean_Japanese=row['source_Japanese'], English_lines=row['lines'],
            complete_row_pixels=counts, frame=hold['frame']))
    assert len(pages) == 6
    folder = extras.stage.ROOT / 'capture'
    old_report = folder / 'capture_report.json'
    old_boxes = shots(base.load(old_report))
    for n in proof['exact_navigation_control_frames']:
        a, b = old_boxes[n], boxes[n]
        assert ImageChops.difference(captured(a), captured(b)).getbbox() is None
        evidence.update({p['path']: p['PNG_sha256'] for p in (a, b)})
    evidence[str(old_report)] = base.digest(old_report)
    return pages


def main():
    assert not OUTPUT.exists() and not DOC.exists()
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release['candidate_sha256']
    assert base.digest(stage.CLEAN) == release['clean_input_sha256']
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    rom = files(base.NdsImage.open(current.ROM))
    clean_rom = base.NdsImage.open(stage.CLEAN)
    arm, clean = rom[stage.ARM], clean_rom.read_file(stage.ARM)
    assert sha256(arm).hexdigest() == release['target_ARM9_sha256']
    assert sha256(rom[stage.COMMON]).hexdigest() == release['target_COMMON_sha256']
    original = common_message_entries(clean_rom.read_file(stage.COMMON), clean)
    stored = owned_entries(rom[stage.COMMON], arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    historical = files(base.NdsImage.open(guide.ROM))
    old = base.load(OLD)
    earlier = {r['message_ID']: r for r in base.load(PREVIOUS_OWNER_MAP)['maps']}
    before_ledger = base.LEDGER.read_bytes()
    ledger = base.load(base.LEDGER)
    pending = ledger['pending_shared_consumer_checkpoint_20261114']
    assert pending['candidate_sha256'] == release['candidate_sha256'] and pending['remaining_total'] == 276
    assert ledger['records_editorially_completed'] == 27700 and not ledger['full_goal_complete']
    credited = {r['id'] for r in ledger[base.CONTEXT]['integrated_record_keys'] if r['file_path'] == stage.COMMON}
    evidence = {str(p): base.digest(p) for p in (OLD, PREVIOUS_OWNER_MAP, ONLINE, extras.REVIEW,
        current.RELEASE, Path(__file__), Path(replay.__file__))}
    online = guide_pages(clean, arm, rom, historical, release['candidate_sha256'], evidence)
    tie_in = extras_pages(clean, arm, release['candidate_sha256'], evidence)
    owners = {n: [row['id']] for row in online for n in row['COMMON_IDs']}
    owners.update({3317: [tie_in[0]['id']], 3318: [tie_in[0]['id']], 3319: [row['id'] for row in tie_in[1:4]]})
    assert set(owners) == set(NOTES) == set(NUMBERS)
    rows = []
    for prior, n in zip(old['records'], NUMBERS, strict=True):
        a, b = original[n], stored[n]
        assert n == prior['message_id'] == a.message_id == b.message_id
        assert prior['id'] not in credited
        assert a.text == b.text == bytes.fromhex(prior['source_hex']) == bytes.fromhex(earlier[n]['stored_hex'])
        assert prior['japanese'] == a.text.decode('cp932')
        previous = prior['english'].removesuffix('{PAD}')
        text = REVISIONS.get(n, previous)
        assert text.isascii() and not any(c in text for c in ('\r', '{', '}', '%'))
        assert all(' '.join(paragraph.split()) == paragraph and paragraph for paragraph in text.split('\n\n'))
        rows.append(dict(id=prior['id'], message_ID=n, file_path=stage.COMMON, clean_reference=reference(a),
            current_reference=reference(b), clean_hex=a.text.hex(), current_hex=b.text.hex(),
            clean_Japanese=prior['japanese'], current_text=b.text.decode('cp932'), previous_draft_English=previous,
            english=text, source_meaning=prior['source_meaning'] if n != 3300 else
                'At least fifty professions fall into adventure, trade and combat. Experience permits a guild career change that affects skills and development.',
            context='Original Online promotional copy.' if n < 3317 else 'Original Windows tie-in copy.',
            localization_note=NOTES[n], decision='revision' if n in REVISIONS else 'retention',
            independently_displayed_related_ARM9_owners=owners[n], COMMON_display_status='other_paths_unresolved',
            review=dict.fromkeys(GATES, True) | {'formatting': False}))
    assert rows[3291 - 3289]['english'] == rows[3293 - 3289]['english']
    counts = Counter(row['decision'] for row in rows)
    base.save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='pending_consumer',
        review_gates=list(GATES), status='clean_source_reviewed_with_no_current_COMMON_render_on_the_tested_menus',
        candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        records=rows, revisions=counts['revision'], justified_draft_retentions=counts['retention'],
        actual_independent_guide_pages=online, actual_independent_about_extras_pages=tie_in,
        actual_tested_paths_COMMON_requests=0, global_COMMON_non_use_verified=False,
        artwork_separate=True, hardware=False, new_dialogue_credit=0, evidence=evidence))
    ledger['online_promotional_current_20261115'] = dict(review=str(OUTPUT), candidate_sha256=release['candidate_sha256'],
        source_reviewed_drafts=len(rows), wording_refinements=counts['revision'], justified_draft_retentions=counts['retention'],
        current_verified_ARM9_guide_pages=13, current_verified_ARM9_extras_pages=6, unresolved_COMMON_display_owners=len(rows),
        new_dialogue_credit=0)
    line = 'The 31 Online and tie-in COMMON drafts have current source comparisons, and all 19 visible guide and About Extras pages are verified.'
    ledger['latest_checkpoint'] = line
    assert base.LEDGER.read_bytes() == before_ledger
    base.replace_checked(base.LEDGER, encode_ledger(ledger))
    doc = f"""# Online promotional text and the Windows tie-in

The [review ledger](../{OUTPUT.as_posix()}) compares 31 full Japanese COMMON records with their exact bytes in the Square Rumors candidate. All 31 received a contextual prose review. {counts['revision']} drafts were revised and {counts['retention']} retained with individual reasons. The full copy keeps the guide’s examples and the original tie-in’s quest, village name, Promised Words, and new trade goods.

Two ordinary cold boots visited all 13 Online guide pages and all six About Extras panels. The native Online caption pointers and the six independent About Extras strings matched the registered English, and all 19 panels passed complete glyph checks. Both tested menu paths made zero COMMON requests. The visible About Extras steps describe learning the village name and Promised Words from a character. The older COMMON copy explicitly says to complete a quest.

The 31 records still need a display owner before formatting or ROM insertion. The ledger remains at 27,700 credited reviews and 276 pending shared records. Raster artwork stays in the separate graphics audit. Hardware was outside this replay.
"""
    base.replace_checked(DOC, doc.encode())
    prefix = f"# Current editorial checkpoint - 2026-11-15\n\n{line} [Checkpoint]({DOC.name})\n\n".encode()
    for name in ('editorial_handoff_current.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, prefix + path.read_bytes())
    print(f'{len(rows)} source reviews, {counts["revision"]} draft revisions, and 19 visible page checks. No duplicate credit.')


if __name__ == '__main__':
    main()
