"""Review flagged breaks in Rafael's recruitment, training and crew conversations."""

import argparse
from collections import defaultdict
from inspect import getsource
from pathlib import Path
import re
from types import FunctionType

from scripts import register_rafael_name_wraps_20261114 as parent
from scripts import stage_rafael_name_wraps_20261114 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, sha, prior, wraps = previous.base, previous.sha, previous.prior, previous.wraps
FILE, ARM, CLEAN, IlnkContainer = previous.FILE, previous.ARM, previous.CLEAN, previous.IlnkContainer
ROOT = Path('work/rafael_crew_wraps_20261114_v1')
CAPTURE = ROOT / 'rafael_startup/capture_report.json'
RUNTIME = ROOT / 'rafael_native_context.json'
REVIEW = parent.TRIAGE.with_name('rafael_crew_wraps_context_v1.json')
PROOF = ROOT / 'stored_and_native.json'
DEFAULTS = previous.DEFAULTS | {'FO': 'Castor Co.'}
TOKEN = re.compile(r'\{MACRO:(FI|FA|FO)\}')
DECISIONS = {
    (81,94): ('Julio', None, 'Julio identifies the man as the picador, the supporting bullfighter.',
        'Keep the established introduction to the term. Julio explains what the picador does in the following line.',
        ("the matador's assistant.",)),
    (81,224): ('Rafael', "It's settled, then! What's your name? I'm {MACRO:FI} {MACRO:FA}.",
        'Rafael takes Emilio’s agreement as settled and asks his name before introducing himself.',
        'Use separate beats for the agreement, the question and the introduction. Emilio follows with his own name.',
        ("What's your name?", "I'm {MACRO:FI} {MACRO:FA}.")),
    (82,103): ('Mivor', "I-it's not just because my parents told me to! I really do care about Miss Cristina...",
        'Mivor stammers a protest that his parents’ instructions are not the reason. His feelings for Cristina are genuine.',
        'Keep his nervous insistence and deferential address. Cristina talks over him to explain what her own parents want.',
        ('my parents', 'told me to!', 'I really do care about', 'Miss Cristina...')),
    (82,183): ('Cristina', "You just don't get it! Hyah!",
        'Cristina exclaims that he simply does not understand, then gives a fighting cry.',
        'She stops trying to explain herself during the duel. Use an exasperated outburst and a cry she can shout as she strikes.',
        ("You just don't get it!",)),
    (82,224): ('Cristina', "Really? We can go?! Now that's my kind of admiral! This'll be fun!",
        'Cristina is delighted that Rafael will take her to Spain and calls him an admiral she can talk to.',
        'Keep the snap from surprise to approval to excitement. Julio’s next line recognizes her familiar exuberance.',
        ("Now that's my kind of admiral!", "This'll be fun!")),
    (83,63): ('Cristina', None, 'Cristina is relieved that she will no longer be pursued.',
        'Keep the sigh and what she thinks is the end of the problem. The next startled line immediately breaks that relief.',
        ('At least', "he won't be chasing me anymore...")),
    (83,307): ('Mivor', "Really?! You thought I was impressive?! I'm so, so happy!",
        'Mivor asks in disbelief if she really thought he was impressive, then repeats how happy he is.',
        'Keep the delighted echo and repetition before Cristina warns him he is getting the wrong idea.',
        ('You thought I was impressive?!', "I'm so, so happy!")),
    (84,64): ('Rafael', "...You're awfully eager, Clau.",
        'Rafael notices that Claudio is unusually eager to find Gerhard.',
        'Use a familiar observation instead of a stiff explanation. Claudio brushes it off without revealing his motive.',
        ("You're awfully eager, Clau.",)),
    (84,89): ('Rafael', "Oh, hello. I'm with {MACRO:FO}, and...",
        'Rafael gives a polite first greeting and begins identifying his company before being interrupted.',
        'Keep the unfinished introduction and the whole company substitution. Claudio jumps in to introduce both of them.',
        ("I'm with {MACRO:FO}, and...",)),
    (84,93): ('Claudio', None, 'Claudio introduces Rafael as admiral and himself as the navigator Claudio Manaus.',
        'Keep the abrupt full introduction as Claudio takes over. The rank and navigator role are explicit in the Japanese.',
        ('Admiral {MACRO:FI} {MACRO:FA}.', "I'm Claudio Manaus,", 'a navigator.')),
    (84,193): ('Rafael', "But that hasn't settled it, has it?",
        'Rafael asks Gerhard whether living quietly ashore really resolves what happened.',
        'Keep his respectful challenge as a question. Gerhard invites him to say what he means plainly.',
        ("that hasn't settled it, has it?",)),
    (84,206): ('Gerhard', "Help...? What good is an old man's advice? He took everything from me.",
        'Gerhard doubts the value of an old man’s advice and says the man took everything from him.',
        'Preserve his weary self-doubt after Rafael asks for help. The unnamed he still points to Vels from the previous turn.',
        ("What good is", "an old man's advice?", 'He took everything from me.')),
    (84,417): ('Gerhard', "Before I go to sea, I have something to teach you. Will you take some special training?",
        'Before putting to sea, Gerhard says he has something to teach and asks if Rafael is willing to undergo special training.',
        'Keep the condition and invitation clear at the choice. The next response depends on whether Rafael takes him up on it.',
        ('Before I go to sea,', 'something to teach you.', 'some special training?')),
    (85,25): ('Rafael', None, 'Rafael calls for the admiral and gives his full name to identify himself.',
        'Keep the polite address and the full name as one reply, answered by Gerhard’s recognition.',
        ('are you there?', "It's {MACRO:FI} {MACRO:FA}.")),
    (86,95): ('Cesare', "By my calculations, he'd give us quite an advantage in battle.",
        'Cesare says his calculations indicate the man would contribute greatly to their fighting strength.',
        'Keep his calculated assessment and emphatic scale. Claudio reduces the calculation to the practical point that the inventor could be useful.',
        ('By my calculations,', "he'd give", 'quite an advantage', 'in battle.')),
    (86,150): ('Charles', "I told you. This isn't a failure! I've almost got it right. Besides...",
        'Charles insists he told the man before that the experiment was not a failure and that success is close.',
        'Let him protest with confidence and trail off when the visitor cuts him short. He gives no guarantee of success.',
        ('I told you.', "This isn't a failure!", "I've almost got it right.", 'Besides...')),
    (87,66): ('Sojin Kurushima', "Look what you've done! You ran right into my man on purpose! He's broken a bone! This is serious!",
        'Kurushima accuses Rafael’s group of intentionally bumping into his underling and claims a bone is broken.',
        'Keep the loud performance and the accusation as his version of what happened. Rafael immediately says they were the ones who ran into him.',
        ("Look what you've done!", 'ran right into my man', 'on purpose!', "He's broken a bone!", 'This is serious!')),
    (87,93): ('Sailor', "Oh, you want a fight? Boss, they ran into us and now they're picking a fight!",
        'The underling echoes the accusation and claims the group intends to start a fight.',
        'Keep the reported escalation and the address to his boss. Kurushima responds by ordering his men to attack.',
        ('you want a fight?', 'ran into us', "they're picking a fight!")),
    (87,213): ('Rafael', None, 'Rafael welcomes Yukihisa and introduces himself with both names.',
        'Retain Rafael’s easy acceptance and his full-name introduction. Yukihisa answers with his own full name and a formal greeting.',
        ("I'm {MACRO:FI} {MACRO:FA}.",)),
    (90,14): ('Janus', None, 'Janus addresses the admiral and remarks fondly that ships are a wonderful thing.',
        'Keep the quiet enthusiasm and short tag. He goes on to imagine what he would do if he had a fleet of his own.',
        ('Oh, Admiral...', "Ships are wonderful, aren't they?")),
    (91,32): ('Fernando', "Watch your mouth! That's our admiral!",
        'Fernando angrily objects to how the sailor spoke to his admiral.',
        'Keep the sharp defense before the sailor challenges him. The source gives Fernando the admiral title in this rebuke.',
        ('Watch your mouth!', "That's our admiral!")),
    (91,62): ('Sailor', "I've asked around every time a ship came in. You're the hundredth.",
        'The sailor has approached arrivals here each time a ship docked. Rafael’s group is exactly the hundredth.',
        'Keep the repeated effort and the punch of the exact count. It explains why he has been waiting with the charm.',
        ('every time a ship came in.', "You're the hundredth.")),
    (91,70): ('Sailor', None, 'The sailor identifies the bullet pendant and says it is reputed to bring miracles.',
        'Keep the item name together and the claim attributed to reputation. Rafael next asks if he really may accept something so precious.',
        ('Miracle Bullet Charm.', "It's said to bring miracles.")),
    (93,68): ('Rafael', "Emilio, want to try the local specialty?",
        'Rafael asks Emilio if he would like to try a local specialty.',
        'Make the quick change of subject sound like a friendly invitation. Emilio stops demanding his banana when he hears the offer.',
        ('the local specialty?',)),
    (97,47): ('Angelo', "I hear it's an all-black outfit called Ninja Garb. It's actually armor, not just clothing!",
        'Angelo reports that the all-black outfit is called Ninja Garb and is actually armor.',
        'Keep the hearsay, the exact item name and the surprise that prompts Yukihisa to echo the word armor.',
        ('called Ninja Garb.', "It's actually armor,")),
    (101,68): ('Julio', "The Mediterranean... or was it the Black Sea? They say there's a piece of legendary armor tucked away somewhere around there. I never looked hard for it, but...",
        'Julio remembers conflicting locations for the rumored legendary armor. He did not seriously search for it before.',
        'Keep the old sailor’s wavering memory and the unfinished thought, then let his wish to give the shield to Cristina explain what changed.',
        ('The Mediterranean...', 'the Black Sea?', 'legendary armor', 'somewhere around there.', 'I never looked hard for it, but...')),
    (101,83): ('Julio', 'Back to work for you too, Admiral.',
        'Julio tells the admiral to get back to work as well.',
        'After calling his own story an old man’s rambling, Julio briskly turns both of them back to work.',
        ('Back to work', 'for you too, Admiral.')),
    (102,29): ('Samwell', "So close! Really close! It's mail with peacock tail feathers on the back.",
        'Samwell says Rafael nearly guessed it. The mail has peacock tail feathers attached to its back.',
        'Keep his delighted repetition and the distinction between decoration and construction before Rafael questions how useful the armor is.',
        ('So close!', 'Really close!', "It's mail", 'peacock tail feathers', 'on the back.')),
    (102,46): ('Samwell', "I heard it's on a little island way, way, way southeast of the Cape of Good Hope. That's all I found out.",
        'Samwell heard that it is on a small island far to the southeast of the Cape of Good Hope and knows no more.',
        'Preserve the exaggerated distance and hearsay. Rafael’s skepticism needs the clue to stay imprecise.',
        ('way, way, way southeast', 'Cape of Good Hope.', "That's all I found out.")),
    (103,23): ('Samwell', 'Just what the name says. A vest the jaguar god is supposed to inhabit. I hear it is in the New World.',
        'Samwell says the garment is believed to house the jaguar god and is reportedly in the New World.',
        'Keep his casual explanation and both attributions. The next line recognizes that this is another rumor.',
        ('the jaguar god', 'is supposed to inhabit.', 'I hear it is', 'in the New World.')),
    (103,39): ('Samwell', "It's a lot of work finding out where these things are. I'm bored with it already.",
        'Samwell finds it hard to locate such things and is already tired of doing it.',
        'Keep the abrupt admission after he says this is his last rumor. He explains his short-lived interests in the next line.',
        ('finding out where', 'these things are.', "I'm bored with it already.")),
}


