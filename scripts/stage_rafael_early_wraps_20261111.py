"""Review wrap leads in Rafael's early exchanges and compile fixed-extent revisions."""

from collections import defaultdict
from inspect import getsource
from pathlib import Path

from PIL import Image, ImageDraw

from scripts import register_story_question_wraps_20261111 as parent
from scripts import stage_historical_story_wraps_20261111 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, sha, IlnkContainer = prior.base, prior.sha, prior.IlnkContainer
CLEAN, ARM = prior.CLEAN, prior.ARM
FILE = '/data/SC0.DK4'
ROOT = Path('work/rafael_early_wraps_20261111_v2')
REVIEW = parent.storage.TRIAGE.with_name('rafael_early_wraps_context_v2.json')
PROOF = ROOT / 'stored_and_native.json'
DECISIONS = {
    (0,42,26): ('Rafael', 'At last they are about to set sail. Rafael wonders what they should do afterward.',
        'Keep the excitement followed by a practical question. Claudio immediately needles him for getting ahead of himself.',
        "We're finally setting sail! So... what do we do once we're out there?",
        ("We're finally setting sail!", 'what do we do', "once we're out there?")),
    (0,42,36): ('Claudio', 'Claudio protests that Janus makes him sound as if he never thinks.',
        'The exaggerated “never” restores the joke that Janus then extends by asking for Claudio’s brilliant plan.',
        'What?! You think I never think?!', ('I never think?!',)),
    (0,44,25): ('Claudio', 'Claudio names Prince Henry and Duke Leon as his exciting examples of men of the sea.',
        'Keep his incredulity and unabashed admiration. Both names and the short exclamation should read as units.',
        None, ('Prince Henry', 'Duke Leon', "they're really cool!")),
    (0,44,110): ('Claudio', 'Claudio remarks that Rafael turned out to be the most enthusiastic of them.',
        'Keep Claudio’s amused reaction to Rafael taking off to ask Julio for money. Janus replies that Rafael is taking after Claudio.',
        "Would you look at that... He's more excited than we are!", ("He's more excited than we are!",)),
    (0,44,160): ('Claudio', 'Claudio insists this time is different and they are serious. He calls Julio stingy for refusing a loan.',
        '“Quit being stingy” is Claudio’s familiar jab. The Japanese gives him no claim that Julio hoards his money.',
        "This time's different. We're serious! Quit being stingy and lend us the money!",
        ("This time's different.", "We're serious!", 'being stingy', 'lend us the money!')),
    (0,48,189): ('Claudio', 'Claudio admires Hans for braving dangerous seas at his age to carry his research through.',
        'Retain the surprising burst of sincere respect after Claudio’s earlier objections. Keep the exclamation together.',
        "At his age, he's risking his neck at sea to finish his research. That's dedication! I respect that!",
        ("At his age, he's risking his neck", 'at sea to finish his research.', "That's dedication!")),
    (0,48,221): ('Arcadius', 'Arcadius gives a full name and offers a polite greeting at Hans’s request.',
        'The hesitant introduction and formal greeting fit Arcadius’s first appearance. Keep both clauses intact.',
        None, ("I'm Arcadius Eudoxios.", "It's a pleasure to meet you.")),
    (0,48,324): ('Julio', 'Julio confirms he knows Hans and says Hans has been studying the Proof of Conquest for years.',
        'The plainspoken reply suits Julio’s reunion with Hans. “I know him” preserves the acquaintance without implying a closer relationship.',
        "Yes. I know him. He's studied the Proof for years.", ("He's studied the Proof", 'for years.')),
    (0,48,354): ('Rafael', 'Rafael starts to ask what would happen if the group collected the seven treasures itself.',
        'Keep the unfinished thought and the emphasis on doing it themselves. Julio takes up the thought in the next turn.',
        'If we collected them ourselves...!', ('collected them ourselves...!',)),
    (0,49,367): ('Camille', 'Camille calls after Lil, stammers an apology for the commotion, then calls after her again.',
        'Keep the flustered repetition and the stammer. His apology should run directly into what he is apologizing for.',
        None, ('S-sorry for the commotion!', 'Please excuse us.')),
    (0,50,73): ('Lil', 'Lil cautiously admits that she has found a way to live that is about more than making money.',
        'Keep the revelation personal and tentative. Rafael pretends to understand, and Lil asks him for a present without naming the occasion.',
        "Well, I guess I've found more to live for than making money.",
        ("I've found more", 'to live for', 'than making money.')),
    (0,52,18): ('Port Worker', 'Admiral Albuquerque of the Portuguese regular forces asked the port worker to tell Rafael to return to Lisbon if they met.',
        'Keep the admiral’s title, the conditional relay and the destination. Rafael’s surprise in the next turn is about the military’s interest.',
        'Admiral Albuquerque of the Portuguese military asked me to pass on a message if I saw you. He wants you back home in Lisbon.',
        ('Admiral Albuquerque', 'Portuguese military', 'pass on a message', 'if I saw you.', 'He wants you back home in Lisbon.')),
    (0,54,31): ('Shopkeeper', 'The shopkeeper reports hearing that the governor’s office is being moved to Sofala.',
        'Keep the rumor and the reference to Silveira. The second row preserves the whole office and destination phrase. Rafael rushes off at the place name.',
        None, ("I hear he's moving", "the governor's office", 'to Sofala...')),
    (0,55,115): ('Fernando', 'Fernando shouts that Silveira has made him take this seriously.',
        '“Now you’ve done it” carries the threat in the crew’s chorus of reactions. Silveira has provoked him into taking this seriously.',
        "Silveira! Now you've done it!", ("Now you've done it!",)),
    (0,55,142): ('Rafael', 'Rafael hesitates to fight other Portuguese people but dislikes the idea of backing down even more.',
        'Keep his stammer and reluctance after the louder reactions. “Fight” preserves the source’s range without asserting a formal war.',
        "Y-yes. I don't want to fight fellow Portuguese, but backing down is worse.",
        ("I don't want to fight", 'fellow Portuguese', 'backing down is worse.')),
    (0,56,69): ('Port Worker', 'The port worker condemns the adventurer’s plan to make money by revealing a Proof of Conquest’s location to Espinosa.',
        'Make the sale of information explicit. The townspeople bought the clue to keep it away from Espinosa and give it to Rafael.',
        'Telling that devil where to find a Proof of Conquest for money... What nerve!',
        ('that devil', 'where to find', 'a Proof of Conquest', 'for money...', 'What nerve!')),
    (0,57,95): ('Arcadius', 'Arcadius says of course he would visit Claudio too. They are crewmates.',
        'Keep the gentle reassurance and the full tag. Claudio is embarrassed by his own question and tells Arcadius to go see Emilio.',
        None, ("We're crewmates, aren't we?",)),
    (0,57,122): ('Arcadius', 'Arcadius did not know Emilio liked flowers, is glad he does, and tells him to eat plenty.',
        'The admission and warm encouragement land well. Keep the clauses clear so “them” still answers the question about the flowers.',
        None, ("But I'm glad you like them.", 'Have plenty to eat', 'all right?')),
    (0,58,76): ('Uddin', 'Uddin expects the Indian Ocean’s Proof of Conquest to be a book called the Rigveda.',
        'The existing line preserves the region, the book’s name and Uddin’s qualified certainty. The short opening gives room to say “Proof of Conquest” as a unit.',
        None, ('Proof of Conquest', 'should be a book', 'called the Rigveda.')),
    (0,60,234): ('Pereira', 'Pereira laughs and says he already knows a failed plan could cost him his governorship.',
        'Keep his confidence and dismissive laugh. Rafael presses on because someone needs to be able to take responsibility if they fail.',
        "Ha ha ha! Is that what's worrying you? I know full well!", ("Is that what's worrying you?", 'I know full well!')),
    (0,60,277): ('Rafael', 'Rafael says his company will leave Southeast Asia immediately.',
        'Keep the brief announcement and its intact destination and timing. Pereira asks what happens next and Rafael explains who will handle the region.',
        None, ("We're leaving", 'Southeast Asia', 'at once.')),
    (0,60,301): ('Rafael', 'Rafael entrusts the region to Pereira as governor of Indochina and the official responsible for Southeast Asia.',
        'Rafael leads with Pereira’s jurisdiction and then states his trust. Pereira recognizes that he is being asked to guard the rear.',
        "No. As governor of Indochina, you oversee Southeast Asia. I'm leaving it all to you, Pereira.",
        ('governor of Indochina', 'you oversee Southeast Asia.', "I'm leaving it all to you, Pereira.")),
    (0,60,399): ('Pereira', 'Pereira points out that regional goods besides spices bring in vast profits. Their controller could use that wealth to set out to conquer.',
        'Smooth the opening while preserving the hypothetical unfinished thought. Rafael supplies its conclusion in the next turn.',
        "And it's not just spices. The goods here bring in huge profits. Say someone controlled that trade. With that money, they could start conquering...",
        ("it's not just spices.", 'bring in huge profits.', 'controlled that trade.', 'With that money,', 'start conquering...')),
    (0,61,136): ('Claudio', 'Claudio exclaims over Pereira’s generosity after the governor gives the group military funds.',
        'Keep Claudio’s delighted surprise and direct compliment. The others follow with their own reactions to the gift.',
        "Whoa, that's generous! You're amazing, Governor!", ("that's generous!", "You're amazing, Governor!")),
    (0,61,158): ('Pereira', 'Pereira assures Rafael the gift is fine and urges him to do his best. He is counting on him.',
        'Keep Pereira’s easy reassurance and firm encouragement before Rafael’s simple acceptance.',
        None, ("I'm counting on you!",)),
}


