"""Check the original provider and caption planes for the nine B201–B220 binary menus."""
from scripts import check_rafael_two_choice_batch_v2 as previous
from scripts.plan_rafael_B201_B220_v1 import TWO_MENUS
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    "    assert groups and all(len(rows) == 2 for rows in groups.values())":
        "    assert set(groups) == TWO_MENUS and all(len(rows) == 2 for rows in groups.values())",
})
exec(compile(source, __file__ + '::same-native-two-choice-providers-and-planes', 'exec'), globals())

