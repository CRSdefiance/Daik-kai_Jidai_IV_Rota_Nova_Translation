"""Review complete town trend scenes on all four routes in their original records."""

from pathlib import Path
from types import FunctionType

from scripts import register_trade_and_armed_ship_labels_20261115 as parent
from scripts import stage_rafael_early_wraps_20261111 as layout
from scripts.checkpoint_story_glyph_consistency_20261115 import catalogue
from scripts.stage_embedded_story_roles_20261115 import (
    ARM, CLEAN, GATES, IlnkContainer, RegisteredRuntime, digest, files,
    raw_speeches, references, scoped_inventory,
)
from scripts.stage_kurushima_encounter_20261115 import visible_lines


base = parent.base
BLOCK_MAP = {151: (190, 182, 178, 151), 153: (192, 184, 180, 153), 154: (193, 185, 181, 154),
             155: (194, 186, 182, 155), 159: (198, 190, 186, 159), 166: (205, 197, 193, 166)}
ROOT = Path('work/town_trend_exchanges_20261115_v2')
ROM = ROOT / 'Town_Trend_Exchanges_RESEARCH_ONLY.nds'
STORED = ROOT / 'staged.json'
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/town_trend_exchanges_20261115_v2.json')
PREVIOUS = MANUSCRIPT.with_name('special_town_and_story_nameplates_reviewed_20261114.json')
ALEXANDRIA = Path('releases/all_routes_editorial_20261114_alexandria_cooking_candidate/verification/registered_review.json')
SPEAKERS = {166: 'Lady', 167: 'Lady', 168: 'Lady', 174: 'Owner', 175: 'Cook', 254: 'System notice'}
CONTEXT = {
    151: 'In Amsterdam, three women compare homemade bread with the bakery’s. One offers to teach another, and they decide to shop for wheat.',
    153: 'In Lisbon, two women admire a fragrance and agree to ask its wearer before it becomes fashionable.',
    154: 'In Athens, three women admire a lady’s ruby necklace. They wish for a gift like it and sigh in turn.',
    155: 'In London, two women gossip about the princess’s engagement. They want to identify the ring’s gem before it becomes fashionable.',
    159: 'In Alexandria, the owner insists that customers want sweeter food. The cook asks how to sweeten it. The owner leaves the answer to the cook and keeps insisting on the trend.',
    166: 'In Seoul, three friends enjoy a meal. One explains that chili peppers give it a kick, and offers to show the others how to use them.',
}
# The notes follow the original turn order and include the trend notice after each exchange.
MEANINGS = {
    151: {
        6: 'She declares that bread baked at home is best. Keep her wholehearted preference.',
        9: 'She agrees and says her husband was delighted. Keep the explicitly stated relationship and reaction.',
        12: 'She asks whether bread is really that delicious when you bake it yourself. Let the preceding turn establish what “it” means.',
        16: 'She enthusiastically agrees and invites her companion to agree. Keep the quick affirmation before the second woman backs her up.',
        20: 'She says the bakery on the corner cannot compare. Keep the familiar local point of comparison.',
        23: 'She is surprised and considers baking bread herself. Keep the tentative decision to try it.',
        27: 'She encourages her to do it. Keep the quick, friendly nudge.',
        31: 'She offers to teach her. Keep the simple offer and let the other woman respond.',
        35: 'She is delighted by the offer. Keep the two beats of surprise and pleasure.',
        39: 'She proposes buying ingredients immediately. Keep the practical next step and the shared invitation.',
        42: 'She asks what they need. Keep the short question without supplying ingredients of our own.',
        46: 'She names wheat as the first ingredient. Wheat is the source commodity and the forecast that follows.',
        50: 'The notice forecasts a trend for wheat in Amsterdam. Keep the tentative forecast and the game’s commodity name.',
    },
    153: {
        4: 'She wonders if her companion noticed how lovely the fragrance was. The question leaves the wearer’s identity to the exchange.',
        8: 'She is pleased that her companion noticed it too. Keep the shared recognition.',
        12: 'She wonders what the fragrance was. Keep the direct question.',
        16: 'She does not know the fragrance but is sure it will catch on. Use a complete sentence that flows into the prediction.',
        19: 'She is alarmed at the prospect and wants to obtain it first. Keep her elegant urgency and competitive impulse.',
        23: 'She agrees with the urgency. Keep the brief, polite assent.',
        27: 'She suggests being bold enough to ask the wearer when they next meet. Keep both the hesitation and timing.',
        30: 'She approves the plan and agrees to do it. Keep the cheerful two-beat answer.',
        33: 'She takes her leave politely. Keep a distinct farewell from her companion’s reply.',
        37: 'She returns the farewell. Keep the succinct response.',
        72: 'The notice forecasts a trend for scents in Lisbon. Keep the established name for the trade good.',
    },
    154: {
        5: 'She asks if the others saw the vividly red ruby. Keep her eager attention to its color.',
        8: 'She answers that it was magnificent. Keep the clipped admiration.',
        12: 'The third woman asks what they mean. Keep her polite interruption as the conversation opens to her.',
        16: 'She identifies the necklace the lady was wearing. Keep the reference to an unnamed woman and her necklace.',
        19: 'The third woman remembers the big, beautiful stone. Keep her recognition and both qualities.',
        22: 'She wishes a gentleman would give her such a gift just once in her life. Keep the existing longing and wrap the comparison together.',
        26: 'She agrees and sighs. Keep the sigh as the first in a three-part comic chorus.',
        30: 'She sighs too. Keep the silent reaction as a short printed sound cue.',
        34: 'She joins the other two with a sigh. Keep the matching third beat.',
        38: 'The notice forecasts a ruby trend in Athens. Keep the gem, town, and tentative outcome.',
    },
    155: {
        4: 'She asks if her companion heard that the princess is getting engaged. Keep the excited opening and the complete announcement.',
        7: 'She has heard and asks whether the match is the duke’s son. Give her a natural confirmation tag.',
        10: 'She reports the ring supposedly costs enough to buy a whole mountain. Keep the hearsay and comic scale.',
        13: 'She admires what she expects of a duke and wonders when they can see the princess wearing the jewel. Keep the social admiration and anticipation.',
        16: 'She expects it before long and predicts other ladies will want the jewel. Keep the time, prediction, and qualified number of people.',
        20: 'She says it will be too late once the jewel is fashionable and asks which gem it is. Keep the rush and direct question.',
        24: 'She does not know and says they should ask immediately. Keep the moment of decision.',
        61: 'The notice forecasts a trend for gems in London. Keep the broad category because the characters have not identified the gem.',
    },
    159: {
        4: 'The owner thinks something is missing, then decides the food needs sweetness. Keep the sudden discovery and the practical conclusion.',
        8: 'The cook echoes the word in surprise. Keep the single questioning beat.',
        12: 'The owner says the mild flavor will not satisfy customers and insists twice on sweetness. Keep the comic escalation and repeated word.',
        15: 'The cook expresses polite doubt. Keep the short question before the owner cuts in.',
        19: 'The owner claims she must be right because she is the one saying it. Give the joke two blunt beats in her own voice.',
        22: 'The cook asks how to make the food sweeter. Keep the practical reply rather than adding an ingredient.',
        25: 'The owner says figuring it out is the cook’s job. Keep the curt handoff in the context of the preceding question.',
        28: 'The cook reluctantly acknowledges the instruction. Keep the hesitation and flat reply.',
        32: 'The owner returns to her certainty that sweets will catch on. Keep the assertion and its pivot away from the cook’s concern.',
        35: 'The cook gives another flat acknowledgment. Keep the echo of the earlier reply.',
        39: 'The owner insists again on sweet food, urges the cook to try, and laughs. Keep the written laugh and contrast her enthusiasm with the cook’s replies.',
        62: 'The notice forecasts a trend for sweets in Alexandria. Keep the link to the discussion and the established market wording.',
    },
    166: {
        5: 'She savors the delicious meal and says it is unlike any she has had. Keep her delighted pause and sense of discovery.',
        9: 'She agrees and says the flavors had a stimulating edge. “Had a kick” points naturally toward the chili without claiming she knows the ingredient.',
        13: 'She asks how such delicious food is made. Keep the practical question and put it on one line.',
        16: 'She chuckles and reveals she has a secret. Keep the playful lead-in to the ingredient.',
        20: 'She gives a puzzled reaction before the ingredient is named. Keep the original brief punctuation beat.',
        24: 'She names chili peppers, says she has heard they are a spice, and finds they suit local ingredients. Keep the reported classification and the local flavor pairing together.',
        28: 'She asks whether the peppers are expensive. Keep her polite concern about the price.',
        32: 'She says they are not especially expensive. Keep the light qualification.',
        36: 'She is relieved and considers using the peppers for dinner that evening. Keep the tentative response, ingredient reference and timing together.',
        39: 'She wants to make it as well. Keep the brief echo of the other woman’s interest.',
        43: 'She offers to teach them immediately. Keep the hospitable offer and timing.',
        46: 'She reacts with delighted surprise. Keep the short exclamation.',
        50: 'She says the offer is kind. Keep the brief thanks implicit in the compliment.',
        54: 'She says it is only natural because they are friends. Keep the explicitly stated friendship and gracious answer.',
        58: 'The notice forecasts a trend for chili peppers in Seoul. Keep the ingredient and the city.',
    },
}
# A None value keeps the words while revisiting their automatic wrapping.
REVISIONS = {
    (151, 12): ('Is it that good?', ()),
    (151, 23): ("Really? Maybe I'll bake some.", ()),
    (153, 16): ("I don't know, but it'll catch on.", ()),
    (154, 22): (None, ('a gentleman', 'something like that')),
    (155, 4): (None, ('The princess is getting engaged!',)),
    (155, 7): ("Yes, to the duke's son, right?", ()),
    (155, 10): (None, ('costs enough to buy', 'an entire mountain.')),
    (155, 13): ("As you'd expect from a duke. I wonder when we'll see the princess wearing that jewel.",
                 ("As you'd expect from a duke.", 'the princess', 'wearing that jewel.')),
    (155, 16): ("Before long, I'm sure. Once she wears it, more ladies will want one.", ('Once she wears it,', 'more ladies will want one.')),
    (155, 20): ("Once it catches on, it's too late! Do you know which gem?", ('Do you know which gem?',)),
    (159, 12): ("Yes! Our customers won't settle for a flavor this mild. It has to be sweeet! Sweet!",
                ("Our customers won't settle", 'for a flavor this mild.', 'It has to be sweeet! Sweet!')),
    (159, 32): ('Anyway, sweets will catch on!', ()),
    (166, 5): ("Oh, that was delicious... I've never had a meal like it.", ("I've never had a meal like it.",)),
    (166, 9): ('It certainly had a kick.', ()),
    (166, 13): ('How do you get it to taste so good?', ()),
    (166, 24): ("They're called chili peppers, a kind of spice, I'm told. They go beautifully with local ingredients.",
                 ('chili peppers', "a kind of spice, I'm told.", 'They go beautifully', 'with local ingredients.')),
    (166, 36): ("Oh, that's a relief. I may use some for dinner tonight.", ("I may use some for dinner tonight.",)),
}