def contract():
    """Retain the established pair phase and allow each original page count."""
    source = getsource(previous.planner)
    source = checked_text(source, {
        "macro_ascii_lengths={'FI':6,'FA':6}, macro_widths={'FI':36,'FA':36}":
            "macro_ascii_lengths={'FI':6,'FA':6,'FO':10}, macro_widths={'FI':36,'FA':36,'FO':60}",
        "'def solve(start,line):': 'def solve(start,line,budget):',":
            """'def solve(start,line):': 'def solve(start,line,budget):',
        'if line==4:': 'if line==limit:',
        '    @cache': "    limit=8 if bytes.fromhex(row['current_hex'])[1:].count(10)>=4 else 4\\n    @cache",
        'max_lines=4,': 'max_lines=limit,',
        'max_total_rows=4,native_rows_per_page=4,expected_native_pages=1':
            'max_total_rows=limit,native_rows_per_page=4,expected_native_pages=(len(lines)+3)//4',""",
        "'return (0,0,0,0),()': 'return (0,0,0,0,0),()',": "'return (0,0,0,0),()': 'return (0,0,0,0,0,0),()',",
        '(cost[0]+tiny,cost[1]+protected,cost[2]+1,cost[3]+weak,cost[4]+':
            '(cost[0]+tiny,cost[1]+int(line==3 and not final and not terminal),cost[2]+protected,cost[3]+1,cost[4]+weak,cost[5]+',
    })
    env = vars(previous) | dict(expanded=expanded, TOKEN=TOKEN)
    exec(compile(source, __file__ + '::same-pair-phase-and-multi-page-allowance', 'exec'), env)
    return env['planner']()


