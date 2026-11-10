"""Keep exact actual pixel/menu/input guards for the disclosed321-record sample."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/approve_maria305_actual_v1.py').read_text(encoding='utf-8'), {
    "Path('work/Maria_B176_B195_clean_20261110')": "Path('work/Maria_B196_B215_clean_20261110')",
    "['Maria305_random_trade_menu0', 'Maria305_letters_refusal_menu1', 'Maria305_armor_glyphs_menu2']":
        "['Maria321_letters_training_attempt_menu0', 'Maria321_Francisca_recovery_menu0', 'Maria321_Jam_figurehead_refusal_menu1']",
    '[7, 3, 3][index]': '[7, 6, 3][index]',
    '(127, 135, 132, 63843)': '(156, 178, 162, 73443)',
    'len(body_ids-observed_bodies) == 167 and len(observed_style_ids) == 3':
        'len(body_ids-observed_bodies) == 161 and len(observed_style_ids) == 2',
    '(3, 7, 5)': '(2, 4, 6)',
    'states[(185, 242)] == {0, 1, 2} and states[(179, 990)] == {0, 1} and states[(179, 818)] == {0}':
        'states[(215, 716)] == {0, 1} and states[(212, 492)] == {0}',
    "{'DK4_MES_B177_R0066', 'DK4_MES_B188_R0047', 'DK4_MES_B185_R0071', 'DK4_MES_B195_R0004'}":
        "{'DK4_MES_B200_R0015', 'DK4_MES_B198_R0004', 'DK4_MES_B198_R0008', 'DK4_MES_B209_R0045', 'DK4_MES_B215_R0086', 'DK4_MES_B214_R0016', 'DK4_MES_B212_R0094'}",
    'assert len(FE_returns) == len(FE_ids)':
        "assert len(FE_returns) == len(FE_ids) == 1 and FE_ids == {'DK4_MES_B214_R0016'}",
    'dict(frames=63843, initialized_runs=3': 'dict(frames=73443, initialized_runs=3',
    'distinct_source_body_objects=127, observed_pages_including_repeats=135, distinct_body_pages=132':
        'distinct_source_body_objects=156, observed_pages_including_repeats=178, distinct_body_pages=162',
    'offline_only_source_body_objects=167': 'offline_only_source_body_objects=161',
    'actual_caption_strings=7, offline_only_caption_strings=4':
        'actual_caption_strings=4, offline_only_caption_strings=0',
    'actual_menus=3': 'actual_menus=2',
    '''        all135_actual_pages_seven_captions_andthree_host_transitions_directly_viewed=True,
        all_selected_current_pages_match_current_compiled_native_planes=True,
        all_five_two_page_turns_andfollowing_calls_observed=True,
        all_three_style_objects_current_voice4_observed_other19_physical_alternatives_offline_only=True,
        repaired_B177_FE_panel_complete_andnormal_A_return_observed=True,
        both_fullwidth_I_replacements_original_FA_andGuan_Yu_translation_observed=True,
        parrot_complete_echo_exchange_andEmilio_first_person_replies_observed=True,
        both_letter_page_turns_signatures_andSailor_headers_observed=True,''':
    '''        all178_actual_pages_four_captions_andthree_host_transitions_directly_viewed=True,
        all_selected_current_pages_match_current_compiled_native_planes=True,
        all_six_two_page_turns_andfollowing_calls_observed=True,
        two_style_objects_current_voice4_observed_other19_physical_alternatives_offline_only=True,
        Frozen_Rose_FE_complete_andnormal_A_return_observed=True,
        repaired_strength_of_mind_page_andreclaimed_Jam_page_observed=True,
        Boy_andSailor_headers_andcorrected_Julio_departure_instruction_observed=True,
        Ian_andJam_letters_signatures_andscoped_name_headers_observed=True,
        figurehead_success_andFI_Spirit_panel_offline_only=True,''',
    '''contextual_layout_retentions=[dict(id='DK4_MES_B182_R0026',
            reason='Retain the automatic short formal opening: the next complete opening phrase is36 ASCII cells, exceeding this indented35-cell row. Full prose, bane of Tokugawa and leader of Japan remain intact within two pages; forcing joins worsens the boundary. This is not an authored dramatic break.')],''':
    '''contextual_layout_retentions=[dict(id='DK4_MES_B196_R0027',
            reason='Retain the three balanced book-introduction rows: extending the first through intriguing takes36 cells plus the required parity reserve and exceeds the validated first-row budget. The alternative article-ending break is worse. Preserve all prose and native guards; no dramatic break is authored.')],''',
    "str(Path(__file__)):digest(Path(__file__))}":
        "str(Path(__file__)):digest(Path(__file__)), 'scripts/approve_maria305_actual_v1.py':digest('scripts/approve_maria305_actual_v1.py')}",
    'Approved127 actual bodies/132 unique pages/135 observed pages,7 captions,5 page turns and3 sailing returns;167 bodies offline-only.':
        'Approved156 actual bodies/162 unique pages/178 observed pages,4 captions,6 page turns and3 sailing returns;161 bodies offline-only.',
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-actual-ordered-pixels-controls-menu-andtransition-guards-current-sample', 'exec'), globals())
