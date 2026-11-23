"""Review and stage the complete source-bound Kurushima confrontation."""

from pathlib import Path
from types import FunctionType

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC

from scripts import register_voyage_rat_and_search_dialogue_20261115 as parent
from scripts import stage_rafael_early_wraps_20261111 as layout
from scripts.checkpoint_story_glyph_consistency_20261115 import catalogue
from scripts.native_call_abi_v764 import STOP, call
from scripts.stage_embedded_story_roles_20261115 import (
    ARM, CLEAN, GATES, IlnkContainer, RegisteredRuntime, digest, files, raw_speeches, references, scoped_inventory,
)


base = parent.base
ROOT = Path('work/kurushima_encounter_20261115_v1')
ROM, STORED = ROOT / 'Kurushima_Encounter_RESEARCH_ONLY.nds', ROOT / 'staged.json'
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/kurushima_encounter_20261115_v1.json')
OBSERVATION = parent.VERIFY / 'lisbon_voyage_nagasaki_observation_20261115_v1.json'
FILE, BLOCKS = '/data/SC3.DK4', (3,)
MARKER = '{MACRO:FI}'
CONTEXT = ('Sojin challenges Maria at sea. Yukihisa tells him to stop. Sojin calls him a disgrace for siding '
           'with foreigners, and Yukihisa challenges his attacks on the mainland coast. Sojin jeers at him and '
           'offers to spare only Maria if she surrenders and becomes his. Maria mocks his beard, and he answers with a threat.')
SPEAKERS = {41: 'Sojin Kurushima', 12: 'Yukihisa Shiraki', 3: 'Maria Li'}
REVISION = {
    5: ("Well, {MACRO:FI}! Today we settle this for good!", ('Today we settle this for good!',)),
    18: ("A samurai siding with foreigners? You're a disgrace!", ('A samurai siding with foreigners?', "You're a disgrace!")),
    32: ("Heh heh, {MACRO:FI}! Surrender quietly and be mine, and I'll spare only you!",
         ('Surrender quietly and be mine,', "and I'll spare only you!")),
    35: ("Sojin Kurushima... Mouth off again and I'll pluck out that high-and-mighty beard!",
         ('Sojin Kurushima...', "Mouth off again and I'll pluck out", 'that high-and-mighty beard!')),
}
NOTES = {
    5: ('Sojin calls to the captain with rough familiarity and declares that today he will settle the score.',
        'Keep the personalized address and the decisive challenge. Put the rest of the threat after the salute so '
        'a long captain name cannot force “settling” onto a line by itself.'),
    15: ('Yukihisa tells Kurushima to stop his foolish conduct.',
         '“End this folly” fits Yukihisa’s formal, direct rebuke and the short pause before Sojin lashes back.'),
    18: ('Sojin sneers that Yukihisa sides with foreigners despite being a samurai, and calls him unworthy of the name.',
         'Aim the disgrace at Yukihisa himself and keep the accusation about taking the foreigners’ side.'),
    22: ('Yukihisa asks whether raiding the mainland coast and plundering defenseless people is conduct worthy of a proud samurai.',
         'The rhetorical question answers Sojin’s accusation in the same formal register and keeps both charges.'),
    26: ('Sojin mocks Yukihisa’s stiffness and says that is the disposition he hates most.',
         'Keep the jeer, the two-beat disdain and his personal dislike immediately before he turns back to Maria.'),
    32: ('Sojin laughs, addresses the captain, and makes a coercive offer. If she surrenders quietly and becomes his, he will spare her alone.',
         'Keep both conditions and put the promise in Sojin’s own voice. “Only you” keeps the threat to everyone else implicit.'),
    35: ('Maria tells Sojin that if he keeps talking nonsense she will pluck out his haughty-looking beard.',
         '“Mouth off” matches the provocation. “High-and-mighty beard” preserves the joke while Maria answers his threat with one of her own.'),
    39: ('Sojin laughs loudly, pauses, then threatens to kill her.',
         'The existing laugh and sudden threat carry the turn from mockery to open hostility.'),
}


