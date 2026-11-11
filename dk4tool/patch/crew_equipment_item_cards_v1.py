"""Use the registered item formatter and fixed main cache allocation for crew equipment."""

from types import FunctionType

from dk4tool.patch.reviewed_item_cards import item_table, replace_category
from dk4tool.patch.utility_weapon_item_cards_v1 import compile_item as previous_format

PHRASES = (
    'raise or lower', 'Milky Way', 'night sky', 'a young woman', '1,001 nights',
    'around the world', 'spared no expense', 'divine favor', 'veteran navigator', 'life story',
    'Marco Polo', 'the 13th century', 'saw and heard', 'advance or withdraw', 'god of the sea',
    'first century BC', 'fourth century BC', 'king of Macedon', 'against the Gauls',
    'the age of myth', 'throne room', 'ancient Greek sculptor', 'Hellenistic age', 'Leonardo da Vinci',
    'Muslim world', 'hearth goddess', 'Livestock Room', 'Pope Gregory VII', '11th century',
    'at sea', 'Gupta dynasty', 'Carthaginian general', 'famous Muslim merchant',
    'For some reason', 'before the Common Era', 'mysterious bracelet', 'inspire them to act',
    'tall tale', 'in the East', 'never chips', 'rough sailors', 'by hand', 'difficult passages',
    'It is said', 'years underground', 'without the slightest error',
)
compile_item = FunctionType(previous_format.__code__, previous_format.__globals__ | {
    'PROTECTED_PHRASES': previous_format.__globals__['PROTECTED_PHRASES'] + PHRASES,
})


def transform(source, records, table, pointers, payload):
    return replace_category(source, records, table, pointers, payload,
                            first=74, end=114, compile_paragraph=compile_item)
