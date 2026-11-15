"""Store the new catalogue prose while preserving the registered Shachihoko record."""

from hashlib import sha256
import inspect
from types import FunctionType

from ndspy.code import MainCodeFile

from dk4tool.patch import reviewed_item_cards as storage
from dk4tool.patch.utility_weapon_item_cards_v1 import compile_item as previous_format
from scripts.source_locked_derivation_v5118 import checked_text

FIRST, SHACHIHOKO, END = 114, 116, 148
item_table = storage.item_table
PHRASES = (
    'swift flight', 'For some reason', 'white whale', 'stay afloat', 'cannon fire',
    'open sea', 'delicate beauty', 'demon\'s curse', 'lifts the spirits', "Heaven's protection",
    'finding your bearings', 'your position at sea', 'Hellenistic astronomer',
    'living bloom', 'keep secret', 'gold bars', 'bread dough', 'Northern Song emperor',
    'painting and calligraphy', 'ancient Greek', 'Korean Peninsula', 'ceramic beads',
    'celestial maiden', 'fourth century', 'vivid blue mottling', 'large sunflower',
    'pure white cloth', 'Goryeo celadon', "It's said", 'Its beauty', 'refined upbringing', "world's largest lens", 'human speech',
)
compile_item = FunctionType(previous_format.__code__, previous_format.__globals__ | {
    'PROTECTED_PHRASES': previous_format.__globals__['PROTECTED_PHRASES'] + PHRASES,
})
first_source = checked_text(inspect.getsource(storage.replace_category), {
    'start, limit = pointers[first] - POOL, pointers[end] - POOL':
        """start = pointers[first] - POOL
    limit = pointers[end - 1] - POOL + len(bytes.fromhex(records[-1]['prior_private_hex']))""",
    '        assert start <= offset < pointers[ident + 1] - POOL <= limit':
        """        following = limit if ident + 1 == end else pointers[ident + 1] - POOL
        assert start <= offset < following <= limit""",
    'payload[offset:pointers[ident + 1] - POOL]': 'payload[offset:following]',
})
env = vars(storage) | globals()
exec(compile(first_source, __file__ + '::first-figurehead-owned-span', 'exec'), env)
replace_prefix = env['replace_category']


def transform(source, records, table, pointers, payload):
    assert tuple(row['item_ID'] for row in records) == tuple(i for i in range(FIRST, END) if i != SHACHIHOKO)
    original = MainCodeFile(source, storage.BASE)
    source_resident = bytes(original.sections[5].data)
    first, first_proof = replace_prefix(source, records[:2], table, pointers, payload,
        first=FIRST, end=SHACHIHOKO, compile_paragraph=compile_item)
    mid_payload, mid_table, mid_pointers = item_table(first)
    assert table == mid_table and pointers[SHACHIHOKO:] == mid_pointers[SHACHIHOKO:]
    target, second_proof = storage.replace_category(first, records[2:], table, mid_pointers, mid_payload,
        first=SHACHIHOKO + 1, end=END, compile_paragraph=compile_item)
    new_payload, new_table, new_pointers = item_table(target)
    assert table == new_table and new_pointers[SHACHIHOKO] == pointers[SHACHIHOKO]
    shachihoko, _ = storage.item_paragraph(payload, pointers[SHACHIHOKO])
    assert storage.item_paragraph(new_payload, new_pointers[SHACHIHOKO])[0] == shachihoko

    restored = MainCodeFile(target, storage.BASE)
    active_fields, spans = [], []
    for run, a, b in ((first_proof, FIRST, SHACHIHOKO), (second_proof, SHACHIHOKO + 1, END)):
        low, high = run['selected_original_text_span']
        spans.append([low, high])
        active_fields.append([table + 4 * a, table + 4 * b])
        for start, end in ((low, high), active_fields[-1]):
            lo, hi = start - storage.POOL, end - storage.POOL
            restored.sections[3].data[lo:hi] = original.sections[3].data[lo:hi]
    assert new_payload[spans[0][1] - storage.POOL:spans[1][0] - storage.POOL] == \
        payload[spans[0][1] - storage.POOL:spans[1][0] - storage.POOL]
    resident = bytes(restored.sections[5].data)
    restored.sections[5].data = bytearray(source_resident)
    assert bytes(restored.save()) == source
    return target, dict(
        old_payload_bytes=len(payload), new_payload_bytes=len(payload), new_cache_plan=storage.cache_plan(target),
        item_paragraphs=first_proof['item_paragraphs'] + second_proof['item_paragraphs'],
        exact_parent_ARM9_inverse=True, main_pool_geometry_and_startup_exact=True,
        selected_original_text_spans=spans, selected_pointer_field_spans=active_fields,
        preserved_Shachihoko=dict(message_ID=2931, item_ID=SHACHIHOKO,
            pointer=pointers[SHACHIHOKO], pointer_field=table + 4 * SHACHIHOKO, private_hex=shachihoko.hex()),
        appended_resident_text_span=[storage.RESIDENT_BASE + len(source_resident),
                                     storage.RESIDENT_BASE + len(resident)],
        appended_resident_text_sha256=sha256(resident[len(source_resident):]).hexdigest(),
        active_pointer_fields=len(records),
    )