OTHER_ROUTES = {
    (0, 151, 20): ("Absolutely. The corner bakery can't touch it.", ("can't touch it.",)),
    (0, 151, 23): REVISIONS[151, 23],
    (1, 151, 12): REVISIONS[151, 12],
    (1, 151, 23): REVISIONS[151, 23],
    (1, 153, 16): REVISIONS[153, 16],
    (0, 154, 22): (None, ('a gentleman', 'something like that')),
    (1, 154, 22): (None, ('a gift like that.',)),
    (2, 154, 22): (None, ('something like that.',)),
    (0, 155, 4): (None, ('the princess is getting engaged.',)),
    (1, 155, 4): ('Did you hear? The princess is getting engaged!', ('The princess is getting engaged!',)),
    (2, 155, 4): (None, ('the princess is getting engaged!',)),
    (0, 155, 13): (None, ("we'll see the princess", 'wearing that jewel.')),
    (1, 155, 13): ("You'd expect as much from a duke. When will we see her wearing it?", ('When will we see her wearing it?',)),
    (2, 155, 13): ("That's the duke for you... When do you suppose we'll see the princess wearing that jewel?",
                   ("That's the duke for you...", "When do you suppose", 'the princess', 'wearing that jewel?')),
    (0, 155, 16): (None, ('Once they see it,', "I'm sure", 'a stone just like it.')),
    (1, 155, 16): ("It won't be long. Once she wears it, imagine how many ladies will want one!",
                   ('Once she wears it,', 'ladies will want one!')),
    (2, 155, 16): (None, ('many more ladies will want', 'that gemstone then.')),
    (0, 159, 32): REVISIONS[159, 32],
    (1, 166, 24): REVISIONS[166, 24],
    (2, 166, 24): REVISIONS[166, 24],
    (0, 166, 36): REVISIONS[166, 36],
    (1, 166, 36): ("What a relief. I may use some for dinner tonight.", ("I may use some for dinner tonight.",)),
    (2, 166, 36): ("Oh, that's a relief. Perhaps I'll cook with them tonight.", ("cook with them tonight.",)),
    (2, 166, 39): ("I'd like to try them, too.", ()),
    (1, 166, 43): ('Would you like me to show you now?', ()),
}
for route in range(3):
    OTHER_ROUTES[route, 155, 7] = REVISIONS[155, 7]
    OTHER_ROUTES[route, 155, 10] = (None, ('costs enough to buy',))
    OTHER_ROUTES[route, 155, 20] = (
        "Oh! Once it's in fashion, it'll be too late! Do you know which gem it is?", ('Do you know which gem it is?',))
    OTHER_ROUTES[route, 166, 5] = REVISIONS[166, 5]
    OTHER_ROUTES[route, 166, 9] = REVISIONS[166, 9]
