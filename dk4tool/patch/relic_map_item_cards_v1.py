"""Pack the reviewed proof and map cards with the established item display metrics."""

from types import FunctionType

from dk4tool.patch.reviewed_item_cards import item_table, replace_category
from dk4tool.patch.utility_weapon_item_cards_v1 import compile_item as previous_format

PHRASES = (
    'Norse god of hunting', 'Achaemenid realm', '5th century BC', 'solid gold seal',
    'precursor to Ethiopia', '2nd-6th centuries', '15th-10th centuries BC',
    'Indian thought', 'early Aryan life', 'every islander', '3rd century BC', 'Qin Shi Huang',
    'stone tablet', 'lotus leaf', 'never withers', 'knife blade', 'southern England',
    'ancient Roman capital', 'hidden Christian village', 'King\'s Mosque', 'Mughal Empire',
    'northern India', 'Cambodian dynasty', 'northern China', "great king's tomb",
    'legendary temple', 'distant island', 'ancient city', 'in ruins', 'cultural roots',
    'Aztec kingdom', 'mysterious design', 'ancient times', 'Tang dynasty',
    'New World dynasty', 'milky white liquid', 'sun emblem', 'ancient kingdom', 'No one knows',
)
compile_item = FunctionType(previous_format.__code__, previous_format.__globals__ | {
    'PROTECTED_PHRASES': previous_format.__globals__['PROTECTED_PHRASES'] + PHRASES,
})


def transform(source, records, table, pointers, payload):
    return replace_category(source, records, table, pointers, payload,
                            first=148, end=188, compile_paragraph=compile_item)