def expanded(text):
    return TOKEN.sub(lambda match: DEFAULTS[match[1]], text)


def expand_bytes(body):
    for token, output in DEFAULTS.items():
        body = body.replace(token.encode('ascii'), output.encode('ascii'))
    return body


bind_runtime = FunctionType(previous.bind_runtime.__code__, vars(previous) | globals())
native_source = checked_text(getsource(previous.native), {
    "body.replace(b'FI', b'Rafael').replace(b'FA', b'Castor')": 'expand_bytes(body)',
})
native_env = vars(previous) | {'expand_bytes': expand_bytes}
exec(compile(native_source, __file__ + '::same-native-Rafael-expander', 'exec'), native_env)
native = native_env['native']


def get_exchanges(current, clean):
    queue = base.load(parent.TRIAGE)
    assert queue['candidate_sha256'] == base.digest(parent.ROM)
    bank, original = (IlnkContainer.parse(image.read_file(FILE)).blocks for image in (current, clean))
    assert queue['scanned'][FILE]['archive_sha256'] == sha(current.read_file(FILE))
    inventory, _, _ = prior.scoped_inventory()
    source_arm, arm = clean.read_file(ARM), current.read_file(ARM)
    blocks = {block for block, _ in DECISIONS}
    flags = defaultdict(dict)
    for row in queue['records']:
        if row['file_path'] == FILE and row['block'] in blocks:
            flags[row['block']][row['offset']] = row
    keys, contexts, selected = set(), [], []
    for block, leads in sorted(flags.items()):
        ja_cmd, ja_rows = prior.raw_speeches(source_arm, original[block], inventory)
        en_cmd, en_rows = prior.raw_speeches(arm, bank[block], inventory)
        # Block 84 already contains two registered FE continuation commands.
        extras = {6096, 7436} if block == 84 else set()
        if extras:
            for extra in extras:
                before, after = next((a, b) for a, b in zip(en_cmd, en_cmd[1:]) if b['offset'] == extra)
                assert before['word'] == after['word'] == 0x4000
                assert all(bytes.fromhex(row['whole_command_hex'])[5] == 254 for row in (before, after))
        assert [x['word'] for x in ja_cmd] == [x['word'] for x in en_cmd if x['offset'] not in extras]
        pairs = list(zip(ja_rows, [r for r in en_rows if r['offset'] - 5 not in extras], strict=True))
        assert all(a['complete_preamble_hex'] == b['complete_preamble_hex'] for a, b in pairs)
        digest = sha(bank[block])
        assert {r['block_sha256'] for r in leads.values()} == {digest}
        contexts.append(dict(file_path=FILE, block=block, source_block_sha256=sha(original[block]),
            current_block_sha256=digest, source_progressive_exchange=ja_rows, current_progressive_exchange=en_rows,
            existing_extra_FE_commands=sorted(extras)))
        for ja, en in pairs:
            if en['offset'] not in leads:
                continue
            lead = leads[en['offset']]
            assert en['raw_hex'][2:] == lead['stored_body_hex'] and en['selector'] == lead['source_selector']
            key = block, ja['record_index']
            keys.add(key)
            selected.append((key, ja, en))
    assert keys == DECISIONS.keys()
    return contexts, selected