for route in (0, 1):
    OTHER_ROUTES[route, 166, 13] = REVISIONS[166, 13]


def review_block(ja, old, source_arm, arm, inventory, route, group, block, evidence, alexandria):
    a, source = raw_speeches(source_arm, ja, inventory)
    b, current = raw_speeches(arm, old, inventory)
    assert [c['word'] for c in a] == [c['word'] for c in b]
    assert [r['raw_hex'] for r in source] == [r['raw_hex'] for r in evidence['clean_speeches']]
    if route == 3:
        assert digest(ja) == evidence['source_block_sha256']
        if group != 159:
            assert digest(old) == evidence['current_block_sha256']
    shared_indices = list(MEANINGS[group])
    rows = []
    for ordinal, (s, c) in enumerate(zip(references(a, source), references(b, current), strict=True)):
        selector, index = s['selector'], s['record_index']
        context_index = shared_indices[ordinal]
        assert s['complete_preamble_hex'] == c['complete_preamble_hex']
        j, e = (bytes.fromhex(x['raw_hex']) for x in (s, c))
        assert j[0] == e[0] == selector
        previous = ' '.join(e[1:].decode('ascii').split())
        change = REVISIONS.get((group, context_index)) if route == 3 else OTHER_ROUTES.get((route, group, context_index))
        revised, protected = change or (None, ())
        revision = change is not None
        english = revised if revised is not None else previous
        marker = f'{{SPEAKER:{selector:02X}}}' if selector != 254 else '{SYSTEM}'
        assert not any(token in raw for raw in (j[1:], e[1:], english.encode('ascii'))
                       for token in (b'FI', b'FA', b'FO', b'FU', b'%'))
        note = MEANINGS[group][context_index]
        row = dict(id=f'DK4_MES_B{block}_R{index:04d}', file_path=f'/data/SC{route}.DK4', block=block, route=route,
            group=group, ordinal=ordinal,
            kind='system-FE' if selector == 254 else 'progressive', source_selector=selector,
            speaker=SPEAKERS[selector], context=CONTEXT[group], Japanese=j[1:].decode('cp932'),
            previous_English=previous, source_meaning=note, localization_note=note,
            english=marker + english, decision='revision' if revision else 'retention',
            source_reference=s, current_reference=c, source_hex=s['raw_hex'], current_hex=c['raw_hex'],
            source_block_sha256=digest(ja), current_block_sha256=digest(old), review=dict.fromkeys(GATES, True))
        if group == 159:
            prior = alexandria[row['file_path'], row['id']]
            active_text = prior['english'].split('}', 1)[-1]
            assert ' '.join(active_text.split()) == previous, (route, index, active_text, previous)
            row['earlier_review'] = str(ALEXANDRIA)
        if revision:
            assert selector != 254
            norm = layout.prior.layout.norm
            pairs = [(norm(x), norm(y)) for phrase in protected for x, y in zip(phrase.split(), phrase.split()[1:])]
            try:
                compiled = layout.plan_record(row | {'protected_pairs': pairs})
            except (AssertionError, ValueError) as error:
                raise ValueError((route, group, index, len(e)-1, english)) from error
            assert compiled['expected_native_pages'] == 1
            assert all(any(phrase.casefold() in line.casefold() for line in compiled['lines']) for phrase in protected), (
                route, group, index, compiled['lines'], protected)
            if compiled['diagnostics']:
                assert all(d['code'] == 'line-break-count' and d['severity'] == 'warning' for d in compiled['diagnostics'])
                row.update(qa_waivers=['line-break-count'], qa_waiver_reason='Native English layout determines the row count.')
            encoded = bytes.fromhex(compiled['encoded_hex'])
            assert encoded[0] == selector and len(encoded) <= len(e) and b'\0' not in encoded
            row.update(target_hex=encoded.ljust(len(e), b' ').hex(), automatic_layout=compiled,
                       trailing_blank_bytes=len(e)-len(encoded))
            layout.fit_storage_padding(row)
            if row['target_hex'] == row['current_hex']:
                row['decision'] = 'retention'
        rows.append(row)
    return rows, b


