"""Match item titles to their exact prior native crops in the same saved context."""

from pathlib import Path
from types import FunctionType

from scripts import verify_figurehead_navigation_gift_advice_v1 as previous


REFERENCE = Path('releases/all_routes_editorial_20261111_figurehead_navigation_gift_cards_candidate'
                 '/verification/figurehead_navigation_gift_gameplay_verification.json')


def item_fields(font, image, number):
    earlier = previous.stage.load(REFERENCE)
    assert earlier['original_Items_screen'] and earlier['complete_description_foreground_and_blank_cells_exact']
    card = earlier['observed'][str(number - 218)]
    frame = card['capture_frames'][0]
    title = next(row for row in card['title_role_effect_and_description_fields']
                 if row['native_source_origin'] == [48, 0] and row['frame'] == frame['frame'])
    x, y = title['destination']
    width, height = title['size']
    assert [x, y, width, height] == [56, 24, 144, 12]
    crop = (x, y, x + width, y + height)
    expected = previous.precedent.portrait.captured(frame).crop(crop)
    assert image.crop(crop).tobytes() == expected.tobytes()
    action = {3158: 'Remove', 3147: 'Equip'}.get(number)
    footer = (102, 365, 160, 384) if action else (152, 365, 209, 384)
    fields = [
        dict(text=previous.ITEM_NAMES[number], crop=crop, exact_registered_card_title=title,
             reference=str(REFERENCE), reference_sha256=previous.stage.digest(REFERENCE),
             exact_reference_capture=frame),
        previous.precedent.find_mask(font, 'Advice', image, footer),
    ]
    if action:
        fields.append(previous.precedent.find_mask(font, action, image, (160, 365, 211, 384)))
    return fields


if __name__ == '__main__':
    FunctionType(previous.verify_live.__code__, vars(previous) | globals())()