def transform(image, records):
    bank = IlnkContainer.parse(image.read_file(FILE))
    block, = BLOCKS
    revised = bytearray(bank.blocks[block])
    for row in records:
        if row['decision'] != 'revision':
            continue
        pos = row['current_reference']['offset']
        old, new = map(bytes.fromhex, (row['current_hex'], row['target_hex']))
        assert len(old) == len(new) and old[0] == new[0] == row['source_selector']
        end = pos + len(old)
        assert revised[pos:end + 1] == old + b'\0'
        revised[pos:end] = new
    bank.blocks[block] = bytes(revised)
    yield FILE, bank.to_bytes()


def compile_revision(row, phrases):
    # The established planner measures printable width and storage separately.
    # Credit the markup characters discarded when FI becomes a two-byte token.
    text = row['english']
    extra = (len(MARKER) - 2) * text.count(MARKER)
    planner = FunctionType(layout.PLANNER.__code__, layout.PLANNER.__globals__ |
                           {'display': lambda line: line.replace(MARKER, 'W' * 16)})
    norm = layout.prior.layout.norm
    pairs = [(norm(a), norm(b)) for phrase in phrases for a, b in zip(phrase.split(), phrase.split()[1:])]
    compiled = planner(row | {'current_hex': row['current_hex'] + '20' * extra, 'protected_pairs': pairs})
    assert compiled['expected_native_pages'] == 1
    assert all(any(part in line for line in compiled['lines']) for part in phrases)
    diagnostics = compiled['diagnostics']
    assert all(d['code'] == 'line-break-count' and d['severity'] == 'warning' for d in diagnostics)
    if diagnostics:
        row['qa_waivers'] = ['line-break-count']
        row['qa_waiver_reason'] = 'The verified English paragraphs use automatic one-page wrapping.'
    old = bytes.fromhex(row['current_hex'])
    encoded = bytes.fromhex(compiled['encoded_hex'])
    assert encoded[0] == old[0] and len(encoded) <= len(old)
    assert b'%' not in encoded and b'\0' not in encoded and encoded.count(b'FI') == old.count(b'FI')
    target = encoded.ljust(len(old), b' ')
    row.update(target_hex=target.hex(), automatic_layout=compiled, trailing_blank_bytes=len(target) - len(encoded))


def expand(ctx, selector, raw, name):
    cpu, get, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    assert get(0x7F244) == 3 and get(0x2434C, selector) == selector
    root = get(0xCB184)
    player = root + 0x19E4
    actor = player if selector == 3 else root + 4 + 32 * selector
    field = player + 0x20
    original = bytes(cpu.mem_read(field, 17))
    assert original.split(b'\0', 1)[0] == b'Maria' and 1 <= len(name) <= 16
    cpu.mem_write(field, name.ljust(17, b'\0'))
    before = bytes(cpu.mem_read(0x02000000, 0x400000))
    # Use the same isolated parser entry as the existing progressive proof.
    cpu.hook_add(UC_HOOK_CODE, lambda u, a, s, d: u.reg_write(UC_ARM_REG_PC, STOP),
                 begin=0x020242CC, end=0x020242CC)
    source, destination = 0x02660000, 0x02662000
    guard = b'\xa5' * 16
    result = raw.replace(b'FI', name)
    for alignment in range(4):
        packet = guard + b'\xa5' * alignment + raw + b'\0' + guard
        cpu.mem_write(source - 16, packet)
        cpu.mem_write(destination - 16, b'\xa5' * 288)
        call(cpu, 0x242C8, (destination, source + alignment, actor), instruction_limit=300000)
        assert bytes(cpu.mem_read(destination - 16, 288)) == guard + (result + b'\0').ljust(272, b'\xa5')
        assert bytes(cpu.mem_read(source - 16, len(packet))) == packet
        assert bytes(cpu.mem_read(0x02000000, 0x400000)) == before
    cpu.mem_write(field, original)
    assert bytes(cpu.mem_read(root, 0x1A04)) == ctx.actor_bytes and not provider.reads
    ctx.calls.clear()
    return result