def transform(image, records):
    return layout.prior.transform(image, [row for row in records if row['decision'] == 'revision'])


def native_previews(ctx, rows):
    updated = [r for r in rows if r['decision'] == 'revision']
    evidence = layout.native_validation(ctx, updated)
    pictures = []
    assert len(evidence) == 2 * len(updated)
    _, paint = layout.prior.precedent.planners(ctx.arm)
    font = ctx.image.read_file('/GRP/KANJI.FNT')
    for row in rows:
        revision = row['decision'] == 'revision'
        if revision:
            native, = row['after_native']['pages']
            authored = bytes.fromhex(row['automatic_layout']['encoded_hex'])[1:]
            ideal_page, = paint(ctx.arm, font, authored)['pages']
            assert native['native_plane_hex'] == ideal_page['native_plane_hex']
            assert visible_lines(native) == row['automatic_layout']['lines'], row['id']
            pictures.append((f"SC{row['route']} {row['id'].split('_B')[1]}", bytes.fromhex(native['native_plane_hex'])))
        if row['route'] == 3 and row['block'] == 159 and row['source_selector'] != 254 and not revision:
            retained = bytes.fromhex(row['current_hex'])[1:]
            page, = paint(ctx.arm, font, retained)['pages']
            row['retained_plane_hex'] = page['native_plane_hex']
    return pictures