def bind(ctx, clean):
    queue = base.load(parent.storage.TRIAGE)
    assert queue['candidate_sha256'] == ctx.release['candidate_sha256']
    blocks = {block for _, block, _ in DECISIONS}
    selected = defaultdict(list)
    for lead in queue['records']:
        if lead['file_path'] == FILE and lead['block'] in blocks:
            selected[lead['block']].append(lead)
    inventory, _, _ = prior.scoped_inventory()
    source_bank, current_bank = [
        IlnkContainer.parse(image.read_file(FILE)) for image in (clean, ctx.image)
    ]
    groups = {}
    actual_keys = set()
    for block, leads in selected.items():
        source, current = source_bank.blocks[block], current_bank.blocks[block]
        assert {lead['block_sha256'] for lead in leads} == {sha(current)}
        original, clean_rows = prior.raw_speeches(clean.read_file(ARM), source, inventory)
        commands, current_rows = prior.raw_speeches(ctx.arm, current, inventory)
        assert [row['word'] for row in original] == [row['word'] for row in commands]
        assert [row['complete_preamble_hex'] for row in clean_rows] == [
            row['complete_preamble_hex'] for row in current_rows
        ]
        pairs = {right['offset']: (left, right) for left, right in zip(clean_rows, current_rows, strict=True)}
        matches = []
        for lead in leads:
            ja, en = pairs[lead['offset']]
            assert en['raw_hex'][2:] == lead['stored_body_hex'] and en['selector'] == lead['source_selector']
            actual_keys.add((0, block, ja['record_index']))
            matches.append(dict(id=f"DK4_MES_B{block}_R{ja['record_index']:04d}",
                                source_reference=ja, current_reference=en))
        groups[FILE, block] = source, current, commands, clean_rows, current_rows, matches
    assert actual_keys == DECISIONS.keys(), (actual_keys - DECISIONS.keys(), DECISIONS.keys() - actual_keys)
    return groups


