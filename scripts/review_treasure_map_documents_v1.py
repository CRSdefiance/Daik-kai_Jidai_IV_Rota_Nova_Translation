"""Review the full native Ancient Map document across its four display fields."""

from collections import Counter
from hashlib import sha256
from pathlib import Path
from struct import unpack_from
from unicodedata import normalize

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import stage_arrival_month_labels_v1 as label
from scripts.probe_common_display_name_hook import branch_link
from scripts.seal_shared_text_source_v1 import reference


base, BASE, ARM, COMMON, CLEAN = label.base, label.BASE, label.ARM, label.COMMON, label.CLEAN
SOURCE = Path('translations/common_b39_treasure_clues_manuscript_v2.json')
OUTPUT = label.review.prior.ROOT / 'treasure_map_documents_context_v1.json'
GATES = ('source', 'context', 'localization', 'naturalness', 'formatting')
CALLS = {
    'artifact_lore': (0x103384, 0x10338C, 0x103398, 0x10355C, 0x12F6FC, 3648, 3657),
    'sea_region': (0x1033DC, 0x1033E4, 0x1033F0, 0x103560, 0x12F724, 3608, 3627),
    'direction': (0x103424, 0x10342C, 0x103438, 0x103564, 0x12F774, 3628, 3647),
    'cross_instruction': (0x103464, 0x10346C, 0x103478, 0x103568, 0x12F660, 3607, 3607),
}
CONTEXT = {
    'artifact_lore': 'The clue document describes the artifact in an inscription. The native view chooses this field with the second document index. Preserve the distinction between an asserted property and a legend about it.',
    'sea_region': 'The clue document gives a sea-region lead using the first document index. Some maps identify where the treasure lies. Others give the waters to depart from before following the direction clue.',
    'direction': 'The clue document gives a direction using the same index as the sea-region lead. Its distance and orientation qualify that lead. A relative position and an instruction to travel serve different functions.',
    'cross_instruction': 'The clue document tells the player to search the location marked with an X when this field is visible.',
}
DECISIONS = {
    3607: (None, 'Keep the imperative and the exact X marker.'),
    3608: (None, 'Keep the hidden treasure in New World waters.'),
    3609: (None, 'Keep the same wording in this second native slot with the same Japanese clue.'),
    3610: ('Set sail from New World waters if you seek the treasure.', 'Keep the waters as the point of departure and the conditional address to the reader.'),
    3611: (None, 'Keep the North Sea as the starting point for the search.'),
    3612: (None, 'Keep the North Sea as the sea containing the hidden treasure.'),
    3613: (None, 'Keep the second North Sea departure clue in the same wording as its source duplicate.'),
    3614: (None, 'Keep the Mediterranean as the departure point in the conditional instruction.'),
    3615: (None, 'Keep the treasure in Mediterranean waters and the measured inscription voice.'),
    3616: (None, 'Keep the treasure in African waters.'),
    3617: (None, 'Keep the repeated North Sea location consistent with its companion slot.'),
    3618: (None, 'Keep the repeated Mediterranean location in the same words.'),
    3619: (None, 'Keep the African-waters location in this separate map slot.'),
    3620: (None, 'Keep the same African-waters clue and leave the distinction to the direction field.'),
    3621: (None, 'Keep the common African-waters clue in this map slot.'),
    3622: (None, 'Keep the Indian Ocean location and use a standard Latin I.'),
    3623: (None, 'Keep the same Indian Ocean wording in this second slot with a standard Latin I.'),
    3624: (None, 'Keep the treasure in the seas of Southeast Asia.'),
    3625: ('Set sail from Southeast Asian waters if you seek the treasure.', 'Name the waters as the starting point of this voyage.'),
    3626: (None, 'Keep the same Southeast Asian location wording in this separate map slot.'),
    3627: (None, 'Keep the treasure in East Asian waters.'),
    3628: (None, 'Keep the short offset north of the paired New World location.'),
    3629: (None, 'Keep the reference to the center of the paired New World waters.'),
    3630: (None, 'Keep the far northeast voyage from the New World departure clue.'),
    3631: (None, 'Keep the far northwest voyage from the North Sea departure clue.'),
    3632: (None, 'Keep the northwest position relative to the paired North Sea location.'),
    3633: (None, 'Keep the far north voyage from the paired North Sea departure clue.'),
    3634: (None, 'Keep the far west voyage from the Mediterranean.'),
    3635: (None, 'Keep the northwest position relative to the Mediterranean clue.'),
    3636: (None, 'Keep the same northwest wording for this distinct African-waters map.'),
    3637: (None, 'Keep the center of the North Sea region in this pairing.'),
    3638: (None, 'Keep the center of the Mediterranean in this pairing.'),
    3639: (None, 'Keep the center of African waters in this pairing.'),
    3640: (None, 'Keep the slight southerly offset from the paired African-waters location.'),
    3641: (None, 'Keep the southeast position relative to the paired African-waters location.'),
    3642: (None, 'Keep the western position relative to the paired Indian Ocean location.'),
    3643: (None, 'Keep the precise due-south bearing from the paired Indian Ocean clue.'),
    3644: (None, 'Keep the slight westerly offset from the paired Southeast Asian seas.'),
    3645: (None, 'Keep the far south voyage from the Southeast Asian departure clue.'),
    3646: (None, 'Keep the slight southerly offset from the paired Southeast Asian waters.'),
    3647: (None, 'Keep the northeast position relative to East Asian waters.'),
    3648: (None, 'Keep the talisman, the lion’s strength and the formidable foes. Use a standard Latin I.'),
    3649: ('This weapon banishes evil. In ages past, it was used in rites to drive out demons.', 'Keep the two claims and give the old inscription a natural cadence.'),
    3650: (None, 'Keep the serpent deity, the warriors and the attribution of the protective power. Use a standard Latin I.'),
    3651: ('This treasure belonged to a marksman who fired magic bullets. They say its bearer never misses.', 'Attribute magic to the bullets and keep the perfect aim as a report.'),
    3652: (None, 'Keep the strength of mind and the story of the fortune without asserting it as fact.'),
    3653: (None, 'Keep the weapon’s fearsome reputation and its legendary ability to cut without contact. Use a standard Latin I.'),
    3654: ('A symbol of destruction. Its magic sank every ship that opposed it.', 'Separate the inscription’s title-like description from the claim about what the magic did.'),
    3655: (None, 'Keep the horn’s unusual shape and the claim that it repels every disease.'),
    3656: (None, 'Keep the royal shield, the goddess’s blessing and protection from misfortune.'),
    3657: ('A great red spear with the power to drive evil away.', 'Keep the spear’s color, size and power in a natural inscription.'),
}