def main():
    assert not ROOT.exists() and not MANUSCRIPT.exists()
    release, manifest = map(base.load, (parent.RELEASE, parent.MANIFEST))
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    ctx = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    clean, image = base.NdsImage.open(CLEAN), ctx.image
    before = files(image)
    banks = [IlnkContainer.parse(before[f'/data/SC{i}.DK4']).blocks for i in range(4)]
    originals = [IlnkContainer.parse(clean.read_file(f'/data/SC{i}.DK4')).blocks for i in range(4)]
    inventory, _, _ = scoped_inventory()
    previous = base.load(PREVIOUS)['complete_speech_exchanges']
    earlier = base.load(ALEXANDRIA)
    alexandria = {(row['file_path'], row['id']): row
                  for row in earlier['records'] + earlier['unchanged_leads']}
    assert len(alexandria) == 48
    config = manifest['relocations'][ARM]['reviewed_name_integration']['catalog']
    catalog_before = catalogue(ctx.arm, config, banks)
    updates, commands = [], {}
    clean_arm = clean.read_file(ARM)
    for group, numbers in BLOCK_MAP.items():
        for route, block in enumerate(numbers):
            rows, commands[route, block] = review_block(originals[route][block], banks[route][block], clean_arm,
                ctx.arm, inventory, route, group, block, previous[f'SC3_B{group}'], alexandria)
            updates.extend(rows)
    assert len(updates) == 276
    credited = {(x['file_path'], x['id']) for x in base.load(base.LEDGER)[base.CONTEXT]['integrated_record_keys']}
    assert all((row['file_path'], row['id']) in credited for row in updates)
    changed = dict(transform(image, updates))
    newbanks = [IlnkContainer.parse(changed[f'/data/SC{i}.DK4']).blocks for i in range(4)]
    assert catalogue(ctx.arm, config, newbanks) == catalog_before
    for (route, block), old_commands in commands.items():
        newbank = newbanks[route]
        parsed, texts = raw_speeches(ctx.arm, newbank[block], inventory)
        columns = ('offset', 'word', 'native_extent', 'ancestor_0100_offsets')
        assert all(all(a[k] == b[k] for k in columns) for a, b in zip(old_commands, parsed, strict=True))
        for row, target in zip((r for r in updates if (r['route'], r['block']) == (route, block)),
                               references(parsed, texts), strict=True):
            assert target['raw_hex'] == row.get('target_hex', row['current_hex'])
            assert target['complete_preamble_hex'] == row['current_reference']['complete_preamble_hex']
            row['staged_reference'] = target | {'block_sha256': digest(newbank[block])}
    pictures = native_previews(ctx, updates)
    for path, payload in changed.items():
        image.replace_file(path, payload)
    after = files(image)
    assert {name for name in before if before[name] != after[name]} == changed.keys()
    ROOT.mkdir(parents=True)
    image.save(ROM)
    for path in changed:
        image.replace_file(path, before[path])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    candidate = base.digest(ROM)
    sheets = FunctionType(layout.contact_sheets.__code__, vars(layout) | {'ROOT': ROOT})(pictures)
    base.save(MANUSCRIPT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=list(GATES), candidate_sha256=candidate,
        previous_sha256=release['candidate_sha256'], records=updates))
    base.save(STORED, dict(candidate_sha256=candidate, previous_sha256=release['candidate_sha256'],
        target_ARM9_sha256=digest(ctx.arm), target_story_archive_sha256={p: digest(x) for p, x in changed.items()},
        whole_parent_inverse=True,
        sheets=sheets, preview_count=len(pictures), manuscript_sha256=base.digest(MANUSCRIPT)))
    print(f'Staged {len(pictures)} revisions and {len(updates)-len(pictures)} retentions across 24 town-scene copies.')


if __name__ == '__main__':
    main()
