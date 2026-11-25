"""Bind current mixed-width leads to source dialogue and the installed catalogue."""

import re
from collections import Counter
from dataclasses import asdict
from hashlib import sha256
from pathlib import Path
from struct import pack, unpack_from

from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R1, UC_ARM_REG_SP

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.confirmed_name_message_catalog import CALLS, MACRO
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, cache_plan, target
from dk4tool.patch.reviewed_name_catalog import ROUTE, helper
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import register_forces_relationships_20261115 as current
from scripts.audit_story_glyph_consistency import independent_pixels
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.scan_completed_contraction_wraps_v7831 import raw_speeches
from scripts.verify_name_catalog_glyphs_v278 import raster
from scripts.verify_ordinary_name_fidelity_research import initialized


COMMON, ARM = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/story_glyph_consistency_20261115_v1.json')
HEADER = re.compile(rb'\x00\x40\xff\xff\x00.[^\0]*?(?=\x00)', re.DOTALL)
ASCII = re.compile('[A-Za-z]')
WIDE = re.compile('[Ａ-Ｚａ-ｚ]')
JAPANESE = re.compile('[ぁ-ゖァ-ヺ一-龯]')
RETENTIONS = {
    (0, 154, 138): 'The companion trails off after the account of abuse, giving Rafael room to respond. Keep the name substitution and pause.',
    (0, 159, 38): 'Arcadius notices Rafael is uneasy and waits for him to explain. Keep the unfinished address and its pause.',
    (1, 40, 99): 'The surrounding exclamations use symbols for speech the crew cannot understand. Keep the recognizably opaque outburst and its emphatic punctuation.',
    (1, 49, 66): 'Hodram hesitates and qualifies his refusal after Lil challenges his reaction to the swap. Keep the reluctant double negative and opening pause.',
    (1, 62, 118): 'Sera trails off as she takes in Hodram’s kindness about her memory and his praise of her cooking. Keep the address and pause.',
    (1, 80, 26): 'The speaker calls out to the captain, then bursts into speech represented by opaque symbols in Japanese. Keep both the name substitution and the visible distinction.',
    (1, 81, 47): 'Sera pauses after Hodram recognizes that someone from her village is directing the construction. Keep the brief address and pause.',
    (1, 82, 41): 'Sera pauses as Hodram explains how investment could help the village. Keep the brief address and leave her response implicit.',
    (3, 35, 17): 'Maria answers Hodram’s question about her identity with a guarded counterquestion. Keep the short pause before she answers.',
    (3, 35, 53): 'Maria weighs talking to Camille. Keep the tentative wording and pause before she commits to an answer.',
    (3, 35, 100): 'Camille struggles to say she cannot see Lil right now. Keep the hesitation and unfinished ending without implying a permanent refusal.',
    (3, 35, 103): 'Hodram pauses, accepts Camille’s decision and gives her space. Keep the measured response.',
    (3, 108, 88): 'Maria presses the informant for the plan and promises safety. Keep the deliberate pause before the direct request.',
    (3, 108, 114): 'Xien works out what Kuhn is counting on after the informant speaks. Keep the opening pause and the distinction between inference and testimony.',
}
LETTER_RETENTIONS = {
    (0, 166, 791): ('166_B167', 117, 'Keep Charlotte’s halting Portuguese as written. The indented line continues the separate pronunciation aid.'),
    (0, 166, 794): ('166_B167', 118, 'Keep Charlotte’s second Portuguese line, its pronunciation aid and the separately indented signature.'),
    (0, 166, 797): ('166_B167', 119, 'Keep the translated letter’s opening name substitution, two distinct thanks and separately indented signature.'),
    (0, 216, 74): ('201_B220', 320, 'Keep Jam’s informal farewell and the separately indented signature, using the established full name.'),
}
COMMAND_MATCHES = {(0, 306, 1009): b'CCb\x81C', (2, 26, 3070): b'Bb\x81C', (3, 49, 3529): b'CDb\x81C'}


