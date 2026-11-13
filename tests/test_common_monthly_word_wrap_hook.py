import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_common_monthly_tribute_preparation import execute
from scripts.probe_common_monthly_word_wrap_hook import caller_frame, prepare
from scripts.probe_common_tribute_loaded_copy import research_dataset


@pytest.mark.parametrize('parent,table,active', [
    (0x02053F40, 0x021189C0, True),
    (0x02053F40, 0x021189E0, False),
    (0x02054014, 0x021189C0, False),
])
def test_monthly_scope_preserves_other_portrait_paths(parent, table, active):
    source = NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')
    saved, _ = prepare(source)
    result = execute(saved, "This month's tribute is %s gold coins. Please accept it.", 999999, 1,
                     word_wrapped=active, parent_return=parent, selector_table=table)
    assert result['word_wrapper_invoked'] == active


def test_actual_selector_fallback_reaches_hook_with_intact_caller_state():
    source = NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')
    saved, _ = prepare(source)
    dataset = research_dataset(saved)
    result = caller_frame(dataset.arm9, dataset.common, 6)
    assert result['selected_text'] == "This month's tribute is %s gold coins. Please accept it."
    assert result['complete_prepared_text'].replace('\n  ', ' ') == "This month's tribute is ９９９９９９ gold coins. Please accept it."
    assert result['caller_lookup_formatter_and_hook_share_one_machine']
