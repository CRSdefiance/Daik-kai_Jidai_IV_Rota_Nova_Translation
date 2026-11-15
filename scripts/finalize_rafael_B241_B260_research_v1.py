"""Seal the 292 B241–B260 research gates against stored and emulator evidence."""
from pathlib import Path

from scripts import finalize_rafael_B221_B240_research_v1 as prior
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(Path(prior.__file__).read_text(encoding='utf-8'), {
    'assemble_rafael_B221_B240_offline_v2': 'assemble_rafael_B241_B260_offline_v2',
    'seal_rafael_B221_B240_visual_v1': 'seal_rafael_B241_B260_visual_v1',
    'from scripts.write_rafael_B221_B240_contextual_v1 import LABELS, digest':
        'from scripts.write_rafael_B241_B260_contextual_v1 import LABELS\nfrom scripts.assemble_rafael_B241_B260_offline_v2 import digest',
    'rebuilt_research_v1/': 'reconstruction_v1/',
    'stored_native_v1/': 'stored_v1/',
    'all263_stored_effective_body_bindings.json': 'all286_stored_effective_body_bindings.json',
    "MENU_ACTUAL = ROOT / 'actual_menus_v1/menu_actual_pixels.json'":
        """MENU_ACTUAL = [ROOT / folder / 'menu_actual_pixels.json'
               for folder in ('actual_rose_menu_v1', 'actual_figurehead_menus_v1')]
FRANCISCA = ROOT / 'Francisca_name_field_v1/native/native_name_fields_verification.json'""",
    'rafael_B221_B240_final_review_v1.json': 'rafael_B241_B260_final_review_v1.json',
    'rafael_B221_B240_scoped_names_final_v1.json': 'rafael_B241_B260_scoped_names_final_v1.json',
    "RUNS = (('rafael_letters_swans_and_names', 51, 55, 18161), ('rafael_books_guard_and_town', 35, 39, 15041))":
        """RUNS = (('rafael_letters_and_ruins_greeting', 38, 40, 14561),
        ('rafael_frozen_rose_town_exchange', 42, 42, 15281),
        ('rafael_two_figureheads', 52, 53, 18161))""",
    "ROOT/f'actual_fixtures_v1/": "ROOT/f'fixtures_v1/",
    "        actors.update(row['expected_actor_ID'] for row in proof['headers'])":
        """        actors.update(row['expected_actor_ID'] for row in proof['headers'])
        if name == 'rafael_frozen_rose_town_exchange':
            assert fixture['verified_Francisca_field_applied']
            assert fixture['Francisca_name_proof_sha256'] == digest(FRANCISCA)
            headers = [row for row in proof['headers'] if row['expected_actor_ID'] == 186]
            assert headers and all(row['text'] == 'Francisca' for row in headers)
            ellipses = {row['id'] for row in proof['body_pages'] if row.get('ellipsis_shadow')}
            assert ellipses == {'DK4_MES_B251_R0020', 'DK4_MES_B251_R0039'}""",
    "== (94, 16, 4, 7)": "== (135, 13, 2, 10)",
    "len({ident for ident, _ in found}) == 86": "len({ident for ident, _ in found}) == 132",
    "LOADERS, VISUAL, MENU_ACTUAL, FINAL_MANUSCRIPT": "LOADERS, VISUAL, *MENU_ACTUAL, FRANCISCA, FINAL_MANUSCRIPT",
    "rebuilt, stored, lookup, loaders, visual, live_menus, doc, plan, native, menu, styles, names = map(load, paths)":
        """rebuilt, stored, lookup, loaders, visual, rose_menus, figures_menus, name_proof, doc, plan, native, menu, styles, names = map(load, paths)
    assert name_proof['original_progressive_andfull_name_getters_pass']
    required = ('ordinary_A_return_to_next_fixture_speech_observed',
                'observed_each_menu_between_its_own_exact_preceding_and_following_speech',
                'all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches')
    live_menus = {key: all(m[key] for m in (rose_menus, figures_menus)) for key in required}
    live_menus['menus'] = rose_menus['menus'] + figures_menus['menus']
    live_menus['complete_live_caption_samples'] = sum(m['complete_live_caption_samples'] for m in (rose_menus, figures_menus))
    menu_sheets = [m['review_sheet'] for m in (rose_menus, figures_menus)]""",
    'all263_ordinary_and_style_bodies_checked': 'all286_ordinary_and_style_bodies_checked',
    '== (234, 29, 263)': '== (272, 14, 286)',
    '== (279, 127, 152, 170)': '== (294, 128, 166, 120)',
    '== (343, 38, 648)': '== (343, 36, 650)',
    "== [231] and len(rebuilt['changed_blocks']) == 19": "== [244] and len(rebuilt['changed_blocks']) == 18",
    'len(captions) == 7': 'len(captions) == 6',
    "visual['scoped_name_count'] == 26": "visual['scoped_name_count'] == 20",
    "for row in stored['style_records']}) == 4": "for row in stored['style_records']}) == 2",
    "assert digest(Path(live_menus['review_sheet']['path'])) == live_menus['review_sheet']['sha256']":
        "assert all(digest(Path(sheet['path'])) == sheet['sha256'] for sheet in menu_sheets)",
    "{'DK4_MES_B224_R0072', 'DK4_MES_B227_R0019', 'DK4_MES_B223_R0017'}":
        "{'DK4_MES_B259_R0006', 'DK4_MES_B247_R0050', 'DK4_MES_B248_R0049', 'DK4_MES_B251_R0012'}",
    "{'revision': 221, 'retention': 49}": "{'revision': 244, 'retention': 48}",
    "actual_header_observed_in_disclosed_fixture=row['actor_ID'] in actors)":
        """actual_header_observed_in_disclosed_fixture=row['actor_ID'] in actors)
        if row['actor_ID'] == 186:
            row.update(exclusive_field_native_and_progressive_fixture_pass=True, registered_name_field_pending=True)""",
    "actual_sheets + [live_menus['review_sheet']]": "actual_sheets + menu_sheets",
    "body_pages=279, observed_pages=94, reviewed_caption_planes=28, scoped_public_names=26, typed_labels=7":
        "body_pages=294, observed_pages=135, reviewed_caption_planes=24, scoped_public_names=20, typed_labels=6",
    'total_frames=33202, initialized_fixture_runs=2, source_speech_variants_observed=86':
        'total_frames=48003, initialized_fixture_runs=3, source_speech_variants_observed=132',
    'native_body_pages_observed=94, actual_choice_labels=7, offline_only_speech_variants=177':
        'native_body_pages_observed=135, actual_choice_labels=6, offline_only_speech_variants=154',
    'all_four_complete_style_commands_observed_under_unmodified_default_roles=True':
        'both_complete_style_commands_observed_under_unmodified_default_roles=True',
    'native_body_pages=279, actual_source_speech_variants=86, actual_body_pages=94':
        'native_body_pages=294, actual_source_speech_variants=132, actual_body_pages=135',
    'offline_only_source_speech_variants=177': 'offline_only_source_speech_variants=154',
    'records=270, revisions=221, retentions=49, body_pages=279, typed_labels=7, scoped_public_names=26':
        'records=292, revisions=244, retentions=48, body_pages=294, typed_labels=6, scoped_public_names=20',
    'actual_source_variants=86, actual_pages=94, actual_choice_labels=7':
        'actual_source_variants=132, actual_pages=135, actual_choice_labels=6',
    'actual_name_headers=16, offline_only_source_variants=177, registered_integration_pending=True':
        'actual_name_headers=13, offline_only_source_variants=154, registered_integration_pending=True',
    'Sealed 270 five-gate reviews, 279 offline and stored pages, and 94 focused emulator pages.':
        'Sealed 292 five-gate reviews, 294 offline and stored pages, and 135 focused emulator pages.',
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-five-gates-with-exact-current-evidence', 'exec'), globals())