def digest(raw):
    return sha256(raw).hexdigest()


def decoded(raw):
    try:
        return raw.decode('cp932')
    except UnicodeDecodeError:
        return ''


def mixed(text):
    return ASCII.search(text) is not None and any(ord(char) > 127 for char in text)


def catalogue(arm, config, archives):
    plan = cache_plan(arm)
    assert plan and plan['pool_span'][0] == POOL
    payload = bytes(MainCodeFile(arm, BASE).sections[3].data[:-48])
    rows, entry, table = (config[key] for key in ('records', 'entry', 'table'))
    assert len(payload) == plan['payload_bytes'] and len(rows) == config['unique_route_scoped_keys'] == 467
    assert all(target(arm, field) == entry for field in CALLS)
    code = helper(entry, table, len(rows))
    assert payload[entry - POOL:entry - POOL + len(code)] == code
    # Join blocks with a marker that cannot occur in any catalogue key or its NUL terminator.
    assert not any(b'\xff' in bytes.fromhex(row['key_hex']) for row in rows)
    stores = [b'\xff'.join(blocks) for blocks in archives]
    wide_rows, matches = [], []
    for index, row in enumerate(rows):
        key = bytes.fromhex(row['key_hex']) + b'\0'
        replacement = bytes.fromhex(row['target_hex']) + b'\0'
        key_at, target_at, size, mask = unpack_from('<4I', payload, table - POOL + 16 * index)
        assert (key_at, target_at, size, mask) == (row['key_pointer'], row['target_pointer'], len(key), row['route_mask'])
        assert payload[key_at - POOL:key_at - POOL + size] == key
        assert payload[target_at - POOL:target_at - POOL + len(replacement)] == replacement
        routes = [route for route, stored in enumerate(stores) if mask & (1 << route) and key in stored]
        if WIDE.search(decoded(replacement)):
            assert not routes, (row, routes)
            wide_rows.append(dict(index=index, **row))
        elif routes:
            matches.append(dict(index=index, routes=routes, **row))
    return dict(entry=entry, table=table, helper_sha256=digest(code), startup_payload_sha256=digest(payload),
                total_rows=len(rows), wide_rows_without_stored_route_key=wide_rows, other_rows_with_stored_key=matches)


def lookup_cases(arm, catalogue_result, julio):
    cpu = initialized(arm)
    entry = catalogue_result['entry']
    historical = next(row for row in catalogue_result['wide_rows_without_stored_route_key']
                      if any(owner['owner'] == ['/data/SC0.DK4', 'DK4_MES_B43_R0017'] for owner in row['requests']))
    cases = [('corrected whole', julio, 0, None), ('corrected body', julio[1:], 0, None),
             ('historical positive control', bytes.fromhex(historical['key_hex']), 0, historical['target_pointer'])]
    results = []
    for label, raw, route, expected in cases:
        for alignment in range(4):
            address = 0x02468020 + alignment
            guarded = b'\xa5' * 16 + raw + b'\0' + b'\xa5' * 16
            cpu.mem_write(address - 16, guarded)
            cpu.mem_write(ROUTE, pack('<I', route))
            cpu.reg_write(UC_ARM_REG_R1, address)
            cpu.reg_write(UC_ARM_REG_LR, BASE + CALLS[0] + 4)
            cpu.reg_write(UC_ARM_REG_SP, 0x027F0000)
            cpu.emu_start(entry, MACRO, count=1000000)
            assert cpu.reg_read(UC_ARM_REG_PC) == MACRO and cpu.reg_read(UC_ARM_REG_R1) == (expected or address)
            assert bytes(cpu.mem_read(address - 16, len(guarded))) == guarded
            results.append(dict(case=label, alignment=alignment, catalogue_replacement_selected=expected is not None))
    return results