def native_tables(clean, current):
    result = {}
    for kind, (load, lookup, draw, pool, table, first, last) in CALLS.items():
        count = last - first + 1
        assert unpack_from('<I', clean, pool)[0] == unpack_from('<I', current, pool)[0] == BASE + table
        assert unpack_from(f'<{count}I', clean, table) == tuple(range(first, last + 1))
        assert clean[table:table + count * 4] == current[table:table + count * 4]
        bound = clean[load:draw + 4]
        assert current[load:draw + 4] == bound
        assert unpack_from('<I', bound, lookup - load)[0] == branch_link(BASE + lookup, BASE + 0x5528C)
        assert unpack_from('<I', bound, draw - load)[0] == branch_link(BASE + draw, label.RENDERER)
        result[kind] = dict(table=BASE + table, literal_address=BASE + pool, original_load=BASE + load,
            original_lookup=BASE + lookup, original_renderer_call=BASE + draw, code_hex=bound.hex(),
            ids=list(range(first, last + 1)), context=CONTEXT[kind])
    return result


def main():
    assert not OUTPUT.exists()
    proof = base.load(label.PROOF)
    assert base.digest(label.ROM) == proof['research_ROM_sha256']
    clean, current = map(base.NdsImage.open, (CLEAN, label.ROM))
    ca, arm = clean.read_file(ARM), current.read_file(ARM)
    assert sha256(current.read_file(COMMON)).hexdigest() == proof['research_COMMON_sha256']
    source = common_message_entries(clean.read_file(COMMON), ca)
    existing = owned_entries(current.read_file(COMMON), arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    tables = native_tables(ca, arm)
    prior = {row['message_id']: row for row in base.load(SOURCE)['records']}
    ledger = base.load(base.LEDGER)
    credits = {row['id'] for row in ledger[base.CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}
    records = []
    for number, (replacement, reason) in DECISIONS.items():
        japanese, before = source[number], existing[number]
        historical = prior[number]
        assert japanese.text.hex() == historical['source_hex'].lower()
        field, = [field for field, table in tables.items() if number in table['ids']]
        old = before.text.decode('cp932')
        logical = ' '.join(normalize('NFKC', old).split())
        english = replacement or logical
        assert english.isascii() and (english != logical) == bool(replacement)
        assert b'%' not in japanese.text and b'%' not in before.text and '%' not in english
        key = f'COMMON_MESSAGE_{number}'
        assert key not in credits
        records.append(dict(id=key, message_ID=number, file_path=COMMON, source_reference=reference(japanese),
            current_reference=reference(before), source_Japanese=japanese.text.decode('cp932'),
            current_English=old, source_hex=japanese.text.hex(), current_hex=before.text.hex(),
            english=english, speaker='Ancient Map inscription', context=CONTEXT[field], native_field=field,
            source_meaning=historical['source_meaning'], localization_note=reason,
            decision='revision' if replacement else 'retention', original_substitution_count=0,
            review={gate: gate != 'formatting' for gate in GATES}))
    assert [row['message_ID'] for row in records] == list(range(3607, 3658))
    pairs = [dict(document_index=i, sea_region=sea, direction=direction)
             for i, (sea, direction) in enumerate(zip(tables['sea_region']['ids'], tables['direction']['ids'], strict=True))]
    counts = dict(Counter(row['decision'] for row in records))
    base.save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=GATES, records=records, counts=counts,
        native_fields=tables, original_region_direction_pairs=pairs,
        artifact_lore_has_independent_native_index=True, clean_ROM_sha256=base.digest(CLEAN),
        current_ROM_sha256=proof['research_ROM_sha256'], current_COMMON_sha256=proof['research_COMMON_sha256'],
        previous_manuscript_sha256=base.digest(SOURCE), new_credit=0, formatting_pending=True,
        gameplay_pending=True, full_goal_complete=False))
    print(f'{len(records)} Ancient Map decisions {counts} with all {len(pairs)} original clue pairings.')


if __name__ == '__main__':
    main()