def visible_lines(page):
    rows = {}
    for event in page['events']:
        if event['code'] != 32:
            assert event['kind'] == 'ascii' and event['x'] % 6 == 0
            rows.setdefault(event['y'], {})[event['x'] // 6] = chr(event['code'])
    assert list(rows) == list(range(0, 16 * len(rows), 16))
    return [''.join(cells.get(x, ' ') for x in range(max(cells) + 1)).lstrip() for cells in rows.values()]


def validate_pages(ctx, rows):
    _, paint = layout.prior.precedent.planners(ctx.arm)
    kanji = ctx.image.read_file('/GRP/KANJI.FNT')
    pictures = []
    for row in rows:
        revision = row['decision'] == 'revision'
        sides = ('before', 'after') if revision else ('retained',)
        selector = row['source_selector']
        has_name = MARKER in row['english']
        for side in sides:
            raw = bytes.fromhex(row['target_hex' if side == 'after' else 'current_hex'])[1:]
            examples = [b'Maria']
            if has_name and side in ('before', 'after'):
                examples += [b'Abcdefghijklmnop']
            if has_name and side == 'after':
                examples += [b'Q', b'Al', b'Abcdefghijklmno']
            for name in examples:
                body = expand(ctx, selector, raw, name)
                display = paint(ctx.arm, kanji, body)
                page, = display['pages']
                assert display['complete_consumed_bytes'] == len(body)
                lines = visible_lines(page)
                if side == 'after':
                    expected = [text.replace(MARKER, name.decode('ascii')) for text in row['automatic_layout']['lines']]
                    assert lines == expected, (row['id'], name, lines, expected)
                    if row.get('trailing_blank_bytes'):
                        unpadded = body[:-row['trailing_blank_bytes']]
                        fresh, = paint(ctx.arm, kanji, unpadded)['pages']
                        assert fresh['native_plane_hex'] == page['native_plane_hex']
                pixels = bytes.fromhex(page['native_plane_hex'])
                example = name.decode('ascii') if has_name else 'literal'
                pictures.append((f"{row['id'].split('_R')[1]} {side} {example}", pixels))
                item = dict(example=example, lines=lines, native_plane_sha256=digest(pixels),
                            consumed_bytes=len(body), stored_processor_alignments=4, page_count=1)
                if name == b'Maria':
                    item['native_plane_hex'] = page['native_plane_hex']
                row.setdefault('native_pages', {}).setdefault(side, []).append(item)
    assert len(pictures) == 22
    return pictures


def main():
    assert not ROOT.exists() and not MANUSCRIPT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    ctx = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    clean = base.NdsImage.open(CLEAN)
    manifest = base.load(parent.MANIFEST)
    banks = [IlnkContainer.parse(ctx.image.read_file(f'/data/SC{i}.DK4')).blocks for i in range(4)]
    config = manifest['relocations'][ARM]['reviewed_name_integration']['catalog']
    catalog = catalogue(ctx.arm, config, banks)
    block, = BLOCKS
    old_block = banks[3][block]
    source_block = IlnkContainer.parse(clean.read_file(FILE)).blocks[block]
    inv, _, _ = scoped_inventory()
    source_commands, source = raw_speeches(clean.read_file(ARM), source_block, inv)
    commands, old = raw_speeches(ctx.arm, old_block, inv)
    assert [r['word'] for r in source_commands] == [r['word'] for r in commands]
    observation = base.load(OBSERVATION)
    assert observation['current_block_sha256'] == digest(old_block) and observation['source_block_sha256'] == digest(source_block)
    assert observation['ordinary_saved_game'] and not observation['injected_location']
    credited = {(r['file_path'], r['id']) for r in base.load(base.LEDGER)[base.CONTEXT]['integrated_record_keys']}
    rows = []
    for ordinal, (a, b, observed) in enumerate(zip(references(source_commands, source),
            references(commands, old), observation['nagasaki_encounter'], strict=True)):
        n, selector = a['record_index'], a['selector']
        assert a['complete_preamble_hex'] == b['complete_preamble_hex']
        assert a['raw_hex'] == observed['source_reference']['raw_hex'] and b['raw_hex'] == observed['current_reference']['raw_hex']
        j, e = map(bytes.fromhex, (a['raw_hex'], b['raw_hex']))
        assert j.count(b'FI') == e.count(b'FI') == int(n in (5, 32))
        identity = observed['id']
        assert (FILE, identity) in credited
        previous = ' '.join(e[1:].decode('ascii').split())
        meaning, note = NOTES[n]
        english, phrases = REVISION.get(n, (previous.replace('FI', MARKER), ()))
        row = dict(id=identity, file_path=FILE, block=block, route=3, ordinal=ordinal,
            kind='progressive', source_selector=selector, speaker=SPEAKERS[selector], context=CONTEXT,
            Japanese=j[1:].decode('cp932'), previous_English=previous, source_meaning=meaning, localization_note=note,
            english=f'{{SPEAKER:{selector:02X}}}' + english, decision='revision' if n in REVISION else 'retention',
            source_hex=a['raw_hex'], current_hex=b['raw_hex'], source_reference=a, current_reference=b,
            source_block_sha256=digest(source_block), current_block_sha256=digest(old_block),
            review=dict.fromkeys(GATES, True))
        if n in REVISION:
            compile_revision(row, phrases)
        rows.append(row)
    assert len(rows) == 8 and sum(row['decision'] == 'revision' for row in rows) == 4
    pictures = validate_pages(ctx, rows)
    path, packed = next(transform(ctx.image, rows))
    new = IlnkContainer.parse(packed).blocks
    assert [i for i, (a, b) in enumerate(zip(banks[3], new, strict=True)) if a != b] == [block]
    final_commands, final = raw_speeches(ctx.arm, new[block], inv)
    changed = set()
    inverse = bytearray(new[block])
    for row in rows:
        if row['decision'] == 'revision':
            ref = row['current_reference']
            changed.update((ref['command_offset'], *ref['ancestors']))
            pos = ref['offset']
            previous = bytes.fromhex(row['current_hex'])
            inverse[pos:pos + len(previous)] = previous
    assert inverse == old_block
    for a, b in zip(commands, final_commands, strict=True):
        assert all(a[key] == b[key] for key in ('offset', 'word', 'native_extent', 'ancestor_0100_offsets'))
        assert (a['whole_command_hex'] != b['whole_command_hex']) == (a['offset'] in changed)
    for row, final_ref in zip(rows, references(final_commands, final), strict=True):
        assert final_ref['complete_preamble_hex'] == row['current_reference']['complete_preamble_hex']
        assert final_ref['raw_hex'] == row.get('target_hex', row['current_hex'])
        row['staged_reference'] = final_ref | {'block_sha256': digest(new[block])}
    assert catalogue(ctx.arm, config, [*banks[:3], new]) == catalog
    image = base.NdsImage.open(parent.ROM)
    before = files(image)
    image.replace_file(path, packed)
    after = files(image)
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {FILE}
    ROOT.mkdir(parents=True)
    image.save(ROM)
    image.replace_file(FILE, before[FILE])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    candidate = base.digest(ROM)
    collect = FunctionType(layout.contact_sheets.__code__, vars(layout) | {'ROOT': ROOT})
    base.save(MANUSCRIPT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=list(GATES), candidate_sha256=candidate,
        previous_sha256=release['candidate_sha256'], records=rows))
    base.save(STORED, dict(candidate_sha256=candidate, previous_sha256=release['candidate_sha256'],
        target_ARM9_sha256=digest(ctx.arm), target_story_archive_sha256={FILE: digest(packed)}, whole_parent_inverse=True,
        sheets=collect(pictures), preview_count=len(pictures), manuscript_sha256=base.digest(MANUSCRIPT),
        observation=str(OBSERVATION), observation_sha256=base.digest(OBSERVATION)))
    print('Staged four revisions and four retentions with 22 complete native previews.')


if __name__ == '__main__':
    main()