def review_story(images, arms, archives, bindings):
    inventory, _, _ = scoped_inventory()
    review = []
    for route, block, record in (*RETENTIONS, *LETTER_RETENTIONS, (0, 43, 17)):
        path = f'/data/SC{route}.DK4'
        old = IlnkContainer.parse(images[0].read_file(path)).blocks[block]
        new = archives[route][block]
        source, installed = [raw_speeches(arm, data, inventory)[1] for arm, data in ((arms[0], old), (arms[1], new))]
        ordinal = next(i for i, row in enumerate(installed) if row['record_index'] == record)
        assert len(source) == len(installed)
        assert [r['complete_preamble_hex'] for r in source] == [r['complete_preamble_hex'] for r in installed]
        context = []
        for before, after in zip(source[max(0, ordinal-2):ordinal+3], installed[max(0, ordinal-2):ordinal+3], strict=True):
            japanese = bytes.fromhex(before['raw_hex'])[1:].decode('cp932')
            english = bytes.fromhex(after['raw_hex'])[1:].decode('cp932')
            context.append(dict(source=before, current=after, Japanese=japanese, English=english,
                                selected=after['record_index'] == record))
        selected = next(row for row in context if row['selected'])
        if (route, block, record) == (0, 43, 17):
            raw = bytes.fromhex(selected['current']['raw_hex'])
            assert raw[:2] == b'\x06F' and raw.count(b'FI') == 1
            assert b"It can't choose where" in raw and raw[1:].isascii()
            preview = raw[1:].replace(b'FI', b'Rafael')
            pixels, events, font = raster(arms[1], preview)
            assert pixels == independent_pixels(arms[1], font, events)
            assert events[0]['code'] == ord('F') and all(event['kind'] == 'ascii' for event in events)
            assert len({event['y'] for event in events}) == 4
            julio = dict(file=path, block=block, clean_block_sha256=digest(old), current_block_sha256=digest(new),
                         exchange_context=context, lookups=lookup_cases(arms[1], bindings, raw), rows=4,
                         supplied_preview_substitution='Rafael', native_pixels_sha256=digest(pixels),
                         earlier_initialized_gameplay='docs/editorial_hodram_julio_release_20261101.md')
            continue
        key = (route, block, record)
        prior = None
        if key in LETTER_RETENTIONS:
            family, index, reason = LETTER_RETENTIONS[key]
            receipt = Path(f'translations/rafael_B{family}_integrated_final_review_v1.json')
            record_review = current.base.load(receipt)['records'][index]
            assert all(record_review['review'].values()) and len(record_review['review']) == 5
            assert record_review['actual_utterance_observed_in_disclosed_fixture']
            expected = record_review['planned_integrated_reference']['exact_stored_hex']
            assert selected['current']['raw_hex'] == expected and selected['current']['selector'] == 254
            assert selected['source']['raw_hex'] == record_review['source_hex'].lower()
            prior = dict(receipt=str(receipt), sha256=current.base.digest(receipt), record_index=index,
                         id=record_review['id'], gates=record_review['review'], initialized_fixture_observed=True)
        else:
            reason = RETENTIONS[key]
        assert selected['source']['selector'] == selected['current']['selector']
        review.append(dict(file=path, block=block, clean_block_sha256=digest(old), current_block_sha256=digest(new),
                           decision='retain', reason=reason, exchange_context=context, exact_prior_letter_review=prior))
    return review, julio


