"""Preserve exact initialized pixel/input guards for the disclosed363 sample."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/approve_maria305_actual_v1.py').read_text(encoding='utf-8'), {
    'Maria_B176_B195_clean_20261110': 'Maria_B216_B252_clean_20261110',
    'formatting_v1/formatting_input.json': 'formatting_v1/formatting_input_v2.json',
    "['Maria305_random_trade_menu0', 'Maria305_letters_refusal_menu1', 'Maria305_armor_glyphs_menu2']":
        "['Maria363_towns_take_Plett_scare_menu0', 'Maria363_refusal_riddle_left_sleep_menu1', 'Maria363_guilds_riddle_right_forest_other_menu2']",
    "ROOT/f'actual_menus{index}_v1/menu_actual_pixels.json'": "ROOT/f'actual_menus{index}_v{2 if index == 2 else 1}/menu_actual_pixels.json'",
    "assert actual_menu['ordinary_A_return_to_next_fixture_speech_observed']":
        """if index == 2:
            assert actual_menu['ordinary_A_returns_to_next_menu_or_fixture_speech_observed']
            assert not actual_menu['ordinary_A_return_to_next_fixture_speech_observed']
            assert actual_menu['consecutive_menu_transition']
        else:
            assert actual_menu['ordinary_A_return_to_next_fixture_speech_observed']""",
    '[7, 3, 3][index]': '[8, 7, 9][index]',
    '(127, 135, 132, 63843)': '(252, 273, 254, 97683)',
    'len(body_ids-observed_bodies) == 167 and len(observed_style_ids) == 3':
        'len(body_ids-observed_bodies) == 99 and len(observed_style_ids) == 10',
    '(3, 7, 5)': '(5, 12, 2)',
    'states[(185, 242)] == {0, 1, 2} and states[(179, 990)] == {0, 1} and states[(179, 818)] == {0}':
        'states == {(220,404):{0,1}, (221,270):{0,1,2}, (221,1622):{0,1}, (252,882):{0,1,2}, (252,1876):{0,1}}',
    "{'DK4_MES_B177_R0066', 'DK4_MES_B188_R0047', 'DK4_MES_B185_R0071', 'DK4_MES_B195_R0004'}":
        "{'DK4_MES_B221_R0008', 'DK4_MES_B221_R0011', 'DK4_MES_B221_R0183', 'DK4_MES_B242_R0011', 'DK4_MES_B247_R0060'}",
    'assert len(FE_returns) == len(FE_ids)': 'assert len(FE_returns) == 34 and len(FE_ids) == 32 and {r[\'id\'] for r in FE_returns} == FE_ids',
    'dict(frames=63843, initialized_runs=3': 'dict(frames=97683, initialized_runs=3',
    'distinct_source_body_objects=127, observed_pages_including_repeats=135, distinct_body_pages=132':
        'distinct_source_body_objects=252, observed_pages_including_repeats=273, distinct_body_pages=254',
    'offline_only_source_body_objects=167': 'offline_only_source_body_objects=99',
    'actual_caption_strings=7, offline_only_caption_strings=4': 'actual_caption_strings=12, offline_only_caption_strings=0',
    'actual_menus=3': 'actual_menus=5',
    '''        all135_actual_pages_seven_captions_andthree_host_transitions_directly_viewed=True,
        all_selected_current_pages_match_current_compiled_native_planes=True,
        all_five_two_page_turns_andfollowing_calls_observed=True,
        all_three_style_objects_current_voice4_observed_other19_physical_alternatives_offline_only=True,
        repaired_B177_FE_panel_complete_andnormal_A_return_observed=True,
        both_fullwidth_I_replacements_original_FA_andGuan_Yu_translation_observed=True,
        parrot_complete_echo_exchange_andEmilio_first_person_replies_observed=True,
        both_letter_page_turns_signatures_andSailor_headers_observed=True,''':
    '''        all273_actual_pages_twelve_captions_andthree_host_transitions_directly_viewed=True,
        all_selected_current_pages_match_current_compiled_native_planes=True,
        both_two_page_turns_andfollowing_calls_observed=True,
        ten_style_objects_current_voice4_observed_other75_physical_alternatives_offline_only=True,
        repaired_three_FE_panels_complete_andnormal_A_returns_observed=True,
        consecutive_menu_return_andboth_A_inputs_observed=True,
        restored_Jacob_reply_andWilliam_second_page_observed=True,
        runtime_selector216_only_offline_bound_andrendered=True,''',
    '''contextual_layout_retentions=[dict(id='DK4_MES_B182_R0026',
            reason='Retain the automatic short formal opening: the next complete opening phrase is36 ASCII cells, exceeding this indented35-cell row. Full prose, bane of Tokugawa and leader of Japan remain intact within two pages; forcing joins worsens the boundary. This is not an authored dramatic break.')],''':
    '''contextual_layout_retentions=[dict(id='DK4_MES_B234_R0037',
            reason='Retain the complete question Where are you from? as one phrase; source-bound formatter preference preserves prose and all native bounds without shortening.')],''',
    "str(Path(__file__)):digest(Path(__file__))}": "str(Path(__file__)):digest(Path(__file__)), 'scripts/approve_maria305_actual_v1.py':digest('scripts/approve_maria305_actual_v1.py')}",
    'Approved127 actual bodies/132 unique pages/135 observed pages,7 captions,5 page turns and3 sailing returns;167 bodies offline-only.':
        'Approved252 actual bodies/254 unique pages/273 observed pages,12 captions,2 page turns and3 sailing returns;99 bodies offline-only.',
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-complete-pixel-input-andtransition-guards-current-sample', 'exec'), globals())