def compile_rows(current, clean):
    plan = contract()
    contexts, selected = get_exchanges(current, clean)
    rows = []
    for (block, index), source, at in selected:
        ident = f'DK4_MES_B{block}_R{index:04d}'
        ja, old = bytes.fromhex(source['raw_hex']), bytes.fromhex(at['raw_hex'])
        assert ja[0] == old[0] == at['selector']
        current_english = ' '.join(re.sub(r'FI|FA|FO', lambda m: '{MACRO:' + m[0] + '}', old[1:].decode('ascii')).split())
        actor, draft, meaning, note, phrases = DECISIONS[block, index]
        english = draft or current_english
        token_order = [match.encode('ascii') for match in TOKEN.findall(english)]
        assert token_order == previous.bare_tokens(ja[1:]) == previous.bare_tokens(old[1:]), ident
        protected = set()
        for phrase in phrases:
            assert phrase.casefold() in english.casefold(), (ident, phrase, english)
            words = [prior.layout.norm(word) for word in phrase.split()]
            protected.update(zip(words, words[1:]))
        row = dict(id=ident, file_path=FILE, block=block, source_selector=ja[0], kind='progressive',
            speaker=actor, source_meaning=meaning, localization_note=note, context=f'Original Rafael exchange in block {block}.',
            source_reference=source, current_reference=at, source_Japanese=ja[1:].decode('cp932'),
            source_hex=ja.hex(), current_hex=old.hex(), current_English=current_english,
            english=f'{{SPEAKER:{ja[0]:02X}}}{english}', decision='retention' if english == current_english else 'revision',
            protected_pairs=protected, review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False))
        layout = plan(row)
        assert all(d['code'] == 'line-break-count' and d['severity'] == 'warning' for d in layout['diagnostics']), (ident, layout['diagnostics'])
        assert ' '.join(layout['lines']) == english
        del row['protected_pairs']
        encoded = bytes.fromhex(layout['encoded_hex'])
        assert previous.bare_tokens(encoded[1:]) == token_order and encoded[0] == ja[0] and b'\0' not in encoded[1:]
        pad = len(old) - len(encoded)
        assert 0 <= pad < 36, (ident, pad)
        row.update(automatic_layout=layout, target_hex=(encoded + b' ' * pad).hex(), trailing_blank_bytes=pad,
                   line_count_reason='Phrase flow sets line count within the original viewport.' if layout['diagnostics'] else None)
        if not token_order:
            wraps.fit_storage_padding(row)
        rows.append(row)
    return contexts, rows


