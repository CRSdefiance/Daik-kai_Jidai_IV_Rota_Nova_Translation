"""Bind the directly viewed Lil261 emulator sample and its native returns."""

from scripts.approve_lil254_actual_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    "work/Lil254_B312_B319_clean_20261110": "work/Lil261_B323_B335_clean_20261110",
    "Lil254_wolf_ruins_trade": "Lil261_fog_cave_commission_alchemy",
    "formatting_v2/formatting_input.json": "formatting_v1/formatting_input.json",
    "{(312, 754): [1, 2], (314, 684): [0, 1], (316, 812): [0, 1]}": "{(323, 674): [1], (323, 934): [0, 1], (324, 758): [1]}",
    "len(receipt['sheets']) == 5": "len(receipt['sheets']) == 6",
    "(53, 58, 58, 25841)": "(58, 61, 61, 26561)",
    "len(set(byid) - observed) == 193 and len(styles) == 4 and len(captions) == 8": "len(set(byid) - observed) == 197 and len(styles) == 4 and len(captions) == 6",
    "len(turns) == 5 and len(FE_returns) == 7 and len(sheets) == 7": "len(turns) == 3 and len(FE_returns) == 13 and len(sheets) == 8",
    "    assert 'DK4_MES_B316_R0205' in {r['id'] for r in FE_returns}\n    assert {'DK4_MES_B317_R0030', 'DK4_MES_B317_R0043', 'DK4_MES_B319_R0008'} <= observed\n    assert any(h['source_selector'] == 0 and h['text'] == 'Rafael Castor' for h in headers)": "    assert {r['id'] for r in turns} == {'DK4_MES_B327_R0025', 'DK4_MES_B331_R0024', 'DK4_MES_B335_R0013'}\n    assert {r['id'] for r in FE_returns} == {r['id'] for r in byid.values() if r['kind'] == 'system-FE'}\n    for actor, name in [(18, 'Charles Rochefort'), (147, 'Guildmaster')]:\n        assert any(h['expected_actor_ID'] == actor and h['text'] == name for h in headers)",
    "frames=25841, initialized_runs=1": "frames=26561, initialized_runs=1",
    "distinct_source_body_objects=53": "distinct_source_body_objects=58",
    "observed_pages_including_repeats=58, distinct_body_pages=58, offline_only_source_body_objects=193": "observed_pages_including_repeats=61, distinct_body_pages=61, offline_only_source_body_objects=197",
    "actual_caption_strings=8": "actual_caption_strings=6",
    "repaired_B316_alert_and_B319_company_substitution_observed=True, both_B317_source_selector_00_headers_observed=True": "all_thirteen_FE_returns_observed=True, scoped_Guildmaster_and_Charles_headers_observed=True",
    "PASS 53 bodies, 58 pages, five turns, seven FE returns, three menus, and seven directly viewed sheets. 193 bodies remain offline-only.": "PASS 58 bodies, 61 pages, three turns, 13 FE returns, three menus and eight directly viewed sheets. 197 bodies remain offline-only.",
})


if __name__ == '__main__':
    exec(compile(source, __file__, 'exec'), globals())