def main():
    base = current.base
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release['candidate_sha256']
    assert base.digest(current.stage.CLEAN) == release['clean_input_sha256']
    assert base.digest(current.MANIFEST) == release['manifest_sha256']
    images = [base.NdsImage.open(path) for path in (current.stage.CLEAN, current.ROM)]
    arms = [image.read_file(ARM) for image in images]
    archives = [IlnkContainer.parse(images[1].read_file(f'/data/SC{route}.DK4')).blocks for route in range(4)]
    catalog = base.load(current.MANIFEST)['relocations'][ARM]['reviewed_name_integration']['catalog']
    bound_catalogue = catalogue(arms[1], catalog, archives)
    review, julio = review_story(images, arms, archives, bound_catalogue)

    counts, mixed_keys, language_keys = Counter(), set(), set()
    for route, blocks in enumerate(archives):
        for block, blob in enumerate(blocks):
            for match in HEADER.finditer(blob):
                selector_offset = match.start() + 5
                text = decoded(match[0][6:])
                counts['header-shaped matches'] += 1
                if not text:
                    counts['empty or undecodable'] += 1
                    continue
                assert not WIDE.search(text), (route, block, selector_offset, text)
                if any(ord(char) > 127 for char in text):
                    counts['non-ASCII body candidates'] += 1
                key = (route, block, blob[:selector_offset].count(b'\0'))
                if mixed(text):
                    mixed_keys.add(key)
                if JAPANESE.search(text):
                    language_keys.add(key)
    reviewed = RETENTIONS.keys() | LETTER_RETENTIONS.keys()
    found = mixed_keys | language_keys
    assert found == reviewed, (sorted(found - reviewed), sorted(reviewed - found))

    inventory, _, _ = scoped_inventory()
    command_results = []
    for (route, block, offset), raw in COMMAND_MATCHES.items():
        data = archives[route][block]
        assert data[offset:offset + len(raw) + 1] == raw + b'\0'
        commands, _ = raw_speeches(arms[1], data, inventory)
        covered = [row for row in commands if row['word'] != 0x0100 and
                   row['offset'] < offset + len(raw) and offset < row['offset'] + row['native_extent']]
        assert covered and all(row['word'] != 0x4000 for row in covered)
        covered_offsets = {byte for row in covered for byte in range(row['offset'], row['offset'] + row['native_extent'])}
        assert set(range(offset, offset + len(raw))) <= covered_offsets
        command_results.append(dict(file=f'/data/SC{route}.DK4', block=block, block_sha256=digest(data),
                                    apparent_offset=offset, apparent_text=raw.decode('cp932'), commands=covered))

    source_common, installed_common = [image.read_file(COMMON) for image in images]
    native = owned_entries(installed_common, arms[1], digest(arms[1][DIRECTORY_OFFSET:TABLE_OFFSET]))
    assert len(native) == 3668
    common_leads = [row for row in native if mixed(decoded(row.text))]
    assert [row.message_id for row in common_leads] == [318]
    old = common_message_entries(source_common, arms[0])[318]
    new, = common_leads
    common = dict(file=COMMON, source=asdict(old), current=asdict(new),
                  decision='pending consumer identification',
                  earlier_evidence='docs/editorial_grand_race_stopping_registered_20261114.md')
    for mode, row in (('source', old), ('current', new)):
        common[mode]['text'] = row.text.decode('cp932')
        common[mode]['bytes_hex'] = row.text.hex()
    base.save(OUTPUT, dict(candidate=str(current.ROM), candidate_sha256=release['candidate_sha256'],
                          clean_sha256=release['clean_input_sha256'], current_ARM9_sha256=digest(arms[1]),
                          manifest_sha256=release['manifest_sha256'], story_signature_counts=dict(counts),
                          scope='Stored 0040ffff00 speaker and FE bodies; typed inventory for individually reviewed records. Catalogue matches are exact direct stored suffixes by route. Independent text stores and synthesized callers require separate checks.',
                          source_bound_glyph_retentions=review, bytes_owned_by_commands=command_results,
                          julio_tutorial=julio, catalogue=bound_catalogue, common_rows_checked=len(native),
                          common_lead=common, additional_editorial_credit=0, new_gameplay_runs=0))
    print(dict(counts, native_retentions=len(review), command_patterns=len(command_results),
               catalogue_positive_key_rows=len(bound_catalogue['other_rows_with_stored_key']),
               wide_catalogue_rows=len(bound_catalogue['wide_rows_without_stored_route_key']),
               julio_lookup_cases=len(julio['lookups']), shared_mixed_leads=[318]))


if __name__ == '__main__':
    main()