def main(preview):
    assert not REVIEW.exists() and not PROOF.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256'] and base.digest(CLEAN) == release['clean_input_sha256']
    current, clean = (base.NdsImage.open(path) for path in (parent.ROM, CLEAN))
    contexts, records = compile_rows(current, clean)
    for row in records:
        print(row['id'], row['decision'], row['trailing_blank_bytes'],
              [expanded(line) for line in row['automatic_layout']['lines']], flush=True)
    if preview:
        return
    runtime = bind_runtime()
    default = native(runtime, 0, b'FI FA FO')
    _, paint = prior.precedent.planners(runtime.arm)
    font = runtime.image.read_file('/GRP/KANJI.FNT')
    pictures = []
    for row in records:
        for label, field in [('before', 'current_hex'), ('after', 'target_hex')]:
            body = bytes.fromhex(row[field])[1:]
            result = native(runtime, row['source_selector'], body, paint)
            pages = result['pages']
            assert pages[0]['first_visible_origin'] == [0, 0]
            if label == 'after':
                assert len(pages) == row['automatic_layout']['expected_native_pages']
                encoded = bytes.fromhex(row['automatic_layout']['encoded_hex'])[1:]
                unpadded = paint(runtime.arm, font, expand_bytes(encoded))['pages']
                assert [p['native_plane_hex'] for p in pages] == [p['native_plane_hex'] for p in unpadded]
            for page in pages:
                pictures.append((f"{row['id'].split('_B')[1]} {label} {page['page']}/{len(pages)}",
                                 bytes.fromhex(page['native_plane_hex'])))
            row[label + '_native'] = result
    retained = [row for row in records if row['current_hex'] == row['target_hex']]
    changed = [row for row in records if row['current_hex'] != row['target_hex']]
    archives = {}
    for name, raw in prior.transform(current, changed):
        path = ROOT / Path(name).name
        path.write_bytes(raw)
        archives[name] = dict(path=path.as_posix(), sha256=sha(raw), source_sha256=sha(current.read_file(name)))
    sheets = FunctionType(wraps.contact_sheets.__code__, vars(wraps) | {'ROOT': ROOT})(pictures)
    base.save(REVIEW, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
        candidate_sha256=release['candidate_sha256'], records=changed, unchanged_leads=retained,
        complete_exchange_references=contexts, zero_new_credit=True, full_goal_complete=False))
    base.save(PROOF, dict(candidate_sha256=release['candidate_sha256'], review_sha256=base.digest(REVIEW),
        archives=archives, sheets=sheets, blocks=[[FILE, group['block']] for group in contexts],
        unchanged_terminators_offsets_block_extents_and_unowned_bytes=True, archive_inverses_exact=True,
        checked_complete_native_pages=len(pictures), checked_original_processor_alignments=8 * len(records),
        verified_default_name_expansion=default, native_runtime=runtime.receipt()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true')
    main(parser.parse_args().preview)