def compile_exchanges(groups):
    source = checked_text(getsource(prior.compile_records), {
        "b'\\0' not in target,": "b'\\0' not in target[1:],",
        'target != old and len(target)': 'len(target)',
    })
    env = vars(prior) | dict(DECISIONS=DECISIONS)
    exec(compile(source, __file__ + '::fixed-native-owner', 'exec'), env)
    contexts, records = env['compile_records'](groups, plan_record)
    for row in records:
        fit_storage_padding(row)
    return contexts, records


def fit_storage_padding(row):
    compiled = row['automatic_layout']
    encoded = bytes.fromhex(compiled['encoded_hex'])
    lines = encoded[1:].split(b'\n')
    trailing = row['trailing_blank_bytes']
    if len(lines) % 4 or len(lines[-1]) + trailing <= 36:
        return
    # At the foot of a page, storage blanks must fit on existing rows.
    # Moving whole glyph pairs before an existing LF preserves its byte phase.
    original_length = len(bytes.fromhex(row['target_hex']))
    moved = {}
    for index, line in enumerate(lines[:-1]):
        needed = len(lines[-1]) + trailing - 36
        if needed <= 0:
            break
        pairs = min((needed + 1) // 2, (35 - len(line)) // 2, trailing // 2)
        if pairs <= 0:
            continue
        count = 2 * pairs
        lines[index] += b' ' * count
        moved[str(index + 1)] = count
        trailing -= count
    assert len(lines[-1]) + trailing <= 36, row['id']
    target = encoded[:1] + b'\n'.join(lines) + b' ' * trailing
    assert len(target) == original_length and target[0] == encoded[0]
    row.update(target_hex=target.hex(), trailing_blank_bytes=trailing, storage_padding_before_line_feed=moved)


def bind_planner():
    source = checked_text(getsource(prior.layout.plan), {
        "row['source_selector'] in [2,21]": "0 < row['source_selector'] < 207",
        'frozenset([2,21])': "frozenset([row['source_selector']])",
        'def solve(start,line):': 'def solve(start,line,budget):',
        'if line==4:': 'if line==limit:',
        'return (0,0,0,0),()': 'return (0,0,0,0,0,0,0),()',
        'tail=solve(stop,line+1)': 'extra=0 if final else 1+reserve\n'
            '            if extra>budget:continue\n'
            '            tail=solve(stop,line+1,budget-extra)',
        "if row['id']=='DK4_MES_B218_R0023' and pair==('it','whatever'):weak=0":
            "protected = int(pair in row['protected_pairs'])\n"
            "            mid_sentence_page = int(line==3 and not final and not terminal)\n"
            "            sparse_fragment = int(not terminal and not final and length<12)",
        '(cost[0]+tiny,cost[1]+1,cost[2]+weak,cost[3]+':
            '(cost[0]+tiny,cost[1]+protected,cost[2]+sparse_fragment,cost[3]+mid_sentence_page,cost[4]+1,cost[5]+weak,cost[6]+',
        'result=solve(0,0)': "result=solve(0,0,len(bytes.fromhex(row['current_hex']))-1-len(body))",
        '    @cache': "    limit=8 if bytes.fromhex(row['current_hex'])[1:].count(10)>=4 else 4\n    @cache",
        'max_lines=4,': 'max_lines=limit,',
        'max_total_rows=4,native_rows_per_page=4,expected_native_pages=1':
            'max_total_rows=limit,native_rows_per_page=4,expected_native_pages=(len(lines)+3)//4',
    })
    env = vars(prior.layout) | {'PAIRS': set()}
    exec(compile(source, __file__ + '::phrase-continuity-and-native-page-limit', 'exec'), env)
    return env['plan']


PLANNER = bind_planner()


def plan_record(row):
    if row['source_selector'] != 0:
        return PLANNER(row)
    assert row['source_hex'].startswith('00') and row['current_hex'].startswith('00')
    assert row['source_reference']['complete_preamble_hex'] == '0040ffff0000'
    assert row['current_reference']['complete_preamble_hex'] == '0040ffff0000'
    virtual = row | dict(source_selector=2, source_hex='02' + row['source_hex'][2:],
        english=row['english'].replace('{SPEAKER:00}', '{SPEAKER:02}', 1))
    result = PLANNER(virtual)
    assert result['encoded_hex'].startswith('02')
    return result | dict(source_hex=row['source_hex'], English=row['english'],
        encoded_hex='00' + result['encoded_hex'][2:],
        formatted_markup=result['formatted_markup'].replace('{SPEAKER:02}', '{SPEAKER:00}', 1),
        original_00_selector_preserved=True)


def native_validation(ctx, records):
    _, paint = prior.precedent.planners(ctx.arm)
    font = ctx.image.read_file('/GRP/KANJI.FNT')
    source = checked_text(getsource(prior.expansion.expand), {
        'assert identity==prefix and captain==2': 'assert identity==prefix and captain==3',
    })
    env = vars(prior.expansion).copy()
    exec(compile(source, __file__ + '::registered-native-processor', 'exec'), env)
    pictures = []
    for row in records:
        for label, field in (('before', 'current_hex'), ('after', 'target_hex')):
            body = bytes.fromhex(row[field])[1:]
            bound = ctx.execute(env['expand'], body, row['source_selector'])
            assert len(bound['cases']) == 4
            assert all(case['output_hex'] == body.hex() for case in bound['cases'])
            try:
                display = paint(ctx.arm, font, body)
            except AssertionError as error:
                raise AssertionError((row['id'], label, body)) from error
            assert display['complete_consumed_bytes'] == len(body)
            pages = display['pages']
            if label == 'after':
                assert len(pages) == row['automatic_layout']['expected_native_pages']
                if row.get('storage_padding_before_line_feed'):
                    unpadded = bytes.fromhex(row['automatic_layout']['encoded_hex'])[1:]
                    reference = paint(ctx.arm, font, unpadded)
                    assert [p['native_plane_hex'] for p in pages] == [p['native_plane_hex'] for p in reference['pages']]
            assert pages[0]['first_visible_origin'] == [0, 0]
            for page in pages:
                pixels = bytes.fromhex(page['native_plane_hex'])
                page['plane_sha256'] = sha(pixels)
                title = f"{row['id'].split('_B')[1]} {label} {page['page']}/{len(pages)}"
                pictures.append((title, pixels))
            row[label + '_native'] = dict(processor=bound, pages=pages)
    return pictures


def contact_sheets(pictures):
    colors = {0: (239,232,201), 1: (0,8,0), 15: (98,97,98)}
    sheets = []
    for start in range(0, len(pictures), 8):
        subset = pictures[start:start + 8]
        sheet = Image.new('RGB', (888, (len(subset) + 1) // 2 * 154), '#263238')
        draw = ImageDraw.Draw(sheet)
        for index, (title, pixels) in enumerate(subset):
            x, y = index % 2 * 444, index // 2 * 154
            draw.text((x + 4, y + 2), title, fill='white')
            plane = Image.new('RGB', (216,64))
            plane.putdata([colors[value] for value in pixels])
            sheet.paste(plane.resize((432,128), Image.Resampling.NEAREST), (x + 4, y + 21))
        path = ROOT / f'before_after_{len(sheets) + 1}.png'
        sheet.save(path)
        sheets.append(dict(path=path.as_posix(), sha256=base.digest(path)))
    return sheets


def main():
    assert not ROOT.exists() and not REVIEW.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(CLEAN) == release['clean_input_sha256']
    ctx = prior.RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    groups = bind(ctx, base.NdsImage.open(CLEAN))
    contexts, records = compile_exchanges(groups)
    unchanged = [row for row in records if row['current_hex'] == row['target_hex']]
    records = [row for row in records if row['current_hex'] != row['target_hex']]
    for row in records:
        print(row['id'], row['automatic_layout']['lines'], row['trailing_blank_bytes'], flush=True)
    for row in unchanged:
        print('UNCHANGED', row['id'], row['automatic_layout']['lines'], flush=True)
    pictures = native_validation(ctx, records + unchanged)
    ROOT.mkdir()
    archives = {}
    for name, raw in prior.transform(ctx.image, records):
        path = ROOT / Path(name).name
        path.write_bytes(raw)
        archives[name] = dict(path=path.as_posix(), sha256=sha(raw), source_sha256=sha(ctx.image.read_file(name)))
    sheets = contact_sheets(pictures)
    base.save(REVIEW, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=['source','context','localization','naturalness','formatting'],
        candidate_sha256=release['candidate_sha256'], records=records, unchanged_leads=unchanged,
        complete_exchange_references=contexts, zero_new_credit=True, full_goal_complete=False))
    base.save(PROOF, dict(candidate_sha256=release['candidate_sha256'], review_sha256=base.digest(REVIEW),
        archives=archives, sheets=sheets, blocks=[list(key) for key in groups],
        unchanged_terminators_offsets_block_extents_and_unowned_bytes=True,
        archive_inverses_exact=True, checked_complete_native_pages=len(pictures),
        checked_original_processor_alignments=8 * (len(records) + len(unchanged))))


if __name__ == '__main__':
    main()
